# -*- coding: utf-8 -*-
"""
engine/main.py
--------------
Blogin 365 AI Master Harness Orchestrator (v6.0)
Coordinates the 6-Phase Autonomous Publishing & Monetization Pipeline:
1. Phase 1: Trend Radar & Demand Matcher (Google Trends KR + High-CPC DB + PVS v2.0)
2. Phase 2: AI Investigative Writer (AgencyStack + Anti-Slop Enforcement)
3. Phase 3: World-Class CRO & Micro-SaaS Assembly (CROMonetizer + Canvas SVG + JS Calculator)
4. Phase 4: gstack & hallmark 57-Gate QA Audit (GStackAuditor - Zero-Persona, Zero Broken Entities)
5. Phase 5: Google Blogger Gateway (BloggerGateway + Schema.org Article JSON-LD)
6. Phase 6: Viral Growth Loop (ViralHookMaker - 15s Reel Script + ManyChat '10' DM Trigger)
"""

import os
import sys
import time
import argparse
from datetime import datetime

# Enforce UTF-8 console output for Windows PowerShell
sys.stdout.reconfigure(encoding='utf-8')

# Ensure engine path is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.radar.trend_scout import TrendScout
from engine.matcher.demand_matcher import DemandMatcher
from engine.agents.agency_stack import AgencyStack
from engine.agents.cro_monetizer import assemble_world_class_article
from engine.qa.gstack_auditor import GStackAuditor
from engine.publisher.blogger_gateway import BloggerGateway
from engine.growth.viral_hook_maker import ViralHookMaker
from engine.company_runtime import CompanyLogger


class BloginMasterHarness:
    def __init__(self):
        self.scout = TrendScout()
        self.matcher = DemandMatcher()
        self.agency = AgencyStack()
        self.auditor = GStackAuditor()
        self.gateway = BloggerGateway()
        self.growth = ViralHookMaker()
        self.logger = CompanyLogger()

    def run_pipeline(self, dry_run: bool = False, keyword_override: str = None) -> dict:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n========================================================")
        print(f"🚀 Blogin 365 AI 파이프라인 가동 [{timestamp_str}]")
        print(f"========================================================")

        # ----------------------------------------------------
        # Phase 1: Radar & Demand Matcher
        # ----------------------------------------------------
        print("[Phase 1/6] 실시간 트렌드 레이더 및 상업적 수요 매칭 분석...")
        if keyword_override:
            trends = [{"keyword": keyword_override, "traffic_volume": 50000, "source": "keyword_override"}]
            expanded_subs = self.scout.expand_autocomplete(keyword_override, limit=6)
        else:
            trends = self.scout.fetch_live_trends(limit=10)
            top_kw = trends[0]["keyword"] if trends else "청년도약계좌"
            expanded_subs = self.scout.expand_autocomplete(top_kw, limit=6)

        matched_topic = self.matcher.select_best_topic(trends, sub_candidates=expanded_subs)
        print(f" -> 선정 메인 키워드: [{matched_topic['keyword']}]")
        print(f" -> 7티어 경쟁 판정: [{matched_topic.get('tier', '최적')}] (골든 비율: {matched_topic.get('ratio', 0):.2f})")
        print(f" -> 서브 키워드(1:1 H2 매핑): {matched_topic.get('subs', [])}")
        print(f" -> 카테고리: {matched_topic['category']} | 검색의도: {matched_topic['intent']}")
        print(f" -> PVS v2.0 수익 속도 점수: {matched_topic['pvs']:,.0f} pt (예상 CPC: {matched_topic['cpc']}원)")

        # ----------------------------------------------------
        # Phase 2: AI Investigative Writer
        # ----------------------------------------------------
        print("\n[Phase 2/6] 저널리즘 에디토리얼 본문 및 FAQ 생성 (1:1 서브키워드 소제목 할당)...")
        editorial = self.agency.write_editorial_content(matched_topic)
        print(f" -> 섹션 {len(editorial.get('sections', []))}개 및 FAQ {len(editorial.get('faq', []))}개 집필 완료")

        # ----------------------------------------------------
        # Phase 3: World-Class CRO & Visual Assembly
        # ----------------------------------------------------
        print("\n[Phase 3/6] 월드클래스 UX/UI 조립 (Bento Hero + SaaS 계산기 + Canvas SVG + 애드센스 4슬롯)...")
        assembled_html = assemble_world_class_article(matched_topic, editorial)
        title = matched_topic.get("title", f"{matched_topic['keyword']} 실측 분석 및 모의 계산 가이드")
        print(f" -> 제목: {title}")
        print(f" -> 최종 HTML 조립 완료: {len(assembled_html):,} bytes")

        # ----------------------------------------------------
        # Phase 4: gstack & hallmark 57-Gate QA Audit
        # ----------------------------------------------------
        print("\n[Phase 4/6] gstack & hallmark 6대 무인 검수 게이트 가동...")
        audit_result = self.auditor.audit_post(title, assembled_html, keyword_package=matched_topic.get("keyword_package"))
        if not audit_result["passed"]:
            print(" ⚠️ QA 게이트 경고 발생:")
            for err in audit_result["errors"]:
                print(f"   - {err}")
            print(" -> 자동 살균(Sanitize) 적용 후 재검수...")
            assembled_html = self.auditor.sanitize_if_possible(assembled_html)
            re_audit = self.auditor.audit_post(title, assembled_html, keyword_package=matched_topic.get("keyword_package"))
            if not re_audit["passed"]:
                raise RuntimeError(f"치명적 QA 검수 실패로 발행을 중단합니다: {re_audit['errors']}")
            print(" -> 살균 후 QA 게이트 통과 완료!")
        else:
            print(" -> 6대 핵심 검수 게이트(Zero-Persona, Zero-Broken-Entity, Anti-Slop, CRO, Content, 1:1-Keyword) 100% 통과!")

        # ----------------------------------------------------
        # Phase 5: Google Blogger Gateway
        # ----------------------------------------------------
        print("\n[Phase 5/6] 구글 블로거 발행 게이트웨이...")
        # 태그(Labels): 메인 키워드 포함 + 서브 키워드 전부 포함 (바이브 메이커 공식)
        raw_labels = [matched_topic["keyword"]] + matched_topic.get("subs", []) + ["정보", matched_topic["category"], "모의계산", "Blogin365AI"]
        seen_labels = set()
        labels = [l for l in raw_labels if l and not (l in seen_labels or seen_labels.add(l))]

        if dry_run:
            print(" -> [DRY RUN 모드] 실제 Blogger 발행을 건너뜁니다.")
            pub_result = {
                "success": True,
                "url": "https://blogin365ai.blogspot.com/preview-dry-run.html",
                "id": "dry-run-post-id"
            }
        else:
            pub_result = self.gateway.publish(title, assembled_html, labels=labels, is_draft=False, category=matched_topic["category"])
            if not pub_result["success"]:
                raise RuntimeError(f"Blogger 발행 오류: {pub_result.get('error')}")
            print(f" 🎉 블로그 발행 완료! URL: {pub_result['url']}")

        # ----------------------------------------------------
        # Phase 6: Viral Growth Loop
        # ----------------------------------------------------
        print("\n[Phase 6/6] Lazyowen 바이럴 그로스 패키지(15초 릴스 + 자동 DM 트리거) 생성...")
        growth_pkg = self.growth.generate_hooks(matched_topic, pub_result.get("url", ""))
        print(f" -> 릴스 후킹 대본: \"{growth_pkg['reel_script']['0-3초_후킹'][:40]}...\"")
        print(f" -> 그로스 큐 저장 완료: data/viral_growth_queue.json")

        cycle_log = {
            "cycle_id": f"CYC-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS",
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
            "growth_package": growth_pkg
        }
        self.logger.record_cycle(cycle_log)

        print(f"\n========================================================")
        print(f"✨ 6단계 파이프라인 전체 완주 성공! [URL: {pub_result.get('url')}]")
        print(f"========================================================\n")

        return {
            "title": title,
            "url": pub_result.get("url"),
            "keyword": matched_topic["keyword"],
            "category": matched_topic["category"],
            "tier": matched_topic.get("tier"),
            "ratio": matched_topic.get("ratio"),
            "subs": matched_topic.get("subs", []),
            "sub_details": matched_topic.get("sub_details", []),
            "keyword_package": matched_topic.get("keyword_package"),
            "pvs": matched_topic["pvs"],
            "growth_package": growth_pkg
        }

    def start_scheduler(self):
        """
        Runs autonomous loop (e.g. 09:00, 15:00, 21:00 schedule)
        """
        target_hours = {9, 15, 21}
        last_executed_slot = None  # (YYYY-MM-DD, hour)
        print("🕒 Blogin 365 AI 무인 스케줄러가 활성화되었습니다. (매일 09:00, 15:00, 21:00 자동 발행)")

        while True:
            now = datetime.now()
            current_slot = (now.strftime("%Y-%m-%d"), now.hour)
            if now.hour in target_hours and current_slot != last_executed_slot:
                print(f"\n[스케줄러 트리거] 정기 발행 시각 감지: {now.strftime('%H:%M')}")
                try:
                    self.run_pipeline(dry_run=False)
                    last_executed_slot = current_slot
                except Exception as e:
                    print(f"❌ 스케줄러 파이프라인 실행 중 오류: {e}")
            time.sleep(30)


if __name__ == "__main__":
    from engine.company_runtime import CompanyRuntime

    parser = argparse.ArgumentParser(description="Blogin 365 AI Master Harness")
    parser.add_argument("--once", action="store_true", help="1회 즉시 실행 후 종료")
    parser.add_argument("--dry-run", action="store_true", help="실제 Blogger 발행 없이 전 과정 테스트")
    parser.add_argument("--keyword", type=str, default=None, help="특정 키워드 강제 지정")
    parser.add_argument("--dashboard", "--status", action="store_true", help="AI 회사 대시보드 출력")
    args = parser.parse_args()

    if args.dashboard:
        CompanyRuntime().print_dashboard()
    else:
        harness = BloginMasterHarness()
        if args.once or args.dry_run or args.keyword:
            harness.run_pipeline(dry_run=args.dry_run, keyword_override=args.keyword)
        else:
            # Default: run once immediately, then enter scheduler
            try:
                harness.run_pipeline(dry_run=False)
            except Exception as e:
                print(f"초회 실행 오류: {e}")
            harness.start_scheduler()
