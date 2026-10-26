"""
Clean banner from post 4307561766392959448.
"""
import sys
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from googleapiclient.discovery import build
from engine.publisher.blogger_gateway import BloggerGateway
from engine.crew.editorial_inspector import EditorialInspector

sys.stdout.reconfigure(encoding="utf-8")

def clean_banner():
    gw = BloggerGateway()
    creds = gw._get_authenticated_credentials()
    service = build("blogger", "v3", credentials=creds)
    post_id = "4307561766392959448"

    post = service.posts().get(blogId=gw.blog_id, postId=post_id).execute()
    title = post.get("title")
    content = post.get("content", "")

    # Remove blogin-vibe-header-callout if present
    cleaned_content = re.sub(r'<div class="blogin-vibe-header-callout".*?</div>\s*', '', content, flags=re.DOTALL)
    print(f"Content length before: {len(content)}, after: {len(cleaned_content)}")

    inspector = EditorialInspector()
    healed, _ = inspector.inspect_and_heal(cleaned_content)

    res = gw.update_post(post_id=post_id, title=title, html_content=healed, labels=post.get("labels", []))
    print("Cleaned post 4307561766392959448 successfully:", res.get("url"))

if __name__ == "__main__":
    clean_banner()
