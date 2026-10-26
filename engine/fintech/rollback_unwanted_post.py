"""
Rollback and delete the unwanted Vibe Trading blog post.
"""
import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from googleapiclient.discovery import build
from engine.publisher.blogger_gateway import BloggerGateway

sys.stdout.reconfigure(encoding="utf-8")

def rollback_post():
    gw = BloggerGateway()
    creds = gw._get_authenticated_credentials()
    service = build("blogger", "v3", credentials=creds)

    posts = service.posts().list(blogId=gw.blog_id, maxResults=15).execute().get("items", [])
    print(f"Total recent posts: {len(posts)}")

    deleted_count = 0
    for p in posts:
        title = p.get("title", "")
        url = p.get("url", "")
        post_id = p.get("id")
        print(f"- Post: [{post_id}] '{title}' -> {url}")

        if "VIBE TRADING" in title or "vibe-trading-live-simulator" in url:
            print(f">>> DELETING UNWANTED POST [{post_id}]: {title}")
            service.posts().delete(blogId=gw.blog_id, postId=post_id).execute()
            print(f">>> DELETED SUCCESSFULLY!")
            deleted_count += 1

    # Clean published_posts.json
    posts_file = os.path.join(BASE_DIR, "data", "published_posts.json")
    if os.path.exists(posts_file):
        with open(posts_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cleaned = [item for item in data if "vibe-trading-live-simulator" not in str(item) and "VIBE TRADING" not in str(item)]
        with open(posts_file, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)
        print(f"Cleaned published_posts.json (retained {len(cleaned)} items)")

    print(f"\nRollback complete. Deleted {deleted_count} unwanted post(s).")

if __name__ == "__main__":
    rollback_post()
