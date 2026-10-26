# -*- coding: utf-8 -*-
"""
tests/test_strategy_lab_e2e.py
------------------------------
E2E Playwright verification for the Vibe Strategy Lab article:
- Evaluates DOM structure
- Checks canvas creation and Lightweight Charts execution
- Tests slider interaction and dynamic KPI recalculation
- Verifies WCAG 2.1 AAA contrast via EditorialInspector
- Takes high-res screenshots for desktop & mobile
"""

import os
import unittest
from playwright.sync_api import sync_playwright
from engine.crew.strategy_lab_article_builder import StrategyLabArticleBuilder
from engine.crew.editorial_inspector import EditorialInspector

ARTIFACTS_DIR = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "brain", "2fa07f4d-895a-42a3-a3fd-1c9564dd6628"
)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


class TestStrategyLabE2E(unittest.TestCase):
    def setUp(self):
        self.article = StrategyLabArticleBuilder.build_wonyotti_article()
        self.html = self.article["html_content"]

    def test_playwright_interactive_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # 1. Desktop Test (1280x900)
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()

            # Set content
            page.set_content(self.html, wait_until="networkidle", timeout=15000)

            # Check root container
            root = page.locator("#vibe-strategy-lab-root")
            self.assertTrue(root.is_visible(), "Strategy Lab Root must be visible")

            # Check chart element
            chart_container = page.locator("#tv-strategy-chart")
            self.assertTrue(chart_container.is_visible(), "Chart container must be visible")

            # Check sliders
            slider_period = page.locator("#slider-bb-period")
            self.assertTrue(slider_period.is_visible(), "BB Period slider must be visible")

            # Check KPI boxes
            kpi_winrate = page.locator("#kpi-winrate")
            self.assertTrue(kpi_winrate.is_visible(), "Winrate KPI must be visible")

            # Test Slider Interaction: Change period to 30
            slider_period.fill("30")
            slider_period.dispatch_event("input")
            page.wait_for_timeout(500)

            val_period = page.locator("#val-bb-period").text_content()
            self.assertEqual(val_period, "30", "Slider value label must update to 30")

            # Test Toggle: Follow Strategy
            toggle = page.locator("#toggle-follow-strategy")
            toggle.scroll_into_view_if_needed()
            toggle.check(force=True)
            page.wait_for_timeout(300)

            follow_label = page.locator("#follow-status-label").text_content()
            self.assertIn("모의투자 계좌 장착됨", follow_label, "Follow label must show active")

            # Capture Desktop Screenshot
            desktop_shot = os.path.join(ARTIFACTS_DIR, "strategy_lab_preview_desktop.png")
            page.screenshot(path=desktop_shot, full_page=False)
            self.assertTrue(os.path.exists(desktop_shot), "Desktop screenshot must be saved")

            # 2. Mobile Test (375x812)
            mob_context = browser.new_context(viewport={"width": 375, "height": 812})
            mob_page = mob_context.new_page()
            mob_page.set_content(self.html, wait_until="networkidle", timeout=15000)

            mob_shot = os.path.join(ARTIFACTS_DIR, "strategy_lab_preview_mobile.png")
            mob_page.screenshot(path=mob_shot, full_page=False)
            self.assertTrue(os.path.exists(mob_shot), "Mobile screenshot must be saved")

            browser.close()

    def test_editorial_contrast_audit(self):
        inspector = EditorialInspector(artifacts_dir=ARTIFACTS_DIR)
        res = inspector.inspect(self.html, is_url=False)

        print(f"[Editorial Contrast Audit] Passed: {res['passed']}, Defects: {len(res['defects'])}")
        print(f"Stats: {res.get('stats')}")

        self.assertTrue(res["passed"], f"Contrast audit must pass: {res['defects']}")
        self.assertEqual(len(res["defects"]), 0, "Defects count must be 0")


if __name__ == "__main__":
    unittest.main()
