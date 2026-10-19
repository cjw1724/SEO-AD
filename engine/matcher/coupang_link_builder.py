import urllib.parse
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from engine.monetization.coupang_api import CoupangPartnersClient, get_coupang_client
from engine.matcher.domain_router import (
    classify_domain,
    DOMAIN_AUTO_INSURANCE,
    DOMAIN_HEALTH_INSURANCE,
    DOMAIN_SUBSIDY,
    DOMAIN_TELECOM,
    DOMAIN_CARDS_TRAVEL,
    DOMAIN_SAVINGS,
    DOMAIN_MEDICAL,
    DOMAIN_CAREER,
    DOMAIN_TECH
)

def build_coupang_search_url(keyword: str, partners_subid: str = "blogin365") -> str:
    """
    키워드 기반 쿠팡 최저가 검색 딥링크를 생성합니다.
    쿠팡 파트너스 API 키가 연동된 경우 HMAC-SHA256 1위 상품 또는 단축 딥링크(link.coupang.com) 생성.
    키가 비어있을 경우 기존 검색 URL로 안전하게 폴백(Fallback).
    """
    clean_keyword = keyword.replace(" 비교", "").replace(" 추천", "").strip()
    client = get_coupang_client()
    if partners_subid:
        client.sub_id = partners_subid
    return client.get_affiliate_search_link(clean_keyword)

def resolve_cpa_type(keyword: str, category: str = "TECH") -> str:
    """
    키워드와 카테고리를 분석하여 최적의 제휴 CPA 유형을 결정합니다.
    도메인 라우터를 기반으로 100% 일관된 매핑을 보장합니다.
    """
    domain = classify_domain(keyword, category)
    if domain in [DOMAIN_AUTO_INSURANCE, DOMAIN_HEALTH_INSURANCE]:
        return "CPA_INSURANCE"
    elif domain == DOMAIN_TELECOM:
        return "CPA_TELECOM"
    elif domain == DOMAIN_CARDS_TRAVEL:
        return "CPA_CARD"
    elif domain == DOMAIN_SUBSIDY:
        return "CPA_REFUND"
    elif domain == DOMAIN_MEDICAL:
        return "CPA_CLINIC"
    elif domain == DOMAIN_CAREER:
        return "CPA_EDUCATION"
    elif domain == DOMAIN_SAVINGS:
        return "CPA_SAVINGS"
    else:
        return "CPS_COUPANG"

def generate_affiliate_cta_button(keyword: str, cpa_type: str = None) -> str:
    """
    본문 중간 및 스펙 비교표 하단에 삽입되는 고전환율 네이티브 CTA 버튼을 생성합니다.
    키워드 도메인과 cpa_type 간 불일치가 감지되면 안전하게 교정합니다.
    """
    clean_kw = keyword.replace(" 비교", "").replace(" 추천", "").strip()
    
    # 도메인 교차 오염 방지: 키워드가 통신이 아닌데 CPA_TELECOM이 넘어온 경우 교정
    resolved_type = resolve_cpa_type(clean_kw)
    if cpa_type == "CPA_TELECOM" and resolved_type != "CPA_TELECOM":
        cpa_type = resolved_type
    elif not cpa_type:
        cpa_type = resolved_type
    
    if cpa_type == "CPS_COUPANG":
        url = build_coupang_search_url(clean_kw)
        btn_label = f"🛒 {clean_kw} 실시간 로켓배송 최저가 확인하기"
        badge_text = "쿠팡 파트너스 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다."
    elif cpa_type == "CPA_INSURANCE":
        url = "https://e-insmarket.or.kr/"
        btn_label = f"🚗 {clean_kw} 보험다모아 공식 최저가 견적 비교하기"
        badge_text = "금융위원회 및 손해보험협회·생명보험협회 공식 포털 '보험다모아'로 연결됩니다."
    elif cpa_type == "CPA_CARD":
        url = "https://www.fss.or.kr/"
        btn_label = f"💳 {clean_kw} 금융감독원 공식 수수료 혜택 비교하기"
        badge_text = "금융감독원 금융상품통합비교포털 공식 링크입니다."
    elif cpa_type == "CPA_REFUND":
        url = "https://www.hometax.go.kr/"
        btn_label = f"🏛️ {clean_kw} 정부 공식 환급금 즉시 조회하기"
        badge_text = "정부 공식 홈택스 및 복지로 포털로 연결됩니다."
    elif cpa_type == "CPA_TELECOM":
        url = "https://www.mvnohub.kr/"
        btn_label = f"📱 {clean_kw} 0원/최저가 요금제 실시간 가입하기"
        badge_text = "알뜰폰허브 공공 포털 및 통신사 공식 링크로 연결됩니다."
    elif cpa_type == "CPA_CLINIC":
        url = "https://www.hira.or.kr/"
        btn_label = f"🏥 {clean_kw} 건강보험심사평가원 비급여 진료비 확인"
        badge_text = "보건복지부 심평원 공식 포털 표준 진료비 정보입니다."
    elif cpa_type == "CPA_SAVINGS":
        url = "https://www.fss.or.kr/"
        btn_label = f"💰 {clean_kw} 금융상품 공식 한눈에 비교하기"
        badge_text = "금융감독원 금융소비자정보포털 파인 공식 링크입니다."
    else:
        url = "https://www.hrd.go.kr/"
        btn_label = f"🎓 {clean_kw} 고용노동부 HRD-Net 국비지원 신청하기"
        badge_text = "고용노동부 직업훈련포털 HRD-Net 공식 링크입니다."
        
    html = f"""
    <div class="editorial-affiliate-box" style="margin:36px auto; max-width:760px; padding:24px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; text-align:center; box-sizing:border-box;">
      <a href="{url}" target="_blank" rel="noopener noreferrer nofollow" class="btn-affiliate-action" style="display:inline-block; width:100%; max-width:480px; padding:16px 24px; background:#2563eb; color:#ffffff; font-size:1.05rem; font-weight:800; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); transition:background 0.2s;">
        {btn_label}
      </a>
      <p style="margin:10px 0 0 0; font-size:0.75rem; color:#94a3b8; font-weight:500;">ⓘ {badge_text}</p>
    </div>
    """
    return html

def render_affiliate_cta_box(keyword: str, category: str = "TECH") -> str:
    cpa_type = resolve_cpa_type(keyword, category)
    return generate_affiliate_cta_button(keyword, cpa_type)
