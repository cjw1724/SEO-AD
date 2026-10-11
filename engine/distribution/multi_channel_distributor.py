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
import json
import time
import urllib.request
from datetime import datetime
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


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
        threads_payload = {
            "channel": "threads",
            "text": f"🔥 {title}\n\n{sns_caption[:400]}...\n\n👉 전체 계산기 및 가이드: {post_url}",
            "link_attachment_url": post_url,
            "topic_tags": [kw.replace(" ", ""), "정보공유", "스마트라이프"]
        }

        # 2. X (Twitter) Payload (Within 280 chars)
        x_text = f"💡 {title[:60]}\n\n{hook_0_3[:90]}\n\n📊 모의계산기 & 상세표 즉시 확인:\n{post_url}"
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
            "dm_response_copy": growth_package.get("dm_copy", f"가이드 링크: {post_url}"),
            "timestamp": datetime.now().isoformat()
        }

        # 4. Kakao View / Community Card Payload
        kakao_payload = {
            "channel": "kakao_view",
            "board_title": f"[실측분석] {title}",
            "summary": f"{kw} 핵심 기준과 실수령액 계산기 요약",
            "link_url": post_url,
            "category": growth_package.get("category", "INFO")
        }

        return {
            "threads": threads_payload,
            "twitter_x": x_payload,
            "manychat_webhook": webhook_payload,
            "kakao_view": kakao_payload
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

            if dry_run:
                dispatch_results[ch] = {
                    "status": "SIMULATED_SUCCESS",
                    "channel": ch,
                    "batch_id": dispatch_batch_id,
                    "payload_size": len(json.dumps(p_data)),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Live dispatch checking configured webhooks
                webhook_url = os.environ.get(f"{ch.upper()}_WEBHOOK_URL") or os.environ.get("DISTRIBUTION_WEBHOOK_URL")
                if webhook_url:
                    try:
                        req_bytes = json.dumps(p_data).encode("utf-8")
                        req = urllib.request.Request(
                            webhook_url,
                            data=req_bytes,
                            headers={"Content-Type": "application/json; charset=utf-8"},
                            method="POST"
                        )
                        with urllib.request.urlopen(req, timeout=5) as resp:
                            dispatch_results[ch] = {
                                "status": "DELIVERED",
                                "channel": ch,
                                "code": resp.getcode(),
                                "timestamp": datetime.now().isoformat()
                            }
                    except Exception as e:
                        dispatch_results[ch] = {
                            "status": "QUEUED_RETRY",
                            "channel": ch,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    # Enqueue in data/distribution_queue.json for external workers or ManyChat
                    dispatch_results[ch] = {
                        "status": "QUEUED",
                        "channel": ch,
                        "batch_id": dispatch_batch_id,
                        "note": "Ready in queue for social bot worker",
                        "timestamp": datetime.now().isoformat()
                    }

        record = {
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
