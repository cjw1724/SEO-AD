# -*- coding: utf-8 -*-
"""
tests/test_microsaas_crew_pipeline.py
-------------------------------------
CrewAI Programmatic Micro-SaaS 4대 패치 종합 검증 스위트:
1. [Patch 1] 자가치유 루프 시 original_spec_json 유지 검증
2. [Patch 2] qa_validator의 한글/단위 결합(NaNGB, NaN원, undefined초 등) 포착 검증
3. [Patch 3] ImageUploader 및 Blogger 이미지 배너 결합 검증
4. [Patch 4] Playwright WebP 썸네일 동적 생성 및 파라미터 연동 검증
"""

import os
import sys
import unittest
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.crew.qa_validator import DeterministicQAValidator, run_validator
from engine.crew.thumbnail_generator import create_thumbnail_sync
from engine.crew.image_uploader import ImageUploader
from engine.crew.publisher import MicroSaaSBloggerPublisher
from engine.crew.tasks import MicroSaaSCrewTasks
from engine.crew.agents import MicroSaaSCrewAgents


class TestMicroSaaSCrewPipeline(unittest.TestCase):

    # --------------------------------------------------------------------------
    # [Patch 2 검증] QA Validator의 \b 버그 해결 및 한글/단위 결합 NaN 검출
    # --------------------------------------------------------------------------
    def test_01_qa_validator_catches_nankorean_and_units(self):
        """NaNGB, NaN원, undefined초, nullTokens 등이 단어 경계(\b) 실패 없이 100% 검출되는지 확인"""
        dirty_cases = [
            "필요 총 VRAM: NaNGB 입니다.",
            "예상 월간 전기세: NaN원 발생",
            "토큰 생성 지연시간: undefined초",
            "캐시 메모리: nullTokens",
            "동시 처리량: Infinity%"
        ]
        
        validator = DeterministicQAValidator("<html><body></body></html>")
        for case in dirty_cases:
            matches = validator.INVALID_TOKEN_PATTERN.findall(case)
            self.assertTrue(len(matches) > 0, f"Failed to detect invalid token in: '{case}'")

    def test_02_qa_validator_allows_clean_units(self):
        """정상적인 수치와 단위(24.5 GB, 3,200원, 120 Tokens)는 오탐 없이 통과하는지 확인"""
        clean_cases = [
            "필요 총 VRAM: 24.5 GB 입니다.",
            "예상 월간 전기세: 14,200원 발생",
            "토큰 생성 지연시간: 0.12초",
            "캐시 메모리: 4096 Tokens",
            "동시 처리량: 100%"
        ]
        
        validator = DeterministicQAValidator("<html><body></body></html>")
        for case in clean_cases:
            matches = validator.INVALID_TOKEN_PATTERN.findall(case)
            self.assertEqual(len(matches), 0, f"False positive detected in clean text: '{case}' (Found: {matches})")

    # --------------------------------------------------------------------------
    # [Patch 1 검증] 자가치유 루프 태스크의 원래 기획 명세서(JSON) 보존 검증
    # --------------------------------------------------------------------------
    def test_03_self_healing_task_preserves_original_spec(self):
        """repair_micro_saas_widget_task가 원래의 기획 JSON과 에러 로그를 누락 없이 유지하는지 확인"""
        tasks = MicroSaaSCrewTasks()
        agents = MicroSaaSCrewAgents()
        coder = agents.frontend_tool_builder()

        dummy_spec = json.dumps({
            "target_keyword": "로컬 LLM 퀀타이즈 VRAM 계산기",
            "math_formula": "VRAM = P * Q / 8",
            "outputs": ["필요 총 VRAM (GB)"]
        }, ensure_ascii=False)
        dummy_errors = [
            "[GATE 3 FAIL] JS 계산 결과에 비정상 토큰 검출: [('NaN', 'GB')]",
            "[GATE 3 FAIL] 모바일 360px 기준 가로 스크롤 발생"
        ]

        repair_task = tasks.repair_micro_saas_widget_task(
            agent=coder,
            original_spec_json=dummy_spec,
            error_logs=dummy_errors
        )

        desc = repair_task.description
        # 1. 원래 기획 JSON 명세서 포함 여부
        self.assertIn("로컬 LLM 퀀타이즈 VRAM 계산기", desc)
        self.assertIn("VRAM = P * Q / 8", desc)
        # 2. QA 에러 로그 포함 여부
        self.assertIn("NaN", desc)
        self.assertIn("360px", desc)

    # --------------------------------------------------------------------------
    # [Patch 4 검증] Playwright WebP 썸네일 동적 생성
    # --------------------------------------------------------------------------
    def test_04_playwright_thumbnail_dynamic_generation(self):
        """HTML/CSS 기반 Playwright WebP 썸네일이 파일 시스템에 실제 생성되는지 확인"""
        thumb_path = create_thumbnail_sync(
            filename="test_vram_thumb",
            title="로컬 LLM 양자화 모델별 필요 VRAM 계산기",
            formula_badge="VRAM = (P * Q / 8) * 1.2 + KV_Cache",
            key_stat="LLaMA 3 70B Q4 : 42.4 GB",
            sub_label="MINIMUM GPU REQUIREMENT"
        )

        self.assertTrue(os.path.exists(thumb_path), f"Thumbnail not created at: {thumb_path}")
        self.assertTrue(thumb_path.endswith(".webp"))
        self.assertGreater(os.path.getsize(thumb_path), 5000, "Thumbnail file too small!")

    # --------------------------------------------------------------------------
    # [Patch 3 검증] ImageUploader 및 Blogger 배너 결합 검증
    # --------------------------------------------------------------------------
    def test_05_image_uploader_and_publisher_banner(self):
        """로컬 이미지를 Uploader가 처리하고, Publisher가 본문 상단에 <img> 배너를 결합하는지 확인"""
        thumb_path = os.path.join(BASE_DIR, "data", "thumbnails", "test_vram_thumb.webp")
        self.assertTrue(os.path.exists(thumb_path))

        uploader = ImageUploader()
        upload_res = uploader.upload_image(thumb_path)
        self.assertTrue(upload_res.get("success"))
        self.assertTrue(upload_res.get("url") is not None)

        publisher = MicroSaaSBloggerPublisher()
        record = publisher.publish_post(
            title="테스트 LLM 계산기",
            html_content="<p>테스트 본문 내용</p>",
            thumbnail_url=upload_res["url"],
            keyword="LLM VRAM",
            dry_run=True
        )

        self.assertEqual(record["status"], "SIMULATED_SUCCESS")
        self.assertEqual(record["thumbnail_url"], upload_res["url"])


if __name__ == "__main__":
    unittest.main()
