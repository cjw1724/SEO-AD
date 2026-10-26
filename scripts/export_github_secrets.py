# -*- coding: utf-8 -*-
"""
scripts/export_github_secrets.py
---------------------------------
Formats and displays the 5 required GitHub Secrets for:
https://github.com/cjw1724/SEO-AD/settings/secrets/actions
"""

import os
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import json
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "SEO.env"))

def export_secrets():
    print("═" * 78)
    print("  🔑 [GitHub Actions Secrets 복사 도우미]")
    print("  아래 5개 비밀키를 복사하여 다음 주소에 등록하십시오:")
    print("  👉 https://github.com/cjw1724/SEO-AD/settings/secrets/actions")
    print("═" * 78)

    # 1. OPENROUTER_API_KEY
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    print("\n[1] Secret 이름: OPENROUTER_API_KEY")
    print("─" * 78)
    print(openrouter_key)
    print("─" * 78)

    # 2. BLOGGER_BLOG_ID
    blog_id = os.getenv("BLOGGER_BLOG_ID", "2002031376804677477")
    print("\n[2] Secret 이름: BLOGGER_BLOG_ID")
    print("─" * 78)
    print(blog_id)
    print("─" * 78)

    # 3. GOOGLE_CSE_CX
    cse_cx = os.getenv("GOOGLE_CSE_CX", "863c2f0c96b064551")
    print("\n[3] Secret 이름: GOOGLE_CSE_CX")
    print("─" * 78)
    print(cse_cx)
    print("─" * 78)

    # 4. BLOGGER_CREDENTIALS_JSON
    creds_path = os.path.join(BASE_DIR, "credentials.json")
    if os.path.exists(creds_path):
        with open(creds_path, "r", encoding="utf-8") as f:
            creds_str = json.dumps(json.load(f))
        print("\n[4] Secret 이름: BLOGGER_CREDENTIALS_JSON")
        print("─" * 78)
        print(creds_str)
        print("─" * 78)
    else:
        print("\n[4] ❌ credentials.json 파일을 찾을 수 없습니다.")

    # 5. BLOGGER_TOKEN_JSON
    token_path = os.path.join(BASE_DIR, "token.json")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8") as f:
            token_str = json.dumps(json.load(f))
        print("\n[5] Secret 이름: BLOGGER_TOKEN_JSON")
        print("─" * 78)
        print(token_str)
        print("─" * 78)
    else:
        print("\n[5] ❌ token.json 파일을 찾을 수 없습니다.")

    print("\n" + "═" * 78)
    print("  ✅ 등록 완료 후, GitHub 저장소 'Actions' 탭에서 'Run workflow' 버튼을 누르면")
    print("  클라우드 서버에서 즉시 무인 자동 배포가 시작됩니다!")
    print("═" * 78 + "\n")

if __name__ == "__main__":
    export_secrets()
