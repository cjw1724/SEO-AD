# -*- coding: utf-8 -*-
"""
Unit Test Suite for CanvasChartGenerator & PaperTradeEngine.
Verifies HTML5 Canvas chart generation, financial mathematics (PnL, liquidation, Kelly),
DOM structure integrity, LocalStorage persistence scripts, and Schema.org compliance.
"""
import os
import sys
import json
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.fintech.chart_oracle import CanvasChartGenerator, MarketStreamOracle
from engine.fintech.paper_trade_engine import PaperTradeEngine
from engine.crew.dataset_resolver import TradingDatasetResolver


class TestCanvasChartGenerator(unittest.TestCase):
    """Verifies ultra-lightweight HTML5 Canvas candlestick chart generation."""

    def setUp(self):
        self.generator = CanvasChartGenerator()

    def test_generate_chart_html_structure(self):
        """Checks if generated HTML contains canvas, live HUD, and 3-tier streaming script."""
        html = self.generator.generate_chart_html(
            ticker="NVDA",
            initial_price=140.50,
            currency="USD",
        )
        self.assertIn("blogin-chart-nvda-canvas", html)
        self.assertIn("<canvas", html)
        self.assertIn("NVDA 실시간 차트", html)
        self.assertIn("$140.50", html)
        self.assertIn("WSS 실시간 스트림", html)
        self.assertIn("blogin_price_tick", html)  # CustomEvent dispatched for paper trade engine
        self.assertIn("drawChart", html)
        self.assertIn("MA(5)", html)
        self.assertIn("MA(20)", html)


class TestPaperTradeEngineMath(unittest.TestCase):
    """Verifies financial mathematics: PnL, liquidation price, and Kelly criterion."""

    def setUp(self):
        self.engine = PaperTradeEngine()

    def test_long_and_short_pnl(self):
        """Verifies Long and Short unrealized PnL formulas."""
        # Long: (120 - 100) * 2 * 5 = 200.0
        long_pnl = self.engine.calculate_long_pnl(entry_price=100.0, current_price=120.0, quantity=2.0, leverage=5.0)
        self.assertAlmostEqual(long_pnl, 200.0, places=2)

        # Short: (100 - 80) * 2 * 5 = 200.0
        short_pnl = self.engine.calculate_short_pnl(entry_price=100.0, current_price=80.0, quantity=2.0, leverage=5.0)
        self.assertAlmostEqual(short_pnl, 200.0, places=2)

        # Loss check (Long drop)
        long_loss = self.engine.calculate_long_pnl(entry_price=100.0, current_price=90.0, quantity=1.0, leverage=1.0)
        self.assertAlmostEqual(long_loss, -10.0, places=2)

    def test_liquidation_price(self):
        """Verifies liquidation price calculation across leverage tiers."""
        # Long 10x with 0.005 maintenance margin: 100 * (1 - 0.1 + 0.005) = 90.5
        long_liq = self.engine.calculate_liquidation_price(entry_price=100.0, is_long=True, leverage=10.0, maintenance_margin=0.005)
        self.assertAlmostEqual(long_liq, 90.5, places=2)

        # Short 10x with 0.005 maintenance margin: 100 * (1 + 0.1 - 0.005) = 109.5
        short_liq = self.engine.calculate_liquidation_price(entry_price=100.0, is_long=False, leverage=10.0, maintenance_margin=0.005)
        self.assertAlmostEqual(short_liq, 109.5, places=2)

        # Spot 1x (No liquidation)
        spot_long_liq = self.engine.calculate_liquidation_price(entry_price=100.0, is_long=True, leverage=1.0)
        self.assertEqual(spot_long_liq, 0.0)

    def test_kelly_criterion(self):
        """Verifies Kelly fraction calculation and edge bounds."""
        # 60% win rate, 1.5 payout ratio: f* = (0.6 * 2.5 - 1) / 1.5 = 0.5 / 1.5 = 0.3333
        f_star = self.engine.calculate_kelly_fraction(win_rate=0.6, profit_loss_ratio=1.5)
        self.assertAlmostEqual(f_star, 0.3333, places=3)

        # Losing strategy (30% win rate, 1.0 ratio): f* <= 0 -> clamped to 0.0
        f_zero = self.engine.calculate_kelly_fraction(win_rate=0.3, profit_loss_ratio=1.0)
        self.assertEqual(f_zero, 0.0)


class TestPaperTradeEngineDOMAndSchema(unittest.TestCase):
    """Verifies DOM elements, LocalStorage persistence, URL sharing, and Schema.org JSON-LD."""

    def setUp(self):
        self.engine = PaperTradeEngine()

    def test_generate_widget_html(self):
        """Checks if interactive paper trading widget contains essential controls."""
        html = self.engine.generate_widget_html(
            ticker="BTC",
            initial_price=95000.0,
            currency="USD",
            default_seed=10000.0,
        )
        self.assertIn("100% 가상 모의투자 시뮬레이터", html)
        self.assertIn("자본시장법 제101조", html)
        self.assertIn("blogin-paper-btc-equity", html)
        self.assertIn("blogin-paper-btc-btn-buy", html)
        self.assertIn("blogin-paper-btc-btn-sell", html)
        self.assertIn("blogin-paper-btc-btn-share", html)
        self.assertIn("localStorage.setItem", html)
        self.assertIn("#paper=1", html)  # Viral sharing hash
        self.assertIn("바이낸스", html)

    def test_schema_json_ld(self):
        """Verifies valid JSON-LD structure conforming to Schema.org."""
        json_ld_str = self.engine.generate_schema_json_ld(ticker="TSLA", post_url="https://blogin365ai.blogspot.com/tsla.html")
        self.assertIn('<script type="application/ld+json">', json_ld_str)
        raw_json = json_ld_str.replace('<script type="application/ld+json">', '').replace('</script>', '').strip()
        data = json.loads(raw_json)

        self.assertEqual(data["@context"], "https://schema.org")
        self.assertIn("FinancialApplication", data["@type"])
        self.assertIn("TSLA", data["name"])
        self.assertIn("offers", data)


class TestDatasetResolverPaperTradingIntegration(unittest.TestCase):
    """Verifies TradingDatasetResolver integration with the paper trading component."""

    def setUp(self):
        self.resolver = TradingDatasetResolver()

    def test_render_paper_trading_component(self):
        """Checks if dataset resolver bundles chart, paper trade widget, and schema."""
        bundle = self.resolver.render_paper_trading_component("nvda_stock_tax")
        self.assertIn("blogin-chart-nvda-canvas", bundle)
        self.assertIn("blogin-paper-nvda-container", bundle)
        self.assertIn("application/ld+json", bundle)
        self.assertIn("NVDA 실시간 차트", bundle)


if __name__ == "__main__":
    unittest.main()
