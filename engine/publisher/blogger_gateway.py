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

    def update_post(self, post_id: str, title: str, html_content: str, labels: list = None, category: str = "FINANCE", max_retries: int = 3) -> dict:
        """
        Updates an existing Blogger post using posts().patch().
        """
        if not self.blog_id:
            return {"success": False, "error": "BLOGGER_BLOG_ID is missing"}

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)

                schema_tag = self.build_schema_markup(title, title, category)
                final_content = f"{schema_tag}\n\n{html_content}"

                body = {
                    "title": title,
                    "content": final_content
                }
                if labels is not None:
                    body["labels"] = labels

                posts_resource = service.posts()
                result = posts_resource.patch(
                    blogId=self.blog_id,
                    postId=post_id,
                    body=body
                ).execute()

                post_url = result.get("url", "")
                return {
                    "success": True,
                    "url": post_url,
                    "id": post_id,
                    "title": title,
                    "attempts": attempt
                }
            except Exception as e:
                last_error = e
                print(f"[BloggerGateway] Update attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)

        return {
            "success": False,
            "error": str(last_error),
            "attempts": max_retries
        }

    def list_pages(self, max_retries: int = 3) -> list:
        """
        Lists all static pages of the Blogger blog.
        """
        if not self.blog_id:
            return []

        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)
                result = service.pages().list(blogId=self.blog_id).execute()
                return result.get("items", [])
            except Exception as e:
                print(f"[BloggerGateway] list_pages attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)
        return []

    def publish_page(self, title: str, html_content: str, is_draft: bool = False, max_retries: int = 3) -> dict:
        """
        Creates and publishes a static Page on Google Blogger.
        """
        if not self.blog_id:
            return {"success": False, "error": "BLOGGER_BLOG_ID is missing"}

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)

                body = {
                    "kind": "blogger#page",
                    "title": title,
                    "content": html_content
                }

                result = service.pages().insert(
                    blogId=self.blog_id,
                    body=body,
                    isDraft=is_draft
                ).execute()

                page_url = result.get("url", "")
                page_id = result.get("id", "")
                return {
                    "success": True,
                    "url": page_url,
                    "id": page_id,
                    "title": title,
                    "is_draft": is_draft,
                    "attempts": attempt
                }
            except Exception as e:
                last_error = e
                print(f"[BloggerGateway] publish_page attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)

        return {
            "success": False,
            "error": str(last_error),
            "attempts": max_retries
        }

    def update_page(self, page_id: str, title: str, html_content: str, max_retries: int = 3) -> dict:
        """
        Updates an existing static Page on Google Blogger.
        """
        if not self.blog_id:
            return {"success": False, "error": "BLOGGER_BLOG_ID is missing"}

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)

                body = {
                    "title": title,
                    "content": html_content
                }

                result = service.pages().patch(
                    blogId=self.blog_id,
                    pageId=page_id,
                    body=body
                ).execute()

                page_url = result.get("url", "")
                return {
                    "success": True,
                    "url": page_url,
                    "id": page_id,
                    "title": title,
                    "attempts": attempt
                }
            except Exception as e:
                last_error = e
                print(f"[BloggerGateway] update_page attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)

        return {
            "success": False,
            "error": str(last_error),
            "attempts": max_retries
        }

    def ensure_mandatory_static_pages(self, dry_run: bool = False) -> dict:
        """
        Ensures the 4 mandatory Google AdSense trust/policy static pages exist on Blogger:
        1. About Us
        2. Privacy Policy
        3. Terms of Service
        4. Contact Us
        """
        from engine.publisher.static_pages_builder import get_mandatory_static_pages
        package = get_mandatory_static_pages()

        if dry_run:
            results = {}
            for key, data in package.items():
                results[key] = {
                    "success": True,
                    "url": f"https://blogin365ai.blogspot.com/p/{data['slug']}.html",
                    "id": f"dry-run-{key}",
                    "title": data["title"],
                    "action": "dry_run_simulated"
                }
            return {"success": True, "pages": results}

        existing_pages = self.list_pages()
        results = {}

        for key, data in package.items():
            target_title = data["title"]
            target_slug = data["slug"]
            target_html = data["html"]

            matched = None
            for p in existing_pages:
                p_url = p.get("url", "").lower()
                p_title = p.get("title", "").lower()
                if f"/{target_slug}.html" in p_url or target_slug in p_title or key in p_title:
                    matched = p
                    break

            if matched:
                page_id = matched["id"]
                upd_res = self.update_page(page_id, target_title, target_html)
                upd_res["action"] = "updated"
                results[key] = upd_res
                print(f"[BloggerGateway] Static page '{target_title}' updated: {upd_res.get('url')}")
            else:
                pub_res = self.publish_page(target_title, target_html, is_draft=False)
                pub_res["action"] = "created"
                results[key] = pub_res
                print(f"[BloggerGateway] Static page '{target_title}' created: {pub_res.get('url')}")

        all_ok = all(r.get("success", False) for r in results.values())
        return {"success": all_ok, "pages": results}

    def revert_to_draft(self, post_id: str, max_retries: int = 3) -> dict:
        """
        Reverts a published post to draft status (unpublishes it).
        Useful for unpublishing thin / low-value / obsolete legacy posts without 404 dead links.
        """
        if not self.blog_id:
            return {"success": False, "error": "BLOGGER_BLOG_ID is missing"}

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)

                result = service.posts().revert(
                    blogId=self.blog_id,
                    postId=post_id
                ).execute()

                return {
                    "success": True,
                    "id": post_id,
                    "status": "DRAFT",
                    "attempts": attempt
                }
            except Exception as e:
                last_error = e
                print(f"[BloggerGateway] revert_to_draft attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)

        return {
            "success": False,
            "error": str(last_error),
            "attempts": max_retries
        }

    def list_all_posts(self, max_posts: int = 100, max_retries: int = 3) -> list:
        """
        Retrieves all published posts from the Blogger blog.
        """
        if not self.blog_id:
            return []

        for attempt in range(1, max_retries + 1):
            try:
                force_refresh = (attempt > 1)
                creds = self._get_authenticated_credentials(force_refresh=force_refresh)
                service = build('blogger', 'v3', credentials=creds)

                posts = []
                page_token = None
                while len(posts) < max_posts:
                    req = service.posts().list(
                        blogId=self.blog_id,
                        maxResults=min(50, max_posts - len(posts)),
                        pageToken=page_token
                    )
                    res = req.execute()
                    items = res.get("items", [])
                    posts.extend(items)
                    page_token = res.get("nextPageToken")
                    if not page_token or not items:
                        break
                return posts
            except Exception as e:
                print(f"[BloggerGateway] list_all_posts attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 * attempt)
        return []

    def sanitize_existing_posts_for_ghost_mode(self, dry_run: bool = False) -> dict:
        """
        Sanitizes all existing published posts on the blog to enforce AdSense Ghost Mode:
        1. Identifies obsolete thin posts (< 1600 chars or 2023 legacy) and unpublishes them (reverts to draft).
        2. In all other posts, strips any empty ad slots (<div class="adsense-slot">...</div>) and adsbygoogle calls.
        3. Ensures mandatory policy/trust links (About Us, Privacy Policy, Terms, Contact) are present in every post footer.
        """
        import re
        from bs4 import BeautifulSoup
        posts = self.list_all_posts(max_posts=100)
        reverted = []
        sanitized = []
        skipped = []

        trust_links_block = (
            '<div class="editorial-trust-links" style="margin-top: 32px; padding: 18px 20px; background: #f8fafc; '
            'border: 1px solid #e2e8f0; border-radius: 12px; display: flex; flex-wrap: wrap; gap: 12px; '
            'align-items: center; font-size: 13px; color: #64748b; line-height: 1.6;">\n'
            '  <span style="font-weight: 700; color: #0f172a;">공식 정책 및 신뢰 센터:</span>\n'
            '  <a href="https://blogin365ai.blogspot.com/p/about-us-blogin-365-ai.html" target="_blank" rel="noopener" style="color: #2563eb; text-decoration: none; font-weight: 600;">블로그 소개</a>\n'
            '  <span style="color: #cbd5e1;">·</span>\n'
            '  <a href="https://blogin365ai.blogspot.com/p/privacy-policy.html" target="_blank" rel="noopener" style="color: #2563eb; text-decoration: none; font-weight: 600;">개인정보처리방침</a>\n'
            '  <span style="color: #cbd5e1;">·</span>\n'
            '  <a href="https://blogin365ai.blogspot.com/p/terms-of-service.html" target="_blank" rel="noopener" style="color: #2563eb; text-decoration: none; font-weight: 600;">이용약관</a>\n'
            '  <span style="color: #cbd5e1;">·</span>\n'
            '  <a href="https://blogin365ai.blogspot.com/p/contact-us.html" target="_blank" rel="noopener" style="color: #2563eb; text-decoration: none; font-weight: 600;">문의하기</a>\n'
            '</div>'
        )

        for p in posts:
            pid = p.get("id")
            title = p.get("title", "")
            content = p.get("content", "")
            pub_date = p.get("published", "")

            # 1. Check for obsolete thin / 2023 legacy posts
            is_legacy_2023 = "2023-" in pub_date or "2023" in title or len(content) < 1600
            if is_legacy_2023 and not any(k in title for k in ["2026", "알뜰폰", "지원금", "보험", "환급", "도수치료", "임플란트", "모니터"]):
                if dry_run:
                    reverted.append({"id": pid, "title": title, "reason": "thin_legacy_2023", "dry_run": True})
                else:
                    rev_res = self.revert_to_draft(pid)
                    if rev_res.get("success"):
                        reverted.append({"id": pid, "title": title, "reason": "thin_legacy_2023"})
                        print(f"[BloggerGateway] Reverted legacy thin post to draft: [{pid}] {title}")
                continue

            # 2. Check if post has adsense slots or unapproved ads
            has_ad_slot = "adsense-slot" in content or "adsbygoogle" in content or "ADVERTISEMENT · B365 AD NETWORK" in content
            has_trust = "editorial-trust-links" in content or "about-us-blogin-365-ai.html" in content

            if not has_ad_slot and has_trust:
                skipped.append({"id": pid, "title": title, "status": "already_clean"})
                continue

            # DOM-safe sanitization via BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Decompose all adsense slot containers
            for div in soup.find_all('div', class_=re.compile(r'\badsense-slot\b')):
                div.decompose()
            # Decompose all ins.adsbygoogle elements
            for ins in soup.find_all('ins', class_='adsbygoogle'):
                ins.decompose()
            # Decompose adsbygoogle push script tags
            for sc in soup.find_all('script'):
                if sc.string and 'adsbygoogle' in sc.string:
                    sc.decompose()

            # Ensure trust links block exists
            if not soup.find(class_='editorial-trust-links'):
                trust_soup = BeautifulSoup(trust_links_block, 'html.parser')
                container = soup.find(class_='article-container')
                if container:
                    container.append(trust_soup)
                else:
                    soup.append(trust_soup)

            cleaned_html = str(soup)

            if dry_run:
                sanitized.append({"id": pid, "title": title, "dry_run": True})
            else:
                patch_res = self.update_post(post_id=pid, title=title, html_content=cleaned_html)
                if patch_res.get("success"):
                    sanitized.append({"id": pid, "title": title})
                    print(f"[BloggerGateway] Sanitized post for Ghost Mode: [{pid}] {title}")
                else:
                    print(f"[BloggerGateway] Failed to patch post [{pid}] {title}: {patch_res.get('error')}")

        return {
            "success": True,
            "reverted_thin_posts": reverted,
            "sanitized_posts": sanitized,
            "skipped_posts": skipped
        }



if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    gw = BloggerGateway()
    print("=== Blogger Gateway Initialized ===")
    print("Target Blog ID:", gw.blog_id)
    print("Token File Exists:", os.path.exists(gw.token_path))
    print("Credentials File Exists:", os.path.exists(gw.creds_path))
