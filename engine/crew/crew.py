# -*- coding: utf-8 -*-
"""
engine/crew/crew.py
-------------------
CrewAI Programmatic Micro-SaaS 파이프라인 수석 오케스트레이터
타겟 도메인: 투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터 (FinTech Micro-SaaS)
- [Requirement 1] SSOT data/trading_rules_db.json 금융/세무 데이터베이스 연동
- [Requirement 2] 0ms 반응형 Vanilla JS 인터랙티브 계산기 템플릿 & 실시간 수식
- [Requirement 3] 헤드리스 Playwright 자동 검증기 (0원/음수/10억 경계값, YMYL 면책 조항, FinanceApplication 스키마)
- [Requirement 4] 4대장 일괄 배포(Batch Run) & 사일로 내부 링크(Internal Silo Mesh) 자동 연계
"""

import os
import sys
import json
import re
import time
import argparse
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, "SEO.env"))

from crewai import Crew, Process
from engine.crew.agents import MicroSaaSCrewAgents
from engine.crew.tasks import MicroSaaSCrewTasks
from engine.crew.thumbnail_generator import create_thumbnail_sync
from engine.crew.image_uploader import ImageUploader
from engine.crew.qa_validator import run_validator
from engine.crew.publisher import MicroSaaSBloggerPublisher
from engine.crew.dataset_resolver import TradingDatasetResolver, HardwareDatasetResolver


RULE_CATEGORY_LABELS = {
    "overseas_stock_tax": ["세금·절세 시뮬레이터", "해외주식 양도세", "손익통산", "핀테크 계산기"],
    "water_averaging_dca": ["물타기·평단가 계산기", "주식 코인 물타기", "BEP 탈출", "핀테크 계산기"],
    "leverage_liquidation_kelly": ["선물·레버리지 계산기", "강제청산가", "켈리 공식", "핀테크 계산기"],
    "dividend_compound_tax": ["배당·복리 시뮬레이터", "금융소득종합과세", "배당금 복리", "핀테크 계산기"]
}


class MicroSaaSPipelineOrchestrator:
    def __init__(self):
        self.agents = MicroSaaSCrewAgents()
        self.tasks = MicroSaaSCrewTasks()
        self.uploader = ImageUploader()
        self.publisher = MicroSaaSBloggerPublisher()
        self.resolver = TradingDatasetResolver()
        self.hw_resolver = HardwareDatasetResolver()

    def _extract_spec_json(self, t1_raw_text: str, default_rule_info: Dict[str, Any]) -> Dict[str, Any]:
        """t1 기획 결과물에서 JSON 블록을 안전하게 파싱"""
        try:
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', t1_raw_text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(t1_raw_text.strip())
        except Exception:
            return {
                "target_keyword": default_rule_info.get("target_keyword", "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터"),
                "math_formula": default_rule_info.get("formula_badge", "Tax = Max(0, (Gain - Loss - Fees) - 2500000) * 0.22"),
                "formula_badge": default_rule_info.get("formula_badge", "양도세 = Max(0, 순수익 - 250만) × 22%"),
                "key_stat": default_rule_info.get("key_stat", "기본공제: 2,500,000원 | 총세율: 22%"),
                "sub_label": default_rule_info.get("sub_label", "2026 소득세법 제94조 손익통산 기준")
            }

    def run_pipeline(self, user_topic_hint: str = "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터", max_qa_retries: int = 2, dry_run: bool = True, custom_labels: Optional[List[str]] = None) -> Dict[str, Any]:
        print("\n" + "═" * 78)
        print("  🏢 [CrewAI FinTech Micro-SaaS Engine] 4단계 자율 엔터프라이즈 파이프라인 가동")
        print(f"  • 타겟 니치 : 투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터 (FinTech)")
        print(f"  • 주제 힌트 : {user_topic_hint}")
        print(f"  • 실행 모드 : {'🟢 LIVE PUBLISH (실제 블로거 배포)' if not dry_run else '🟡 DRY-RUN (시뮬레이션 검증)'}")
        print("═" * 78 + "\n")

        researcher = self.agents.keyword_intent_researcher()
        coder = self.agents.frontend_tool_builder()
        seo_packager = self.agents.technical_seo_writer()

        # [FinTech Engine] SSOT 금융 DB에서 정확한 스펙 및 위젯/테이블/사일로 링크 사전 매핑
        resolved = self.resolver.resolve_topic(user_topic_hint)
        rule_key = resolved["rule_key"]
        fintech_widget = self.resolver.render_trading_saas_html(rule_key)
        paper_trading_widget = self.resolver.render_paper_trading_component(rule_key)
        fintech_tables = self.resolver.render_trading_tables(rule_key)
        monetization_cta = self.resolver.render_monetization_cta(rule_key)
        legal_disclaimer = self.resolver.render_legal_disclaimer()
        internal_silo_links = self.resolver.render_internal_silo_links(rule_key)
        
        rule_info = resolved.get("rule_info", {})
        cat = rule_info.get("category", "")
        ticker = rule_info.get("ticker", "")
        if custom_labels:
            post_labels = custom_labels
        elif rule_key in RULE_CATEGORY_LABELS:
            post_labels = RULE_CATEGORY_LABELS[rule_key]
        elif cat == "us_stock":
            post_labels = ["미국주식 세금", ticker, "해외주식 양도세", "핀테크 계산기"]
        elif cat == "crypto":
            post_labels = ["가상자산", ticker, "코인 선물 청산가", "핀테크 계산기"]
        elif cat == "retirement":
            post_labels = ["절세계좌", "연금 세액공제", "비과세 시뮬레이터", "핀테크 계산기"]
        else:
            post_labels = ["핀테크 계산기", "퀀트 유틸리티"]

        # [Stage 1] 키워드 & 인터랙티브 수식 기획 태스크
        print("[Step 1/4] 키워드 의도 및 엣지 케이스 금융 수식 기획 실행 중...")
        t1 = self.tasks.plan_interactive_keyword_task(researcher, user_hint=user_topic_hint)
        crew_stage1 = Crew(agents=[researcher], tasks=[t1], verbose=False)
        t1_output = crew_stage1.kickoff()
        t1_raw = str(t1_output.raw if hasattr(t1_output, 'raw') else t1_output)
        
        # 기획 결과물 영구 보존 및 동적 파싱
        spec_data = self._extract_spec_json(t1_raw, resolved)
        target_keyword = spec_data.get("target_keyword") or resolved["target_keyword"]
        spec_data.setdefault("formula_badge", resolved["formula_badge"])
        spec_data.setdefault("key_stat", resolved["key_stat"])
        spec_data.setdefault("sub_label", resolved["sub_label"])
        print(f" -> 기획 완료 타겟 키워드: [{target_keyword}]")
        print(f" -> 공식 계산 수식: [{spec_data.get('math_formula', resolved['formula_badge'])}]")

        # [Stage 2 & 3] 프론트엔드 위젯 개발 및 SEO 패키징
        print("\n[Step 2/4] Single-File FinTech Micro-SaaS 빌드 및 Technical SEO 결합 중...")
        t2 = self.tasks.build_micro_saas_widget_task(coder)
        t3 = self.tasks.package_technical_seo_task(seo_packager)

        crew_stage2 = Crew(agents=[coder, seo_packager], tasks=[t2, t3], verbose=False)
        stage2_output = crew_stage2.kickoff()
        generated_html = str(stage2_output.raw if hasattr(stage2_output, 'raw') else stage2_output)

        # 고밀도 인터랙티브 위젯 & 실측 대조표 및 면책조항 결합
        full_interactive_bundle = fintech_widget + "\n" + paper_trading_widget + "\n" + fintech_tables
        if "[FRONTEND_WIDGET_CODE]" in generated_html:
            generated_html = generated_html.replace("[FRONTEND_WIDGET_CODE]", full_interactive_bundle)
        elif "blogin-saas-container" not in generated_html:
            generated_html = full_interactive_bundle + "\n" + generated_html

        # 테이블 삽입 보장
        if "과세표준" not in generated_html and "본전 탈출" not in generated_html and "청산 위험" not in generated_html and "복리 총자산" not in generated_html:
            generated_html = generated_html + "\n" + fintech_tables

        # 제휴 수익화 파이프라인 CTA 결합
        if monetization_cta and "blogin-monetization-box" not in generated_html:
            generated_html = generated_html + "\n" + monetization_cta

        # 내부 링크(Internal Silo) 결합
        if internal_silo_links and "blogin-internal-silo" not in generated_html:
            generated_html = generated_html + "\n" + internal_silo_links

        # 법적 면책 조항 결합
        if "legal-disclaimer" not in generated_html:
            generated_html = generated_html + "\n" + legal_disclaimer

        # [Stage 4] Playwright 샌드박스 무인 품질 검증 (Zero-Error Gate)
        print("\n[Step 3/4] Playwright 헤드리스 샌드박스 무인 검증 (Zero-Error Gate) 가동...")
        qa_result = run_validator(generated_html)
        if qa_result.get("html"):
            generated_html = qa_result["html"]

        retry_count = 0
        while not qa_result["passed"] and retry_count < max_qa_retries:
            retry_count += 1
            print(f"\n⚠️ [QA Rejected] 결함 감지 (시도 {retry_count}/{max_qa_retries}): {qa_result['errors']}")
            
            # Harness² Self-Scaffolding Intercept
            try:
                from engine.harness.harness_facade import harness_facade
                harness_facade.handle_runtime_failure(
                    module_name="MicroSaaSCoder",
                    error=Exception("; ".join(qa_result.get("errors", ["QA Validation failed"]))),
                    context={"target_keyword": target_keyword, "attempt": retry_count}
                )
            except Exception as h_err:
                print(f"🧬 [Harness² Warning]: {h_err}")

            print("🔄 [Self-Healing] Coder에게 t1 기획 명세서 + 에러 로그를 동시 주입하여 자가치유 재작성...")

            fix_task = self.tasks.repair_micro_saas_widget_task(
                agent=coder,
                original_spec_json=t1_raw,
                error_logs=qa_result["errors"]
            )

            repair_crew = Crew(agents=[coder, seo_packager], tasks=[fix_task, t3], verbose=False)
            repair_output = repair_crew.kickoff()
            generated_html = str(repair_output.raw if hasattr(repair_output, 'raw') else repair_output)
            
            if internal_silo_links and "blogin-internal-silo" not in generated_html:
                generated_html = generated_html + "\n" + internal_silo_links
            if "legal-disclaimer" not in generated_html:
                generated_html = generated_html + "\n" + legal_disclaimer
            qa_result = run_validator(generated_html)
            if qa_result.get("html"):
                generated_html = qa_result["html"]
            if qa_result.get("html"):
                generated_html = qa_result["html"]

        if not qa_result["passed"]:
            print("⚠️ [FinTech Fallback] Coder 출력이 QA 기준 미달이므로 SSOT 검증 완료된 핀테크 템플릿으로 안전 조립...")
            generated_html = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "SoftwareApplication",
      "name": "{target_keyword}",
      "operatingSystem": "Any",
      "applicationCategory": "FinanceApplication",
      "offers": {{ "@type": "Offer", "price": "0" }}
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "{target_keyword}의 연산 원리는 무엇인가요?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{resolved.get('rule_info', {}).get('name', target_keyword)}의 공식을 기반으로 수학적 모델에 따라 0ms로 실시간 산출됩니다."
          }}
        }}
      ]
    }}
  ]
}}
</script>
<div style="max-width:880px; margin:0 auto; padding:12px; color:#f8fafc; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <h1 style="font-size:26px; font-weight:900; color:#f8fafc; margin-bottom:16px;">{target_keyword}</h1>
  <div style="background:#131c31; border:1px solid #1e293b; border-radius:12px; padding:16px; margin-bottom:24px;">
    <span style="background:#10b981; color:#0b0f19; font-size:11px; font-weight:800; padding:3px 8px; border-radius:4px;">핵심 요약</span>
    <p style="margin:8px 0 0 0; font-size:14px; color:#cbd5e1; line-height:1.6;">
      본 시뮬레이터는 최신 금융·세무 공식과 퀀트 알고리즘에 기반하여 오차 없는 정확한 수치를 0ms로 도출합니다. 복잡한 수식을 직접 계산할 필요 없이 입력값에 따라 즉시 최적의 결과를 확인하실 수 있습니다.
    </p>
  </div>
  {fintech_widget}
  {fintech_tables}
  {monetization_cta}
  {internal_silo_links}
  {legal_disclaimer}
</div>
"""
            qa_result = run_validator(generated_html)
            if qa_result.get("html"):
                generated_html = qa_result["html"]

        if not qa_result["passed"]:
            raise RuntimeError(f"🚨 [파이프라인 중단] QA 검증 최종 실패 (에러율 0% 원칙 위반): {qa_result['errors']}")

        print("✅ [QA Approved] 샌드박스 경계값 테스트 통과, FinanceApplication 스키마 적격, YMYL 면책조항 탑재 완료!")

        # 로컬 HTML 파일 영구 저장
        slug = rule_key
        local_html_path = os.path.join(BASE_DIR, "data", f"generated_{slug}_microsaas.html")
        with open(local_html_path, "w", encoding="utf-8") as f:
            f.write(generated_html)
        print(f" -> [Local Artifact] 완성된 HTML 파일 로컬 저장 완료: {local_html_path}")

        # Playwright WebP 썸네일 생성
        print("\n[Step 4/4] 썸네일 캡처, 외부 호스팅 업로드 및 Blogger 자동 발행...")
        thumb_dir = os.path.join(BASE_DIR, "data", "thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)
        thumb_filename = f"thumb_{slug}"
        
        local_thumb_path = create_thumbnail_sync(
            filename=thumb_filename,
            title=target_keyword,
            formula_badge=spec_data.get("formula_badge") or resolved["formula_badge"],
            key_stat=spec_data.get("key_stat") or resolved["key_stat"],
            sub_label=spec_data.get("sub_label") or resolved["sub_label"],
            output_dir=thumb_dir
        )
        print(f" -> [Playwright] 고해상도 WebP 썸네일 로컬 캡처 완료: {local_thumb_path}")

        # 썸네일 외부 호스팅 업로드 (ImgBB/GitHub)
        upload_res = self.uploader.upload_image(local_thumb_path)
        hosted_thumb_url = upload_res.get("url")
        print(f" -> [ImageUploader] 호스팅된 썸네일 URL: {hosted_thumb_url} (제공자: {upload_res.get('provider')})")

        # [8인 AI 직원 실물 검수 & WCAG 2.1 AAA 자가치유 게이트]
        from engine.crew.editorial_inspector import EditorialInspector
        inspector = EditorialInspector()
        generated_html, editorial_review = inspector.inspect_and_heal(generated_html)
        print(f" -> [Editorial Board] 8인 AI 직원 실물 검수 완료 (자가치유 여부: {editorial_review.get('healed', False)})")

        # Google Blogger 발행 및 내부 사일로 DB 갱신
        publish_record = self.publisher.publish_post(
            title=target_keyword,
            html_content=generated_html,
            thumbnail_url=hosted_thumb_url,
            keyword=target_keyword,
            labels=post_labels,
            dry_run=dry_run,
            english_slug=resolved.get("english_slug")
        )

        print("\n" + "═" * 78)
        print(f"✨ [SUCCESS] FinTech Micro-SaaS 배포 완주!")
        print(f"• 포스트 제목 : {publish_record.get('title')}")
        print(f"• 카테고리    : {post_labels}")
        print(f"• 로컬 HTML  : {local_html_path}")
        print(f"• 썸네일 파일 : {local_thumb_path}")
        print(f"• 발행 URL   : {publish_record.get('url')}")
        print(f"• 발행 상태   : {publish_record.get('status')}")
        print("═" * 78 + "\n")

        return {
            "status": "COMPLETED",
            "rule_key": rule_key,
            "target_keyword": target_keyword,
            "labels": post_labels,
            "local_html_path": local_html_path,
            "local_thumb_path": local_thumb_path,
            "url": publish_record.get("url"),
            "publish_record": publish_record,
            "qa_result": qa_result
        }

    def run_batch_all_four(self, dry_run: bool = False) -> List[Dict[str, Any]]:
        """
        4대 핵심 금융 계산기 순차 일괄 배포 (Batch Run):
        1) 해외주식 양도소득세
        2) 물타기/BEP 역산 (직전 #1 내부 링크 결합)
        3) 선물 청산가/켈리 공식 (직전 #1, #2 내부 링크 결합)
        4) 배당금 복리/종합과세 (직전 #1, #2, #3 내부 링크 결합)
        """
        rules_sequence = [
            ("overseas_stock_tax", "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터"),
            ("water_averaging_dca", "주식 코인 물타기 평단가 및 본전 탈출 역산 시뮬레이터"),
            ("leverage_liquidation_kelly", "선물 레버리지 청산가 및 켈리 공식 포지션 사이징 계산기"),
            ("dividend_compound_tax", "배당금 복리 재투자 및 금융소득종합과세 시뮬레이터")
        ]

        print("\n" + "╔" + "═" * 76 + "╗")
        print("║   🚀 FinTech 4대 핵심 계산기 연속 자동 배포 (Batch Pipeline) 가동           ║")
        print(f"║   • 실행 모드 : {'🟢 LIVE PRODUCTION (Google Blogger 실제 발행)' if not dry_run else '🟡 DRY-RUN (모의 검증)'}  ║")
        print("╚" + "═" * 76 + "╝\n")

        results = []
        for idx, (r_key, hint) in enumerate(rules_sequence, 1):
            print(f"\n[{idx}/4] >>> '{hint}' 빌드 및 발행 시작...")
            res = self.run_pipeline(user_topic_hint=hint, dry_run=dry_run)
            results.append(res)
            
            # API 호출 간격 안정화
            if idx < len(rules_sequence) and not dry_run:
                print(" -> Blogger API 안정화를 위해 3초 대기 중...")
                time.sleep(3)

        print("\n" + "╔" + "═" * 76 + "╗")
        print("║   🎉 4대 핵심 핀테크 Micro-SaaS 배포 완료 리포트                             ║")
        print("╠" + "═" * 76 + "╣")
        for i, r in enumerate(results, 1):
            print(f"║ [{i}] {r['target_keyword']}")
            print(f"║     카테고리: {', '.join(r['labels'])}")
            print(f"║     발행 URL: {r.get('url')}")
            print(f"║     로컬파일: {r.get('local_html_path')}")
            print("╟" + "─" * 76 + "╢")
        print("╚" + "═" * 76 + "╝\n")

        return results

    def run_programmatic_asset_matrix(self, asset_keys: Optional[List[str]] = None, dry_run: bool = True) -> List[Dict[str, Any]]:
        """
        20대 핵심 자산군 프로그래매틱 Micro-SaaS 배치 발행 매트릭스
        미국 주식(NVDA, TSLA 등) + 크립토(BTC, ETH 등) + 절세계좌(ISA, 연금 등)
        """
        if not asset_keys:
            asset_keys = [
                "nvda_stock_tax",
                "tsla_water_averaging",
                "btc_futures_liquidation",
                "eth_futures_liquidation",
                "isa_tax_saving"
            ]

        print("\n" + "╔" + "═" * 76 + "╗")
        print("║   🏭 20대 핵심 자산 Programmatic Micro-SaaS Matrix 파이프라인 가동            ║")
        print(f"║   • 대상 자산 수 : {len(asset_keys)}개 자산                                                ║")
        print(f"║   • 실행 모드    : {'🟢 LIVE PRODUCTION' if not dry_run else '🟡 DRY-RUN (검증 모드)'}                           ║")
        print("╚" + "═" * 76 + "╝\n")

        results = []
        for idx, a_key in enumerate(asset_keys, 1):
            rule = self.resolver.rules.get(a_key, {})
            name = rule.get("name", a_key)
            print(f"\n[{idx}/{len(asset_keys)}] >>> 자산 '{name}' ({a_key}) 파이프라인 실행 중...")
            res = self.run_pipeline(user_topic_hint=name, dry_run=dry_run)
            results.append(res)
            if idx < len(asset_keys) and not dry_run:
                print(" -> Blogger API 속도 제한 방어를 위해 3초 대기 중...")
                time.sleep(3)

        return results

    def update_live_posts_batch(self) -> List[Dict[str, Any]]:
        """
        Blogger API의 posts().update()를 사용하여 기존 4대 라이브 포스트의 썸네일과 본문을 새 규격으로 덮어쓰기(Update)
        """
        print("\n" + "╔" + "═" * 76 + "╗")
        print("║   🔄 4대 핀테크 Micro-SaaS 기존 라이브 포스트 덮어쓰기 (Update Mode)         ║")
        print("║   • 썸네일 재캡처(CSS 핫픽스), 실시간 BEP 문구 및 수식 배지 반영             ║")
        print("╚" + "═" * 76 + "╝\n")

        # published_posts.json에서 기존 4개 포스트 ID 매핑
        history_file = os.path.join(BASE_DIR, "data", "published_posts.json")
        published_posts = []
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f:
                published_posts = json.load(f)

        rules_info = [
            ("overseas_stock_tax", "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터"),
            ("water_averaging_dca", "주식 코인 물타기 평단가 및 본전 탈출 역산 시뮬레이터"),
            ("leverage_liquidation_kelly", "선물 레버리지 청산가 및 켈리 공식 포지션 사이징 계산기"),
            ("dividend_compound_tax", "배당금 복리 재투자 및 금융소득종합과세 시뮬레이터")
        ]

        thumb_dir = os.path.join(BASE_DIR, "data", "thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)

        updated_results = []

        for idx, (r_key, default_title) in enumerate(rules_info, 1):
            # 대상 포스트 ID 및 URL 탐색
            target_post_id = None
            target_url = None
            for p in published_posts:
                p_id = str(p.get("id", ""))
                if p_id.startswith("sim-"):
                    continue
                p_title = p.get("title", "")
                if default_title in p_title or p_title in default_title or r_key in p.get("url", ""):
                    target_post_id = p_id
                    target_url = p.get("url")
                    break

            if not target_post_id:
                print(f"⚠️ [{idx}/4] '{default_title}'의 기존 Post ID를 찾지 못했습니다. 건너뜁니다.")
                continue

            resolved = self.resolver.resolve_topic(r_key)
            target_keyword = resolved["target_keyword"]
            post_labels = RULE_CATEGORY_LABELS.get(r_key, ["핀테크 계산기", "퀀트 유틸리티"])

            print(f"\n[{idx}/4] >>> Post ID: {target_post_id} ('{target_keyword}') 업데이트 중...")

            # 1. 썸네일 재캡처 (수정된 CSS & 문구 반영)
            thumb_filename = f"thumb_{r_key}"
            local_thumb_path = create_thumbnail_sync(
                filename=thumb_filename,
                title=target_keyword,
                formula_badge=resolved["formula_badge"],
                key_stat=resolved["key_stat"],
                sub_label=resolved["sub_label"],
                output_dir=thumb_dir
            )
            print(f" -> [Playwright] 고해상도 WebP 썸네일 재캡처 완료: {local_thumb_path}")

            upload_res = self.uploader.upload_image(local_thumb_path)
            hosted_thumb_url = upload_res.get("url")

            # 2. 본문 재조립
            fintech_widget = self.resolver.render_trading_saas_html(r_key)
            fintech_tables = self.resolver.render_trading_tables(r_key)
            monetization_cta = self.resolver.render_monetization_cta(r_key)
            internal_silo_links = self.resolver.render_internal_silo_links(r_key)
            legal_disclaimer = self.resolver.render_legal_disclaimer()

            complete_html = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "SoftwareApplication",
      "name": "{target_keyword}",
      "operatingSystem": "Any",
      "applicationCategory": "FinanceApplication",
      "offers": {{ "@type": "Offer", "price": "0" }}
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "{target_keyword}의 연산 원리는 무엇인가요?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{resolved.get('rule_info', {}).get('name', target_keyword)}의 공식을 기반으로 수학적 모델에 따라 0ms로 실시간 산출됩니다."
          }}
        }}
      ]
    }}
  ]
}}
</script>
<div style="max-width:880px; margin:0 auto; padding:12px; color:#f8fafc; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <h1 style="font-size:26px; font-weight:900; color:#f8fafc; margin-bottom:16px;">{target_keyword}</h1>
  <div style="background:#131c31; border:1px solid #1e293b; border-radius:12px; padding:16px; margin-bottom:24px;">
    <span style="background:#10b981; color:#0b0f19; font-size:11px; font-weight:800; padding:3px 8px; border-radius:4px;">핵심 요약</span>
    <p style="margin:8px 0 0 0; font-size:14px; color:#cbd5e1; line-height:1.6;">
      본 시뮬레이터는 최신 금융·세무 공식과 퀀트 알고리즘에 기반하여 오차 없는 정확한 수치를 0ms로 도출합니다. 복잡한 수식을 직접 계산할 필요 없이 입력값에 따라 즉시 최적의 결과를 확인하실 수 있습니다.
    </p>
  </div>
  {fintech_widget}
  {fintech_tables}
  {monetization_cta}
  {internal_silo_links}
  {legal_disclaimer}
</div>
"""
            # 로컬 파일 갱신
            local_html_path = os.path.join(BASE_DIR, "data", f"generated_{r_key}_microsaas.html")
            with open(local_html_path, "w", encoding="utf-8") as f:
                f.write(complete_html)

            # 3. Blogger API posts().update() 호출
            update_res = self.publisher.update_post(
                post_id=target_post_id,
                title=target_keyword,
                html_content=complete_html,
                thumbnail_url=hosted_thumb_url,
                keyword=target_keyword,
                labels=post_labels
            )
            updated_results.append({
                "rule_key": r_key,
                "post_id": target_post_id,
                "title": target_keyword,
                "url": update_res.get("url") or target_url,
                "local_html": local_html_path,
                "local_thumb": local_thumb_path,
                "status": update_res.get("status")
            })

            time.sleep(3)

        print("\n" + "╔" + "═" * 76 + "╗")
        print("║   🎉 4대 핵심 핀테크 포스트 Blogger 덮어쓰기(Update) 완료 리포트             ║")
        print("╠" + "═" * 76 + "╣")
        for i, r in enumerate(updated_results, 1):
            print(f"║ [{i}] {r['title']} (ID: {r['post_id']})")
            print(f"║     상태: {r['status']} | URL: {r['url']}")
            print("╟" + "─" * 76 + "╢")
        print("╚" + "═" * 76 + "╝\n")

        return updated_results


def run_interactive_menu(orchestrator: MicroSaaSPipelineOrchestrator):
    """더블클릭 또는 CLI 인자 없이 실행되었을 때 터미널 대화형 제어 센터 가동"""
    while True:
        print("\n" + "╔" + "═" * 76 + "╗")
        print("║   📈 Blogin 365 AI Holdings - FinTech Micro-SaaS Engine (v9.0 Apex)         ║")
        print("║   • 1호 도메인: 투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터        ║")
        print("╚" + "═" * 76 + "╝\n")
        print("  [1] 4대 핵심 계산기 일괄 실전 배포 (LIVE PRODUCTION - 4대장 연속 발행)")
        print("  [2] 1회 실전 무인 배포 (LIVE PRODUCTION - 단일 1건 실제 발행)")
        print("  [3] 안전 모의 실행 (DRY-RUN - 썸네일 생성, HTML 빌드, 샌드박스 QA 검증)")
        print("  [4] 특정 주제/키워드 직접 입력 실행 (Custom Topic Input)")
        print("  [5] 4대 무인 QA 패치 및 샌드박스 유닛 테스트 실행 (Test Suite)")
        print("  [6] 최근 발행된 포스트 목록 확인 (published_posts.json)")
        print("  [7] Google Blogger OAuth 토큰 재인증 (만료 해결)")
        print("  [8] 4대 라이브 포스트 최신 썸네일/수식 덮어쓰기 (Update Existing Live Posts)")
        print("  [9] 종료 (Exit)")
        print("─" * 78)

        try:
            choice = input("실행할 메뉴 번호를 선택하십시오 (1-9) [기본값: 1]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n프로그램을 종료합니다.")
            break

        if not choice:
            choice = "1"

        if choice == "1":
            try:
                orchestrator.run_batch_all_four(dry_run=False)
            except Exception as e:
                print(f"\n❌ 실행 에러 발생: {e}")
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "2":
            try:
                orchestrator.run_pipeline(dry_run=False)
            except Exception as e:
                print(f"\n❌ 실행 에러 발생: {e}")
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "3":
            try:
                orchestrator.run_batch_all_four(dry_run=True)
            except Exception as e:
                print(f"\n❌ 실행 에러 발생: {e}")
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "4":
            custom_hint = input("\n원하는 금융/세무 계산기 주제를 입력하십시오 (예: 코인 물타기 계산기): ").strip()
            if custom_hint:
                try:
                    orchestrator.run_pipeline(user_topic_hint=custom_hint, dry_run=False)
                except Exception as e:
                    print(f"\n❌ 실행 에러 발생: {e}")
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "5":
            import unittest
            print("\n[QA Engine] FinTech & Micro-SaaS 테스트 스위트 실행 중...")
            loader = unittest.TestLoader()
            suite = loader.discover("tests", pattern="test_*.py")
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "6":
            history_file = os.path.join(BASE_DIR, "data", "published_posts.json")
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as f:
                    posts = json.load(f)
                print(f"\n[발행 이력] 총 {len(posts)}개 포스트:")
                for idx, p in enumerate(posts[-10:], 1):
                    print(f" {idx}. [{p.get('published_at', 'N/A')}] {p.get('title')}")
                    print(f"    URL: {p.get('url')}")
            else:
                print("\n발행 이력 파일이 없습니다.")
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "7":
            from engine.crew.publisher import MicroSaaSBloggerPublisher
            pub = MicroSaaSBloggerPublisher()
            pub.authenticate(force_browser=True)
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "8":
            try:
                orchestrator.update_live_posts_batch()
            except Exception as e:
                print(f"\n❌ 실행 에러 발생: {e}")
            input("\n메뉴로 돌아가려면 엔터를 누르십시오...")

        elif choice == "9":
            print("\n시스템을 종료합니다. 감사합니다.")
            break
        else:
            print("올바른 번호를 입력하십시오.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FinTech Micro-SaaS Crew Pipeline Orchestrator")
    parser.add_argument("--once", action="store_true", help="1회 즉시 실행 (Live)")
    parser.add_argument("--dry-run", action="store_true", help="안전 모의 실행 (No Publish)")
    parser.add_argument("--batch", action="store_true", help="4대 금융 계산기 일괄 연속 배포")
    parser.add_argument("--matrix", action="store_true", help="20대 자산 프로그래매틱 Micro-SaaS 매트릭스 일괄 배포")
    parser.add_argument("--assets", type=str, default=None, help="매트릭스 대상 자산 키 목록 (콤마 구분)")
    parser.add_argument("--update", action="store_true", help="기존 4대 라이브 포스트 덮어쓰기(Update)")
    parser.add_argument("--topic", type=str, default="2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터", help="주제 힌트")
    parser.add_argument("--menu", action="store_true", help="대화형 메뉴 모드 강제 실행")
    args = parser.parse_args()

    orchestrator = MicroSaaSPipelineOrchestrator()

    if args.matrix:
        target_assets = [a.strip() for a in args.assets.split(",")] if args.assets else None
        orchestrator.run_programmatic_asset_matrix(asset_keys=target_assets, dry_run=args.dry_run)
    elif args.update:
        orchestrator.update_live_posts_batch()
    elif args.batch:
        orchestrator.run_batch_all_four(dry_run=args.dry_run)
    elif args.once:
        orchestrator.run_pipeline(user_topic_hint=args.topic, dry_run=False)
    elif args.dry_run:
        orchestrator.run_pipeline(user_topic_hint=args.topic, dry_run=True)
    else:
        run_interactive_menu(orchestrator)
