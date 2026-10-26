# -*- coding: utf-8 -*-
"""
engine/crew/thumbnail_generator.py
-----------------------------------
HTML/CSS 카드 템플릿 기반 Playwright WebP 썸네일 생성기
- 1200x630 규격 오픈그래프(OG) 카드
- 고해상도 WebP 스냅샷
"""

import os
import asyncio
from playwright.async_api import async_playwright


class PlaywrightThumbnailGenerator:
    def __init__(self, output_dir: str = "data/thumbnails"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _render_html_template(self, title: str, formula_badge: str, key_stat: str, sub_label: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
          <meta charset="UTF-8">
          <style>
            * {{
              box-sizing: border-box;
              margin: 0;
              padding: 0;
              font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
              word-break: keep-all;
            }}
            body {{
              width: 1200px;
              height: 630px;
              display: flex;
              align-items: center;
              justify-content: center;
              background: #090d16;
              overflow: hidden;
            }}
            .card {{
              width: 1140px;
              height: 570px;
              background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
              border: 2px solid #334155;
              border-radius: 28px;
              padding: 56px 64px;
              display: flex;
              flex-direction: column;
              justify-content: space-between;
              box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
              position: relative;
            }}
            .card::before {{
              content: "";
              position: absolute;
              top: -80px;
              right: -80px;
              width: 380px;
              height: 380px;
              background: radial-gradient(circle, rgba(56, 189, 248, 0.16) 0%, rgba(0, 0, 0, 0) 70%);
              border-radius: 50%;
            }}
            .header {{
              display: flex;
              align-items: center;
              gap: 16px;
            }}
            .badge-brand {{
              background: #2563eb;
              color: #ffffff;
              font-size: 15px;
              font-weight: 800;
              padding: 8px 18px;
              border-radius: 9999px;
              letter-spacing: 0.05em;
              white-space: nowrap;
            }}
            .badge-formula {{
              background: #1e293b;
              color: #38bdf8;
              border: 1px solid #0284c7;
              font-size: 15px;
              font-weight: 700;
              padding: 8px 18px;
              border-radius: 9999px;
              max-width: 800px;
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
              word-break: keep-all;
            }}
            .title-box {{
              margin: 16px 0;
            }}
            .title {{
              font-size: 42px;
              font-weight: 900;
              color: #f8fafc;
              line-height: 1.35;
              letter-spacing: -0.03em;
              word-break: keep-all;
            }}
            .footer-stat {{
              display: flex;
              justify-content: space-between;
              align-items: flex-end;
              border-top: 1px solid #334155;
              padding-top: 26px;
              gap: 24px;
            }}
            .stat-group {{
              display: flex;
              flex-direction: column;
              gap: 6px;
              flex: 1;
              min-width: 0;
              max-width: 780px;
            }}
            .stat-label {{
              font-size: 15px;
              color: #94a3b8;
              font-weight: 700;
              letter-spacing: 0.02em;
              white-space: nowrap;
              word-break: keep-all;
            }}
            .stat-value {{
              font-size: 28px;
              color: #38bdf8;
              font-weight: 900;
              letter-spacing: -0.02em;
              line-height: 1.25;
              word-break: keep-all;
            }}
            .watermark {{
              font-size: 14px;
              color: #64748b;
              font-weight: 700;
              letter-spacing: 0.05em;
              white-space: nowrap;
              flex-shrink: 0;
            }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="header">
              <span class="badge-brand">MICRO-SAAS TOOL</span>
              <span class="badge-formula">{formula_badge}</span>
            </div>
            
            <div class="title-box">
              <h1 class="title">{title}</h1>
            </div>

            <div class="footer-stat">
              <div class="stat-group">
                <span class="stat-label">{sub_label}</span>
                <span class="stat-value">{key_stat}</span>
              </div>
              <span class="watermark">BLOGIN 365 AI ENGINE · RUNTIME BENCHMARK</span>
            </div>
          </div>
        </body>
        </html>
        """

    async def generate_thumbnail(self, filename: str, title: str, formula_badge: str, key_stat: str, sub_label: str = "BENCHMARK SPEC") -> str:
        out_path = os.path.join(self.output_dir, f"{filename}.webp")
        html_content = self._render_html_template(title, formula_badge, key_stat, sub_label)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1200, "height": 630})
            await page.set_content(html_content, wait_until="networkidle")
            await page.screenshot(path=out_path, type="webp", quality=90)
            await browser.close()

        return out_path


def create_thumbnail_sync(filename: str, title: str, formula_badge: str, key_stat: str, sub_label: str = "BENCHMARK SPEC", output_dir: str = "data/thumbnails") -> str:
    gen = PlaywrightThumbnailGenerator(output_dir=output_dir)
    return asyncio.run(gen.generate_thumbnail(filename, title, formula_badge, key_stat, sub_label))
