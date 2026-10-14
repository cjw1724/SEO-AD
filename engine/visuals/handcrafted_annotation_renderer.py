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
        [Patch 2] Deactivated: Mock viewfinder box (AUTO-FOCUS / REC) has been permanently
        deactivated from the publishing pipeline as it does not align with editorial content quality.
        Returns an empty string to ensure zero rendering overhead.
        """
        return ""


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
      📋 에디토리얼 실측 분석 요약
    </span>
    <span style="font-size: 11px; color: #64748b; font-weight: 600;">
      스마트 라이프 에디토리얼 팀
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
    assert card_html == ""  # Verified permanently deactivated
    circle_svg = renderer.render_hand_drawn_circle_svg()
    assert "hand-drawn-marker" in circle_svg
    print("Deactivation and visual components verified!")
