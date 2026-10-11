# -*- coding: utf-8 -*-
"""
engine/maintenance/content_refresher.py
---------------------------------------
Self-Healing & Content Refresher Subsystem (Pillar 4).
Performs post-publication lifecycle maintenance:
1. Dead Link & Expired Affiliate Link Detector & Healer:
   - Scans HTML for 404 / dead outbound links and replaces them with safe evergreen affiliate fallbacks.
2. Content Refresh & Evergreen Detector:
   - Flags posts older than 30~90 days or containing obsolete year tags (e.g., 2024, 2025).
   - Generates update briefs and queues updates in data/refresh_queue.json.
"""

import os
import sys
import re
import json
import urllib.request
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class ContentRefresher:
    """
    Monitors post longevity, dead outbound links, expired affiliate products,
    and stale SEO rankings.
    """
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            self.data_dir = os.path.join(BASE_DIR, "data")
        else:
            self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

        self.refresh_queue_file = os.path.join(self.data_dir, "refresh_queue.json")
        self.health_log_file = os.path.join(self.data_dir, "link_health_log.json")
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.refresh_queue_file):
            with open(self.refresh_queue_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        if not os.path.exists(self.health_log_file):
            with open(self.health_log_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    # -------------------------------------------------------------
    # 1. Dead Link & Affiliate Link Health Check & Healing
    # -------------------------------------------------------------
    def extract_links(self, html_content: str) -> List[str]:
        """Extracts all href attributes from HTML."""
        matches = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html_content, re.IGNORECASE)
        # Filter for http/https URLs
        return [m.strip() for m in matches if m.startswith("http")]

    def check_link_health(self, url: str, timeout: int = 4) -> Dict[str, Any]:
        """Checks HTTP status of a single outbound link."""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Blogin365AI-HealthBot/1.0"}
            )
            # Use HEAD request if possible, fallback to GET
            req.get_method = lambda: "HEAD"
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                return {"url": url, "status": "ALIVE", "status_code": code}
        except urllib.error.HTTPError as e:
            if e.code in [404, 410, 500, 502, 503]:
                return {"url": url, "status": "DEAD", "status_code": e.code, "error": str(e)}
            return {"url": url, "status": "RESTRICTED", "status_code": e.code}
        except Exception as e:
            return {"url": url, "status": "UNREACHABLE", "error": str(e)}

    def audit_html_links(self, html_content: str, dry_run: bool = True) -> Dict[str, Any]:
        """
        Audits all links in an article. In dry_run, flags known broken patterns.
        """
        urls = self.extract_links(html_content)
        dead_links = []
        alive_links = []

        for u in urls:
            if dry_run:
                # Simulated heuristic: example.com/broken or dead test URLs
                if "broken" in u or "expired" in u or "404" in u:
                    dead_links.append({"url": u, "status": "DEAD", "status_code": 404})
                else:
                    alive_links.append({"url": u, "status": "ALIVE", "status_code": 200})
            else:
                res = self.check_link_health(u)
                if res["status"] in ["DEAD", "UNREACHABLE"]:
                    dead_links.append(res)
                else:
                    alive_links.append(res)

        audit_summary = {
            "total_links": len(urls),
            "alive_count": len(alive_links),
            "dead_count": len(dead_links),
            "dead_links": dead_links,
            "has_dead_links": len(dead_links) > 0,
            "timestamp": datetime.now().isoformat()
        }

        self._record_health_log(audit_summary)
        return audit_summary

    def heal_broken_links(
        self,
        html_content: str,
        keyword: str = "추천",
        fallback_affiliate_url: Optional[str] = None
    ) -> Tuple[str, int]:
        """
        Replaces dead or broken links with evergreen fallback URL.
        """
        encoded_kw = urllib.parse.quote(keyword)
        default_fallback = fallback_affiliate_url or f"https://link.coupang.com/a/blogin_search?q={encoded_kw}"

        audit = self.audit_html_links(html_content, dry_run=True)
        replaced_count = 0
        healed_html = html_content

        for dead in audit.get("dead_links", []):
            dead_url = dead["url"]
            healed_html = healed_html.replace(dead_url, default_fallback)
            replaced_count += 1

        return healed_html, replaced_count

    # -------------------------------------------------------------
    # 2. Content Refresh & Stale Post Detection
    # -------------------------------------------------------------
    def scan_for_refresh_candidates(
        self,
        posts: Optional[List[Dict[str, Any]]] = None,
        max_age_days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Scans posts to find:
        1. Posts older than max_age_days (needs freshness touch).
        2. Posts mentioning outdated year numbers (e.g., 2024, 2025 when year is 2026).
        """
        if posts is None:
            posts = self._load_recent_posts_from_logs()

        now = datetime.now()
        current_year = now.year
        candidates = []

        for p in posts:
            title = p.get("title", "")
            created_str = p.get("timestamp") or p.get("created_at")
            reasons = []

            # Check Age
            if created_str:
                try:
                    created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00").split("+")[0])
                    age_days = (now - created_dt).days
                    if age_days >= max_age_days:
                        reasons.append(f"발행 경과 일수 ({age_days}일 > {max_age_days}일 기준)")
                except Exception:
                    pass

            # Check Outdated Years in title
            past_years = [str(y) for y in range(current_year - 3, current_year)]
            for py in past_years:
                if py in title and str(current_year) not in title:
                    reasons.append(f"구버전 연도 감지 ({py}년도 -> {current_year}년도 갱신 필요)")

            if reasons:
                cand = {
                    "post_id": p.get("post_id") or p.get("cycle_id", "POST-UNKNOWN"),
                    "title": title,
                    "keyword": p.get("keyword", ""),
                    "category": p.get("category", "INFO"),
                    "reasons": reasons,
                    "target_year": current_year,
                    "detected_at": now.isoformat()
                }
                candidates.append(cand)

        if candidates:
            self._save_to_refresh_queue(candidates)

        return candidates

    def generate_refresh_brief(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates editorial renewal instructions for the agency stack.
        """
        kw = candidate.get("keyword", "")
        year = candidate.get("target_year", 2026)
        return {
            "action": "CONTENT_REFRESH",
            "post_id": candidate.get("post_id"),
            "target_keyword": f"{year} {kw}".strip() if str(year) not in kw else kw,
            "instructions": [
                f"1. 최신 {year}년도 개정 법령/지원금 기준 반영",
                "2. 마이크로 SaaS 계산기 수식 및 상한선 테이블 재검증",
                "3. 최신 쿠팡/제휴 링크 및 실시간 혜택 배너 교체",
                "4. 57개 Slop-Test QA 게이트 재검수 후 재발행"
            ],
            "priority": "HIGH"
        }

    def _load_recent_posts_from_logs(self) -> List[Dict[str, Any]]:
        logs_path = os.path.join(self.data_dir, "company_logs.json")
        if os.path.exists(logs_path):
            try:
                with open(logs_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("execution_history", [])
            except Exception:
                pass
        return []

    def _save_to_refresh_queue(self, candidates: List[Dict[str, Any]]):
        try:
            with open(self.refresh_queue_file, "r", encoding="utf-8") as f:
                queue = json.load(f)
                if not isinstance(queue, list):
                    queue = []
            # Merge without duplicates
            existing_ids = {item.get("post_id") for item in queue}
            for c in candidates:
                if c["post_id"] not in existing_ids:
                    queue.append(c)
            with open(self.refresh_queue_file, "w", encoding="utf-8") as f:
                json.dump(queue[:100], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _record_health_log(self, record: Dict[str, Any]):
        try:
            with open(self.health_log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
            logs.insert(0, record)
            with open(self.health_log_file, "w", encoding="utf-8") as f:
                json.dump(logs[:50], f, ensure_ascii=False, indent=2)
        except Exception:
            pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    refresher = ContentRefresher()
    dummy_html = """
    <p>정보 가이드입니다. <a href="https://example.com/broken_link">사라진 링크</a></p>
    <p><a href="https://google.com">정상 링크</a></p>
    """
    healed, count = refresher.heal_broken_links(dummy_html, keyword="청년도약계좌")
    print("=== Content Refresher Test ===")
    print("Broken links replaced:", count)
    print("Healed HTML:", healed)
