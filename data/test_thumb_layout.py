import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright
from engine.crew.thumbnail_generator import PlaywrightThumbnailGenerator
from engine.crew.dataset_resolver import TradingDatasetResolver

async def inspect_all():
    resolver = TradingDatasetResolver()
    gen = PlaywrightThumbnailGenerator()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 630})
        for key in ['overseas_stock_tax', 'water_averaging_dca', 'leverage_liquidation_kelly', 'dividend_compound_tax']:
            r = resolver.resolve_topic(key)
            html = gen._render_html_template(r['target_keyword'], r['formula_badge'], r['key_stat'], r['sub_label'])
            html_fixed = html.replace('font-size: 32px;', 'font-size: 28px;').replace('white-space: nowrap;', '').replace('overflow: hidden;', '').replace('text-overflow: ellipsis;', '')
            await page.set_content(html_fixed, wait_until='networkidle')
            val = await page.eval_on_selector('.stat-value', 'el => ({h: el.offsetHeight, w: el.offsetWidth, scrollW: el.scrollWidth, clientW: el.clientWidth})')
            wm = await page.eval_on_selector('.watermark', 'el => ({left: el.getBoundingClientRect().left})')
            stat_right = await page.eval_on_selector('.stat-value', 'el => el.getBoundingClientRect().right')
            gap = wm['left'] - stat_right
            overflow = val['scrollW'] > val['clientW']
            print(f"[{key}] h={val['h']}, gap={gap:.1f}px, overflow={overflow}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_all())
