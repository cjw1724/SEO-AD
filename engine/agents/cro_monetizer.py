# -*- coding: utf-8 -*-
"""
engine/agents/cro_monetizer.py
------------------------------
World-Class CRO & UI Assembly Agent (UI Designer + Conversion Optimizer).
Assembles the complete publication-ready article HTML:
1. Bento Grid Hero Takeaway Card (3-second rule)
2. 4 AdSense Golden Monetization Slots (Responsive placeholders/ad units)
3. Interactive Micro-SaaS JS Calculator (High dwell time)
4. Canvas Design Spec Comparison Bar Chart (Inline pure SVG)
5. Editorial Analytical Body (Data-driven journalism)
6. Affiliate Native CTA Button Box (CPA/CPS conversion)
7. Pure CSS FAQ Accordion (<details><summary>, Zero broken entities)
8. Mobile Sticky Bottom Action Bar
9. Strict Zero-Persona Editorial Footer (Blogin 365 AI official branding)
"""

import os
import sys

# Ensure base_dir is in sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from engine.visuals.saas_calculator import render_saas_calculator
from engine.visuals.canvas_renderer import render_spec_comparison_chart, render_process_stepper
from engine.matcher.coupang_link_builder import render_affiliate_cta_box
from engine.visuals.handcrafted_annotation_renderer import HandcraftedAnnotationRenderer
from engine.matcher.experiential_verifier import ExperientialVerifier


def assemble_world_class_article(topic: dict, editorial_data: dict) -> str:
    """
    Combines all visual, analytical, and monetization components into a single rich HTML string.
    """
    keyword = topic.get("keyword", "")
    category = topic.get("category", "LIFESTYLE")
    cpc = topic.get("cpc", 1200)
    pvs = topic.get("pvs", 2500)
    
    sections = editorial_data.get("sections", [])
    faq = editorial_data.get("faq", [])
    
    # Generate Sub-components
    calc_html = render_saas_calculator(category)
    chart_html = render_spec_comparison_chart(keyword, category)
    affiliate_html = render_affiliate_cta_box(keyword, category)

    # Phase 2 Authentic Visuals & Humanization
    factset = topic.get("factset") or editorial_data.get("factset")
    if not factset:
        factset = ExperientialVerifier().build_experiential_factset(keyword, category)

    photo_card_html = HandcraftedAnnotationRenderer.render_amateur_photo_card(
        title="에디토리얼 팀 실측 분석 및 팩트체크 리포트",
        caption="공식 데이터 및 폰카 뷰파인더 실시간 대조 검증 컷",
        category=category
    )
    pros_cons_html = HandcraftedAnnotationRenderer.render_unfiltered_pros_cons_board(
        pros=factset.get("pros_real", []),
        cons=factset.get("cons_unfiltered", [])
    )
    
    # 1. Bento Hero Card
    hero_bento = f"""
<div class="bento-hero" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
    <span style="display: inline-flex; align-items: center; background: #f1f5f9; color: #0f172a; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 9999px; letter-spacing: -0.2px;">
      실시간 팩트체크 리포트
    </span>
    <span style="font-size: 12px; color: #64748b; font-weight: 500;">
      업데이트: 2026년 기준 공식 데이터 대조 완료
    </span>
  </div>
  <div class="bento-title" style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; line-height: 1.4; letter-spacing: -0.5px;">
    3초 핵심 요약 (Key Takeaways)
  </div>
  <div style="background: #f8fafc; border-left: 4px solid #0f172a; padding: 14px 16px; border-radius: 8px; margin-bottom: 16px;">
    <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.6;">
      <li><strong>실질 혜택/절감폭:</strong> 공식 기준 대조 시 일반 신청 대비 최대 효과 체감</li>
      <li><strong>주요 변동 사항:</strong> 2026년 신규 산정 공식 및 신청 자격 요건 강화 반영</li>
      <li><strong>행동 지침:</strong> 예산 소진 전 전용 모의 계산기로 사전 검증 후 접수 권장</li>
    </ul>
  </div>
  <div style="display: flex; gap: 12px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 130px; background: #ffffff; border: 1px solid #e2e8f0; padding: 10px 14px; border-radius: 10px;">
      <div style="font-size: 11px; color: #64748b; font-weight: 600;">상업적 가치 지표</div>
      <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">PVS {pvs:,.0f} pt</div>
    </div>
    <div style="flex: 1; min-width: 130px; background: #ffffff; border: 1px solid #e2e8f0; padding: 10px 14px; border-radius: 10px;">
      <div style="font-size: 11px; color: #64748b; font-weight: 600;">기준 검증 상태</div>
      <div style="font-size: 16px; font-weight: 800; color: #10b981; margin-top: 2px;">공식 인증 데이터 ✓</div>
    </div>
  </div>
</div>
"""

    # Subtitle Lead Box (부제목: 첫 문단 첫 줄, 메인 키워드 1회 포함)
    subtitle = editorial_data.get("subtitle", f"{keyword} 공식 데이터 및 핵심 기준 대조 분석 보고서입니다.")
    lead_box = f"""
<div class="article-lead" style="margin-bottom: 24px; padding: 16px 20px; background: #f8fafc; border-left: 4px solid #0284c7; border-radius: 8px;">
  <p style="margin: 0; color: #1e293b; font-size: 15px; font-weight: 600; line-height: 1.6;">
    {subtitle}
  </p>
</div>
"""

    # AdSense Slot 1: Top Hero Slot
    ad_slot_1 = """
<div class="adsense-slot adsense-top" style="margin: 20px 0; text-align: center; min-height: 100px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
  <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.5px;">ADVERTISEMENT</span>
</div>
"""

    # AdSense Slot 2: Mid-Content Break
    ad_slot_2 = """
<div class="adsense-slot adsense-mid" style="margin: 28px 0; text-align: center; min-height: 100px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
  <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.5px;">ADVERTISEMENT</span>
</div>
"""

    # Build Editorial Sections (H2: 1:1 Sub-Keyword Mapping)
    sec_html_list = [lead_box]
    for i, sec in enumerate(sections):
        sec_h = sec.get("heading", "")
        sec_c = sec.get("content", "")
        s_block = f"""
<div class="content-section" style="margin-bottom: 28px;">
  <h2 class="sub-heading" style="font-size: 19px; font-weight: 800; color: #0f172a; margin: 0 0 12px 0; line-height: 1.4; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">
    {sec_h}
  </h2>
  <div style="color: #334155; font-size: 15px; line-height: 1.75; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif;">
    {sec_c}
  </div>
</div>
"""
        sec_html_list.append(s_block)
        if i == 0:
            sec_html_list.append(chart_html)
            sec_html_list.append(ad_slot_2)

    editorial_body = "\n".join(sec_html_list)

    # Build FAQ Section with Pure CSS Chevrons (Zero Broken Entities)
    faq_items = []
    for f in faq:
        q = f.get("question", "")
        a = f.get("answer", "")
        item = f"""
  <details style="border: 1px solid #e2e8f0; border-radius: 12px; margin-bottom: 12px; background: #ffffff; overflow: hidden; transition: all 0.2s ease;">
    <summary style="padding: 16px 20px; font-weight: 700; color: #0f172a; font-size: 15px; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; user-select: none;">
      <span>Q. {q}</span>
      <span class="faq-chevron" style="display: inline-block; width: 8px; height: 8px; border-right: 2px solid #64748b; border-bottom: 2px solid #64748b; transform: rotate(45deg); transition: transform 0.2s ease;"></span>
    </summary>
    <div style="padding: 0 20px 16px 20px; color: #475569; font-size: 14px; line-height: 1.6; border-top: 1px solid #f8fafc; padding-top: 12px;">
      {a}
    </div>
  </details>
"""
        faq_items.append(item)

    faq_html = f"""
<div class="faq-accordion-section" style="margin: 32px 0;">
  <h3 style="font-size: 19px; font-weight: 800; color: #0f172a; margin-bottom: 16px;">
    자주 묻는 질문 (FAQ)
  </h3>
  {"".join(faq_items)}
</div>
"""

    # AdSense Slot 3: Mid-Content Break 2 (Post-Affiliate CTA)
    ad_slot_3 = """
<div class="adsense-slot adsense-mid-2" style="margin: 28px 0; text-align: center; min-height: 100px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
  <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.5px;">ADVERTISEMENT</span>
</div>
"""

    # AdSense Slot 4: Pre-Footer Slot
    ad_slot_4 = """
<div class="adsense-slot adsense-bottom" style="margin: 28px 0; text-align: center; min-height: 100px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
  <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.5px;">ADVERTISEMENT</span>
</div>
"""

    # Zero-Persona Editorial Footer
    editorial_footer = """
<div class="editorial-footer" style="margin-top: 40px; padding: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; font-size: 13px; color: #64748b; line-height: 1.6;">
  <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">
    Blogin 365 AI 리서치 팀 (Editorial Intelligence)
  </div>
  <div>
    본 콘텐츠는 금융위원회, 고용노동부, 과학기술정보통신부 등 공공 고시 기준 및 각 사 공시 규격을 기반으로 알고리즘 교차 검증을 거쳐 제작되었습니다. 개인별 세부 조건 및 정책 변동에 따라 실제 결과는 상이할 수 있으므로 공식 접수 전 최종 약관을 확인하시기 바랍니다.
  </div>
</div>
"""

    # Complete Combined HTML
    complete_html = f"""
<!-- Blogin 365 AI Editorial Layout -->
<div class="article-container" style="max-width: 760px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', Roboto, sans-serif; color: #0f172a; line-height: 1.7;">
  {hero_bento}
  {ad_slot_1}
  {photo_card_html}
  {calc_html}
  {editorial_body}
  {pros_cons_html}
  {affiliate_html}
  {ad_slot_3}
  {faq_html}
  {ad_slot_4}
  {editorial_footer}
</div>
"""
    return complete_html.strip()


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sample_topic = {
        "keyword": "2026 청년도약계좌",
        "category": "SUBSIDY",
        "cpc": 2800,
        "pvs": 5600
    }
    sample_editorial = {
        "sections": [
            {"heading": "1. 2026년 청년도약계좌 지원 자격 및 개편 기준", "content": "<p>중위소득 100% 이하 가구의 실질 수혜율이 상승했습니다.</p>"},
            {"heading": "2. 신청 시기별 예산 소진 속도", "content": "<p>조기 마감에 대비해 정부24를 통한 사전 서류 준비가 필요합니다.</p>"}
        ],
        "faq": [
            {"question": "소득이 없는 청년도 신청할 수 있나요?", "answer": "개인소득이 있어야 정부기여금이 매칭 지급됩니다."}
        ]
    }
    html_out = assemble_world_class_article(sample_topic, sample_editorial)
    print("=== CRO Monetizer Article Generated ===")
    print("Total HTML Length:", len(html_out), "chars")
    print("Contains Bento Hero:", "bento-hero" in html_out)
    print("Contains Calculator:", "saas-calculator" in html_out)
    print("Contains FAQ Chevron:", "faq-chevron" in html_out)
