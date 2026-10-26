# -*- coding: utf-8 -*-
"""
engine/analytics/unit_economics.py
----------------------------------
Blogin 365 AI Holdings - Unit Economics & 1,000-Page BEP Reverse Calculator (v9.0 Apex).
[철칙 5-1] 1,000페이지 발행당 총 API/호스팅 원가($5~$15) 대비 목표 RPM($35~$50) 및 손익분기점(BEP) 실시간 산출.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

COMPANY_LOGS_PATH = os.path.join(BASE_DIR, "data", "company_logs.json")


class UnitEconomicsCalculator:
    """
    단위 경제성(Unit Economics) 및 손익분기점(BEP) 역산기.
    - 1,000페이지 생성 원가(Gemini Flash API + Crawl4AI + 인프라) 대비
      색인율, CTR, 목표 RPM을 대입하여 정확한 손익분기 도달 일수를 산출.
    """

    # 1,000-Page Standard Economic Parameters
    COST_PER_INPUT_TOKEN = 0.075 / 1_000_000   # Gemini Flash $0.075 / 1M tokens
    COST_PER_OUTPUT_TOKEN = 0.30 / 1_000_000   # Gemini Flash $0.30 / 1M tokens
    AVG_INPUT_TOKENS_PER_POST = 3200           # Editorial context + 1st party facts
    AVG_OUTPUT_TOKENS_PER_POST = 2400          # 8-block Apolia content JSON
    AMORTIZED_INFRA_PER_1000 = 5.00            # Domain, storage, indexer overhead ($5.00)

    DEFAULT_TARGET_RPM = 38.50                 # Conservative Blend (AdSense $15 + CPA/CSE $23.5)
    DEFAULT_INDEX_RATE = 0.85                  # 85% Google Search Console target indexing
    DEFAULT_MONTHLY_IMPR_PER_PAGE = 380        # Median organic search impressions per long-tail
    DEFAULT_CTR = 0.024                        # 2.4% Click-Through Rate
    KRW_USD_RATE = 1380.0                      # Standard currency conversion

    def __init__(self, logs_path: str = COMPANY_LOGS_PATH):
        self.logs_path = logs_path

    def calculate_cost_per_page(self) -> Dict[str, float]:
        """Calculates exact API and compute cost per single published page."""
        api_input_cost = self.AVG_INPUT_TOKENS_PER_POST * self.COST_PER_INPUT_TOKEN
        api_output_cost = self.AVG_OUTPUT_TOKENS_PER_POST * self.COST_PER_OUTPUT_TOKEN
        api_total_usd = api_input_cost + api_output_cost
        infra_usd = self.AMORTIZED_INFRA_PER_1000 / 1000.0
        total_usd = api_total_usd + infra_usd

        return {
            "api_input_usd": round(api_input_cost, 6),
            "api_output_usd": round(api_output_cost, 6),
            "api_total_usd": round(api_total_usd, 6),
            "infra_usd": round(infra_usd, 6),
            "total_usd": round(total_usd, 5),
            "total_krw": round(total_usd * self.KRW_USD_RATE, 2)
        }

    def simulate_1000_page_batch(
        self,
        batch_size: int = 1000,
        target_rpm: float = DEFAULT_TARGET_RPM,
        index_rate: float = DEFAULT_INDEX_RATE,
        ctr: float = DEFAULT_CTR
    ) -> Dict[str, Any]:
        """
        [철칙 5-1] 1,000페이지 배치 시뮬레이션 및 BEP 역산.
        """
        page_cost = self.calculate_cost_per_page()
        total_batch_cost_usd = page_cost["total_usd"] * batch_size
        total_batch_cost_krw = total_batch_cost_usd * self.KRW_USD_RATE

        indexed_pages = int(batch_size * index_rate)
        monthly_total_impressions = indexed_pages * self.DEFAULT_MONTHLY_IMPR_PER_PAGE
        monthly_clicks = int(monthly_total_impressions * ctr)
        monthly_revenue_usd = (monthly_clicks / 1000.0) * target_rpm
        monthly_revenue_krw = monthly_revenue_usd * self.KRW_USD_RATE

        # Daily Recurring Revenue (DRR) after indexing stabilization (typically Day 14)
        daily_revenue_usd = monthly_revenue_usd / 30.0
        daily_revenue_krw = monthly_revenue_krw / 30.0

        # Days to achieve break-even on the batch creation cost
        days_to_bep = round(total_batch_cost_usd / max(0.01, daily_revenue_usd), 1)
        annual_roi_percent = round(((monthly_revenue_usd * 12 - total_batch_cost_usd) / max(1.0, total_batch_cost_usd)) * 100, 1)

        return {
            "timestamp": datetime.now().isoformat(),
            "batch_size": batch_size,
            "cost_breakdown": {
                "cost_per_page_usd": page_cost["total_usd"],
                "cost_per_page_krw": page_cost["total_krw"],
                "total_batch_cost_usd": round(total_batch_cost_usd, 2),
                "total_batch_cost_krw": round(total_batch_cost_krw, 0)
            },
            "performance_projection": {
                "target_rpm": target_rpm,
                "index_rate_percent": round(index_rate * 100, 1),
                "indexed_pages": indexed_pages,
                "monthly_impressions": monthly_total_impressions,
                "monthly_clicks": monthly_clicks,
                "monthly_revenue_usd": round(monthly_revenue_usd, 2),
                "monthly_revenue_krw": round(monthly_revenue_krw, 0),
                "daily_revenue_usd": round(daily_revenue_usd, 2),
                "daily_revenue_krw": round(daily_revenue_krw, 0)
            },
            "bep_metrics": {
                "days_to_bep_post_indexing": days_to_bep,
                "first_year_roi_percent": annual_roi_percent,
                "unit_economic_health": "ULTRA_HIGH_MARGIN" if annual_roi_percent > 1000 else "HEALTHY"
            }
        }

    def record_to_company_logs(self, metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Appends the unit economics audit to data/company_logs.json."""
        if metrics is None:
            metrics = self.simulate_1000_page_batch()

        logs = {}
        if os.path.exists(self.logs_path):
            try:
                with open(self.logs_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except Exception:
                logs = {}

        logs.setdefault("unit_economics_history", []).append(metrics)
        logs["latest_unit_economics"] = metrics

        os.makedirs(os.path.dirname(self.logs_path), exist_ok=True)
        with open(self.logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        return metrics

    def print_executive_report(self):
        """Prints a high-impact executive unit economics breakdown."""
        metrics = self.simulate_1000_page_batch()
        print("\n" + "=" * 65)
        print("📊 [Blogin 365 AI] 1,000-Page Unit Economics & BEP Report (v9.0 Apex)")
        print("=" * 65)
        cb = metrics["cost_breakdown"]
        pj = metrics["performance_projection"]
        bp = metrics["bep_metrics"]

        print(f"• 1개 포스트 생성 원가 : ${cb['cost_per_page_usd']:.4f} (약 {cb['cost_per_page_krw']:,.1f}원)")
        print(f"• 1,000개 배치 총 원가 : ${cb['total_batch_cost_usd']:,.2f} (약 {cb['total_batch_cost_krw']:,.0f}원)")
        print("-" * 65)
        print(f"• 목표 RPM             : ${pj['target_rpm']:.2f} (AdSense + CPA + CSE 통합)")
        print(f"• 예상 색인율 (GSC)    : {pj['index_rate_percent']}% ({pj['indexed_pages']}개 색인 완료)")
        print(f"• 월간 예상 유입 트래픽: {pj['monthly_clicks']:,} Clicks (노출 {pj['monthly_impressions']:,}회)")
        print(f"• 월간 예상 순매출     : ${pj['monthly_revenue_usd']:,.2f} (약 {pj['monthly_revenue_krw']:,.0f}원/월)")
        print("-" * 65)
        print(f"• 손익분기점(BEP) 도달 : 색인 완료 후 단 {bp['days_to_bep_post_indexing']}일!")
        print(f"• 1차년도 연간 ROI     : +{bp['first_year_roi_percent']:,}% ({bp['unit_economic_health']})")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    calc = UnitEconomicsCalculator()
    calc.print_executive_report()
    calc.record_to_company_logs()
