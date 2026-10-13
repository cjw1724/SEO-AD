# -*- coding: utf-8 -*-
"""
tests/test_trick_b_search_monetization.py
-------------------------------------------
Comprehensive verification suite for Trick B (Google CSE & AdSense for Search):
1. Dual Architecture: Official Google CSE rendering vs. Blog Internal Search fallback
2. High-CTR Trigger Pills: 5 golden niches, clean URL encoding, deep query routing
3. AgencyStack Integration: Automatic related_searches extraction & deterministic fallback
4. CRO Monetizer Integration: Placement within 7-phase article, zero slop & zero persona
5. Theme XML Compliance: Valid XML structure with embedded search widget & dynamic script
6. Environment Template: GOOGLE_CSE_CX presence in SEO.env and .env.example
7. Edge cases: Empty, None, special characters, and keyword density safety
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import unquote

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.agents.cro_monetizer import render_search_navigation_widget, assemble_world_class_article
from engine.agents.agency_stack import AgencyStack
from engine.qa.gstack_auditor import GStackAuditor, FORBIDDEN_ENTITIES, FORBIDDEN_PERSONA_KEYWORDS


class TestTrickBSearchMonetization(unittest.TestCase):

    def setUp(self):
        self.auditor = GStackAuditor()

    def test_01_search_navigation_widget_with_cse_cx(self):
        """GOOGLE_CSE_CX 설정 시 공식 구글 CSE 스크립트 및 gcse-search 컨테이너 렌더링 검증"""
        test_cx = "012345678901234567890:abcdefghijk"
        html = render_search_navigation_widget(
            keyword="2026 청년도약계좌",
            category="SUBSIDY",
            related_keywords=["청년도약계좌 자격", "청년도약계좌 금액"],
            cse_cx=test_cx
        )

        self.assertIn("b365-search-nav", html)
        self.assertIn("b365-cse-box", html)
        self.assertIn(f"https://cse.google.com/cse.js?cx={test_cx}", html)
        self.assertIn("gcse-search", html)
        self.assertIn("b365-search-pills", html)
        self.assertIn("b365-search-pill", html)

    def test_02_search_navigation_widget_fallback_without_cx(self):
        """GOOGLE_CSE_CX 미설정 시 블로그 자체 검색 URL 무중단 듀얼 폴백 렌더링 검증"""
        html = render_search_navigation_widget(
            keyword="알뜰폰 요금제 비교",
            category="SAVINGS",
            related_keywords=None,
            cse_cx=""
        )

        self.assertIn("b365-search-nav", html)
        self.assertIn("b365-search-form", html)
        self.assertIn("https://blogin365ai.blogspot.com/search", html)
        self.assertIn("method=\"get\"", html)
        self.assertIn("name=\"q\"", html)
        self.assertNotIn("cse.google.com/cse.js", html)
        self.assertIn("b365-search-pills", html)

    def test_03_pill_tags_generation_for_all_5_niches(self):
        """5대 황금 니치별 검색 트리거 알약(Pill 태그) 생성 및 URL 인코딩 검증"""
        niches = ["TECH", "SUBSIDY", "SAVINGS", "MEDICAL", "CAREER"]
        for cat in niches:
            kw = f"2026 {cat} 테스트"
            html = render_search_navigation_widget(keyword=kw, category=cat)

            self.assertIn("b365-search-pills", html)
            self.assertIn("b365-search-pill", html)
            self.assertIn("https://blogin365ai.blogspot.com/search?q=", html)

            # Check clean entity compliance
            for ent in FORBIDDEN_ENTITIES:
                self.assertNotRegex(html, ent, f"Forbidden entity {ent} found in {cat} search nav")

            # Check zero persona
            for p in FORBIDDEN_PERSONA_KEYWORDS:
                self.assertNotIn(p, html, f"Forbidden persona {p} found in {cat} search nav")

    def test_04_agency_stack_related_searches_generation(self):
        """AgencyStack이 deterministic 및 LLM 출력 시 related_searches를 생성하는지 검증"""
        stack = AgencyStack(api_key=None)  # Force deterministic mode
        sample_topic = {
            "keyword": "2026 근로장려금 정기신청",
            "category": "SUBSIDY",
            "subs": ["근로장려금 자격조건", "근로장려금 지급일", "근로장려금 금액"]
        }
        content = stack.write_editorial_content(sample_topic)
        self.assertIn("related_searches", content)
        self.assertIsInstance(content["related_searches"], list)
        self.assertGreaterEqual(len(content["related_searches"]), 3)
        for s in content["related_searches"]:
            self.assertIsInstance(s, str)
            self.assertTrue(len(s.strip()) > 0)

    def test_05_article_assembly_trick_b_integration(self):
        """assemble_world_class_article 내에 Trick B 위젯 배치 및 GStack 무인 검수 통과 검증"""
        sample_topic = {
            "keyword": "2026 청년도약계좌",
            "category": "SUBSIDY",
            "cpc": 3200,
            "pvs": 25000000,
            "keyword_package": {
                "main": "2026 청년도약계좌",
                "subs": ["2026 청년도약계좌 조건", "2026 청년도약계좌 신청기간", "2026 청년도약계좌 금액"]
            }
        }
        sample_editorial = {
            "keyword": "2026 청년도약계좌",
            "subtitle": "2026 청년도약계좌 공식 데이터 및 핵심 기준 대조 분석 보고서입니다.",
            "sections": [
                {"heading": "1. 2026 청년도약계좌 조건 핵심 분석", "content": "<p>2026 청년도약계좌 조건 기준을 상세히 확인합니다.</p>"},
                {"heading": "2. 2026 청년도약계좌 신청기간 안내", "content": "<p>2026 청년도약계좌 신청기간 일정에 맞춰 서류를 준비합니다.</p>"},
                {"heading": "3. 2026 청년도약계좌 금액 모의 계산", "content": "<p>2026 청년도약계좌 금액 수령액을 사전에 점검합니다.</p>"}
            ],
            "faq": [
                {"question": "자격 요건은 어떻게 되나요?", "answer": "중위소득 기준을 충족해야 합니다."}
            ],
            "related_searches": [
                "2026 청년도약계좌 조건",
                "2026 청년도약계좌 신청기간",
                "2026 청년도약계좌 금액",
                "청년도약계좌 모의계산"
            ]
        }

        article_html = assemble_world_class_article(sample_topic, sample_editorial)

        # Trick B markers
        self.assertIn("b365-search-nav", article_html)
        self.assertIn("b365-search-pills", article_html)
        self.assertIn("b365-search-pill", article_html)
        self.assertIn("https://blogin365ai.blogspot.com/search?q=", article_html)

        # Audit with GStack
        audit_res = self.auditor.audit_post(
            title="2026 청년도약계좌 실수령액 모의계산 및 자격 조건 핵심 가이드",
            html_content=article_html,
            keyword_package=sample_topic["keyword_package"]
        )
        self.assertTrue(audit_res["passed"], f"GStack audit failed with Trick B: {audit_res.get('errors')}")

    def test_06_theme_xml_trick_b_elements(self):
        """blogin365_fintech_theme.xml 내 Trick B 검색 위젯 및 스크립트 무결성 검증"""
        theme_path = os.path.join(BASE_DIR, "blogin365_fintech_theme.xml")
        self.assertTrue(os.path.exists(theme_path))

        # XML Parsing
        tree = ET.parse(theme_path)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("html"))

        with open(theme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # CSS and Widget Assertions
        self.assertIn(".b365-search-nav", content)
        self.assertIn(".b365-search-pill", content)
        self.assertIn(".b365-search-form", content)
        self.assertIn("id='sidebar-search-widget'", content)
        self.assertIn("gcse-search", content)
        self.assertIn("window.B365_CSE_CX", content)

    def test_07_env_configuration_templates(self):
        """SEO.env 및 .env.example 내 GOOGLE_CSE_CX 환경변수 템플릿 존재 검증"""
        seo_env_path = os.path.join(BASE_DIR, "SEO.env")
        example_env_path = os.path.join(BASE_DIR, ".env.example")

        self.assertTrue(os.path.exists(seo_env_path), "SEO.env must exist")
        self.assertTrue(os.path.exists(example_env_path), ".env.example must exist")

        with open(seo_env_path, "r", encoding="utf-8") as f:
            seo_content = f.read()
        self.assertIn("GOOGLE_CSE_CX=", seo_content)

        with open(example_env_path, "r", encoding="utf-8") as f:
            example_content = f.read()
        self.assertIn("GOOGLE_CSE_CX=", example_content)

    def test_08_edge_cases_and_robustness(self):
        """빈 키워드, None 카테고리, 특수문자 등의 엣지 케이스 처리 안정성 검증"""
        # None inputs
        html_none = render_search_navigation_widget(keyword="", category=None, related_keywords=None, cse_cx=None)
        self.assertIn("b365-search-nav", html_none)
        self.assertIn("b365-search-pills", html_none)

        # Keyword with brackets & symbols
        html_sym = render_search_navigation_widget(
            keyword="[2026] <특가> 맥북 '에어' M3 & 프로",
            category="TECH",
            related_keywords=["<테스트> 검색어", "M3 프로 스펙"]
        )
        self.assertIn("b365-search-nav", html_sym)
        self.assertNotIn("&#10003;", html_sym)
        self.assertNotIn("&#9662;", html_sym)
        # HTML tag escaping
        self.assertIn("&lt;테스트&gt;", html_sym)

    def test_09_search_query_deduplication(self):
        """키워드 중복 반복 방지 알고리즘 검증 (e.g., 2026 청년도약계좌 + 청년도약계좌 조건 -> 2026 청년도약계좌 조건)"""
        html = render_search_navigation_widget(
            keyword="2026 청년도약계좌",
            category="SUBSIDY",
            related_keywords=["청년도약계좌 조건", "청년도약계좌 신청기간"]
        )
        self.assertNotIn("청년도약계좌+청년도약계좌", html)
        self.assertNotIn("청년도약계좌%20청년도약계좌", html)
        self.assertIn("2026+%EC%B2%AD%EB%85%84%EB%8F%84%EC%95%BD%EA%B3%84%EC%A2%8C+%EC%A1%B0%EA%B1%B4", html)

    def test_10_24_7_autonomous_management_integration(self):
        """24/7 AI 기업 런타임 및 파이프라인의 Trick B 자동 관리 및 메트릭 기록 검증"""
        from engine.company_runtime import AICompanyStaff, CompanyLogger, SelfHealingPipeline
        from engine.pipeline.pipeline_flow import SequentialMediaPipeline
        from engine.maintenance.content_refresher import ContentRefresher
        from engine.analytics.feedback_loop import FeedbackLoop

        # 1. AI Staff Health Check
        staff = AICompanyStaff()
        health = staff.check_health()
        self.assertIn("05_Developer", health)
        self.assertIn("trick_b", health["05_Developer"])
        self.assertIn("details", health["05_Developer"])

        # 2. Pipeline Phase 3 component tracking & to_dict
        pipeline = SequentialMediaPipeline()
        p1 = pipeline.execute_phase1_discovery(keyword_override="2026 청년도약계좌")
        p2 = pipeline.execute_phase2_editorial(p1)
        p3 = pipeline.execute_phase3_assembly(p1, p2)
        self.assertIn("b365-search-nav", p3.components_present)

        # 3. Content Refresher protects internal search links
        refresher = ContentRefresher()
        audit_res = refresher.audit_html_links(p3.html_content, dry_run=False)
        self.assertFalse(audit_res["has_dead_links"])

        # 4. Feedback Loop factors in AFS search revenue
        feedback = FeedbackLoop()
        post_metric = feedback.simulate_performance_sync("test_post", "2026 청년도약계좌", "SUBSIDY", 100000)
        self.assertGreater(post_metric["adsense_revenue"], 0)


if __name__ == "__main__":
    unittest.main()
