# -*- coding: utf-8 -*-
"""
engine/analytics/feedback_loop.py
---------------------------------
Closed-Loop Feedback & Weight Tuner Subsystem (Pillar 2).
Connects published post performance back into the Demand Matcher:
1. Ingests GSC (impressions, clicks, CTR, position) & AdSense / CPA conversion data.
2. Tracks PVS accuracy ratio (Actual Revenue / Estimated PVS).
3. Automatically tunes category multipliers in data/niche_weights.json.
4. Supplies tuned scoring weights to DemandMatcher so high-ROI topics are automatically boosted.
"""

import os
import sys
import json
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class FeedbackLoop:
    """
    Manages performance metric tracking and autonomous machine-learning style
    feedback weight tuning for the Blogin 365 AI pipeline.
    """
    DEFAULT_WEIGHTS = {
        "TECH": 1.0,
        "SUBSIDY": 1.15,
        "SAVINGS": 1.10,
        "CASHFLOW": 1.05,
        "MEDICAL": 1.0,
        "CAREER": 1.0,
        "LIFESTYLE": 1.0
    }

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            self.data_dir = os.path.join(BASE_DIR, "data")
        else:
            self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

        self.metrics_file = os.path.join(self.data_dir, "performance_metrics.json")
        self.weights_file = os.path.join(self.data_dir, "niche_weights.json")
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.weights_file):
            with open(self.weights_file, "w", encoding="utf-8") as f:
                json.dump({
                    "version": "1.0",
                    "last_tuned": datetime.now().isoformat(),
                    "category_weights": self.DEFAULT_WEIGHTS
                }, f, ensure_ascii=False, indent=2)

        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump({
                    "posts": {},
                    "summary": {
                        "total_impressions": 0,
                        "total_clicks": 0,
                        "total_conversions": 0,
                        "total_actual_revenue": 0.0,
                        "average_ctr": 0.0,
                        "average_pvs_accuracy": 1.0
                    }
                }, f, ensure_ascii=False, indent=2)

    def load_metrics(self) -> Dict[str, Any]:
        try:
            with open(self.metrics_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            self._ensure_files()
            with open(self.metrics_file, "r", encoding="utf-8") as f:
                return json.load(f)

    def load_weights(self) -> Dict[str, float]:
        try:
            with open(self.weights_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("category_weights", self.DEFAULT_WEIGHTS)
        except Exception:
            return self.DEFAULT_WEIGHTS.copy()

    def get_category_weight(self, category: str) -> float:
        weights = self.load_weights()
        return weights.get(category.upper(), 1.0)

    def record_post_metric(
        self,
        post_id: str,
        keyword: str,
        category: str,
        impressions: int,
        clicks: int,
        conversions: int,
        affiliate_rev: float,
        adsense_rev: float,
        est_pvs: float,
        dwell_time_sec: float = 125.0
    ) -> Dict[str, Any]:
        """
        Records or updates performance telemetry for a single post.
        """
        metrics_data = self.load_metrics()
        posts = metrics_data.setdefault("posts", {})

        actual_rev = round(affiliate_rev + adsense_rev, 2)
        ctr = round((clicks / max(impressions, 1)) * 100, 2)
        cvr = round((conversions / max(clicks, 1)) * 100, 2)
        accuracy = round(actual_rev / max(est_pvs, 1.0), 3)

        cat_clean = str(category or "LIFESTYLE").upper()
        post_record = {
            "post_id": post_id,
            "keyword": keyword,
            "category": cat_clean,
            "updated_at": datetime.now().isoformat(),
            "impressions": impressions,
            "clicks": clicks,
            "ctr_percent": ctr,
            "conversions": conversions,
            "cvr_percent": cvr,
            "affiliate_revenue": affiliate_rev,
            "adsense_revenue": adsense_rev,
            "actual_revenue": actual_rev,
            "estimated_pvs": est_pvs,
            "pvs_accuracy_ratio": accuracy,
            "dwell_time_sec": dwell_time_sec
        }

        posts[post_id] = post_record
        self._update_summary(metrics_data)
        
        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, ensure_ascii=False, indent=2)

        return post_record

    def simulate_performance_sync(
        self,
        post_id: str,
        keyword: str,
        category: str,
        est_pvs: float
    ) -> Dict[str, Any]:
        """
        Simulates Search Console & AdSense data collection for newly published posts
        or dry-run verification.
        """
        # Realistic simulation: high-dwell Micro-SaaS generates 3.8% ~ 7.2% CTR
        impressions = random.randint(1200, 4800)
        ctr = round(random.uniform(3.5, 6.8), 2)
        clicks = int(impressions * (ctr / 100.0))
        conversions = max(1, int(clicks * random.uniform(0.018, 0.045)))
        
        affiliate_rev = round(conversions * random.randint(15000, 38000), 2)
        adsense_rev = round((impressions / 1000.0) * random.uniform(8.0, 16.0) * 1350, 2)
        dwell_time = round(random.uniform(110.0, 195.0), 1)

        return self.record_post_metric(
            post_id=post_id,
            keyword=keyword,
            category=category,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            affiliate_rev=affiliate_rev,
            adsense_rev=adsense_rev,
            est_pvs=est_pvs,
            dwell_time_sec=dwell_time
        )

    def tune_niche_weights(self) -> Dict[str, Any]:
        """
        Analyzes historical performance across niches and dynamically updates category weights.
        - High CTR / High conversion categories receive boost.
        - Low engagement categories receive penalty.
        - Bases updates relative to baseline DEFAULT_WEIGHTS to prevent runaway compounding.
        """
        metrics_data = self.load_metrics()
        posts = metrics_data.get("posts", {})
        baseline_weights = self.DEFAULT_WEIGHTS.copy()

        if not posts:
            return {
                "tuned_weights": baseline_weights,
                "message": "No historical posts found, using default weights."
            }

        # Group stats by category
        cat_stats: Dict[str, Dict[str, Any]] = {}
        for p in posts.values():
            cat = p.get("category", "LIFESTYLE")
            if cat not in cat_stats:
                cat_stats[cat] = {"impressions": 0, "clicks": 0, "conversions": 0, "rev": 0.0, "count": 0}
            cat_stats[cat]["impressions"] += p.get("impressions", 0)
            cat_stats[cat]["clicks"] += p.get("clicks", 0)
            cat_stats[cat]["conversions"] += p.get("conversions", 0)
            cat_stats[cat]["rev"] += p.get("actual_revenue", 0.0)
            cat_stats[cat]["count"] += 1

        tuned = baseline_weights.copy()
        adjustments = {}

        for cat, stats in cat_stats.items():
            tot_imp = stats["impressions"]
            tot_clicks = stats["clicks"]
            avg_ctr = (tot_clicks / max(tot_imp, 1)) * 100.0
            avg_rev = stats["rev"] / max(stats["count"], 1)

            # Base weight is taken from DEFAULT_WEIGHTS baseline to prevent exponential runaway
            base_w = self.DEFAULT_WEIGHTS.get(cat, 1.0)
            multiplier = 1.0

            # Boost conditions
            if avg_ctr >= 5.0 or avg_rev >= 30000:
                multiplier = 1.15
            elif avg_ctr >= 4.0:
                multiplier = 1.05
            # Penalty condition
            elif avg_ctr < 2.0 and tot_imp >= 500:
                multiplier = 0.90

            new_w = round(max(0.4, min(2.5, base_w * multiplier)), 3)
            tuned[cat] = new_w
            adjustments[cat] = {
                "baseline_weight": base_w,
                "tuned_weight": new_w,
                "factor": multiplier,
                "avg_ctr": round(avg_ctr, 2),
                "avg_revenue": round(avg_rev, 2)
            }

        # Persist updated weights
        with open(self.weights_file, "w", encoding="utf-8") as f:
            json.dump({
                "version": "1.0",
                "last_tuned": datetime.now().isoformat(),
                "category_weights": tuned,
                "adjustments": adjustments
            }, f, ensure_ascii=False, indent=2)

        return {
            "tuned_weights": tuned,
            "adjustments": adjustments,
            "total_analyzed_posts": len(posts)
        }

    def _update_summary(self, metrics_data: Dict[str, Any]):
        posts = metrics_data.get("posts", {})
        if not posts:
            return

        tot_imp = sum(p.get("impressions", 0) for p in posts.values())
        tot_clicks = sum(p.get("clicks", 0) for p in posts.values())
        tot_conv = sum(p.get("conversions", 0) for p in posts.values())
        tot_rev = sum(p.get("actual_revenue", 0.0) for p in posts.values())
        avg_ctr = round((tot_clicks / max(tot_imp, 1)) * 100.0, 2)
        avg_acc = round(sum(p.get("pvs_accuracy_ratio", 1.0) for p in posts.values()) / max(len(posts), 1), 3)

        metrics_data["summary"] = {
            "total_posts_tracked": len(posts),
            "total_impressions": tot_imp,
            "total_clicks": tot_clicks,
            "total_conversions": tot_conv,
            "total_actual_revenue": round(tot_rev, 2),
            "average_ctr": avg_ctr,
            "average_pvs_accuracy": avg_acc,
            "last_updated": datetime.now().isoformat()
        }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    fb = FeedbackLoop()
    # Test record & simulation
    rec = fb.simulate_performance_sync("post-test-1", "2026 청년도약계좌", "SUBSIDY", est_pvs=10980000)
    tuning = fb.tune_niche_weights()
    print("=== Feedback Loop Test ===")
    print("Simulated metric recorded:", rec["post_id"], "CTR:", rec["ctr_percent"], "%")
    print("Tuned weights:", tuning["tuned_weights"])
