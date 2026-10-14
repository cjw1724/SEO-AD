# -*- coding: utf-8 -*-
"""
tests/test_humanization_upgrade.py
-----------------------------------
Comprehensive verification suite for the Natural Humanization & Authentic Visual Upgrade Architecture:
1. CommunitySentimentScout (Phase 1-1 Community & Forum Raw Voice Scraper)
2. ExperientialVerifier (Phase 1-2 3-Week Editorial Fact Verification & Zero-Persona Compliance)
3. HandcraftedAnnotationRenderer (Phase 2 Mock Amateur Photo Frame & Inline SVG Annotations)
4. HumanVoiceEngine (Phase 3 Sentence Burstiness, Colloquialization, Conversational Subheaders)
5. GStackAuditor Gate 8 Integration (AI Detection Bypass & Naturalness QA)
6. SequentialMediaPipeline E2E Humanization Dataflow
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.radar.community_sentiment_scout import CommunitySentimentScout
from engine.matcher.experiential_verifier import ExperientialVerifier
from engine.visuals.handcrafted_annotation_renderer import HandcraftedAnnotationRenderer
from engine.agents.human_voice_engine import HumanVoiceEngine
from engine.qa.gstack_auditor import GStackAuditor
from engine.agents.cro_monetizer import assemble_world_class_article
from engine.pipeline.pipeline_flow import SequentialMediaPipeline


class TestHumanizationUpgrade(unittest.TestCase):

    def setUp(self):
        self.scout = CommunitySentimentScout()
        self.verifier = ExperientialVerifier()
        self.renderer = HandcraftedAnnotationRenderer()
        self.human_voice = HumanVoiceEngine()
        self.auditor = GStackAuditor()

    # --------------------------------------------------------------------------
    # 1. Community Sentiment Scout Tests
    # --------------------------------------------------------------------------
    def test_community_sentiment_scout_multi_categories(self):
        categories = ["TECH", "SUBSIDY", "SAVINGS", "CASHFLOW", "MEDICAL", "CAREER"]
        for cat in categories:
            res = self.scout.scout_community_sentiment(keyword=f"2026 {cat} 테스트", category=cat)
            self.assertEqual(res["category"], cat)
            self.assertIn("raw_opinions", res)
            self.assertGreaterEqual(len(res["raw_opinions"]), 1)
            self.assertIn("core_pain_points", res)
            self.assertGreaterEqual(len(res["core_pain_points"]), 1)
            self.assertIn("colloquial_slang", res)
            self.assertGreaterEqual(len(res["colloquial_slang"]), 2)
            self.assertTrue(len(res["sentiment_summary"]) > 10)
            self.assertTrue(len(res["community_sources"]) >= 1)

    # --------------------------------------------------------------------------
    # 2. Experiential Verifier & Zero-Persona Compliance
    # --------------------------------------------------------------------------
    def test_experiential_verifier_structure_and_zero_persona(self):
        factset = self.verifier.build_experiential_factset("2026 청년도약계좌", category="SUBSIDY")
        
        # Structure assertions
        self.assertIn("pros_real", factset)
        self.assertIn("cons_unfiltered", factset)
        self.assertEqual(len(factset["pros_real"]), 3)
        self.assertEqual(len(factset["cons_unfiltered"]), 2)
        self.assertIn("failure_anecdote", factset)
        self.assertIn("subtle_pro_tip", factset)
        
        # Zero-Persona Policy enforcement: No fake names or journalist credentials
        forbidden_names = ["김재현", "금융 전문 기자", "전문 기자", "수석 에디터", "박민수", "이진우"]
        factset_str = str(factset)
        for fn in forbidden_names:
            self.assertNotIn(fn, factset_str, f"Forbidden persona '{fn}' detected in experiential factset")
        
        self.assertIn("에디토리얼 팀", factset["tester_attribution"])

    # --------------------------------------------------------------------------
    # 3. Handcrafted Annotation & Mock Photo Visual Renderer
    # --------------------------------------------------------------------------
    def test_handcrafted_annotation_renderer(self):
        # 1. Circle & Arrow SVG
        circle_svg = self.renderer.render_hand_drawn_circle_svg()
        arrow_svg = self.renderer.render_hand_drawn_arrow_svg()
        self.assertIn("<svg", circle_svg)
        self.assertIn("hand-drawn-marker", circle_svg)
        self.assertIn("<svg", arrow_svg)
        self.assertIn("hand-drawn-arrow", arrow_svg)

        # 2. Mock Amateur Camera Photo Frame (Permanently deactivated in Patch 2)
        photo_card = self.renderer.render_amateur_photo_card(
            title="청년도약계좌 실측 대조 리포트",
            caption="홈택스 모의 화면 캡처",
            category="SUBSIDY"
        )
        self.assertEqual("", photo_card, "Viewfinder photo card must be permanently deactivated")

        # 3. Unfiltered Pros & Cons Board
        pros = ["장점1", "장점2", "장점3"]
        cons = ["단점1", "단점2"]
        board_html = self.renderer.render_unfiltered_pros_cons_board(pros, cons)
        self.assertIn("unfiltered-review-board", board_html)
        self.assertIn("실사용 찐 장점 3가지", board_html)
        self.assertIn("솔직히 아쉬웠던 찐 단점 2가지", board_html)
        self.assertIn("✓", board_html)
        self.assertIn("✗", board_html)
        self.assertNotIn("&#10003;", board_html)

    # --------------------------------------------------------------------------
    # 4. Human Voice Engine & Burstiness
    # --------------------------------------------------------------------------
    def test_human_voice_engine_burstiness_and_subheaders(self):
        # Burstiness injection
        sample_paragraph = (
            "청년도약계좌는 정부 기여금을 매칭해주는 정책 금융 상품입니다. "
            "매월 최대 70만원을 납입할 수 있으며 연 6퍼센트 상당의 우대 금리를 제공합니다. "
            "5년 만기 시 최대 5천만원의 목돈을 수령할 수 있습니다."
        )
        burst_text = self.human_voice.inject_burstiness_to_paragraphs(sample_paragraph)
        self.assertNotEqual(sample_paragraph, burst_text)
        self.assertIn("<strong>", burst_text)

        # Subheader transformation preserving 1:1 sub-keyword
        sub_kw = "2026 청년도약계좌 조건"
        h2 = self.human_voice.humanize_subheaders(sub_kw, "1. 2026 청년도약계좌 조건 분석", index=1)
        self.assertIn(sub_kw, h2, "Sub-keyword must be preserved in humanized H2")

        # Full editorial content humanization
        editorial = {
            "keyword": "2026 청년도약계좌",
            "subtitle": "2026 청년도약계좌 공식 데이터 분석 보고서입니다.",
            "sections": [
                {
                    "heading": f"1. {sub_kw} 분석",
                    "content": f"<p>{sub_kw}에 대해 알아봅니다. 정부 기여금이 지원됩니다.</p>"
                },
                {
                    "heading": "2. 신청 절차",
                    "content": "<p>서류 준비가 필수적입니다. 기한을 지켜야 합니다.</p>"
                }
            ],
            "faq": []
        }
        sentiment = self.scout.scout_community_sentiment("2026 청년도약계좌", "SUBSIDY")
        factset = self.verifier.build_experiential_factset("2026 청년도약계좌", "SUBSIDY")
        humanized = self.human_voice.humanize_editorial_content(
            editorial_data=editorial,
            sentiment_data=sentiment,
            factset_data=factset,
            sub_keywords=[sub_kw, "신청 절차"]
        )
        self.assertTrue(humanized.get("humanized"))
        self.assertTrue(len(humanized["subtitle"]) > 10)
        self.assertNotIn("직접 3주간 테스트해본 결론", humanized["subtitle"])
        self.assertIn("커뮤니티 실제 이용자들의 솔직한 반응", humanized["sections"][0]["content"])
        self.assertIn("에디토리얼 팀의 실제 시행착오", humanized["sections"][1]["content"])

    # --------------------------------------------------------------------------
    # 5. GStack Auditor Gate 8 Naturalness & AI Detection Bypass Integration
    # --------------------------------------------------------------------------
    def test_gstack_gate8_naturalness_audit(self):
        topic = {
            "keyword": "2026 청년도약계좌",
            "category": "SUBSIDY",
            "tier": "최적",
            "ratio": 75.0,
            "subs": ["2026 청년도약계좌 조건", "2026 청년도약계좌 금리", "2026 청년도약계좌 금액"],
            "pvs": 25000000,
            "cpc": 3200,
            "keyword_package": {
                "main": "2026 청년도약계좌",
                "subs": ["2026 청년도약계좌 조건", "2026 청년도약계좌 금리", "2026 청년도약계좌 금액"]
            }
        }
        editorial = {
            "keyword": "2026 청년도약계좌",
            "subtitle": "2026 청년도약계좌 공식 데이터 및 핵심 기준 대조 분석 보고서입니다.",
            "sections": [
                {
                    "heading": "1. 2026 청년도약계좌 조건 핵심 분석",
                    "content": "<p>2026 청년도약계좌 조건 기준이 완화되었습니다. 실제 수혜율이 상승했습니다.</p>"
                },
                {
                    "heading": "2. 2026 청년도약계좌 금리 비교",
                    "content": "<p>2026 청년도약계좌 금리 세부 구간을 점검해야 합니다. 우대 금리가 차등 적용됩니다.</p>"
                },
                {
                    "heading": "3. 2026 청년도약계좌 금액 모의 계산",
                    "content": "<p>2026 청년도약계좌 금액 산정 시 비과세 혜택이 적용됩니다. 최대 5천만원 수령이 가능합니다.</p>"
                }
            ],
            "faq": [
                {"question": "자격 기준은 어떻게 되나요?", "answer": "중위소득 기준을 충족해야 합니다."}
            ]
        }
        
        # Add sentiment & factset and humanize
        sentiment = self.scout.scout_community_sentiment(topic["keyword"], topic["category"])
        factset = self.verifier.build_experiential_factset(topic["keyword"], topic["category"])
        topic["sentiment"] = sentiment
        topic["factset"] = factset
        humanized_editorial = self.human_voice.humanize_editorial_content(
            editorial_data=editorial,
            sentiment_data=sentiment,
            factset_data=factset,
            sub_keywords=topic["subs"]
        )

        assembled_html = assemble_world_class_article(topic, humanized_editorial)
        title = "2026 청년도약계좌 실수령액 모의계산 및 자격 조건 핵심 가이드"

        # Gate 8 evaluation
        nat_res = self.auditor.evaluate_human_naturalness(title, assembled_html)
        self.assertTrue(nat_res["passed"], f"Gate 8 Naturalness failed: {nat_res.get('errors')}")
        self.assertGreaterEqual(nat_res["score"], 80)
        self.assertTrue(nat_res["metrics"]["has_authentic_visuals"])
        self.assertGreaterEqual(nat_res["metrics"]["colloquial_markers"], 4)

        # Full 8-Gate post audit
        full_audit = self.auditor.audit_post(title, assembled_html, keyword_package=topic["keyword_package"])
        self.assertTrue(full_audit["passed"], f"Full 8-Gate Audit failed: {full_audit.get('errors')}")

    # --------------------------------------------------------------------------
    # 6. SequentialMediaPipeline E2E Humanization Dataflow
    # --------------------------------------------------------------------------
    def test_pipeline_flow_humanization_integration(self):
        pipeline = SequentialMediaPipeline()
        p1 = pipeline.execute_phase1_discovery(keyword_override="2026 청년도약계좌")
        
        self.assertIn("sentiment", p1.raw_topic)
        self.assertIn("factset", p1.raw_topic)
        self.assertIn("raw_opinions", p1.sentiment)
        self.assertIn("pros_real", p1.factset)
        
        p2 = pipeline.execute_phase2_editorial(p1)
        self.assertTrue(p2.editorial_dict.get("humanized"))
        
        p3 = pipeline.execute_phase3_assembly(p1, p2)
        self.assertNotIn("amateur-photo-card-wrapper", p3.html_content)
        self.assertIn("unfiltered-review-board", p3.html_content)
        
        p4 = pipeline.execute_phase4_qa(p1, p3)
        self.assertTrue(p4.passed)
        self.assertGreaterEqual(p4.hcu_score, 80)


if __name__ == "__main__":
    unittest.main()
