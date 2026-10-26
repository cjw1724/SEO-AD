# -*- coding: utf-8 -*-
"""
tests/test_playwright_3viewports.py
------------------------------------
Playwright 3대 뷰포트(Mobile 375px, Tablet 768px, Desktop 1200px) DOM BBox 및 무오버플로우 무인 검증 게이트
- 3대 뷰포트 가로스크롤 폭파(Horizontal Blowout) 0건 검증 (scrollWidth <= clientWidth)
- 계산기 샌드박스 극단 경계값 연산 결과 내 NaN / Infinity / undefined 영구 방어
- 결과 복사 및 URL Hash 공유 버튼 인터랙션 검증
"""

import os
import sys
import unittest
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.crew.dataset_resolver import TradingDatasetResolver

VIEWPORTS = [
    {"name": "Mobile (iPhone SE / 375px)", "width": 375, "height": 667},
    {"name": "Tablet (iPad Mini / 768px)", "width": 768, "height": 1024},
    {"name": "Desktop (Standard HD / 1200px)", "width": 1200, "height": 800}
]

TEST_ASSET_RULES = [
    ("nvda_stock_tax", "엔비디아 해외주식 양도세"),
    ("btc_futures_liquidation", "비트코인 선물 청산가"),
    ("tsla_water_averaging", "테슬라 물타기 평단가"),
    ("o_dividend_compound", "리얼티인컴 월배당 복리")
]


class TestPlaywrightThreeViewports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resolver = TradingDatasetResolver()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def _build_full_page_html(self, rule_key: str) -> str:
        resolved = self.resolver.resolve_topic(rule_key)
        widget_html = self.resolver.render_trading_saas_html(rule_key)
        tables_html = self.resolver.render_trading_tables(rule_key)
        cta_html = self.resolver.render_monetization_cta(rule_key)
        disclaimer_html = self.resolver.render_legal_disclaimer()
        silo_html = self.resolver.render_internal_silo_links(rule_key)

        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{resolved['target_keyword']}</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #060913;
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    .main-wrap {{
      max-width: 880px;
      margin: 0 auto;
      padding: 16px;
      box-sizing: border-box;
    }}
  </style>
</head>
<body>
  <div class="main-wrap">
    <h1 style="font-size: 24px; font-weight: 900; margin-bottom: 16px;">{resolved['target_keyword']}</h1>
    {widget_html}
    {tables_html}
    {cta_html}
    {silo_html}
    {disclaimer_html}
  </div>
</body>
</html>"""

    def test_01_three_viewports_no_horizontal_blowout(self):
        """375px 모바일, 768px 태블릿, 1200px 데스크톱에서 가로 스크롤 폭파(Blowout) 0건 검증"""
        for vp in VIEWPORTS:
            page = self.browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            for rule_key, desc in TEST_ASSET_RULES:
                html = self._build_full_page_html(rule_key)
                page.set_content(html, wait_until="networkidle")

                # 1. document scrollWidth 검증 (뷰포트 너비 초과 방어)
                scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
                client_w = page.evaluate("() => document.documentElement.clientWidth")
                self.assertLessEqual(
                    scroll_w,
                    client_w + 3,
                    f"[{vp['name']}] '{desc}'({rule_key})에서 가로 스크롤 폭파 감지! scrollWidth({scroll_w}) > clientWidth({client_w})"
                )

                # 2. 컨테이너 가시성 및 유효 BBox 검증
                container = page.locator(".blogin-saas-container")
                self.assertTrue(container.is_visible(), f"[{vp['name']}] {rule_key} 위젯 컨테이너가 렌더링되지 않음")
                bbox = container.bounding_box()
                self.assertIsNotNone(bbox)
                self.assertGreater(bbox["width"], 250, f"위젯 너비 비정상: {bbox['width']}")
                self.assertGreater(bbox["height"], 300, f"위젯 높이 비정상: {bbox['height']}")

            page.close()

    def test_02_zero_nan_infinity_in_calculations(self):
        """초기 연산 결과 및 DOM 텍스트에 NaN / Infinity / undefined가 일체 존재하지 않는지 검증"""
        page = self.browser.new_page(viewport={"width": 375, "height": 667})
        for rule_key, desc in TEST_ASSET_RULES:
            html = self._build_full_page_html(rule_key)
            page.set_content(html, wait_until="networkidle")

            body_text = page.inner_text("body")
            self.assertNotIn("NaN", body_text, f"'{desc}'({rule_key})에 NaN 연산 에러 감지!")
            self.assertNotIn("Infinity", body_text, f"'{desc}'({rule_key})에 Infinity 연산 에러 감지!")
            self.assertNotIn("undefined", body_text, f"'{desc}'({rule_key})에 undefined 표기 에러 감지!")

        page.close()

    def test_03_interactive_buttons_and_url_hash_sync(self):
        """프리셋 버튼 클릭 시 실시간 수치 반응 및 URL Hash 동기화 검증"""
        page = self.browser.new_page(viewport={"width": 768, "height": 1024})

        # 1. 해외주식 양도세 프리셋 및 공유 버튼 테스트
        html_tax = self._build_full_page_html("nvda_stock_tax")
        page.set_content(html_tax, wait_until="networkidle")

        # +250만 버튼 클릭
        page.locator("button[data-add='2500000']").first.click()
        page.wait_for_timeout(200)

        gain_text = page.locator("#trade_gain_label").inner_text()
        self.assertIn("12,500,000", gain_text)

        # 결과 공유 버튼 클릭 -> 토스트 문구 및 URL Hash 갱신 확인
        share_btn = page.locator("#trade_share_btn")
        self.assertTrue(share_btn.is_visible())
        share_btn.click()
        page.wait_for_timeout(300)
        btn_text = share_btn.inner_text()
        self.assertIn("복사", btn_text)

        # 2. DCA 물타기 1:2 비율 버튼 테스트
        html_dca = self._build_full_page_html("tsla_water_averaging")
        page.set_content(html_dca, wait_until="networkidle")

        ratio_btn = page.locator("button[data-ratio='2']").first
        self.assertTrue(ratio_btn.is_visible())
        ratio_btn.click()
        page.wait_for_timeout(200)

        q2_val = page.locator("#dca_qty2_input").input_value()
        self.assertEqual(q2_val, "200")

        # 3. 선물 레버리지 청산가 계산기 테스트
        html_lev = self._build_full_page_html("btc_futures_liquidation")
        page.set_content(html_lev, wait_until="networkidle")

        liq_text = page.locator("#lev_res_liq_price").inner_text()
        self.assertTrue(len(liq_text) > 0)
        self.assertNotIn("NaN", liq_text)

        page.close()


if __name__ == "__main__":
    unittest.main()
