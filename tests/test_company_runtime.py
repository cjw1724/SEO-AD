# -*- coding: utf-8 -*-
"""
tests/test_company_runtime.py
------------------------------
Comprehensive verification of Blogin 365 AI Holdings Company Operating System:
1. Company Logger persistence & KPI metric calculations
2. 8 AI Staff health checks
3. Self-healing pipeline in dry-run & fallback scenarios
4. Zero-Persona & Zero Broken Entity enforcement
"""

import os
import sys
import json
import tempfile
import unittest

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.company_runtime import CompanyLogger, AICompanyStaff, CompanyRuntime, SelfHealingPipeline
from engine.qa.gstack_auditor import GStackAuditor


class TestCompanyRuntime(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_log_path = os.path.join(self.temp_dir.name, "test_company_logs.json")
        self.logger = CompanyLogger(self.temp_log_path)
        self.staff = AICompanyStaff()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_logger_initialization_and_metrics(self):
        data = self.logger.load_data()
        self.assertEqual(data["company_name"], "Blogin 365 AI Holdings")
        self.assertEqual(data["metrics"]["total_cycles_run"], 0)

        # Record a successful cycle
        cycle = {
            "cycle_id": "TEST-01",
            "timestamp": "2026-10-11T12:00:00",
            "status": "SUCCESS",
            "dry_run": True,
            "keyword": "테스트 키워드",
            "pvs_score": 500000.0,
            "url": "https://example.com/test"
        }
        self.logger.record_cycle(cycle)

        updated = self.logger.load_data()
        self.assertEqual(updated["metrics"]["total_cycles_run"], 1)
        self.assertEqual(updated["metrics"]["successful_cycles"], 1)
        self.assertEqual(updated["metrics"]["success_rate_percent"], 100.0)
        self.assertEqual(updated["metrics"]["cumulative_pvs_score"], 500000.0)
        self.assertEqual(len(updated["execution_history"]), 1)

    def test_02_staff_health_check(self):
        health = self.staff.check_health()
        self.assertEqual(len(health), 8, "Must monitor exactly 8 AI staff roles")
        for role_key, info in health.items():
            self.assertIn("status", info)
            self.assertIn(info["status"], ["HEALTHY", "WARNING"])
            self.assertTrue(info["name"])

    def test_03_autonomous_cycle_dry_run(self):
        runtime = CompanyRuntime()
        result = runtime.run_once(dry_run=True, keyword_override="2026 근로장려금 정기신청")

        self.assertIsNotNone(result)
        self.assertIn(result["status"], ["SUCCESS", "HEALED"])
        self.assertEqual(result["keyword"], "2026 근로장려금 정기신청")
        self.assertTrue(result["title"])
        self.assertTrue(result["url"])
        self.assertGreater(result["pvs_score"], 0)
        self.assertIn("growth_package", result)

    def test_04_zero_persona_and_zero_broken_entity_gates(self):
        auditor = GStackAuditor()
        
        # Test fake journalist violation
        facts_dummy = "<p>지원 기준은 월 70만원 한도이며 연 4.5% 금리와 24개월 만기 조건으로 총 5000명 대상입니다.</p>" * 20
        fake_content = "<div class='bento-hero'>Hero</div><div class='saas-calculator'>Calc</div><div class='adsense-slot'>Ad</div><details><summary>FAQ</summary>A</details><p>작성자: 금융 전문 기자 김재현</p>" + facts_dummy
        bad_res = auditor.audit_post("기사 제목", fake_content)
        self.assertFalse(bad_res["passed"], "Must fail when fake persona '김재현' is present")

        # Test broken entity detection & sanitization
        entity_content = "<div class='bento-hero'>Hero</div><div class='saas-calculator'>Calc</div><div class='adsense-slot'>Ad</div><details><summary>FAQ</summary>A</details><p>체크: &#10003; 완료</p>" + facts_dummy
        entity_res = auditor.audit_post("기사 제목", entity_content)
        self.assertFalse(entity_res["passed"], "Must detect &#10003; as broken entity")
        
        sanitized = auditor.sanitize_if_possible(entity_content)
        self.assertNotIn("&#10003;", sanitized)
        re_res = auditor.audit_post("기사 제목", sanitized)
        self.assertTrue(re_res["passed"], f"Sanitized content must pass all gates: {re_res.get('errors')}")

    def test_05_keyword_7tier_classification(self):
        from engine.matcher.demand_matcher import classify_keyword_tier

        # 1. 허수: 월간 검색 20 이하
        t1 = classify_keyword_tier(monthly_search_vol=15, blog_doc_count=100, monthly_published=5)
        self.assertEqual(t1["tier"], "허수")
        self.assertFalse(t1["is_viable"])

        # 2. 벽: 블로그 문서 3,000 이상
        t2 = classify_keyword_tier(monthly_search_vol=50000, blog_doc_count=3500, monthly_published=100)
        self.assertEqual(t2["tier"], "벽")
        self.assertFalse(t2["is_viable"])

        # 3. 과열: 한 달 발행 300편 이상
        t3 = classify_keyword_tier(monthly_search_vol=10000, blog_doc_count=800, monthly_published=350)
        self.assertEqual(t3["tier"], "과열")

        # 4. 어려움: 블로그 문서 1,000~3,000
        t4 = classify_keyword_tier(monthly_search_vol=1500, blog_doc_count=1500, monthly_published=50)
        self.assertEqual(t4["tier"], "어려움")

        # 5. 최적: 비율 0.5 초과
        t5 = classify_keyword_tier(monthly_search_vol=35000, blog_doc_count=500, monthly_published=100)
        self.assertEqual(t5["tier"], "최적")
        self.assertTrue(t5["is_optimal"])
        self.assertGreater(t5["ratio"], 0.5)

        # 6. 가능: 비율 0.1 ~ 0.5
        t6 = classify_keyword_tier(monthly_search_vol=200, blog_doc_count=600, monthly_published=50)
        self.assertEqual(t6["tier"], "가능")
        self.assertTrue(t6["is_viable"])

        # 7. 포화: 비율 0.1 이하
        t7 = classify_keyword_tier(monthly_search_vol=50, blog_doc_count=800, monthly_published=50)
        self.assertEqual(t7["tier"], "포화")
        self.assertFalse(t7["is_viable"])

    def test_06_keyword_package_and_title_generation(self):
        from engine.matcher.demand_matcher import build_keyword_package, generate_optimized_title

        pkg = build_keyword_package(
            main_kw="청년도약계좌",
            category="SUBSIDY",
            sub_candidates=["청년도약계좌 만기", "청년도약계좌 중도해지", "청년도약계좌 갈아타기"],
            search_vol=40000,
            doc_count=600,
            monthly_pub=120
        )

        self.assertEqual(pkg["main"], "청년도약계좌")
        self.assertEqual(len(pkg["subs"]), 3)
        self.assertEqual(pkg["tier"], "최적")
        self.assertGreater(pkg["ratio"], 0.5)
        self.assertIn("sub_details", pkg)
        self.assertEqual(len(pkg["sub_details"]), 3)

        # Title verification
        title = generate_optimized_title(pkg["main"], "SUBSIDY", subs=pkg["subs"])
        self.assertTrue(title.startswith("청년도약계좌"), f"Title must start with main keyword: {title}")
        self.assertNotIn("[2026]", title, "Title must not have date brackets prefix")
        self.assertGreaterEqual(len(title), 25, "Title should be sufficiently descriptive (30-40 chars)")
        self.assertLessEqual(len(title), 42, "Title should not exceed 42 chars")

        # Sub-keywords must NOT be in title
        for sub in pkg["subs"]:
            self.assertNotIn(sub, title, f"Sub-keyword '{sub}' must not appear in title '{title}'")

        # Edge Case 1: [2026] Bracket prefix input must be cleanly stripped
        bracket_pkg = build_keyword_package("[2026] 청년도약계좌", "SUBSIDY")
        self.assertEqual(bracket_pkg["main"], "청년도약계좌")
        bracket_title = generate_optimized_title("[2026] 청년도약계좌", "SUBSIDY")
        self.assertTrue(bracket_title.startswith("청년도약계좌"))
        self.assertNotIn("[2026]", bracket_title)

        # Edge Case 2: Short keyword ending in '총정리' must not duplicate '총정리 총정리'
        short_title = generate_optimized_title("TV", "TECH")
        self.assertNotIn("총정리 총정리", short_title)
        self.assertGreaterEqual(len(short_title), 25)

    def test_07_gate_6_keyword_placement_audit(self):
        auditor = GStackAuditor()
        pkg = {
            "main": "청년도약계좌",
            "subs": ["청년도약계좌 신청 자격 조건", "청년도약계좌 실수령액 모의계산", "청년도약계좌 지급일 및 필수 서류"]
        }

        # 1. Valid compliant HTML passing Gate 6
        valid_title = "청년도약계좌 혜택 분석 및 최신 금리 비교 완벽 가이드"
        valid_html = f"""
        <div class="bento-hero">Hero</div>
        <div class="article-lead"><p>{pkg['main']} 공식 분석 리포트입니다.</p></div>
        <div class="saas-calculator">Calc</div>
        <div class="adsense-slot">Ad</div>
        <div class="content-section">
            <h2>1. {pkg['subs'][0]} 분석</h2>
            <p>{pkg['main']} 관련 세부 기준입니다. {pkg['subs'][0]} 항목을 확인하세요.</p>
        </div>
        <div class="content-section">
            <h2>2. {pkg['subs'][1]} 안내</h2>
            <p>{pkg['main']} 금액을 모의계산합니다. {pkg['subs'][1]} 결과를 확인하세요.</p>
        </div>
        <div class="content-section">
            <h2>3. {pkg['subs'][2]} 정리</h2>
            <p>{pkg['main']} 신청 절차입니다. {pkg['subs'][2]} 목록입니다.</p>
        </div>
        <details><summary>FAQ</summary><p>답변</p></details>
        """ + ("<p>기준 금리 4.5%, 지원금 70만원, 기간 24개월, 신청 100건 확인</p>" * 20)

        res = auditor.audit_post(valid_title, valid_html, keyword_package=pkg)
        self.assertTrue(res["passed"], f"Expected PASS but got errors: {res.get('errors')}")

        # 2. Main keyword NOT at title start -> must FAIL Gate 6
        bad_title_res = auditor.audit_post("최신 꿀팁 청년도약계좌 가이드", valid_html, keyword_package=pkg)
        self.assertFalse(bad_title_res["passed"], "Must fail when main keyword is not at title start")
        self.assertTrue(any("GATE 6" in e for e in bad_title_res["errors"]))

        # 3. Sub-keyword in title -> must FAIL Gate 6
        bad_sub_title_res = auditor.audit_post(f"청년도약계좌 {pkg['subs'][0]} 완벽 가이드", valid_html, keyword_package=pkg)
        self.assertFalse(bad_sub_title_res["passed"], "Must fail when sub-keyword is in title")

        # 4. Sub-keyword missing from H2 -> must FAIL Gate 6
        missing_h2_html = valid_html.replace(f"<h2>1. {pkg['subs'][0]} 분석</h2>", "<h2>1. 일반 정보 분석</h2>")
        bad_h2_res = auditor.audit_post(valid_title, missing_h2_html, keyword_package=pkg)
        self.assertFalse(bad_h2_res["passed"], "Must fail when sub-keyword is not mapped to H2")

        # 5. Multiple sub-keywords crammed into single H2 -> must FAIL Gate 6 (1:1 violation)
        crammed_h2_html = valid_html.replace(f"<h2>1. {pkg['subs'][0]} 분석</h2>", f"<h2>1. {pkg['subs'][0]} 및 {pkg['subs'][1]}</h2>")
        crammed_h2_html = crammed_h2_html.replace(f"<h2>2. {pkg['subs'][1]} 안내</h2>", "<h2>2. 추가 정보 안내</h2>")
        crammed_res = auditor.audit_post(valid_title, crammed_h2_html, keyword_package=pkg)
        self.assertFalse(crammed_res["passed"], "Must fail when multiple sub-keywords are crammed into a single H2")

        # 6. Sub-keyword in subtitle (article-lead) -> must FAIL Gate 6
        sub_in_lead_html = valid_html.replace(f"{pkg['main']} 공식 분석 리포트입니다.", f"{pkg['main']} {pkg['subs'][0]} 공식 분석 리포트입니다.")
        sub_lead_res = auditor.audit_post(valid_title, sub_in_lead_html, keyword_package=pkg)
        self.assertFalse(sub_lead_res["passed"], "Must fail when sub-keyword appears in subtitle")

        # 7. Date bracket in title -> must FAIL Gate 6
        bracket_title_res = auditor.audit_post(f"[2026] {valid_title}", valid_html, keyword_package=pkg)
        self.assertFalse(bracket_title_res["passed"], "Must fail when title has date bracket label")


if __name__ == "__main__":
    unittest.main()
