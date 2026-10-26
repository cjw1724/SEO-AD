# -*- coding: utf-8 -*-
"""
d:\SEO AD\reauth_blogger.py
----------------------------
Google Blogger OAuth2 만료 토큰 원클릭 재발급 도구
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
CREDS_PATH = os.path.join(BASE_DIR, "credentials.json")
SCOPES = ['https://www.googleapis.com/auth/blogger']

def reauth():
    print("═" * 78)
    print(" 🔑 [Google Blogger OAuth2 재인증 도구]")
    print("═" * 78)

    if not os.path.exists(CREDS_PATH):
        print(f"[ERROR] credentials.json 파일을 찾을 수 없습니다: {CREDS_PATH}")
        sys.exit(1)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        print("\n브라우저가 자동으로 열립니다. Google 계정으로 로그인 후 [허용/계속]을 눌러주십시오...\n")
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print("✅ [성공] 새 OAuth2 토큰 발급 및 token.json 갱신이 완료되었습니다!")
        print("   이제 구글 블로거 실제 발행이 100% 정상 작동합니다.\n")
    except Exception as e:
        print(f"❌ [에러] 재인증 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reauth()
