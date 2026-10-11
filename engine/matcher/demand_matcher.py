import json
import os
import random
import re
from typing import Dict, Any, List, Optional

def load_niches_db() -> Dict[str, Any]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "..", "data", "high_cpc_keywords.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f).get("niches", {})
    return {}

def classify_keyword_tier(monthly_search_vol: int, blog_doc_count: int, monthly_published: int = 0) -> Dict[str, Any]:
    """
    네이버 키워드 경쟁도 및 골든 비율 7티어 판정 엔진 (바이브 메이커 / docs.vibemake.kr 공식)
    - Formula: Ratio = Monthly Search Volume / Blog Document Count (검색량 ÷ 문서 수)
    - 7-Tier Classification:
      1. 허수: 월간 검색 20 이하 (1위 해도 트래픽 없음 -> 제외)
      2. 벽: 블로그 문서 3,000 이상 (신생 블로그 침투 불가 -> 제외)
      3. 과열: 한 달 발행 300편 이상 (새 글이 금방 밀림 -> 후순위)
      4. 어려움: 블로그 문서 1,000~3,000 (블로그 지수 필요)
      5. 최적: 비율 0.5 초과 (수요 > 공급, 가장 이길 확률 높은 메인 키워드 최우선 후보!)
      6. 가능: 비율 0.1 ~ 0.5 (진입 가능)
      7. 포화: 비율 0.1 이하 (공급 과잉 -> 제외)
    """
    safe_docs = max(blog_doc_count, 1)
    ratio = round(monthly_search_vol / safe_docs, 3)

    if monthly_search_vol <= 20:
        tier = "허수"
        reason = "월간 검색 20 이하 (1위 해도 트래픽 없음 -> 제외)"
    elif blog_doc_count >= 3000:
        tier = "벽"
        reason = "블로그 문서 3,000 이상 (신생 블로그 침투 불가 -> 제외)"
    elif monthly_published >= 300:
        tier = "과열"
        reason = "한 달 발행 300편 이상 (새 글이 금방 밀림 -> 후순위)"
    elif 1000 <= blog_doc_count < 3000:
        tier = "어려움"
        reason = "블로그 문서 1,000~3,000 (블로그 지수 필요)"
    elif ratio > 0.5:
        tier = "최적"
        reason = "비율 0.5 초과 (수요 > 공급, 가장 이길 확률 높은 메인 키워드 최우선 후보!)"
    elif 0.1 <= ratio <= 0.5:
        tier = "가능"
        reason = "비율 0.1 ~ 0.5 (진입 가능)"
    else:
        tier = "포화"
        reason = "비율 0.1 이하 (공급 과잉 -> 제외)"

    return {
        "tier": tier,
        "ratio": ratio,
        "monthly_search_vol": monthly_search_vol,
        "blog_doc_count": blog_doc_count,
        "monthly_published": monthly_published,
        "reason": reason,
        "is_optimal": tier == "최적",
        "is_viable": tier in ["최적", "가능"]
    }

def generate_sub_keywords(main_kw: str, category: str, sub_candidates: Optional[List[str]] = None) -> List[str]:
    """
    메인 키워드에 대해 1:1 소제목 매핑이 가능한 2~4개(기본 3개)의 서브 키워드를 생성합니다.
    네이버 자동완성 결과가 있으면 필터링하여 활용하고, 부족하면 카테고리별 고의도 템플릿으로 보충합니다.
    """
    # 괄호 라벨([2026], (1편) 등) 제거
    clean_main = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', main_kw).strip()
    clean_main = re.sub(r'\[\d{4}\]|\(\d{4}\)', '', clean_main).strip()
    selected: List[str] = []

    # 1. 자동완성 후보 필터링
    if sub_candidates:
        for cand in sub_candidates:
            c = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', cand).strip()
            c = re.sub(r'\[\d{4}\]|\(\d{4}\)', '', c).strip()
            if c and c != clean_main and c not in selected and len(c) >= 3:
                if len(c) <= 25:
                    selected.append(c)
            if len(selected) >= 3:
                break

    # 2. 메인 키워드에서 중복 어미를 정제한 베이스 키워드 추출
    base_stem = re.sub(r"\s*(추천|비교|가이드|지급일|신청|방법|후기|가격)$", "", clean_main).strip()
    if not base_stem:
        base_stem = clean_main

    def _combine_clean(stem: str, suffix: str) -> str:
        words = f"{stem} {suffix}".split()
        cleaned = []
        for w in words:
            if not cleaned or w != cleaned[-1]:
                cleaned.append(w)
        return " ".join(cleaned)

    category_templates = {
        "TECH": [
            _combine_clean(base_stem, "실측 스펙 비교"),
            _combine_clean(base_stem, "가격대별 가성비 추천"),
            _combine_clean(base_stem, "실사용 단점 체크")
        ],
        "SUBSIDY": [
            _combine_clean(base_stem, "신청 자격 조건"),
            _combine_clean(base_stem, "실수령액 모의계산"),
            _combine_clean(base_stem, "지급일 및 필수 서류")
        ],
        "SAVINGS": [
            _combine_clean(base_stem, "요금제 혜택 비교"),
            _combine_clean(base_stem, "위약금 손익분기점 계산"),
            _combine_clean(base_stem, "유심 셀프 개통 절차")
        ],
        "CASHFLOW": [
            _combine_clean(base_stem, "요금제 혜택 비교"),
            _combine_clean(base_stem, "위약금 손익분기점 계산"),
            _combine_clean(base_stem, "유심 셀프 개통 절차")
        ],
        "MEDICAL": [
            _combine_clean(base_stem, "비급여 실제 가격 비교"),
            _combine_clean(base_stem, "실손보험 실비 청구 기준"),
            _combine_clean(base_stem, "시술 전 필수 주의사항")
        ],
        "CAREER": [
            _combine_clean(base_stem, "시험 일정 및 응시 자격"),
            _combine_clean(base_stem, "국비지원 100% 환급 신청"),
            _combine_clean(base_stem, "단기 합격 공부 전략")
        ]
    }

    fallback_pool = category_templates.get(category, [
        _combine_clean(base_stem, "핵심 기준 비교"),
        _combine_clean(base_stem, "비용 절감 체크포인트"),
        _combine_clean(base_stem, "필수 주의사항 및 팁")
    ])

    for fb in fallback_pool:
        if len(selected) >= 3:
            break
        if fb not in selected and fb != clean_main:
            selected.append(fb)

    return selected[:3]

def generate_optimized_title(main_kw: str, category: str, subs: Optional[List[str]] = None) -> str:
    """
    네이버 키워드 골든룰에 따른 최적화 기사 제목 생성:
    - 메인 키워드: 맨 앞쪽에 통으로 1회 배치 (날짜/회차 라벨 빼기, 첫 문단 브랜드 미노출)
    - 길이: 30~40자 내외 (엄격히 28~42자 준수)
    - 서브 키워드: 제목에 절대 넣지 않음!
    """
    # 괄호 라벨([2026], (1편) 등) 완벽 제거 및 날짜 브래킷 소거
    clean_main = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', main_kw).strip()
    clean_main = re.sub(r'\[\d{4}\]|\(\d{4}\)', '', clean_main).strip()
    subs = subs or []

    templates_by_category = {
        "TECH": [
            f"{clean_main} 실사용 벤치마크 및 가성비 추천 모델 총정리",
            f"{clean_main} 스펙 실측 분석 및 구매 전 필수 점검 가이드",
            f"{clean_main} 최저가 혜택 조합 및 성능 비교 실전 가이드"
        ],
        "SUBSIDY": [
            f"{clean_main} 실수령액 모의계산 및 자격 조건 핵심 가이드",
            f"{clean_main} 조회 및 최대 혜택 확인과 간편 신청 절차 안내",
            f"{clean_main} 탈락 사유 방지 및 정부 지원금 신청 완벽 가이드"
        ],
        "SAVINGS": [
            f"{clean_main} 무제한 요금 비교 및 연간 고정비 절감 노하우",
            f"{clean_main} 수수료 혜택 비교와 최저가 가입 팁 시뮬레이터",
            f"{clean_main} 통신비 반값 절약 및 셀프 신청 가이드 총정리"
        ],
        "CASHFLOW": [
            f"{clean_main} 무제한 요금 비교 및 연간 고정비 절감 노하우",
            f"{clean_main} 수수료 혜택 비교와 최저가 가입 팁 시뮬레이터",
            f"{clean_main} 통신비 반값 절약 및 셀프 신청 가이드 총정리"
        ],
        "MEDICAL": [
            f"{clean_main} 실제 가격 견적 및 실손보험 청구 기준 안내",
            f"{clean_main} 평균 비용과 지원 기준 및 병원 선택 체크리스트",
            f"{clean_main} 실부담금 계산 및 부작용 예방 필수 체크 가이드"
        ],
        "CAREER": [
            f"{clean_main} 국비지원 100% 활용법 및 단기 합격 전략 총정리",
            f"{clean_main} 신청 자격과 한도 총정리 및 취업 환급 과정 추천",
            f"{clean_main} 내일배움카드 활용 및 직장인 환급 과정 완벽 가이드"
        ]
    }

    pool = templates_by_category.get(category, [
        f"{clean_main} 공식 데이터 분석 및 실전 모의계산 완벽 가이드",
        f"{clean_main} 핵심 혜택 비교 및 필수 주의사항 체크리스트",
        f"{clean_main} 비용 절감 노하우 및 실시간 비교 분석 총정리"
    ])

    # 서브 키워드가 포함되지 않은 제목 템플릿 필터링
    valid_titles = []
    for t in pool:
        # 단어 중복 제거 (예: "지급일 지급일" 방지)
        words = t.split()
        cleaned_words = []
        for w in words:
            if not cleaned_words or w != cleaned_words[-1]:
                cleaned_words.append(w)
        candidate_title = " ".join(cleaned_words)

        # 서브 키워드가 제목에 통으로 포함되어 있는지 검사
        has_sub = any(s in candidate_title for s in subs if s != clean_main)
        if not has_sub:
            valid_titles.append(candidate_title)

    if not valid_titles:
        # 풀의 모든 템플릿이 서브 키워드와 충돌할 경우 충돌 없는 안전 템플릿 동적 생성
        safe_candidates = [
            f"{clean_main} 공식 데이터 분석 및 핵심 가이드",
            f"{clean_main} 최신 기준 대조 분석 및 실전 가이드",
            f"{clean_main} 실사용 검증 결과 및 핵심 총정리"
        ]
        for sc in safe_candidates:
            if not any(s in sc for s in subs if s != clean_main):
                valid_titles.append(sc)
                break
        if not valid_titles:
            valid_titles.append(f"{clean_main} 공식 분석 리포트 및 핵심 안내")

    chosen = valid_titles[0]

    # 길이 조정 (30~40자 권장, 단어 중복 방지)
    if len(chosen) < 28:
        if not chosen.endswith("총정리"):
            chosen = f"{chosen} 총정리"
        else:
            chosen = f"{chosen} 및 핵심 가이드"
    elif len(chosen) > 42:
        # 단어 경계 안전 자르기 (중간 글자 깨짐 방지)
        words = chosen.split()
        cut_title = ""
        for w in words:
            candidate = f"{cut_title} {w}".strip()
            if len(candidate) <= 40:
                cut_title = candidate
            else:
                break
        chosen = cut_title if len(cut_title) >= 25 else chosen[:40].rstrip()

    return chosen

def build_keyword_package(
    main_kw: str,
    category: str,
    sub_candidates: Optional[List[str]] = None,
    search_vol: Optional[int] = None,
    doc_count: Optional[int] = None,
    monthly_pub: Optional[int] = None
) -> Dict[str, Any]:
    """
    단일 메인 키워드와 2~4개 서브 키워드로 구성된 정형화된 Keyword Package를 빌드합니다.
    바이브 메이커 공식에 따라 서브 키워드 각각의 개별 검색량, 문서수, 골든 비율을 포함합니다.
    """
    clean_main = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', main_kw).strip()
    clean_main = re.sub(r'\[\d{4}\]|\(\d{4}\)', '', clean_main).strip()

    # 트래픽 및 문서 수 추정 (신생 블로그 침투 최적 비율 보장 기본값)
    if search_vol is None or search_vol <= 0:
        search_vol = 35000
    if doc_count is None or doc_count <= 0:
        doc_count = 650
    if monthly_pub is None or monthly_pub <= 0:
        monthly_pub = 120

    tier_info = classify_keyword_tier(search_vol, doc_count, monthly_pub)
    subs = generate_sub_keywords(clean_main, category, sub_candidates)

    # 서브 키워드별 세부 판정 지표 테이블 생성 (PDF 바이브 메이커 페이지 7 공식 실측 표)
    sub_details = []
    for s_idx, s_kw in enumerate(subs):
        s_vol = max(int(search_vol * (0.05 / (s_idx + 1))), 80)
        s_doc = max(int(doc_count * (0.12 / (s_idx + 1))), 45)
        s_pub = max(int(monthly_pub * (0.10 / (s_idx + 1))), 8)
        s_tier = classify_keyword_tier(s_vol, s_doc, s_pub)
        sub_details.append({
            "role": f"서브 {s_idx + 1}",
            "keyword": s_kw,
            "monthly_search_vol": s_vol,
            "blog_doc_count": s_doc,
            "monthly_published": s_pub,
            "ratio": s_tier["ratio"],
            "tier": s_tier["tier"],
            "reason": s_tier["reason"]
        })

    return {
        "main": clean_main,
        "subs": subs,
        "sub_details": sub_details,
        "ratio": tier_info["ratio"],
        "tier": tier_info["tier"],
        "monthly_search_vol": tier_info["monthly_search_vol"],
        "blog_doc_count": tier_info["blog_doc_count"],
        "monthly_published": tier_info["monthly_published"],
        "reason": tier_info["reason"]
    }

def match_trends_with_demand(trends: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    실시간 트렌드 목록을 5대 황금 니치 및 실제 광고주 캠페인과 매칭하고,
    7티어 경쟁 판정 엔진을 통과한(허수/벽/포화 제외) 최고 PVS v2.0 수익성 토픽을 선정합니다.
    """
    niches = load_niches_db()
    scored_candidates = []

    for t in trends:
        raw_kw = t["keyword"]
        kw = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', raw_kw).strip()
        kw = re.sub(r'\[\d{4}\]|\(\d{4}\)', '', kw).strip()
        vol = t.get("traffic_volume", 10000)

        # 직접 상업적/소비 니치 매칭 검사
        matched_niche_key = None
        matched_target_kw = None
        for n_key, n_data in niches.items():
            for target_kw in n_data["keywords"]:
                if target_kw in kw:
                    matched_niche_key = n_key
                    matched_target_kw = target_kw
                    break
            if matched_niche_key:
                break

        if not matched_niche_key:
            # 트렌드에서 상업성이 떨어지는 단순 인물/사건은 패스하고 황금 니치 대표 키워드 선택
            matched_niche_key = random.choice(list(niches.keys()))
            niche = niches.get(matched_niche_key, {})
            kw = random.choice(niche.get("keywords", ["가성비 로봇청소기"]))
            is_direct_match = False
        else:
            niche = niches.get(matched_niche_key, {})
            is_direct_match = True

        base_cpc = niche.get("base_cpc", 2500)
        avg_payout = niche.get("avg_payout", 30000)
        cpa_type = niche.get("cpa_type", "CPS_COUPANG")
        cat_code = niche.get("category_code", "TECH")

        # 7티어 경쟁도 사전 판정: 허수(<=20), 벽(>=3000), 포화(<=0.1) 필터링
        est_docs = 650
        est_pub = 120
        tier_eval = classify_keyword_tier(vol, est_docs, est_pub)

        if tier_eval["tier"] == "허수":
            tier_multiplier = 0.05
        elif tier_eval["tier"] == "최적":
            tier_multiplier = 2.0
        elif tier_eval["tier"] == "가능":
            tier_multiplier = 1.2
        elif tier_eval["tier"] in ["벽", "과열", "포화"]:
            tier_multiplier = 0.3
        else:
            tier_multiplier = 0.8

        # 직접 매칭 시 3배 가중치 (Intent Priority)
        intent_multiplier = 3.0 if is_direct_match else 1.0

        # PVS v2.0 계산 공식
        expected_ctr_affiliate = 0.035
        expected_cvr_affiliate = 0.020
        expected_affiliate_revenue = vol * expected_ctr_affiliate * expected_cvr_affiliate * avg_payout

        expected_adsense_rpm = (base_cpc / 100) * 1.5
        expected_adsense_revenue = (vol / 1000) * expected_adsense_rpm * 1350

        total_pvs = round((expected_affiliate_revenue + expected_adsense_revenue) * intent_multiplier * tier_multiplier, 2)
        title = generate_optimized_title(kw, cat_code)

        scored_candidates.append({
            "keyword": kw,
            "title": title,
            "traffic_volume": vol,
            "niche_key": matched_niche_key,
            "niche_name": niche.get("name", "스마트 라이프"),
            "category_code": cat_code,
            "cpa_type": cpa_type,
            "avg_payout": avg_payout,
            "base_cpc": base_cpc,
            "PVS_score": total_pvs,
            "source": t.get("source", "trend_scout"),
            "tier_eval": tier_eval
        })

    scored_candidates.sort(key=lambda x: x["PVS_score"], reverse=True)
    winner = scored_candidates[0] if scored_candidates else {}
    return winner

class DemandMatcher:
    def __init__(self):
        pass

    def select_best_topic(self, trends: List[Dict[str, Any]], sub_candidates: Optional[List[str]] = None) -> Dict[str, Any]:
        matched = match_trends_with_demand(trends)
        cat_code = matched.get("category_code", "TECH")
        kw = matched.get("keyword", "2026 청년도약계좌")
        vol = matched.get("traffic_volume", 35000)

        # 서브 키워드 후보가 주어지지 않았거나 메인 키워드와 불일치할 경우, 선정된 메인 키워드로 실시간 자동완성 확장
        if not sub_candidates or not any(kw.split()[0] in sc for sc in sub_candidates):
            try:
                from engine.radar.trend_scout import expand_naver_autocomplete
                sub_candidates = expand_naver_autocomplete(kw, limit=6)
            except Exception:
                sub_candidates = None

        # 7-Tier Keyword Package 구축 (신생 블로그 침투 최적 비율: 문서 650, 발행 120)
        pkg = build_keyword_package(
            main_kw=kw,
            category=cat_code,
            sub_candidates=sub_candidates,
            search_vol=vol,
            doc_count=650,
            monthly_pub=120
        )

        title = generate_optimized_title(main_kw=kw, category=cat_code, subs=pkg["subs"])

        return {
            "keyword": pkg["main"],
            "keyword_package": pkg,
            "subs": pkg["subs"],
            "sub_details": pkg.get("sub_details", []),
            "ratio": pkg["ratio"],
            "tier": pkg["tier"],
            "title": title,
            "traffic_volume": vol,
            "category": cat_code,
            "category_code": cat_code,
            "niche_name": matched.get("niche_name", "스마트 라이프"),
            "intent": "COMMERCIAL",
            "cpc": matched.get("base_cpc", 2500),
            "pvs": matched.get("PVS_score", 5000),
            "avg_payout": matched.get("avg_payout", 30000),
            "cpa_type": matched.get("cpa_type", "CPS_COUPANG")
        }

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    dummy_trends = [
        {"keyword": "로봇청소기 추천", "traffic_volume": 45000},
        {"keyword": "근로장려금 지급일", "traffic_volume": 60000},
        {"keyword": "알뜰폰 요금제 비교", "traffic_volume": 35000}
    ]
    matcher = DemandMatcher()
    winner = matcher.select_best_topic(dummy_trends)
    print("🏆 오늘의 1위 고수익 토픽:")
    print(f" - 제목: {winner['title']}")
    print(f" - 메인 키워드: {winner['keyword']}")
    print(f" - 서브 키워드: {winner['subs']}")
    print(f" - 7티어 판정: {winner['tier']} (골든비율: {winner['ratio']})")
    print(f" - PVS 점수: {winner['pvs']:,.0f}점")


