# -*- coding: utf-8 -*-
"""
engine/crew/publisher.py
------------------------
Google Blogger API v3 게이트웨이 및 내부 사일로 DB(published_posts.json) 동기화기
- 검증 완료된 HTML 및 호스팅된 썸네일 URL을 결합하여 Blogger에 안전 배포
- 발행 즉시 published_posts.json에 메타데이터를 저장하여 차기 포스트의 내부 링크(Internal Silo) 소스로 제공
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
CREDS_PATH = os.path.join(BASE_DIR, "credentials.json")
PUBLISHED_DB_PATH = os.path.join(BASE_DIR, "data", "published_posts.json")
SCOPES = ['https://www.googleapis.com/auth/blogger']


class MicroSaaSBloggerPublisher:
    def __init__(self, blog_id: Optional[str] = None):
        self.blog_id = blog_id or os.getenv("BLOGGER_BLOG_ID", "2002031376804677477")
        self.published_db_path = PUBLISHED_DB_PATH
        self._ensure_db()

    def _ensure_db(self):
        os.makedirs(os.path.dirname(self.published_db_path), exist_ok=True)
        if not os.path.exists(self.published_db_path):
            with open(self.published_db_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _get_authenticated_service(self):
        creds = None
        if os.path.exists(TOKEN_PATH):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
            except Exception as e:
                print(f"[Publisher] token.json 로드 실패: {e}")

        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
                print("[Publisher] OAuth2 액세스 토큰 자동 갱신 완료.")
            except Exception as e:
                print(f"[Publisher] 토큰 갱신 실패: {e}")
                creds = None

        if not creds or not creds.valid:
            if not os.path.exists(CREDS_PATH):
                print(f"[Publisher] credentials.json 파일을 찾을 수 없습니다: {CREDS_PATH}")
                return None
            try:
                from google_auth_oauthlib.flow import InstalledAppFlow
                print("\n" + "═" * 78)
                print(" 🔑 [Google Blogger 재인증] 기존 인증 토큰(token.json)이 만료되었습니다.")
                print("    웹 브라우저가 열리면 Google 계정으로 로그인 후 [허용]을 클릭하십시오...")
                print("═" * 78 + "\n")
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(TOKEN_PATH, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
                print(" -> [Publisher] 새 OAuth2 토큰 발급 및 token.json 갱신 완료!\n")
            except Exception as auth_err:
                print(f"[Publisher] 브라우저 OAuth2 로그인 실패: {auth_err}")
                return None

        return build('blogger', 'v3', credentials=creds)

    def publish_post(self, title: str, html_content: str, thumbnail_url: str, keyword: str, labels: list = None, dry_run: bool = False, english_slug: str = None) -> Dict[str, Any]:
        """
        Blogger API v3를 통한 포스트 안전 배포
        - [2-Step SEO Slug Reservation]: 최초 영문 슬러그로 insert하여 깨끗한 영문 URL 영구 확보 후 한글 타이틀 덮어쓰기
        - 썸네일 배너 본문 삽입 (블로거 대표 이미지 강제 인식)
        - published_posts.json에 발행 메타데이터 영구 기록
        """
        # [Patch 3] 본문 최상단에 호스팅된 썸네일 이미지 배너 결합 (Blogger OG 이미지 추출용)
        banner_html = f"""
<div class="blogin-thumbnail-banner" style="margin-bottom: 24px; text-align: center;">
  <img src="{thumbnail_url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 14px; box-shadow: 0 8px 30px rgba(0,0,0,0.15); display: inline-block;" />
</div>
"""
        final_html = banner_html + html_content
        post_labels = labels or ["세금·절세 시뮬레이터", "핀테크 계산기"]

        if dry_run or not os.path.exists(TOKEN_PATH):
            print(" -> [Publisher] DRY-RUN 모드 또는 인증키 부재: 로컬 발행 시뮬레이션 실행")
            sim_slug = english_slug if english_slug else f"preview-microsaas-{int(time.time())}"
            simulated_url = f"https://blogin365ai.blogspot.com/{sim_slug}.html"
            record = {
                "id": f"sim-{int(time.time())}",
                "title": title,
                "keyword": keyword,
                "url": simulated_url,
                "thumbnail_url": thumbnail_url,
                "published_at": datetime.now().isoformat(),
                "status": "SIMULATED_SUCCESS"
            }
            self._record_published_post(record)
            return record

        try:
            service = self._get_authenticated_service()
            if not service:
                raise RuntimeError("Blogger API 인증 세션 생성 실패")

            # [Step 1: Clean English Slug 확보를 위한 1차 Insert]
            initial_title = english_slug.strip() if english_slug and english_slug.strip() else title
            body = {
                "kind": "blogger#post",
                "blog": {"id": self.blog_id},
                "title": initial_title,
                "content": final_html,
                "labels": post_labels
            }

            post = service.posts().insert(blogId=self.blog_id, body=body, isDraft=False).execute()
            pub_url = post.get("url")
            post_id = post.get("id")
            print(f" -> [Publisher] 1단계 Blogger 실발행 성공 (영문 슬러그 확보)! URL: {pub_url}")

            # [Step 2: 영문 퍼머링크 보존 상태에서 정식 한글 타이틀 즉시 Update]
            if english_slug and initial_title != title:
                time.sleep(0.5)
                update_body = {
                    "kind": "blogger#post",
                    "id": post_id,
                    "blog": {"id": self.blog_id},
                    "title": title,
                    "content": final_html,
                    "labels": post_labels
                }
                updated_post = service.posts().update(blogId=self.blog_id, postId=post_id, body=update_body).execute()
                pub_url = updated_post.get("url") or pub_url
                print(f" -> [Publisher] 2단계 정식 한글 타이틀 업데이트 완료 (영문 URL 보존): {title}")

            record = {
                "id": post_id,
                "title": title,
                "keyword": keyword,
                "url": pub_url,
                "thumbnail_url": thumbnail_url,
                "published_at": datetime.now().isoformat(),
                "status": "LIVE_PUBLISHED"
            }
            self._record_published_post(record)
            return record

        except Exception as e:
            print(f" -> [Publisher] Blogger 발행 에러 발생: {e}")
            return {
                "success": False,
                "error": str(e),
                "status": "FAILED"
            }

    def update_post(self, post_id: str, title: str, html_content: str, thumbnail_url: str, keyword: str, labels: list = None) -> Dict[str, Any]:
        """
        Blogger API의 posts().update()를 사용하여 기존 포스트의 본문, 썸네일, 라벨을 덮어쓰기(Update)
        """
        banner_html = f"""
<div class="blogin-thumbnail-banner" style="margin-bottom: 24px; text-align: center;">
  <img src="{thumbnail_url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 14px; box-shadow: 0 8px 30px rgba(0,0,0,0.15); display: inline-block;" />
</div>
"""
        final_html = banner_html + html_content
        post_labels = labels or ["세금·절세 시뮬레이터", "핀테크 계산기"]

        try:
            service = self._get_authenticated_service()
            if not service:
                raise RuntimeError("Blogger API 인증 세션 생성 실패")

            body = {
                "kind": "blogger#post",
                "id": post_id,
                "blog": {"id": self.blog_id},
                "title": title,
                "content": final_html,
                "labels": post_labels
            }

            updated_post = service.posts().update(blogId=self.blog_id, postId=post_id, body=body).execute()
            pub_url = updated_post.get("url")
            print(f" -> [Publisher] Blogger 포스트(ID: {post_id}) 업데이트 성공! URL: {pub_url}")

            record = {
                "id": post_id,
                "title": title,
                "keyword": keyword,
                "url": pub_url,
                "thumbnail_url": thumbnail_url,
                "updated_at": datetime.now().isoformat(),
                "status": "LIVE_UPDATED"
            }
            self._update_recorded_post(record)
            return record

        except Exception as e:
            print(f" -> [Publisher] Blogger 업데이트 에러 발생 (Post ID: {post_id}): {e}")
            return {
                "success": False,
                "id": post_id,
                "error": str(e),
                "status": "FAILED"
            }

    def _update_recorded_post(self, record: dict):
        try:
            with open(self.published_db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            updated = False
            for idx, p in enumerate(data):
                if str(p.get("id")) == str(record.get("id")) or p.get("url") == record.get("url"):
                    data[idx].update(record)
                    updated = True
                    break
            if not updated:
                data.insert(0, record)
            with open(self.published_db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f" -> [Publisher] 사일로 DB(published_posts.json) 포스트 갱신 완료")
        except Exception as e:
            print(f" -> [Publisher] DB 갱신 경고: {e}")

    def _record_published_post(self, record: dict):
        try:
            with open(self.published_db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.insert(0, record)
            data = data[:100]  # 최근 100건 보존
            with open(self.published_db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f" -> [Publisher] 사일로 DB(published_posts.json) 동기화 완료 ({len(data)}건 누적)")
        except Exception as e:
            print(f" -> [Publisher] DB 저장 경고: {e}")
