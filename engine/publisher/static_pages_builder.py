# -*- coding: utf-8 -*-
"""
engine/publisher/static_pages_builder.py
------------------------------------------
AdSense Review Mandatory 4 Static Policy & Trust Pages Builder:
1. About Us (회사 및 블로그 공식 소개)
2. Privacy Policy (개인정보처리방침 - Google DART 쿠키, GA4, 제휴 고지 준수)
3. Terms of Service (이용약관 - 저작권, 면책 조항, 공공데이터 출처 명시)
4. Contact Us (고객 문의 및 팩트 오류 제보 창구)

Adheres strictly to:
- Zero-Persona Policy: Official editorial branding (Blogin 365 AI / 스마트 라이프 에디토리얼 팀)
- Zero Broken Entity: Clean UTF-8 text and pure CSS styling
- Responsive Bento Layout: Seamless integration with Blogger theme
"""

from typing import Dict, Any


def build_about_page_html() -> str:
    """회사 및 블로그 공식 소개 페이지 (About Us)"""
    return """
<div class="static-policy-container" style="max-width: 760px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif; color: #0f172a; line-height: 1.75;">
  <!-- Hero Section -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px 24px; margin-bottom: 24px; box-shadow: 0 4px 16px -2px rgba(15,23,42,0.04);">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
      <span style="font-size: 11px; font-weight: 800; color: #2563eb; background: #eff6ff; padding: 4px 10px; border-radius: 9999px;">
        OFFICIAL MEDIA PROFILE
      </span>
      <span style="font-size: 11px; color: #64748b; font-weight: 600;">
        공식 블로그 소개
      </span>
    </div>
    <h1 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; letter-spacing: -0.5px;">
      Blogin 365 AI 소개 (About Us)
    </h1>
    <p style="font-size: 15px; color: #334155; margin: 0; line-height: 1.7;">
      <strong>Blogin 365 AI</strong>는 공공 정책, 금융, 테크, 생활 절약 정보를 데이터 기반으로 분석하고, 누구나 쉽게 이해할 수 있는 실시간 인터랙티브 모의 계산 솔루션을 제공하는 독립 디지털 미디어입니다.
    </p>
  </div>

  <!-- Editorial Mission & Pillars -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 18px; font-weight: 800; color: #0f172a; margin: 0 0 16px 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">
      1. 에디토리얼 미션 (Our Mission)
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 16px; line-height: 1.7;">
      복잡한 정부 지원금 기준, 매년 개편되는 세제 혜택, 난해한 금융 상품의 세부 약관은 국민 개개인이 직접 혜택을 챙기기 어렵게 만듭니다. Blogin 365 AI는 소관 부처의 공식 고시 규격과 시장 표준 데이터를 교차 검증하여, 독자가 3초 만에 핵심 결론을 파악하고 직접 계산해볼 수 있는 투명한 정보 환경을 구축합니다.
    </p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
        <div style="font-size: 13px; font-weight: 800; color: #2563eb; margin-bottom: 4px;">공식 고시 팩트 대조</div>
        <div style="font-size: 12px; color: #64748b; line-height: 1.6;">정부24, 국세청, 금융위원회 등 소관 기관 공식 공고문을 원천 데이터로 채택합니다.</div>
      </div>
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
        <div style="font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">인터랙티브 모의 계산기</div>
        <div style="font-size: 12px; color: #64748b; line-height: 1.6;">단순 텍스트 나열을 배제하고 즉각적인 수치 시뮬레이션을 지원합니다.</div>
      </div>
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
        <div style="font-size: 13px; font-weight: 800; color: #10b981; margin-bottom: 4px;">무결점 편집 원칙</div>
        <div style="font-size: 12px; color: #64748b; line-height: 1.6;">가상 인물이나 허위 과장 표현을 엄격히 배제하는 공식 에디토리얼 규범을 준수합니다.</div>
      </div>
    </div>
  </div>

  <!-- Editorial Team Profile -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 18px; font-weight: 800; color: #0f172a; margin: 0 0 16px 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">
      2. 편집국 조직 및 운영 체계 (Editorial Team)
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 14px; line-height: 1.7;">
      Blogin 365 AI의 모든 분석 리포트는 <strong>스마트 라이프 에디토리얼 팀 (Smart Life Editorial Team)</strong> 공식 명의로 기획 및 감수됩니다. 개인 저자의 편향이나 이해관계 충돌을 방지하기 위해 엄격한 데이터 대조 가이드라인을 적용하고 있습니다.
    </p>
    <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #334155; line-height: 1.8;">
      <li><strong>리서치 랩</strong>: 공공 고시 개정안 추적 및 정책 자격 요건 정밀 대조</li>
      <li><strong>엔지니어링 팀</strong>: 클라이언트 사이드 반응형 Micro-SaaS 시뮬레이터 개발</li>
      <li><strong>QA 검수팀</strong>: 엔티티 무결성 검증, 안티스팸 가이드라인 점검 및 링크 유효성 상시 모니터링</li>
    </ul>
  </div>

  <!-- Contact & Location Box -->
  <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; font-size: 13px; color: #64748b;">
    <div style="font-weight: 700; color: #0f172a; margin-bottom: 6px;">공식 문의 및 운영 안내</div>
    <div>공식 웹사이트: <a href="https://blogin365ai.blogspot.com" style="color: #2563eb; text-decoration: none;">blogin365ai.blogspot.com</a></div>
    <div>문의 및 제보 이메일: <a href="mailto:blogin365ai@gmail.com" style="color: #2563eb; text-decoration: none;">blogin365ai@gmail.com</a></div>
    <div style="margin-top: 6px; font-size: 12px; color: #94a3b8;">최종 업데이트: 2026년 10월 19일 · Blogin 365 AI All Rights Reserved.</div>
  </div>
</div>
""".strip()


def build_privacy_page_html() -> str:
    """개인정보처리방침 (Privacy Policy) - 구글 애드센스, 쿠키, GA4, 제휴 고지 준수"""
    return """
<div class="static-policy-container" style="max-width: 760px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif; color: #0f172a; line-height: 1.75;">
  <!-- Header Card -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px 24px; margin-bottom: 24px; box-shadow: 0 4px 16px -2px rgba(15,23,42,0.04);">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
      <span style="font-size: 11px; font-weight: 800; color: #2563eb; background: #eff6ff; padding: 4px 10px; border-radius: 9999px;">
        PRIVACY &amp; DATA PROTECTION
      </span>
      <span style="font-size: 11px; color: #64748b; font-weight: 600;">
        개인정보보호법 및 글로벌 표준 준수
      </span>
    </div>
    <h1 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; letter-spacing: -0.5px;">
      개인정보처리방침 (Privacy Policy)
    </h1>
    <p style="font-size: 14px; color: #334155; margin: 0; line-height: 1.7;">
      <strong>Blogin 365 AI</strong>(이하 "본 사이트")는 이용자의 개인정보를 매우 소중하게 생각하며, 대한민국의 「개인정보 보호법」 및 구글(Google)의 게시자 정책을 철저히 준수합니다. 본 방침은 본 사이트를 이용하실 때 수집되는 정보의 유형과 이용 목적, 보호 조치에 대해 설명합니다.
    </p>
  </div>

  <!-- Content Sections -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      1. 개인정보 수집 항목 및 수집 방법
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 12px; line-height: 1.7;">
      본 사이트는 별도의 회원가입 없이 모든 정보성 콘텐츠 및 모의 계산기를 전면 무료로 열람하실 수 있습니다. 따라서 주민등록번호, 계좌번호, 주소 등 민감한 개인 식별 정보를 일체 요구하거나 수집하지 않습니다.
    </p>
    <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #475569; line-height: 1.8;">
      <li><strong>자동 수집 데이터</strong>: 방문 일시, 접속 IP 주소, 브라우저 종류, 운영체제, 이전 참조 URL(리퍼러) 등 웹 서버 표준 통계 로그.</li>
      <li><strong>문의 시 수집 데이터</strong>: 이용자가 문의하기 채널(이메일)을 통해 자발적으로 제공하는 이메일 주소 및 문의 내용.</li>
    </ul>
  </div>

  <!-- AdSense & Cookies Clause (Strict AdSense Mandatory Requirement) -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px; border-left: 4px solid #2563eb;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      2. 쿠키(Cookie) 및 구글 애드센스(Google AdSense) 관련 고지
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 12px; line-height: 1.7;">
      본 사이트는 이용자에게 최적화된 서비스 환경을 제공하고 관련성 높은 정보를 전달하기 위해 쿠키(Cookie)를 사용합니다.
    </p>
    <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #475569; line-height: 1.8;">
      <li><strong>구글 애드센스(Google AdSense)</strong>: Google을 포함한 제3자 광고 공급업체는 이용자가 본 웹사이트 또는 다른 웹사이트를 이전에 방문한 내역을 바탕으로 광고를 게재하기 위해 쿠키(DoubleClick DART 쿠키 포함)를 사용합니다.</li>
      <li><strong>맞춤형 광고 해제(Opt-Out)</strong>: 이용자는 <a href="https://adssettings.google.com" target="_blank" rel="noopener" style="color: #2563eb; font-weight: 600;">Google 광고 설정</a> 또는 <a href="https://www.aboutads.info/choices" target="_blank" rel="noopener" style="color: #2563eb; font-weight: 600;">www.aboutads.info</a>를 방문하여 맞춤 광고에 사용되는 제3자 쿠키 사용을 직접 차단 및 거부하실 수 있습니다.</li>
      <li><strong>구글 애널리틱스(GA4)</strong>: 웹사이트 트래픽 통계 및 독자 콘텐츠 선호도 분석을 위해 익명화된 식별자를 사용합니다.</li>
    </ul>
  </div>

  <!-- Affiliate Notice -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      3. 제휴 마케팅 링크 안내
    </h2>
    <p style="font-size: 14px; color: #475569; margin: 0; line-height: 1.7;">
      본 사이트의 일부 콘텐츠에는 공정거래위원회의 「추천·보증 등에 관한 표시·광고 심사지침」에 따라 제휴 마케팅 링크(예: 쿠팡 파트너스 등)가 포함될 수 있습니다. 제휴 링크 클릭 시 제휴 플랫폼의 정책에 따른 임시 추적 쿠키가 생성될 수 있으며, 이는 이용자의 개인정보를 침해하지 않는 고유 전환 식별자만을 처리합니다.
    </p>
  </div>

  <!-- Cookie Control Guide -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      4. 쿠키 설치 거부 및 삭제 방법
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 12px; line-height: 1.7;">
      이용자는 웹 브라우저의 옵션을 설정하여 모든 쿠키를 허용하거나, 쿠키가 저장될 때마다 확인을 거치거나, 모든 쿠키의 저장을 거부할 수 있는 선택권을 가집니다.
    </p>
    <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #64748b; line-height: 1.8;">
      <li><strong>Chrome</strong>: 설정 &gt; 개인정보 보호 및 보안 &gt; 서드 파티 쿠키 &gt; 타사 쿠키 차단</li>
      <li><strong>Edge</strong>: 설정 &gt; 쿠키 및 사이트 권한 &gt; 쿠키 및 사이트 데이터 관리 및 삭제</li>
      <li><strong>Safari</strong>: 환경설정 &gt; 개인정보 보호 &gt; 모든 쿠키 차단</li>
    </ul>
  </div>

  <!-- Responsible Officer -->
  <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; font-size: 13px; color: #64748b;">
    <div style="font-weight: 700; color: #0f172a; margin-bottom: 6px;">5. 개인정보보호 책임자 및 연락처</div>
    <div>부서: Blogin 365 AI 정보보호 에디토리얼 팀</div>
    <div>전자우편: <a href="mailto:blogin365ai@gmail.com" style="color: #2563eb; text-decoration: none;">blogin365ai@gmail.com</a></div>
    <div>본 개인정보처리방침은 2026년 10월 19일부터 적용됩니다.</div>
  </div>
</div>
""".strip()


def build_terms_page_html() -> str:
    """이용약관 (Terms of Service) - 저작권, 면책 조항, 공공데이터 출처 명시"""
    return """
<div class="static-policy-container" style="max-width: 760px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif; color: #0f172a; line-height: 1.75;">
  <!-- Header Card -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px 24px; margin-bottom: 24px; box-shadow: 0 4px 16px -2px rgba(15,23,42,0.04);">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
      <span style="font-size: 11px; font-weight: 800; color: #2563eb; background: #eff6ff; padding: 4px 10px; border-radius: 9999px;">
        TERMS &amp; CONDITIONS
      </span>
      <span style="font-size: 11px; color: #64748b; font-weight: 600;">
        서비스 이용 기본 약관
      </span>
    </div>
    <h1 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; letter-spacing: -0.5px;">
      서비스 이용약관 (Terms of Service)
    </h1>
    <p style="font-size: 14px; color: #334155; margin: 0; line-height: 1.7;">
      본 약관은 <strong>Blogin 365 AI</strong>(이하 "본 사이트")가 제공하는 온라인 정보 및 대화형 시뮬레이션 계산 서비스의 이용 조건, 절차 및 이용자와 사이트 간의 권리·의무 사항을 규정함을 목적으로 합니다.
    </p>
  </div>

  <!-- Terms Clauses -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      제1조 (서비스의 성격 및 목적)
    </h2>
    <p style="font-size: 14px; color: #475569; margin: 0; line-height: 1.7;">
      본 사이트는 정부 부처 공공 고시, 금융 공시, 테크 규격 데이터를 바탕으로 독자의 합리적인 의사결정을 지원하는 순수 정보성 에디토리얼과 인터랙티브 SaaS 모의 계산기를 비상업적 무료 열람 형태로 제공합니다.
    </p>
  </div>

  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      제2조 (지적재산권 및 저작권)
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 12px; line-height: 1.7;">
      1. 본 사이트에 게재된 모든 독창적 저작물(분석 원고, 텍스트, 인라인 SVG 스펙 차트, 인터랙티브 JS 계산기 위젯 등)에 대한 저작권 및 지적재산권은 Blogin 365 AI에 귀속됩니다.
    </p>
    <p style="font-size: 14px; color: #475569; margin: 0; line-height: 1.7;">
      2. 이용자는 본 사이트의 사전 서면 승낙 없이 본 사이트의 콘텐츠를 복제, 송신, 출판, 배포, 방송 기타 방법에 의하여 영리 목적으로 이용하거나 제3자에게 이용하게 하여서는 안 됩니다. (출처를 명시한 비영리적 단순 인용은 가능합니다.)
    </p>
  </div>

  <!-- Disclaimer Section (Crucial for AdSense & Legal Protection) -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px; border-left: 4px solid #f59e0b;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      제3조 (정보의 정확성 및 법적 면책 조항 / Disclaimer)
    </h2>
    <p style="font-size: 14px; color: #475569; margin-bottom: 12px; line-height: 1.7;">
      1. 본 사이트의 에디토리얼 팀은 최신 공공 고시 및 공식 약관을 반영하기 위해 정기적인 검증을 수행하나, 정부 정책의 수시 개정, 금융기관의 세부 상품 약관 변경, 개별 이용자의 고유 자격 요건(소득 인정액, 가구 구성 등)에 따라 실제 결과는 본 사이트의 모의 계산 및 분석과 상이할 수 있습니다.
    </p>
    <p style="font-size: 14px; color: #475569; margin: 0; line-height: 1.7;">
      2. 본 사이트에서 제공하는 정보는 법률적, 재정적, 세무적 최종 자문이 아니며, 참고 자료로만 활용되어야 합니다. 최종 신청이나 계약 전 소관 부처(정부24, 복지로, 국세청 등) 또는 금융사 공식 창구를 통해 세부 사항을 직접 확인하시기 바라며, 본 사이트의 정보만을 신뢰하여 발생한 일체의 직접적·간접적 손해에 대해 본 사이트는 법적 책임을 부담하지 않습니다.
    </p>
  </div>

  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px 24px; margin-bottom: 24px;">
    <h2 style="font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px;">
      제4조 (준거법 및 재판관할)
    </h2>
    <p style="font-size: 14px; color: #475569; margin: 0; line-height: 1.7;">
      본 약관의 해석 및 본 사이트 이용과 관련하여 발생한 분쟁에 대해서는 대한민국 법률을 준거법으로 하며, 관할 법원은 민사소송법상의 관할 법원으로 합니다.
    </p>
  </div>

  <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; font-size: 13px; color: #64748b;">
    <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">부칙</div>
    <div>본 약관은 2026년 10월 19일부터 효력이 발생합니다.</div>
  </div>
</div>
""".strip()


def build_contact_page_html() -> str:
    """고객 문의 및 팩트 오류 제보 창구 (Contact Us)"""
    return """
<div class="static-policy-container" style="max-width: 760px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif; color: #0f172a; line-height: 1.75;">
  <!-- Header Card -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px 24px; margin-bottom: 24px; box-shadow: 0 4px 16px -2px rgba(15,23,42,0.04);">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
      <span style="font-size: 11px; font-weight: 800; color: #2563eb; background: #eff6ff; padding: 4px 10px; border-radius: 9999px;">
        COMMUNICATION HUB
      </span>
      <span style="font-size: 11px; color: #64748b; font-weight: 600;">
        공식 소통 및 팩트 제보
      </span>
    </div>
    <h1 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; letter-spacing: -0.5px;">
      문의하기 (Contact Us)
    </h1>
    <p style="font-size: 14px; color: #334155; margin: 0; line-height: 1.7;">
      Blogin 365 AI 에디토리얼 팀은 독자 여러분의 의견과 제보를 환영합니다. 게재된 정보의 오류 정정 요청, 미디어 제휴 문의, 또는 추가적인 분석 요청은 공식 채널을 통해 언제든지 접수해 주시기 바랍니다.
    </p>
  </div>

  <!-- Channel Cards -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;">
    <!-- Fact Check Channel -->
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px;">
      <div style="font-size: 20px; margin-bottom: 8px;">🔍</div>
      <h2 style="font-size: 16px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">
        팩트 오류 수정 제보
      </h2>
      <p style="font-size: 13px; color: #475569; margin-bottom: 12px; line-height: 1.6;">
        정책 개정이나 최신 공시로 인해 기사 내 수치나 자격 조건에 변동이 있을 경우 제보해 주시면, 에디토리얼 팀이 즉시 원본 대조 후 24시간 이내 업데이트를 반영합니다.
      </p>
      <div style="font-size: 13px; font-weight: 700; color: #2563eb;">
        blogin365ai@gmail.com
      </div>
    </div>

    <!-- Media & Partnership Channel -->
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px;">
      <div style="font-size: 20px; margin-bottom: 8px;">🤝</div>
      <h2 style="font-size: 16px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">
        미디어 제휴 및 비즈니스
      </h2>
      <p style="font-size: 13px; color: #475569; margin-bottom: 12px; line-height: 1.6;">
        데이터 인용, 공동 기획 리서치, 테크 시뮬레이터 임베드 제휴 등 공식 비즈니스 협력 관련 제안을 접수합니다.
      </p>
      <div style="font-size: 13px; font-weight: 700; color: #2563eb;">
        blogin365ai@gmail.com
      </div>
    </div>
  </div>

  <!-- Response Guideline -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 24px;">
    <h2 style="font-size: 16px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0;">
      운영 시간 및 응답 기준
    </h2>
    <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #475569; line-height: 1.8;">
      <li><strong>운영 시간</strong>: 평일 09:00 ~ 18:00 (KST, 대한민국 표준시)</li>
      <li><strong>응답 소요 기간</strong>: 영업일 기준 24~48시간 이내 회신 (긴급 팩트 오류 제보는 최우선 검토)</li>
      <li><strong>공식 발행처</strong>: Blogin 365 AI (스마트 라이프 에디토리얼 랩)</li>
    </ul>
  </div>

  <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px 24px; font-size: 13px; color: #64748b; text-align: center;">
    Blogin 365 AI는 투명하고 정확한 공공 데이터 저널리즘을 추구합니다.
  </div>
</div>
""".strip()


def get_mandatory_static_pages() -> Dict[str, Dict[str, str]]:
    """애드센스 심사 통과를 위한 4대 필수 정적 페이지 패키지"""
    return {
        "about": {
            "title": "About Us - Blogin 365 AI",
            "slug": "about",
            "html": build_about_page_html()
        },
        "privacy": {
            "title": "Privacy Policy - 개인정보처리방침",
            "slug": "privacy",
            "html": build_privacy_page_html()
        },
        "terms": {
            "title": "Terms of Service - 이용약관",
            "slug": "terms",
            "html": build_terms_page_html()
        },
        "contact": {
            "title": "Contact Us - 고객 문의 및 오류 제보",
            "slug": "contact",
            "html": build_contact_page_html()
        }
    }
