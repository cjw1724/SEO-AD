# -*- coding: utf-8 -*-
"""
tests/test_advanced_pillars.py
------------------------------
Unit & Integration Tests for the 5 Core Expansion Pillars:
1. Pillar 1: Instant Indexing (Google Indexing API & IndexNow Protocol)
2. Pillar 2: Closed-Loop Feedback & Weight Tuner (GA4/GSC Performance & Demand Matcher Tuning)
3. Pillar 3: Multi-Channel Distribution Engine (Threads, X/Twitter, ManyChat, Webhook)
4. Pillar 4: Self-Healing & Content Refresher (Dead Link Healer & Outdated Post Refresh Detector)
5. Pillar 5: Google Helpful Content (HCU) & Anti-Spam Gate 7
6. Architecture Flow: SequentialMediaPipeline strongly typed 7-phase execution
"""

import os
import sys
import json
import tempfile
import unittest

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.indexing.instant_indexer import InstantIndexer
from engine.analytics.feedback_loop import FeedbackLoop
from engine.distribution.multi_channel_distributor import MultiChannelDistributor
from engine.maintenance.content_refresher import ContentRefresher
from engine.qa.gstack_auditor import GStackAuditor
from engine.matcher.demand_matcher import DemandMatcher
from engine.pipeline.pipeline_flow import SequentialMediaPipeline


class TestAdvancedPillars(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    # --------------------------------------------------------------------------
    # Pillar 1 Tests: Instant Indexing
    # --------------------------------------------------------------------------
    def test_pillar1_instant_indexer(self):
        log_path = os.path.join(self.data_dir, "test_indexing_logs.json")
        indexer = InstantIndexer(log_path=log_path)
        test_url = "https://blogin365ai.blogspot.com/2026/05/youth-account.html"

        # 1. Google Indexing API dry-run submission
        g_res = indexer.submit_google_indexing(test_url, dry_run=True)
        self.assertEqual(g_res["engine"], "google_indexing_api")
        self.assertIn("urlNotificationMetadata", g_res["response"])
        self.assertEqual(g_res["status_code"], 200)

        # 2. IndexNow submission
        in_res = indexer.submit_indexnow([test_url], dry_run=True)
        self.assertEqual(in_res["engine"], "indexnow")
        self.assertEqual(in_res["submitted_count"], 1)
        self.assertEqual(in_res["status"], "SIMULATED_SUCCESS")
        self.assertIn("keyLocation", in_res["payload"])

        # 3. Sitemap Ping
        sm_res = indexer.ping_sitemaps(dry_run=True)
        self.assertEqual(sm_res["engine"], "sitemap_ping")
        self.assertIn("google", sm_res["pings"])
        self.assertIn("bing", sm_res["pings"])

        # 4. Batch All
        all_res = indexer.submit_all(test_url, dry_run=True)
        self.assertEqual(all_res["target_url"], test_url)
        self.assertTrue(os.path.exists(log_path), "Indexing log must be persisted")
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
            self.assertGreaterEqual(len(logs), 1)

    # --------------------------------------------------------------------------
    # Pillar 2 Tests: Closed-Loop Feedback & Weight Tuner
    # --------------------------------------------------------------------------
    def test_pillar2_feedback_loop_and_weight_tuning(self):
        fb = FeedbackLoop(data_dir=self.data_dir)

        # 1. Record Post Performance
        rec = fb.record_post_metric(
            post_id="POST-101",
            keyword="2026 청년도약계좌",
            category="SUBSIDY",
            impressions=2500,
            clicks=150,     # 6.0% CTR (High performer)
            conversions=8,   # 5.3% CVR
            affiliate_rev=96000.0,
            adsense_rev=32400.0,
            est_pvs=100000.0
        )
        self.assertEqual(rec["ctr_percent"], 6.0)
        self.assertEqual(rec["actual_revenue"], 128400.0)
        self.assertGreater(rec["pvs_accuracy_ratio"], 1.0)

        # 2. Record Low Performer Post
        fb.record_post_metric(
            post_id="POST-102",
            keyword="구형 청소기",
            category="TECH",
            impressions=1200,
            clicks=12,      # 1.0% CTR (Low performer)
            conversions=0,
            affiliate_rev=0.0,
            adsense_rev=5000.0,
            est_pvs=80000.0
        )

        # 3. Dynamic Weight Tuning
        tune_result = fb.tune_niche_weights()
        weights = tune_result["tuned_weights"]
        self.assertIn("SUBSIDY", weights)
        self.assertIn("TECH", weights)
        # SUBSIDY should be boosted due to 6% CTR
        self.assertGreater(weights["SUBSIDY"], 1.0)
        # TECH should be discounted due to 1% CTR
        self.assertLess(weights["TECH"], 1.0)

        # 4. Verify DemandMatcher incorporates tuned weight
        matcher = DemandMatcher()
        best = matcher.select_best_topic([{"keyword": "근로장려금 정기신청", "traffic_volume": 60000}])
        self.assertIsNotNone(best)
        self.assertGreater(best["pvs"], 0)

    # --------------------------------------------------------------------------
    # Pillar 3 Tests: Multi-Channel Distribution Engine
    # --------------------------------------------------------------------------
    def test_pillar3_multi_channel_distributor(self):
        dist = MultiChannelDistributor(data_dir=self.data_dir)
        sample_growth = {
            "keyword": "2026 근로장려금",
            "title": "2026 근로장려금 정기신청 실수령액 모의계산 가이드",
            "post_url": "https://blogin365ai.blogspot.com/post-sample.html",
            "category": "SUBSIDY",
            "reel_script": {
                "0-3초_후킹": "[화면: 붉은 경고 뱃지] 근로장려금 신청 안하면 소멸!",
                "3-10초_핵심내용": "30초 만에 확인 가능한 실수령액 계산기",
                "10-15초_행동유도(CTA)": "댓글에 10 남기시면 가이드 발송"
            },
            "sns_caption": "근로장려금 실수령액 총정리...",
            "dm_copy": "요청하신 가이드 링크입니다."
        }

        # 1. Formatting
        payloads = dist.format_channel_payloads(sample_growth)
        self.assertIn("threads", payloads)
        self.assertIn("twitter_x", payloads)
        self.assertIn("manychat_webhook", payloads)
        self.assertIn("kakao_view", payloads)
        self.assertEqual(payloads["manychat_webhook"]["trigger_keyword"], "10")

        # 2. Dispatch in dry-run
        dispatch_res = dist.dispatch_to_channels(sample_growth, dry_run=True)
        self.assertEqual(len(dispatch_res["channels"]), 4)
        for ch, ch_res in dispatch_res["channels"].items():
            self.assertEqual(ch_res["status"], "SIMULATED_SUCCESS")

        # 3. Persistent Queue
        queue = dist.get_queue()
        self.assertGreaterEqual(len(queue), 1)
        self.assertEqual(queue[0]["keyword"], "2026 근로장려금")

    # --------------------------------------------------------------------------
    # Pillar 4 Tests: Self-Healing & Content Refresher
    # --------------------------------------------------------------------------
    def test_pillar4_content_refresher_and_link_health(self):
        refresher = ContentRefresher(data_dir=self.data_dir)

        # 1. Link Extraction & Broken Link Audit
        sample_html = """
        <div>
          <p>공식 안내 가이드: <a href="https://example.com/broken_product">품절된 쿠팡 상품</a></p>
          <p>정상 포털: <a href="https://www.nts.go.kr">국세청 홈택스</a></p>
        </div>
        """
        audit = refresher.audit_html_links(sample_html, dry_run=True)
        self.assertEqual(audit["total_links"], 2)
        self.assertEqual(audit["dead_count"], 1)
        self.assertEqual(audit["alive_count"], 1)

        # 2. Broken Link Healing
        healed_html, count = refresher.heal_broken_links(sample_html, keyword="근로장려금")
        self.assertEqual(count, 1)
        self.assertNotIn("https://example.com/broken_product", healed_html)
        self.assertIn("link.coupang.com", healed_html)

        # 3. Stale Post & Outdated Year Refresh Detection
        dummy_posts = [
            {
                "post_id": "POST-OLD-YEAR",
                "title": "2024 근로장려금 신청 자격 총정리",
                "keyword": "근로장려금",
                "category": "SUBSIDY",
                "timestamp": "2024-05-01T10:00:00"
            },
            {
                "post_id": "POST-FRESH-2026",
                "title": "2026 청년도약계좌 모의계산 가이드",
                "keyword": "청년도약계좌",
                "category": "SUBSIDY",
                "timestamp": "2026-10-10T10:00:00"
            }
        ]
        candidates = refresher.scan_for_refresh_candidates(dummy_posts, max_age_days=30)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["post_id"], "POST-OLD-YEAR")
        self.assertIn("2024", candidates[0]["reasons"][0] + candidates[0]["reasons"][-1])

        brief = refresher.generate_refresh_brief(candidates[0])
        self.assertEqual(brief["action"], "CONTENT_REFRESH")
        self.assertIn("2026", brief["target_keyword"])

    # --------------------------------------------------------------------------
    # Pillar 5 Tests: Google Helpful Content (HCU) & Anti-Spam Gate 7
    # --------------------------------------------------------------------------
    def test_pillar5_google_hcu_and_anti_spam_gate(self):
        auditor = GStackAuditor()

        # 1. High-Quality Journalism with Rich Data (Should Pass HCU)
        good_html = """
        <div class="bento-hero">Bento Key Takeaway</div>
        <div class="saas-calculator">JS Calculator</div>
        <div class="adsense-slot">Ad Slot</div>
        <details><summary>FAQ 1</summary><p>답변</p></details>
        <p>2026년 기준 청년도약계좌 월 최대 지원금은 50만원이며 연 6.0% 우대 금리가 제공됩니다.</p>
        <p>가구 소득 중위 180% 이하 청년 150만명이 대상이며 만기 시 5,000만원의 목돈을 수령합니다.</p>
        <p>실제 자격 요건은 직전 과세기간 총급여 7,500만원 이하로 국세청 홈택스에서 3분 만에 모의 조회할 수 있습니다.</p>
        """ + ("<p>체계적 심층 분석 데이터를 바탕으로 산출된 비교 보고서 내용입니다.</p>" * 30)

        eval_res = auditor.evaluate_hcu_quality("2026 청년도약계좌 모의계산", good_html)
        self.assertTrue(eval_res["passed"])
        self.assertGreaterEqual(eval_res["score"], 70)
        self.assertGreater(eval_res["metrics"]["facts_count"], 4)

        # 2. Hidden Cloaking Text Violation (Spam Attempt)
        spam_html = good_html + '<div style="display:none">청년도약계좌 청년도약계좌 불법키워드도배</div>'
        spam_eval = auditor.evaluate_hcu_quality("2026 청년도약계좌", spam_html)
        self.assertFalse(spam_eval["passed"], "Must fail when hidden text cloaking is detected")
        self.assertIn("스팸 회피/클로킹", spam_eval["errors"][0])

        # Sanitizer removes cloaking style
        sanitized = auditor.sanitize_if_possible(spam_html)
        self.assertNotIn("display:none", sanitized)

        # 3. Excessive Thin Affiliate Ratio Violation (> 15% footprint)
        thin_affiliate_html = (
            '<div class="bento-hero">Hero</div><div class="saas-calculator">Calc</div><div class="adsense-slot">Ad</div><details><summary>FAQ</summary>A</details>'
            + ('<a class="btn-affiliate" href="https://link.coupang.com/a/1234">지금 구매하기 초특가 할인 링크</a>' * 40)
        )
        thin_eval = auditor.evaluate_hcu_quality("과도한 어필리에이트", thin_affiliate_html)
        self.assertFalse(thin_eval["passed"], "Must fail when affiliate footprint dominates page")
        self.assertIn("씬 어필리에이트", thin_eval["errors"][0])

    # --------------------------------------------------------------------------
    # Sequential Pipeline Integration Test (Phase 1 -> 7)
    # --------------------------------------------------------------------------
    def test_sequential_7phase_pipeline(self):
        pipeline = SequentialMediaPipeline()
        summary = pipeline.run_full_cycle(keyword_override="2026 청년도약계좌", dry_run=True)

        self.assertIsNotNone(summary)
        self.assertEqual(summary.status, "SUCCESS")
        self.assertEqual(summary.phase1.keyword, "2026 청년도약계좌")
        self.assertEqual(summary.phase1.tier, "최적")
        self.assertGreater(len(summary.phase2.sections), 0)
        self.assertGreater(summary.phase3.bytes_length, 5000)
        self.assertTrue(summary.phase4.passed)
        self.assertGreaterEqual(summary.phase4.hcu_score, 70)
        self.assertTrue(summary.phase5.success)
        self.assertIn("google_indexing", summary.phase5.indexing_result["results"])
        self.assertIn("threads", summary.phase6.dispatched_channels)
        self.assertGreater(summary.phase7.performance_metric["ctr_percent"], 0.0)


if __name__ == "__main__":
    unittest.main()
