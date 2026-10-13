# -*- coding: utf-8 -*-
"""
tests/test_omni_nerdwallet_benchmark.py
---------------------------------------
Comprehensive verification suite for Omni Calculator & NerdWallet Benchmark:
1. Omni Calculator: Pure JS reactivity, breakdown bar, dual controls, and 5 golden niches
2. NerdWallet Bento Grid: Takeaways card, 3-metric score card, 4 AdSense golden viewability slots
3. Strict QA Gates: Zero-Persona, Zero-Broken-Entity, Anti-Slop, Naver 1:1 keyword placement
4. Blogger Theme XML: Valid XML structure and stylesheet integrity
"""

import os
import sys
import xml.etree.ElementTree as ET
import unittest

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.visuals.saas_calculator import render_saas_calculator, get_calculator_by_category
from engine.agents.cro_monetizer import assemble_world_class_article
from engine.qa.gstack_auditor import GStackAuditor, FORBIDDEN_ENTITIES, FORBIDDEN_PERSONA_KEYWORDS
from engine.matcher.coupang_link_builder import render_affiliate_cta_box


class TestOmniNerdWalletBenchmark(unittest.TestCase):

    def setUp(self):
        self.auditor = GStackAuditor()

    def test_01_all_5_niches_calculator_generation(self):
        """5대 골든 니치 전용 계산기 생성 및 핵심 컴포넌트 검증"""
        categories = ["SAVINGS", "SUBSIDY", "TECH", "MEDICAL", "CAREER"]
        for cat in categories:
            html = render_saas_calculator(category_code=cat, keyword=f"2026 {cat} 테스트")
            self.assertIn("saas-calculator", html)
            self.assertIn("custom-saas-tool", html)
            self.assertIn("<script>", html)
            self.assertIn("</script>", html)
            self.assertIn("type=\"range\"", html)
            self.assertIn("copyToolVal", html)
            self.assertIn("초기화", html)
            self.assertIn("OMNI SIMULATOR", html)

            # Omni Visual Breakdown Bar existence
            self.assertIn("bar-", html, f"Breakdown bar missing for category {cat}")

            # Zero broken entities check
            for ent in FORBIDDEN_ENTITIES:
                self.assertNotRegex(html, ent, f"Broken entity {ent} found in {cat} calculator")

            # Zero persona check
            for p in FORBIDDEN_PERSONA_KEYWORDS:
                self.assertNotIn(p, html, f"Forbidden persona {p} found in {cat} calculator")

    def test_02_calculator_fallback_robustness(self):
        """알 수 없는 카테고리나 빈 키워드 처리 안전성 검증"""
        html_unknown = render_saas_calculator("UNKNOWN_NICHE", "")
        self.assertIn("saas-calculator", html_unknown)
        self.assertIn("<script>", html_unknown)
        self.assertIn("type=\"range\"", html_unknown)

        html_none = get_calculator_by_category(None, None)
        self.assertIn("saas-calculator", html_none)

    def test_03_nerdwallet_bento_hero_and_adsense_slots(self):
        """NerdWallet Bento Hero Card 및 4대 애드센스 슬롯 무결성 검증"""
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
            ]
        }

        article_html = assemble_world_class_article(sample_topic, sample_editorial)

        # 1. Bento Hero Card
        self.assertIn("bento-hero", article_html)
        self.assertIn("3초 핵심 요약", article_html)
        self.assertIn("PVS 25,000,000 pt", article_html)
        self.assertIn("에디토리얼 평점", article_html)
        self.assertIn("공식 인증 데이터 ✓", article_html)

        # 2. 4 Golden AdSense Slots
        self.assertIn("adsense-top", article_html)
        self.assertIn("adsense-mid", article_html)
        self.assertIn("adsense-mid-2", article_html)
        self.assertIn("adsense-bottom", article_html)
        self.assertIn("ADVERTISEMENT · B365 AD NETWORK", article_html)

        # 3. FAQ Chevron with pure CSS (Zero broken entities)
        self.assertIn("faq-chevron", article_html)
        self.assertNotIn("&#9662;", article_html)
        self.assertNotIn("&#10003;", article_html)

        # 4. Trick B: Google CSE & AFS Search Navigation Hub with Trigger Pills
        self.assertIn("b365-search-nav", article_html)
        self.assertIn("b365-search-pill", article_html)
        self.assertIn("b365-search-pills", article_html)
        self.assertIn("blogin365ai.blogspot.com/search?q=", article_html)

        # 5. GStack Auditor Full Audit Pass
        audit_res = self.auditor.audit_post(
            title="2026 청년도약계좌 실수령액 모의계산 및 자격 조건 핵심 가이드",
            html_content=article_html,
            keyword_package=sample_topic["keyword_package"]
        )
        self.assertTrue(audit_res["passed"], f"GStack audit failed: {audit_res.get('errors')}")

    def test_04_affiliate_cta_box_category_routing(self):
        """5대 카테고리별 제휴 CTA 박스 목적지 라우팅 검증"""
        # TECH -> Coupang
        tech_cta = render_affiliate_cta_box("맥북 에어 M3", "TECH")
        self.assertIn("coupang.com", tech_cta)
        self.assertIn("btn-affiliate-action", tech_cta)

        # SAVINGS -> MVNOHub
        savings_cta = render_affiliate_cta_box("알뜰폰 요금제", "SAVINGS")
        self.assertIn("mvnohub.kr", savings_cta)

        # SUBSIDY -> Hometax
        subsidy_cta = render_affiliate_cta_box("근로장려금", "SUBSIDY")
        self.assertIn("hometax.go.kr", subsidy_cta)

        # MEDICAL -> HIRA
        med_cta = render_affiliate_cta_box("라식 라섹", "MEDICAL")
        self.assertIn("hira.or.kr", med_cta)

        # CAREER -> HRD-Net
        career_cta = render_affiliate_cta_box("내일배움카드", "CAREER")
        self.assertIn("hrd.go.kr", career_cta)

    def test_05_blogin365_theme_xml_validity(self):
        """Blogger 전용 테마 XML 파일 유효성 및 구조 검증"""
        theme_path = os.path.join(BASE_DIR, "blogin365_fintech_theme.xml")
        self.assertTrue(os.path.exists(theme_path), "blogin365_fintech_theme.xml must exist")

        # Must parse cleanly with standard XML parser
        tree = ET.parse(theme_path)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("html"), f"Root tag must be html, got {root.tag}")

        # Read content to verify essential theme markers
        with open(theme_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Pretendard", content)
        self.assertIn("JetBrains Mono", content)
        self.assertIn("b365-site-wrapper", content)
        self.assertIn("b365-header", content)
        self.assertIn("b365-post", content)
        self.assertIn("b365-sidebar", content)
        self.assertIn("b365-footer", content)
        self.assertIn("saas-calculator", content)
        self.assertIn("adsense-slot", content)
        self.assertIn("b365-search-nav", content)
        self.assertIn("b365-search-pill", content)
        self.assertIn("gcse-search", content)
        self.assertIn("스마트 라이프 에디토리얼 팀", content)


if __name__ == "__main__":
    unittest.main()
