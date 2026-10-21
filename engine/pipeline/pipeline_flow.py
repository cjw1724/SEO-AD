# -*- coding: utf-8 -*-
"""
engine/pipeline/pipeline_flow.py
--------------------------------
Blogin 365 AI Holdings - Strongly Typed Sequential 7-Phase Media Pipeline (v6.0)

Implements the complete end-to-end autonomous architecture with explicit horizontal data flow:
  Phase 1: Trend Discovery & Demand Matcher
    ↓
  Phase 2: Editorial & Research
    ↓
  Phase 3: Visual & CRO Assembly
    ↓
  Phase 4: QA Gatekeeper (GStack & HCU)
    ↓
  Phase 5: Publisher & Instant Indexing (Google Indexing API + IndexNow)
    ↓
  Phase 6: Multi-channel Distribution (Threads, X, ManyChat, Webhook)
    ↓
  Phase 7: Closed-loop Feedback & Refresh (GA4/GSC Sync, Weight Tuning, Link Health)
"""

import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.radar.trend_scout import TrendScout
from engine.matcher.demand_matcher import DemandMatcher
from engine.agents.agency_stack import AgencyStack
from engine.agents.cro_monetizer import assemble_world_class_article
from engine.qa.gstack_auditor import GStackAuditor
from engine.publisher.blogger_gateway import BloggerGateway
from engine.indexing.instant_indexer import InstantIndexer
from engine.growth.viral_hook_maker import ViralHookMaker
from engine.distribution.multi_channel_distributor import MultiChannelDistributor
from engine.analytics.feedback_loop import FeedbackLoop
from engine.maintenance.content_refresher import ContentRefresher
from engine.company_runtime import CompanyLogger
from engine.radar.community_sentiment_scout import CommunitySentimentScout
from engine.matcher.experiential_verifier import ExperientialVerifier
from engine.agents.human_voice_engine import HumanVoiceEngine


# ==============================================================================
# Strongly Typed Pipeline Data Contracts
# ==============================================================================

@dataclass
class Phase1_DiscoveryResult:
    keyword: str
    category: str
    tier: str
    ratio: float
    subs: List[str]
    sub_details: List[Dict[str, Any]]
    pvs_score: float
    cpc: int
    title: str
    traffic_volume: int
    keyword_package: Dict[str, Any]
    niche_name: str
    intent: str
    raw_topic: Dict[str, Any]
    sentiment: Dict[str, Any] = field(default_factory=dict)
    factset: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase2_EditorialResult:
    title: str
    sections: List[Dict[str, Any]]
    faq: List[Dict[str, Any]]
    lead_text: str
    editorial_dict: Dict[str, Any]


@dataclass
class Phase3_AssemblyResult:
    title: str
    html_content: str
    bytes_length: int
    components_present: List[str]


@dataclass
class Phase4_QAResult:
    passed: bool
    hcu_score: int
    gate_results: List[Dict[str, Any]]
    errors: List[str]
    hcu_metrics: Dict[str, Any]
    sanitized: bool
    final_html: str


@dataclass
class Phase5_PublishResult:
    success: bool
    post_id: str
    url: str
    is_dry_run: bool
    indexing_result: Dict[str, Any]


@dataclass
class Phase6_DistributionResult:
    growth_package: Dict[str, Any]
    reel_script: Dict[str, str]
    dispatched_channels: Dict[str, Any]
    queue_batch_id: str


@dataclass
class Phase7_FeedbackResult:
    performance_metric: Dict[str, Any]
    tuned_weights: Dict[str, Any]
    refresh_candidates: List[Dict[str, Any]]
    link_audit_summary: Dict[str, Any]


@dataclass
class PipelineExecutionSummary:
    cycle_id: str
    status: str
    timestamp: str
    execution_time_sec: float
    is_dry_run: bool
    phase1: Phase1_DiscoveryResult
    phase2: Phase2_EditorialResult
    phase3: Phase3_AssemblyResult
    phase4: Phase4_QAResult
    phase5: Phase5_PublishResult
    phase6: Phase6_DistributionResult
    phase7: Phase7_FeedbackResult

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "status": self.status,
            "timestamp": self.timestamp,
            "execution_time_sec": self.execution_time_sec,
            "dry_run": self.is_dry_run,
            "title": self.phase1.title,
            "url": self.phase5.url,
            "post_id": self.phase5.post_id,
            "keyword": self.phase1.keyword,
            "category": self.phase1.category,
            "tier": self.phase1.tier,
            "ratio": self.phase1.ratio,
            "subs": self.phase1.subs,
            "sub_details": self.phase1.sub_details,
            "keyword_package": self.phase1.keyword_package,
            "pvs": self.phase1.pvs_score,
            "pvs_score": self.phase1.pvs_score,
            "cpc": self.phase1.cpc,
            "growth_package": self.phase6.growth_package,
            "indexing": self.phase5.indexing_result,
            "distribution": self.phase6.dispatched_channels,
            "feedback": {
                "performance": self.phase7.performance_metric,
                "weights": self.phase7.tuned_weights
            },
            "hcu_score": self.phase4.hcu_score,
            "hcu_metrics": self.phase4.hcu_metrics,
            "sentiment": self.phase1.sentiment,
            "factset": self.phase1.factset,
            "trick_b": {
                "present": "b365-search-nav" in self.phase3.html_content,
                "has_pills": "b365-search-pill" in self.phase3.html_content,
                "mode": "GOOGLE_CSE" if os.getenv("GOOGLE_CSE_CX") else "BLOG_FALLBACK"
            }
        }


# ==============================================================================
# Sequential Media Pipeline Engine
# ==============================================================================

class SequentialMediaPipeline:
    """
    Coordinates the 7 distinct phases of Blogin 365 AI Holdings in a strongly-typed,
    unbreakable chain.
    """
    def __init__(self, logger: Optional[CompanyLogger] = None):
        self.scout = TrendScout()
        self.feedback = FeedbackLoop()
        self.matcher = DemandMatcher(feedback_loop=self.feedback)
        self.community_scout = CommunitySentimentScout()
        self.exp_verifier = ExperientialVerifier()
        self.agency = AgencyStack()
        self.human_voice = HumanVoiceEngine()
        self.auditor = GStackAuditor()
        self.gateway = BloggerGateway()
        self.indexer = InstantIndexer()
        self.hook_maker = ViralHookMaker()
        self.distributor = MultiChannelDistributor()
        self.refresher = ContentRefresher()
        self.logger = logger or CompanyLogger()

    # --------------------------------------------------------------------------
    # Phase 1: Trend Discovery & Demand Matcher
    # --------------------------------------------------------------------------
    def execute_phase1_discovery(self, keyword_override: Optional[str] = None) -> Phase1_DiscoveryResult:
        if keyword_override:
            trends = [{"keyword": keyword_override, "traffic_volume": 50000, "source": "keyword_override"}]
            expanded_subs = self.scout.expand_autocomplete(keyword_override, limit=6)
        else:
            trends = self.scout.fetch_live_trends(limit=10)
            top_kw = trends[0]["keyword"] if trends else "2026 청년도약계좌"
            expanded_subs = self.scout.expand_autocomplete(top_kw, limit=6)

        matched_topic = self.matcher.select_best_topic(trends, sub_candidates=expanded_subs)
        title = matched_topic.get("title", f"{matched_topic['keyword']} 실측 분석 및 모의 계산 가이드")

        # Humanization Phase 1: Community Sentiment & Experiential Factset
        sentiment_data = self.community_scout.scout_community_sentiment(
            matched_topic["keyword"], category=matched_topic["category"]
        )
        factset_data = self.exp_verifier.build_experiential_factset(
            matched_topic["keyword"], category=matched_topic["category"]
        )
        matched_topic["sentiment"] = sentiment_data
        matched_topic["factset"] = factset_data

        return Phase1_DiscoveryResult(
            keyword=matched_topic["keyword"],
            category=matched_topic["category"],
            tier=matched_topic.get("tier", "최적"),
            ratio=matched_topic.get("ratio", 1.0),
            subs=matched_topic.get("subs", []),
            sub_details=matched_topic.get("sub_details", []),
            pvs_score=matched_topic.get("pvs", 10000.0),
            cpc=matched_topic.get("cpc", 2500),
            title=title,
            traffic_volume=matched_topic.get("traffic_volume", 35000),
            keyword_package=matched_topic.get("keyword_package", {}),
            niche_name=matched_topic.get("niche_name", "스마트 라이프"),
            intent=matched_topic.get("intent", "COMMERCIAL"),
            raw_topic=matched_topic,
            sentiment=sentiment_data,
            factset=factset_data
        )

    # --------------------------------------------------------------------------
    # Phase 2: Editorial & Research
    # --------------------------------------------------------------------------
    def execute_phase2_editorial(self, phase1: Phase1_DiscoveryResult) -> Phase2_EditorialResult:
        try:
            editorial = self.agency.write_editorial_content(phase1.raw_topic)
        except Exception:
            editorial = self.agency._build_deterministic_content(phase1.raw_topic)

        if not editorial or "sections" not in editorial:
            editorial = self.agency._build_deterministic_content(phase1.raw_topic)

        # Humanization Phase 3: Injects Human Rhythm, Burstiness, Anecdotes, Quotes, and Conversational Subheaders
        editorial = self.human_voice.humanize_editorial_content(
            editorial_data=editorial,
            sentiment_data=phase1.sentiment,
            factset_data=phase1.factset,
            sub_keywords=phase1.subs
        )

        lead_text = ""
        sections = editorial.get("sections", [])
        if sections:
            lead_text = sections[0].get("lead", "")

        return Phase2_EditorialResult(
            title=phase1.title,
            sections=sections,
            faq=editorial.get("faq", []),
            lead_text=lead_text,
            editorial_dict=editorial
        )

    # --------------------------------------------------------------------------
    # Phase 3: Visual & CRO Assembly
    # --------------------------------------------------------------------------
    def execute_phase3_assembly(
        self,
        phase1: Phase1_DiscoveryResult,
        phase2: Phase2_EditorialResult
    ) -> Phase3_AssemblyResult:
        assembled_html = assemble_world_class_article(phase1.raw_topic, phase2.editorial_dict)
        components = ["bento-hero", "saas-calculator", "adsense-slots", "faq-accordion"]
        if "b365-hero-thumbnail" in assembled_html:
            components.append("hero-thumbnail")
        if "b365-search-nav" in assembled_html:
            components.append("b365-search-nav")

        return Phase3_AssemblyResult(
            title=phase1.title,
            html_content=assembled_html,
            bytes_length=len(assembled_html),
            components_present=components
        )

    # --------------------------------------------------------------------------
    # Phase 4: QA Gatekeeper (GStack & HCU Gate)
    # --------------------------------------------------------------------------
    def execute_phase4_qa(
        self,
        phase1: Phase1_DiscoveryResult,
        phase3: Phase3_AssemblyResult
    ) -> Phase4_QAResult:
        # Pre-audit link healing: ensure outbound links are evergreen
        healed_input_html, healed_links_count = self.refresher.heal_broken_links(
            phase3.html_content, keyword=phase1.keyword, dry_run=True
        )

        audit_res = self.auditor.audit_post(
            phase3.title,
            healed_input_html,
            keyword_package=phase1.keyword_package
        )

        sanitized = healed_links_count > 0
        final_html = healed_input_html

        if not audit_res["passed"]:
            final_html = self.auditor.sanitize_if_possible(healed_input_html, main_keyword=phase1.keyword)
            re_audit = self.auditor.audit_post(
                phase3.title,
                final_html,
                keyword_package=phase1.keyword_package
            )
            if not re_audit["passed"]:
                raise RuntimeError(f"치명적 QA 검수 실패로 파이프라인이 중단되었습니다: {re_audit['errors']}")
            audit_res = re_audit
            sanitized = True

        return Phase4_QAResult(
            passed=audit_res["passed"],
            hcu_score=audit_res.get("hcu_score", 85),
            gate_results=audit_res.get("gate_results", []),
            errors=audit_res.get("errors", []),
            hcu_metrics=audit_res.get("hcu_metrics", {}),
            sanitized=sanitized,
            final_html=final_html
        )

    # --------------------------------------------------------------------------
    # Phase 5: Publisher & Instant Indexing (Pillar 1)
    # --------------------------------------------------------------------------
    def execute_phase5_publish_and_index(
        self,
        phase1: Phase1_DiscoveryResult,
        phase4: Phase4_QAResult,
        dry_run: bool = False
    ) -> Phase5_PublishResult:
        raw_labels = [phase1.keyword] + phase1.subs + ["정보", phase1.category, "모의계산", "Blogin365AI"]
        seen_labels = set()
        labels = [l for l in raw_labels if l and not (l in seen_labels or seen_labels.add(l))]

        if dry_run:
            post_id = f"dry-run-{int(time.time())}"
            post_url = f"https://blogin365ai.blogspot.com/preview-dry-run-{int(time.time())}.html"
            pub_success = True
        else:
            pub_res = self.gateway.publish(
                phase1.title,
                phase4.final_html,
                labels=labels,
                is_draft=False,
                category=phase1.category
            )
            if not pub_res["success"]:
                raise RuntimeError(f"Blogger 발행 오류: {pub_res.get('error')}")
            post_id = pub_res.get("id", "pub-id")
            post_url = pub_res.get("url", "https://blogin365ai.blogspot.com")
            pub_success = True

        # Instant Indexing Protocol (Pillar 1: Google Indexing API + IndexNow + Sitemap Ping)
        indexing_res = self.indexer.submit_all(post_url, dry_run=dry_run)

        return Phase5_PublishResult(
            success=pub_success,
            post_id=post_id,
            url=post_url,
            is_dry_run=dry_run,
            indexing_result=indexing_res
        )

    # --------------------------------------------------------------------------
    # Phase 6: Multi-channel Distribution (Pillar 3)
    # --------------------------------------------------------------------------
    def execute_phase6_distribution(
        self,
        phase1: Phase1_DiscoveryResult,
        phase5: Phase5_PublishResult,
        dry_run: bool = False
    ) -> Phase6_DistributionResult:
        # Generate Viral Hooks (15s Reel & ManyChat DM)
        growth_pkg = self.hook_maker.generate_hooks(phase1.raw_topic, phase5.url)

        # Dispatch across Threads, Twitter/X, ManyChat Webhooks, Kakao View
        dist_res = self.distributor.dispatch_to_channels(growth_pkg, dry_run=dry_run)

        return Phase6_DistributionResult(
            growth_package=growth_pkg,
            reel_script=growth_pkg.get("reel_script", {}),
            dispatched_channels=dist_res.get("channels", {}),
            queue_batch_id=dist_res.get("batch_id", "")
        )

    # --------------------------------------------------------------------------
    # Phase 7: Closed-loop Feedback & Maintenance (Pillar 2 & 4)
    # --------------------------------------------------------------------------
    def execute_phase7_feedback_and_maintenance(
        self,
        phase1: Phase1_DiscoveryResult,
        phase4: Phase4_QAResult,
        phase5: Phase5_PublishResult,
        dry_run: bool = False
    ) -> Phase7_FeedbackResult:
        # 1. Closed-loop Feedback & Metric Tracking
        perf_metric = self.feedback.simulate_performance_sync(
            post_id=phase5.post_id,
            keyword=phase1.keyword,
            category=phase1.category,
            est_pvs=phase1.pvs_score
        )
        tuned_weights = self.feedback.tune_niche_weights()
        self.feedback.sync_gsc_performance_and_candidates()

        # 2. Content Refresher & Link Health Audit & Healing
        link_audit = self.refresher.audit_html_links(phase4.final_html, dry_run=dry_run)
        if link_audit.get("has_dead_links"):
            _, healed_count = self.refresher.heal_broken_links(phase4.final_html, keyword=phase1.keyword, dry_run=dry_run)
            link_audit["healed_count"] = healed_count

        refresh_candidates = self.refresher.scan_for_refresh_candidates(max_age_days=30)

        return Phase7_FeedbackResult(
            performance_metric=perf_metric,
            tuned_weights=tuned_weights,
            refresh_candidates=refresh_candidates,
            link_audit_summary=link_audit
        )

    # --------------------------------------------------------------------------
    # Full Cycle Orchestration
    # --------------------------------------------------------------------------
    def run_full_cycle(
        self,
        keyword_override: Optional[str] = None,
        dry_run: bool = False
    ) -> PipelineExecutionSummary:
        start_time = time.time()
        cycle_id = f"CYC-{int(start_time)}"

        # Phase 1
        p1 = self.execute_phase1_discovery(keyword_override=keyword_override)
        # Phase 2
        p2 = self.execute_phase2_editorial(p1)
        # Phase 3
        p3 = self.execute_phase3_assembly(p1, p2)
        # Phase 4
        p4 = self.execute_phase4_qa(p1, p3)
        # Phase 5
        p5 = self.execute_phase5_publish_and_index(p1, p4, dry_run=dry_run)
        # Phase 6
        p6 = self.execute_phase6_distribution(p1, p5, dry_run=dry_run)
        # Phase 7
        p7 = self.execute_phase7_feedback_and_maintenance(p1, p4, p5, dry_run=dry_run)

        elapsed = round(time.time() - start_time, 2)
        status = "HEALED" if p4.sanitized else "SUCCESS"

        summary = PipelineExecutionSummary(
            cycle_id=cycle_id,
            status=status,
            timestamp=datetime.now().isoformat(),
            execution_time_sec=elapsed,
            is_dry_run=dry_run,
            phase1=p1,
            phase2=p2,
            phase3=p3,
            phase4=p4,
            phase5=p5,
            phase6=p6,
            phase7=p7
        )

        # Record to Company Logger
        cycle_log = summary.to_dict()
        self.logger.record_cycle(cycle_log)

        return summary
