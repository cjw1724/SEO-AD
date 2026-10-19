# -*- coding: utf-8 -*-
"""
tests/test_adsense_ghost_mode_and_static_pages.py
--------------------------------------------------
Verification suite for AdSense Re-Review Boost Actions:
1. Ghost Mode Ad Suppression: Zero adsbygoogle tags, zero empty adsense-slot boxes when IS_ADSENSE_APPROVED=false
2. Theme XML Protection: Guard condition preventing adsbygoogle on 404, search, and archive pages
3. 4 Mandatory Static Pages Builder: About Us, Privacy Policy, Terms of Service, Contact Us
4. BloggerGateway Static Pages Management: dry-run, create, update, and ensure methods
5. Strict Editorial Standards: Zero-Persona (Blogin 365 AI), Zero-Broken-Entities, AdSense DART cookie compliance
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.agents.cro_monetizer import assemble_world_class_article, render_search_navigation_widget
from engine.publisher.static_pages_builder import (
    build_about_page_html,
    build_privacy_page_html,
    build_terms_page_html,
    build_contact_page_html,
    get_mandatory_static_pages
)
from engine.publisher.blogger_gateway import BloggerGateway
from engine.qa.gstack_auditor import GStackAuditor, FORBIDDEN_ENTITIES, FORBIDDEN_PERSONA_KEYWORDS


class TestAdSenseGhostModeAndStaticPages(unittest.TestCase):

    def setUp(self):
        self.auditor = GStackAuditor()
        self.sample_topic = {
            "keyword": "2026 청년도약계좌",
            "category": "SUBSIDY",
            "cpc": 3200,
            "pvs": 25000000,
            "keyword_package": {
                "main": "2026 청년도약계좌",
                "subs": ["2026 청년도약계좌 조건", "2026 청년도약계좌 신청기간", "2026 청년도약계좌 금액"]
            }
        }
        self.sample_editorial = {
            "keyword": "2026 청년도약계좌",
            "subtitle": "2026 청년도약계좌 공식 데이터 및 핵심 기준 대조 분석 보고서입니다.",
            "sections": [
                {"heading": "1. 2026 청년도약계좌 조건 핵심 분석", "content": "<p>2026 청년도약계좌 조건 기준을 상세히 확인합니다.</p>"},
                {"heading": "2. 2026 청년도약계좌 신청기간 안내", "content": "<p>2026 청년도약계좌 신청기간 일정에 맞춰 서류를 준비합니다.</p>"},
                {"heading": "3. 2026 청년도약계좌 금액 모의 계산", "content": "<p>2026 청년도약계좌 금액 수령액을 사전에 점검합니다.</p>"}
            ],
            "faq": [
                {"question": "자격 요건은 어떻게 되나요?", "answer": "중위소득 기준을 충족해야 합니다."}
            ]
        }

    # --------------------------------------------------------------------------
    # 1. Action 1: Ghost Mode Defense in Article Assembly
    # --------------------------------------------------------------------------

    def test_01_ghost_mode_complete_ad_suppression(self):
        """IS_ADSENSE_APPROVED=false 상태에서 모든 광고 코드 및 빈 슬롯 완전 배제 검증"""
        html = assemble_world_class_article(
            self.sample_topic,
            self.sample_editorial,
            is_adsense_approved=False
        )

        # No AdSense JavaScript tag or push execution
        self.assertNotIn("adsbygoogle", html)
        self.assertNotIn("window.adsbygoogle", html)

        # No empty adsense-slot container or placeholder box
        self.assertNotIn("adsense-slot", html)
        self.assertNotIn("ADVERTISEMENT · B365 AD NETWORK", html)

        # No intrusive affiliate conversion buttons
        self.assertNotIn("btn-affiliate-action", html)

        # No Google CSE ad scripts loaded in search nav
        self.assertNotIn("cse.google.com/cse.js", html)

        # Pure informational guide box & trust links present
        self.assertIn("editorial-info-box", html)
        self.assertIn("editorial-trust-links", html)
        self.assertIn("about-us-blogin-365-ai.html", html)
        self.assertIn("privacy-policy.html", html)
        self.assertIn("terms-of-service.html", html)
        self.assertIn("contact-us.html", html)

    def test_02_full_monetization_mode_active_when_approved(self):
        """IS_ADSENSE_APPROVED=true 상태에서는 4대 황금 슬롯이 모두 활성화됨을 검증"""
        html = assemble_world_class_article(
            self.sample_topic,
            self.sample_editorial,
            is_adsense_approved=True
        )

        self.assertIn("adsense-top", html)
        self.assertIn("adsense-mid", html)
        self.assertIn("adsense-mid-2", html)
        self.assertIn("adsense-bottom", html)
        self.assertIn("editorial-affiliate-box", html)

    # --------------------------------------------------------------------------
    # 2. Action 1: Theme XML Conditional Protection
    # --------------------------------------------------------------------------

    def test_03_theme_xml_adsense_guard_condition(self):
        """blogin365_fintech_theme.xml 내 AdSense 스크립트가 404, 검색, 아카이브 화면을 방어하는지 검증"""
        theme_path = os.path.join(BASE_DIR, "blogin365_fintech_theme.xml")
        self.assertTrue(os.path.exists(theme_path))

        with open(theme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must have condition guarding against error, archive, search
        self.assertIn("data:view.isSingleItem", content)
        self.assertIn("not data:view.isError", content)
        self.assertIn("not data:view.isArchive", content)
        self.assertIn("not data:view.isSearch", content)

        # Empty slot CSS suppression
        self.assertIn(".adsense-slot:empty", content)
        self.assertIn(".b365-ad-slot:empty", content)

        # Footer policy links
        self.assertIn("b365-footer-policy-links", content)
        self.assertIn("privacy-policy.html", content)
        self.assertIn("terms-of-service.html", content)

        # Must parse as valid XML
        tree = ET.parse(theme_path)
        self.assertTrue(tree.getroot().tag.endswith("html"))

    # --------------------------------------------------------------------------
    # 3. Action 2: 4 Static Policy & Trust Pages Builder
    # --------------------------------------------------------------------------

    def test_04_static_pages_builder_content_quality(self):
        """4대 정적 페이지가 애드센스 필수 조항 및 제로 슬롭 정책을 엄격 준수하는지 검증"""
        pages = get_mandatory_static_pages()
        self.assertEqual(len(pages), 4, "Must provide exactly 4 static policy pages")
        self.assertIn("about", pages)
        self.assertIn("privacy", pages)
        self.assertIn("terms", pages)
        self.assertIn("contact", pages)

        for key, pdata in pages.items():
            html = pdata["html"]
            title = pdata["title"]

            # 1. Zero Broken Entities check
            for ent in FORBIDDEN_ENTITIES:
                self.assertNotRegex(html, ent, f"Forbidden entity {ent} found in {key} static page")

            # 2. Zero Persona check (No fake journalists)
            for p in FORBIDDEN_PERSONA_KEYWORDS:
                self.assertNotIn(p, html, f"Forbidden persona {p} found in {key} static page")

            # 3. Official branding presence
            self.assertIn("Blogin 365 AI", html)

            # 4. Content volume sufficiency
            self.assertGreater(len(html), 500, f"Page {key} HTML length too short: {len(html)}")

        # Specific AdSense compliance in Privacy Policy
        priv_html = pages["privacy"]["html"]
        self.assertIn("Google AdSense", priv_html)
        self.assertIn("쿠키", priv_html)
        self.assertIn("DoubleClick", priv_html)
        self.assertIn("aboutads.info", priv_html)
        self.assertIn("blogin365ai@gmail.com", priv_html)

        # Specific legal compliance in Terms of Service
        terms_html = pages["terms"]["html"]
        self.assertIn("지적재산권", terms_html)
        self.assertIn("면책 조항", terms_html)
        self.assertIn("Disclaimer", terms_html)

    # --------------------------------------------------------------------------
    # 4. Action 2: BloggerGateway Static Pages Methods
    # --------------------------------------------------------------------------

    def test_05_blogger_gateway_static_pages_dry_run(self):
        """BloggerGateway.ensure_mandatory_static_pages dry-run 모드 검증"""
        gw = BloggerGateway()
        res = gw.ensure_mandatory_static_pages(dry_run=True)

        self.assertTrue(res["success"])
        self.assertEqual(len(res["pages"]), 4)
        for key in ["about", "privacy", "terms", "contact"]:
            self.assertIn(key, res["pages"])
            self.assertTrue(res["pages"][key]["url"].startswith("https://blogin365ai.blogspot.com/p/"))

    def test_06_env_defense_flag_enforced(self):
        """SEO.env 내 IS_ADSENSE_APPROVED=false 상태 검증"""
        env_path = os.path.join(BASE_DIR, "SEO.env")
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("IS_ADSENSE_APPROVED=false", content, "IS_ADSENSE_APPROVED must be false for review defense")

    # --------------------------------------------------------------------------
    # 5. Action 1 & 2: Median UI Theme Protection & Post Sanitization
    # --------------------------------------------------------------------------

    def test_07_median_ui_theme_protection(self):
        """median_ui_theme.xml 내 404 킬스위치, 빈 광고 CSS 숨김, 4대 정책 링크 검증"""
        theme_path = os.path.join(BASE_DIR, "median_ui_theme.xml")
        self.assertTrue(os.path.exists(theme_path))

        with open(theme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # AdSense killswitch on error, archive, search
        self.assertIn("data:view.isError or data:view.isArchive or data:view.isSearch", content)
        self.assertIn("window.adsbygoogle = { push: function()", content)

        # Empty slot CSS suppression
        self.assertIn(".adsense-slot:empty", content)

        # Footer policy links
        self.assertIn("b365-footer-policy-links", content)
        self.assertIn("about-us-blogin-365-ai.html", content)
        self.assertIn("privacy-policy.html", content)
        self.assertIn("terms-of-service.html", content)
        self.assertIn("contact-us.html", content)

        # Valid XML parsing
        tree = ET.parse(theme_path)
        self.assertTrue(tree.getroot().tag.endswith("html"))

    def test_08_blogger_gateway_sanitize_and_revert(self):
        """BloggerGateway.sanitize_existing_posts_for_ghost_mode 및 revert_to_draft 로직 검증"""
        gw = BloggerGateway()
        res = gw.sanitize_existing_posts_for_ghost_mode(dry_run=True)
        self.assertTrue(res["success"])
        self.assertIn("reverted_thin_posts", res)
        self.assertIn("sanitized_posts", res)
        self.assertIn("skipped_posts", res)


if __name__ == "__main__":
    unittest.main()

