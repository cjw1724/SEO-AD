# -*- coding: utf-8 -*-
"""
tests/test_strategy_lab_renderer.py
-----------------------------------
Unit tests for Vibe Strategy Lab Renderer (v9.0 Apex).
Verifies:
1. Preset configs availability
2. HTML generation integrity
3. Lightweight Charts script presence
4. In-browser backtester & Binance WebSocket endpoints
5. Interactive slider elements and KPI boxes
6. Dark theme WCAG contrast classes
"""

import unittest
from engine.visuals.strategy_lab_renderer import StrategyLabRenderer


class TestStrategyLabRenderer(unittest.TestCase):
    def setUp(self):
        self.presets = StrategyLabRenderer.get_strategy_presets()

    def test_presets_exist(self):
        self.assertIn("wonyotti_bollinger_reversal", self.presets)
        self.assertIn("supertrend_rsi_scalping", self.presets)
        self.assertIn("larry_williams_breakout", self.presets)

        wonyotti = self.presets["wonyotti_bollinger_reversal"]
        self.assertEqual(wonyotti["symbol"], "BTCUSDT")
        self.assertEqual(wonyotti["interval"], "15m")
        self.assertIn("bb_period", wonyotti["default_params"])
        self.assertIn("tp_percent", wonyotti["default_params"])

    def test_render_default_html_structure(self):
        html = StrategyLabRenderer.render()

        # 1. Essential IDs & Wrappers
        self.assertIn('id="vibe-strategy-lab-root"', html)
        self.assertIn('id="tv-strategy-chart"', html)
        self.assertIn('id="kpi-winrate"', html)
        self.assertIn('id="kpi-trades"', html)
        self.assertIn('id="kpi-pf"', html)
        self.assertIn('id="kpi-mdd"', html)
        self.assertIn('id="kpi-pnl"', html)

        # 2. Sliders
        self.assertIn('id="slider-bb-period"', html)
        self.assertIn('id="slider-bb-std"', html)
        self.assertIn('id="slider-vol-mult"', html)
        self.assertIn('id="slider-rsi-th"', html)
        self.assertIn('id="slider-tp"', html)
        self.assertIn('id="slider-sl"', html)
        self.assertIn('id="slider-lev"', html)

        # 3. Paper Trading Follow Toggle
        self.assertIn('id="toggle-follow-strategy"', html)
        self.assertIn('id="live-paper-status-bar"', html)

        # 4. Lightweight Charts Library CDN
        self.assertIn('lightweight-charts@4.1.1', html)

        # 5. Binance Endpoints
        self.assertIn('api.binance.com/api/v3/klines', html)
        self.assertIn('wss://stream.binance.com:9443', html)

        # 6. Flagship Backlink Button
        self.assertIn('/p/vibe-trading.html', html)

        # 7. Toss Dark Theme Colors
        self.assertIn('#0a0e17', html)
        self.assertIn('#111827', html)
        self.assertIn('#f8fafc', html)

        # 8. Dual-Directional Long/Short Quantitative Engine
        self.assertIn('BUY (롱)', html)
        self.assertIn('SELL (숏)', html)
        self.assertIn('TP (숏)', html)

    def test_custom_config_override(self):
        custom_cfg = {
            "strategy_id": "custom_eth_scalp",
            "title": "이더리움 1분봉 초단타 퀀트 랩",
            "subtitle": "ETHUSDT 실시간 캔들 백테스트",
            "symbol": "ETHUSDT",
            "interval": "1m",
            "default_params": {
                "bb_period": 15,
                "bb_std": 2.2,
                "vol_mult": 2.0,
                "rsi_threshold": 30,
                "tp_percent": 1.5,
                "sl_percent": 0.8,
                "leverage": 5
            },
            "strategy_description": "이더리움 1분봉 볼린저 하단 터치 시 2.0배 거래량 확인 후 진입"
        }
        html = StrategyLabRenderer.render(custom_cfg)

        self.assertIn("이더리움 1분봉 초단타 퀀트 랩", html)
        self.assertIn("ETHUSDT", html)
        self.assertIn("1m", html)
        self.assertIn("ETHUSDT 실시간 캔들 백테스트", html)


if __name__ == "__main__":
    unittest.main()
