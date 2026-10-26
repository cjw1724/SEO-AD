# -*- coding: utf-8 -*-
"""
engine/maintenance/batch_pruner.py
----------------------------------
Blogin 365 AI Holdings - 21-Day Batch & Pruning Self-Healing Engine (v9.0 Apex).
[철칙 5-2] 21-Day Batch & Pruning Protocol:
1. 1차: 50~100건 배치 발행 후 14일간 Google Search Console API로 색인율 85% 이상 확인.
2. 2차: 발행 21일 후 노출은 발생하나 클릭이 없는 포스트는 제목 및 H2 결론부를 자동 리라이팅(Self-Healing)하고,
   노출조차 없는 저품질 포스트는 자동 가지치기(Pruning)하여 크롤링 예산을 회수.
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

PRUNER_STATE_PATH = os.path.join(BASE_DIR, "data", "pruner_state.json")
COMPANY_LOGS_PATH = os.path.join(BASE_DIR, "data", "company_logs.json")

from engine.agents.prompts_chat_pack import APEX_STAFF_PROMPTS, get_staff_prompt

CS_PUBLISHER_PROMPT = get_staff_prompt("08_CSPublisher")


class BatchPrunerEngine:
    """
    21일 수명주기 무인 감사 및 자가치유/가지치기 오케스트레이터.
    - 검색엔진 크롤링 예산(Crawl Budget) 낭비를 방지하고
      죽은 문서(Deadweight Pages)의 트래픽 전환율을 기계적으로 부활.
    """

    THRESHOLD_MATURITY_DAYS = 21   # 21 days after initial publication
    INDEXING_CHECK_DAYS = 14       # 14 days indexing milestone
    MIN_HEALTHY_CTR = 0.015        # 1.5% CTR minimum healthy bar
    MIN_IMPRESSIONS = 40           # Baseline impressions to evaluate CTR

    def __init__(self, state_path: str = PRUNER_STATE_PATH):
        self.state_path = state_path
        self._ensure_state_file()

    def _ensure_state_file(self):
        if not os.path.exists(self.state_path):
            os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
            initial = {
                "last_run": None,
                "posts_evaluated": 0,
                "pruned_count": 0,
                "self_healed_count": 0,
                "winner_count": 0,
                "monitored_posts": {},
                "action_history": []
            }
            with open(self.state_path, "w", encoding="utf-8") as f:
                json.dump(initial, f, ensure_ascii=False, indent=2)

    def load_state(self) -> Dict[str, Any]:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "last_run": None,
                "posts_evaluated": 0,
                "pruned_count": 0,
                "self_healed_count": 0,
                "winner_count": 0,
                "monitored_posts": {},
                "action_history": []
            }

    def save_state(self, state: Dict[str, Any]):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def register_published_post(self, post_id: str, title: str, keyword: str, category: str, url: str):
        """Registers a newly published post for 14-day and 21-day lifecycle monitoring."""
        state = self.load_state()
        posts = state.setdefault("monitored_posts", {})
        now_str = datetime.now().isoformat()

        posts[post_id] = {
            "post_id": post_id,
            "title": title,
            "keyword": keyword,
            "category": category,
            "url": url,
            "published_at": now_str,
            "indexed_status": "PENDING_CHECK",
            "impressions": 0,
            "clicks": 0,
            "lifecycle_status": "MATURING",  # MATURING -> HEALTHY / REWRITE_NEEDED / PRUNE_CANDIDATE
            "revisions_count": 0
        }
        self.save_state(state)

    def evaluate_post(self, post_data: Dict[str, Any], current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        [철칙 5-2] 포스트 수명주기 및 의사결정 판정 로직:
        1. 14일 미만: 색인 유예 기간 (MATURING)
        2. 21일 도달 후:
           - Impressions >= 40 & Clicks == 0 or CTR < 1.0%: REWRITE_NEEDED (제목 훅 자가치유)
           - Impressions == 0 & Clicks == 0: PRUNE_CANDIDATE (크롤링 예산 회수 가지치기)
           - CTR >= 1.5%: WINNER (트래픽 캐시카우)
        """
        now = current_time or datetime.now()
        pub_date_str = post_data.get("published_at")
        if not pub_date_str:
            age_days = 0
        else:
            try:
                pub_date = datetime.fromisoformat(pub_date_str)
                age_days = (now - pub_date).days
            except Exception:
                age_days = 0

        impr = post_data.get("impressions", 0)
        clicks = post_data.get("clicks", 0)
        ctr = (clicks / max(1, impr)) if impr > 0 else 0.0

        decision = "MATURING"
        action = "WAIT"
        reason = f"발행 {age_days}일차 (14~21일 숙성 관찰 기간)"

        if age_days >= self.THRESHOLD_MATURITY_DAYS:
            if impr >= self.MIN_IMPRESSIONS and (clicks == 0 or ctr < 0.010):
                decision = "REWRITE_NEEDED"
                action = "SELF_HEAL"
                reason = f"고노출({impr}회) 대비 무클릭(CTR {ctr*100:.1f}%) -> 제목 및 H2 결론부 긴급 자가치유 권고"
            elif impr < 5 and clicks == 0:
                decision = "PRUNE_CANDIDATE"
                action = "PRUNE"
                reason = f"발행 {age_days}일 경과 후에도 노출 전무(노출 {impr}회) -> 크롤링 예산 회수를 위한 가지치기 권고"
            elif ctr >= self.MIN_HEALTHY_CTR:
                decision = "WINNER"
                action = "BOOST"
                reason = f"정상 상위 랭킹 안착 (노출 {impr}회, 클릭 {clicks}회, CTR {ctr*100:.1f}%)"
            else:
                decision = "NEUTRAL"
                action = "MONITOR"
                reason = f"지속 관찰 (CTR {ctr*100:.1f}%)"

        return {
            "post_id": post_data.get("post_id"),
            "title": post_data.get("title"),
            "keyword": post_data.get("keyword"),
            "age_days": age_days,
            "impressions": impr,
            "clicks": clicks,
            "ctr": round(ctr, 4),
            "decision": decision,
            "action": action,
            "reason": reason
        }

    def generate_self_healing_title(self, original_title: str, keyword: str) -> str:
        """
        Creates an aggressive high-CTR curiosity gap hook title to revive low-CTR posts.
        """
        clean_kw = re.sub(r'^\d{4}\s*', '', keyword).strip()
        hooks = [
            f"{clean_kw} 견적서 열어보고 손해 본 3가지 팩트 (2026 심평원 실측)",
            f"{clean_kw} 아직도 정가 내시나요? 1원 단위 숨은 환급 총정리",
            f"병원에서 절대 먼저 말 안 해주는 {clean_kw} 진짜 현실 단가표",
            f"{clean_kw} 수술 전 꼭 봐야 할 3개년 누적 비용 계산기 대조"
        ]
        # Return candidate distinct from current title
        for h in hooks:
            if h != original_title:
                return h
        return hooks[0]

    def scan_all_posts(self, simulated_metrics: Optional[Dict[str, Dict[str, int]]] = None) -> Dict[str, Any]:
        """
        Scans all monitored posts and executes the 21-day Batch & Pruning Protocol.
        """
        state = self.load_state()
        posts = state.get("monitored_posts", {})
        results = []
        healed_count = 0
        pruned_count = 0
        winner_count = 0

        for pid, pdata in posts.items():
            # Inject simulated telemetry if provided
            if simulated_metrics and pid in simulated_metrics:
                pdata["impressions"] = simulated_metrics[pid].get("impressions", pdata.get("impressions", 0))
                pdata["clicks"] = simulated_metrics[pid].get("clicks", pdata.get("clicks", 0))

            evaluation = self.evaluate_post(pdata)
            results.append(evaluation)

            if evaluation["action"] == "SELF_HEAL":
                healed_count += 1
                new_title = self.generate_self_healing_title(pdata["title"], pdata["keyword"])
                evaluation["recommended_new_title"] = new_title
            elif evaluation["action"] == "PRUNE":
                pruned_count += 1
            elif evaluation["action"] == "BOOST":
                winner_count += 1

        state["last_run"] = datetime.now().isoformat()
        state["posts_evaluated"] = len(posts)
        state["pruned_count"] = pruned_count
        state["self_healed_count"] = healed_count
        state["winner_count"] = winner_count
        self.save_state(state)

        return {
            "timestamp": datetime.now().isoformat(),
            "total_monitored": len(posts),
            "self_heal_candidates": healed_count,
            "prune_candidates": pruned_count,
            "winner_posts": winner_count,
            "evaluations": results
        }


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    pruner = BatchPrunerEngine()

    # Seed sample posts for verification if empty
    test_state = pruner.load_state()
    if not test_state.get("monitored_posts"):
        past_25_days = (datetime.now() - timedelta(days=25)).isoformat()
        past_10_days = (datetime.now() - timedelta(days=10)).isoformat()
        
        pruner.register_published_post("post_sample_1", "3000모 모발이식 가격 및 견적서", "3000모 모발이식 가격", "HAIR", "https://blogin365ai.blogspot.com/post1")
        pruner.register_published_post("post_sample_2", "청년도약계좌 지원금 총정리", "2026 청년도약계좌", "SUBSIDY", "https://blogin365ai.blogspot.com/post2")
        pruner.register_published_post("post_sample_3", "알뜰폰 무제한 요금제 비교", "알뜰폰 요금제 비교", "SAVINGS", "https://blogin365ai.blogspot.com/post3")

        # Manually mature for verification test
        state = pruner.load_state()
        state["monitored_posts"]["post_sample_1"]["published_at"] = past_25_days
        state["monitored_posts"]["post_sample_1"]["impressions"] = 120
        state["monitored_posts"]["post_sample_1"]["clicks"] = 0  # High impr, zero click -> Self-heal!

        state["monitored_posts"]["post_sample_2"]["published_at"] = past_25_days
        state["monitored_posts"]["post_sample_2"]["impressions"] = 0
        state["monitored_posts"]["post_sample_2"]["clicks"] = 0  # 0 impr -> Prune!

        state["monitored_posts"]["post_sample_3"]["published_at"] = past_25_days
        state["monitored_posts"]["post_sample_3"]["impressions"] = 250
        state["monitored_posts"]["post_sample_3"]["clicks"] = 8  # CTR 3.2% -> Winner!
        pruner.save_state(state)

    report = pruner.scan_all_posts()
    print("\n" + "=" * 65)
    print("✂️ [Blogin 365 AI] 21-Day Batch & Pruning Protocol Report (v9.0 Apex)")
    print("=" * 65)
    print(f"• 총 모니터링 포스트 : {report['total_monitored']}건")
    print(f"• 자가치유 대상 (Self-Heal): {report['self_heal_candidates']}건 (노출 대비 저클릭 개선)")
    print(f"• 가지치기 대상 (Prune)    : {report['prune_candidates']}건 (크롤링 예산 회수)")
    print(f"• 상위 안착 포스트 (Winner)  : {report['winner_posts']}건 (트래픽 캐시카우)")
    print("-" * 65)
    for ev in report["evaluations"]:
        print(f"[{ev['action']}] {ev['title'][:32]}... | 노출: {ev['impressions']}, 클릭: {ev['clicks']} -> {ev['reason']}")
    print("=" * 65 + "\n")
