"""
Patch existing post 4307561766392959448 with top Vibe Trading banner.
"""
import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from googleapiclient.discovery import build
from engine.publisher.blogger_gateway import BloggerGateway
from engine.crew.editorial_inspector import EditorialInspector

sys.stdout.reconfigure(encoding="utf-8")

def patch_banner():
    gw = BloggerGateway()
    creds = gw._get_authenticated_credentials()
    service = build("blogger", "v3", credentials=creds)
    post_id = "4307561766392959448"

    post = service.posts().get(blogId=gw.blog_id, postId=post_id).execute()
    title = post.get("title")
    content = post.get("content", "")

    if "blogin-vibe-header-callout" in content:
        print("Banner already present!")
        return

    banner = """
<div class="blogin-vibe-header-callout" style="margin:20px 0 32px 0; padding:18px 24px; background:linear-gradient(135deg, #0d1527 0%, #1e3a8a 100%); border:1px solid #3b82f6; border-radius:14px; display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;">
  <div>
    <strong style="color:#ffffff; font-size:16px; display:block; margin-bottom:4px;">🔥 [공식 서비스 개장] VIBE TRADING 프로 스테이션 오픈!</strong>
    <span style="color:#cbd5e1; font-size:13px;">실시간 트레이딩뷰 차트와 $10,000 가상 자금으로 1x~20x 모의투자 Top 10 랭킹전에 참여하세요.</span>
  </div>
  <div style="display:flex; gap:8px;">
    <a href="https://blogin365ai.blogspot.com/p/vibe-trading.html" style="background:#10b981; color:#ffffff !important; font-weight:800; font-size:13px; padding:10px 18px; border-radius:8px; text-decoration:none; white-space:nowrap;">
      모의투자 랭킹전 참여 →
    </a>
  </div>
</div>
"""
    # Insert banner after title / H1 or at top of post
    new_content = f"{banner}\n{content}"
    inspector = EditorialInspector()
    healed, _ = inspector.inspect_and_heal(new_content)

    res = gw.update_post(post_id=post_id, title=title, html_content=healed, labels=post.get("labels", []))
    print("Patched existing post banner successfully:", res.get("url"))

if __name__ == "__main__":
    patch_banner()
