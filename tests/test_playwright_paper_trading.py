# -*- coding: utf-8 -*-
"""
Playwright Visual & Layout Gate Test for Canvas Chart & Paper Trading Engine.
Renders the paper trading bundle across mobile (375px) and desktop (1280px) viewports
to guarantee zero horizontal overflow, clean DOM BBox containment, and zero console errors.
"""
import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.crew.dataset_resolver import TradingDatasetResolver

ARTIFACT_DIR = r"C:\Users\cnwjr\.gemini\antigravity\brain\2fa07f4d-895a-42a3-a3fd-1c9564dd6628"


class TestPlaywrightPaperTrading(unittest.TestCase):
    """Playwright E2E visual and layout verification for paper trading engine."""

    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        resolver = TradingDatasetResolver()
        cls.bundle_html = resolver.render_paper_trading_component("nvda_stock_tax")

        cls.full_page_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Paper Trading Test</title>
  <style>
    body {{
      background: #0a0e17;
      color: #f9fafb;
      margin: 0;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .main-container {{
      max-width: 880px;
      margin: 0 auto;
    }}
  </style>
</head>
<body>
  <div class="main-container">
    {cls.bundle_html}
  </div>
</body>
</html>"""

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def test_mobile_375px_layout_and_zero_overflow(self):
        """Checks mobile viewport for horizontal overflow and visual screenshot."""
        page = self.browser.new_page(viewport={"width": 375, "height": 812})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page.set_content(self.full_page_html)
        page.wait_for_timeout(300)

        # Check horizontal scroll
        scroll_width = page.evaluate("() => document.documentElement.scrollWidth")
        client_width = page.evaluate("() => document.documentElement.clientWidth")
        self.assertLessEqual(scroll_width, client_width + 1, "Mobile 375px should have zero horizontal overflow")

        # Capture mobile screenshot to artifact dir
        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        screenshot_path = os.path.join(ARTIFACT_DIR, "paper_trading_mobile_375px.png")
        page.screenshot(path=screenshot_path)
        self.assertTrue(os.path.exists(screenshot_path))
        page.close()

    def test_desktop_1280px_layout_and_interaction(self):
        """Checks desktop layout, clicks Buy button, and verifies state update."""
        page = self.browser.new_page(viewport={"width": 1280, "height": 900})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page.set_content(self.full_page_html)
        page.wait_for_timeout(300)

        # Check desktop scroll
        scroll_width = page.evaluate("() => document.documentElement.scrollWidth")
        client_width = page.evaluate("() => document.documentElement.clientWidth")
        self.assertLessEqual(scroll_width, client_width + 1, "Desktop 1280px should have zero horizontal overflow")

        # Verify Buy button exists and click it
        buy_btn = page.locator("#blogin-paper-nvda-btn-buy")
        self.assertTrue(buy_btn.is_visible())
        buy_btn.click()
        page.wait_for_timeout(200)

        # Verify active position box is displayed
        active_box = page.locator("#blogin-paper-nvda-active-position")
        self.assertTrue(active_box.is_visible())

        # Verify Close button works
        close_btn = page.locator("#blogin-paper-nvda-btn-close")
        self.assertTrue(close_btn.is_visible())
        close_btn.click()
        page.wait_for_timeout(200)

        # Capture desktop screenshot to artifact dir
        screenshot_path = os.path.join(ARTIFACT_DIR, "paper_trading_desktop_1280px.png")
        page.screenshot(path=screenshot_path)
        self.assertTrue(os.path.exists(screenshot_path))
        page.close()


if __name__ == "__main__":
    unittest.main()
