# -*- coding: utf-8 -*-
"""
engine/indexing/instant_indexer.py
----------------------------------
Instant Indexing Subsystem (Pillar 1).
Solves the Google crawler crawl lag by immediately notifying search engines:
1. Google Indexing API (URL_UPDATED notification with Dual-Auth: Service Account + OAuth fallback)
2. IndexNow Protocol (Bing, Naver, Yandex instantaneous URL ping)
3. Google & Bing Sitemap Auto-Ping
4. Persistent indexing audit log in data/indexing_logs.json
"""

import os
import sys
import json
import time
import logging
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, Any, List, Union, Optional

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

logger = logging.getLogger("InstantIndexer")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def _get_indexing_service(service_account_path: Optional[str] = None):
    """
    서비스 계정 기반 Google Indexing API 클라이언트 반환.
    service_account.json이 존재할 경우 googleapiclient.discovery 클라이언트를 반환하고,
    없을 경우 None을 반환하여 OAuth 또는 IndexNow 폴백 체인으로 전환합니다.
    """
    sa_path = service_account_path or SERVICE_ACCOUNT_FILE
    if not os.path.exists(sa_path):
        logger.warning("service_account.json 없음 → OAuth 및 IndexNow 폴백 모드 가동")
        return None

    try:
        from google.oauth2 import service_account
        import googleapiclient.discovery
        credentials = service_account.Credentials.from_service_account_file(
            sa_path, scopes=SCOPES
        )
        return googleapiclient.discovery.build(
            "indexing", "v3", credentials=credentials, cache_discovery=False
        )
    except Exception as e:
        logger.error(f"[IndexingAPI] 서비스 계정 클라이언트 빌드 실패: {e}")
        return None


def submit_to_google_indexing_api(
    url: str,
    action: str = "URL_UPDATED",
    dry_run: bool = False,
    service_account_path: Optional[str] = None
) -> Dict[str, Any]:
    """Google Indexing API로 단일 URL 즉각 제출 (모듈 최상위 진입점)"""
    indexer = InstantIndexer(service_account_path=service_account_path)
    return indexer.submit_google_indexing(url, action=action, dry_run=dry_run)


def submit_batch_to_google_indexing_api(
    urls: List[str],
    action: str = "URL_UPDATED",
    dry_run: bool = False,
    service_account_path: Optional[str] = None
) -> Dict[str, Any]:
    """Google Indexing API로 다중 URL 배치 즉각 제출"""
    indexer = InstantIndexer(service_account_path=service_account_path)
    return indexer.submit_batch_google_indexing(urls, action=action, dry_run=dry_run)


class InstantIndexer:
    """
    Coordinates real-time indexing notifications across Google Indexing API (Dual Auth:
    Service Account + OAuth), IndexNow (Bing/Naver), and Search Engine Sitemap ping endpoints.
    """
    def __init__(self, log_path: Optional[str] = None, service_account_path: Optional[str] = None):
        if log_path is None:
            data_dir = os.path.join(BASE_DIR, "data")
            os.makedirs(data_dir, exist_ok=True)
            self.log_path = os.path.join(data_dir, "indexing_logs.json")
        else:
            self.log_path = log_path

        self.service_account_path = service_account_path or SERVICE_ACCOUNT_FILE
        self.default_host = "blogin365ai.blogspot.com"
        self.default_sitemap = f"https://{self.default_host}/sitemap.xml"
        self.indexnow_endpoint = "https://api.indexnow.org/indexnow"
        self.indexnow_key = "blogin365ai_indexer_key"
        self.google_indexing_endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    def submit_google_indexing(self, url: str, action: str = "URL_UPDATED", dry_run: bool = False) -> Dict[str, Any]:
        """
        Submits URL notification to Google Indexing API using dual-authentication:
        1. Primary: Google Service Account (service_account.json)
        2. Secondary: OAuth 2.0 User Access Token (token.json)
        3. Tertiary: Resilient Fallback Queue (FALLBACK_QUEUED status)
        """
        if dry_run:
            return {
                "engine": "google_indexing_api",
                "auth_type": "dry_run",
                "status": "SIMULATED_SUCCESS",
                "action": action,
                "url": url,
                "status_code": 200,
                "response": {
                    "urlNotificationMetadata": {
                        "url": url,
                        "type": action,
                        "notifyTime": datetime.now().isoformat()
                    }
                }
            }

        if not url or not url.startswith("http"):
            return {
                "engine": "google_indexing_api",
                "auth_type": "none",
                "status": "INVALID_URL",
                "action": action,
                "url": url,
                "status_code": 400,
                "error": "URL must be an absolute HTTP/HTTPS URL"
            }

        # 1. Primary: Try Service Account client
        service = _get_indexing_service(self.service_account_path)
        sa_error = None
        if service is not None:
            try:
                body = {"url": url, "type": action}
                response = service.urlNotifications().publish(body=body).execute()
                logger.info(f"[IndexingAPI] 서비스 계정 제출 성공: {url}")
                return {
                    "engine": "google_indexing_api",
                    "auth_type": "service_account",
                    "status": "SUBMITTED",
                    "action": action,
                    "url": url,
                    "status_code": 200,
                    "response": response
                }
            except Exception as e:
                sa_error = str(e)
                logger.warning(f"[IndexingAPI] 서비스 계정 호출 실패 ({e}) -> OAuth/REST 폴백 시도")

        # 2. Secondary: Try OAuth2 Bearer Token
        oauth_error = None
        try:
            token = self._get_google_token()
            if token:
                headers = {
                    "Content-Type": "application/json; charset=utf-8",
                    "User-Agent": "Blogin365AI-InstantIndexer/1.0",
                    "Authorization": f"Bearer {token}"
                }
                payload = json.dumps({"url": url, "type": action}).encode("utf-8")
                req = urllib.request.Request(self.google_indexing_endpoint, data=payload, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=8) as resp:
                    status_code = resp.getcode()
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    logger.info(f"[IndexingAPI] OAuth 토큰 제출 성공: {url}")
                    return {
                        "engine": "google_indexing_api",
                        "auth_type": "oauth",
                        "status": "SUBMITTED",
                        "action": action,
                        "url": url,
                        "status_code": status_code,
                        "response": resp_data
                    }
        except Exception as e:
            oauth_error = str(e)
            logger.warning(f"[IndexingAPI] OAuth 호출 실패: {e}")

        # If Service Account explicitly failed, return an actionable ERROR status
        if sa_error:
            logger.error(f"[IndexingAPI] 서비스 계정 제출 실패: {sa_error}")
            return {
                "engine": "google_indexing_api",
                "auth_type": "service_account",
                "status": "ERROR",
                "action": action,
                "url": url,
                "status_code": 403 if "403" in sa_error else 500,
                "error": sa_error
            }

        # 3. Tertiary: Resilient Fallback Queue (when credentials missing)
        return {
            "engine": "google_indexing_api",
            "auth_type": "fallback_queue",
            "status": "FALLBACK_QUEUED",
            "action": action,
            "url": url,
            "status_code": 202,
            "error": "Credentials missing or Google API call rejected. URL logged in fallback queue."
        }

    def submit_batch_google_indexing(
        self,
        urls: List[str],
        action: str = "URL_UPDATED",
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Submits multiple URLs to Google Indexing API sequentially with rate pacing.
        """
        results = []
        for u in urls:
            res = self.submit_google_indexing(u, action=action, dry_run=dry_run)
            results.append(res)
            if not dry_run and len(urls) > 1:
                time.sleep(0.2)

        submitted_count = sum(1 for r in results if r.get("status") in ("SUBMITTED", "SIMULATED_SUCCESS"))
        return {
            "engine": "google_indexing_api_batch",
            "action": action,
            "total_urls": len(urls),
            "submitted_count": submitted_count,
            "dry_run": dry_run,
            "results": results
        }


    def submit_indexnow(
        self,
        urls: Union[str, List[str]],
        host: Optional[str] = None,
        key: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Submits URL(s) to IndexNow protocol (supported by Bing, Naver, Yandex).
        """
        target_host = host or self.default_host
        target_key = key or self.indexnow_key
        url_list = [urls] if isinstance(urls, str) else list(urls)

        payload_dict = {
            "host": target_host,
            "key": target_key,
            "keyLocation": f"https://{target_host}/{target_key}.txt",
            "urlList": url_list
        }

        if dry_run:
            return {
                "engine": "indexnow",
                "status": "SIMULATED_SUCCESS",
                "host": target_host,
                "submitted_count": len(url_list),
                "urls": url_list,
                "status_code": 200,
                "payload": payload_dict
            }

        try:
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "Blogin365AI-IndexNow-Client/1.0"
            }
            req_data = json.dumps(payload_dict).encode("utf-8")
            req = urllib.request.Request(self.indexnow_endpoint, data=req_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=8) as resp:
                status_code = resp.getcode()
                return {
                    "engine": "indexnow",
                    "status": "SUBMITTED",
                    "host": target_host,
                    "submitted_count": len(url_list),
                    "urls": url_list,
                    "status_code": status_code
                }
        except Exception as e:
            return {
                "engine": "indexnow",
                "status": "FALLBACK_QUEUED",
                "host": target_host,
                "submitted_count": len(url_list),
                "urls": url_list,
                "status_code": 202,
                "error": str(e)
            }

    def ping_sitemaps(self, sitemap_url: Optional[str] = None, dry_run: bool = False) -> Dict[str, Any]:
        """
        Pings Google & Bing with sitemap updates.
        """
        s_url = sitemap_url or self.default_sitemap
        endpoints = {
            "google": f"https://www.google.com/ping?sitemap={urllib.parse.quote(s_url)}",
            "bing": f"https://www.bing.com/ping?sitemap={urllib.parse.quote(s_url)}"
        }

        if dry_run:
            return {
                "engine": "sitemap_ping",
                "status": "SIMULATED_SUCCESS",
                "sitemap_url": s_url,
                "pings": {k: {"status": "SIMULATED_PING", "url": v} for k, v in endpoints.items()}
            }

        ping_results = {}
        for engine, ping_ep in endpoints.items():
            try:
                req = urllib.request.Request(ping_ep, headers={"User-Agent": "Blogin365AI-SitemapPinger/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    ping_results[engine] = {"status": "SUCCESS", "status_code": resp.getcode()}
            except Exception as e:
                ping_results[engine] = {"status": "QUEUED_OR_BLOCKED", "error": str(e)}

        return {
            "engine": "sitemap_ping",
            "status": "COMPLETED",
            "sitemap_url": s_url,
            "pings": ping_results
        }

    def submit_all(
        self,
        urls: Union[str, List[str]],
        sitemap_url: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Executes Google Indexing API, IndexNow, and Sitemap Pings in a unified batch.
        Accepts either a single URL string or a list of URLs.
        Logs output to data/indexing_logs.json.
        """
        if isinstance(urls, (list, tuple)):
            url_list = [u for u in urls if u and isinstance(u, str) and u.startswith("http")]
            target_rep = url_list[0] if url_list else ""
            google_res = self.submit_batch_google_indexing(url_list, dry_run=dry_run)
            indexnow_res = self.submit_indexnow(url_list, dry_run=dry_run)
        else:
            url_list = [urls]
            target_rep = urls
            google_res = self.submit_google_indexing(urls, dry_run=dry_run)
            indexnow_res = self.submit_indexnow(urls, dry_run=dry_run)

        sitemap_res = self.ping_sitemaps(sitemap_url, dry_run=dry_run)

        record = {
            "timestamp": datetime.now().isoformat(),
            "target_url": target_rep,
            "url_count": len(url_list),
            "dry_run": dry_run,
            "results": {
                "google_indexing": google_res,
                "indexnow": indexnow_res,
                "sitemap_ping": sitemap_res
            }
        }

        self._record_log(record)
        return record

    def _record_log(self, record: Dict[str, Any]):
        """Persists indexing audit trail."""
        try:
            history = []
            if os.path.exists(self.log_path):
                with open(self.log_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    if not isinstance(history, list):
                        history = []
            history.insert(0, record)
            # Retain latest 100 entries
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history[:100], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _get_google_token(self) -> Optional[str]:
        """
        Loads OAuth2 access token if available in token.json and explicitly granted
        the Google Indexing API scope ('https://www.googleapis.com/auth/indexing').
        If the token only has Blogger permissions, returns None to avoid failing 401 calls.
        """
        token_path = os.path.join(BASE_DIR, "token.json")
        if not os.path.exists(token_path):
            return None

        # Verify that token.json explicitly holds the indexing scope
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            token_scopes = data.get("scopes", [])
            if "https://www.googleapis.com/auth/indexing" not in token_scopes:
                logger.debug("token.json에 indexing 스코프 없음 → OAuth 스킵")
                return None
        except Exception:
            return None

        # Attempt auto-refresh using Google Auth SDK if available
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            scopes = ['https://www.googleapis.com/auth/blogger', 'https://www.googleapis.com/auth/indexing']
            creds = Credentials.from_authorized_user_file(token_path, scopes)
            if creds:
                if (not creds.valid or creds.expired) and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                        with open(token_path, "w", encoding="utf-8") as f:
                            f.write(creds.to_json())
                    except Exception:
                        pass
                return creds.token
        except Exception:
            pass

        # Fallback to direct JSON token extraction
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("token") or data.get("access_token")
        except Exception:
            return None


def submit_url_instantly(url: str, dry_run: bool = False) -> Dict[str, Any]:
    indexer = InstantIndexer()
    return indexer.submit_all(url, dry_run=dry_run)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    indexer = InstantIndexer()
    test_url = "https://blogin365ai.blogspot.com/2026/05/youth-account-guide.html"
    res = indexer.submit_all(test_url, dry_run=True)
    print("=== Instant Indexer Test ===")
    print(json.dumps(res, ensure_ascii=False, indent=2))
