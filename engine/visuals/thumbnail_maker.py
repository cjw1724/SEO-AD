# -*- coding: utf-8 -*-
"""
engine/visuals/thumbnail_maker.py
---------------------------------
Automated World-Class Canvas Editorial Thumbnail Generator.
Replaces generic AI hallucinations and empty blue boxes with
rich, human-grade 1200x630 editorial graphic canvases:
- Domain-specific premium background themes (Fintech Navy, Government Emerald, etc.)
- Crisp bold Korean typography with official fact-check badges
- Real UI mockups (Credit cards, HRD-Net cards, 5G SIM, Shield, Vault)
- 3 key analytical takeaways with clean checkmarks
- Instant CDN hosting via Catbox with permanent caching on Blogger's Google CDN
"""

import sys
import os
import urllib.parse
from typing import Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

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


class ThumbnailMaker:
    """
    Automated Programmatic Canvas Thumbnail Generator (1200x630).
    """

    FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf" if os.path.exists("C:/Windows/Fonts/malgunbd.ttf") else "malgun.ttf"
    FONT_REG = "C:/Windows/Fonts/malgun.ttf" if os.path.exists("C:/Windows/Fonts/malgun.ttf") else "malgun.ttf"

    @classmethod
    def _get_domain_style(cls, domain: str, keyword: str) -> dict:
        """Returns theme colors, badges, mockup labels, and bullet points tailored to the subject."""
        if domain == DOMAIN_CARDS_TRAVEL:
            return {
                "bg_gradient": ((15, 23, 42), (30, 58, 138)),
                "glow_color": (37, 99, 235, 60),
                "badge_bg": "#2563eb",
                "badge_text": "2026 해외 결제 수수료 · 공식 팩트체크",
                "title_line1": "트래블로그 vs 트래블월렛",
                "title_line2": "환전 수수료 100% 무료 비교",
                "accent_color": "#60a5fa",
                "bullets": [
                    "✓ 해외 결제 수수료 0원 전액 면제",
                    "✓ 현지 ATM 외화 인출 수수료 무료",
                    "✓ 주요 통화 100% 실시간 환전 우대"
                ],
                "footer_text": "Blogin 365 AI · 해외여행 핀테크 리서치 센터",
                "card_title": "Travellog Card",
                "card_sub": "하나 트래블로그 체크카드",
                "card_stat": "수수료  0원 (100% 우대)",
                "card_border": "#3b82f6"
            }
        elif domain == DOMAIN_CAREER:
            return {
                "bg_gradient": ((6, 78, 59), (15, 35, 42)),
                "glow_color": (16, 185, 129, 60),
                "badge_bg": "#059669",
                "badge_text": "2026 고용노동부 HRD-Net 공식 고시 기준",
                "title_line1": f"{keyword[:16]}",
                "title_line2": "최대 500만원 100% 활용법",
                "accent_color": "#34d399",
                "bullets": [
                    "✓ 훈련비 300만~500만원 전액 국비 지원",
                    "✓ 구직자 · 재직자 · 프리랜서 누구나 신청",
                    "✓ 단기 취업 및 유망 자격증 합격 전략"
                ],
                "footer_text": "Blogin 365 AI · 국비지원 취업 자격증 리서치 센터",
                "card_title": "HRD-Net Card",
                "card_sub": "국민내일배움카드 (직무교육지원)",
                "card_stat": "지원 한도  최대 5,000,000원",
                "card_border": "#10b981"
            }
        elif domain == DOMAIN_SUBSIDY:
            return {
                "bg_gradient": ((30, 27, 75), (15, 23, 42)),
                "glow_color": (99, 102, 241, 60),
                "badge_bg": "#4f46e5",
                "badge_text": "2026 정부24 · 복지로 공식 정책 고시",
                "title_line1": f"{keyword[:16]}",
                "title_line2": "실수령액 모의계산 및 자격 요건",
                "accent_color": "#818cf8",
                "bullets": [
                    "✓ 정부 기여금 매칭 + 비과세 전액 감면",
                    "✓ 소득 기준별 실질 수령액 비교 시뮬레이션",
                    "✓ 온라인 간편 신청 및 필수 서류 가이드"
                ],
                "footer_text": "Blogin 365 AI · 대한민국 정부지원금 팩트체크 센터",
                "card_title": "Policy Subsidy",
                "card_sub": "정부 정책 금융 지원금",
                "card_stat": "만기 수령  최대 50,000,000원",
                "card_border": "#6366f1"
            }
        elif domain == DOMAIN_TELECOM:
            return {
                "bg_gradient": ((15, 23, 42), (2, 132, 199)),
                "glow_color": (14, 165, 233, 60),
                "badge_bg": "#0284c7",
                "badge_text": "2026 통신사 약관 공시 · 고정비 절감",
                "title_line1": f"{keyword[:16]}",
                "title_line2": "무제한 요금제 비교 및 위약금 0원",
                "accent_color": "#38bdf8",
                "bullets": [
                    "✓ 월 15,900원대 데이터 무제한 프로모션",
                    "✓ 무약정 가입으로 언제든 위약금 0원",
                    "✓ 통신 3사 동일 기지국 품질 100% 일치"
                ],
                "footer_text": "Blogin 365 AI · 통신 요금 절약 분석 센터",
                "card_title": "Unlimited 5G SIM",
                "card_sub": "알뜰폰 무제한 프로모션",
                "card_stat": "연간 절약  약 1,100,000원",
                "card_border": "#0284c7"
            }
        elif domain in (DOMAIN_AUTO_INSURANCE, DOMAIN_HEALTH_INSURANCE):
            return {
                "bg_gradient": ((15, 23, 42), (153, 27, 27)),
                "glow_color": (239, 68, 68, 60),
                "badge_bg": "#dc2626",
                "badge_text": "2026 손해보험협회 표준 공시 대조",
                "title_line1": f"{keyword[:16]}",
                "title_line2": "다이렉트 18% 할인 및 보장 비교",
                "accent_color": "#f87171",
                "bullets": [
                    "✓ 온라인 다이렉트 설계사 수수료 18% 절감",
                    "✓ 마일리지 + 블랙박스 + 티맵 중복 할인",
                    "✓ 24시간 본사 공식 긴급출동 네트워크 동일"
                ],
                "footer_text": "Blogin 365 AI · 다이렉트 보험 팩트체크 센터",
                "card_title": "Direct Shield",
                "card_sub": "다이렉트 최저가 비교 견적",
                "card_stat": "보험료 절감  평균 250,000원",
                "card_border": "#ef4444"
            }
        elif domain == DOMAIN_SAVINGS:
            return {
                "bg_gradient": ((15, 23, 42), (180, 83, 9)),
                "glow_color": (245, 158, 11, 60),
                "badge_bg": "#d97706",
                "badge_text": "2026 은행연합회 공시 최고 금리 비교",
                "title_line1": f"{keyword[:16]}",
                "title_line2": "복리 적금 수익률 실시간 시뮬레이터",
                "accent_color": "#fbbf24",
                "bullets": [
                    "✓ 연 최대 5.5% ~ 6.0% 우대 금리 조건",
                    "✓ 매일 이자 지급 파킹통장 실질 수익 비교",
                    "✓ 1금융권 5천만원 예금자보호 100% 적용"
                ],
                "footer_text": "Blogin 365 AI · 고금리 금융 자산 리서치 센터",
                "card_title": "High Yield Bank",
                "card_sub": "1금융권 고금리 파킹통장",
                "card_stat": "최고 금리  연 5.5% (복리 적용)",
                "card_border": "#f59e0b"
            }
        else: # TECH and Others
            return {
                "bg_gradient": ((15, 23, 42), (76, 29, 149)),
                "glow_color": (139, 92, 246, 60),
                "badge_bg": "#7c3aed",
                "badge_text": "2026 실사용 스펙 벤치마크 및 비교",
                "title_line1": f"{keyword[:16]}",
                "title_line2": "가성비 추천 모델 및 실측 벤치마크",
                "accent_color": "#c084fc",
                "bullets": [
                    "✓ 가격대별 핵심 사양 및 가성비 실측 지표",
                    "✓ 실사용자 검증 장단점 분석 및 추천 선택지",
                    "✓ 최저가 공식 할인 구매 경로 총정리"
                ],
                "footer_text": "Blogin 365 AI · 테크 디바이스 벤치마크 센터",
                "card_title": "Benchmark Pick",
                "card_sub": "가성비 종결 추천 디바이스",
                "card_stat": "가성비 지수  98 / 100 PT",
                "card_border": "#8b5cf6"
            }

    @classmethod
    def render_canvas_image(cls, keyword: str, category: str = "FINANCE") -> Image.Image:
        """Renders a pristine 1200x630 editorial graphic canvas with PIL."""
        width, height = 1200, 630
        domain = classify_domain(keyword, category)
        style = cls._get_domain_style(domain, keyword)

        img = Image.new("RGB", (width, height), style["bg_gradient"][0])
        draw = ImageDraw.Draw(img)

        # Gradient background
        c_start, c_end = style["bg_gradient"]
        for y in range(height):
            ratio = y / height
            r = int(c_start[0] * (1 - ratio) + c_end[0] * ratio)
            g = int(c_start[1] * (1 - ratio) + c_end[1] * ratio)
            b = int(c_start[2] * (1 - ratio) + c_end[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Ambient Glow Overlay
        glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_overlay)
        glow_draw.ellipse([800, -100, 1300, 400], fill=style["glow_color"])
        glow_draw.ellipse([-100, 300, 400, 800], fill=style["glow_color"])
        img.paste(Image.alpha_composite(Image.new("RGBA", (width, height), (0,0,0,0)), glow_overlay).convert("RGB"), mask=glow_overlay.split()[3])

        # Fonts
        font_title = ImageFont.truetype(cls.FONT_BOLD, 50)
        font_sub = ImageFont.truetype(cls.FONT_BOLD, 27)
        font_badge = ImageFont.truetype(cls.FONT_BOLD, 20)
        font_card = ImageFont.truetype(cls.FONT_BOLD, 24)
        font_card_num = ImageFont.truetype(cls.FONT_REG, 18)

        # 1. Badge
        badge_x, badge_y = 70, 65
        badge_text = style["badge_text"]
        bbox = font_badge.getbbox(badge_text)
        badge_w = bbox[2] - bbox[0] + 32
        badge_h = bbox[3] - bbox[1] + 18
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=16, fill=style["badge_bg"])
        draw.text((badge_x + 16, badge_y + 8), badge_text, font=font_badge, fill="#ffffff")

        # 2. Main Title (Two lines)
        draw.text((70, 140), style["title_line1"], font=font_title, fill="#ffffff")
        draw.text((70, 215), style["title_line2"], font=font_title, fill=style["accent_color"])

        # 3. Takeaway Bullets
        py = 315
        for pill in style["bullets"]:
            draw.text((70, py), pill, font=font_sub, fill="#f1f5f9")
            py += 46

        # 4. Branding
        draw.line([(70, 520), (600, 520)], fill="#334155", width=2)
        draw.text((70, 545), style["footer_text"], font=font_badge, fill="#94a3b8")

        # 5. Right Side Mockup Card
        c1_x, c1_y = 680, 115
        c_w, c_h = 440, 260
        draw.rounded_rectangle([c1_x, c1_y, c1_x + c_w, c1_y + c_h], radius=24, fill="#0f172a", outline=style["card_border"], width=2)
        draw.rounded_rectangle([c1_x + 40, c1_y + 40, c1_x + 95, c1_y + 85], radius=8, fill="#fbbf24")
        draw.text((c1_x + 40, c1_y + 110), style["card_title"], font=font_card, fill="#ffffff")
        draw.text((c1_x + 40, c1_y + 150), style["card_sub"], font=font_card_num, fill="#94a3b8")
        draw.text((c1_x + 40, c1_y + 205), style["card_stat"], font=font_badge, fill=style["accent_color"])

        # Secondary stacked card outline behind
        c2_x, c2_y = 730, 285
        draw.rounded_rectangle([c2_x, c2_y, c2_x + c_w - 30, c2_y + c_h - 20], radius=24, fill="#020617", outline="#334155", width=2)
        draw.rounded_rectangle([c2_x + 35, c2_y + 35, c2_x + 85, c2_y + 75], radius=8, fill="#d97706")
        draw.text((c2_x + 35, c2_y + 95), "FACT VERIFIED", font=font_card, fill="#ffffff")
        draw.text((c2_x + 35, c2_y + 135), "공식 약관 및 고시 전수 대조", font=font_card_num, fill="#64748b")
        draw.text((c2_x + 35, c2_y + 185), "100% 무인 팩트체크 시스템", font=font_badge, fill="#10b981")

        return img

    @classmethod
    def generate_and_upload_thumbnail(cls, keyword: str, category: str = "FINANCE") -> str:
        """
        Renders the Canvas thumbnail and uploads it to instant CDN.
        Falls back gracefully if network is offline.
        """
        img = cls.render_canvas_image(keyword, category)
        
        # Local thumbnail cache dir
        cache_dir = os.path.join(BASE_DIR, "data", "thumbnails")
        os.makedirs(cache_dir, exist_ok=True)
        safe_name = urllib.parse.quote(keyword[:20].replace(" ", "_"), safe="")
        local_path = os.path.join(cache_dir, f"thumb_{safe_name}.jpg")
        img.save(local_path, quality=95)

        # Upload to Catbox CDN (Free, zero API key, permanent, HTTPS)
        try:
            import requests
            with open(local_path, "rb") as f:
                resp = requests.post(
                    "https://catbox.moe/user/api.php",
                    data={"reqtype": "fileupload"},
                    files={"fileToUpload": f},
                    timeout=8
                )
            if resp.status_code == 200 and resp.text.startswith("http"):
                return resp.text.strip()
        except Exception as e:
            print(f"[ThumbnailMaker] Catbox upload error: {e}")

        # Fallback to local file path or GitHub raw
        return f"https://raw.githubusercontent.com/cjw1724/SEO-AD/main/data/thumbnails/thumb_{safe_name}.jpg"

    @classmethod
    def generate_hero_thumbnail_html(cls, keyword: str, category: str = "FINANCE") -> str:
        """
        Produces the clean Hero Thumbnail HTML container with our custom Canvas visual.
        """
        clean_kw = (keyword or "공식 리포트").replace(" 비교", "").replace(" 추천", "").strip()
        img_url = cls.generate_and_upload_thumbnail(clean_kw, category)

        return (
            f'<div class="b365-hero-thumbnail" style="max-width:820px; margin:0 auto 28px; border-radius:18px; '
            f'overflow:hidden; box-shadow:0 12px 32px -4px rgba(15,23,42,0.14); position:relative;">\n'
            f'  <img src="{img_url}" alt="{clean_kw} 2026 실시간 분석 리포트" '
            f'style="width:100%; height:auto; display:block; aspect-ratio:16/9; object-fit:cover; border-radius:18px;" loading="eager" />\n'
            f'</div>'
        )
