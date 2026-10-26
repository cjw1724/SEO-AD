# -*- coding: utf-8 -*-
"""
engine/matcher/topic_cluster_engine.py
---------------------------------------
Blogin 365 AI Holdings - 30-Day Topic Cluster & Autonomous Portfolio Manager (v8.0 Apex).
[철칙 1] 단발성 키워드 영구 금지 & 30-Day 토픽 클러스터(Topic Cluster) 독점
- 5대 골든 니치(모발이식, 정부지원금, 고정비 절감, 비급여 의료, 국비지원 자격증) 전 영역 30-Day 지식 그래프 상시 구비.
- 자율 포트폴리오 관리자(Autonomous Portfolio Manager)가 PVS 수익 속도와 30일 완주 상태에 따라 무인 자율 선택·순환·발행.
- 중간 이탈 영구 금지: 30일 수명주기 완주 전까지 해당 니치를 그물망(Interlinking Mesh)으로 완전 독점.
- 30일 완주 시 최고 수익성 미완료 니치 클러스터로 자동 승계 및 다음 30일 사이클 자율 개시.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.matcher.topic_clusters import (
    ALL_CLUSTERS,
    CATEGORY_TO_CLUSTER_MAP,
    HAIR_TRANSPLANT_CLUSTER,
    GOVERNMENT_SUBSIDY_CLUSTER,
    CASHFLOW_HACKS_CLUSTER,
    MEDICAL_WELLNESS_CLUSTER,
    CAREER_CERT_CLUSTER
)
from engine.agents.prompts_chat_pack import APEX_STAFF_PROMPTS, get_staff_prompt
from engine.matcher.semantic_cannibalization_engine import LocalSemanticVectorizer

CHIEF_OF_STAFF_PROMPT = get_staff_prompt("01_ChiefOfStaff")
PRODUCT_PLANNER_PROMPT = get_staff_prompt("02_ProductPlanner")

STATE_FILE_PATH = os.path.join(BASE_DIR, "data", "topic_cluster_state.json")
NICHE_WEIGHTS_PATH = os.path.join(BASE_DIR, "data", "niche_weights.json")
HIGH_CPC_PATH = os.path.join(BASE_DIR, "data", "high_cpc_keywords.json")


class AutonomousClusterPortfolioManager:
    """
    무인 AI 기업 지주회사 자율 클러스터 포트폴리오 매니저 (v8.0 Apex).
    - 5대 골든 니치 포트폴리오의 생애주기(0% -> 100%) 및 PVS v2.0 수익 속도를 기계적으로 평가.
    - 사람의 개입 없이 최적의 니치 클러스터를 자율 선택하고, 30일 완주 시 차기 니치로 자동 로테이션.
    """

    def __init__(self, state_file: str = STATE_FILE_PATH):
        self.state_file = state_file
        self._ensure_state_file()

    def _ensure_state_file(self):
        if not os.path.exists(self.state_file):
            initial_state = {
                "active_cluster_id": "hair_transplant",
                "current_day": 1,
                "total_published_in_cluster": 0,
                "cluster_progress": {
                    cid: {
                        "cluster_name": cdata["cluster_name"],
                        "current_day": 1,
                        "total_published": 0,
                        "status": "ACTIVE" if cid == "hair_transplant" else "QUEUED",
                        "completed_cycles": 0
                    }
                    for cid, cdata in ALL_CLUSTERS.items()
                },
                "history": []
            }
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(initial_state, f, ensure_ascii=False, indent=2)
        else:
            # Upgrade existing state if missing new clusters
            state = self.load_state()
            progress = state.get("cluster_progress", {})
            updated = False
            for cid, cdata in ALL_CLUSTERS.items():
                if cid not in progress:
                    progress[cid] = {
                        "cluster_name": cdata["cluster_name"],
                        "current_day": 1,
                        "total_published": 0,
                        "status": "QUEUED",
                        "completed_cycles": 0
                    }
                    updated = True
            if updated or "cluster_progress" not in state:
                state["cluster_progress"] = progress
                self.save_state(state)

    def load_state(self) -> Dict[str, Any]:
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "active_cluster_id": "hair_transplant",
                "current_day": 1,
                "total_published_in_cluster": 0,
                "cluster_progress": {},
                "history": []
            }

    def save_state(self, state: Dict[str, Any]):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def calculate_cluster_priority(self, cluster_id: str) -> float:
        """
        PVS v2.0 및 CPC x CPA 기대 수익 점수 계산:
        Score = (CPC * 0.35) + (Avg_Payout * 0.45) + (Weight * 1000 * 0.20)
        """
        cluster = ALL_CLUSTERS.get(cluster_id, {})
        base_cpc = cluster.get("cpc", 3000)
        avg_payout = cluster.get("avg_payout", 20000)

        # Load feedback weights if available
        weight = 1.0
        try:
            if os.path.exists(NICHE_WEIGHTS_PATH):
                with open(NICHE_WEIGHTS_PATH, "r", encoding="utf-8") as f:
                    weights = json.load(f)
                    weight = weights.get(cluster_id, 1.0)
        except Exception:
            weight = 1.0

        score = (base_cpc * 0.35) + (avg_payout * 0.45) + (weight * 1000 * 0.20)
        return round(score, 2)

    def auto_select_active_cluster(self) -> Dict[str, Any]:
        """
        자율 클러스터 포트폴리오 거버넌스:
        1. 철칙 1 준수: 현재 활성 클러스터가 30일 이하라면 절대 이탈 금지 (중간 도망 방지).
        2. 30일 완주(Day > 30) 시:
           - 현재 클러스터를 'COMPLETED' 처리 및 완료 주기(completed_cycles) +1.
           - 완료 주기수가 가장 적고 PVS 수익 점수가 가장 높은 차기 골든 니치를 자동 선택.
           - 차기 니치를 활성화하고 Day 1로 자동 리셋하여 30-Day 독점 사이클 자율 개시.
        """
        state = self.load_state()
        active_id = state.get("active_cluster_id", "hair_transplant")
        current_day = state.get("current_day", 1)
        progress = state.get("cluster_progress", {})

        # Ensure active cluster data is in progress dict
        if active_id not in progress:
            progress[active_id] = {
                "cluster_name": ALL_CLUSTERS[active_id]["cluster_name"],
                "current_day": current_day,
                "total_published": state.get("total_published_in_cluster", 0),
                "status": "ACTIVE",
                "completed_cycles": 0
            }

        # Case 1: In-progress 30-day cluster (철칙 1 엄수)
        if current_day <= 30:
            progress[active_id]["status"] = "ACTIVE"
            progress[active_id]["current_day"] = current_day
            state["cluster_progress"] = progress
            self.save_state(state)
            return {
                "action": "CONTINUE",
                "cluster_id": active_id,
                "cluster_name": ALL_CLUSTERS[active_id]["cluster_name"],
                "current_day": current_day,
                "progress_percent": round((current_day / 30.0) * 100, 1),
                "reason": "30-Day Cluster In Progress (철칙 1 엄수: 30일 독점 완주 전 카테고리 이탈 금지)"
            }

        # Case 2: Current cluster reached 30 days! Graduate and autonomously rotate
        prev_cluster_id = active_id
        prev_cluster_name = ALL_CLUSTERS[prev_cluster_id]["cluster_name"]
        progress[prev_cluster_id]["status"] = "COMPLETED"
        progress[prev_cluster_id]["completed_cycles"] = progress[prev_cluster_id].get("completed_cycles", 0) + 1
        progress[prev_cluster_id]["current_day"] = 30

        # Evaluate candidate clusters
        candidates = []
        for cid, cdata in ALL_CLUSTERS.items():
            c_prog = progress.get(cid, {"completed_cycles": 0})
            cycles = c_prog.get("completed_cycles", 0)
            p_score = self.calculate_cluster_priority(cid)
            candidates.append({
                "cluster_id": cid,
                "cluster_name": cdata["cluster_name"],
                "completed_cycles": cycles,
                "priority_score": p_score
            })

        # Sort: least completed cycles first, then highest priority score
        candidates.sort(key=lambda x: (x["completed_cycles"], -x["priority_score"]))
        next_winner = candidates[0]
        new_cluster_id = next_winner["cluster_id"]

        # Activate new cluster
        state["active_cluster_id"] = new_cluster_id
        state["current_day"] = 1
        state["total_published_in_cluster"] = 0
        progress[new_cluster_id]["status"] = "ACTIVE"
        progress[new_cluster_id]["current_day"] = 1
        state["cluster_progress"] = progress
        self.save_state(state)

        return {
            "action": "ROTATE",
            "prev_cluster_id": prev_cluster_id,
            "prev_cluster_name": prev_cluster_name,
            "cluster_id": new_cluster_id,
            "cluster_name": ALL_CLUSTERS[new_cluster_id]["cluster_name"],
            "current_day": 1,
            "progress_percent": 3.3,
            "priority_score": next_winner["priority_score"],
            "reason": f"30-Day Monopoly Complete for '{prev_cluster_name}' -> Autonomously Promoted Highest-Yield Niche '{ALL_CLUSTERS[new_cluster_id]['cluster_name']}'"
        }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        state = self.load_state()
        active_id = state.get("active_cluster_id", "hair_transplant")
        current_day = state.get("current_day", 1)
        progress = state.get("cluster_progress", {})

        summary_list = []
        for cid, cdata in ALL_CLUSTERS.items():
            c_prog = progress.get(cid, {"current_day": 1, "completed_cycles": 0, "status": "QUEUED"})
            c_day = current_day if cid == active_id else c_prog.get("current_day", 1)
            is_active = (cid == active_id)
            summary_list.append({
                "cluster_id": cid,
                "cluster_name": cdata["cluster_name"],
                "category": cdata["category"],
                "cpc": cdata["cpc"],
                "avg_payout": cdata.get("avg_payout", 30000),
                "is_active": is_active,
                "current_day": c_day,
                "progress_percent": round((c_day / 30.0) * 100, 1) if is_active else (100.0 if c_prog.get("completed_cycles", 0) > 0 else 0.0),
                "completed_cycles": c_prog.get("completed_cycles", 0),
                "status": "ACTIVE" if is_active else ("COMPLETED" if c_prog.get("completed_cycles", 0) > 0 else "QUEUED"),
                "priority_score": self.calculate_cluster_priority(cid)
            })

        summary_list.sort(key=lambda x: (not x["is_active"], -x["priority_score"]))
        return {
            "active_cluster_id": active_id,
            "current_day": current_day,
            "total_clusters": len(ALL_CLUSTERS),
            "clusters": summary_list
        }


class TopicClusterEngine:
    """
    Topic Cluster Knowledge Graph & Interlinking Orchestrator (v8.0 Apex).
    Prevents single-off keyword generation and enforces complete 30-day niche monopolization.
    """

    def __init__(self, state_file: str = STATE_FILE_PATH):
        self.portfolio_mgr = AutonomousClusterPortfolioManager(state_file=state_file)
        self.chief_prompt = CHIEF_OF_STAFF_PROMPT
        self.planner_prompt = PRODUCT_PLANNER_PROMPT
        self.semantic_vectorizer = LocalSemanticVectorizer()

    def load_state(self) -> Dict[str, Any]:
        return self.portfolio_mgr.load_state()

    def save_state(self, state: Dict[str, Any]):
        self.portfolio_mgr.save_state(state)

    def get_cluster(self, cluster_id: str = "hair_transplant") -> Dict[str, Any]:
        return ALL_CLUSTERS.get(cluster_id, HAIR_TRANSPLANT_CLUSTER)

    def resolve_cluster_id_from_category(self, category: str, keyword: str = "") -> str:
        cat_upper = category.upper() if category else ""
        if cat_upper in CATEGORY_TO_CLUSTER_MAP:
            return CATEGORY_TO_CLUSTER_MAP[cat_upper]

        kw_clean = keyword.lower()
        if "모발" in kw_clean or "탈모" in kw_clean or "이식" in kw_clean:
            return "hair_transplant"
        elif "환급" in kw_clean or "지원금" in kw_clean or "도약" in kw_clean or "장려금" in kw_clean:
            return "government_subsidy"
        elif "알뜰폰" in kw_clean or "요금제" in kw_clean or "절감" in kw_clean or "카드" in kw_clean:
            return "cashflow_hacks"
        elif "라식" in kw_clean or "임플란트" in kw_clean or "도수" in kw_clean or "비급여" in kw_clean:
            return "medical_wellness"
        elif "자격증" in kw_clean or "내일배움" in kw_clean or "국비" in kw_clean or "기사" in kw_clean:
            return "career_cert"

        return "hair_transplant"

    def get_next_cluster_topic(self, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Pulls the next sequential topic node from the 30-day topic cluster mesh.
        Autonomously governs portfolio lifecycle and enforces 30-day niche monopoly.
        """
        # Run autonomous portfolio governance
        governance = self.portfolio_mgr.auto_select_active_cluster()
        c_id = cluster_id or governance["cluster_id"]
        cluster = self.get_cluster(c_id)

        state = self.portfolio_mgr.load_state()
        current_day = state.get("current_day", 1)

        spokes = cluster.get("spokes", [])
        idx = (current_day - 1) % len(spokes)
        spoke = spokes[idx]

        return {
            "cluster_id": c_id,
            "cluster_name": cluster.get("cluster_name"),
            "category": cluster.get("category", "HAIR"),
            "domain": cluster.get("domain", "HAIR_TRANSPLANT"),
            "cpc": cluster.get("cpc", 6800),
            "avg_payout": cluster.get("avg_payout", 50000),
            "day": spoke["day"],
            "keyword": spoke["keyword"],
            "title": spoke["title"],
            "phase": spoke["phase"],
            "core_question": spoke["question"],
            "hook_next": spoke.get("hook_next", ""),
            "pillar": cluster.get("pillar"),
            "governance": governance
        }

    def record_publication(self, keyword: str, post_id: str, post_url: str):
        """Advances the cluster day index by 1 and records the publication node."""
        state = self.portfolio_mgr.load_state()
        c_id = state.get("active_cluster_id", "hair_transplant")
        current_day = state.get("current_day", 1)

        state.setdefault("history", []).append({
            "day": current_day,
            "cluster_id": c_id,
            "keyword": keyword,
            "post_id": post_id,
            "url": post_url
        })
        state["total_published_in_cluster"] = state.get("total_published_in_cluster", 0) + 1
        state["current_day"] = current_day + 1

        # Update progress tracking
        progress = state.setdefault("cluster_progress", {})
        if c_id in progress:
            progress[c_id]["current_day"] = current_day + 1
            progress[c_id]["total_published"] = progress[c_id].get("total_published", 0) + 1

        self.portfolio_mgr.save_state(state)

        # Trigger auto-governance check (if Day > 30, it will graduate on next fetch)
        self.portfolio_mgr.auto_select_active_cluster()

    def render_interlinking_mesh(self, keyword: str, category: str = "HAIR", cluster_id: Optional[str] = None) -> str:
        """
        Generates the Apolia Interlinking Mesh Card Box (그물망 내부링크 UI) for whichever niche is active.
        Connects the Pillar, Previous Spoke, Next Spoke, and 2 Related Curiosity Spokes
        to keep visitors reading 3~4 articles in sequence (North Star: Dwell Time 3m 30s+).
        """
        if not cluster_id:
            cluster_id = self.resolve_cluster_id_from_category(category, keyword)

        cluster = self.get_cluster(cluster_id)
        pillar = cluster["pillar"]
        spokes = cluster["spokes"]

        # Identify current spoke index
        current_idx = 0
        for i, s in enumerate(spokes):
            if s["keyword"] in keyword or keyword in s["keyword"]:
                current_idx = i
                break

        prev_spoke = spokes[(current_idx - 1) % len(spokes)]
        next_spoke = spokes[(current_idx + 1) % len(spokes)]

        # Pick 2 related curiosity spokes
        rel1 = spokes[(current_idx + 3) % len(spokes)]
        rel2 = spokes[(current_idx + 7) % len(spokes)]

        html = f"""
<!-- Blogin 365 AI 30-Day Topic Cluster Interlinking Mesh -->
<div class="b365-cluster-nav" style="margin: 36px 0; padding: 24px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 16px; box-shadow: 0 4px 16px -2px rgba(15,23,42,0.04);">
  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
    <span style="font-size: 11px; font-weight: 800; color: #2563eb; background: #eff6ff; padding: 3px 10px; border-radius: 9999px;">
      🔗 30-DAY TOPIC CLUSTER · 연계 심층 탐색
    </span>
    <span style="font-size: 11px; color: #64748b; font-weight: 600;">
      독점 팩트체크 시리즈 (3~4개 글 연속 정독 권장)
    </span>
  </div>

  <div style="font-size: 17px; font-weight: 800; color: #0f172a; margin-bottom: 12px; letter-spacing: -0.3px;">
    📚 {cluster['cluster_name']} 연계 분석 가이드
  </div>

  <!-- 1. Pillar Hub Card -->
  <div style="background: #ffffff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; border-radius: 10px; padding: 14px 16px; margin-bottom: 14px;">
    <div style="font-size: 11px; font-weight: 700; color: #2563eb; margin-bottom: 4px;">🏛️ [마스터 종합 기둥글]</div>
    <a href="{pillar['url']}" target="_blank" rel="noopener" style="font-size: 14px; font-weight: 700; color: #0f172a; text-decoration: none; line-height: 1.4;">
      {pillar['title']}
    </a>
    <div style="font-size: 12px; color: #64748b; margin-top: 4px;">{pillar['description']}</div>
  </div>

  <!-- 2. Prev & Next Sequence -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-bottom: 14px;">
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px;">
      <div style="font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 3px;">👈 [이전 필수 분석]</div>
      <a href="https://blogin365ai.blogspot.com/search?q={re.sub(r'\\s+', '+', prev_spoke['keyword'])}" target="_blank" rel="noopener" style="font-size: 13px; font-weight: 700; color: #1e293b; text-decoration: none;">
        {prev_spoke['title']}
      </a>
    </div>
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px;">
      <div style="font-size: 11px; font-weight: 700; color: #2563eb; margin-bottom: 3px;">👉 [다음 추천 필독]</div>
      <a href="https://blogin365ai.blogspot.com/search?q={re.sub(r'\\s+', '+', next_spoke['keyword'])}" target="_blank" rel="noopener" style="font-size: 13px; font-weight: 700; color: #2563eb; text-decoration: none;">
        {next_spoke['title']}
      </a>
    </div>
  </div>

  <!-- 3. Curiosity Deep-Dive Nodes -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 16px;">
    <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">🔥 독자들이 함께 확인한 핵심 궁금증:</div>
    <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #475569; line-height: 1.7;">
      <li style="margin-bottom: 4px;">
        <a href="https://blogin365ai.blogspot.com/search?q={re.sub(r'\\s+', '+', rel1['keyword'])}" target="_blank" rel="noopener" style="color: #0f172a; text-decoration: none; font-weight: 600;">
          {rel1['question']}
        </a>
      </li>
      <li>
        <a href="https://blogin365ai.blogspot.com/search?q={re.sub(r'\\s+', '+', rel2['keyword'])}" target="_blank" rel="noopener" style="color: #0f172a; text-decoration: none; font-weight: 600;">
          {rel2['question']}
        </a>
      </li>
    </ul>
  </div>
</div>
""".strip()
        return html

    @staticmethod
    def disambiguate_intent(keyword: str) -> str:
        """
        Classifies keyword into distinct search intent clusters:
        - CALC: Interactive simulation, cost estimation, unit math
        - COMPARE: VS comparison, technique tradeoffs, table breakdown
        - INFO: Procedural guide, recovery, regulations, qualifications
        """
        kw = keyword.lower()
        if any(k in kw for k in ["계산", "모의", "시뮬", "견적", "1원", "환산", "수가", "비용"]):
            return "CALC"
        elif any(k in kw for k in ["비교", "vs", "차이", "장단점", "기법", "대조", "분석"]):
            return "COMPARE"
        else:
            return "INFO"

    def check_cannibalization(self, candidate_kw: str, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """
        [철칙 1-3] 키워드 카니발라이제이션 방어:
        로컬 CPU 의미론적 코사인 유사도(Cosine Distance > 0.35)를 검증하여
        동일 인텐트 내 중복 키워드를 원천 차단하고 정보형/계산형/비교형 의도를 격리.
        """
        c_id = cluster_id or self.portfolio_mgr.load_state().get("active_cluster_id", "hair_transplant")
        cluster = self.get_cluster(c_id)
        candidate_intent = self.disambiguate_intent(candidate_kw)

        spokes = cluster.get("spokes", [])
        collisions = []

        for s in spokes:
            spoke_kw = s["keyword"]
            if spoke_kw == candidate_kw:
                continue
            spoke_intent = self.disambiguate_intent(spoke_kw)
            
            # [Patch 4] 로컬 CPU 기반 의미론적 코사인 거리 측정
            dist = self.semantic_vectorizer.calculate_cosine_distance(candidate_kw, spoke_kw)
            sim = round(1.0 - dist, 3)

            # If semantic similarity is high (dist < 0.35) and search intent is identical:
            if dist < 0.35 and candidate_intent == spoke_intent:
                collisions.append({
                    "colliding_spoke": spoke_kw,
                    "similarity": sim,
                    "cosine_distance": dist,
                    "shared_intent": candidate_intent
                })

        passed = (len(collisions) == 0)
        return {
            "passed": passed,
            "candidate_keyword": candidate_kw,
            "candidate_intent": candidate_intent,
            "cluster_id": c_id,
            "collisions": collisions,
            "reason": "카니발라이제이션 없음 (의미론적 거리 확보 또는 의도 분리 완료)" if passed else f"카니발라이제이션 위험 감지 ({len(collisions)}건 중복)"
        }


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    engine = TopicClusterEngine()
    summary = engine.portfolio_mgr.get_portfolio_summary()
    print("=== Autonomous Cluster Portfolio Summary ===")
    print(f"Active Cluster: {summary['active_cluster_id']} (Day {summary['current_day']})")
    print("\nAll 5 Golden Niches:")
    for c in summary["clusters"]:
        act_mark = "▶ [ACTIVE]" if c["is_active"] else "  [QUEUED]"
        print(f"{act_mark} {c['cluster_name']:<25} | Day: {c['current_day']:>2}/30 ({c['progress_percent']:>5.1f}%) | Score: {c['priority_score']:>8,.1f} pt")

    next_t = engine.get_next_cluster_topic()
    print("\n=== Next Autonomous Topic Node ===")
    print(f"Cluster: {next_t['cluster_name']}")
    print(f"Day: {next_t['day']}")
    print(f"Keyword: {next_t['keyword']}")
    print(f"Title: {next_t['title']}")
    print(f"Core Question: {next_t['core_question']}")
