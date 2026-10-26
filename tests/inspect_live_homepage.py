import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HOME_URL = "https://blogin365ai.blogspot.com/"
ARTIFACTS_DIR = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "brain", "2fa07f4d-895a-42a3-a3fd-1c9564dd6628"
)

def inspect_homepage():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print(f"Connecting to live homepage: {HOME_URL}...")
        page.goto(HOME_URL, wait_until="networkidle", timeout=25000)

        # Capture desktop screenshot
        shot_path = os.path.join(ARTIFACTS_DIR, "live_homepage_before.png")
        page.screenshot(path=shot_path, full_page=False)
        print(f"Saved homepage screenshot: {shot_path}")

        # Extract all titles and links on homepage
        posts = page.locator(".post-title, .entry-title, h2.post-title, .apex-post-title, h1, h2, h3").all_inner_texts()
        print(f"Total post headers found on homepage: {len(posts)}")
        for i, t in enumerate(posts[:10]):
            print(f" [{i+1}] {t.strip()}")

        links = page.locator("a").all_text_contents()
        vibe_links = [l.strip() for l in links if "VIBE" in l or "트레이딩" in l]
        print(f"Vibe links found on homepage: {vibe_links}")

        context.close()
        browser.close()

if __name__ == "__main__":
    inspect_homepage()
