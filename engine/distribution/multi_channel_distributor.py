# -*- coding: utf-8 -*-
"""
engine/distribution/multi_channel_distributor.py
------------------------------------------------
Multi-Channel Distribution Engine (Pillar 3).
Extends the Viral Hook Maker into an active multi-platform syndicate dispatcher:
1. Formats payloads tailored for Threads, X/Twitter, ManyChat Webhooks, Kakao View, and Pinterest.
2. Manages persistent queue in data/distribution_queue.json and execution log in data/distribution_history.json.
3. Automatically triggers seed external traffic to newly published posts, breaking Google sandbox periods.
"""

import os
import sys
import re
import json
import time
import logging
import urllib.request
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, "SEO.env"))
except ImportError:
    pass

logger = logging.getLogger("MultiChannelDistributor")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

WEBHOOK_ENV_MAP = {
    "threads": ["THREADS_WEBHOOK_URL", "THREAD_WEBHOOK_URL", "INSTAGRAM_WEBHOOK_URL"],
    "twitter_x": ["X_WEBHOOK_URL", "TWITTER_WEBHOOK_URL", "TWITTER_X_WEBHOOK_URL"],
    "manychat_webhook": ["MANYCHAT_WEBHOOK_URL", "MANYCHAT_URL"],
    "kakao_view": ["KAKAO_VIEW_WEBHOOK_URL", "KAKAO_WEBHOOK_URL"],
}


class MultiChannelDistributor:
    """
    Syndicates post hooks and summaries across multi-channel social networks
    and webhook listeners (ManyChat, Discord, Slack, Zapier, Threads, X).
    """
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            self.data_dir = os.path.join(BASE_DIR, "data")
        else:
            self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

        self.queue_file = os.path.join(self.data_dir, "distribution_queue.json")
        self.history_file = os.path.join(self.data_dir, "distribution_history.json")
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.queue_file):
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)


    def format_channel_payloads(self, growth_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates platform-optimized payloads from the growth package.
        """
        kw = growth_package.get("keyword", "")
        title = growth_package.get("title", "")
        post_url = growth_package.get("post_url", "https://blogin365ai.blogspot.com")
        sns_caption = growth_package.get("sns_caption", "")
        reel_script = growth_package.get("reel_script", {})
        hook_0_3 = reel_script.get("0-3초_후킹", "")

        # 1. Instagram / Threads Payload
        caption_body = sns_caption.strip()
        if len(caption_body) > 400:
            caption_trimmed = caption_body[:400].rsplit(" ", 1)[0] + "..."
        else:
            caption_trimmed = caption_body

        parts = []
        if title and title not in caption_trimmed:
            parts.append(f"🔥 {title}")
        if caption_trimmed:
            parts.append(caption_trimmed)
        if post_url and post_url not in caption_trimmed:
            parts.append(f"👉 전체 계산기 및 가이드: {post_url}")

        threads_text = "\n\n".join(parts) if parts else f"🔥 {title}\n\n👉 가이드: {post_url}"
        tags = [kw.replace(" ", ""), "정보공유", "스마트라이프"] if kw else ["정보공유", "스마트라이프"]

        threads_payload = {
            "channel": "threads",
            "text": threads_text,
            "link_attachment_url": post_url,
            "topic_tags": [t for t in tags if t]
        }

        # 2. X (Twitter) Payload (Within 280 chars)
        clean_hook = re.sub(r'\[.*?\]', '', hook_0_3)
        clean_hook = clean_hook.replace('🎙️', '').strip().strip('"').strip()
        if not clean_hook:
            clean_hook = f"{kw} 핵심 기준과 실수령액 계산기 요약"

        x_text = f"💡 {title[:60]}\n\n{clean_hook[:90]}\n\n📊 모의계산기 & 상세표 즉시 확인:\n{post_url}"
        x_payload = {
            "channel": "twitter_x",
            "text": x_text,
            "url": post_url
        }

        # 3. ManyChat / Automation Webhook Payload (DM Keyword Trigger: "10")
        webhook_payload = {
            "channel": "manychat_webhook",
            "event": "new_editorial_post",
            "trigger_keyword": "10",
            "title": title,
            "keyword": kw,
            "post_url": post_url,
            "dm_response_copy": growth_package.get("dm_copy", f"안녕하세요! 요청하신 [{title}] 가이드 링크입니다: {post_url}"),
            "timestamp": datetime.now().isoformat()
        }

        # 4. Kakao View / Community Card Payload
        board_prefix = "[실측분석] " if not title.startswith("[") else ""
        kakao_payload = {
            "channel": "kakao_view",
            "board_title": f"{board_prefix}{title}"[:80],
            "summary": f"{kw} 핵심 기준과 실수령액 계산기 요약"[:120],
            "link_url": post_url,
            "category": growth_package.get("category", "INFO")
        }

        return {
            "threads": threads_payload,
            "twitter_x": x_payload,
            "manychat_webhook": webhook_payload,
            "kakao_view": kakao_payload
        }

    def get_channel_webhook_url(self, channel: str) -> Optional[str]:
        """Resolves target webhook URL for the specified channel from environment."""
        keys = WEBHOOK_ENV_MAP.get(channel, [f"{channel.upper()}_WEBHOOK_URL"])
        for k in keys:
            val = os.environ.get(k, "").strip()
            if val:
                return val
        fallback = os.environ.get("DISTRIBUTION_WEBHOOK_URL", "").strip()
        return fallback or None

    def dispatch_single_payload(
        self,
        channel: str,
        payload: Dict[str, Any],
        batch_id: str,
        dry_run: bool = False,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Dispatches a single platform payload:
        - dry_run: returns SIMULATED_SUCCESS
        - webhook_url present: attempts HTTP POST (via requests or urllib)
        - webhook_url missing: returns QUEUED for offline workers
        """
        if dry_run:
            return {
                "status": "SIMULATED_SUCCESS",
                "channel": channel,
                "platform": channel,
                "batch_id": batch_id,
                "payload_size": len(json.dumps(payload)),
                "timestamp": datetime.now().isoformat()
            }

        webhook_url = self.get_channel_webhook_url(channel)
        if not webhook_url:
            return {
                "status": "QUEUED",
                "channel": channel,
                "platform": channel,
                "batch_id": batch_id,
                "note": "Ready in queue for social bot worker",
                "timestamp": datetime.now().isoformat()
            }

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Blogin365AI-Distributor/2.0"
        }

        # 1. Attempt using requests library
        use_urllib = False
        try:
            import requests
            resp = requests.post(webhook_url, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            logger.info(f"[Distributor] {channel} 웹훅 발송 성공 ({resp.status_code}): {webhook_url}")
            return {
                "status": "SENT",
                "channel": channel,
                "platform": channel,
                "code": resp.status_code,
                "batch_id": batch_id,
                "timestamp": datetime.now().isoformat()
            }
        except ImportError:
            use_urllib = True
        except Exception as e:
            logger.error(f"[Distributor] {channel} requests 발송 실패: {e}")
            return {
                "status": "QUEUED_RETRY",
                "channel": channel,
                "platform": channel,
                "batch_id": batch_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

        # 2. Resilient fallback using standard urllib.request (only if requests not installed)
        if use_urllib:
            try:
                req_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(webhook_url, data=req_bytes, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    status_code = resp.getcode()
                    logger.info(f"[Distributor] {channel} urllib 웹훅 발송 성공 ({status_code})")
                    return {
                        "status": "SENT",
                        "channel": channel,
                        "platform": channel,
                        "code": status_code,
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat()
                    }
            except Exception as e:
                logger.error(f"[Distributor] {channel} urllib 웹훅 실패: {e}")
                return {
                    "status": "QUEUED_RETRY",
                    "channel": channel,
                    "platform": channel,
                    "batch_id": batch_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

    def dispatch_to_channels(
        self,
        growth_package: Dict[str, Any],
        channels: Optional[List[str]] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Dispatches or enqueues social publication payloads.
        """
        payloads = self.format_channel_payloads(growth_package)
        selected_channels = channels or list(payloads.keys())
        dispatch_results = {}

        dispatch_batch_id = f"DIST-{int(time.time())}"

        for ch in selected_channels:
            p_data = payloads.get(ch)
            if not p_data:
                continue

            dispatch_results[ch] = self.dispatch_single_payload(
                channel=ch,
                payload=p_data,
                batch_id=dispatch_batch_id,
                dry_run=dry_run
            )

        if dry_run:
            overall_status = "SIMULATED_SUCCESS"
        else:
            statuses = [res.get("status") for res in dispatch_results.values()]
            if all(s == "SENT" for s in statuses):
                overall_status = "SENT"
            elif all(s == "QUEUED" for s in statuses):
                overall_status = "QUEUED"
            elif any(s == "QUEUED_RETRY" for s in statuses):
                overall_status = "QUEUED_RETRY"
            else:
                overall_status = "PARTIAL"

        record = {
            "status": overall_status,
            "batch_id": dispatch_batch_id,
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "keyword": growth_package.get("keyword"),
            "post_url": growth_package.get("post_url"),
            "channels": dispatch_results,
            "payloads": payloads
        }

        self._save_to_queue(record)
        self._record_history(record)

        return record

    def _save_to_queue(self, record: Dict[str, Any]):
        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                queue = json.load(f)
                if not isinstance(queue, list):
                    queue = []
            queue.insert(0, record)
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(queue[:100], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _record_history(self, record: Dict[str, Any]):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
            history.insert(0, record)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history[:100], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_queue(self) -> List[Dict[str, Any]]:
        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []


def dispatch_to_all_channels(growth_package: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    distributor = MultiChannelDistributor()
    return distributor.dispatch_to_channels(growth_package, dry_run=dry_run)


def distribute_post(
    title: str,
    url: str,
    hook: str,
    channels: Optional[List[str]] = None,
    category: str = "INFO",
    dry_run: bool = False,
    data_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    단일 포스트에 대한 멀티채널 배포 진입점 (GEMINI_INSTRUCTIONS 표준 준수).
    웹훅 URL이 환경변수에 있으면 즉시 발송(SENT), 없으면 큐에 안전 적재(QUEUED).
    """
    distributor = MultiChannelDistributor(data_dir=data_dir)
    growth_package = {
        "keyword": title,
        "title": title,
        "post_url": url,
        "category": category,
        "reel_script": {
            "0-3초_후킹": hook,
            "3-10초_핵심내용": f"{title} 핵심 분석 및 수혜 조건",
            "10-15초_행동유도(CTA)": "댓글에 10 남겨주시면 가이드 자동 발송"
        },
        "sns_caption": f"💡 {title}\n\n{hook}\n\n👉 공식 계산기 및 상세 가이드:\n{url}",
        "dm_copy": f"안녕하세요! 요청하신 [{title}] 가이드 링크입니다: {url}"
    }
    return distributor.dispatch_to_channels(growth_package, channels=channels, dry_run=dry_run)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dist = MultiChannelDistributor()
    sample_pkg = {
        "keyword": "2026 청년도약계좌",
        "title": "2026 청년도약계좌 실수령액 모의계산 및 자격 조건 핵심 가이드",
        "post_url": "https://blogin365ai.blogspot.com/preview.html",
        "category": "SUBSIDY",
        "reel_script": {
            "0-3초_후킹": "[화면: 붉은 경고 뱃지]\n🎙️ \"2026 청년도약계좌 지금 모르면 최대 5천만원 기회 놓칩니다.\""
        },
        "sns_caption": "2026 청년도약계좌 실측 비교 가이드...",
        "dm_copy": "안녕하세요! 요청하신 계산기 링크 보내드립니다."
    }
    res = dist.dispatch_to_channels(sample_pkg, dry_run=True)
    print("=== Multi-Channel Distribution Test ===")
    print("Batch ID:", res["batch_id"])
    print("Channels queued:", list(res["channels"].keys()))
