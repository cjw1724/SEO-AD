import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Blogger API 권한 범위
SCOPES = ['https://www.googleapis.com/auth/blogger']

class PublisherAgent:
    def __init__(self):
        self.blog_id = os.getenv("BLOGGER_BLOG_ID")
        self.creds = None
        self._authenticate()

    def _get_token_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(current_dir, "..", "..", "token.json"),
            os.path.join(current_dir, "..", "token.json"),
            os.path.join(os.getcwd(), "token.json"),
            "token.json"
        ]
        for c in candidates:
            c_norm = os.path.normpath(c)
            if os.path.exists(c_norm):
                return c_norm
        return os.path.normpath(candidates[0])

    def _get_creds_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(current_dir, "..", "..", "credentials.json"),
            os.path.join(current_dir, "..", "credentials.json"),
            os.path.join(os.getcwd(), "credentials.json"),
            "credentials.json"
        ]
        for c in candidates:
            c_norm = os.path.normpath(c)
            if os.path.exists(c_norm):
                return c_norm
        return os.path.normpath(candidates[0])

    def _authenticate(self):
        """Google Blogger API 인증을 수행합니다."""
        token_path = self._get_token_path()
        creds_path = self._get_creds_path()

        if os.path.exists(token_path):
            try:
                self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                print(f"⚠️ token.json 로드 실패: {e}")
            
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"⚠️ 토큰 갱신 실패: {e}")
            else:
                if not os.path.exists(creds_path):
                    print("⚠️ credentials.json 파일이 없습니다! 구글 클라우드 콘솔에서 발급받아야 합니다.")
                    return
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            if self.creds:
                with open(token_path, 'w', encoding='utf-8') as token:
                    token.write(self.creds.to_json())

    def publish(self, article):
        """Blogger에 글을 발행합니다."""
        if not self.creds:
            print("❌ Blogger API 인증이 되어있지 않아 발행할 수 없습니다.")
            return False
            
        if not self.blog_id:
            print("❌ .env 파일에 BLOGGER_BLOG_ID가 설정되어 있지 않습니다.")
            return False

        try:
            service = build('blogger', 'v3', credentials=self.creds)
            
            body = {
                "kind": "blogger#post",
                "title": article['title'],
                "content": article['content'],
                "labels": article.get('tags', [])
            }
            
            print(f"📡 [구글 블로거 API 호출 중...] 제목: {article['title']}")
            posts = service.posts()
            result = posts.insert(blogId=self.blog_id, body=body, isDraft=False).execute()
            
            url = result.get('url')
            print(f"✅ 글 발행 완료! URL: {url}")
            return url
            
        except Exception as e:
            print(f"❌ 발행 중 오류 발생: {e}")
            return False

    def update(self, post_id: str, article: dict):
        """Blogger의 기존 글을 업데이트합니다."""
        if not self.creds:
            print("❌ Blogger API 인증이 되어있지 않아 업데이트할 수 없습니다.")
            return False
            
        if not self.blog_id:
            print("❌ .env 파일에 BLOGGER_BLOG_ID가 설정되어 있지 않습니다.")
            return False

        try:
            service = build('blogger', 'v3', credentials=self.creds)
            
            body = {
                "kind": "blogger#post",
                "id": post_id,
                "title": article['title'],
                "content": article['content'],
                "labels": article.get('tags', [])
            }
            
            print(f"📡 [구글 블로거 API 업데이트 호출 중...] ID: {post_id}, 제목: {article['title']}")
            posts = service.posts()
            result = posts.update(blogId=self.blog_id, postId=post_id, body=body).execute()
            
            url = result.get('url')
            print(f"✅ 글 업데이트 완료! URL: {url}")
            return url
            
        except Exception as e:
            print(f"❌ 업데이트 중 오류 발생: {e}")
            return False
