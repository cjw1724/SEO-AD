"""
Playwright E2E Test Suite for Live Vibe Trading Station (v9.0 Apex)
Tests live URL: https://blogin365ai.blogspot.com/p/vibe-trading.html
"""

import unittest
import os
import sys
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.crew.editorial_inspector import EditorialInspector

class TestVibeTradingStationLive(unittest.TestCase):
    LIVE_URL = "https://blogin365ai.blogspot.com/p/vibe-trading.html"
    ARTIFACTS_DIR = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "brain", "2fa07f4d-895a-42a3-a3fd-1c9564dd6628"
    )

    def test_live_vibe_trading_terminal_e2e(self):
        os.makedirs(self.ARTIFACTS_DIR, exist_ok=True)
        console_errors = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # 1. Desktop 1280x900 Viewport Test
            context_desk = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context_desk.new_page()

            all_console = []
            page.on("console", lambda msg: all_console.append(f"[{msg.type}] {msg.text}"))
            page.on("pageerror", lambda err: print(f"[FULL PAGE ERROR] {err}"))

            print(f"\n[Playwright E2E] Connecting to live Vibe Trading URL: {self.LIVE_URL}")
            page.goto(self.LIVE_URL, wait_until="networkidle", timeout=30000)

            print("--- BROWSER CONSOLE LOGS ---")
            for c in all_console[:20]:
                print(c)
            print("----------------------------")

            # Check HUD elements
            equity_text = page.locator("#hud-equity").inner_text()
            print(f" -> Initial Equity: {equity_text}")
            self.assertIn("$10,000", equity_text)

            cash_text = page.locator("#hud-cash").inner_text()
            print(f" -> Initial Cash: {cash_text}")
            self.assertIn("$10,000", cash_text)

            # Check Leaderboard table populated
            lb_rows = page.locator("#tbody-leaderboard tr").count()
            print(f" -> Leaderboard Rows: {lb_rows}")
            self.assertGreaterEqual(lb_rows, 5)

            # Execute a test trade (Long BTC, 10x leverage)
            print(" -> Executing mock trade: Long BTC 10x...")
            page.click("#btn-submit-order")
            page.wait_for_timeout(1000)

            # Verify positions table has 1 active position
            pos_count = page.locator("#pos-count").inner_text()
            print(f" -> Active Position Count: {pos_count}")
            self.assertGreaterEqual(int(pos_count), 1)

            # Register nickname in Leaderboard
            print(" -> Registering nickname: '압구정퀀트킹'...")
            page.fill("#input-trader-name", "압구정퀀트킹")
            # Close browser prompt automatically
            page.on("dialog", lambda dialog: dialog.accept())
            page.locator("button:has-text('닉네임 저장')").click()
            page.wait_for_timeout(500)

            # Take high-res Desktop screenshot
            desktop_shot = os.path.join(self.ARTIFACTS_DIR, "vibe_trading_live_desktop.png")
            page.screenshot(path=desktop_shot, full_page=False)
            print(f" -> Desktop screenshot saved: {desktop_shot}")
            self.assertTrue(os.path.exists(desktop_shot))

            context_desk.close()

            # 2. Mobile 375x812 Viewport Test
            context_mob = browser.new_context(viewport={"width": 375, "height": 812})
            page_mob = context_mob.new_page()
            page_mob.goto(self.LIVE_URL, wait_until="networkidle", timeout=30000)

            mobile_shot = os.path.join(self.ARTIFACTS_DIR, "vibe_trading_live_mobile.png")
            page_mob.screenshot(path=mobile_shot, full_page=False)
            print(f" -> Mobile screenshot saved: {mobile_shot}")
            self.assertTrue(os.path.exists(mobile_shot))

            context_mob.close()
            browser.close()

        # 3. Editorial Inspector WCAG 2.1 AAA Contrast Gate
        inspector = EditorialInspector(artifacts_dir=self.ARTIFACTS_DIR)
        review = inspector.inspect(self.LIVE_URL, is_url=True)
        print(f" -> Editorial Inspector Contrast Passed: {review['passed']}")
        for vp, s in review.get("stats", {}).items():
            print(f"    * [{vp}] Min Contrast: {s['min_contrast']}:1 | Avg: {s['avg_contrast']}:1 | Defects: {s['defect_count']}")

        self.assertTrue(review["passed"], f"Contrast defects detected: {review.get('defects')}")

if __name__ == "__main__":
    unittest.main()
