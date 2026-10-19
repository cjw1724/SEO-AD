# -*- coding: utf-8 -*-
"""
tests/test_money_printer_bridge.py
-----------------------------------
Unit & Integration Tests for MoneyPrinterTurbo Short-Form Video Generator Bridge:
  1. MoneyPrinterBridge initialization & FFmpeg binary resolution
  2. Script cleaner & subtitle cue formatting (.srt timestamp check)
  3. 9:16 Vertical Slide Canvas generation (1080x1920 via Pillow)
  4. Neural TTS synthesis & silent audio fallback
  5. MoneyPrinterTurbo Manifest & Spec export
  6. ViralHookMaker end-to-end integration
"""

import os
import sys
import json
import tempfile
import unittest
from PIL import Image

# Ensure UTF-8
sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.growth.money_printer_bridge import (
    MoneyPrinterBridge,
    format_srt_timestamp,
    get_available_font
)
from engine.growth.viral_hook_maker import ViralHookMaker


class TestMoneyPrinterBridge(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.bridge = MoneyPrinterBridge(render_dir=self.temp_dir.name)
        self.sample_topic = {
            "keyword": "2026 청년도약계좌",
            "category": "SUBSIDY",
            "title": "2026 청년도약계좌 모의계산 및 정부기여금 가이드"
        }
        self.sample_reel = {
            "0-3초_후킹": '[화면: 붉은 경고 뱃지 + 볼드 텍스트]\n🎙️ "2026 청년도약계좌, 신청 안 하면 전액 소멸됩니다."',
            "3-10초_핵심내용": '[화면: 인터랙티브 표 빠르게 전개]\n🎙️ "복잡한 약관 뒤질 필요 없이, 30초 간편 자격 모의 조회기로 확인하세요."',
            "10-15초_행동유도(CTA)": '[화면: 댓글창 애니메이션 + \'10\' 입력 효과]\n🎙️ "댓글에 숫자 \'10\'만 남겨주시면, 이 계산기와 상세 비교표 링크를 1초 만에 DM으로 보내드립니다!"'
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_bridge_initialization(self):
        """Verifies bridge initialization and bundled FFmpeg resolution."""
        self.assertTrue(os.path.exists(self.bridge.render_dir))
        self.assertEqual(self.bridge.default_voice, "ko-KR-SunHiNeural")
        self.assertIsNotNone(self.bridge._ffmpeg_exe, "Bundled FFmpeg executable must be resolved")
        self.assertTrue(os.path.exists(self.bridge._ffmpeg_exe))

    def test_script_cleaner(self):
        """Verifies removal of stage directions, brackets, and emojis from script."""
        raw = '[화면: 붉은 경고 뱃지]\n🎙️ "2026 청년도약계좌 놓치지 마세요!"'
        cleaned = self.bridge.clean_script_line(raw)
        self.assertEqual(cleaned, "2026 청년도약계좌 놓치지 마세요!")
        self.assertNotIn("[화면:", cleaned)
        self.assertNotIn("🎙️", cleaned)
        self.assertNotIn('"', cleaned)

    def test_format_srt_timestamp(self):
        """Verifies standard SRT timestamp format: HH:MM:SS,mmm."""
        ts0 = format_srt_timestamp(0.0)
        self.assertEqual(ts0, "00:00:00,000")
        ts1 = format_srt_timestamp(3.5)
        self.assertEqual(ts1, "00:00:03,500")
        ts2 = format_srt_timestamp(65.25)
        self.assertEqual(ts2, "00:01:05,250")

    def test_generate_subtitles(self):
        """Verifies subtitle generation and 3-phase segmentation."""
        segments, srt_content = self.bridge.generate_subtitles(self.sample_reel, total_duration=15.0)
        self.assertEqual(len(segments), 3)
        self.assertEqual(segments[0]["phase"], "HOOK")
        self.assertEqual(segments[1]["phase"], "CORE")
        self.assertEqual(segments[2]["phase"], "CTA")
        self.assertEqual(segments[0]["start"], 0.0)
        self.assertEqual(segments[0]["end"], 3.5)
        self.assertEqual(segments[1]["start"], 3.5)
        self.assertEqual(segments[1]["end"], 10.5)

        self.assertIn("00:00:00,000 --> 00:00:03,500", srt_content)
        self.assertIn("00:00:03,500 --> 00:00:10,500", srt_content)
        self.assertIn("00:00:10,500 --> 00:00:15,000", srt_content)

    def test_generate_slide_assets(self):
        """Verifies generation of 3 9:16 vertical PNG cards (1080x1920)."""
        segments, _ = self.bridge.generate_subtitles(self.sample_reel)
        assets_dir = os.path.join(self.temp_dir.name, "test_assets")
        slides = self.bridge.generate_slide_assets(self.sample_topic, segments, assets_dir)

        self.assertEqual(len(slides), 3)
        for s in slides:
            self.assertTrue(os.path.exists(s), f"Slide file {s} must exist")
            self.assertGreater(os.path.getsize(s), 1000)
            with Image.open(s) as img:
                self.assertEqual(img.size, (1080, 1920), "Must be 9:16 vertical resolution 1080x1920")

    def test_manifest_export_and_queue(self):
        """Verifies full MoneyPrinterTurbo package export and manifest structure."""
        # Use render_video=False for instant unit test speed
        pkg = self.bridge.create_video_package(self.sample_topic, self.sample_reel, render_video=False)

        self.assertIn("batch_id", pkg)
        self.assertTrue(pkg["batch_id"].startswith("MPT-"))
        self.assertEqual(pkg["aspect_ratio"], "9:16")
        self.assertEqual(pkg["resolution"], "1080x1920")
        self.assertTrue(os.path.exists(pkg["manifest_dir"]))
        self.assertTrue(os.path.exists(pkg["subtitles_srt"]))
        self.assertTrue(os.path.exists(pkg["subtitles_json"]))
        self.assertTrue(os.path.exists(pkg["audio_path"]))
        self.assertEqual(len(pkg["assets"]), 3)

        # MoneyPrinterTurbo schema compatibility check
        mpt_spec = pkg["money_printer_turbo_spec"]
        self.assertEqual(mpt_spec["video_aspect"], "9:16")
        self.assertEqual(mpt_spec["video_subject"], self.sample_topic["keyword"])
        self.assertTrue(mpt_spec["subtitle_enabled"])

    def test_viral_hook_maker_integration(self):
        """Verifies ViralHookMaker automatically produces video_package."""
        maker = ViralHookMaker(output_dir=self.temp_dir.name)
        # Fast mode: render_video=False
        res = maker.generate_hooks(self.sample_topic, post_url="https://example.com/post", render_video=False)

        self.assertIn("keyword", res)
        self.assertIn("reel_script", res)
        self.assertIn("0-3초_후킹", res["reel_script"])
        self.assertIn("sns_caption", res)
        self.assertIn("dm_copy", res)
        self.assertIn("video_package", res)
        self.assertIn("video_batch_id", res)
        self.assertTrue(res["video_batch_id"].startswith("MPT-"))

    def test_calibrate_segments_to_duration(self):
        """Verifies dynamic calibration aligns segments and SRT timestamps to actual speech duration."""
        segments, _ = self.bridge.generate_subtitles(self.sample_reel)
        actual_dur = 21.5
        calibrated, srt_content = self.bridge.calibrate_segments_to_duration(segments, actual_dur)

        self.assertEqual(len(calibrated), 3)
        self.assertEqual(calibrated[0]["start"], 0.0)
        self.assertEqual(calibrated[-1]["end"], actual_dur)
        total_calibrated = sum(s["duration"] for s in calibrated)
        self.assertAlmostEqual(total_calibrated, actual_dur, delta=0.1)
        self.assertIn(f"--> {format_srt_timestamp(actual_dur)}", srt_content)

    def test_synthesize_voiceover_active_event_loop(self):
        """Verifies synthesize_voiceover works smoothly inside an active asyncio event loop without RuntimeError."""
        import asyncio
        async def run_in_loop():
            audio_path = os.path.join(self.temp_dir.name, "loop_test.mp3")
            segments = [{"text": "이벤트 루프 안전성 테스트입니다."}]
            return self.bridge.synthesize_voiceover(segments, audio_path)

        res = asyncio.run(run_in_loop())
        self.assertTrue(res["success"])
        self.assertTrue(os.path.exists(res["output_path"]))
        self.assertGreater(res["file_size"], 100)

    def test_render_mp4_video_sync(self):
        """Verifies actual MP4 rendering produces a valid playable video file."""
        if not self.bridge._ffmpeg_exe:
            self.skipTest("FFmpeg not available")

        pkg = self.bridge.create_video_package(self.sample_topic, self.sample_reel, render_video=True)
        self.assertEqual(pkg["status"], "COMPLETED")
        self.assertIsNotNone(pkg["video_path"])
        self.assertTrue(os.path.exists(pkg["video_path"]))
        self.assertGreater(os.path.getsize(pkg["video_path"]), 5000)

        # Probe duration of rendered video
        dur = self.bridge._probe_audio_duration(pkg["video_path"])
        self.assertAlmostEqual(dur, pkg["duration_sec"], delta=0.5)


if __name__ == "__main__":
    unittest.main()
