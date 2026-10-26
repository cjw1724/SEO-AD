# -*- coding: utf-8 -*-
"""
engine/matcher/domain_router.py
--------------------------------
Centralized, deterministic domain resolution engine.
Prevents semantic mismatches (e.g. auto insurance vs telecom vs health insurance vs subsidy).
"""

from typing import Dict, Any, List


DOMAIN_AUTO_INSURANCE = "AUTO_INSURANCE"
DOMAIN_HEALTH_INSURANCE = "HEALTH_INSURANCE"
DOMAIN_SUBSIDY = "SUBSIDY"
DOMAIN_TELECOM = "TELECOM"
DOMAIN_CARDS_TRAVEL = "CARDS_TRAVEL"
DOMAIN_SAVINGS = "SAVINGS"
DOMAIN_MEDICAL = "MEDICAL"
DOMAIN_HAIR_TRANSPLANT = "HAIR_TRANSPLANT"
DOMAIN_CAREER = "CAREER"
DOMAIN_TECH = "TECH"


# Domain strict negative anti-contamination dictionaries (철칙 2: 템플릿 오염 0건 강제)
DOMAIN_FORBIDDEN_CONTAMINATION = {
    DOMAIN_HAIR_TRANSPLANT: [
        "임플란트", "치과", "도수치료", "골유착", "치조골 뼈이식", "상악동거상술",
        "지르코니아", "라식", "라섹", "스마일라식", "치아", "보철", "골이식",
        "틀니", "상악동", "치조골", "체외충격파", "도수 치료", "알뜰폰", "유심",
        "esim", "통신비", "자동차보험", "운전자보험"
    ],
    DOMAIN_AUTO_INSURANCE: [
        "알뜰폰", "유심", "esim", "통신비", "임플란트", "치과", "도수치료", "모발이식"
    ],
    DOMAIN_TELECOM: [
        "자동차보험", "운전자보험", "임플란트", "치과", "도수치료", "모발이식"
    ]
}


def get_domain_forbidden_words(domain: str) -> List[str]:
    """Returns strictly prohibited cross-domain words for the given domain."""
    return DOMAIN_FORBIDDEN_CONTAMINATION.get(domain, [])


def classify_domain(keyword: str, category: str = "") -> str:
    """
    Classifies a keyword and category into a precise semantic domain.
    Priority order is strictly calibrated to prevent cross-domain contamination:
    1. Subsidy / Government / Welfare (even if containing '보험' like '건강보험 피부양자' or '숨은 보험금')
    2. Auto / Vehicle Insurance (strictly car/driving insurance)
    3. Health / Life / Indemnity Insurance (실비, 치아, 암 등)
    4. Telecom / SIM / Plan (알뜰폰, 유심, 통신비 등)
    5. Cards / Foreign Exchange / Travel
    6. Medical / Procedures (임플란트, 라식 등)
    7. Career / Education (국비지원, 자격증)
    8. General Fixed Cost Savings / Cashflow (non-telecom)
    9. Tech / Gadgets
    """
    kw_lower = (keyword or "").lower()
    cat_upper = (category or "").upper()

    # 1. SUBSIDY / GOVERNMENT / WELFARE FIRST
    # (High priority: Protects '건강보험 피부양자', '숨은 보험금' from being routed to private insurance)
    subsidy_indicators = [
        "피부양자", "건강보험 피부양자", "건강보험료", "숨은 보험금", "청년도약계좌",
        "근로장려금", "자녀장려금", "부모급여", "국민연금", "기초연금", "신생아 특례대출",
        "버팀목", "지원금", "환급금", "실업급여", "청년주택드림", "아동수당", "생계급여"
    ]
    if any(k in kw_lower for k in subsidy_indicators):
        return DOMAIN_SUBSIDY

    if cat_upper in ["SUBSIDY", "REFUND", "GOVERNMENT"]:
        # Verify it's not explicitly car insurance or telecom
        is_auto = any(k in kw_lower for k in ["자동차", "운전자", "차량"]) and "보험" in kw_lower
        is_tel = any(k in kw_lower for k in ["알뜰폰", "유심", "esim", "통신비"])
        if not is_auto and not is_tel:
            return DOMAIN_SUBSIDY

    # 2. AUTO / VEHICLE INSURANCE
    auto_insurance_indicators = [
        "자동차보험", "운전자보험", "자동차 보험", "운전자 보험",
        "다이렉트자동차", "다이렉트차량", "차량보험", "자동차 다이렉트",
        "차량 다이렉트", "법인자동차보험", "중고차 다이렉트"
    ]
    if any(k in kw_lower for k in auto_insurance_indicators):
        return DOMAIN_AUTO_INSURANCE
    if any(car in kw_lower for car in ["자동차", "운전자", "차량", "자차"]) and any(ins in kw_lower for ins in ["보험", "다이렉트"]):
        return DOMAIN_AUTO_INSURANCE

    # 3. HEALTH / INDEMNITY / LIFE INSURANCE
    health_insurance_indicators = [
        "실비보험", "실손보험", "암보험", "치아보험", "태아보험",
        "펫보험", "화재보험", "여행자보험", "상해보험", "간병보험",
        "수술비보험", "정기보험", "종신보험", "치아 보험", "실비 보험"
    ]
    if any(k in kw_lower for k in health_insurance_indicators):
        return DOMAIN_HEALTH_INSURANCE
    if "보험" in kw_lower and not any(k in kw_lower for k in ["건강보험", "고용보험", "산재보험"]):
        return DOMAIN_HEALTH_INSURANCE

    # 4. EXPLICIT TELECOM
    telecom_indicators = [
        "알뜰폰", "요금제", "통신비", "유심", "esim", "0원 요금제",
        "0원요금제", "통신 3사", "통신사", "자급제 요금제", "데이터 무제한",
        "알뜰 요금제", "셀프 개통", "번호이동"
    ]
    if any(k in kw_lower for k in telecom_indicators):
        return DOMAIN_TELECOM

    # 5. CARDS / TRAVEL / FOREIGN EXCHANGE
    card_indicators = [
        "트래블로그", "트래블월렛", "트래블", "환전", "해외결제",
        "체크카드", "신용카드", "카드 피킹률", "외화 충전"
    ]
    if any(k in kw_lower for k in card_indicators):
        return DOMAIN_CARDS_TRAVEL

    # 6. HAIR TRANSPLANT & HAIR RESTORATION (Dedicated domain isolation - 철칙 2 엄수)
    hair_indicators = [
        "모발이식", "모발 이식", "모낭", "모수", "헤어라인", "헤어라인 교정",
        "m자 탈모", "엠자 탈모", "정수리 탈모", "탈모약", "프로페시아", "아보다트",
        "피나스테리드", "두타스테리드", "미녹시딜", "동반탈락", "암흑기", "대다모",
        "비절개 모발이식", "절개 모발이식", "3000모", "2000모", "4000모", "모낭수",
        "무삭발", "ishrs", "국제모발이식"
    ]
    if any(k in kw_lower for k in hair_indicators):
        return DOMAIN_HAIR_TRANSPLANT

    # 7. GENERAL MEDICAL / DENTAL / PROCEDURES
    procedure_indicators = [
        "임플란트", "라식", "라섹", "스마일라식", "치과", "치아",
        "보철", "비급여", "도수치료", "백내장", "피부과", "성형"
    ]
    if any(k in kw_lower for k in procedure_indicators) or cat_upper in ["MEDICAL", "CLINIC"]:
        return DOMAIN_MEDICAL

    # 8. CAREER / EDUCATION
    career_indicators = [
        "내일배움카드", "국비지원", "직업훈련", "자격증", "손해평가사",
        "공인중개사", "전기기사", "데이터분석"
    ]
    if any(k in kw_lower for k in career_indicators) or cat_upper in ["CAREER", "EDUCATION", "CERT"]:
        return DOMAIN_CAREER

    # 9. GENERAL SAVINGS / CASHFLOW (Fixed costs, non-telecom)
    if cat_upper in ["SAVINGS", "CASHFLOW"] or any(k in kw_lower for k in ["고정비", "생활비", "전기요금", "난방비", "도시가스", "통장 쪼개기", "가계부", "적금"]):
        return DOMAIN_SAVINGS

    # 10. DEFAULT TO TECH
    return DOMAIN_TECH
