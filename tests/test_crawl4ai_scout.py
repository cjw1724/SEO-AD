# -*- coding: utf-8 -*-
"""
tests/test_crawl4ai_scout.py
----------------------------
Unit & Integration Tests for Crawl4AI Zero-Cost Real-Time Data Extractor:
  1. Crawl4AIScout initialization and configuration
  2. HTML Table to Markdown parsing engine
  3. Tier 1 / Tier 2 fallback parser mechanism
  4. Tier 3 Deterministic Authoritative Factset Vault
  5. PublicDataScout & ExperientialVerifier integration
"""

import os
import sys
import unittest
from unittest import mock
import warnings
from bs4 import BeautifulSoup

# Ensure UTF-8 & suppress playwright resource warnings
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore", category=ResourceWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.radar.crawl4ai_scout import Crawl4AIScout, html_table_to_markdown
from engine.radar.public_data_scout import PublicDataScout


class TestCrawl4AIScout(unittest.TestCase):
    def setUp(self):
        self.scout = Crawl4AIScout(timeout=5, headless=True)

    def test_scout_initialization(self):
        """Verifies proper scout configuration and deterministic vaults."""
        self.assertEqual(self.scout.timeout, 5)
        self.assertTrue(self.scout.headless)
        self.assertIn("청년도약계좌", self.scout.DETERMINISTIC_TABLE_VAULT)
        self.assertIn("근로장려금", self.scout.DETERMINISTIC_TABLE_VAULT)
        self.assertIn("알뜰폰", self.scout.DETERMINISTIC_TABLE_VAULT)

    def test_html_table_to_markdown_converter(self):
        """Verifies clean conversion of raw HTML <table> to Markdown table."""
        sample_html = """
        <table>
            <thead>
                <tr><th>소득구간</th><th>지원비율</th><th>최대한도</th></tr>
            </thead>
            <tbody>
                <tr><td>2400만원 이하</td><td>6.0%</td><td>월 2.4만원</td></tr>
                <tr><td>3600만원 이하</td><td>4.6%</td><td>월 2.3만원</td></tr>
            </tbody>
        </table>
        """
        soup = BeautifulSoup(sample_html, "html.parser")
        table_tag = soup.find("table")
        md_table = html_table_to_markdown(table_tag)

        self.assertIn("| 소득구간 | 지원비율 | 최대한도 |", md_table)
        self.assertIn("| 2400만원 이하 | 6.0% | 월 2.4만원 |", md_table)
        self.assertIn("| --- |", md_table)

    def test_markdown_table_extractor(self):
        """Verifies regex extraction of markdown tables from page text."""
        md_text = (
            "# 정책 안내\n\n"
            "| 구분 | 기준 | 혜택 |\n"
            "|---|---|---|\n"
            "| 청년 | 만 19~34세 | 비과세 |\n"
            "| 일반 | 전 연령 | 기본이자 |\n\n"
            "기타 안내 사항입니다."
        )
        tables = self.scout._extract_tables_from_markdown(md_text)
        self.assertEqual(len(tables), 1)
        self.assertIn("만 19~34세", tables[0])

    def test_tier3_deterministic_fallback_policy_tables(self):
        """Verifies 100% crash-proof Tier 3 fallback returns authoritative tables."""
        res = self.scout.extract_rich_policy_tables("2026 청년도약계좌", portal_url=None)
        self.assertTrue(res["success"])
        self.assertIn(res["method"], ["deterministic_vault", "crawl4ai", "soup_fallback"])
        self.assertTrue(res["primary_table"], "Primary table must not be empty")
        self.assertIn("정부 매칭 기여금 비율", res["primary_table"])

    def test_tier2_soup_fallback_mock(self):
        """Verifies Tier 2 BeautifulSoup crawler cleanly parses HTML on network simulation."""
        mock_html = b"""
        <html>
            <head><title>Test Policy Page</title></head>
            <body>
                <main>
                    <h1>2026 \xec\xa0\x95\xeb\xb6\x80 \xec\xa7\x80\xec\x9b\x90\xea\xb8\x88</h1>
                    <p>\xec\x8b\xa0\xec\xb2\xad \xec\x9e\x90\xea\xb2\xa9\xea\xb3\xbc \xec\xa1\xb0\xea\xb1\xb4\xec\x9d\x84 \xed\x95\x9c\xeb\x88\x88\xec\x97\x90 \xed\x99\x95\xec\x9d\xb8\xed\x95\xa9\xeb\x8b\x88\xeb\x8b\xa4.</p>
                    <table>
                        <tr><th>\xec\x9c\xa0\xed\x98\x95</th><th>\xec\xa7\x80\xec\x9b\x90\xec\x95\xa1</th></tr>
                        <tr><td>\xeb\x8b\xa8\xeb\x8f\x85</td><td>165\xeb\xa7\x8c\xec\x9b\x90</td></tr>
                    </table>
                </main>
            </body>
        </html>
        """
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_resp = mock.MagicMock()
            mock_resp.read.return_value = mock_html
            mock_resp.__enter__.return_value = mock_resp
            mock_urlopen.return_value = mock_resp

            result = self.scout._crawl_with_soup("https://example.gov.kr/policy")
            self.assertTrue(result["success"])
            self.assertEqual(result["method"], "soup_fallback")
            self.assertEqual(result["title"], "Test Policy Page")
            self.assertGreaterEqual(len(result["tables"]), 1)

    def test_public_data_scout_integration(self):
        """Verifies PublicDataScout returns live tables and markdown context."""
        p_scout = PublicDataScout()
        fact = p_scout.verify_official_facts("2026 근로장려금 정기신청", category="SUBSIDY")
        
        self.assertTrue(fact["is_verified"])
        self.assertEqual(fact["department"], "국세청 소득지원국")
        self.assertIn("live_tables", fact)
        self.assertIn("primary_table", fact)
        self.assertIn("live_markdown", fact)
        self.assertIn("crawl_method", fact)
        self.assertGreater(len(fact["primary_table"]), 0)

    def test_empty_or_irrelevant_crawl_preserves_vault_markdown(self):
        """Verifies when a crawled page has no tables/relevant text, vault table and facts are preserved in live_markdown."""
        # Simulate a crawl result that has success=True but 0 tables and irrelevant generic text
        with mock.patch.object(self.scout, "crawl_page_sync") as mock_crawl:
            mock_crawl.return_value = {
                "url": "https://portal.example.go.kr",
                "success": True,
                "method": "soup_fallback",
                "markdown": "공식 누리집 메인 메뉴 바로가기 로그인 회원가입",
                "tables": [],
                "title": "공식 누리집",
                "status_code": 200,
                "error": None
            }
            res = self.scout.extract_rich_policy_tables("2026 청년도약계좌", portal_url="https://portal.example.go.kr")
            self.assertTrue(res["success"])
            self.assertEqual(res["method"], "soup_fallback_with_vault")
            self.assertIn("정부 매칭 기여금 비율", res["primary_table"])
            self.assertIn("정부 매칭 기여금 비율", res["live_markdown"])
            self.assertIn("공식 기준 요약", res["live_markdown"])

    def test_public_data_scout_registry_immutability(self):
        """Verifies verify_official_facts does not mutate the class-level GOVERNMENT_PORTAL_REGISTRY."""
        p_scout = PublicDataScout()
        self.assertNotIn("matched_key", PublicDataScout.GOVERNMENT_PORTAL_REGISTRY["근로장려금"])
        p_scout.verify_official_facts("근로장려금", fetch_live_table=False)
        self.assertNotIn("matched_key", PublicDataScout.GOVERNMENT_PORTAL_REGISTRY["근로장려금"])

    def test_expanded_vault_coverage(self):
        """Verifies newly added high-CPC niches are present and well-formed."""
        niches = ["신생아특례", "버팀목", "국민연금", "종합소득세", "트래블로그", "실비보험", "임플란트"]
        for niche in niches:
            self.assertIn(niche, self.scout.DETERMINISTIC_TABLE_VAULT)
            table_text = self.scout.DETERMINISTIC_TABLE_VAULT[niche]
            self.assertIn("|", table_text)
            self.assertGreaterEqual(len(table_text.splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
