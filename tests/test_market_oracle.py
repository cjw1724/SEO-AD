# -*- coding: utf-8 -*-
"""
tests/test_market_oracle.py
----------------------------
실시간 환율 및 마켓 데이터 오라클 무결성 테스트
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.fintech.market_oracle import MarketDataOracle, DEFAULT_USD_KRW_RATE


class TestMarketDataOracle(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_file = os.path.join(self.temp_dir.name, "test_market_cache.json")
        self.oracle = MarketDataOracle(cache_file=self.cache_file, ttl_seconds=3600)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_usd_krw_rate_returns_reasonable_value(self):
        """USD/KRW 환율이 1,000원 이상 2,000원 이하의 정상 범위로 도출되는지 검증"""
        rate = self.oracle.get_usd_krw_rate()
        self.assertIsInstance(rate, float)
        self.assertGreaterEqual(rate, 1000.0)
        self.assertLessEqual(rate, 2000.0)
        self.assertTrue(os.path.exists(self.cache_file), "Cache file should be created upon fetching rate")

    def test_02_cache_reuse_within_ttl(self):
        """TTL 1시간 내에 캐시된 환율이 네트워크 호출 없이 즉시 재사용되는지 검증"""
        self.oracle.cache["USD_KRW"] = {
            "rate": 1395.50,
            "timestamp": 9999999999.0,
            "source": "mock_cache"
        }
        self.oracle._save_cache()

        rate = self.oracle.get_usd_krw_rate()
        self.assertEqual(rate, 1395.50)

    def test_03_fallback_when_offline(self):
        """완전 오프라인/네트워크 장애 시 안전 상수(1380.0)로 Graceful Fallback 검증"""
        with patch.object(self.oracle, "_fetch_yahoo_fx", return_value=None), \
             patch.object(self.oracle, "_fetch_open_er_fx", return_value=None):
            self.oracle.cache.clear()
            rate = self.oracle.get_usd_krw_rate()
            self.assertEqual(rate, DEFAULT_USD_KRW_RATE)

    def test_04_ticker_price_fetching_and_fallback(self):
        """주요 자산(NVDA, BTC) 티커 시세 조회 및 Fallback 검증"""
        nvda_price = self.oracle.get_ticker_price("NVDA")
        self.assertGreater(nvda_price, 0)
        self.assertIsInstance(nvda_price, float)

        btc_price = self.oracle.get_ticker_price("BTC")
        self.assertGreater(btc_price, 1000)

        # 알 수 없는 가짜 티커 요청 시 Fallback 기본가(100.0) 반환 검증
        unknown_price = self.oracle.get_ticker_price("NONEXISTENT_TICKER_XYZ")
        self.assertEqual(unknown_price, 100.0)

    def test_05_client_side_fx_script_generation(self):
        """클라이언트 사이드 Vanilla JS 비동기 주입 스크립트 규격 검증"""
        script = self.oracle.get_client_fx_script(fallback_rate=1385.0)
        self.assertIn("<script>", script)
        self.assertIn("FALLBACK_FX = 1385.0;", script)
        self.assertIn("blogin-fx-input", script)
        self.assertIn("blogin-fx-label", script)
        self.assertIn("open.er-api.com", script)


if __name__ == "__main__":
    unittest.main()
