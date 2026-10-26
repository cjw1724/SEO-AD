# -*- coding: utf-8 -*-
"""
tests/test_v8_apex_architecture.py
-----------------------------------
Supreme Autonomous Media Enterprise (v8.0 Apex) Complete Verification Suite.
Validates all 4 Ironclad Directives & Multi-Niche Autonomous Portfolio:
  [철칙 1] 단발성 키워드 영구 금지 & 30-Day 토픽 클러스터(Topic Cluster) 독점
  [철칙 2] 1차 원천 데이터(Ground Truth) 100% 기반 집필 & 도메인 엄격 격리
  [철칙 3] 아폴리아식 8-Block 공감 카피라이팅 & UI 아키텍처 (Sticky TOC, 3대 비교표, 1원 단위 계산기)
  [철칙 4] 4대 무인 검증 게이트 (Zero-Slop, Zero-Persona, Zero-Broken-Entity, Information Gain, Ghost Mode)
  [추가] 5대 골든 니치 30-Day 클러스터 전수 완비 & 무인 자율 포트폴리오 관리자
"""

import os
import sys
import unittest
import tempfile
import json

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.matcher.domain_router import (
    classify_domain,
    get_domain_forbidden_words,
    DOMAIN_HAIR_TRANSPLANT,
    DOMAIN_AUTO_INSURANCE,
    DOMAIN_TELECOM,
    DOMAIN_SUBSIDY,
    DOMAIN_MEDICAL
)
from engine.matcher.topic_cluster_engine import (
    TopicClusterEngine,
    AutonomousClusterPortfolioManager,
    HAIR_TRANSPLANT_CLUSTER
)
from engine.matcher.topic_clusters import ALL_CLUSTERS
from engine.radar.crawl4ai_scout import Crawl4AIScout
from engine.radar.community_sentiment_scout import CommunitySentimentScout
from engine.matcher.experiential_verifier import ExperientialVerifier
from engine.visuals.saas_calculator import render_saas_calculator
from engine.agents.agency_stack import AgencyStack
from engine.agents.cro_monetizer import assemble_world_class_article, render_sticky_toc
from engine.qa.gstack_auditor import GStackAuditor, FORBIDDEN_ENTITIES, FORBIDDEN_PERSONA_KEYWORDS
from engine.agents.prompts_chat_pack import FORBIDDEN_SLOP_PHRASES


class TestV8ApexArchitecture(unittest.TestCase):

    def setUp(self):
        self.auditor = GStackAuditor()
        self.cluster_engine = TopicClusterEngine()

    # ==========================================================================
    # [철칙 1] 단발성 키워드 영구 금지 & 30-Day 토픽 클러스터 독점
    # ==========================================================================
    def test_01_topic_cluster_mesh_structure(self):
        """30-Day 토픽 클러스터 구조 및 30개 스포크 연속성 검증"""
        cluster = self.cluster_engine.get_cluster("hair_transplant")
        self.assertEqual(cluster["cluster_id"], "hair_transplant")
        self.assertEqual(cluster["category"], "HAIR")
        self.assertEqual(cluster["domain"], DOMAIN_HAIR_TRANSPLANT)
        self.assertIn("pillar", cluster)
        self.assertEqual(len(cluster["spokes"]), 30)

        # 1일차부터 30일차까지 순차 스포크 무결성 검사
        for day_idx in range(1, 31):
            spoke = cluster["spokes"][day_idx - 1]
            self.assertEqual(spoke["day"], day_idx)
            self.assertTrue(len(spoke["keyword"]) > 2)
            self.assertTrue(len(spoke["title"]) > 10)
            self.assertTrue(len(spoke["question"]) > 10)
            self.assertTrue(len(spoke["hook_next"]) > 5)

    def test_02_interlinking_mesh_rendering(self):
        """그물망 내부링크 박스 UI 생성 및 연속 소비 동선 검증"""
        html = self.cluster_engine.render_interlinking_mesh("3000모 모발이식 가격", category="HAIR")
        self.assertIn("b365-cluster-nav", html)
        self.assertIn("30-DAY TOPIC CLUSTER", html)
        self.assertIn("모발이식 & 탈모 팩트체크", html)
        self.assertIn("마스터 종합 기둥글", html)
        self.assertIn("이전 필수 분석", html)
        self.assertIn("다음 추천 필독", html)
        self.assertIn("핵심 궁금증", html)

    # ==========================================================================
    # [철칙 2] 1차 원천 데이터(Ground Truth) 100% 기반 집필
    # ==========================================================================
    def test_03_ground_truth_factset_integrity(self):
        """심평원 비급여 공시가 및 법령 조항 원천 데이터셋 무결성 검증"""
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

    def test_04_community_raw_pain_points_sentiment(self):
        """대다모, 디시 탈모갤, 뽐뿌 등 날것의 소비자 질문 수집 검증"""
        comm_scout = CommunitySentimentScout()
        sentiment = comm_scout.scout_community_sentiment("3000모 모발이식 가격", category="HAIR")
        sources_str = "".join(sentiment.get("community_sources", []))
        self.assertTrue("대다모" in sources_str or "디시" in sources_str)
        raw_ops = "".join(sentiment.get("raw_opinions", []))
        pains = "".join(sentiment.get("core_pain_points", []))
        self.assertTrue("스쿼트" in raw_ops or "스쿼트" in pains)
        self.assertTrue("테크니션" in raw_ops or "모수" in raw_ops)

    def test_05_strict_domain_isolation_zero_contamination(self):
        """모발이식 포스트에 임플란트, 치과, 도수치료, 알뜰폰 등 단 1단어도 유입되지 않음을 검증"""
        domain = classify_domain("3000모 모발이식 가격", category="HAIR")
        self.assertEqual(domain, DOMAIN_HAIR_TRANSPLANT)

        forbidden_words = get_domain_forbidden_words(DOMAIN_HAIR_TRANSPLANT)
        self.assertIn("임플란트", forbidden_words)
        self.assertIn("골유착", forbidden_words)
        self.assertIn("치조골 뼈이식", forbidden_words)
        self.assertIn("상악동거상술", forbidden_words)
        self.assertIn("지르코니아", forbidden_words)
        self.assertIn("도수치료", forbidden_words)

        agency = AgencyStack()
        topic = {
            "keyword": "3000모 모발이식 가격",
            "category": "HAIR",
            "cpc": 6800,
            "title": "3000모 모발이식 가격 및 비절개 FUE vs 절개 FUT 견적서 함정 분석",
            "subs": ["3000모 모발이식 가격 비교", "모발이식 모수 모낭수 차이", "모발이식 2주차 운동 주의사항"]
        }
        editorial = agency._build_deterministic_content(topic)
        html = assemble_world_class_article(topic, editorial)

        # Contamination inspection
        audit = self.auditor.audit_post(topic["title"], html, keyword_package={"main": topic["keyword"], "subs": topic["subs"]})
        gate9 = next(g for g in audit["gate_results"] if "Gate 9" in g["gate"])
        self.assertEqual(gate9["status"], "PASS")

        for fw in forbidden_words:
            self.assertNotIn(fw, html, f"Cross-domain contamination detected: '{fw}' in hair transplant post!")

    # ==========================================================================
    # [철칙 3] 아폴리아식 8-Block 공감 카피라이팅 & UI 아키텍처
    # ==========================================================================
    def test_06_hair_transplant_saas_calculator_1krw_precision(self):
        """1원 단위 모발이식 숨은 비용 모의계산기 (FUE/FUT/무삭발/약값/세액공제) 검증"""
        calc_html = render_saas_calculator("HAIR", "3000모 모발이식 가격")
        self.assertIn("editorial-calculator-card", calc_html)
        self.assertIn("calcHairTransplant()", calc_html)
        self.assertIn("slider-hair-count", calc_html)
        self.assertIn("select-hair-method", calc_html)
        self.assertIn("select-hair-years", calc_html)
        self.assertIn("select-hair-tax", calc_html)
        self.assertIn("result-hair-total", calc_html)
        self.assertIn("소득세법 제59조의4", calc_html)
        self.assertIn("미용 목적 (세액공제 0원", calc_html)

    def test_07_apolia_8block_and_sticky_toc(self):
        """8개 블록(Hero, 3줄 Bento, Hook, H2별 한줄답, 비교표, 계산기, Sticky TOC, 클러스터) 완결 검증"""
        topic = {
            "keyword": "3000모 모발이식 가격",
            "category": "HAIR",
            "cpc": 6800,
            "title": "3000모 모발이식 가격 및 비절개 FUE vs 절개 FUT 견적서 함정 분석",
            "subs": ["3000모 모발이식 가격 비교", "모발이식 모수 모낭수 차이", "모발이식 2주차 운동 주의사항"]
        }
        agency = AgencyStack()
        editorial = agency._build_deterministic_content(topic)
        html = assemble_world_class_article(topic, editorial)

        # Block 1: Hero title & badges
        self.assertIn("b365-hero-header", html)
        self.assertIn("badge-dwell", html)
        self.assertIn("Blogin 365 AI 에디토리얼 팀", html)

        # Block 2: 3-line Bento Hero Box
        self.assertIn("bento-hero", html)

        # Block 3: Psychological Hook
        self.assertIn("b365-psychological-hook", html)

        # Block 4: H2 callout one-line answer
        self.assertIn("b365-featured-callout", html)

        # Block 5: 3 comparative tables & timeline stepper
        self.assertIn("b365-comp-table-1", html)
        self.assertIn("비절개 (FUE)", html)
        self.assertIn("절개 (FUT)", html)
        self.assertIn("b365-comp-table-2", html)
        self.assertIn("b365-comp-table-3", html)
        self.assertIn("b365-stepper", html)
        self.assertIn("골든타임", html)

        # Block 6: 1 KRW Reactive SaaS Calculator
        self.assertIn("custom-saas-tool", html)

        # Block 7: Floating Sticky TOC
        self.assertIn("b365-sticky-toc", html)
        self.assertIn("b365-toc-link", html)

        # Block 8: Topic Cluster Interlinking Mesh
        self.assertIn("b365-cluster-nav", html)

    # ==========================================================================
    # [철칙 4] 4대 무인 검증 게이트 (Zero-Slop, Zero-Persona, Zero-Broken-Entity, HCU)
    # ==========================================================================
    def test_08_gstack_ten_gates_audit_pass(self):
        """10대 무인 검수 게이트 전원 통과 검증"""
        topic = {
            "keyword": "3000모 모발이식 가격",
            "category": "HAIR",
            "cpc": 6800,
            "title": "3000모 모발이식 가격 및 비절개 FUE vs 절개 FUT 견적서 함정 분석",
            "subs": ["3000모 모발이식 가격 비교", "모발이식 모수 모낭수 차이", "모발이식 2주차 운동 주의사항"]
        }
        agency = AgencyStack()
        editorial = agency._build_deterministic_content(topic)
        html = assemble_world_class_article(topic, editorial)

        audit = self.auditor.audit_post(
            topic["title"],
            html,
            keyword_package={"main": topic["keyword"], "subs": topic["subs"]}
        )

        self.assertTrue(audit["passed"], f"GStack audit failed: {audit['errors']}")
        self.assertEqual(len(audit["errors"]), 0)
        self.assertGreaterEqual(audit["hcu_score"], 85)
        self.assertGreaterEqual(audit["naturalness_score"], 80)
        self.assertGreaterEqual(audit["info_gain_score"], 85)

        # Check Zero Broken Entity
        for ent in FORBIDDEN_ENTITIES:
            self.assertNotRegex(html, ent)

        # Check Zero Persona
        for persona in FORBIDDEN_PERSONA_KEYWORDS:
            self.assertNotIn(persona, html)

    def test_09_ghost_mode_defensive_ad_and_link_hiding(self):
        """Ghost Mode(IS_ADSENSE_APPROVED=false) 시 빈 광고 슬롯 및 제휴 가교 링크 100% 숨김 검증"""
        topic = {
            "keyword": "3000모 모발이식 가격",
            "category": "HAIR",
            "cpc": 6800,
            "title": "3000모 모발이식 가격 및 비절개 FUE vs 절개 FUT 견적서 함정 분석",
            "subs": ["3000모 모발이식 가격 비교", "모발이식 모수 모낭수 차이", "모발이식 2주차 운동 주의사항"]
        }
        agency = AgencyStack()
        editorial = agency._build_deterministic_content(topic)

        # Force dry-run ghost mode (IS_ADSENSE_APPROVED=false)
        html = assemble_world_class_article(topic, editorial, is_adsense_approved=False)

        self.assertNotIn("<ins class=\"adsbygoogle\"", html, "Ghost mode must hide live adsbygoogle units!")
        self.assertNotIn("coupang.com", html, "Ghost mode must not expose direct affiliate bridge links!")
        self.assertIn("editorial-info-box", html, "Ghost mode must render pure informational guide box!")

    # ==========================================================================
    # [추가 검증] 5대 골든 니치 30-Day 토픽 클러스터 전수 완비 & 무인 자율 포트폴리오
    # ==========================================================================
    def test_10_all_five_golden_niches_clusters_complete(self):
        """5대 골든 니치 전 영역 30-Day 클러스터 지식 그래프(총 150개 스포크) 완전성 검증"""
        expected_clusters = ["hair_transplant", "government_subsidy", "cashflow_hacks", "medical_wellness", "career_cert"]
        self.assertEqual(len(ALL_CLUSTERS), 5)
        for cid in expected_clusters:
            self.assertIn(cid, ALL_CLUSTERS, f"Cluster '{cid}' missing in ALL_CLUSTERS!")
            cdata = ALL_CLUSTERS[cid]
            self.assertEqual(len(cdata["spokes"]), 30, f"Cluster '{cid}' must contain exactly 30 spokes!")
            self.assertIn("pillar", cdata)
            self.assertTrue(len(cdata["pillar"]["title"]) > 10)
            # Verify each spoke
            for spoke in cdata["spokes"]:
                self.assertIn("day", spoke)
                self.assertIn("keyword", spoke)
                self.assertIn("title", spoke)
                self.assertIn("question", spoke)
                self.assertIn("hook_next", spoke)
                self.assertTrue(len(spoke["keyword"]) > 2)

    def test_11_autonomous_portfolio_graduation_and_rotation(self):
        """클러스터 30일 완주 시 최고 수익성 니치로 무인 자율 로테이션(승계) 검증"""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as f:
            f.write(json.dumps({
                "active_cluster_id": "hair_transplant",
                "current_day": 31,
                "total_published_in_cluster": 30,
                "cluster_progress": {
                    "hair_transplant": {"cluster_name": "모발이식", "current_day": 31, "completed_cycles": 0}
                }
            }))
            temp_path = f.name

        try:
            mgr = AutonomousClusterPortfolioManager(state_file=temp_path)
            res = mgr.auto_select_active_cluster()
            self.assertEqual(res["action"], "ROTATE")
            self.assertEqual(res["current_day"], 1)
            self.assertNotEqual(res["cluster_id"], "hair_transplant")
            # hair_transplant should now have completed_cycles = 1
            state = mgr.load_state()
            self.assertEqual(state["cluster_progress"]["hair_transplant"]["completed_cycles"], 1)
            self.assertEqual(state["cluster_progress"]["hair_transplant"]["status"], "COMPLETED")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_12_multi_niche_interlinking_mesh_rendering(self):
        """5대 골든 니치 전 카테고리별 상호 내부링크 그물망 HTML 렌더링 검증"""
        for cat in ["HAIR", "SUBSIDY", "SAVINGS", "MEDICAL", "CAREER"]:
            html = self.cluster_engine.render_interlinking_mesh("테스트키워드", category=cat)
            self.assertIn("b365-cluster-nav", html)
            self.assertIn("30-DAY TOPIC CLUSTER", html)
            self.assertIn("마스터 종합 기둥글", html)
            self.assertIn("이전 필수 분석", html)
            self.assertIn("다음 추천 필독", html)
            self.assertTrue(len(html) > 2500)


if __name__ == "__main__":
    unittest.main()
