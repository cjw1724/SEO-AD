# -*- coding: utf-8 -*-
"""
tests/test_master_theme_xml.py
-------------------------------
Unit tests for blogin365_apex_master_theme.xml validation:
1. Strict XML well-formedness parsing (No syntax errors, unclosed tags, or bad entities).
2. Blogger XML Namespace & Schema Compliance (b:skin, b:section, b:widget, b:includable).
3. TDS (Toss Design System) FinTech Design Tokens verification.
4. AdSense Non-Content Killswitch and Dual-Shield guard verification.
5. Zero-Blogger-Footprint suppression rule verification.
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_XML_PATH = os.path.join(BASE_DIR, "blogin365_apex_master_theme.xml")


class TestBloggerMasterThemeXML(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(THEME_XML_PATH), f"Master theme XML missing: {THEME_XML_PATH}")
        with open(THEME_XML_PATH, "r", encoding="utf-8") as f:
            self.xml_content = f.read()

    def test_01_xml_well_formedness(self):
        """XML 문법 및 구조적 정합성 검증 (파싱 에러 0건 보장)"""
        try:
            root = ET.fromstring(self.xml_content)
            self.assertIsNotNone(root, "Root element should not be None")
            self.assertTrue(root.tag.endswith("html"), f"Root element must be html, got {root.tag}")
        except ET.ParseError as e:
            self.fail(f"Master Theme XML ParseError: {e}")

    def test_02_blogger_namespaces_and_schema(self):
        """Blogger v2/v3 필수 네임스페이스 및 섹션/위젯 선언 검증"""
        self.assertIn("xmlns:b='http://www.google.com/namespaces/2010'", self.xml_content)
        self.assertIn("xmlns:data='http://www.google.com/namespaces/2010'", self.xml_content)
        self.assertIn("xmlns:expr='http://www.google.com/namespaces/2010'", self.xml_content)
        
        # Verify b:section and b:widget
        self.assertIn("<b:section", self.xml_content)
        self.assertIn("id='main'", self.xml_content)
        self.assertIn("<b:widget id='Blog1'", self.xml_content)
        self.assertIn("type='Blog'", self.xml_content)
        self.assertIn("<b:includable id='main'", self.xml_content)

    def test_03_toss_design_system_tokens(self):
        """TDS 다크 매트 핀테크 디자인 토큰 검증"""
        self.assertIn("--apex-bg-base: #0a0e17;", self.xml_content)
        self.assertIn("--apex-bg-surface: #111827;", self.xml_content)
        self.assertIn("--apex-border-card: #1f2d47;", self.xml_content)
        self.assertIn("--apex-content-width: 880px;", self.xml_content)
        self.assertIn("Pretendard Variable", self.xml_content)

    def test_04_zero_blogger_footprint_suppression(self):
        """Blogger 기본 쓰레기 위젯 및 불필요 요소 100% 영구 차단 검증"""
        suppression_tokens = [
            ".quickedit",
            ".Navbar",
            ".widget.Attribution",
            ".widget.Profile",
            ".widget.BlogArchive",
            "display: none !important;"
        ]
        for token in suppression_tokens:
            self.assertIn(token, self.xml_content, f"Missing suppression token: {token}")

    def test_05_adsense_dual_shield_guards(self):
        """애드센스 정책 위반 방어 킬스위치 및 조건부 로드 검증"""
        # Guard: Single item only, suppress on error/archive/search
        self.assertIn("data:view.isSingleItem and not data:view.isError", self.xml_content)
        self.assertIn("data:view.isError or data:view.isArchive or data:view.isSearch", self.xml_content)
        self.assertIn("AdSense suppressed on non-content screen", self.xml_content)

    def test_06_file_size_and_performance_budget(self):
        """40KB 이하 초경량 퍼포먼스 예산 검증"""
        file_size_kb = len(self.xml_content.encode('utf-8')) / 1024
        print(f"\n -> [Master Theme XML Budget] Total Size: {file_size_kb:.2f} KB (Target: <= 40KB)")
        self.assertLessEqual(file_size_kb, 40.0, "Master Theme XML must be <= 40KB for 100 Core Web Vitals score")


if __name__ == "__main__":
    unittest.main()
