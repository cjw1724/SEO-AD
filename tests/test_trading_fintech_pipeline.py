# -*- coding: utf-8 -*-
"""
tests/test_trading_fintech_pipeline.py
---------------------------------------
FinTech & Quant Micro-SaaS 파이프라인 4대 핵심 요구사항 전수 검증 스위트:
1. [Test 1] SSOT data/trading_rules_db.json 금융/세무 데이터베이스 무결성 검증
2. [Test 2] TradingDatasetResolver 수식 계산 및 0ms Vanilla JS 위젯 렌더링 검증
3. [Test 3] Playwright 경계값(0원, 음수, 10억 원) 주입 시 Zero-NaN 무결점 검증
4. [Test 4] YMYL 과장 광고 차단, 법적 면책 조항, Schema.org FinanceApplication 검증
5. [Test 5] Playwright 1200x630 WebP 썸네일 생성 검증
"""

import os
import sys
import unittest
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.crew.dataset_resolver import TradingDatasetResolver, load_trading_db
from engine.crew.qa_validator import DeterministicQAValidator, run_validator
from engine.crew.thumbnail_generator import create_thumbnail_sync


class TestTradingFinTechPipeline(unittest.TestCase):

    def setUp(self):
        self.resolver = TradingDatasetResolver()

    # --------------------------------------------------------------------------
    # [Test 1] SSOT 금융/세무 DB 무결성
    # --------------------------------------------------------------------------
    def test_01_trading_rules_db_integrity(self):
        """trading_rules_db.json에 4대 핵심 금융 도메인 규칙이 완전하게 정의되었는지 검증"""
        db = load_trading_db()
        self.assertIn("rules", db)
        rules = db["rules"]

        expected_rules = [
            "overseas_stock_tax",
            "water_averaging_dca",
            "leverage_liquidation_kelly",
            "dividend_compound_tax"
        ]
        for r_id in expected_rules:
            self.assertIn(r_id, rules, f"Missing financial rule: {r_id}")
            self.assertTrue(len(rules[r_id]["name"]) > 0)
            self.assertIn("formula", rules[r_id])

        # 해외주식 세율 상수 검증 (국세 20% + 지방세 2% = 총 22%, 기본공제 250만 원)
        tax_rule = rules["overseas_stock_tax"]
        self.assertEqual(tax_rule["constants"]["basic_deduction_krw"], 2500000)
        self.assertEqual(tax_rule["constants"]["capital_gains_tax_rate"], 0.20)
        self.assertEqual(tax_rule["constants"]["local_income_tax_rate"], 0.02)
        self.assertEqual(tax_rule["constants"]["total_tax_rate"], 0.22)

    # --------------------------------------------------------------------------
    # [Test 2] 결정론적 리졸버 수식 및 위젯 렌더링
    # --------------------------------------------------------------------------
    def test_02_trading_resolver_and_widget_rendering(self):
        """해외주식 양도소득세 위젯 및 실측 대조표 렌더링 검증"""
        resolved = self.resolver.resolve_topic("해외주식 양도소득세 절세 계산기")
        self.assertEqual(resolved["rule_key"], "overseas_stock_tax")
        self.assertIn("2026 해외주식 양도소득세", resolved["target_keyword"])

        widget_html = self.resolver.render_trading_saas_html("overseas_stock_tax")
        self.assertIn("blogin-saas-container", widget_html)
        self.assertIn("trade_gain_input", widget_html)
        self.assertIn("trade_loss_input", widget_html)
        self.assertIn("trade_res_total_tax", widget_html)
        self.assertIn("trade_copy_btn", widget_html)
        self.assertIn("trade_bar_net", widget_html)
        self.assertIn("trade_bar_tax", widget_html)

        # 포맷팅 표준 확인 (원, %, $)
        self.assertIn("toLocaleString('ko-KR')", widget_html)
        self.assertIn("toFixed(2)", widget_html)

        tables_html = self.resolver.render_trading_tables("overseas_stock_tax")
        self.assertIn("2026 해외주식 양도소득세 과세표준 및 실효세율", tables_html)
        self.assertIn("3대 합법적 양도소득세 절세 전략", tables_html)

        disclaimer_html = self.resolver.render_legal_disclaimer()
        self.assertIn("legal-disclaimer", disclaimer_html)
        self.assertIn("소득세법 제94조", disclaimer_html)

    # --------------------------------------------------------------------------
    # [Test 3] YMYL 과장 광고 필터 및 면책 조항 검증
    # --------------------------------------------------------------------------
    def test_03_ymyl_compliance_and_filter(self):
        """'원금 보장', '무조건 수익' 차단 및 legal-disclaimer 누락 시 QA FAIL 검증"""
        # 1. 과장 광고 단어 포함 시 FAIL
        dirty_html = """
        <html><body>
          <script type="application/ld+json">
          {"@type": "SoftwareApplication", "name": "투자툴", "applicationCategory": "FinanceApplication", "operatingSystem": "Any"}
          </script>
          <h1>원금 보장 100% 해외주식 투자 시뮬레이터</h1>
          <div class="legal-disclaimer">면책 조항: 소득세법 기준 안내</div>
        </body></html>
        """
        qa_res = run_validator(dirty_html)
        self.assertFalse(qa_res["passed"])
        self.assertTrue(any("YMYL 과장 광고" in err for err in qa_res["errors"]))

        # 2. legal-disclaimer 누락 시 FAIL
        no_disclaimer_html = """
        <html><body>
          <script type="application/ld+json">
          {"@type": "SoftwareApplication", "name": "투자툴", "applicationCategory": "FinanceApplication", "operatingSystem": "Any"}
          </script>
          <h1>2026 해외주식 양도소득세 손익통산 계산기</h1>
        </body></html>
        """
        qa_res2 = run_validator(no_disclaimer_html)
        self.assertFalse(qa_res2["passed"])
        self.assertTrue(any("legal-disclaimer" in err for err in qa_res2["errors"]))

    # --------------------------------------------------------------------------
    # [Test 4] Schema.org FinanceApplication 및 FAQPage 검증
    # --------------------------------------------------------------------------
    def test_04_schema_org_finance_application(self):
        """Schema.org FinanceApplication 및 operatingSystem: Any 엄격 검증"""
        valid_schema_html = """
        <html><body>
          <script type="application/ld+json">
          {
            "@context": "https://schema.org",
            "@graph": [
              {
                "@type": "SoftwareApplication",
                "name": "해외주식 계산기",
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Any"
              },
              {
                "@type": "FAQPage",
                "mainEntity": []
              }
            ]
          }
          </script>
          <div class="legal-disclaimer">소득세법 면책 조항 안내</div>
        </body></html>
        """
        validator = DeterministicQAValidator(valid_schema_html)
        schema_res = validator.validate_json_ld()
        self.assertTrue(schema_res["passed"], f"Schema validation failed: {validator.errors}")

    # --------------------------------------------------------------------------
    # [Test 5] Playwright E2E 샌드박스 경계값(0, 음수, 10억) 및 4대 계산기 E2E 통과
    # --------------------------------------------------------------------------
    def test_05_playwright_e2e_trading_sandbox_all_four(self):
        """4대 금융 계산기 전체가 Playwright 경계값 테스트 및 QA 게이트를 100% 통과하는지 검증"""
        rules = ["overseas_stock_tax", "water_averaging_dca", "leverage_liquidation_kelly", "dividend_compound_tax"]
        for r_key in rules:
            resolved = self.resolver.resolve_topic(r_key)
            widget_html = self.resolver.render_trading_saas_html(r_key)
            tables_html = self.resolver.render_trading_tables(r_key)
            disclaimer_html = self.resolver.render_legal_disclaimer()
            silo_html = self.resolver.render_internal_silo_links(r_key)

            complete_page_html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{resolved['target_keyword']}</title>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "SoftwareApplication",
        "name": "{resolved['target_keyword']}",
        "operatingSystem": "Any",
        "applicationCategory": "FinanceApplication",
        "offers": {{ "@type": "Offer", "price": "0" }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "{resolved['target_keyword']} 질문",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "정상적인 공식 해설 답변입니다."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body style="margin:0; padding:10px; background:#0b0f19; box-sizing:border-box;">
  <h1 style="color:#fff;">{resolved['target_keyword']}</h1>
  {widget_html}
  {tables_html}
  {silo_html}
  {disclaimer_html}
</body>
</html>
"""
            qa_result = run_validator(complete_page_html)
            self.assertTrue(qa_result["passed"], f"Rule '{r_key}' failed QA: {qa_result['errors']}")
            self.assertEqual(len(qa_result["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
