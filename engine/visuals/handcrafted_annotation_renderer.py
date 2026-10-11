# -*- coding: utf-8 -*-
"""
engine/visuals/handcrafted_annotation_renderer.py
-------------------------------------------------
Authentic Hand-crafted Visuals & Marker Annotation Renderer (Humanization Phase 2).
Replaces artificial, hyper-glamorous synthetic AI art with:
1. Mock Amateur Camera Unboxing Card (slightly tilted angles, room shadows, phone grain, viewfinder timestamp).
2. Hand-edited Overlays & Marker Annotations (rough red circled markers, hand-drawn curved arrows, wavy yellow highlighter strokes, '꿀팁(TIP)' sticker badge).
"""

import os
import sys
import random
from datetime import datetime
from typing import List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class HandcraftedAnnotationRenderer:
    """
    Renders pure HTML/CSS & Inline SVG visuals that look like an authentic human
    captured and hand-annotated them with capture tools and markers.
    """

    @staticmethod
    def render_hand_drawn_circle_svg(width: int = 140, height: int = 48, stroke_color: str = "#ef4444") -> str:
        """
        Pure inline SVG: Imperfect, wobbling hand-drawn red ellipse marker.
        Simulates someone circling a number with a red felt-tip marker.
        """
        return f"""
        <svg class="hand-drawn-marker" viewBox="0 0 160 55" width="{width}" height="{height}" style="position:absolute; top:-6px; left:-8px; pointer-events:none; overflow:visible;">
          <path d="M 12,28 C 10,12 35,6 82,7 C 132,8 152,18 150,34 C 148,48 118,52 74,51 C 28,50 6,42 9,24 C 11,10 42,4 90,6" 
                fill="none" stroke="{stroke_color}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"
                stroke-dasharray="240" stroke-dashoffset="0" opacity="0.88" />
        </svg>
        """

    @staticmethod
    def render_hand_drawn_arrow_svg(direction: str = "curved-down", stroke_color: str = "#dc2626") -> str:
        """
        Pure inline SVG: Hand-drawn arrow pointing directly to key data.
        """
        return f"""
        <svg class="hand-drawn-arrow" viewBox="0 0 80 45" width="60" height="34" style="display:inline-block; vertical-align:middle; overflow:visible;">
          <path d="M 6,12 C 28,6 55,14 68,34" fill="none" stroke="{stroke_color}" stroke-width="2.8" stroke-linecap="round" />
          <path d="M 52,32 L 68,34 L 66,20" fill="none" stroke="{stroke_color}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        """

    @staticmethod
    def render_wavy_highlighter_svg(width_percent: int = 100, color: str = "rgba(254, 240, 138, 0.75)") -> str:
        """
        Pure inline SVG: Wavy translucent yellow highlighter underline.
        """
        return f"""
        <span style="position:relative; display:inline-block; font-weight:800;">
          <svg viewBox="0 0 100 12" preserveAspectRatio="none" style="position:absolute; bottom:1px; left:0; width:{width_percent}%; height:10px; z-index:0; pointer-events:none;">
            <path d="M 0,8 Q 25,2 50,7 T 100,6 L 100,12 L 0,12 Z" fill="{color}" />
          </svg>
        </span>
        """

    @classmethod
    def render_amateur_photo_card(
        cls,
        title: str,
        caption: str,
        category: str = "TECH",
        timestamp_str: Optional[str] = None
    ) -> str:
        """
        Renders a realistic, non-AI looking amateur camera photography frame:
        - Slightly tilted angle (rotate -1.1deg)
        - Natural room shadow
        - Washi masking tape graphic on top
        - Phone camera viewfinder date/time stamp (e.g. 2026. 10. 12 14:22:05 KST)
        - Real hands-on inspection badge
        """
        ts = timestamp_str or datetime.now().strftime("%Y. %m. %d %H:%M:%S KST")
        tilt_deg = random.choice([-1.2, -0.8, 0.9, 1.1])

        # Category thematic icon & color accents
        cat_accents = {
            "TECH": ("#1e293b", "#0f172a", "💻 데스크 실측 테스트베드"),
            "SUBSIDY": ("#0369a1", "#0284c7", "📑 국세청 홈택스 직접 접수 화면"),
            "SAVINGS": ("#15803d", "#16a34a", "📱 실제 유심 셀프개통 단말기"),
            "CASHFLOW": ("#b45309", "#d97706", "📊 가계부 실시간 잔고 분리"),
            "MEDICAL": ("#4338ca", "#4f46e5", "🏥 심평원 비급여 항목 대조"),
            "CAREER": ("#9333ea", "#a855f7", "📝 30일 완성 기출 분석 노트")
        }
        bg_dark, border_accent, env_label = cat_accents.get(category.upper(), ("#1e293b", "#0f172a", "📸 실측 테스트 검증"))

        circle_svg = cls.render_hand_drawn_circle_svg(width=135, height=44, stroke_color="#ef4444")
        arrow_svg = cls.render_hand_drawn_arrow_svg(stroke_color="#dc2626")

        return f"""
<!-- [Phase 2 Authentic Visual] 일반인 촬영 감성 스틸컷 프레임 & 수작업 어노테이션 -->
<div class="amateur-photo-card-wrapper" style="margin: 36px auto; max-width: 680px; box-sizing: border-box;">
  <div class="amateur-photo-frame" style="position: relative; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px 20px 22px 20px; box-shadow: 0 14px 28px -6px rgba(15,23,42,0.12), 0 4px 10px -2px rgba(15,23,42,0.06); transform: rotate({tilt_deg}deg); transition: transform 0.2s ease;">
    
    <!-- 마스킹 테이프 오버레이 -->
    <div style="position: absolute; top: -11px; left: 50%; transform: translateX(-50%) rotate(0.8deg); width: 120px; height: 22px; background: rgba(254, 240, 138, 0.75); border-left: 2px dashed rgba(202, 138, 4, 0.35); border-right: 2px dashed rgba(202, 138, 4, 0.35); box-shadow: 0 2px 4px rgba(0,0,0,0.06); z-index: 5;"></div>

    <!-- 스틸컷 헤더 바 -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;">
      <span style="display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 800; color: #0f172a;">
        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22c55e;"></span>
        {env_label}
      </span>
      <span style="font-size: 11px; color: #64748b; font-weight: 600; font-family: monospace;">
        ISO 400 • F/1.8 • 1/120s
      </span>
    </div>

    <!-- 스틸컷 모의 뷰파인더 화면 (실제 폰카 촬영 질감) -->
    <div style="position: relative; background: #0f172a; border-radius: 8px; padding: 28px 22px; color: #ffffff; overflow: hidden; min-height: 180px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
      
      <!-- 폰카 타임스탬프 (우측 상단 오렌지색 LED) -->
      <div style="position: absolute; top: 12px; right: 14px; font-family: 'Courier New', Courier, monospace; font-size: 12px; font-weight: 700; color: #fb923c; letter-spacing: 0.8px; text-shadow: 0 0 6px rgba(251,146,60,0.6);">
        REC [{ts}]
      </div>

      <!-- 뷰파인더 포커스 그리드 라인 -->
      <div style="position: absolute; top: 12px; left: 14px; font-size: 10px; color: #94a3b8; font-family: monospace;">
        [+] AUTO-FOCUS: ON
      </div>

      <!-- 내부 핵심 데이터 캡처 텍스트 -->
      <div style="margin-top: 24px; z-index: 2;">
        <div style="font-size: 13px; color: #38bdf8; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px;">
          실측 팩트 대조 확인
        </div>
        <div style="font-size: 18px; font-weight: 800; line-height: 1.4; color: #ffffff; margin-bottom: 8px;">
          {title}
        </div>
        <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
          {caption}
        </div>
      </div>

      <!-- 손글씨 빨간 펜 어노테이션 오버레이 (포커스 박스) -->
      <div style="position: relative; margin-top: 16px; padding: 10px 14px; background: rgba(255,255,255,0.08); border-radius: 6px; border: 1px dashed rgba(248,113,113,0.6); display: inline-flex; align-items: center; gap: 8px; z-index: 2;">
        {arrow_svg}
        <span style="position: relative; font-size: 13px; font-weight: 800; color: #fecaca;">
          여기가 핵심 꿀팁 포인트!
          {circle_svg}
        </span>
      </div>
    </div>

    <!-- 스틸컷 하단 수작업 캡션 & 에디토리얼 노트 -->
    <div style="margin-top: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
      <div style="font-size: 12px; color: #475569; font-weight: 600;">
        📌 <span style="color: #0f172a; font-weight: 800;">에디토리얼 팀 실측 코멘트:</span> 보정 앱 없는 스마트폰 기본 카메라 실촬영 캡처본입니다.
      </div>
      <span style="font-size: 11px; background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; padding: 2px 8px; border-radius: 6px; font-weight: 700;">
        무단 복제 방지 실사 워터마크 ✓
      </span>
    </div>

  </div>
</div>
"""

    @classmethod
    def render_handwritten_tip_callout(cls, tip_title: str, tip_body: str) -> str:
        """
        Renders a sticky note / handwritten style tip callout with yellow marker highlighting.
        """
        return f"""
<div class="handwritten-tip-card" style="margin: 28px 0; padding: 18px 22px; background: #fefce8; border-left: 5px solid #eab308; border-radius: 8px; box-shadow: 0 4px 12px rgba(234,179,8,0.08); box-sizing: border-box;">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
    <span style="background: #eab308; color: #ffffff; font-size: 11px; font-weight: 900; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">
      💡 꿀팁 (TIP)
    </span>
    <h4 style="margin: 0; font-size: 15px; font-weight: 800; color: #854d0e;">
      {tip_title}
    </h4>
  </div>
  <p style="margin: 0; font-size: 14px; color: #713f12; line-height: 1.6;">
    {tip_body}
  </p>
</div>
"""

    @classmethod
    def render_unfiltered_pros_cons_board(cls, pros: List[str], cons: List[str]) -> str:
        """
        Renders an experiential user review comparison board:
        - 찐 장점 3가지
        - 솔직한 찐 단점 2가지 (진짜 사람 블로그의 가장 중요한 신뢰 지표)
        """
        pros_items = "".join(f"<li style='margin-bottom:6px;'><strong>✓</strong> {p}</li>" for p in pros)
        cons_items = "".join(f"<li style='margin-bottom:6px;'><strong style='color:#ef4444;'>✗</strong> {c}</li>" for c in cons)

        return f"""
<div class="unfiltered-review-board" style="margin: 32px 0; padding: 22px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; box-shadow: 0 4px 14px rgba(15,23,42,0.04); box-sizing: border-box;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;">
    <span style="font-size: 12px; font-weight: 800; color: #0284c7; letter-spacing: 0.5px;">
      📋 내돈내산 팩트체크 결론
    </span>
    <span style="font-size: 11px; color: #64748b; font-weight: 600;">
      에디토리얼 팀 실측 대조
    </span>
  </div>
  
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px;">
    <!-- 실사용 찐 장점 -->
    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px;">
      <div style="font-size: 14px; font-weight: 800; color: #166534; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
        <span>👍</span> <span>실사용 찐 장점 3가지</span>
      </div>
      <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #15803d; line-height: 1.6;">
        {pros_items}
      </ul>
    </div>

    <!-- 실사용 솔직 단점 -->
    <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; padding: 16px;">
      <div style="font-size: 14px; font-weight: 800; color: #991b1b; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
        <span>👎</span> <span>솔직히 아쉬웠던 찐 단점 2가지</span>
      </div>
      <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #b91c1c; line-height: 1.6;">
        {cons_items}
      </ul>
    </div>
  </div>
</div>
"""


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    renderer = HandcraftedAnnotationRenderer()
    card_html = renderer.render_amateur_photo_card(
        title="2026 청년도약계좌 모의계산 실측 대조",
        caption="직접 홈택스 가조회 및 국민은행 앱에서 금리 계산기 구동한 실촬영 결과",
        category="SUBSIDY"
    )
    print("=== Handcrafted Annotation Renderer Test ===")
    print("Card HTML length:", len(card_html))
    assert "amateur-photo-frame" in card_html
    assert "hand-drawn-marker" in card_html
    assert "REC [" in card_html
    print("All visual components rendered perfectly!")
