# -*- coding: utf-8 -*-
"""
tests/test_v9_apex_architecture.py
----------------------------------
Blogin 365 AI Holdings - Comprehensive v9.0 Apex Architecture Test Suite.
Validates the complete 5 Iron Rules and 5 External Oracle Gates:
- [철칙 1] 단발성 키워드 영구 금지 & 30-Day 토픽 클러스터 & 카니발라이제이션 방어 (Cosine Distance > 0.35)
- [철칙 2] 1차 원천 데이터(Ground Truth 100%) & Strict Domain Isolation
- [철칙 3] AEO 면역형 인터랙티브 Micro-SaaS (2x2 대칭, 빈 공간 0%, Dual Shield) & 아폴리아 8-Block & Sticky TOC
- [철칙 4] 무인 품질 검증(Linter) 10대 게이트 (Zero-Persona, Zero-Broken-Entity, Information Gain 30%, Ghost Mode)
- [철칙 5] 단위 경제성(Unit Economics) & 21-Day Pruning 자가치유 & Empire Flippers 35~40배수 엑시트 밸류에이션
"""

import os
import sys
import unittest
import json
import re

# Ensure UTF-8 console output for Windows PowerShell
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.matcher.topic_cluster_engine import TopicClusterEngine
from engine.matcher.domain_router import classify_domain, DOMAIN_HAIR_TRANSPLANT
from engine.radar.crawl4ai_scout import Crawl4AIScout
from engine.radar.community_sentiment_scout import CommunitySentimentScout
from engine.agents.agency_stack import AgencyStack
from engine.agents.cro_monetizer import assemble_world_class_article
from engine.visuals.saas_calculator import render_saas_calculator
from engine.qa.gstack_auditor import GStackAuditor
from engine.publisher.blogger_gateway import BloggerGateway
from engine.analytics.unit_economics import UnitEconomicsCalculator
from engine.maintenance.batch_pruner import BatchPrunerEngine
from engine.analytics.asset_valuation import AssetValuationEngine


class TestV9ApexArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.topic = {
            "keyword": "3000모 모발이식 가격",
            "category": "HAIR",
            "cpc": 6800,
            "title": "3000모 모발이식 가격 및 비절개 FUE vs 절개 FUT 견적서 함정 분석",
            "subs": ["3000모 모발이식 가격 비교", "모발이식 모수 모낭수 차이", "모발이식 2주차 운동 주의사항"],
            "pvs": 68000
        }
        cls.agency = AgencyStack()
        cls.editorial = cls.agency._build_deterministic_content(cls.topic)
        cls.html = assemble_world_class_article(cls.topic, cls.editorial, is_adsense_approved=False)

    # --------------------------------------------------------------------------
    # [철칙 1] 토픽 클러스터 & 카니발라이제이션 방어
    # --------------------------------------------------------------------------
    def test_01_topic_cluster_30day_mesh_and_governance(self):
        engine = TopicClusterEngine()
        summary = engine.portfolio_mgr.get_portfolio_summary()
        self.assertIn("active_cluster_id", summary)
        self.assertGreaterEqual(summary["total_clusters"], 5)
        self.assertEqual(len(summary["clusters"]), 5)

        next_topic = engine.get_next_cluster_topic()
        self.assertIn("keyword", next_topic)
        self.assertIn("pillar", next_topic)
        self.assertIn("day", next_topic)

        # Check interlinking mesh HTML
        mesh_html = engine.render_interlinking_mesh(next_topic["keyword"], category="HAIR")
        self.assertIn("b365-cluster-nav", mesh_html)
        self.assertIn("30-DAY TOPIC CLUSTER", mesh_html)
        self.assertIn("마스터 종합 기둥글", mesh_html)

    def test_02_semantic_cannibalization_insulation(self):
        engine = TopicClusterEngine()
        cand_calc = "3000모 모발이식 1원단위 견적 시뮬레이터"
        cand_compare = "모발이식 비절개 vs 절개 3000모 비교 대조"

        res_calc = engine.check_cannibalization(cand_calc, cluster_id="hair_transplant")
        self.assertTrue(res_calc["passed"])
        self.assertEqual(res_calc["candidate_intent"], "CALC")

        res_compare = engine.check_cannibalization(cand_compare, cluster_id="hair_transplant")
        self.assertTrue(res_compare["passed"])
        self.assertEqual(res_compare["candidate_intent"], "COMPARE")

    # --------------------------------------------------------------------------
    # [철칙 2] 1차 원천 데이터(Ground Truth 100%) & Strict Domain Isolation
    # --------------------------------------------------------------------------
    def test_03_community_real_questions_gathered(self):
        scout = CommunitySentimentScout()
        res = scout.scout_community_sentiment("3000모 모발이식 가격", category="HAIR")
        sources_str = "".join(res.get("community_sources", []))
        self.assertTrue("대다모" in sources_str or "디시" in sources_str)
        all_text = "".join(res.get("raw_opinions", [])) + "".join(res.get("core_pain_points", []))
        hair_keywords = ["스쿼트", "모수", "모낭", "견적", "약값", "테크니션", "생착", "동반탈락"]
        self.assertTrue(any(hk in all_text for hk in hair_keywords), f"No hair keywords found in: {all_text}")

    def test_04_crawl4ai_ground_truth_factset(self):
        scout = Crawl4AIScout()
        vault = scout.DETERMINISTIC_TABLE_VAULT
        self.assertIn("모발이식", vault)
        self.assertIn("모발이식비용", vault)

        hair_table = vault["모발이식"]
        self.assertIn("비절개 (FUE)", hair_table)
        self.assertIn("절개 (FUT)", hair_table)
        self.assertIn("3,000모", hair_table)

        cost_table = vault["모발이식비용"]
        self.assertIn("소득세법 제59조의4", cost_table)
        self.assertIn("ISHRS", cost_table)

    def test_05_strict_domain_isolation_zero_contamination(self):
        domain = classify_domain("3000모 모발이식 가격", "HAIR")
        self.assertEqual(domain, DOMAIN_HAIR_TRANSPLANT)

        forbidden_medical_words = ["임플란트", "도수치료", "백내장", "라식", "라섹", "스마일라식", "치과", "보철", "크라운"]
        for word in forbidden_medical_words:
            self.assertNotIn(word, self.html, f"Strict Domain Isolation Violated: Found '{word}' in hair article!")

    # --------------------------------------------------------------------------
    # [철칙 3] AEO 면역형 8-Block & 2x2 대칭 무공백 Micro-SaaS & Sticky TOC
    # --------------------------------------------------------------------------
    def test_06_apolia_8block_and_sticky_toc(self):
        # 1. Hero Title & Badge
        self.assertIn("b365-hero-header", self.html)
        self.assertIn("badge-dwell", self.html)
        self.assertIn("Blogin 365 AI 에디토리얼 팀", self.html)

        # 2. Bento Hero 3-line Summary
        self.assertIn("bento-hero", self.html)

        # 3. Psychological Hook
        self.assertIn("b365-psychological-hook", self.html)

        # 4. H2 1-line answer Callouts
        self.assertIn("b365-featured-callout", self.html)

        # 5. Comparative Tables (FUE vs FUT, Grafts vs Hairs, 3-year costs)
        self.assertIn("b365-comp-table-1", self.html)
        self.assertIn("b365-comp-table-2", self.html)
        self.assertIn("b365-comp-table-3", self.html)

        # 6. Micro-SaaS Calculator
        self.assertIn("custom-saas-tool", self.html)

        # 7. Sticky TOC with Scroll-Spy
        self.assertIn("b365-sticky-toc", self.html)
        self.assertIn("b365-toc-link", self.html)

        # 8. Interlinking Mesh & FAQ
        self.assertIn("b365-cluster-nav", self.html)
        self.assertIn("faq-section", self.html)

    def test_07_saas_calculator_2x2_zero_gap_dual_shield(self):
        calc_html = render_saas_calculator("HAIR", "3000모 모발이식 가격")
        # Full width 100%
        self.assertIn("width:100%", calc_html)
        self.assertIn("max-width:100%", calc_html)

        # 2-Column Balanced Grid
        self.assertIn("grid-template-columns:repeat(2, 1fr)", calc_html)
        self.assertIn("b365-calc-input-grid", calc_html)

        # Explicit Card Data Tags (data-calc-card="true")
        self.assertEqual(calc_html.count('data-calc-card="true"'), 4, "Expected exactly 4 legitimate input cards tagged!")

        # Dual Shield: CSS display:none on alien widgets
        self.assertIn(".b365-calc-input-grid > [id^=\"HTML\"]", self.html)
        self.assertIn("display: none !important;", self.html)

        # Dual Shield: JS MutationObserver auto-ejection
        self.assertIn("ejectCalcAliens", calc_html)
        self.assertIn("MutationObserver", calc_html)

    # --------------------------------------------------------------------------
    # [철칙 4] 무인 품질 검증(Linter) 10대 게이트
    # --------------------------------------------------------------------------
    def test_08_zero_persona_and_zero_broken_entity(self):
        fake_names = ["김재현", "박민우", "이진우", "최현우", "김현철", "기자", "전문기자"]
        for fn in fake_names:
            self.assertNotIn(f"전문가 {fn}", self.html)
            self.assertNotIn(f"기자 {fn}", self.html)

        broken_entities = ["&#10003;", "&#9662;", "&amp;#10003;", "&amp;#9662;"]
        for be in broken_entities:
            self.assertNotIn(be, self.html)

    def test_09_gstack_ten_gates_audit_pass(self):
        auditor = GStackAuditor()
        audit = auditor.audit_post(
            self.topic["title"],
            self.html,
            keyword_package={"main": self.topic["keyword"], "subs": self.topic["subs"]}
        )
        self.assertTrue(audit["passed"], f"GStack audit failed with errors: {audit.get('errors')}")
        self.assertGreaterEqual(audit.get("hcu_score", 0), 85)

    def test_10_ghost_mode_defensive_ad_and_link_hiding(self):
        html_ghost = assemble_world_class_article(self.topic, self.editorial, is_adsense_approved=False)
        self.assertNotIn("adsbygoogle", html_ghost)
        self.assertNotIn("linkprice.com", html_ghost)
        self.assertNotIn("adpick.co.kr", html_ghost)

    def test_11_blogger_gateway_schema_markup(self):
        bg = BloggerGateway()
        schema_json = bg.build_schema_markup(self.topic["title"], self.topic["keyword"], self.topic["category"])
        self.assertIn("https://schema.org", schema_json)
        self.assertIn("Blogin 365 AI Editorial Team", schema_json)

    # --------------------------------------------------------------------------
    # [철칙 5] 단위 경제성 & 21-Day Pruner & Empire Flippers 35~40배수 밸류에이션
    # --------------------------------------------------------------------------
    def test_12_unit_economics_1000_page_bep(self):
        ue = UnitEconomicsCalculator()
        metrics = ue.simulate_1000_page_batch()
        cost_breakdown = metrics["cost_breakdown"]
        performance = metrics["performance_projection"]
        bep = metrics["bep_metrics"]

        self.assertLessEqual(cost_breakdown["total_batch_cost_usd"], 15.0)
        self.assertGreaterEqual(cost_breakdown["total_batch_cost_usd"], 2.0)
        self.assertLessEqual(bep["days_to_bep_post_indexing"], 7.0)
        self.assertEqual(bep["unit_economic_health"], "ULTRA_HIGH_MARGIN")

    def test_13_batch_pruner_21day_lifecycle(self):
        pruner = BatchPrunerEngine()

        post_high_impr_no_click = {
            "post_id": "test_1",
            "title": "3000모 모발이식 가격 정보",
            "keyword": "3000모 모발이식 가격",
            "published_at": "2026-01-01T00:00:00",
            "impressions": 150,
            "clicks": 0
        }
        eval_1 = pruner.evaluate_post(post_high_impr_no_click)
        self.assertEqual(eval_1["decision"], "REWRITE_NEEDED")
        self.assertEqual(eval_1["action"], "SELF_HEAL")

        post_deadweight = {
            "post_id": "test_2",
            "title": "단발성 버려진 글",
            "keyword": "버려진 키워드",
            "published_at": "2026-01-01T00:00:00",
            "impressions": 0,
            "clicks": 0
        }
        eval_2 = pruner.evaluate_post(post_deadweight)
        self.assertEqual(eval_2["decision"], "PRUNE_CANDIDATE")
        self.assertEqual(eval_2["action"], "PRUNE")

        post_winner = {
            "post_id": "test_3",
            "title": "인기 포스트",
            "keyword": "인기 키워드",
            "published_at": "2026-01-01T00:00:00",
            "impressions": 300,
            "clicks": 12
        }
        eval_3 = pruner.evaluate_post(post_winner)
        self.assertEqual(eval_3["decision"], "WINNER")
        self.assertEqual(eval_3["action"], "BOOST")

    def test_14_empire_flippers_exit_valuation(self):
        val_engine = AssetValuationEngine()
        val = val_engine.calculate_valuation(monthly_gross_usd=4000.0, monthly_opex_usd=80.0)

        fn = val["financials_monthly"]
        av = val["asset_valuation"]
        multiples = val["multiples"]

        self.assertAlmostEqual(fn["net_profit_usd"], 3920.0, delta=1.0)
        self.assertEqual(multiples["low_multiple"], 32.0)
        self.assertEqual(multiples["median_multiple"], 36.0)
        self.assertEqual(multiples["apex_multiple"], 40.0)

        expected_median = 3920.0 * 36.0
        self.assertAlmostEqual(av["valuation_median_usd"], expected_median, delta=10.0)
        self.assertGreater(av["valuation_median_krw"], 100_000_000)

    # --------------------------------------------------------------------------
    # 8인 AI 직원 전용 마스터 시스템 프롬프트 하모니 전수 검증
    # --------------------------------------------------------------------------
    def test_15_all_8_staff_prompts_fully_wired(self):
        from engine.agents.prompts_chat_pack import APEX_STAFF_PROMPTS, get_staff_prompt
        from engine.company_runtime import AICompanyStaff
        from engine.growth.viral_hook_maker import ViralHookMaker, MARKETER_PROMPT
        from engine.agents import cro_monetizer
        from engine.visuals import saas_calculator, canvas_renderer
        import engine.maintenance.batch_pruner as bp_mod

        expected_roles = [
            "01_ChiefOfStaff",
            "02_ProductPlanner",
            "03_MarketResearcher",
            "04_UIDesigner",
            "05_Developer",
            "06_QATester",
            "07_Marketer",
            "08_CSPublisher"
        ]

        # 1. APEX_STAFF_PROMPTS 전수 등록 및 프롬프트 완결성 검증
        for rk in expected_roles:
            self.assertIn(rk, APEX_STAFF_PROMPTS, f"Role {rk} missing in APEX_STAFF_PROMPTS")
            p_data = APEX_STAFF_PROMPTS[rk]
            self.assertIn("title", p_data)
            self.assertIn("description", p_data)
            self.assertIn("system_prompt", p_data)
            self.assertGreater(len(p_data["system_prompt"]), 300, f"Prompt for {rk} too short!")
            self.assertTrue(p_data["system_prompt"].startswith("# Role:"), f"Prompt for {rk} missing '# Role:' header")
            self.assertEqual(get_staff_prompt(rk), p_data["system_prompt"].strip())

        # 2. AICompanyStaff 하네스 바인딩 검증
        staff = AICompanyStaff()
        all_prompts = staff.get_all_prompts()
        self.assertEqual(len(all_prompts), 8)
        for rk in expected_roles:
            self.assertEqual(staff.get_prompt(rk), APEX_STAFF_PROMPTS[rk]["system_prompt"].strip())

        # 3. 헬스체크 프롬프트 상태 검증
        health = staff.check_health()
        for rk in expected_roles:
            self.assertEqual(health[rk]["prompt_status"], "ACTIVE_V9_APEX")
            self.assertGreater(health[rk]["prompt_chars"], 300)

        # 4. 개별 에이전트 모듈 직접 주입 검증
        agency = AgencyStack()
        self.assertIn("01_ChiefOfStaff", agency.staff_prompts)
        self.assertEqual(agency.chief_prompt, APEX_STAFF_PROMPTS["01_ChiefOfStaff"]["system_prompt"].strip())
        self.assertEqual(agency.planner_prompt, APEX_STAFF_PROMPTS["02_ProductPlanner"]["system_prompt"].strip())
        self.assertEqual(agency.researcher_prompt, APEX_STAFF_PROMPTS["03_MarketResearcher"]["system_prompt"].strip())
        self.assertEqual(agency.qa_prompt, APEX_STAFF_PROMPTS["06_QATester"]["system_prompt"].strip())

        auditor = GStackAuditor()
        self.assertEqual(auditor.staff_prompt, APEX_STAFF_PROMPTS["06_QATester"]["system_prompt"].strip())

        marketer = ViralHookMaker()
        self.assertEqual(marketer.staff_prompt, APEX_STAFF_PROMPTS["07_Marketer"]["system_prompt"].strip())
        self.assertEqual(MARKETER_PROMPT, APEX_STAFF_PROMPTS["07_Marketer"]["system_prompt"].strip())

        bg = BloggerGateway()
        self.assertEqual(bg.staff_prompt, APEX_STAFF_PROMPTS["08_CSPublisher"]["system_prompt"].strip())

        self.assertEqual(cro_monetizer.UI_DESIGNER_PROMPT, APEX_STAFF_PROMPTS["04_UIDesigner"]["system_prompt"].strip())
        self.assertEqual(cro_monetizer.DEVELOPER_PROMPT, APEX_STAFF_PROMPTS["05_Developer"]["system_prompt"].strip())

        self.assertEqual(saas_calculator.DEVELOPER_PROMPT, APEX_STAFF_PROMPTS["05_Developer"]["system_prompt"].strip())
        self.assertEqual(canvas_renderer.UI_DESIGNER_PROMPT, APEX_STAFF_PROMPTS["04_UIDesigner"]["system_prompt"].strip())

        cluster_eng = TopicClusterEngine()
        self.assertEqual(cluster_eng.chief_prompt, APEX_STAFF_PROMPTS["01_ChiefOfStaff"]["system_prompt"].strip())
        self.assertEqual(cluster_eng.planner_prompt, APEX_STAFF_PROMPTS["02_ProductPlanner"]["system_prompt"].strip())

        self.assertEqual(bp_mod.CS_PUBLISHER_PROMPT, APEX_STAFF_PROMPTS["08_CSPublisher"]["system_prompt"].strip())


if __name__ == "__main__":
    unittest.main()
