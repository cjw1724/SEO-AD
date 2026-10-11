# -*- coding: utf-8 -*-
"""
engine/publisher/blogger_gateway.py
-----------------------------------
Google Blogger API v3 Publishing Gateway (Developer & Publisher Role).
- Robust OAuth2 token management with auto-refresh
- Inject JSON-LD Schema.org structured markup for Google Search Rich Snippets
- Safe publishing with draft mode toggle
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']


class BloggerGateway:
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        else:
            self.base_dir = base_dir

        load_dotenv(os.path.join(self.base_dir, "SEO.env"))
        self.blog_id = os.getenv("BLOGGER_BLOG_ID", "2002031376804677477")
        self.token_path = os.path.join(self.base_dir, "token.json")
        self.creds_path = os.path.join(self.base_dir, "credentials.json")

    def _get_authenticated_credentials(self, force_refresh: bool = False):
        creds = None
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                print(f"[BloggerGateway] Error loading token.json: {e}")

        # If force_refresh is requested or credentials expired, refresh using refresh_token
        if creds and (force_refresh or not creds.valid):
            if creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(self.token_path, "w", encoding="utf-8") as f:
                        f.write(creds.to_json())
                    print("[BloggerGateway] OAuth2 access token refreshed successfully.")
                except Exception as e:
                    print(f"[BloggerGateway] Error refreshing token: {e}")
                    creds = None

        if not creds or not creds.valid:
            if not os.path.exists(self.creds_path):
                raise FileNotFoundError(f"credentials.json not found at {self.creds_path}")
            print("[BloggerGateway] Launching browser OAuth authorization flow...")
            flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(self.token_path, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

        return creds

    def build_schema_markup(self, title: str, keyword: str, category: str) -> str:
        """
        Creates Schema.org Article / TechArticle JSON-LD structured data.
        """
        schema_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": f"2026 {keyword} 핵심 요약 및 인터랙티브 모의 계산 리포트",
            "articleSection": category,
            "keywords": [keyword, "2026", "모의계산", "절약팁", "Blogin365AI"],
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "author": {
                "@type": "Organization",
                "name": "Blogin 365 AI Editorial Team",
                "url": "https://blogin365ai.blogspot.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Blogin 365 AI",
                "url": "https://blogin365ai.blogspot.com"
            }
        }
        return f'<script type="application/ld+json">\n{json.dumps(schema_data, ensure_ascii=False, indent=2)}\n</script>'

    def publish(self, title: str, html_content: str, labels: list = None, is_draft: bool = False, category: str = "FINANCE", max_retries: int = 3) -> dict:
        """
        Publishes post to Google Blogger with self-healing retries.
        """
        if not self.blog_id:
            return {"success": False, "error": "BLOGGER_BLOG_ID is missing"}

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)

                # Injected schema markup
                schema_tag = self.build_schema_markup(title, title, category)
                final_content = f"{schema_tag}\n\n{html_content}"

                body = {
                    "kind": "blogger#post",
                    "title": title,
                    "content": final_content,
                    "labels": labels or ["정보", "실측분석", "Blogin365AI"]
                }

                posts_resource = service.posts()
                result = posts_resource.insert(
                    blogId=self.blog_id,
                    body=body,
                    isDraft=is_draft
                ).execute()

                post_url = result.get("url", "")
                post_id = result.get("id", "")
                return {
                    "success": True,
                    "url": post_url,
                    "id": post_id,
                    "title": title,
                    "is_draft": is_draft,
                    "attempts": attempt
                }
            except Exception as e:
                last_error = e
                print(f"[BloggerGateway] Publish attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)

        return {
            "success": False,
            "error": str(last_error),
            "attempts": max_retries
        }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    gw = BloggerGateway()
    print("=== Blogger Gateway Initialized ===")
    print("Target Blog ID:", gw.blog_id)
    print("Token File Exists:", os.path.exists(gw.token_path))
    print("Credentials File Exists:", os.path.exists(gw.creds_path))
