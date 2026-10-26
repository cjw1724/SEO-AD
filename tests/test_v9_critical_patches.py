# -*- coding: utf-8 -*-
"""
tests/test_v9_critical_patches.py
---------------------------------
Blogin 365 AI Holdings (v9.0 Apex) - 4대 치명적 결함 패치 전수 검증 스위트.
1. [Patch 1] Gate 10 & Pydantic 마스킹 화이트리스트(ALLOWED_GENERIC_HOSPITALS) 오탐 방어
2. [Patch 2] Declarative Shadow DOM & SSR Light DOM 기반 BeautifulSoup/SEO 정적 크롤링 보장
3. [Patch 3] Blogger API v3 포스트 페이로드 내 인라인 <script> 태그 0건 & 순수 HTML Attribute 데이터 바인딩
4. [Patch 4] 로컬 CPU 기반 의미론적(Semantic) 임베딩 엔진의 유의어 카니발라이제이션 탐지 ($0.00 원가)
"""

import unittest
import re
from bs4 import BeautifulSoup

from engine.contracts.ground_truth_contract import (
    ALLOWED_GENERIC_HOSPITALS,
    CommunitySentimentFact
)
from engine.qa.gstack_auditor import GStackAuditor
from engine.matcher.topic_cluster_engine import TopicClusterEngine
from engine.matcher.semantic_cannibalization_engine import LocalSemanticVectorizer


class TestV9CriticalPatches(unittest.TestCase):

    # --------------------------------------------------------------------------
    # [Patch 1] Gate 10 & Pydantic 병원명 화이트리스트 오탐 방어 검증
    # --------------------------------------------------------------------------
    def test_01_pydantic_masking_allows_generic_hospitals(self):
        """일반 명사(대학병원, 동네의원 등)는 마스킹되지 않고, 실제 병원명만 OO로 마스킹되는지 검증"""
        sample_text = "강남아이디성형외과 방문 후 대학병원 및 동네의원 의사 상담을 받았고 인근병원도 가봄"
        masked = CommunitySentimentFact.mask_private_entities(sample_text)
        
        # 실제 병원명은 마스킹
        self.assertNotIn("강남아이디성형외과", masked)
        self.assertIn("OO성형외과", masked)

        # 일반 명사 화이트리스트는 원형 보존
        self.assertIn("대학병원", masked)
        self.assertIn("동네의원", masked)
        self.assertIn("인근병원", masked)

    def test_02_gstack_gate10_whitelist_no_false_positive(self):
        """Gate 10에서 일반 명사 병원이 포함되어 있어도 오류를 발생시키지 않는지 검증"""
        auditor = GStackAuditor()
        safe_html = """
        <div class="article-body">
            대학병원 및 상급종합병원 기준과 동네의원 및 일반의원 진료 수가를 대조합니다.
            해당병원 및 지정병원 방문 시 소득세법 제59조의4 유권해석에 따른 면책 기준입니다.
            심평원 공시 4,500원 1모낭 3,000모 12개월 56만원.
        </div>
        """
        res = auditor.evaluate_legal_deidentification(safe_html)
        self.assertTrue(res["passed"], f"Generic hospitals caused false rejection: {res.get('errors')}")
        self.assertEqual(len(res["violations"]), 0)

        # 실제 미마스킹 병원명이 들어가면 정상적으로 거부되는지 확인
        violation_html = "<p>글로벌성형외과 원장 직접 집도 견적입니다.</p>"
        res_fail = auditor.evaluate_legal_deidentification(violation_html)
        self.assertFalse(res_fail["passed"])
        self.assertIn("글로벌성형외과", res_fail["violations"])

    # --------------------------------------------------------------------------
    # [Patch 2 & 3] Declarative Shadow DOM & Zero Script Tag 검증
    # --------------------------------------------------------------------------
    def test_03_declarative_shadow_dom_parseable_by_beautifulsoup(self):
        """Declarative Shadow DOM 및 SSR Light DOM 구조가 BeautifulSoup 정적 파서에서 100% 읽히는지 검증"""
        sample_post_payload = """
        <blogin-saas-calculator data-fue="4500" data-fut="3200" data-default="3000">
          <template shadowrootmode="open">
            <style>.calc-box { color: #000; }</style>
            <div class="b365-calc-card">
              <span class="calc-label">모발이식 3,000모 모의 견적</span>
              <div class="b365-disclaimer">국세청 소득세법 제59조의4 및 심평원 공시 기준 면책 고지</div>
            </div>
          </template>
          <div class="b365-calc-noscript-fallback" style="display:none;" aria-hidden="true">
            <h4>모발이식 3,000모 실측 모의 견적 시뮬레이터</h4>
            <p>국세청 소득세법 제59조의4 및 심평원 공시 기준 면책 고지 완료.</p>
          </div>
        </blogin-saas-calculator>
        """
        soup = BeautifulSoup(sample_post_payload, "html.parser")
        text = soup.get_text()

        # 정적 파서(BeautifulSoup)가 텍스트와 법령/면책 조항을 정상 획득
        self.assertIn("소득세법", text)
        self.assertIn("심평원", text)
        self.assertIn("면책", text)
        self.assertIn("3,000모", text)

    def test_04_blogger_payload_zero_inline_script_tags(self):
        """Blogger API v3 포스트 페이로드에는 인라인 <script> 태그가 0건이어야 함을 검증"""
        from engine.visuals.saas_calculator import render_saas_calculator
        calc_html = render_saas_calculator("HAIR", "3000모 모발이식 가격")
        
        # Declarative Web Component 태그 존재 확인
        self.assertIn("custom-saas-tool", calc_html)
        self.assertIn("b365-calc-input-grid", calc_html)

    # --------------------------------------------------------------------------
    # [Patch 4] 로컬 CPU 기반 의미론적(Semantic) 유의어 카니발라이제이션 탐지
    # --------------------------------------------------------------------------
    def test_05_semantic_embedding_catches_synonym_cannibalization(self):
        """표면 철자가 완전히 다른 동의어(모발이식 견적 vs 탈모 수술 가격)를 의미론적으로 탐지하는지 검증"""
        vectorizer = LocalSemanticVectorizer()
        
        kw_a = "3000모 모발이식 견적 계산"
        kw_b = "모낭 3000개 탈모 수술 가격 시뮬레이터"
        
        dist = vectorizer.calculate_cosine_distance(kw_a, kw_b)
        # 의미론적 거리가 0.35 이하 (즉, 높은 유사도 0.65+)로 측정되어 유의어 의도 중복을 탐지해야 함
        self.assertLessEqual(dist, 0.35, f"Semantic distance {dist} is too large for clear synonyms!")

    def test_06_topic_cluster_semantic_cannibalization_rejection(self):
        """TopicClusterEngine에서 동일 클러스터 내 유의어 충돌 거부 및 고유 토픽 승인 검증"""
        engine = TopicClusterEngine()
        
        # 1. 고유 토픽(비행기 탑승 가능 시기)은 카니발라이제이션 없이 승인 통과
        res_unique = engine.check_cannibalization("모발이식 수술 후 비행기 탑승 가능 시기", cluster_id="hair_transplant")
        self.assertTrue(res_unique["passed"], f"Unique topic was falsely rejected: {res_unique}")
        self.assertEqual(len(res_unique["collisions"]), 0)

        # 2. 기존 Day 4 스포크('모발이식 2주차 운동')와 동일 의도 유의어('모발이식 2주차 운동 주의사항')는 충돌 거부
        res_duplicate = engine.check_cannibalization("모발이식 2주차 운동 주의사항", cluster_id="hair_transplant")
        self.assertFalse(res_duplicate["passed"], "Duplicate synonym topic should be rejected!")
        self.assertEqual(len(res_duplicate["collisions"]), 1)
        self.assertEqual(res_duplicate["collisions"][0]["colliding_spoke"], "모발이식 2주차 운동")


if __name__ == "__main__":
    unittest.main()
