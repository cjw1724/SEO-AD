"""
Tests for 8-Agent Editorial Inspection Board & WCAG 2.1 Contrast Gate (v9.0 Apex)
"""

import unittest
from engine.crew.editorial_inspector import EditorialInspector

class TestEditorialInspector(unittest.TestCase):
    def setUp(self):
        self.inspector = EditorialInspector()

    def test_contrast_ratio_calculation(self):
        # Pure black on pure white -> 21:1
        black = (0, 0, 0)
        white = (255, 255, 255)
        ratio = self.inspector.calculate_contrast_ratio(black, white)
        self.assertAlmostEqual(ratio, 21.0, places=1)

        # Same colors -> 1:1
        ratio_same = self.inspector.calculate_contrast_ratio(white, white)
        self.assertAlmostEqual(ratio_same, 1.0, places=1)

        # High contrast: #f8fafc (248, 250, 252) on #0a0e17 (10, 14, 23)
        fg_tds = (248, 250, 252)
        bg_tds = (10, 14, 23)
        tds_ratio = self.inspector.calculate_contrast_ratio(fg_tds, bg_tds)
        self.assertGreater(tds_ratio, 14.0)

        # The ghost text defect: #cbd5e1 (203, 213, 225) on white #ffffff (255, 255, 255)
        fg_ghost = (203, 213, 225)
        ghost_ratio = self.inspector.calculate_contrast_ratio(fg_ghost, white)
        self.assertLess(ghost_ratio, 2.0)  # Severe contrast violation!

    def test_auto_heal_strips_white_container(self):
        buggy_html = """
        <div class="blog-post-container" style="background-color: #fff; color: #333;">
            <h2>2026 해외주식 절세 가이드</h2>
            <p>이 문장은 화이트 컨테이너에 갇혀 투명해질 뻔했습니다.</p>
        </div>
        """
        healed = self.inspector.auto_heal(buggy_html)
        self.assertIn("apex-editorial-shield", healed)
        self.assertNotIn("background-color: #fff", healed)

    def test_inspect_and_heal_lifecycle(self):
        buggy_html = """
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body { background: #0a0e17; color: #cbd5e1; }
            .blog-post-container { background-color: #fff; color: #cbd5e1; }
          </style>
        </head>
        <body>
          <div class="blog-post-container">
            <h1>2026 해외주식 시뮬레이터</h1>
            <p>이 문단은 심각한 투명화 결함이 있습니다.</p>
          </div>
        </body>
        </html>
        """
        healed_html, result = self.inspector.inspect_and_heal(buggy_html)
        self.assertTrue(result.get("healed", False))
        self.assertGreater(result["stats"]["desktop"]["min_contrast"], 4.5)
        self.assertTrue(result["passed"])
        self.assertEqual(len(result["certifications"]), 4)
        cos_cert = next(c for c in result["certifications"] if c["role"] == "Chief of Staff")
        self.assertEqual(cos_cert["verdict"], "APPROVED")

if __name__ == "__main__":
    unittest.main()
