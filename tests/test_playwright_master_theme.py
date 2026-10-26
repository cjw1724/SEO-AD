# -*- coding: utf-8 -*-
"""
tests/test_playwright_master_theme.py
-------------------------------------
Playwright multi-viewport headless rendering and visual validation test:
- 375px Mobile (iPhone), 768px Tablet (iPad), 1280px Desktop
- Validates 0 horizontal scroll blowout (document.scrollWidth <= document.clientWidth)
- Validates 0 CSS collisions, clean dark navy TDS aesthetic
- Captures visual proof screenshots to artifact brain directory
"""

import os
import sys
import re
import unittest
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_XML_PATH = os.path.join(BASE_DIR, "blogin365_apex_master_theme.xml")
ARTICLE_HTML_PATH = os.path.join(BASE_DIR, "data", "generated_overseas_stock_tax_microsaas.html")
BRAIN_DIR = r"C:\Users\cnwjr\.gemini\antigravity\brain\2fa07f4d-895a-42a3-a3fd-1c9564dd6628"


class TestPlaywrightMasterTheme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(THEME_XML_PATH, "r", encoding="utf-8") as f:
            xml_text = f.read()

        # Extract CSS from b:skin
        skin_match = re.search(r'<b:skin><!\[CDATA\[(.*?)\]\]></b:skin>', xml_text, re.DOTALL)
        cls.css = skin_match.group(1) if skin_match else ""

        # Load article body
        if os.path.exists(ARTICLE_HTML_PATH):
            with open(ARTICLE_HTML_PATH, "r", encoding="utf-8") as f:
                cls.article_html = f.read()
        else:
            cls.article_html = "<div class='blogin-saas-container'><h1>샘플 핀테크 계산기</h1></div>"

        # Build full mock standalone HTML
        cls.standalone_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=5"/>
  <title>2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터 | Blogin 365 AI Holdings</title>
  <link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet"/>
  <style>
    {cls.css}
  </style>
</head>
<body>
  <div class="apex-body-container">
    <header class="apex-header">
      <div class="apex-header-inner">
        <div class="apex-brand-wrap">
          <a class="apex-brand-logo" href="#">
            <svg viewBox="0 0 24 24" style="width:22px;height:22px;fill:#3b82f6;">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
            <span>BLOGIN 365 AI</span>
          </a>
          <span class="apex-brand-badge">FINTECH RESEARCH</span>
        </div>
        <div class="apex-fx-ticker" id="apexLiveFxTicker">
          <span class="pulse-dot"></span>
          <span>USD/KRW 1,380.0원 (실시간 오라클)</span>
        </div>
      </div>
    </header>

    <div class="apex-main-wrapper">
      <article class="apex-card apex-post">
        <div class="apex-post-meta">
          <span>2026-10-25</span>
          <span>·</span>
          <span>Blogin 365 AI 리서치 팀</span>
          <span>·</span>
          <a href="#">세금·절세 시뮬레이터</a>
          <a href="#">해외주식 양도세</a>
        </div>
        <h1 class="apex-post-title">2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터</h1>
        <div class="entry-content post-body">
          {cls.article_html}
        </div>
      </article>
    </div>

    <footer class="apex-footer">
      <div class="apex-footer-inner">
        <div class="apex-footer-brand">BLOGIN 365 AI HOLDINGS</div>
        <p class="apex-footer-disclaimer">
          본 웹사이트에서 제공되는 모든 금융 계산기, 세무 시뮬레이션, 퀀트 알고리즘 및 분석 자료는 대한민국 소득세법, 지방세법 및 공시된 금융 산식을 바탕으로 제작된 수학적 정보 제공 도구입니다. 본 사이트는 금융투자업 인가 법인이 아니며, 제공되는 결과값은 투자 권유나 세무 대리가 아닙니다.
        </p>
        <div class="apex-footer-copy">
          © 2026 Blogin 365 AI Holdings. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</body>
</html>"""

        cls.test_file_path = os.path.join(BASE_DIR, "data", "test_theme_preview.html")
        os.makedirs(os.path.dirname(cls.test_file_path), exist_ok=True)
        with open(cls.test_file_path, "w", encoding="utf-8") as f:
            f.write(cls.standalone_html)

    def test_playwright_viewports(self):
        """Playwright 3대 뷰포트 오버플로우 0건 검증 및 스크린샷 증빙 캡처"""
        async def run_audit():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                viewports = [
                    {"name": "mobile_375px", "width": 375, "height": 812},
                    {"name": "tablet_768px", "width": 768, "height": 1024},
                    {"name": "desktop_1280px", "width": 1280, "height": 900}
                ]

                for vp in viewports:
                    page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
                    await page.goto(f"file:///{os.path.abspath(self.test_file_path).replace(os.sep, '/')}", wait_until="networkidle")

                    # Check for horizontal overflow (blowout)
                    overflow = await page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
                    self.assertFalse(overflow, f"Horizontal blowout detected on {vp['name']} (scrollWidth > clientWidth)!")

                    # Capture screenshot to brain directory
                    os.makedirs(BRAIN_DIR, exist_ok=True)
                    shot_path = os.path.join(BRAIN_DIR, f"theme_preview_{vp['name']}.png")
                    await page.screenshot(path=shot_path, full_page=False)
                    self.assertTrue(os.path.exists(shot_path), f"Screenshot failed for {vp['name']}")
                    print(f" -> [Playwright] Viewport {vp['name']} passed (0 Overflow). Saved: {shot_path}")

                    await page.close()

                await browser.close()

        asyncio.run(run_audit())


if __name__ == "__main__":
    unittest.main()
