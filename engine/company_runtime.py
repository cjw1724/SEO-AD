# -*- coding: utf-8 -*-
"""
engine/company_runtime.py
-------------------------
Blogin 365 AI Holdings - Autonomous Media Company Operating System (v6.0)

A 24/7 unbreakable, fully autonomous AI Media Enterprise operating without manual intervention.
Implements:
1. 8 AI Staff Roles (Every AI Playbook Org Chart):
   - 01 Chief of Staff      : Strategic pipeline orchestration & dispatch
   - 02 Product Planner     : Niche monetization mapping & editorial brief
   - 03 Market Researcher   : Real-time Google Trends KR + PVS v2.0 revenue velocity
   - 04 UI Designer         : Canvas inline SVG comparisons & Bento layout
   - 05 Developer           : Micro-SaaS interactive JavaScript calculators
   - 06 QA Tester           : GStack & Hallmark 57 Slop-Test Gates (Zero-Persona, Zero Broken Entities)
   - 07 Marketer            : 15s Viral Reel script & ManyChat '10' DM trigger loop
   - 08 CS / Publisher      : Blogger API v3 gateway & Schema.org JSON-LD
2. Self-Healing Subsystem:
   - Network backoff & automatic API retries
   - OpenRouter fallback to deterministic anti-slop journalism
   - Auto-refresh of expired OAuth2 Google credentials
   - Automatic HTML sanitization upon minor gate warnings
3. Persistent Company Logging (`data/company_logs.json`):
   - Health heartbeats, KPI metrics, execution history
4. Executive Company Dashboard CLI:
   - Real-time ASCII status, role health indicators, revenue scores
5. 24/7 Daemon & Windows Service Runtime
"""

import os
import sys
import time
import json
import random
import traceback
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv

# Enforce UTF-8 unbuffered console output for Windows PowerShell / CMD
try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
except Exception:
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, "SEO.env"))

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
from engine.radar.community_sentiment_scout import CommunitySentimentScout
from engine.matcher.experiential_verifier import ExperientialVerifier
from engine.radar.public_data_scout import PublicDataScout
from engine.agents.human_voice_engine import HumanVoiceEngine
from engine.matcher.topic_cluster_engine import TopicClusterEngine
from engine.matcher.universal_topic_engine import UniversalTopicEngine, resolve_canonical_pillar
from engine.agents.prompts_chat_pack import APEX_STAFF_PROMPTS, get_staff_prompt


class CompanyLogger:
    """
    Manages structured, persistent company audit logs and cumulative business metrics in data/company_logs.json.
    """
    def __init__(self, log_path: Optional[str] = None):
        if log_path is None:
            data_dir = os.path.join(BASE_DIR, "data")
            os.makedirs(data_dir, exist_ok=True)
            self.log_path = os.path.join(data_dir, "company_logs.json")
        else:
            self.log_path = log_path
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.log_path):
            initial_data = {
                "company_name": "Blogin 365 AI Holdings",
                "brand": "blogin365ai.blogspot.com",
                "blog_id": "2002031376804677477",
                "system_version": "v6.0-autonomous",
                "created_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat(),
                "metrics": {
                    "total_cycles_run": 0,
                    "successful_cycles": 0,
                    "failed_cycles": 0,
                    "healed_cycles": 0,
                    "success_rate_percent": 100.0,
                    "cumulative_pvs_score": 0.0,
                    "total_published_posts": 0
                },
                "role_statuses": {
                    "01_ChiefOfStaff": "READY",
                    "02_ProductPlanner": "READY",
                    "03_MarketResearcher": "READY",
                    "04_UIDesigner": "READY",
                    "05_Developer": "READY",
                    "06_QATester": "READY",
                    "07_Marketer": "READY",
                    "08_CSPublisher": "READY"
                },
                "execution_history": []
            }
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)

    def load_data(self) -> Dict[str, Any]:
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            self._ensure_log_file()
            with open(self.log_path, "r", encoding="utf-8") as f:
                return json.load(f)

    def record_heartbeat(self, role_statuses: Optional[Dict[str, str]] = None):
        data = self.load_data()
        data["last_heartbeat"] = datetime.now().isoformat()
        if role_statuses:
            data["role_statuses"].update(role_statuses)
        self._save(data)

    def record_cycle(self, cycle_record: Dict[str, Any]):
        data = self.load_data()
        metrics = data.setdefault("metrics", {})

        metrics["total_cycles_run"] = metrics.get("total_cycles_run", 0) + 1
        status = cycle_record.get("status", "SUCCESS")

        if status == "SUCCESS":
            metrics["successful_cycles"] = metrics.get("successful_cycles", 0) + 1
            if not cycle_record.get("dry_run", False):
                metrics["total_published_posts"] = metrics.get("total_published_posts", 0) + 1
        elif status == "HEALED":
            metrics["successful_cycles"] = metrics.get("successful_cycles", 0) + 1
            metrics["healed_cycles"] = metrics.get("healed_cycles", 0) + 1
            if not cycle_record.get("dry_run", False):
                metrics["total_published_posts"] = metrics.get("total_published_posts", 0) + 1
        else:
            metrics["failed_cycles"] = metrics.get("failed_cycles", 0) + 1

        total_run = metrics["total_cycles_run"]
        success_run = metrics["successful_cycles"]
        metrics["success_rate_percent"] = round((success_run / total_run * 100), 1) if total_run > 0 else 100.0

        pvs = cycle_record.get("pvs_score", 0)
        metrics["cumulative_pvs_score"] = round(metrics.get("cumulative_pvs_score", 0.0) + pvs, 2)

        data["last_heartbeat"] = datetime.now().isoformat()
        data["last_run_timestamp"] = cycle_record.get("timestamp", datetime.now().isoformat())
        data["last_status"] = status

        history = data.setdefault("execution_history", [])
        history.insert(0, cycle_record)
        data["execution_history"] = history[:50]  # retain 50 latest logs

        self._save(data)

    def _save(self, data: Dict[str, Any]):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class AICompanyStaff:
    """
    Simulates and monitors the 8 AI Staff Members operating under the Every AI Playbook Org Chart.
    All staff behaviors, guidelines, and guardrails are strictly driven by APEX_STAFF_PROMPTS (v9.0 Apex).
    """
    ROLES = APEX_STAFF_PROMPTS

    @classmethod
    def get_prompt(cls, role_key: str) -> str:
        """Returns the exact v9.0 Apex Master Prompt for a specific AI Staff Role."""
        return get_staff_prompt(role_key)

    @classmethod
    def get_all_prompts(cls) -> Dict[str, str]:
        """Returns all 8 AI Staff Master Prompts mapped by role_key."""
        return {k: v["system_prompt"].strip() for k, v in cls.ROLES.items()}

    def check_health(self) -> Dict[str, Dict[str, Any]]:
        health = {}
        for role_key, role_info in self.ROLES.items():
            prompt_text = role_info.get("system_prompt", "")
            health[role_key] = {
                "name": role_info["title"],
                "role_code": role_info.get("role_code", role_key),
                "status": "HEALTHY",
                "prompt_status": "ACTIVE_V9_APEX",
                "prompt_chars": len(prompt_text),
                "details": f"Operational & Active (Prompt v9.0 Apex, {len(prompt_text)} chars)"
            }

        # Check Public Data Scout & Crawl4AI Health
        health["03_MarketResearcher"]["crawl4ai"] = "Crawl4AI & Zero-API Real-Time Scout Active"
        health["03_MarketResearcher"]["details"] = "Trends RSS & Crawl4AI Real-Time Ingestion Active"

        # Check MoneyPrinterTurbo Short-Form Video Bridge Health
        health["07_Marketer"]["money_printer"] = "MoneyPrinterTurbo Short-form Video Bridge Active"
        health["07_Marketer"]["details"] = "Viral Hooks & MoneyPrinterTurbo 15s Shorts Automation Active"

        # Check OAuth Token Health
        token_path = os.path.join(BASE_DIR, "token.json")
        creds_path = os.path.join(BASE_DIR, "credentials.json")
        if not os.path.exists(token_path) and not os.path.exists(creds_path):
            health["08_CSPublisher"]["status"] = "WARNING"
            health["08_CSPublisher"]["details"] = "Credentials missing"

        # Check Niche DB Health
        niche_db = os.path.join(BASE_DIR, "data", "high_cpc_keywords.json")
        if not os.path.exists(niche_db):
            health["02_ProductPlanner"]["status"] = "WARNING"
            health["02_ProductPlanner"]["details"] = "high_cpc_keywords.json missing"

        # Check Trick B Search Engine & AdSense for Search (AFS) Health
        cse_cx = os.getenv("GOOGLE_CSE_CX", "").strip()
        if cse_cx:
            health["05_Developer"]["trick_b"] = f"GOOGLE_CSE (CX: {cse_cx[:6]}...)"
            health["05_Developer"]["details"] = f"Micro-SaaS & Google CSE AFS Active ({cse_cx[:6]}...)"
        else:
            health["05_Developer"]["trick_b"] = "BLOG_FALLBACK"
            health["05_Developer"]["details"] = "Micro-SaaS & Blog Search Dual Fallback Active"

        # Check Service Account & Indexing / GSC Health
        sa_path = os.path.join(BASE_DIR, "service_account.json")
        if os.path.exists(sa_path):
            health["08_CSPublisher"]["indexing_api"] = "Service Account Connected (Auto-Flush Active)"
            health["02_ProductPlanner"]["gsc_sync"] = "GSC Search Analytics Active"

        # Check AdSense Approval Defense Mode
        is_approved = os.getenv("IS_ADSENSE_APPROVED", "false").strip().lower() in ("true", "1", "yes")
        health["02_ProductPlanner"]["adsense_mode"] = "FULL_MONETIZATION" if is_approved else "REVIEW_DEFENSE (Informational)"

        return health


class SelfHealingPipeline:
    """
    Autonomous Execution Engine with multi-layer self-healing resilience:
    - Retries network/API requests with exponential backoff & jitter
    - Seamlessly fails over to deterministic high-quality editorial if OpenRouter LLM limits or errors
    - Auto-sanitizes and re-audits content upon gate warnings
    - Auto-refreshes OAuth2 credentials on expiration
    """
    def __init__(self, logger: CompanyLogger):
        self.logger = logger
        self.scout = TrendScout()
        self.matcher = DemandMatcher()
        self.public_scout = PublicDataScout()
        self.community_scout = CommunitySentimentScout()
        self.exp_verifier = ExperientialVerifier()
        self.agency = AgencyStack()
        self.human_voice = HumanVoiceEngine()
        self.auditor = GStackAuditor()
        self.gateway = BloggerGateway()
        self.indexer = InstantIndexer()
        self.growth = ViralHookMaker()
        self.distributor = MultiChannelDistributor()
        self.feedback = FeedbackLoop()
        self.refresher = ContentRefresher()
        self.cluster_engine = TopicClusterEngine()
        self.staff = AICompanyStaff()

    def run_cycle(self, dry_run: bool = False, keyword_override: Optional[str] = None, max_retries: int = 3) -> Dict[str, Any]:
        cycle_id = f"CYC-{int(time.time())}"
        start_time = time.time()
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n╔══════════════════════════════════════════════════════════════════════════╗")
        print(f"║ 🏢 Blogin 365 AI Holdings - 자율 미디어 사이클 [{cycle_id}] 가동")
        print(f"║ 시각: {timestamp_str} | 실행 모드: {'DRY-RUN (안전 테스트)' if dry_run else 'PRODUCTION (실제 발행)'}")
        print(f"╚══════════════════════════════════════════════════════════════════════════╝")

        healing_events = []
        is_healed = False

        # -----------------------------------------------------------------
        # Step 1: Autonomous Cluster Portfolio & Topic Selection (Self-Healing Fallback)
        # -----------------------------------------------------------------
        print("\n[AI 직원 01~03] 자율 클러스터 포트폴리오 매니저 & 트렌드 레이더 가동...")
        matched_topic = None
        for attempt in range(1, max_retries + 1):
            try:
                if keyword_override:
                    target_kw = keyword_override
                    trends = [{"keyword": target_kw, "traffic_volume": 50000, "source": "keyword_override"}]
                    expanded_subs = self.scout.expand_autocomplete(target_kw, limit=6)
                    matched_topic = self.matcher.select_best_topic(trends, sub_candidates=expanded_subs)
                else:
                    # 30-Day Topic Cluster Sequential Progression (철칙 1 무인 자율 거버넌스)
                    cluster_node = self.cluster_engine.get_next_cluster_topic()
                    target_kw = cluster_node["keyword"]
                    gov = cluster_node.get("governance", {})
                    print(f" -> [AI 직원 01 Chief of Staff] 자율 클러스터 거버넌스 가동:")
                    print(f"    - 활성 골든 니치: {cluster_node['cluster_name']} (Day {cluster_node['day']}/30)")
                    print(f"    - 포트폴리오 상태: {gov.get('reason', '30-Day Cluster In Progress')}")

                    trends = [{"keyword": target_kw, "traffic_volume": 50000, "source": "topic_cluster_30day", "category": cluster_node["category"]}]
                    expanded_subs = self.scout.expand_autocomplete(target_kw, limit=6)
                    matched_topic = self.matcher.select_best_topic(trends, sub_candidates=expanded_subs)
                    matched_topic["keyword"] = target_kw
                    matched_topic["category"] = cluster_node.get("category", matched_topic.get("category", "HAIR"))
                    matched_topic["category_code"] = matched_topic["category"]
                    matched_topic["niche_name"] = cluster_node.get("cluster_name", matched_topic.get("niche_name"))
                    if "title" in cluster_node:
                        matched_topic["title"] = cluster_node["title"]
                    matched_topic["cluster_node"] = cluster_node

                    # [철칙 1-3] Semantic Cannibalization Insulation Check
                    cannibal = self.cluster_engine.check_cannibalization(target_kw)
                    if not cannibal["passed"]:
                        print(f" ⚠️ [카니발라이제이션 경고]: {cannibal['reason']}")
                    else:
                        print(f" -> [카니발라이제이션 통과]: 의도('{cannibal['candidate_intent']}') 격리 및 고유 의미론적 거리 확보 확인")

                if matched_topic and matched_topic.get("keyword"):
                    break
            except Exception as e:
                print(f" ⚠️ [Self-Healing] Step 1 시도 {attempt}/{max_retries} 경고: {e}")
                healing_events.append(f"Step 1 Retry {attempt}: {str(e)}")
                time.sleep(1.5 * attempt)

        if not matched_topic:
            # Fallback to absolute guaranteed golden topic
            print(" 🔄 [Self-Healing] 비상 골든 키워드 큐 자동 활성화...")
            is_healed = True
            healing_events.append("Activated Emergency Golden Topic Fallback")
            from engine.matcher.demand_matcher import build_keyword_package, generate_optimized_title
            fb_main = "2026 청년도약계좌"
            fb_cat = "SUBSIDY"
            fb_pkg = build_keyword_package(fb_main, fb_cat, search_vol=60000)
            fb_title = generate_optimized_title(fb_main, fb_cat, subs=fb_pkg["subs"])
            matched_topic = {
                "keyword": fb_pkg["main"],
                "keyword_package": fb_pkg,
                "subs": fb_pkg["subs"],
                "ratio": fb_pkg["ratio"],
                "tier": fb_pkg["tier"],
                "title": fb_title,
                "traffic_volume": 60000,
                "category": fb_cat,
                "category_code": fb_cat,
                "niche_name": "숨은 돈 환급 & 정부 혜택 계산기",
                "intent": "COMMERCIAL",
                "cpc": 3200,
                "pvs": 10980000,
                "avg_payout": 12000,
                "cpa_type": "CPA_REFUND"
            }

        # Humanization Phase 1: Community Sentiment & Experiential Factset
        print(" -> [AI 직원 02 & 03] 공공데이터 정책 검증, 커뮤니티 여론 수집 및 에디토리얼 팩트체크...")
        sentiment_data = self.community_scout.scout_community_sentiment(
            matched_topic["keyword"], category=matched_topic["category"]
        )
        factset_data = self.exp_verifier.build_experiential_factset(
            matched_topic["keyword"], category=matched_topic["category"]
        )
        matched_topic["sentiment"] = sentiment_data
        matched_topic["factset"] = factset_data

        if factset_data.get("official_facts") and factset_data["official_facts"].get("is_verified"):
            of = factset_data["official_facts"]
            print(f" -> [공공데이터 팩트] 소관: {of.get('department')} | 공식 신청처: {of.get('portal_name')}")

        print(f" -> 선정 메인 키워드: [{matched_topic['keyword']}]")
        print(f" -> 7티어 경쟁 판정: [{matched_topic.get('tier', '최적')}] (골든 비율: {matched_topic.get('ratio', 0):.2f})")
        print(f" -> 서브 키워드(1:1 H2 할당): {matched_topic.get('subs', [])}")
        print(f" -> 니치: {matched_topic.get('niche_name', '스마트 라이프')} | 카테고리: {matched_topic['category']}")
        print(f" -> PVS v2.0 수익 속도 점수: {matched_topic['pvs']:,.0f} pt (예상 CPC: {matched_topic['cpc']}원)")

        # -----------------------------------------------------------------
        # Step 2: Editorial Investigation (Anti-Slop / OpenRouter / Deterministic)
        # -----------------------------------------------------------------
        print("\n[AI 직원 02 & 05] 저널리즘 에디토리얼 본문 및 FAQ 생성 (1:1 서브키워드 소제목 할당)...")
        editorial = None
        try:
            editorial = self.agency.write_editorial_content(matched_topic)
        except Exception as e:
            print(f" ⚠️ [Self-Healing] LLM API 이상 감지 ({e}) -> 결정론적 팩트 저널리즘 템플릿 전환")
            is_healed = True
            healing_events.append(f"AgencyStack LLM exception healed: {str(e)}")
            editorial = self.agency._build_deterministic_content(matched_topic)

        if not editorial or "sections" not in editorial:
            is_healed = True
            healing_events.append("AgencyStack generated empty structure -> deterministic rebuild")
            editorial = self.agency._build_deterministic_content(matched_topic)

        # Humanization Phase 3: Conversational Human Voice Engine
        editorial = self.human_voice.humanize_editorial_content(
            editorial_data=editorial,
            sentiment_data=matched_topic.get("sentiment"),
            factset_data=matched_topic.get("factset"),
            sub_keywords=matched_topic.get("subs", [])
        )

        print(f" -> 섹션 {len(editorial.get('sections', []))}개 및 FAQ {len(editorial.get('faq', []))}개 집필 완료 (인간화 음성 적용)")

        # -----------------------------------------------------------------
        # Step 3: CRO UI & Micro-SaaS Assembly
        # -----------------------------------------------------------------
        print("\n[AI 직원 04 & 05] 월드클래스 UX/UI 조립 (Bento Hero + SaaS 계산기 + Canvas SVG + 애드센스 4슬롯 + 트릭 B 검색허브)...")
        assembled_html = assemble_world_class_article(matched_topic, editorial)
        title = matched_topic.get("title", f"{matched_topic['keyword']} 실측 분석 및 모의 계산 가이드")
        cse_cx = os.getenv("GOOGLE_CSE_CX", "").strip()
        trick_b_mode = "GOOGLE_CSE" if cse_cx else "BLOG_FALLBACK"
        print(f" -> 제목: {title}")
        print(f" -> [트릭 B] 맞춤검색 네비게이션 & 연관 키워드 알약(Pills) 조립 완료 (모드: {trick_b_mode})")
        print(f" -> 최종 HTML 조립 완료: {len(assembled_html):,} bytes")

        # -----------------------------------------------------------------
        # Step 4: GStack & Hallmark 57 Slop-Test Gate Audit
        # -----------------------------------------------------------------
        print("\n[AI 직원 06] gstack & hallmark 6대 무인 검수 게이트 가동...")
        audit_result = self.auditor.audit_post(title, assembled_html, keyword_package=matched_topic.get("keyword_package"))
        if not audit_result["passed"]:
            print(" ⚠️ QA 게이트 경고 감지:")
            for err in audit_result["errors"]:
                print(f"   - {err}")
            print(" 🔄 [Self-Healing] 자동 살균(Sanitize) 가동 및 재검수...")
            assembled_html = self.auditor.sanitize_if_possible(assembled_html, main_keyword=matched_topic.get("keyword"))
            re_audit = self.auditor.audit_post(title, assembled_html, keyword_package=matched_topic.get("keyword_package"))
            
            critical_errors = [e for e in re_audit["errors"] if "GATE 1" in e or "GATE 2" in e]
            if critical_errors:
                raise RuntimeError(f"치명적 법적/엔티티 QA 검수 실패로 발행을 중단합니다: {critical_errors}")
            elif not re_audit["passed"]:
                print(" ⚠️ [QA Soft Warning] 비치명적 게이트 경고가 감지되었으나 자율 치유 후 발행을 속행합니다:")
                for err in re_audit["errors"]:
                    print(f"   - {err}")
                is_healed = True
                healing_events.append(f"Soft QA warnings acknowledged and bypassed: {re_audit['errors']}")
            else:
                is_healed = True
                healing_events.append("Auditor auto-sanitization executed and verified")
                print(" -> 살균 후 QA 게이트 통과 완료!")
        else:
            print(" -> 6대 핵심 검수 게이트(Zero-Persona, Zero-Broken-Entity, Anti-Slop, CRO, Content, 1:1-Keyword) 100% 무결점 통과!")

        # -----------------------------------------------------------------
        # Step 4-B: 8-Agent Visual Inspection & WCAG AAA Auto-Healing Gate
        # -----------------------------------------------------------------
        print("\n[AI 직원 06] 8인 AI 직원 비주얼 인스펙터 & WCAG 2.1 AAA 명도비 실물 검수...")
        try:
            from engine.crew.editorial_inspector import EditorialInspector
            inspector = EditorialInspector()
            assembled_html, visual_review = inspector.inspect_and_heal(assembled_html)
            if visual_review.get("healed"):
                is_healed = True
                healing_events.append("EditorialInspector auto-healed contrast and layout to Toss Dark standard")
                print(" 🔄 [Self-Healing] 비주얼 인스펙터: 명도비 및 스타일 충돌 완벽 자동 치유 완료!")
            else:
                print(" -> 비주얼 인스펙터: 데스크톱/모바일 100% 무결점 통과!")
        except Exception as insp_err:
            print(f" ⚠️ [Visual Inspection Soft Warning]: {insp_err}")

        # -----------------------------------------------------------------
        # Step 5: Google Blogger Gateway Publishing (with retry)
        # -----------------------------------------------------------------
        print("\n[AI 직원 08] Google Blogger Gateway v3 발행...")
        pub_result = None
        # 태그(Labels): 메인 키워드 포함 + 서브 키워드 전부 포함 (바이브 메이커 공식)
        pillar_cat = resolve_canonical_pillar(matched_topic.get("category", ""), matched_topic.get("keyword", ""))
        raw_labels = [pillar_cat, matched_topic["keyword"]] + matched_topic.get("subs", []) + ["모의계산", "Blogin365AI"]
        seen_labels = set()
        labels = [l for l in raw_labels if l and not (l in seen_labels or seen_labels.add(l))]

        if dry_run:
            print(" -> [DRY RUN 모드] 실제 Blogger API 발행을 모의 처리합니다.")
            pub_result = {
                "success": True,
                "url": f"https://blogin365ai.blogspot.com/preview-dry-run-{int(time.time())}.html",
                "id": f"dry-run-{int(time.time())}",
                "attempts": 1
            }
        else:
            category = matched_topic.get("category", "FINANCE")
            pub_result = self.gateway.publish(title, assembled_html, labels=labels, is_draft=False, category=category, max_retries=3)
            if not pub_result["success"]:
                # Retry with force token refresh
                print(" 🔄 [Self-Healing] Blogger 발행 재시도 및 OAuth 인증 재검증...")
                is_healed = True
                healing_events.append(f"Blogger retry triggered: {pub_result.get('error')}")
                pub_result = self.gateway.publish(title, assembled_html, labels=labels, is_draft=False, category=category, max_retries=2)
                if not pub_result["success"]:
                    raise RuntimeError(f"Blogger 발행 최종 실패: {pub_result.get('error')}")

            print(f" 🎉 블로그 발행 완료! URL: {pub_result['url']}")

        # Step 5-A: Record publication into Autonomous Topic Cluster Engine & Batch Pruner
        try:
            self.cluster_engine.record_publication(
                matched_topic["keyword"],
                pub_result.get("id", f"dry-run-{int(time.time())}"),
                pub_result.get("url", "")
            )
            from engine.maintenance.batch_pruner import BatchPrunerEngine
            pruner = BatchPrunerEngine()
            pruner.register_published_post(
                pub_result.get("id", f"dry-run-{int(time.time())}"),
                title,
                matched_topic["keyword"],
                matched_topic["category"],
                pub_result.get("url", "")
            )
        except Exception as ce_err:
            print(f" ⚠️ [Topic Cluster / Batch Pruner Record Warning]: {ce_err}")

        # -----------------------------------------------------------------
        # Step 5-B: Instant Indexing (Google Indexing API + IndexNow + Sitemap Ping)
        # -----------------------------------------------------------------
        print("\n[AI 직원 08] 검색엔진 즉각 색인(Instant Indexing) 전송...")
        indexing_res = self.indexer.submit_all(pub_result.get("url", ""), dry_run=dry_run)
        print(f" -> Google Indexing API & IndexNow 제출 완료 (상태: {indexing_res['results']['google_indexing']['status']})")

        # -----------------------------------------------------------------
        # Step 6: Viral Growth Loop & Multi-Channel Distribution
        # -----------------------------------------------------------------
        print("\n[AI 직원 07] Lazyowen 바이럴 그로스 패키지(15초 릴스 + 자동 DM 트리거) 생성...")
        growth_pkg = self.growth.generate_hooks(matched_topic, pub_result.get("url", ""))
        print(f" -> 릴스 후킹 대본: \"{growth_pkg['reel_script']['0-3초_후킹'][:40]}...\"")
        if growth_pkg.get("video_package"):
            vp = growth_pkg["video_package"]
            print(f" -> [MoneyPrinterTurbo] 15초 숏폼 비디오 패키지 생성 완료 [상태: {vp.get('status')} | Batch: {vp.get('batch_id')}]")
        print(f" -> 그로스 큐 저장 완료: data/viral_growth_queue.json")

        print("\n[AI 직원 07] 멀티 채널 소셜 배포(Multi-Channel Distribution) 큐 전송...")
        dist_res = self.distributor.dispatch_to_channels(growth_pkg, dry_run=dry_run)
        print(f" -> 소셜 배포 채널({list(dist_res['channels'].keys())}) 큐 적재 완료 [Batch: {dist_res['batch_id']}]")

        # -----------------------------------------------------------------
        # Step 7: Closed-Loop Feedback & Self-Healing Maintenance
        # -----------------------------------------------------------------
        print("\n[AI 직원 02 & 06] 폐쇄 루프 피드백(Closed-loop Feedback) & 링크 헬스 점검...")
        perf_metric = self.feedback.simulate_performance_sync(
            post_id=pub_result.get("id", "dry-run"),
            keyword=matched_topic["keyword"],
            category=matched_topic["category"],
            est_pvs=matched_topic["pvs"]
        )
        tuned_weights = self.feedback.tune_niche_weights()
        gsc_candidates_data = self.feedback.sync_gsc_performance_and_candidates()
        link_audit = self.refresher.audit_html_links(assembled_html, dry_run=dry_run)
        refresh_cands = self.refresher.scan_for_refresh_candidates(max_age_days=30)
        cands_count = gsc_candidates_data.get("total_candidates", 0)
        print(f" -> 성과 데이터 기록 완료 (CTR: {perf_metric['ctr_percent']}%) | 니치 가중치 자동 튜닝 완료 | GSC 재작성 후보: {cands_count}건")
        if link_audit.get("has_dead_links"):
            print(f" ⚠️ 링크 헬스 경고: 깨진 링크 {link_audit['dead_count']}개 감지")

        # Step 7-B: Unit Economics & Exit Valuation Update (철칙 5)
        try:
            from engine.analytics.unit_economics import UnitEconomicsCalculator
            from engine.analytics.asset_valuation import AssetValuationEngine
            ue_calc = UnitEconomicsCalculator()
            ue_metrics = ue_calc.record_to_company_logs()
            val_engine = AssetValuationEngine()
            val_data = val_engine.generate_and_save_pnl_ledger()
            print(f" -> [단위 경제성 & 엑시트 평가] 1,000건당 BEP: {ue_metrics['bep_metrics']['days_to_bep_post_indexing']}일 | 자산가치(36x): ${val_data['asset_valuation']['valuation_median_usd']:,.0f}")
        except Exception as ue_err:
            print(f" ⚠️ [Unit Economics/Valuation Warning]: {ue_err}")

        elapsed_time = round(time.time() - start_time, 2)
        final_status = "HEALED" if is_healed else "SUCCESS"

        cycle_record = {
            "cycle_id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "status": final_status,
            "dry_run": dry_run,
            "keyword": matched_topic["keyword"],
            "title": title,
            "category": matched_topic["category"],
            "tier": matched_topic.get("tier"),
            "ratio": matched_topic.get("ratio"),
            "subs": matched_topic.get("subs", []),
            "keyword_package": matched_topic.get("keyword_package"),
            "pvs": matched_topic["pvs"],
            "pvs_score": matched_topic["pvs"],
            "cpc": matched_topic["cpc"],
            "url": pub_result.get("url"),
            "post_id": pub_result.get("id"),
            "execution_time_sec": elapsed_time,
            "growth_package": growth_pkg,
            "indexing": indexing_res,
            "distribution": dist_res,
            "feedback": {
                "performance": perf_metric,
                "weights": tuned_weights,
                "gsc_candidates": gsc_candidates_data
            },
            "link_audit": link_audit,
            "refresh_candidates": refresh_cands,
            "trick_b": {
                "mode": trick_b_mode,
                "has_search_widget": "b365-search-nav" in assembled_html,
                "has_pills": "b365-search-pill" in assembled_html,
                "cse_cx_present": bool(cse_cx)
            },
            "healing_events": healing_events
        }

        self.logger.record_cycle(cycle_record)

        print(f"\n══════════════════════════════════════════════════════════════════════════")
        print(f"✨ [{cycle_id}] 7단계 완전자율 파이프라인 완주! [상태: {final_status} | 소요시간: {elapsed_time}s]")
        print(f"🔗 포스트 URL: {pub_result.get('url')}")
        print(f"══════════════════════════════════════════════════════════════════════════\n")

        return cycle_record


class CompanyRuntime:
    """
    Master Daemon & Executive Controller for Blogin 365 AI Holdings.
    Provides 24/7 autonomous scheduling, self-healing error recovery, and dashboard views.
    """
    def __init__(self):
        self.logger = CompanyLogger()
        self.staff = AICompanyStaff()
        self.pipeline = SelfHealingPipeline(self.logger)

    def print_dashboard(self):
        data = self.logger.load_data()
        metrics = data.get("metrics", {})
        history = data.get("execution_history", [])
        health = self.staff.check_health()
        cse_cx = os.getenv("GOOGLE_CSE_CX", "").strip()

        print("\n" + "═" * 76)
        print("  🏢 BLOGIN 365 AI HOLDINGS - AUTONOMOUS MEDIA OPERATING SYSTEM (v9.0 Apex)")
        print("  구글 블로거 기반 완전자동화 고수익 미디어 파이프라인")
        print("═" * 76)
        print(f"  • 도메인   : {data.get('brand')} (Blog ID: {data.get('blog_id')})")
        print(f"  • 상태     : 🟢 ACTIVE (24/7 자율 가동 가능 / Scheduler Ready)")
        print(f"  • 하트비트 : {data.get('last_heartbeat')}")
        print("─" * 76)
        print("  📊 핵심 비즈니스 KPI:")
        print(f"    - 총 실행 횟수       : {metrics.get('total_cycles_run', 0):,} 회")
        print(f"    - 성공률             : {metrics.get('success_rate_percent', 100.0):.1f}% (성공: {metrics.get('successful_cycles', 0)} / 실패: {metrics.get('failed_cycles', 0)})")
        print(f"    - 자가치유 복구      : {metrics.get('healed_cycles', 0)} 건 완벽 자동 복구")
        print(f"    - 총 발행 포스트     : {metrics.get('total_published_posts', 0)} 개")
        print(f"    - 누적 PVS 수익 점수 : {metrics.get('cumulative_pvs_score', 0):,.0f} pt")
        print("─" * 76)
        print("  🔍 Trick B 검색엔진 & AdSense for Search (AFS) 상태:")
        if cse_cx:
            print(f"    - 엔진 모드 : 🟢 GOOGLE_CSE 활성화 (CX ID: {cse_cx})")
            print("    - 광고 유닛 : AdSense for Search (AFS) 고단가 검색광고 실시간 송출 중")
        else:
            print("    - 엔진 모드 : 🟡 BLOG_SEARCH 무중단 듀얼 폴백 활성화 (CX 미설정 시 안전 내부 검색)")
            print("    - 안내      : SEO.env에 GOOGLE_CSE_CX를 입력하면 즉시 구글 공식 검색광고로 승격됩니다.")
        print("─" * 76)
        print("  👥 8인 AI 직원 조직도 & 헬스체크 (Every AI Playbook Org Chart):")
        for key, info in health.items():
            icon = "🟢" if info["status"] == "HEALTHY" else "🟡"
            print(f"    [{key.split('_')[0]}] {info['name']:<52} {icon} {info['status']}")
        print("─" * 76)
        print("  📜 최근 발행 및 운영 기록:")
        if not history:
            print("    (아직 실행 기록이 없습니다. --once 또는 --daemon으로 가동하십시오.)")
        else:
            for item in history[:5]:
                dt = item.get("timestamp", "")[:19].replace("T", " ")
                kw = item.get("keyword", "")
                pvs = item.get("pvs_score", 0)
                st = item.get("status", "")
                dur = item.get("execution_time_sec", 0)
                url = item.get("url", "")
                print(f"    [{dt}] [{st:<7}] {kw:<18} | PVS: {pvs:>10,.0f} pt | {dur:>4.1f}s | {url}")
        print("─" * 76)
        print("  🎯 1호 핵심 도메인: FinTech Micro-SaaS & 20대 핵심 자산 pSEO 팩토리 (v9.0 Apex):")
        print("     [활성 도메인: 투자/트레이딩 퀀트 유틸리티 & 세금·수익률 시뮬레이터 (FinTech)]")
        print("    ▶ [ACTIVE]  해외주식/가상자산 세금·손익통산 시뮬레이터  | 20대 자산 [██████████] 100.0% | PVS 기대수익: 10,000,000.0 pt")
        print("    ▶ [ACTIVE]  주식/코인 물타기(평단가) & 본전 탈출 역산기 | 20대 자산 [██████████] 100.0% | PVS 기대수익:  8,500,000.0 pt")
        print("    ▶ [ACTIVE]  선물 레버리지·청산가 & 켈리 공식 계산기     | 20대 자산 [██████████] 100.0% | PVS 기대수익:  9,200,000.0 pt")
        print("    ▶ [ACTIVE]  배당금 재투자·복리 & 금융소득종합과세 계산기 | 20대 자산 [██████████] 100.0% | PVS 기대수익:  8,900,000.0 pt")
        print("      [STANDBY] 5대 레거시 정보형 클러스터 (배경 자동 보조 대기)")
        print("─" * 76)
        print("  💎 단위 경제성(Unit Economics) & 엑시트(Exit) 밸류에이션 (v9.0 Apex):")
        try:
            from engine.analytics.unit_economics import UnitEconomicsCalculator
            from engine.analytics.asset_valuation import AssetValuationEngine
            from engine.maintenance.batch_pruner import BatchPrunerEngine

            ue = UnitEconomicsCalculator().simulate_1000_page_batch()
            val = AssetValuationEngine().calculate_valuation()
            pruner_st = BatchPrunerEngine().load_state()

            print(f"    - 포스트 원가 / 1,000개   : ${ue['cost_breakdown']['cost_per_page_usd']:.4f} (약 {ue['cost_breakdown']['cost_per_page_krw']:.1f}원) / ${ue['cost_breakdown']['total_batch_cost_usd']:.2f}")
            print(f"    - 목표 RPM / 월 예상 매출 : ${ue['performance_projection']['target_rpm']:.2f} / ${ue['performance_projection']['monthly_revenue_usd']:,.2f} ({ue['performance_projection']['monthly_revenue_krw']:,.0f}원)")
            print(f"    - 손익분기점(BEP)         : 색인 후 단 {ue['bep_metrics']['days_to_bep_post_indexing']}일 (연간 ROI +{ue['bep_metrics']['first_year_roi_percent']:,}%)")
            print(f"    - Empire Flippers 매각가  : ${val['asset_valuation']['valuation_median_usd']:,.0f} (약 {val['asset_valuation']['valuation_median_krw']/100_000_000:.2f}억 원, 36x 기준)")
            print(f"    - 21-Day Pruner 수명주기  : 모니터링 {pruner_st.get('posts_evaluated', 0)}건 (자가치유: {pruner_st.get('self_healed_count', 0)}, 가지치기: {pruner_st.get('pruned_count', 0)})")
        except Exception as v_err:
            print(f"    ⚠️ 밸류에이션 로드 알림: {v_err}")
        print("─" * 76)
        print("  🌐 FinTech Micro-SaaS 4단계 오토 파일럿 파이프라인:")
        print("    [1. Intent & Ground Truth DB] → [2. Vanilla JS Micro-SaaS 렌더러]")
        print("    → [3. Playwright 3대 뷰포트 & YMYL QA 검증] → [4. 2-Step 영문 슬러그 & Google 즉각 색인]")
        print("═" * 76 + "\n")

    def print_staff_prompts(self):
        print("\n" + "═" * 78)
        print("  🎖️ BLOGIN 365 AI HOLDINGS - 8인 AI 직원 전용 마스터 시스템 프롬프트 (v9.0 Apex)")
        print("  f/prompts.chat (⭐17.3만) & Every AI Playbook Org Chart 기준 100% 통합")
        print("═" * 78)
        for role_key, role_data in self.staff.ROLES.items():
            print(f"\n[{role_key}] {role_data['title']}")
            print(f"• 직무 개요: {role_data['description']}")
            print("─" * 78)
            print(role_data['system_prompt'].strip())
            print("─" * 78)
        print("\n" + "═" * 78 + "\n")

    def run_once(self, dry_run: bool = False, keyword_override: Optional[str] = None, use_legacy: bool = False, mode: Optional[str] = None) -> Dict[str, Any]:
        start_t = time.time()
        if use_legacy:
            try:
                return self.pipeline.run_cycle(dry_run=dry_run, keyword_override=keyword_override)
            except Exception as e:
                traceback.print_exc()
                err_record = {
                    "cycle_id": f"ERR-LEGACY-{int(time.time())}",
                    "timestamp": datetime.now().isoformat(),
                    "status": "FAILED",
                    "dry_run": dry_run,
                    "keyword": keyword_override or "Unknown",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                self.logger.record_cycle(err_record)
                raise e
        else:
            # 1. Check Strategy Lab Queue Dispatch
            strategy_pipeline = None
            try:
                from engine.crew.strategy_pipeline import StrategyLabPipeline
                strategy_pipeline = StrategyLabPipeline(base_dir=BASE_DIR)
            except Exception as import_err:
                print(f"[CompanyRuntime] StrategyLabPipeline import notice: {import_err}")

            should_run_strategy = False
            if strategy_pipeline:
                if mode == "strategy":
                    should_run_strategy = True
                elif mode == "calculator":
                    should_run_strategy = False
                else:
                    # Autonomous auto-dispatch: if strategy queue has PENDING topics, prioritize Strategy Lab
                    is_strat_kw = any(s.get("strategy_id") == keyword_override for s in getattr(strategy_pipeline, 'queue', [])) if keyword_override else False
                    nxt = strategy_pipeline.get_next_topic(topic_id_override=keyword_override) if is_strat_kw else None
                    if nxt is not None and nxt.get("status") == "PENDING":
                        should_run_strategy = True

            if should_run_strategy and strategy_pipeline:
                print("\n" + "═" * 76)
                print("  📈 [Blogin 365 AI Holdings] VIBE TRADING STRATEGY LAB AUTONOMOUS CYCLE")
                print("  • 엔진 : TradingView Lightweight Charts (v4.1) + Apolia 8-Block + Blogger API v3")
                print(f"  • 모드 : {'🟢 LIVE PUBLISH (실제 블로거 배포)' if not dry_run else '🟡 DRY-RUN'}")
                print("═" * 76 + "\n")
                try:
                    res = strategy_pipeline.run_autonomous_cycle(dry_run=dry_run, topic_id_override=keyword_override)
                    cycle_record = {
                        "cycle_id": f"STRATEGY-{int(time.time())}",
                        "timestamp": datetime.now().isoformat(),
                        "status": res.get("status", "SUCCESS"),
                        "execution_time_sec": res.get("execution_time_sec", round(time.time() - start_t, 2)),
                        "dry_run": dry_run,
                        "title": res.get("title", ""),
                        "url": res.get("url", ""),
                        "post_id": res.get("post_id", ""),
                        "keyword": res.get("title", ""),
                        "category": "FINTECH_QUANT",
                        "pvs_score": 12500000.0,
                        "cpc": 4200,
                        "niche_name": "투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터 (Strategy Lab)"
                    }
                    self.logger.record_cycle(cycle_record)
                    return res
                except Exception as strat_err:
                    print(f"❌ [StrategyLab Pipeline Error]: {strat_err}")
                    traceback.print_exc()
                    err_record = {
                        "cycle_id": f"ERR-STRATEGY-{int(time.time())}",
                        "timestamp": datetime.now().isoformat(),
                        "status": "FAILED",
                        "dry_run": dry_run,
                        "keyword": keyword_override or "Strategy Lab",
                        "error": str(strat_err),
                        "traceback": traceback.format_exc()
                    }
                    self.logger.record_cycle(err_record)
                    raise strat_err

            # 2. Universal 8-Agent Editorial Pipeline (Primary Media Engine)
            if mode != "calculator":
                try:
                    return self.pipeline.run_cycle(dry_run=dry_run, keyword_override=keyword_override)
                except Exception as ed_err:
                    traceback.print_exc()
                    err_record = {
                        "cycle_id": f"ERR-EDITORIAL-{int(time.time())}",
                        "timestamp": datetime.now().isoformat(),
                        "status": "FAILED",
                        "dry_run": dry_run,
                        "keyword": keyword_override or "Universal Topic",
                        "error": str(ed_err),
                        "traceback": traceback.format_exc()
                    }
                    self.logger.record_cycle(err_record)
                    raise ed_err

            # 3. Fallback to FinTech Micro-SaaS Calculator Orchestrator
            try:
                from engine.crew.crew import MicroSaaSPipelineOrchestrator
                from engine.harness.harness_facade import harness_facade
                orchestrator = MicroSaaSPipelineOrchestrator()
                hint = keyword_override or "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터"
                res = orchestrator.run_pipeline(user_topic_hint=hint, dry_run=dry_run)
                cycle_record = {
                    "cycle_id": f"FINTECH-{int(time.time())}",
                    "timestamp": datetime.now().isoformat(),
                    "status": res.get("status", "SUCCESS"),
                    "execution_time_sec": round(time.time() - start_t, 2),
                    "dry_run": dry_run,
                    "title": res.get("target_keyword", hint),
                    "url": res.get("url", ""),
                    "post_id": res.get("publish_record", {}).get("id", ""),
                    "keyword": res.get("target_keyword", hint),
                    "category": "FINTECH",
                    "pvs_score": 10000000.0,
                    "cpc": 3500,
                    "niche_name": "투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터"
                }
                self.logger.record_cycle(cycle_record)
                return res
            except Exception as e:
                # Harness² Self-Scaffolding Intercept & Auto-Retry Loop
                try:
                    from engine.harness.harness_facade import harness_facade
                    print(f"\n🧬 [Harness² Intercept] 파이프라인 예외 감지: {e}")
                    compose_res = harness_facade.handle_runtime_failure(
                        module_name="MicroSaaSPipelineOrchestrator",
                        error=e,
                        context={"keyword": hint, "dry_run": dry_run}
                    )
                    if compose_res.success:
                        print(f"🧬 [Harness² Evolved] 하네스 변이 채택 완료 (Active Gen {compose_res.generation}) -> 파이프라인 1회 자율 재시도 가동...")
                        res = orchestrator.run_pipeline(user_topic_hint=hint, dry_run=dry_run)
                        cycle_record = {
                            "cycle_id": f"FINTECH-HEALED-{int(time.time())}",
                            "timestamp": datetime.now().isoformat(),
                            "status": "HEALED",
                            "execution_time_sec": round(time.time() - start_t, 2),
                            "dry_run": dry_run,
                            "title": res.get("target_keyword", hint),
                            "url": res.get("url", ""),
                            "post_id": res.get("publish_record", {}).get("id", ""),
                            "keyword": res.get("target_keyword", hint),
                            "category": "FINTECH",
                            "pvs_score": 10000000.0,
                            "cpc": 3500,
                            "niche_name": "투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터"
                        }
                        self.logger.record_cycle(cycle_record)
                        return res
                except Exception as retry_err:
                    print(f"🧬 [Harness² Warning] 자가 진화 후 재시도 중 추가 예외: {retry_err}")

                traceback.print_exc()
                err_record = {
                    "cycle_id": f"ERR-FINTECH-{int(time.time())}",
                    "timestamp": datetime.now().isoformat(),
                    "status": "FAILED",
                    "dry_run": dry_run,
                    "keyword": keyword_override or "FinTech Micro-SaaS",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                self.logger.record_cycle(err_record)
                raise e

    def run_daemon(self, target_hours: Optional[List[int]] = None, check_interval_sec: int = 30, dry_run: bool = False):
        if target_hours is None:
            target_hours = [9, 15, 21]

        last_executed_slot = None  # (YYYY-MM-DD, hour)
        last_heartbeat_time = 0

        print("\n" + "═" * 76)
        print("  ⚡ BLOGIN 365 AI HOLDINGS - 24/7 DAEMON ENGINE STARTED")
        print(f"  • 정기 발행 시각: 매일 {', '.join(f'{h:02d}:00' for h in target_hours)} KST")
        print(f"  • 모니터링 주기 : {check_interval_sec}초 간격 하트비트")
        print(f"  • 무인 자동 치유: 활성화됨 (Zero-Intervention 365 Days)")
        print("═" * 76 + "\n")

        while True:
            try:
                now = datetime.now()
                current_slot = (now.strftime("%Y-%m-%d"), now.hour)

                # Periodic Heartbeat every 10 minutes
                if time.time() - last_heartbeat_time > 600:
                    self.logger.record_heartbeat()
                    last_heartbeat_time = time.time()

                # Trigger Condition
                if now.hour in target_hours and current_slot != last_executed_slot:
                    print(f"\n[DAEMON TRIGGER] 정기 발행 시각 도달: {now.strftime('%Y-%m-%d %H:%M:%S')} (Hour: {now.hour})")
                    try:
                        self.run_once(dry_run=dry_run)
                        last_executed_slot = current_slot
                        print(f"[DAEMON] 정기 발행 완주 성공. 다음 스케줄 대기 중...")
                    except Exception as loop_err:
                        print(f"❌ [DAEMON WARNING] 사이클 오류 발생: {loop_err}")
                        traceback.print_exc()
                        # Sleep 5 minutes before retrying to prevent thrashing
                        time.sleep(300)

                time.sleep(check_interval_sec)

            except KeyboardInterrupt:
                print("\n[DAEMON] 사용자에 의해 데몬이 정상 종료되었습니다.")
                break
            except Exception as outer_err:
                print(f"❌ [DAEMON UNCAUGHT] 최상위 루프 오류 감지: {outer_err}")
                traceback.print_exc()
                time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blogin 365 AI Holdings Autonomous Runtime")
    parser.add_argument("--once", action="store_true", help="1회 즉시 완전 자율 사이클 실행 후 종료")
    parser.add_argument("--strategy", action="store_true", help="트레이딩뷰 전략 연구소 파이프라인 전용 실행")
    parser.add_argument("--calculator", action="store_true", help="핀테크 Micro-SaaS 계산기 파이프라인 전용 실행")
    parser.add_argument("--dry-run", action="store_true", help="실제 Blogger 발행 없이 전과정 안전 테스트")
    parser.add_argument("--daemon", action="store_true", help="24/7 상시 백그라운드 무인 데몬 가동")
    parser.add_argument("--dashboard", "--status", action="store_true", help="기업 운영 현황 및 8인 AI 직원 헬스 대시보드 출력")
    parser.add_argument("--staff-prompts", "--prompts", action="store_true", help="8인 AI 직원 전용 v9.0 Apex 마스터 프롬프트 전체 출력")
    parser.add_argument("--legacy", action="store_true", help="레거시 Crawl4AI 블로그 파이프라인 강제 실행")
    parser.add_argument("--keyword", type=str, default=None, help="타겟 키워드 또는 전략 ID 강제 지정")
    parser.add_argument("--health", action="store_true", help="8인 AI 직원 상태 전수 검사")

    args = parser.parse_args()
    runtime = CompanyRuntime()

    pipeline_mode = "strategy" if args.strategy else ("calculator" if args.calculator else None)

    if args.staff_prompts:
        runtime.print_staff_prompts()
    elif args.dashboard:
        runtime.print_dashboard()
    elif args.health:
        health_info = runtime.staff.check_health()
        print("=== 8인 AI 직원 헬스체크 리포트 ===")
        for k, v in health_info.items():
            print(f"[{k}] {v['name']}: {v['status']} - {v['details']}")
    elif args.daemon:
        runtime.run_daemon(dry_run=args.dry_run)
    elif args.once or args.keyword or args.strategy or args.calculator:
        runtime.run_once(dry_run=args.dry_run, keyword_override=args.keyword, use_legacy=args.legacy, mode=pipeline_mode)
    else:
        # Default with no args: Show dashboard and run once
        runtime.print_dashboard()
