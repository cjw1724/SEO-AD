# -*- coding: utf-8 -*-
"""
engine/visuals/thumbnail_maker.py
---------------------------------
Automated World-Class 3D AI Thumbnail Engine.
Generates 1200x630 (16:9 golden ratio) modern 3D neon fintech/tech editorial hero visuals
via 100% free, zero-key Pollinations AI and injects them as the top featuredImage.
Google Blogger automatically proxies and caches this image onto its global CDN (blogger_img_proxy).
"""

import sys
import os
import urllib.parse
from typing import Optional

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
    Automated Hero Thumbnail Maker producing high-conversion 3D editorial visuals.
    """

    PROMPT_PRESETS = {
        DOMAIN_CARDS_TRAVEL: "modern travel exchange currency credit card passport neon 3d render clean futuristic 8k",
        DOMAIN_SAVINGS: "modern high interest digital bank vault coins glowing neon 3d render clean fintech 8k",
        DOMAIN_SUBSIDY: "modern government subsidy digital growth coins wealth shield neon 3d render clean 8k",
        DOMAIN_TELECOM: "modern 5g smartphone mobile telecom sim card saving money 3d render clean futuristic 8k",
        DOMAIN_AUTO_INSURANCE: "modern electric car digital insurance policy shield neon gradient 3d render clean futuristic 8k",
        DOMAIN_HEALTH_INSURANCE: "modern health medical insurance shield digital cross neon gradient 3d render clean 8k",
        DOMAIN_MEDICAL: "modern dental healthcare medical tech digital clinic glowing neon 3d render clean 8k",
        DOMAIN_CAREER: "modern career vocational education smart student card laptop neon 3d render clean futuristic 8k",
        DOMAIN_TECH: "modern premium tech gadget wireless futuristic device neon 3d render clean 8k",
    }

    @classmethod
    def get_prompt_for_topic(cls, keyword: str, category: str = "FINANCE") -> str:
        """
        Determines the most aesthetic English 3D prompt for the topic domain.
        """
        domain = classify_domain(keyword, category)
        preset = cls.PROMPT_PRESETS.get(domain)
        if preset:
            return preset
        return f"modern futuristic fintech digital analytics neon gradient 3d render clean wallpaper 8k"

    @classmethod
    def generate_hero_thumbnail_html(cls, keyword: str, category: str = "FINANCE", custom_prompt: Optional[str] = None) -> str:
        """
        Returns a responsive, beautiful HTML Hero Thumbnail container.
        Google Blogger parses the first <img> tag in the post body as data:post.featuredImage.
        """
        clean_kw = (keyword or "공식 리포트").replace(" 비교", "").replace(" 추천", "").strip()
        prompt = custom_prompt or cls.get_prompt_for_topic(clean_kw, category)
        
        encoded_prompt = urllib.parse.quote(prompt)
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true"

        return (
            f'<div class="b365-hero-thumbnail" style="max-width:820px; margin:0 auto 28px; border-radius:18px; '
            f'overflow:hidden; box-shadow:0 12px 32px -4px rgba(15,23,42,0.14); position:relative;">\n'
            f'  <img src="{pollinations_url}" alt="{clean_kw} 2026 실시간 분석 리포트" '
            f'style="width:100%; height:auto; display:block; aspect-ratio:16/9; object-fit:cover; border-radius:18px;" loading="eager" />\n'
            f'</div>'
        )
