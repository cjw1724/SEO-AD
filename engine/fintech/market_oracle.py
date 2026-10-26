# -*- coding: utf-8 -*-
"""
engine/fintech/market_oracle.py
--------------------------------
무비용 실시간 마켓 데이터 & 환율(USD/KRW) 오라클 모듈
1. Yahoo Finance / Public Open Rate API 기반 실시간 환율 및 주요 티커 시세 조회
2. 로컬 디스크 캐싱(1시간 TTL, data/market_rates_cache.json)으로 API 호출 최소화
3. 완전 오프라인/네트워크 장애 시 SSOT 정형 DB 기준 안전 상수(1,380.0원)로 즉시 Fallback
4. 블로그 포스트 본문에 주입되는 0ms 클라이언트 사이드 비동기 환율 패처(Vanilla JS) 스니펫 생성
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE_FILE = os.path.join(BASE_DIR, "data", "market_rates_cache.json")
DEFAULT_USD_KRW_RATE = 1380.0

# 20대 핵심 자산 벤치마크 기본가 (오프라인/장애 대비 SSOT Fallback)
FALLBACK_TICKER_PRICES = {
    "NVDA": 140.0,
    "TSLA": 220.0,
    "AAPL": 230.0,
    "MSFT": 430.0,
    "PLTR": 44.0,
    "SOXL": 35.0,
    "TQQQ": 75.0,
    "IONQ": 18.0,
    "COIN": 210.0,
    "O": 54.0,
    "BTC": 68000.0,
    "ETH": 2600.0,
    "XRP": 0.55,
    "SOL": 175.0,
    "DOGE": 0.14,
    "SEI": 0.40,
}


class MarketDataOracle:
    def __init__(self, cache_file: str = CACHE_FILE, ttl_seconds: int = 3600):
        self.cache_file = cache_file
        self.ttl_seconds = ttl_seconds
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[MarketOracle] 캐시 저장 경고: {e}", file=sys.stderr)

    def get_usd_krw_rate(self) -> float:
        """
        USD/KRW 원달러 기준 환율 조회:
        1. 캐시 유효성(TTL 1시간) 확인
        2. Yahoo Finance KRW=X 조회
        3. Open ER-API 폴백
        4. 오프라인 기본값(1380.0) 반환
        """
        now = time.time()
        fx_cache = self.cache.get("USD_KRW")
        if fx_cache and (now - fx_cache.get("timestamp", 0)) < self.ttl_seconds:
            return float(fx_cache.get("rate", DEFAULT_USD_KRW_RATE))

        # 1차 시도: Yahoo Finance API
        rate = self._fetch_yahoo_fx()
        if rate and rate > 500:
            self.cache["USD_KRW"] = {
                "rate": rate,
                "timestamp": now,
                "source": "yahoo_finance",
                "updated_at": datetime.now().isoformat()
            }
            self._save_cache()
            return rate

        # 2차 시도: Open ExchangeRate API 폴백
        rate = self._fetch_open_er_fx()
        if rate and rate > 500:
            self.cache["USD_KRW"] = {
                "rate": rate,
                "timestamp": now,
                "source": "open_er_api",
                "updated_at": datetime.now().isoformat()
            }
            self._save_cache()
            return rate

        # 3차 시도: 기존 캐시값(만료되었더라도) 또는 하드코딩 기준값
        if fx_cache and "rate" in fx_cache:
            return float(fx_cache["rate"])

        return DEFAULT_USD_KRW_RATE

    def _fetch_yahoo_fx(self) -> Optional[float]:
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/KRW=X?interval=1d&range=1d"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                rate = meta.get("regularMarketPrice")
                if rate and isinstance(rate, (int, float)):
                    return round(float(rate), 2)
        except Exception:
            pass
        return None

    def _fetch_open_er_fx(self) -> Optional[float]:
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                rates = data.get("rates", {})
                krw = rates.get("KRW")
                if krw and isinstance(krw, (int, float)):
                    return round(float(krw), 2)
        except Exception:
            pass
        return None

    def get_ticker_price(self, ticker: str) -> float:
        """티커 현재가(USD 또는 KRW) 조회 (캐시 -> 야후 -> 기본값 폴백)"""
        clean_ticker = ticker.upper().strip()
        now = time.time()
        t_cache = self.cache.get(f"TICKER_{clean_ticker}")
        if t_cache and (now - t_cache.get("timestamp", 0)) < self.ttl_seconds:
            return float(t_cache.get("price", FALLBACK_TICKER_PRICES.get(clean_ticker, 100.0)))

        # 야후 파이낸스 티커 심볼 매핑
        yahoo_symbol = clean_ticker
        if clean_ticker in ["BTC", "ETH", "XRP", "SOL", "DOGE", "SEI"]:
            yahoo_symbol = f"{clean_ticker}-USD"

        price = None
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?interval=1d&range=1d"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                p = meta.get("regularMarketPrice")
                if p and isinstance(p, (int, float)):
                    price = round(float(p), 2)
        except Exception:
            pass

        if not price or price <= 0:
            price = FALLBACK_TICKER_PRICES.get(clean_ticker, 100.0)

        self.cache[f"TICKER_{clean_ticker}"] = {
            "price": price,
            "timestamp": now,
            "updated_at": datetime.now().isoformat()
        }
        self._save_cache()
        return price

    def get_client_fx_script(self, fallback_rate: float = DEFAULT_USD_KRW_RATE) -> str:
        """
        블로그 본문 위젯에 주입되는 클라이언트 사이드 실시간 환율 패처:
        - LocalStorage 캐시(1시간) 확인
        - 오픈 환율 API 비동기 fetch
        - 화면 내 환율 입력창/라벨 0ms 실시간 업데이트
        - 외부 장애 시 아무런 경고/에러 없이 fallback_rate 유지
        """
        return f"""
<script>
(function() {{
  const FALLBACK_FX = {fallback_rate};
  const CACHE_KEY = 'blogin_live_fx_usd_krw';
  const CACHE_TIME_KEY = 'blogin_live_fx_ts';
  const ONE_HOUR = 3600000;

  function applyFx(rate) {{
    if (!rate || isNaN(rate) || rate <= 500) return;
    const fxInputs = document.querySelectorAll('.blogin-fx-input');
    fxInputs.forEach(function(inp) {{
      if (!inp.getAttribute('data-user-modified')) {{
        inp.value = Math.round(rate);
        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
      }}
    }});
    const fxLabels = document.querySelectorAll('.blogin-fx-label');
    fxLabels.forEach(function(lbl) {{
      lbl.textContent = Number(rate).toLocaleString('ko-KR') + '원';
    }});
    const fxBadge = document.getElementById('blogin-live-fx-badge');
    if (fxBadge) {{
      fxBadge.textContent = '🟢 실시간 환율 ' + Number(rate).toLocaleString('ko-KR') + '원 적용';
      fxBadge.style.color = '#34d399';
    }}
  }}

  // 1. LocalStorage 캐시 확인
  try {{
    const cachedRate = parseFloat(localStorage.getItem(CACHE_KEY));
    const cachedTs = parseInt(localStorage.getItem(CACHE_TIME_KEY), 10);
    const now = Date.now();
    if (cachedRate && cachedTs && (now - cachedTs < ONE_HOUR)) {{
      applyFx(cachedRate);
      return;
    }}
  }} catch (e) {{}}

  // 2. 비동기 오픈 환율 API 페치 (CORS 지원 무비용 엔드포인트)
  fetch('https://open.er-api.com/v6/latest/USD')
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
      if (data && data.rates && data.rates.KRW) {{
        const liveRate = Math.round(data.rates.KRW * 100) / 100;
        try {{
          localStorage.setItem(CACHE_KEY, liveRate);
          localStorage.setItem(CACHE_TIME_KEY, Date.now());
        }} catch (e) {{}}
        applyFx(liveRate);
      }}
    }})
    .catch(function() {{
      applyFx(FALLBACK_FX);
    }});
}})();
</script>
"""


def get_live_usd_krw(cache_file: str = CACHE_FILE) -> float:
    return MarketDataOracle(cache_file=cache_file).get_usd_krw_rate()
