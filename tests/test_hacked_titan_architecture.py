# -*- coding: utf-8 -*-
"""
tests/test_hacked_titan_architecture.py
----------------------------------------
세계 최상위 0.000001% pSEO 무인 타이탄(Pieter Levels, Ian Nuttall, Wise, NerdWallet) 역공학 아키텍처 전수 검증 스위트:
1. [Test 1] SSOT 하드웨어 벤치마크 데이터셋(hardware_specs_db.json) 무결성 검증
2. [Test 2] 결정론적 리졸버(HardwareDatasetResolver) 수식 계산 정확도 검증
3. [Test 3] Pieter Levels / Wise 스타일 Micro-SaaS 위젯 렌더링 무결점(Zero-NaN) 검증
4. [Test 4] 데이터 밀도 매트릭스(Data Density Matrix) 테이블 2종 생성 검증
5. [Test 5] Playwright 헤드리스 브라우저 샌드박스 무인 품질 게이트 전수 통과 검증
"""

import os
import sys
import unittest
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.crew.dataset_resolver import HardwareDatasetResolver, load_hardware_db
from engine.crew.qa_validator import run_validator


class TestHackedTitanArchitecture(unittest.TestCase):

    def setUp(self):
        self.resolver = HardwareDatasetResolver()

    # --------------------------------------------------------------------------
    # [Test 1] SSOT 하드웨어 벤치마크 DB 무결성
    # --------------------------------------------------------------------------
    def test_01_ssot_hardware_db_integrity(self):
        """HuggingFace 모델 설정 및 GPU 하드웨어 사양 DB 정합성 검증"""
        db = load_hardware_db()
        self.assertIn("models", db)
        self.assertIn("quantizations", db)
        self.assertIn("hardware", db)

        # 핵심 모델 4종 이상 확인
        for expected_model in ["llama-3-8b", "llama-3-70b", "mistral-7b", "qwen-2.5-72b"]:
            self.assertIn(expected_model, db["models"])
            m = db["models"][expected_model]
            self.assertGreater(m["params_b"], 0)
            self.assertGreater(m["layers"], 0)
            self.assertGreater(m["kv_heads"], 0)

        # 주요 GPU 플랫폼 확인
        for expected_gpu in ["rtx-4090", "rtx-3090", "mac-studio-m2-ultra", "nvidia-a100-80gb"]:
            self.assertIn(expected_gpu, db["hardware"])
            h = db["hardware"][expected_gpu]
            self.assertGreater(h["vram_gb"], 0)
            self.assertGreater(h["bandwidth_gbs"], 0)

    # --------------------------------------------------------------------------
    # [Test 2] 결정론적 리졸버 수식 계산 정확도 (오차율 0.00%)
    # --------------------------------------------------------------------------
    def test_02_dataset_resolver_exact_calculations(self):
        """LLaMA-3 70B Q4_K_M의 가중치, KV 캐시, 총 VRAM 및 추천 GPU가 정확한지 검증"""
        calc = self.resolver.calculate_vram("llama-3-70b", "Q4_K_M", context_tokens=8192)

        # 70.6 * 4.5 / 8 * 1.06 ~= 42.10 GB
        self.assertAlmostEqual(calc["weights_vram_gb"], 42.10, places=1)
        # KV cache at 8192 tokens: 2 * 80 * 8 * 128 * 2 * 8192 / 1024^3 ~= 2.50 GB
        self.assertAlmostEqual(calc["kv_cache_gb"], 2.50, places=1)
        # CUDA overhead: 0.60 GB
        self.assertEqual(calc["cuda_overhead_gb"], 0.60)
        # Total: ~45.2 GB
        self.assertAlmostEqual(calc["total_vram_gb"], 45.20, places=1)
        # 45.2GB requires 2x RTX 3090 / 4090 (48GB)
        self.assertIn("2x RTX 3090 / 4090", calc["recommended_gpu"]["name"])

    # --------------------------------------------------------------------------
    # [Test 3] Pieter Levels / Wise 스타일 Micro-SaaS 위젯 렌더링 검증
    # --------------------------------------------------------------------------
    def test_03_rendered_widget_zero_nan_and_interactivity(self):
        """생성된 Single-File HTML 위젯에 비정상 토큰이 없고 필수 조작 컨트롤이 포함되는지 검증"""
        widget_html = self.resolver.render_micro_saas_html("llama-3-70b")

        # 필수 태그 및 ID 검증
        self.assertIn("blogin-saas-container", widget_html)
        self.assertIn("titan_model_select", widget_html)
        self.assertIn("titan_quant_select", widget_html)
        self.assertIn("titan_ctx_range", widget_html)
        self.assertIn("titan_copy_btn", widget_html)

        # 비정상 토큰 방어 검증
        self.assertNotIn("NaNGB", widget_html)
        self.assertNotIn("undefined초", widget_html)
        self.assertNotIn("nullTokens", widget_html)

    # --------------------------------------------------------------------------
    # [Test 4] 데이터 밀도 매트릭스(Data Density Tables) 렌더링 검증
    # --------------------------------------------------------------------------
    def test_04_rendered_tables_contain_high_density_data(self):
        """텍스트 나열을 대체하는 고밀도 수치 대조표 2종이 정상 생성되는지 검증"""
        tables_html = self.resolver.render_data_density_tables("llama-3-70b")

        # 테이블 1: 양자화 포맷별 실측 비교표
        self.assertIn("양자화(Quantization) 비트별 실측 메모리", tables_html)
        self.assertIn("Q4_K_M", tables_html)
        self.assertIn("FP16", tables_html)
        self.assertIn("Q2_K", tables_html)

        # 테이블 2: 하드웨어 GPU 플랫폼 벤치마크
        self.assertIn("주요 하드웨어 플랫폼별 실측 메모리 대역폭", tables_html)
        self.assertIn("RTX 4090", tables_html)
        self.assertIn("Apple Mac Studio", tables_html)
        self.assertIn("NVIDIA A100", tables_html)

    # --------------------------------------------------------------------------
    # [Test 5] Playwright 헤드리스 브라우저 샌드박스 무인 품질 게이트 전수 통과
    # --------------------------------------------------------------------------
    def test_05_playwright_e2e_sandbox_titan_widget(self):
        """조립된 타이탄 포스트가 Playwright QA 검증기에서 0 오류로 100% 통과하는지 검증"""
        resolved = self.resolver.resolve_topic("llama 3 70b vram 계산기")
        widget_html = self.resolver.render_micro_saas_html(resolved["model_key"])
        tables_html = self.resolver.render_data_density_tables(resolved["model_key"])

        complete_page_html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{resolved['target_keyword']}</title>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "SoftwareApplication",
        "name": "{resolved['target_keyword']}",
        "operatingSystem": "Any",
        "applicationCategory": "UtilitiesApplication",
        "offers": {{ "@type": "Offer", "price": "0" }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "LLaMA 3 70B를 돌리려면 최소 VRAM이 얼마나 필요한가요?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Q4_K_M 양자화 기준으로 약 45.2 GB의 VRAM이 필요하며, 24GB GPU 2장(RTX 3090/4090) 또는 Apple Mac Studio 64GB 이상이 필요합니다."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body style="margin:0; padding:10px; background:#0b0f19; box-sizing:border-box;">
  <h1 style="color:#fff;">{resolved['target_keyword']}</h1>
  {widget_html}
  {tables_html}
</body>
</html>
"""

        qa_result = run_validator(complete_page_html)
        self.assertTrue(qa_result["passed"], f"Titan page failed QA: {qa_result['errors']}")
        self.assertEqual(len(qa_result["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
