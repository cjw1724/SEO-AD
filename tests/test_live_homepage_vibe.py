"""
Playwright test to verify VIBE TRADING presence on the live homepage.
URL: https://blogin365ai.blogspot.com/
"""

import os
import sys
import unittest
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HOME_URL = "https://blogin365ai.blogspot.com/"
ARTIFACTS_DIR = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "brain", "2fa07f4d-895a-42a3-a3fd-1c9564dd6628"
)

class TestLiveHomepageVibe(unittest.TestCase):
    def test_vibe_on_homepage(self):
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # 1. Desktop Test
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()

            print(f"\n[Playwright] Navigating to live homepage: {HOME_URL}")
            page.goto(HOME_URL, wait_until="networkidle", timeout=25000)

            # Screenshot after publishing
            desk_shot = os.path.join(ARTIFACTS_DIR, "live_homepage_after_vibe.png")
            page.screenshot(path=desk_shot, full_page=False)
            print(f" -> Desktop screenshot saved: {desk_shot}")

            # Verify Vibe Trading title exists on homepage
            body_text = page.inner_text("body")
            self.assertIn("VIBE TRADING", body_text)
            print(" -> [PASS] 'VIBE TRADING' text confirmed on homepage!")

            # Verify the top post link
            vibe_post_link = page.locator("a[href*='vibe-trading']").first
            self.assertTrue(vibe_post_link.is_visible())
            print(f" -> [PASS] Vibe Trading link is visible: {vibe_post_link.get_attribute('href')}")

            # Click into the Vibe Trading post from the homepage
            print(" -> Clicking Vibe Trading post from homepage...")
            vibe_post_link.click()
            page.wait_for_load_state("networkidle")

            # Check that the terminal elements loaded inside the post
            equity = page.locator("#hud-equity").inner_text()
            print(f" -> Post terminal loaded successfully! Equity: {equity}")
            self.assertIn("$10,000", equity)

            context.close()

            # 2. Mobile Test
            context_mob = browser.new_context(viewport={"width": 375, "height": 812})
            page_mob = context_mob.new_page()
            page_mob.goto(HOME_URL, wait_until="networkidle", timeout=25000)

            mob_shot = os.path.join(ARTIFACTS_DIR, "live_homepage_mobile_vibe.png")
            page_mob.screenshot(path=mob_shot, full_page=False)
            print(f" -> Mobile screenshot saved: {mob_shot}")

            body_mob = page_mob.inner_text("body")
            self.assertIn("VIBE TRADING", body_mob)

            context_mob.close()
            browser.close()

if __name__ == "__main__":
    unittest.main()
