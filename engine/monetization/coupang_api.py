# -*- coding: utf-8 -*-
"""
engine/monetization/coupang_api.py
----------------------------------
Coupang Partners Open API Client with HMAC-SHA256 signature authentication.
Generates real-time affiliate tracking links for products and search queries,
with robust zero-crash fallback to standard search URLs when credentials are not configured.
"""

import os
import sys
import hmac
import hashlib
import urllib.parse
from datetime import datetime, timezone
from typing import Optional
import requests

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CoupangPartnersClient:
    """
    Official Coupang Partners Open API Gateway Client.
    Implements CEA algorithm=HmacSHA256 authorization header specification.
    """
    def __init__(self, access_key: str = "", secret_key: str = "", sub_id: str = "blogin365"):
        self.access_key = (access_key or "").strip()
        self.secret_key = (secret_key or "").strip()
        self.sub_id = (sub_id or "blogin365").strip()
        self.domain = "https://api-gateway.coupang.com"

    def _generate_hmac(self, method: str, url_path: str, query_string: str = "") -> str:
        now = datetime.now(timezone.utc).strftime("%y%m%dT%H%M%SZ")
        message = f"{now}{method}{url_path}{query_string}"
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return f"CEA algorithm=HmacSHA256, access-key={self.access_key}, signed-date={now}, signature={signature}"

    def get_affiliate_search_link(self, keyword: str) -> str:
        """
        Fetches official Coupang Partners affiliate link for given keyword:
        1. Tries product search API (/v2/providers/affiliate_open_api/apis/openapi/products/search)
           to obtain the #1 ranked product's direct affiliate tracking URL.
        2. If empty or fails, requests deeplink API (/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink)
           to produce a shortened 'link.coupang.com' tracking redirect.
        3. Falls back gracefully to standard search URL if API keys are missing or requests fail.
        """
        raw_coupang_url = f"https://www.coupang.com/np/search?q={urllib.parse.quote(keyword)}"
        if not self.access_key or not self.secret_key:
            return raw_coupang_url

        # 1. Product Search Endpoint (#1 product URL)
        search_path = "/v2/providers/affiliate_open_api/apis/openapi/products/search"
        query_params = urllib.parse.urlencode({"keyword": keyword, "limit": 1, "subId": self.sub_id})
        headers = {
            "Authorization": self._generate_hmac("GET", search_path, query_params),
            "Content-Type": "application/json;charset=UTF-8"
        }
        try:
            resp = requests.get(f"{self.domain}{search_path}?{query_params}", headers=headers, timeout=5)
            if resp.status_code == 200:
                products = resp.json().get("data", {}).get("productData", [])
                if products and products[0].get("productUrl"):
                    return products[0]["productUrl"]
        except Exception:
            pass

        # 2. Deeplink Shortener Endpoint
        deeplink_path = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
        headers = {
            "Authorization": self._generate_hmac("POST", deeplink_path),
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {"coupangUrls": [raw_coupang_url], "subId": self.sub_id}
        try:
            resp = requests.post(f"{self.domain}{deeplink_path}", headers=headers, json=payload, timeout=5)
            if resp.status_code == 200:
                data_list = resp.json().get("data", [])
                if data_list and data_list[0].get("shortenUrl"):
                    return data_list[0]["shortenUrl"]
        except Exception:
            pass

        return raw_coupang_url


def get_coupang_client() -> CoupangPartnersClient:
    """Initializes CoupangPartnersClient reading credentials from environment variables."""
    access_key = os.getenv("COUPANG_ACCESS_KEY", "").strip()
    secret_key = os.getenv("COUPANG_SECRET_KEY", "").strip()
    sub_id = os.getenv("COUPANG_SUB_ID", "blogin365").strip() or "blogin365"
    return CoupangPartnersClient(access_key=access_key, secret_key=secret_key, sub_id=sub_id)


def get_coupang_affiliate_link(keyword: str, sub_id: Optional[str] = None) -> str:
    """Convenience helper to retrieve Coupang affiliate tracking link for keyword."""
    client = get_coupang_client()
    if sub_id:
        client.sub_id = sub_id
    return client.get_affiliate_search_link(keyword)


if __name__ == "__main__":
    client = get_coupang_client()
    link = client.get_affiliate_search_link("맥북 에어 M3")
    print(f"Coupang Affiliate Link Generated: {link}")
