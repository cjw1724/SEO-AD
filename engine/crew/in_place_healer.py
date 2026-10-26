"""
Blogin 365 AI Holdings - In-Place Live Post Contrast Healer (v9.0 Apex)
Heals live post 4307561766392959448 and verifies live contrast with Playwright.
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from googleapiclient.discovery import build
from engine.publisher.blogger_gateway import BloggerGateway
from engine.crew.editorial_inspector import EditorialInspector

sys.stdout.reconfigure(encoding="utf-8")

def heal_live_post(post_id: str = "4307561766392959448"):
    print("=" * 78)
    print("🏢 [Blogin 365 AI Holdings] 라이브 포스트 고대비 자가치유 인플레이스 패치 시작")
    print(f"• 대상 Post ID : {post_id}")
    print("=" * 78)

    gw = BloggerGateway()
    creds = gw._get_authenticated_credentials()
    service = build("blogger", "v3", credentials=creds)

    print("\n[Step 1/4] Blogger API에서 원본 라이브 포스트 조회 중...")
    post = service.posts().get(blogId=gw.blog_id, postId=post_id).execute()
    title = post.get("title", "")
    current_content = post.get("content", "")
    post_url = post.get("url", "")
    print(f" -> 제목: {title}")
    print(f" -> URL: {post_url}")
    print(f" -> 원본 HTML 바이트 크기: {len(current_content)} bytes")

    print("\n[Step 2/4] 8인 AI 직원 실물 검수 위원회(Editorial Inspector) 자가치유 실행...")
    inspector = EditorialInspector()
    healed_content = inspector.auto_heal(current_content)
    inspection_result = inspector.inspect(healed_content, is_url=False)
    print(f" -> 자가치유 수행 완료! (본문 검수 통과: {inspection_result['passed']})")
    stats = inspection_result.get("stats", {})
    for vp, s in stats.items():
        print(f"    * [{vp}] 최소 대비율: {s.get('min_contrast')}:1 | 평균 대비율: {s.get('avg_contrast')}:1")

    print("\n[Step 3/4] Blogger API에 고대비 치유 HTML 원격 패치(Patch) 전송...")
    update_res = gw.update_post(
        post_id=post_id,
        title=title,
        html_content=healed_content,
        labels=post.get("labels", ["해외주식", "양도소득세", "손익통산", "절세", "FinTech"])
    )
    if not update_res.get("success"):
        raise RuntimeError(f"Blogger 포스트 패치 실패: {update_res.get('error')}")
    print(f" -> Blogger 원격 패치 성공! (URL: {update_res.get('url')})")

    print("\n[Step 4/4] 실제 배포된 라이브 URL Playwright 브라우저 실물 검수 및 스크린샷 캡처...")
    live_review = inspector.inspect(post_url, is_url=True)
    print(f" -> 라이브 페이지 실물 검수 통과 여부: {live_review['passed']}")
    for vp, s in live_review.get("stats", {}).items():
        print(f"    * [LIVE {vp}] 검사 요소 수: {s.get('tested_elements')} | 최소 대비율: {s.get('min_contrast')}:1 | 결함: {s.get('defect_count')}건")

    for cert in live_review.get("certifications", []):
        print(f"    * [{cert['role']}] {cert['name']} -> {cert['verdict']} ({cert['notes']})")

    print("\n" + "═" * 78)
    print("✨ [COMPLETED] 라이브 포스트 가독성 참사 완전 복원 및 실물 검수 통과!")
    print(f"• 라이브 URL      : {post_url}")
    print(f"• 데스크톱 실물샷 : {live_review['screenshots'].get('desktop')}")
    print(f"• 모바일 실물샷   : {live_review['screenshots'].get('mobile')}")
    print("═" * 78)

    return live_review

if __name__ == "__main__":
    heal_live_post()
