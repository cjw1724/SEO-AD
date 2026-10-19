# -*- coding: utf-8 -*-
"""
engine/growth/money_printer_bridge.py
--------------------------------------
Automated Short-Form Video Generator Bridge inspired by MoneyPrinterTurbo.
Produces 15-30s Reels/Shorts packages into data/video_render_queue/:
  1. Subtitle & Cue Alignment (.srt and .json) from Phase 6 viral hook script
  2. Free Neural Voiceover Synthesis using edge-tts (Korean: ko-KR-SunHiNeural)
     with offline Windows SAPI5 & silent fallback
  3. 9:16 Vertical Visual Asset generation (1080x1920) via Pillow
  4. Local Video Rendering via Bundled FFmpeg (imageio-ffmpeg)
  5. MoneyPrinterTurbo Compatible Manifest Export (manifest.json & spec.json)
"""

import os
import sys
import re
import json
import time
import asyncio
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

# Enforce UTF-8
sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

DEFAULT_RENDER_DIR = os.path.join(BASE_DIR, "data", "video_render_queue")

# Standard Windows Font Lookups for Korean
FONT_CANDIDATES = [
    "C:/Windows/Fonts/malgunbd.ttf",
    "C:/Windows/Fonts/malgun.ttf",
    "C:/Windows/Fonts/gulim.ttc",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf"
]


def get_available_font(size: int = 40):
    """Loads Malgun Gothic or system fallback font."""
    for font_path in FONT_CANDIDATES:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def format_srt_timestamp(seconds: float) -> str:
    """Formats float seconds into SRT timestamp HH:MM:SS,mmm."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


class MoneyPrinterBridge:
    """
    Automated short-form video bridge inspired by MoneyPrinterTurbo.
    Transforms 15-second viral hook scripts into complete video packages.
    """

    def __init__(self, render_dir: Optional[str] = None, default_voice: str = "ko-KR-SunHiNeural"):
        self.render_dir = render_dir or DEFAULT_RENDER_DIR
        os.makedirs(self.render_dir, exist_ok=True)
        self.default_voice = default_voice
        self._ffmpeg_exe = self._resolve_ffmpeg()

    def _resolve_ffmpeg(self) -> Optional[str]:
        """Resolves local or bundled FFmpeg binary path."""
        try:
            import imageio_ffmpeg
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            if os.path.exists(exe):
                return exe
        except Exception:
            pass
        return None

    def clean_script_line(self, raw_line: str) -> str:
        """Removes screen directions, emojis, and quotes from script line."""
        text = re.sub(r'\[화면:[^\]]+\]', '', raw_line)
        text = re.sub(r'[🎙️⚠️🎁🔗📌]', '', text)
        text = text.replace('"', '').replace("'", '').strip()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return " ".join(lines)

    def generate_subtitles(self, reel_script: Dict[str, str], total_duration: float = 15.0) -> Tuple[List[Dict[str, Any]], str]:
        """
        Synthesizes time-aligned subtitle segments and .srt content.
        Default 3 phases: 0-3.5s Hook, 3.5-10.5s Core, 10.5-15.0s CTA.
        """
        hook_raw = reel_script.get("0-3초_후킹", "")
        core_raw = reel_script.get("3-10초_핵심내용", "")
        cta_raw = reel_script.get("10-15초_행동유도(CTA)", "")

        hook_text = self.clean_script_line(hook_raw) or "지금 확인하지 않으면 전액 소멸됩니다!"
        core_text = self.clean_script_line(core_raw) or "복잡한 약관 없이 실측 계산기로 즉시 확인하세요."
        cta_text = self.clean_script_line(cta_raw) or "댓글에 10 남겨주시면 가이드 링크를 즉시 발송합니다!"

        segments = [
            {
                "index": 1,
                "start": 0.0,
                "end": 3.5,
                "duration": 3.5,
                "phase": "HOOK",
                "text": hook_text
            },
            {
                "index": 2,
                "start": 3.5,
                "end": 10.5,
                "duration": 7.0,
                "phase": "CORE",
                "text": core_text
            },
            {
                "index": 3,
                "start": 10.5,
                "end": total_duration,
                "duration": max(1.0, total_duration - 10.5),
                "phase": "CTA",
                "text": cta_text
            }
        ]

        # Format SRT file
        srt_lines = []
        for seg in segments:
            srt_lines.append(str(seg["index"]))
            srt_lines.append(f"{format_srt_timestamp(seg['start'])} --> {format_srt_timestamp(seg['end'])}")
            srt_lines.append(seg["text"])
            srt_lines.append("")

        srt_content = "\n".join(srt_lines)
        return segments, srt_content

    async def _synthesize_edge_tts_async(self, text: str, output_path: str, voice: str) -> bool:
        """Synthesizes speech using edge-tts asynchronously."""
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
        except Exception:
            return False

    def synthesize_voiceover(
        self,
        segments: List[Dict[str, Any]],
        output_path: str,
        voice: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes voiceover audio using edge-tts with SAPI5 and silent fallbacks.
        """
        voice = voice or self.default_voice
        full_text = " ".join([seg["text"] for seg in segments])
        
        # 1. Edge-TTS synthesis with active event loop awareness
        tts_success = False
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(asyncio.run, self._synthesize_edge_tts_async(full_text, output_path, voice))
                    tts_success = future.result(timeout=25)
            else:
                tts_success = asyncio.run(self._synthesize_edge_tts_async(full_text, output_path, voice))
        except Exception:
            tts_success = False

        method = "edge-tts"
        if not tts_success:
            # 2. Windows SAPI5 Fallback
            method = "sapi5_fallback"
            tts_success = self._synthesize_sapi5(full_text, output_path)

        if not tts_success:
            # 3. Silent Audio Fallback (guarantees pipeline never crashes)
            method = "silent_audio_fallback"
            self._create_silent_mp3(output_path, duration_sec=15.0)
            tts_success = True

        duration = self._probe_audio_duration(output_path)

        return {
            "success": tts_success,
            "method": method,
            "voice": voice,
            "output_path": output_path,
            "duration_sec": duration,
            "file_size": os.path.getsize(output_path) if os.path.exists(output_path) else 0
        }

    def _synthesize_sapi5(self, text: str, output_path: str) -> bool:
        """Synthesizes voice using Windows SAPI5 COM object."""
        try:
            import win32com.client
            voice = win32com.client.Dispatch("SAPI.SpVoice")
            file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            wav_path = output_path.replace(".mp3", ".wav")
            # 3 = SSFMCreateForWrite
            file_stream.Open(wav_path, 3, False)
            voice.AudioOutputStream = file_stream
            voice.Speak(text)
            file_stream.Close()

            if os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000:
                if self._ffmpeg_exe:
                    # Convert to mp3
                    subprocess.run(
                        [self._ffmpeg_exe, "-y", "-i", wav_path, "-c:a", "libmp3lame", output_path],
                        capture_output=True
                    )
                    try:
                        os.remove(wav_path)
                    except Exception:
                        pass
                    return os.path.exists(output_path)
                return True
        except Exception:
            pass
        return False

    def _create_silent_mp3(self, output_path: str, duration_sec: float = 15.0):
        """Generates a silent audio file using bundled FFmpeg."""
        if self._ffmpeg_exe:
            cmd = [
                self._ffmpeg_exe, "-y",
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", str(duration_sec),
                "-c:a", "libmp3lame", "-b:a", "128k",
                output_path
            ]
            subprocess.run(cmd, capture_output=True)
        else:
            # Empty dummy write
            with open(output_path, "wb") as f:
                f.write(b"\xFF\xFB\x90\x00" * 200)

    def _probe_audio_duration(self, audio_path: str) -> float:
        """Measures duration of audio file using ffmpeg probe."""
        if not os.path.exists(audio_path) or not self._ffmpeg_exe:
            return 15.0
        try:
            cmd = [
                self._ffmpeg_exe, "-i", audio_path,
                "-f", "null", "-"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            output = res.stderr or ""
            # Search for Duration: 00:00:14.28
            dur_match = re.search(r"Duration:\s*(\d+):(\d+):([\d\.]+)", output)
            if dur_match:
                hours, mins, secs = dur_match.groups()
                return float(hours) * 3600 + float(mins) * 60 + float(secs)
        except Exception:
            pass
        return 15.0

    def calibrate_segments_to_duration(
        self,
        segments: List[Dict[str, Any]],
        total_duration: float
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Dynamically aligns subtitle segments and slide cue durations to the actual synthesized audio duration.
        Eliminates audio truncation and desynchronized subtitles.
        """
        total_len = max(1, sum(len(s.get("text", "")) for s in segments))
        curr_time = 0.0
        calibrated = []

        for i, seg in enumerate(segments):
            if i == len(segments) - 1:
                seg_dur = max(1.0, round(total_duration - curr_time, 2))
            else:
                ratio = len(seg.get("text", "")) / total_len
                seg_dur = max(1.0, round(total_duration * ratio, 2))
            
            calibrated_seg = {
                "index": seg.get("index", i + 1),
                "start": round(curr_time, 2),
                "end": round(curr_time + seg_dur, 2),
                "duration": seg_dur,
                "phase": seg.get("phase", f"PHASE_{i+1}"),
                "text": seg.get("text", "")
            }
            calibrated.append(calibrated_seg)
            curr_time += seg_dur

        srt_lines = []
        for seg in calibrated:
            srt_lines.append(str(seg["index"]))
            srt_lines.append(f"{format_srt_timestamp(seg['start'])} --> {format_srt_timestamp(seg['end'])}")
            srt_lines.append(seg["text"])
            srt_lines.append("")

        return calibrated, "\n".join(srt_lines)

    def generate_slide_assets(
        self,
        topic: Dict[str, Any],
        segments: List[Dict[str, Any]],
        output_dir: str
    ) -> List[str]:
        """
        Generates 3 high-impact 9:16 vertical cards (1080x1920) for Reels/Shorts:
          Slide 1: Hook Screen (Bold Red/Amber Pill + Question)
          Slide 2: Core Analysis & Key Benefit (Cyan/Electric Blue)
          Slide 3: ManyChat '10' CTA Screen (Emerald Green CTA)
        """
        os.makedirs(output_dir, exist_ok=True)
        keyword = topic.get("keyword", "2026 핵심 정책")
        title = topic.get("title", f"{keyword} 가이드")
        category = topic.get("category", "SUBSIDY")

        font_badge = get_available_font(34)
        font_hero = get_available_font(52)
        font_body = get_available_font(38)
        font_cta = get_available_font(60)
        font_sub = get_available_font(30)

        slide_paths = []
        width, height = 1080, 1920

        # Check for royalty-free stock background assets
        bg_dir = os.path.join(BASE_DIR, "data", "video_assets", "backgrounds")
        bg_base = None
        if os.path.exists(bg_dir):
            candidates = [os.path.join(bg_dir, f) for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if candidates:
                try:
                    with Image.open(candidates[0]) as img:
                        bg_raw = img.convert("RGBA").resize((width, height))
                        tint = Image.new("RGBA", (width, height), (15, 23, 42, 200))
                        bg_base = Image.alpha_composite(bg_raw, tint).convert("RGB")
                except Exception:
                    bg_base = None

        # Slide 1: Hook
        im1 = bg_base.copy() if bg_base else Image.new("RGB", (width, height), color=(18, 18, 28))
        d1 = ImageDraw.Draw(im1)
        # Gradient backdrop accent
        d1.rectangle([(0, 0), (width, 220)], fill=(30, 30, 48))
        # Top Badge
        d1.rounded_rectangle([(320, 120), (760, 190)], radius=35, fill=(220, 38, 38))
        d1.text((540, 155), "⚠️ 2026 긴급 점검", fill=(255, 255, 255), font=font_badge, anchor="mm")
        # Main Hero Box
        d1.rounded_rectangle([(80, 420), (1000, 1380)], radius=40, fill=(28, 28, 42), outline=(220, 38, 38), width=4)
        d1.text((540, 520), f"[{keyword}]", fill=(254, 240, 138), font=font_hero, anchor="mm")
        
        hook_text = segments[0]["text"]
        lines = self._wrap_text(hook_text, max_chars=18)
        y_cursor = 680
        for line in lines[:4]:
            d1.text((540, y_cursor), line, fill=(255, 255, 255), font=font_hero, anchor="mm")
            y_cursor += 90

        d1.text((540, 1260), "지금 놓치면 다시 오지 않는 핵심 혜택!", fill=(203, 213, 225), font=font_sub, anchor="mm")
        d1.text((540, 1780), "Blogin 365 AI • 스마트 라이프 에디토리얼 팀", fill=(148, 163, 184), font=font_sub, anchor="mm")
        p1 = os.path.join(output_dir, "slide_01_hook.png")
        im1.save(p1)
        slide_paths.append(p1)

        # Slide 2: Core Takeaway
        im2 = bg_base.copy() if bg_base else Image.new("RGB", (width, height), color=(15, 23, 42))
        d2 = ImageDraw.Draw(im2)
        d2.rectangle([(0, 0), (width, 220)], fill=(30, 41, 59))
        # Top Badge
        d2.rounded_rectangle([(300, 120), (780, 190)], radius=35, fill=(14, 165, 233))
        d2.text((540, 155), "📊 공식 팩트 & 모의 계산", fill=(255, 255, 255), font=font_badge, anchor="mm")
        # Core Bento Box
        d2.rounded_rectangle([(80, 380), (1000, 1450)], radius=40, fill=(24, 34, 53), outline=(56, 189, 248), width=3)
        d2.text((540, 480), "핵심 실측 지표 요약", fill=(56, 189, 248), font=font_hero, anchor="mm")
        
        core_text = segments[1]["text"]
        lines = self._wrap_text(core_text, max_chars=20)
        y_cursor = 620
        for line in lines[:5]:
            d2.text((540, y_cursor), line, fill=(241, 245, 249), font=font_body, anchor="mm")
            y_cursor += 75

        # Feature highlight pills
        d2.rounded_rectangle([(140, 1080), (940, 1180)], radius=20, fill=(30, 41, 59))
        d2.text((540, 1130), "✓ 정부 공식 누리집 및 관계법령 실측 대조", fill=(74, 222, 128), font=font_sub, anchor="mm")
        d2.rounded_rectangle([(140, 1220), (940, 1320)], radius=20, fill=(30, 41, 59))
        d2.text((540, 1270), "✓ 설치 없이 브라우저 30초 모의계산기 지원", fill=(56, 189, 248), font=font_sub, anchor="mm")

        d2.text((540, 1780), "blogin365ai.blogspot.com", fill=(148, 163, 184), font=font_sub, anchor="mm")
        p2 = os.path.join(output_dir, "slide_02_core.png")
        im2.save(p2)
        slide_paths.append(p2)

        # Slide 3: CTA
        im3 = bg_base.copy() if bg_base else Image.new("RGB", (width, height), color=(10, 18, 30))
        d3 = ImageDraw.Draw(im3)
        d3.rectangle([(0, 0), (width, 220)], fill=(16, 28, 48))
        # Top Badge
        d3.rounded_rectangle([(280, 120), (800, 190)], radius=35, fill=(16, 185, 129))
        d3.text((540, 155), "🎁 모의계산기 & 비교표 무료 배포", fill=(255, 255, 255), font=font_badge, anchor="mm")
        # CTA Center Card
        d3.rounded_rectangle([(80, 420), (1000, 1420)], radius=45, fill=(19, 35, 58), outline=(16, 185, 129), width=5)
        d3.text((540, 560), "가이드 & 계산기 즉시 받는 법", fill=(255, 255, 255), font=font_hero, anchor="mm")
        
        # Giant Pulse Button Effect
        d3.rounded_rectangle([(160, 720), (920, 940)], radius=45, fill=(16, 185, 129))
        d3.text((540, 830), "댓글에  ' 1 0 '  입력!", fill=(255, 255, 255), font=font_cta, anchor="mm")

        # Dynamic CTA script text
        cta_raw = segments[2]["text"] if len(segments) > 2 else "댓글에 10 남겨주시면 가이드 링크를 즉시 발송합니다!"
        cta_sub = re.sub(r'댓글에\s*숫자?\s*["\']?10["\']?\s*(?:만\s*)?(?:남겨주시면|입력)?\s*,?', '', cta_raw).strip()
        cta_lines = self._wrap_text(cta_sub or cta_raw, max_chars=18)

        d3.text((540, 1040), "댓글 남겨주시면 즉시", fill=(203, 213, 225), font=font_hero, anchor="mm")
        y_cta = 1120
        for l in cta_lines[:2]:
            d3.text((540, y_cta), l, fill=(254, 240, 138), font=font_hero, anchor="mm")
            y_cta += 80
        d3.text((540, 1330), "(별도 앱 설치 및 회원가입 불필요)", fill=(148, 163, 184), font=font_sub, anchor="mm")

        d3.text((540, 1780), "Blogin 365 AI • Quad-Monetization Engine", fill=(148, 163, 184), font=font_sub, anchor="mm")
        p3 = os.path.join(output_dir, "slide_03_cta.png")
        im3.save(p3)
        slide_paths.append(p3)

        return slide_paths

    def _wrap_text(self, text: str, max_chars: int = 18) -> List[str]:
        """Wraps text cleanly without breaking words abruptly."""
        words = text.split()
        lines = []
        current = ""
        for w in words:
            if len(current) + len(w) + 1 <= max_chars:
                current = (current + " " + w).strip()
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    def render_mp4_video(
        self,
        audio_path: str,
        slide_images: List[str],
        output_mp4: str,
        segments: List[Dict[str, Any]],
        total_duration: float = 15.0
    ) -> bool:
        """
        Renders 9:16 vertical 1080x1920 MP4 video combining slides and voiceover using FFmpeg.
        """
        if not self._ffmpeg_exe or len(slide_images) < 3:
            return False

        try:
            # Calibrated durations for each slide
            d1 = segments[0]["duration"]
            d2 = segments[1]["duration"]
            d3 = segments[2]["duration"]

            concat_txt = os.path.join(os.path.dirname(output_mp4), "slides_concat.txt")
            with open(concat_txt, "w", encoding="utf-8") as f:
                f.write(f"file '{os.path.abspath(slide_images[0]).replace(chr(92), '/')}'\n")
                f.write(f"duration {d1:.2f}\n")
                f.write(f"file '{os.path.abspath(slide_images[1]).replace(chr(92), '/')}'\n")
                f.write(f"duration {d2:.2f}\n")
                f.write(f"file '{os.path.abspath(slide_images[2]).replace(chr(92), '/')}'\n")
                f.write(f"duration {d3:.2f}\n")
                f.write(f"file '{os.path.abspath(slide_images[2]).replace(chr(92), '/')}'\n")

            cmd = [
                self._ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", concat_txt,
                "-i", audio_path,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "128k",
                "-t", f"{total_duration:.2f}",
                output_mp4
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(output_mp4) and os.path.getsize(output_mp4) > 1000:
                try:
                    os.remove(concat_txt)
                except Exception:
                    pass
                return True
        except Exception:
            pass
        return False

    def create_video_package(
        self,
        topic: Dict[str, Any],
        reel_script: Dict[str, str],
        render_video: bool = True
    ) -> Dict[str, Any]:
        """
        Creates complete MoneyPrinterTurbo compatible package in data/video_render_queue/{batch_id}/.
        Dynamically aligns duration, subtitles, and slide cues to voiceover audio.
        """
        batch_id = f"MPT-{int(time.time())}"
        target_dir = os.path.join(self.render_dir, batch_id)
        os.makedirs(target_dir, exist_ok=True)

        keyword = topic.get("keyword", "2026 청년 정책")
        title = topic.get("title", f"{keyword} 핵심 가이드")

        # 1. Generate Subtitles & Preliminary Segments
        segments, _ = self.generate_subtitles(reel_script, total_duration=15.0)

        # 2. Synthesize Voiceover Audio
        audio_path = os.path.join(target_dir, "voiceover.mp3")
        tts_res = self.synthesize_voiceover(segments, audio_path)
        actual_duration = max(5.0, tts_res.get("duration_sec", 15.0))

        # 3. Calibrate Segments & Subtitles to Actual Spoken Duration (Prevents Audio Truncation)
        segments, srt_content = self.calibrate_segments_to_duration(segments, actual_duration)
        srt_path = os.path.join(target_dir, "subtitles.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        sub_json_path = os.path.join(target_dir, "subtitles.json")
        with open(sub_json_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)

        # 4. Generate 9:16 Slide Images with Dynamic CTA & Backgrounds
        assets_dir = os.path.join(target_dir, "assets")
        slide_images = self.generate_slide_assets(topic, segments, assets_dir)

        # 5. Render Video (Matching full spoken audio duration)
        video_path = os.path.join(target_dir, "short_reel.mp4")
        video_rendered = False
        if render_video and self._ffmpeg_exe:
            video_rendered = self.render_mp4_video(
                audio_path=audio_path,
                slide_images=slide_images,
                output_mp4=video_path,
                segments=segments,
                total_duration=actual_duration
            )

        status = "COMPLETED" if video_rendered else ("AUDIO_READY" if tts_res["success"] else "QUEUED")

        # 5. Export MoneyPrinterTurbo Compatible Manifest
        money_printer_spec = {
            "task_id": batch_id,
            "video_subject": keyword,
            "video_script": " ".join([s["text"] for s in segments]),
            "video_terms": [keyword, topic.get("category", "SUBSIDY"), "2026", "모의계산"],
            "video_aspect": "9:16",
            "video_concat_mode": "sequential",
            "video_clip_duration": 5,
            "voice_name": tts_res.get("voice", self.default_voice),
            "voice_rate": 1.0,
            "voice_volume": 1.0,
            "bgm_type": "random",
            "bgm_volume": 0.2,
            "subtitle_enabled": True,
            "font_name": "malgunbd.ttf",
            "text_fore_color": "#FFFFFF",
            "text_background_color": "transparent",
            "stroke_color": "#000000",
            "stroke_width": 1.5,
            "status": status,
            "rendered_file": "short_reel.mp4" if video_rendered else None,
            "audio_file": "voiceover.mp3",
            "subtitles_file": "subtitles.srt"
        }

        manifest = {
            "batch_id": batch_id,
            "keyword": keyword,
            "category": topic.get("category", "SUBSIDY"),
            "title": title,
            "created_at": datetime.now().isoformat(),
            "status": status,
            "duration_sec": actual_duration,
            "aspect_ratio": "9:16",
            "resolution": "1080x1920",
            "manifest_dir": target_dir,
            "subtitles_srt": srt_path,
            "subtitles_json": sub_json_path,
            "audio_path": audio_path,
            "video_path": video_path if video_rendered else None,
            "assets": slide_images,
            "tts_meta": tts_res,
            "money_printer_turbo_spec": money_printer_spec
        }

        manifest_path = os.path.join(target_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        spec_path = os.path.join(target_dir, "money_printer_spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(money_printer_spec, f, ensure_ascii=False, indent=2)

        return manifest


if __name__ == "__main__":
    bridge = MoneyPrinterBridge()
    print("🚀 [MoneyPrinterBridge] Testing short-form package generation...")
    test_topic = {
        "keyword": "2026 청년도약계좌",
        "category": "SUBSIDY",
        "title": "2026 청년도약계좌 정부기여금 개편안 및 실제 만기 수령액 모의계산"
    }
    test_reel = {
        "0-3초_후킹": '[화면: 붉은 경고 뱃지 + 볼드 텍스트]\n🎙️ "2026 청년도약계좌, 신청 안 하면 전액 소멸됩니다."',
        "3-10초_핵심내용": '[화면: 인터랙티브 표 빠르게 전개]\n🎙️ "복잡한 약관 뒤질 필요 없이, 30초 간편 자격 모의 조회기로 1인당 평균 42만원 환급 결과를 바로 확인할 수 있습니다."',
        "10-15초_행동유도(CTA)": '[화면: 댓글창 애니메이션 + \'10\' 입력 효과]\n🎙️ "댓글에 숫자 \'10\'만 남겨주시면, 이 계산기와 상세 비교표 링크를 1초 만에 DM으로 보내드립니다!"'
    }
    pkg = bridge.create_video_package(test_topic, test_reel, render_video=True)
    print(f" - Batch ID: {pkg['batch_id']}")
    print(f" - Status: {pkg['status']}")
    print(f" - Audio: {pkg['audio_path']} (TTS method: {pkg['tts_meta']['method']})")
    print(f" - Video: {pkg['video_path']}")
    print(f" - Assets: {len(pkg['assets'])} slides")
