# -*- coding: utf-8 -*-
"""
tests/test_production_patches.py
---------------------------------
Comprehensive verification suite for the 4 production-level patches:
1. Patch 1: AdSense Approval Defense Flag (IS_ADSENSE_APPROVED)
2. Patch 2: Coupang Partners HMAC-SHA256 Real-time API Client & Fallback
3. Patch 3: Trick B High-CPC Commercial CSE Pills & Real-time Calculator CTA
4. Patch 4: Zero-Random Deterministic Feedback & GSC Candidate Extraction & Queue Flush
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import unquote

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.agents.cro_monetizer import (
    assemble_world_class_article,
    render_informational_guide_box,
    render_search_navigation_widget
)
from engine.matcher.coupang_link_builder import render_affiliate_cta_box, build_coupang_search_url
from engine.monetization.coupang_api import CoupangPartnersClient, get_coupang_client
from engine.visuals.saas_calculator import render_saas_calculator
from engine.indexing.instant_indexer import InstantIndexer, flush_indexing_queue
from engine.analytics.feedback_loop import FeedbackLoop
from engine.qa.gstack_auditor import GStackAuditor


class TestProductionPatches(unittest.TestCase):

    def setUp(self):
        self.auditor = GStackAuditor()
        self.sample_topic = {
            "keyword": "2026 청년도약계좌",
            "category": "SUBSIDY",
            "cpc": 3200,
            "pvs": 25000000,
            "keyword_package": {
                "main": "2026 청년도약계좌",
                "subs": ["2026 청년도약계좌 조건", "2026 청년도약계좌 신청기간", "2026 청년도약계좌 금리"]
            }
        }
        self.sample_editorial = {
            "keyword": "2026 청년도약계좌",
            "subtitle": "2026 청년도약계좌 공식 데이터 및 핵심 기준 대조 분석 보고서입니다.",
            "sections": [
                {"heading": "1. 2026 청년도약계좌 조건 핵심 분석", "content": "<p>2026 청년도약계좌 조건 기준을 상세히 확인합니다.</p>"},
                {"heading": "2. 2026 청년도약계좌 신청기간 안내", "content": "<p>2026 청년도약계좌 신청기간 일정에 맞춰 서류를 준비합니다.</p>"},
                {"heading": "3. 2026 청년도약계좌 금리 모의 계산", "content": "<p>2026 청년도약계좌 금리 수령액을 사전에 점검합니다.</p>"}
            ],
            "faq": [
                {"question": "자격 요건은 어떻게 되나요?", "answer": "중위소득 기준을 충족해야 합니다."}
            ]
        }

    # =========================================================================
    # [패치 1] 애드센스 심사 방어 플래그 (IS_ADSENSE_APPROVED) 검증
    # =========================================================================

    def test_patch_1_adsense_review_defense_when_false(self):
        """IS_ADSENSE_APPROVED=false 일 때 외부 제휴 링크 숨김 및 순수 정보성 박스 렌더링 검증"""
        article_html = assemble_world_class_article(
            self.sample_topic,
            self.sample_editorial,
            is_adsense_approved=False
        )

        # 1. 외부 제휴 CTA 버튼 숨김 확인
        self.assertNotIn("btn-affiliate-action", article_html)
        self.assertNotIn("쿠팡 파트너스 활동의 일환으로", article_html)

        # 2. 순수 정보성 가이드 박스 렌더링 확인
        self.assertIn("editorial-info-box", article_html)
        self.assertIn("공식 정책 가이드라인", article_html)
        self.assertIn("정보성 검증 리포트", article_html)

        # 3. GStack 8대 게이트 무인 검수 통과 검증
        audit_res = self.auditor.audit_post(
            title="2026 청년도약계좌 실수령액 모의계산 및 자격 조건 핵심 가이드",
            html_content=article_html,
            keyword_package=self.sample_topic["keyword_package"]
        )
        self.assertTrue(audit_res["passed"], f"GStack audit failed when IS_ADSENSE_APPROVED=false: {audit_res.get('errors')}")

    def test_patch_1_full_monetization_when_true(self):
        """IS_ADSENSE_APPROVED=true 일 때 모든 제휴 CTA 버튼 풀가동 렌더링 검증"""
        article_html = assemble_world_class_article(
            self.sample_topic,
            self.sample_editorial,
            is_adsense_approved=True
        )

        # 1. 제휴 CTA 버튼 활성화 확인
        self.assertIn("btn-affiliate-action", article_html)
        self.assertIn("editorial-affiliate-box", article_html)

        # 2. 순수 정보성 대체 박스는 렌더링되지 않음 확인
        self.assertNotIn("editorial-info-box", article_html)

        # 3. GStack 8대 게이트 무인 검수 통과 검증
        audit_res = self.auditor.audit_post(
            title="2026 청년도약계좌 실수령액 모의계산 및 자격 조건 핵심 가이드",
            html_content=article_html,
            keyword_package=self.sample_topic["keyword_package"]
        )
        self.assertTrue(audit_res["passed"], f"GStack audit failed when IS_ADSENSE_APPROVED=true: {audit_res.get('errors')}")

    def test_patch_1_env_files_contain_flag(self):
        """SEO.env 및 .env.example에 IS_ADSENSE_APPROVED 환경변수 설정 여부 검증"""
        for env_path in [os.path.join(BASE_DIR, "SEO.env"), os.path.join(BASE_DIR, ".env.example")]:
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("IS_ADSENSE_APPROVED=", content)

    # =========================================================================
    # [패치 2] 쿠팡 파트너스 HMAC-SHA256 실제 딥링크 모듈 검증
    # =========================================================================

    def test_patch_2_coupang_hmac_signature_generation(self):
        """HMAC-SHA256 서명 규격 (CEA algorithm=HmacSHA256, access-key, signed-date, signature) 검증"""
        client = CoupangPartnersClient(
            access_key="test_access_key_123",
            secret_key="test_secret_key_456",
            sub_id="blogin365"
        )
        auth_header = client._generate_hmac("GET", "/v2/providers/affiliate_open_api/apis/openapi/products/search", "keyword=맥북")
        self.assertIn("CEA algorithm=HmacSHA256", auth_header)
        self.assertIn("access-key=test_access_key_123", auth_header)
        self.assertIn("signed-date=", auth_header)
        self.assertIn("signature=", auth_header)

    def test_patch_2_fallback_when_keys_missing(self):
        """API 키가 비어있을 때 standard search URL로 안전하게 폴백하는지 검증"""
        client = CoupangPartnersClient(access_key="", secret_key="")
        link = client.get_affiliate_search_link("맥북 에어 M3")
        self.assertTrue(link.startswith("https://www.coupang.com/np/search?q="))
        self.assertIn("coupang.com", link)

    @patch("requests.get")
    def test_patch_2_product_search_success(self, mock_get):
        """쿠팡 상품 검색 API 성공 시 1위 상품 URL 반환 검증"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "data": {
                "productData": [
                    {"productUrl": "https://link.coupang.com/re/AFFSDP?lptag=blogin365&pageKey=999"}
                ]
            }
        }
        mock_get.return_value = mock_resp

        client = CoupangPartnersClient(access_key="key", secret_key="secret")
        link = client.get_affiliate_search_link("스마트 모니터")
        self.assertEqual(link, "https://link.coupang.com/re/AFFSDP?lptag=blogin365&pageKey=999")

    @patch("requests.get")
    @patch("requests.post")
    def test_patch_2_deeplink_fallback(self, mock_post, mock_get):
        """상품 검색 실패 시 단축 딥링크 API로 폴백 및 link.coupang.com 발급 검증"""
        # 상품 검색은 빈 결과 반환
        mock_get_resp = MagicMock()
        mock_get_resp.status_code = 200
        mock_get_resp.json.return_value = {"data": {"productData": []}}
        mock_get.return_value = mock_get_resp

        # 딥링크 API는 shortenUrl 반환
        mock_post_resp = MagicMock()
        mock_post_resp.status_code = 200
        mock_post_resp.json.return_value = {
            "data": [{"shortenUrl": "https://link.coupang.com/a/blogin365_short"}]
        }
        mock_post.return_value = mock_post_resp

        client = CoupangPartnersClient(access_key="key", secret_key="secret")
        link = client.get_affiliate_search_link("무선 키보드")
        self.assertEqual(link, "https://link.coupang.com/a/blogin365_short")

    def test_patch_2_build_coupang_search_url_integration(self):
        """build_coupang_search_url이 CoupangPartnersClient와 완벽히 결합되어 동작하는지 검증"""
        url = build_coupang_search_url("아이폰 16 프로")
        self.assertIn("coupang.com", url)

    # =========================================================================
    # [패치 3] 트릭 B (Google CSE 알약) 고단가 상업 쿼리 및 계산기 CTA 실시간 연동 검증
    # =========================================================================

    def test_patch_3_cse_pills_commercial_query_separation(self):
        """알약 버튼 텍스트는 깔끔하게 유지되고 data-query 및 onclick에 고단가 상업 키워드가 자동 첨부되는지 검증"""
        html = render_search_navigation_widget(
            keyword="2026 청년도약계좌",
            category="SUBSIDY",
            related_keywords=["청년도약계좌 조건", "청년도약계좌 신청기간"]
        )

        # 1. 알약 태그 존재 확인
        self.assertIn("b365-search-pill", html)

        # 2. data-query에 '금리 비교 추천 자격 조회' 포함 확인
        self.assertIn('data-query="', html)
        self.assertIn("금리 비교 추천 자격 조회", html)

        # 3. onclick 이벤트에서 data-query 또는 상업 쿼리가 execute 인자로 전달되는지 확인
        self.assertIn("el.execute(", html)

        # 4. href는 기존 블로그 맞춤검색 URL 인코딩을 온전히 유지
        self.assertIn("https://blogin365ai.blogspot.com/search?q=", html)

    def test_patch_3_calculator_realtime_cta_buttons(self):
        """5대 골든 니치 모든 계산기에 실시간 CTA/CSE 버튼이 배치되어 있고 슬라이더 이벤트와 연동되는지 검증"""
        categories = ["SAVINGS", "SUBSIDY", "TECH", "MEDICAL", "CAREER"]
        for cat in categories:
            calc_html = render_saas_calculator(cat, f"2026 {cat} 테스트")

            # 1. 동적 CTA 버튼 클래스 존재 확인
            self.assertIn("calc-dynamic-cta-btn", calc_html, f"Missing calc-dynamic-cta-btn in {cat}")

            # 2. 초기 CTA 문구 확인
            self.assertIn("👉 계산된", calc_html)

            # 3. JS 슬라이더 계산 함수 내에서 버튼 텍스트를 실시간으로 업데이트하는지 확인
            self.assertIn("ctaBtn.innerText =", calc_html, f"Missing ctaBtn.innerText update in {cat} JS")

    # =========================================================================
    # [패치 4] Google Indexing API & GSC 실측 피드백 루프 검증
    # =========================================================================

    def test_patch_4_zero_random_in_feedback_loop(self):
        """feedback_loop.py 내에서 random.randint 및 random 모듈이 완전히 제거되었는지 소스 검증"""
        feedback_path = os.path.join(BASE_DIR, "engine", "analytics", "feedback_loop.py")
        with open(feedback_path, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertNotIn("random.randint", code, "random.randint must be completely eliminated from feedback_loop.py")
        self.assertNotIn("import random", code, "random module must be completely eliminated from feedback_loop.py")

    def test_patch_4_deterministic_performance_sync(self):
        """simulate_performance_sync가 난수 없이 안정적이고 결정론적인 CRO 메트릭을 반환하는지 검증"""
        fb = FeedbackLoop()
        p1 = fb.simulate_performance_sync("post-test-1", "2026 청년도약계좌", "SUBSIDY", est_pvs=25000000)
        p2 = fb.simulate_performance_sync("post-test-1", "2026 청년도약계좌", "SUBSIDY", est_pvs=25000000)

        # 동일한 PVS 입력 시 완전 일치 (결정론적)
        self.assertEqual(p1["impressions"], p2["impressions"])
        self.assertEqual(p1["clicks"], p2["clicks"])
        self.assertAlmostEqual(p1["ctr_percent"], 4.8, delta=0.1)
        self.assertGreater(p1["adsense_revenue"], 0)
        self.assertGreater(p1["affiliate_revenue"], 0)

    def test_patch_4_instant_indexer_flush_queue(self):
        """InstantIndexer의 flush_fallback_queue 메서드가 정상 작동하는지 검증"""
        indexer = InstantIndexer()
        # Dry-run flush test
        res = indexer.flush_fallback_queue(dry_run=True)
        self.assertIn(res["status"], ["FLUSHED", "EMPTY_QUEUE", "SKIPPED_NO_CREDENTIALS", "NO_LOGS"])

    def test_patch_4_gsc_candidates_extraction_filtering(self):
        """Google Search Console API 모의 데이터로 노출 50회 이상 & 순위 8~20위 필터링 검증"""
        fb = FeedbackLoop()

        # Mock Search Console API Service
        mock_gsc_service = MagicMock()
        mock_query_api = MagicMock()
        mock_gsc_service.searchanalytics.return_value = mock_query_api

        # 4가지 케이스의 모의 검색 데이터
        mock_query_api.query.return_value.execute.return_value = {
            "rows": [
                # 1. 합격 후보: 노출 120회, 순위 12.5위 (조건 완벽 충족)
                {"keys": ["https://blogin365ai.blogspot.com/post1.html", "청년도약계좌 신청"], "impressions": 120, "clicks": 8, "position": 12.5, "ctr": 0.066},
                # 2. 불합격: 노출 30회 (< 50회 미달)
                {"keys": ["https://blogin365ai.blogspot.com/post2.html", "저소득 지원금"], "impressions": 30, "clicks": 2, "position": 10.0, "ctr": 0.066},
                # 3. 불합격: 순위 3.2위 (< 8위 상위권)
                {"keys": ["https://blogin365ai.blogspot.com/post3.html", "알뜰폰 0원"], "impressions": 300, "clicks": 45, "position": 3.2, "ctr": 0.15},
                # 4. 불합격: 순위 25.0위 (> 20위 하위권)
                {"keys": ["https://blogin365ai.blogspot.com/post4.html", "비급여 실손"], "impressions": 80, "clicks": 1, "position": 25.0, "ctr": 0.012}
            ]
        }

        # service_account.json이 있는 것처럼 mocking
        with patch("os.path.exists", return_value=True), \
             patch("engine.analytics.feedback_loop._get_gsc_service", return_value=mock_gsc_service):

            result = fb.sync_gsc_performance_and_candidates()
            self.assertEqual(result["status"], "SUCCESS")
            self.assertEqual(result["total_candidates"], 1)
            self.assertEqual(result["candidates"][0]["page"], "https://blogin365ai.blogspot.com/post1.html")
            self.assertEqual(result["candidates"][0]["impressions"], 120)
            self.assertEqual(result["candidates"][0]["average_position"], 12.5)

            # gsc_rewrite_candidates.json 파일 저장 확인
            self.assertTrue(os.path.exists(fb.candidates_file))
            with open(fb.candidates_file, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
            self.assertEqual(saved_data["total_candidates"], 1)


if __name__ == "__main__":
    unittest.main()
