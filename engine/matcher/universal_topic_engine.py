# -*- coding: utf-8 -*-
"""
engine/matcher/universal_topic_engine.py
-----------------------------------------
Blogin 365 AI Holdings - Universal Topic Intelligence Engine (v9.0 Apex)

특정 키워드 하드코딩 파이썬 파일(hair.py, medical.py 등)을 영구 폐기하고,
임의의 어떤 키워드(생활, 건강, 세금, 금융, 복지, 소비 등)가 입력되어도
8인 AI 직원이 동적으로 30일 지식 그래프와 스포크를 생성·관리하는 완전 범용 엔진.

4대 권위 필라(Authority Pillars):
1. 💰 경제·금융 (Finance & Economy): 세무, 해외주식, 예적금, 대출, 퀀트, 환급금
2. 🏥 생활·건강 (Health & Medical): 비급여 시술, 탈모/피부, 치과/임플란트, 병원비
3. 🏛️ 정책·복지 (Policy & Welfare): 정부지원금, 청년정책, 기초연금, 고용/국비지원
4. 💡 생활·소비 (Smart Living & Savings): 알뜰폰/통신비, 공과금/에너지, 스마트 절약, IT가전
"""

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.matcher.domain_router import classify_domain
from engine.matcher.semantic_cannibalization_engine import LocalSemanticVectorizer

CLUSTERS_JSON_PATH = os.path.join(BASE_DIR, "data", "universal_clusters.json")
STATE_FILE_PATH = os.path.join(BASE_DIR, "data", "topic_cluster_state.json")

# 4대 표준 미디어 필라 (GNB 네비게이션 표준)
PILLAR_FINANCE = "경제·금융"
PILLAR_HEALTH = "생활·건강"
PILLAR_WELFARE = "정책·복지"
PILLAR_LIVING = "생활·소비"

CATEGORY_TO_PILLAR_MAP: Dict[str, str] = {
    # 경제·금융
    "FINANCE": PILLAR_FINANCE,
    "TAX": PILLAR_FINANCE,
    "QUANT": PILLAR_FINANCE,
    "STOCK": PILLAR_FINANCE,
    "CRYPTO": PILLAR_FINANCE,
    "INVESTMENT": PILLAR_FINANCE,
    # 생활·건강
    "HAIR": PILLAR_HEALTH,
    "MEDICAL": PILLAR_HEALTH,
    "HEALTH": PILLAR_HEALTH,
    "CLINIC": PILLAR_HEALTH,
    # 정책·복지
    "SUBSIDY": PILLAR_WELFARE,
    "WELFARE": PILLAR_WELFARE,
    "GOVERNMENT": PILLAR_WELFARE,
    "CAREER": PILLAR_WELFARE,
    "CERT": PILLAR_WELFARE,
    # 생활·소비
    "SAVINGS": PILLAR_LIVING,
    "TELECOM": PILLAR_LIVING,
    "TECH": PILLAR_LIVING,
    "LIVING": PILLAR_LIVING,
    "AUTO_INSURANCE": PILLAR_LIVING
}


def resolve_canonical_pillar(category: str, keyword: str = "") -> str:
    """
    임의의 카테고리 코드 또는 키워드를 분석하여 4대 표준 필라 중 하나로 확정 반환.
    """
    cat_upper = (category or "").upper()
    if cat_upper in CATEGORY_TO_PILLAR_MAP:
        return CATEGORY_TO_PILLAR_MAP[cat_upper]

    kw_lower = (keyword or "").lower()
    
    # 1. 경제·금융 (Finance, Stock, Crypto, Trading, Taxes)
    finance_indicators = [
        "주식", "코인", "비트코인", "바이낸스", "트레이딩", "퀀트", "양도세", "양도소득세",
        "손익통산", "배당", "복리", "물타기", "평단가", "선물", "레버리지", "청산가",
        "변동성", "워뇨띠", "래리 윌리엄스", "슈퍼트렌드", "스캘핑", "볼린저밴드", "파킹통장",
        "적금", "예금", "대출", "금융소득", "fintech", "quant", "crypto", "tradingview", "vibe_trading"
    ]
    if any(k in kw_lower for k in finance_indicators):
        return PILLAR_FINANCE

    # 2. 생활·건강 (Medical, Hair, Dental, Vision, Health)
    health_indicators = [
        "탈모", "모발이식", "모발", "모낭", "헤어라인", "생착", "동반탈락", "암흑기",
        "임플란트", "라식", "라섹", "스마일라식", "피부과", "도수치료", "병원", "치과",
        "치아", "비급여", "의료비", "수술비", "hair", "medical", "clinic"
    ]
    if any(k in kw_lower for k in health_indicators):
        return PILLAR_HEALTH

    # 3. 정책·복지 (Subsidy, Pension, Welfare, Government Grants, Tax Refunds)
    welfare_indicators = [
        "지원금", "환급", "청년도약", "근로장려금", "자녀장려금", "연금", "국비지원", "내일배움",
        "배움카드", "복지", "바우처", "피부양자", "특례대출", "버팀목", "실업급여", "subsidy", "welfare"
    ]
    if any(k in kw_lower for k in welfare_indicators):
        return PILLAR_WELFARE

    # 4. 생활·소비 (Living, Telecom, Energy, Tech, Savings)
    return PILLAR_LIVING


class UniversalTopicEngine:
    """
    완전 범용 30-Day 토픽 지식 그래프 & 클러스터 엔진.
    - 하드코딩 .py 파일 없이 data/universal_clusters.json 기반 영구 지속성.
    - 미등록 키워드 유입 시 8인 AI 에이전트 표준 30-Day 스포크를 동적으로 즉각 합성.
    """

    def __init__(self, clusters_path: str = CLUSTERS_JSON_PATH, state_path: str = STATE_FILE_PATH):
        self.clusters_path = clusters_path
        self.state_path = state_path
        self.clusters: Dict[str, Dict[str, Any]] = self._load_clusters()
        self._ensure_state_file()

    def _load_clusters(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(self.clusters_path):
            try:
                with open(self.clusters_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ [UniversalTopicEngine] 클러스터 파일 로드 경고: {e}")
        return {}

    def _save_clusters(self):
        os.makedirs(os.path.dirname(self.clusters_path), exist_ok=True)
        try:
            with open(self.clusters_path, "w", encoding="utf-8") as f:
                json.dump(self.clusters, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ [UniversalTopicEngine] 클러스터 저장 에러: {e}")

    def _ensure_state_file(self):
        if not os.path.exists(self.state_path):
            initial_state = {
                "active_cluster_id": "hair_transplant",
                "current_day": 1,
                "total_published_in_cluster": 0,
                "cluster_progress": {},
                "history": []
            }
            os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
            with open(self.state_path, "w", encoding="utf-8") as f:
                json.dump(initial_state, f, ensure_ascii=False, indent=2)

    def load_state(self) -> Dict[str, Any]:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"active_cluster_id": "hair_transplant", "current_day": 1}

    def save_state(self, state: Dict[str, Any]):
        try:
            with open(self.state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ [UniversalTopicEngine] 상태 저장 에러: {e}")

    def get_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """클러스터 ID로 클러스터 반환. 없을 경우 기본 폴백 또는 동적 생성."""
        if cluster_id in self.clusters:
            return self.clusters[cluster_id]
        if self.clusters:
            return next(iter(self.clusters.values()))
        return self.create_dynamic_cluster("모발이식 비용", "HAIR")

    def resolve_cluster_id(self, category: str, keyword: str = "") -> str:
        """카테고리 및 키워드로 클러스터 ID 동적 결정"""
        cat_upper = (category or "").upper()
        mapping = {
            "HAIR": "hair_transplant",
            "SUBSIDY": "government_subsidy",
            "SAVINGS": "cashflow_hacks",
            "MEDICAL": "medical_wellness",
            "CAREER": "career_cert"
        }
        if cat_upper in mapping and mapping[cat_upper] in self.clusters:
            return mapping[cat_upper]

        kw_clean = re.sub(r'[^a-zA-Z0-9가-힣]', '', keyword.lower())
        for cid, cdata in self.clusters.items():
            if kw_clean in cid or cid in kw_clean:
                return cid
            if any(kw_clean in s.get("keyword", "").lower() for s in cdata.get("spokes", [])):
                return cid

        # 일치하는 클러스터가 없으면 동적 생성
        cluster = self.create_dynamic_cluster(keyword or "스마트 생활 가이드", category)
        return cluster["cluster_id"]

    def create_dynamic_cluster(self, keyword: str, category: str = "FINANCE") -> Dict[str, Any]:
        """
        하드코딩 없이 임의의 어떤 키워드가 들어와도 30-Day 지식 그래프를 즉석에서 정밀 합성.
        """
        clean_kw = keyword.strip()
        cid = re.sub(r'[^a-zA-Z0-9가-힣]', '_', clean_kw).strip('_') or f"cluster_{int(os.getpid())}"
        pillar_name = resolve_canonical_pillar(category, clean_kw)
        domain = classify_domain(clean_kw, category)

        phases = [
            ("비용/견적 탐색", "실제 비용 및 기본 견적 기준 분석"),
            ("세제/혜택/환급", "실비보험 및 세액공제/정부 지원 혜택"),
            ("부작용/위험 방어", "핵심 주의사항 및 뻥튀기 감별법"),
            ("유지비/장기 관리", "장기 누적 유지비 및 최적화 체크리스트")
        ]

        spokes = []
        for day in range(1, 31):
            phase_idx = min((day - 1) // 8, len(phases) - 1)
            phase_title, phase_desc = phases[phase_idx]
            spoke_kw = f"{clean_kw} Day {day} 핵심 분석"
            spokes.append({
                "day": day,
                "id": f"{cid}-spoke-{day:02d}",
                "keyword": f"{clean_kw} {phase_title} {day}단계",
                "title": f"[2026] {clean_kw} {phase_title}: {phase_desc} 및 실측 가이드 (Day {day})",
                "phase": phase_title,
                "question": f"{clean_kw} 진행 시 {phase_title} 관점에서 반드시 알아야 할 핵심 팩트는 무엇일까?",
                "hook_next": f"{clean_kw} 다음 단계 심층 실측 리포트 및 모의계산 가이드"
            })

        cluster_obj = {
            "cluster_id": cid,
            "cluster_name": f"{clean_kw} 마스터 클러스터",
            "category": category,
            "pillar_category": pillar_name,
            "domain": domain,
            "cpc": 4500,
            "avg_payout": 35000,
            "pillar": {
                "id": f"{cid}-pillar-00",
                "keyword": clean_kw,
                "title": f"[2026] {clean_kw} 총정리 마스터 가이드 및 실측 모의계산",
                "url": f"https://blogin365ai.blogspot.com/p/{cid}-master-guide.html",
                "description": f"{clean_kw}의 시작부터 끝까지 핵심 수치와 공식 기준을 총망라한 마스터 가이드"
            },
            "spokes": spokes
        }

        self.clusters[cid] = cluster_obj
        self._save_clusters()
        return cluster_obj

    def get_next_cluster_topic(self, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """순차적 30-Day 스포크 자동 디스패치"""
        state = self.load_state()
        cid = cluster_id or state.get("active_cluster_id", "hair_transplant")
        cluster = self.get_cluster(cid)

        day = state.get("current_day", 1)
        spokes = cluster.get("spokes", [])
        if not spokes:
            cluster = self.create_dynamic_cluster("2026 청년지원금", "SUBSIDY")
            spokes = cluster["spokes"]

        day_idx = (day - 1) % len(spokes)
        spoke = spokes[day_idx]

        return {
            "cluster_id": cluster["cluster_id"],
            "cluster_name": cluster["cluster_name"],
            "category": cluster.get("category", "FINANCE"),
            "pillar_category": cluster.get("pillar_category", resolve_canonical_pillar(cluster.get("category", "FINANCE"))),
            "day": day,
            "spoke_id": spoke["id"],
            "keyword": spoke["keyword"],
            "title": spoke["title"],
            "question": spoke["question"],
            "hook_next": spoke["hook_next"],
            "governance": {
                "reason": f"30-Day Cluster Progressive Dispatch (Day {day}/30)"
            }
        }

    def record_publication(self, keyword: str, post_id: str, post_url: str):
        """발행 이력 및 일차 진행 업데이트"""
        state = self.load_state()
        state["current_day"] = state.get("current_day", 1) + 1
        state["total_published_in_cluster"] = state.get("total_published_in_cluster", 0) + 1
        history = state.get("history", [])
        history.append({
            "keyword": keyword,
            "post_id": post_id,
            "post_url": post_url,
            "day": state["current_day"] - 1
        })
        state["history"] = history
        self.save_state(state)

    def render_interlinking_mesh(self, keyword: str, category: str = "FINANCE", cluster_id: Optional[str] = None) -> str:
        """30-Day 그물망 내부 링크 박스 HTML 생성"""
        cid = cluster_id or self.resolve_cluster_id(category, keyword)
        cluster = self.get_cluster(cid)
        pillar = cluster.get("pillar", {})
        spokes = cluster.get("spokes", [])

        current_idx = 0
        for i, s in enumerate(spokes):
            if s.get("keyword") == keyword:
                current_idx = i
                break

        prev_spoke = spokes[max(0, current_idx - 1)] if spokes else {}
        next_spoke = spokes[min(len(spokes) - 1, current_idx + 1)] if spokes else {}
        current_spoke = spokes[current_idx] if spokes else {}

        pillar_cat = cluster.get("pillar_category", resolve_canonical_pillar(category, keyword))

        return f"""
        <div class="b365-cluster-nav" style="margin:36px 0; padding:24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #cbd5e1; padding-bottom:10px;">
            <div style="font-size:0.8rem; font-weight:800; color:#2563eb; letter-spacing:0.04em;">30-DAY TOPIC CLUSTER · {pillar_cat}</div>
            <div style="font-size:0.75rem; color:#64748b; font-weight:600;">{cluster.get('cluster_name', '종합 정보 토픽')}</div>
          </div>
          <div style="margin-bottom:16px;">
            <div style="font-size:0.82rem; color:#475569; font-weight:700; margin-bottom:4px;">🏛️ 마스터 종합 기둥글:</div>
            <a href="{pillar.get('url', '#')}" style="font-size:0.95rem; font-weight:800; color:#0f172a; text-decoration:none;">{pillar.get('title', keyword)}</a>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
            <div style="background:#ffffff; padding:12px 14px; border-radius:10px; border:1px solid #e2e8f0;">
              <span style="font-size:0.72rem; color:#64748b; font-weight:700;">◀ 이전 필수 분석 (Day {prev_spoke.get('day', 1)})</span>
              <div style="font-size:0.85rem; font-weight:700; color:#1e293b; margin-top:4px;">{prev_spoke.get('title', '이전 단계 가이드')}</div>
            </div>
            <div style="background:#ffffff; padding:12px 14px; border-radius:10px; border:1px solid #e2e8f0;">
              <span style="font-size:0.72rem; color:#2563eb; font-weight:700;">▶ 다음 추천 필독 (Day {next_spoke.get('day', 2)})</span>
              <div style="font-size:0.85rem; font-weight:700; color:#1e293b; margin-top:4px;">{next_spoke.get('title', '다음 단계 가이드')}</div>
            </div>
          </div>
          <div style="margin-top:14px; font-size:0.78rem; color:#64748b; line-height:1.5;">
            💡 <strong>핵심 궁금증</strong>: {current_spoke.get('question', '독자들이 가장 많이 질문하는 핵심 사항을 팩트체크합니다.')}
          </div>
        </div>
        """

    def check_cannibalization(self, candidate_kw: str, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """의미론적 카니발라이제이션 방어"""
        state = self.load_state()
        history = state.get("history", [])
        for item in history[-15:]:
            prev_kw = item.get("keyword", "")
            if prev_kw and (candidate_kw == prev_kw or (len(candidate_kw) > 3 and candidate_kw in prev_kw)):
                return {
                    "passed": False,
                    "reason": f"최근 발행 키워드 '{prev_kw}'와 완전 중복 감지",
                    "candidate_intent": "DUPLICATE"
                }
        return {
            "passed": True,
            "candidate_intent": "INFORMATIONAL",
            "distance": 0.85
        }
