# -*- coding: utf-8 -*-
"""
tests/test_end_to_end.py
------------------------
Full End-to-End Pipeline Verification Test for Blogin 365 AI Engine.
Executes all 6 phases in dry-run mode and verifies strict quality gates.
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.main import BloginMasterHarness


def test_full_pipeline():
    print("==================================================")
    print("🧪 Running Blogin 365 AI Full Pipeline E2E Test")
    print("==================================================")

    harness = BloginMasterHarness()
    result = harness.run_pipeline(dry_run=True, keyword_override="2026 청년도약계좌")

    assert result is not None, "Pipeline returned None!"
    assert result["title"], "Title is empty!"
    assert result["url"], "URL is empty!"
    assert result["keyword"] == "2026 청년도약계좌", "Keyword mismatch!"
    
    # 7-Tier and Golden Ratio verification
    assert result["tier"] in ["최적", "가능"], f"Expected optimal/viable tier, got: {result.get('tier')}"
    assert result["ratio"] > 0.5, f"Expected Golden Ratio > 0.5 for optimal, got: {result.get('ratio')}"
    assert isinstance(result["subs"], list) and len(result["subs"]) >= 2, "Sub-keywords must be a list of at least 2 items"
    assert "keyword_package" in result and "sub_details" in result["keyword_package"], "sub_details must be present in keyword package"
    assert len(result["keyword_package"]["sub_details"]) >= 2, "Must have detailed metrics for sub-keywords"

    # Title placement architecture verification (main at start, no subs in title, no brackets)
    assert result["title"].startswith("2026 청년도약계좌"), f"Title must start directly with main keyword: {result['title']}"
    assert "[2026]" not in result["title"], "Title must not contain bracket labels"
    assert len(result["title"]) >= 25 and len(result["title"]) <= 45, f"Title length should be 25-45 chars: {len(result['title'])}"
    for sub in result["subs"]:
        assert sub not in result["title"], f"Sub-keyword '{sub}' must not appear in title '{result['title']}'"

    assert result["growth_package"], "Growth package missing!"
    assert "0-3초_후킹" in result["growth_package"]["reel_script"], "Reel script missing hook!"

    print("\n✅ E2E Pipeline Dry-Run Test PASSED 100%!")


if __name__ == "__main__":
    test_full_pipeline()
