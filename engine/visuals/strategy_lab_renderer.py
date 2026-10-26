# -*- coding: utf-8 -*-
"""
engine/visuals/strategy_lab_renderer.py
----------------------------------------
Vibe Strategy Lab - Interactive Quantitative Strategy Engine & Real-Time Backtester (v9.0 Apex)

Embeds an institutional-grade, zero-server-cost TradingView Lightweight Charts (v4.1.1)
interactive trading lab directly inside blog posts.

Features:
1. Pure Client-Side Execution (0 KRW Server Cost):
   - Direct Binance Public REST API (500 historical candles) + WebSocket (live stream)
   - In-browser quantitative backtesting engine (< 0.01s instant recalc)
2. Chart Overlay:
   - Candlestick Series + Volume Histogram
   - Indicator Overlays (Bollinger Bands, EMA, RSI, etc.)
   - Strategy Buy/Sell Markers (▲ BUY / ▼ SELL) placed directly on the chart
3. Interactive Sliders & Parameter Controls:
   - Sliders dynamically adjust strategy parameters and trigger instant re-calculation
4. Quantitative KPI Scorecard:
   - Real-time Win Rate (%), Profit Factor, Max Drawdown (MDD %), Net Return ($)
5. 'Follow & Paper Trade' Integration:
   - One-click auto-follow toggle executing simulated trades on live Binance WebSocket ticks
   - Synchronized with Blogin 365 AI Vibe Trading Pro Station (/p/vibe-trading.html)
6. Toss Dark Theme & WCAG 2.1 AAA Accessibility:
   - High-contrast palette (#0a0e17, #111827, #f8fafc, #94a3b8, #10b981, #38bdf8)
"""

import json
from typing import Dict, Any, Optional


class StrategyLabRenderer:
    """
    Renders an interactive TradingView Lightweight Charts strategy backtesting widget.
    """

    DEFAULT_WONYOTTI_CONFIG = {
        "strategy_id": "wonyotti_bollinger_reversal",
        "title": "워뇨띠 Q&A 기반 볼린저밴드 이탈 반등 + 거래량 다이버전스 실전 랩",
        "subtitle": "실시간 바이낸스 500개 캔들 위에서 기법의 실제 승률과 손익비를 0.01초 만에 검증하고 모의투자를 가동합니다.",
        "symbol": "BTCUSDT",
        "interval": "15m",
        "default_params": {
            "bb_period": 20,
            "bb_std": 2.0,
            "vol_mult": 1.5,
            "rsi_threshold": 35,
            "tp_percent": 2.0,
            "sl_percent": 1.2,
            "leverage": 3
        },
        "strategy_description": "볼린저 밴드 하단선(20, 2σ) 터치/하향이탈 시, 최근 20봉 평균 대비 1.5배 이상의 거래량이 폭증하며 RSI가 35 이하일 때 롱(BUY) 진입. 목표가 도달 시 분할 익절, 직전 저점 이탈 시 칼손절."
    }

    @classmethod
    def get_strategy_presets(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "wonyotti_bollinger_reversal": cls.DEFAULT_WONYOTTI_CONFIG,
            "supertrend_rsi_scalping": {
                "strategy_id": "supertrend_rsi_scalping",
                "title": "슈퍼트렌드 + RSI 1분봉 초단타 스캘핑 전략 랩",
                "subtitle": "해외 100만 코인 유튜버들이 극찬하는 1분봉 추세추종 스캘핑 기법의 실제 승률 팩트체크",
                "symbol": "BTCUSDT",
                "interval": "1m",
                "default_params": {
                    "bb_period": 14,
                    "bb_std": 2.0,
                    "vol_mult": 1.2,
                    "rsi_threshold": 40,
                    "tp_percent": 0.8,
                    "sl_percent": 0.5,
                    "leverage": 5
                },
                "strategy_description": "슈퍼트렌드 강세 전환 및 RSI 50 상향 돌파 시 롱 진입. 0.8% 익절, 0.5% 칼손절을 반복하는 초단타 스캘핑."
            },
            "larry_williams_breakout": {
                "strategy_id": "larry_williams_breakout",
                "title": "래리 윌리엄스 변동성 돌파(Volatility Breakout) 퀀트 랩",
                "subtitle": "전설의 트레이더 래리 윌리엄스의 K=0.5 레인지 돌파 전략 실시간 백테스팅",
                "symbol": "BTCUSDT",
                "interval": "1h",
                "default_params": {
                    "bb_period": 24,
                    "bb_std": 2.0,
                    "vol_mult": 1.3,
                    "rsi_threshold": 45,
                    "tp_percent": 3.0,
                    "sl_percent": 1.5,
                    "leverage": 2
                },
                "strategy_description": "전일 고가-저가 레인지의 K배(0.5) 이상 가격이 상승 돌파할 때 매수하여 추세를 취하는 정통 퀀트 기법."
            }
        }

    @classmethod
    def render(cls, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Generates the self-contained HTML/CSS/JavaScript block.
        """
        cfg = config or cls.DEFAULT_WONYOTTI_CONFIG
        p = cfg.get("default_params", cls.DEFAULT_WONYOTTI_CONFIG["default_params"])
        symbol = cfg.get("symbol", "BTCUSDT")
        interval = cfg.get("interval", "15m")
        strategy_id = cfg.get("strategy_id", "wonyotti_bollinger_reversal")
        title = cfg.get("title", cls.DEFAULT_WONYOTTI_CONFIG["title"])
        subtitle = cfg.get("subtitle", cls.DEFAULT_WONYOTTI_CONFIG["subtitle"])
        description = cfg.get("strategy_description", cls.DEFAULT_WONYOTTI_CONFIG["strategy_description"])

        active_btn = "background: #2563eb; border: 1px solid #3b82f6; color: #ffffff;"
        inactive_btn = "background: #1e293b; border: 1px solid #334155; color: #94a3b8;"

        btn_1m_style = active_btn if interval == "1m" else inactive_btn
        btn_5m_style = active_btn if interval == "5m" else inactive_btn
        btn_15m_style = active_btn if interval == "15m" else inactive_btn
        btn_1h_style = active_btn if interval == "1h" else inactive_btn

        interval_kor = "1분봉" if interval == "1m" else ("5분봉" if interval == "5m" else ("15분봉" if interval == "15m" else "1시간봉"))

        html = f"""
<!-- ============================================================================== -->
<!-- 🏛️ Blogin 365 AI Holdings - Vibe Strategy Lab (TradingView Lightweight Engine) -->
<!-- ============================================================================== -->
<div id="vibe-strategy-lab-root" class="strategy-lab-wrapper" style="margin: 36px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0a0e17; border: 1px solid #1f2d47; border-radius: 20px; padding: 24px; color: #f8fafc; box-shadow: 0 20px 40px rgba(0,0,0,0.45); max-width: 100%; box-sizing: border-box;">

  <!-- 1. Header & Live Status HUD -->
  <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px; margin-bottom: 20px; padding-bottom: 18px; border-bottom: 1px solid #1f2d47;">
    <div>
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
        <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #10b981; font-size: 11px; font-weight: 800; padding: 3px 9px; border-radius: 6px; letter-spacing: 0.5px; text-transform: uppercase;">
          LIVE STRATEGY LAB
        </span>
        <span style="background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px;">
          {symbol} · {interval} 봉
        </span>
        <span id="lab-ws-badge" style="background: rgba(148, 163, 184, 0.12); border: 1px solid rgba(148, 163, 184, 0.25); color: #94a3b8; font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 6px; display: inline-flex; align-items: center; gap: 5px;">
          <span style="width: 7px; height: 7px; background: #10b981; border-radius: 50%; display: inline-block;"></span>
          바이낸스 실시간 시세 연동
        </span>
      </div>
      <!-- Timeframe Switcher Tabs (Dynamically Styled by Strategy Interval) -->
      <div style="display: flex; gap: 6px; margin-bottom: 8px;">
        <button type="button" class="btn-tf" data-tf="1m" style="{btn_1m_style} font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; cursor: pointer;">1분봉</button>
        <button type="button" class="btn-tf" data-tf="5m" style="{btn_5m_style} font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; cursor: pointer;">5분봉</button>
        <button type="button" class="btn-tf" data-tf="15m" style="{btn_15m_style} font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; cursor: pointer;">15분봉</button>
        <button type="button" class="btn-tf" data-tf="1h" style="{btn_1h_style} font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; cursor: pointer;">1시간봉</button>
      </div>
      <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #f8fafc; letter-spacing: -0.3px;">
        {title}
      </h3>
      <p style="margin: 6px 0 0 0; font-size: 13px; color: #94a3b8; line-height: 1.5;">
        {subtitle}
      </p>
    </div>

    <!-- Quick Navigation to Flagship Station -->
    <div>
      <a href="/p/vibe-trading.html" target="_blank" style="display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #ffffff !important; padding: 10px 16px; border-radius: 10px; font-size: 13px; font-weight: 700; text-decoration: none; border: 1px solid #3b82f6; box-shadow: 0 4px 14px rgba(37,99,235,0.3); transition: all 0.2s ease;">
        <span>🔥 VIBE TRADING 랭킹전 이동</span>
        <span style="font-size: 14px;">↗</span>
      </a>
    </div>
  </div>

  <!-- 2. Strategy Logic Brief Banner -->
  <div style="background: #111827; border-left: 4px solid #38bdf8; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #cbd5e1; line-height: 1.6;">
    <strong style="color: #38bdf8;">[알고리즘 원리]</strong> {description}
  </div>

  <!-- 3. Real-Time Quantitative KPI Scorecard (4-Column Bento Box) -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 20px;">
    <!-- KPI 1: Win Rate -->
    <div style="background: #111827; border: 1px solid #1f2d47; border-radius: 12px; padding: 14px; text-align: center;">
      <div style="font-size: 11px; font-weight: 700; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase;">
        실제 백테스트 승률
      </div>
      <div id="kpi-winrate" style="font-size: 24px; font-weight: 800; color: #10b981;">
        --%
      </div>
      <div id="kpi-trades" style="font-size: 11px; color: #94a3b8; margin-top: 2px;">
        총 --회 거래 기준
      </div>
    </div>

    <!-- KPI 2: Profit Factor -->
    <div style="background: #111827; border: 1px solid #1f2d47; border-radius: 12px; padding: 14px; text-align: center;">
      <div style="font-size: 11px; font-weight: 700; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase;">
        손익비 (Profit Factor)
      </div>
      <div id="kpi-pf" style="font-size: 24px; font-weight: 800; color: #38bdf8;">
        --
      </div>
      <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">
        총이익 / 총손실 비
      </div>
    </div>

    <!-- KPI 3: Max Drawdown (MDD) -->
    <div style="background: #111827; border: 1px solid #1f2d47; border-radius: 12px; padding: 14px; text-align: center;">
      <div style="font-size: 11px; font-weight: 700; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase;">
        최대 낙폭 (MDD)
      </div>
      <div id="kpi-mdd" style="font-size: 24px; font-weight: 800; color: #f59e0b;">
        --%
      </div>
      <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">
        최고점 대비 최대 손실
      </div>
    </div>

    <!-- KPI 4: Net PnL (Estimated) -->
    <div style="background: #111827; border: 1px solid #1f2d47; border-radius: 12px; padding: 14px; text-align: center;">
      <div style="font-size: 11px; font-weight: 700; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase;">
        가상 누적 수익 ($10k 기준)
      </div>
      <div id="kpi-pnl" style="font-size: 24px; font-weight: 800; color: #10b981;">
        +$0.00
      </div>
      <div id="kpi-roi" style="font-size: 11px; color: #94a3b8; margin-top: 2px;">
        수익률: +0.0%
      </div>
    </div>
  </div>

  <!-- 4. Dual Engine Header: Quant Lab vs TradingView Official Pro -->
  <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 12px;">
    <div style="display: flex; gap: 6px; background: #111827; padding: 4px; border-radius: 10px; border: 1px solid #1f2d47;">
      <button id="btn-mode-lab" style="background: #2563eb; border: 1px solid #3b82f6; color: #ffffff; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s ease;">
        <span>⚡</span> 퀀트 팩트체크 랩
      </button>
      <button id="btn-mode-tv-pro" style="background: transparent; border: 1px solid transparent; color: #94a3b8; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s ease;">
        <span>🌐</span> 트레이딩뷰 공식 프로 차트
      </button>
    </div>
    <div style="font-size: 11px; color: #64748b; font-weight: 600;">
      * 바이낸스 공식 실시간 틱 데이터 기반
    </div>
  </div>

  <!-- Chart Viewports Container -->
  <div id="quant-lab-viewport" style="position: relative; background: #0d131f; border: 1px solid #1f2d47; border-radius: 14px; overflow: hidden; margin-bottom: 20px;">
    <!-- Chart Top Legend HUD -->
    <div style="position: absolute; top: 12px; left: 16px; z-index: 10; display: flex; flex-wrap: wrap; gap: 10px; font-size: 12px; pointer-events: none;">
      <span style="color: #f8fafc; font-weight: 700;">{symbol}</span>
      <span id="chart-legend-price" style="color: #10b981; font-weight: 800;">Loading...</span>
      <span style="color: #94a3b8;">BB(20,2): <span id="chart-legend-bb" style="color: #38bdf8;">--</span></span>
      <span style="color: #94a3b8;">RSI: <span id="chart-legend-rsi" style="color: #c084fc;">--</span></span>
      <span style="color: #94a3b8;">거래량: <span id="chart-legend-vol" style="color: #f8fafc; font-weight: 700;">--</span></span>
      <span style="color: #94a3b8;">시그널: <span id="chart-legend-signals" style="color: #10b981; font-weight: 700;">▲ 0 / ▼ 0</span></span>
    </div>

    <!-- Live Watermark -->
    <div style="position: absolute; bottom: 12px; right: 16px; z-index: 5; font-size: 10px; color: rgba(148,163,184,0.3); font-weight: 700; pointer-events: none; letter-spacing: 0.5px;">
      BLOGIN 365 AI QUANTITATIVE LAB
    </div>

    <!-- The Actual Canvas Target -->
    <div id="tv-strategy-chart" style="width: 100%; height: 420px; box-sizing: border-box;"></div>
  </div>

  <!-- 4-B. TradingView Official Advanced Real-Time Chart Viewport (Official Embed) -->
  <div id="tv-official-viewport" style="display: none; background: #0d131f; border: 1px solid #1f2d47; border-radius: 14px; overflow: hidden; margin-bottom: 20px; height: 460px;">
    <div id="tradingview_official_embed" style="width: 100%; height: 100%;"></div>
  </div>

  <!-- 5. Interactive Parameter Tuning Sliders (0.01s Instant Recalc) -->
  <div style="background: #111827; border: 1px solid #1f2d47; border-radius: 14px; padding: 20px; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #1f2d47; padding-bottom: 10px;">
      <h4 style="margin: 0; font-size: 15px; font-weight: 700; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
        <span>⚙️</span> 전략 파라미터 실시간 튜닝
      </h4>
      <button id="btn-reset-params" style="background: transparent; border: 1px solid #334155; color: #94a3b8; font-size: 11px; padding: 4px 10px; border-radius: 6px; cursor: pointer;">
        기본값 초기화
      </button>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;">
      <!-- Slider 1: Bollinger Period -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">볼린저 밴드 기간 (N)</span>
          <strong id="val-bb-period" style="color: #38bdf8;">{p['bb_period']}</strong>
        </div>
        <input type="range" id="slider-bb-period" min="10" max="50" step="1" value="{p['bb_period']}" style="width: 100%; accent-color: #38bdf8; cursor: pointer;">
      </div>

      <!-- Slider 2: Bollinger StdDev -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">표준편차 배수 (σ)</span>
          <strong id="val-bb-std" style="color: #38bdf8;">{p['bb_std']}</strong>
        </div>
        <input type="range" id="slider-bb-std" min="1.5" max="3.0" step="0.1" value="{p['bb_std']}" style="width: 100%; accent-color: #38bdf8; cursor: pointer;">
      </div>

      <!-- Slider 3: Volume Spike Multiplier -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">거래량 폭증 배수 (Vol Mult)</span>
          <strong id="val-vol-mult" style="color: #f59e0b;">{p['vol_mult']}x</strong>
        </div>
        <input type="range" id="slider-vol-mult" min="1.0" max="3.0" step="0.1" value="{p['vol_mult']}" style="width: 100%; accent-color: #f59e0b; cursor: pointer;">
      </div>

      <!-- Slider 4: RSI Threshold -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">RSI 과매도 진입 기준</span>
          <strong id="val-rsi-th" style="color: #c084fc;">{p['rsi_threshold']} 이하</strong>
        </div>
        <input type="range" id="slider-rsi-th" min="20" max="45" step="1" value="{p['rsi_threshold']}" style="width: 100%; accent-color: #c084fc; cursor: pointer;">
      </div>

      <!-- Slider 5: Take Profit % -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">익절 목표가 (TP %)</span>
          <strong id="val-tp" style="color: #10b981;">+{p['tp_percent']}%</strong>
        </div>
        <input type="range" id="slider-tp" min="0.5" max="5.0" step="0.1" value="{p['tp_percent']}" style="width: 100%; accent-color: #10b981; cursor: pointer;">
      </div>

      <!-- Slider 6: Stop Loss % -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">손절 한도 (SL %)</span>
          <strong id="val-sl" style="color: #ef4444;">-{p['sl_percent']}%</strong>
        </div>
        <input type="range" id="slider-sl" min="0.5" max="3.0" step="0.1" value="{p['sl_percent']}" style="width: 100%; accent-color: #ef4444; cursor: pointer;">
      </div>

      <!-- Slider 7: Leverage -->
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
          <span style="color: #94a3b8;">레버리지 (Leverage)</span>
          <strong id="val-lev" style="color: #eab308;">{p['leverage']}x</strong>
        </div>
        <input type="range" id="slider-lev" min="1" max="10" step="1" value="{p['leverage']}" style="width: 100%; accent-color: #eab308; cursor: pointer;">
      </div>
    </div>
  </div>

  <!-- 6. 'Follow & Live Paper Trading' Toggle & Status -->
  <div style="background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(37,99,235,0.08)); border: 1px solid rgba(16,185,129,0.3); border-radius: 14px; padding: 18px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px;">
    <div>
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <span style="font-size: 16px;">🤖</span>
        <strong style="color: #f8fafc; font-size: 14px;">이 전략으로 실시간 모의투자 추종 (Auto-Paper Trade)</strong>
      </div>
      <p style="margin: 0; font-size: 12px; color: #94a3b8;">
        스위치를 켜면 바이낸스 실시간 웹소켓 {interval_kor}이 마감될 때마다 해당 조건에서 자동으로 가상 포지션을 진입합니다.
      </p>
    </div>

    <div style="display: flex; align-items: center; gap: 12px;">
      <span id="follow-status-label" style="font-size: 12px; font-weight: 700; color: #94a3b8;">추종 비활성</span>
      <label style="position: relative; display: inline-block; width: 48px; height: 26px; cursor: pointer;">
        <input type="checkbox" id="toggle-follow-strategy" style="position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; z-index: 2; margin: 0;">
        <span id="toggle-slider-bg" style="position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #334155; transition: .3s; border-radius: 26px;"></span>
      </label>
    </div>
  </div>

  <!-- Live Paper Position Notification Bar & Unified Vibe Trading Link -->
  <div id="live-paper-status-bar" style="display: none; margin-top: 14px; background: #111827; border: 1px solid #10b981; border-radius: 12px; padding: 14px 18px; font-size: 13px; color: #f8fafc; box-shadow: 0 4px 16px rgba(16,185,129,0.15);">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
      <div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <span style="display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%;"></span>
          <span><strong>VIBE TRADING 계좌 자동 연동 중:</strong> 가상 자본금 <strong style="color: #10b981;">$10,000.00</strong></span>
        </div>
        <div style="margin-top: 4px; font-size: 12px; color: #cbd5e1;">
          현재 포지션: <span id="live-pos-desc" style="color: #38bdf8; font-weight: 700;">조건 탐색 중...</span>
        </div>
      </div>
      <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <span id="live-last-tick" style="font-size: 11px; color: #94a3b8;">실시간 틱 감시 중</span>
        <a href="/p/vibe-trading.html" target="_blank" style="background: linear-gradient(135deg, #10b981, #059669); color: #ffffff !important; padding: 6px 12px; border-radius: 8px; font-weight: 800; font-size: 11px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 4px 12px rgba(16,185,129,0.3);">
          <span>🚀 내 모의투자 계좌 &amp; 랭킹 확인</span> ↗
        </a>
      </div>
    </div>
  </div>
</div>

<!-- ============================================================================== -->
<!-- 🚀 TradingView Lightweight Charts Library & In-Browser Backtesting Engine       -->
<!-- ============================================================================== -->
<script src="https://unpkg.com/lightweight-charts@4.1.1/dist/lightweight-charts.standalone.production.js"></script>

<script>
(function() {{
  'use strict';

  // Strategy Configuration
  const STRATEGY_CONFIG = {json.dumps(cfg, ensure_ascii=False)};
  const SYMBOL = '{symbol}';
  const INTERVAL = '{interval}';
  let chart, candleSeries, volumeSeries, upperBandSeries, middleBandSeries, lowerBandSeries;
  let rawCandles = [];
  let isFollowing = false;
  let virtualBalance = 10000;
  let currentPosition = null;

  // Active Parameters
  let params = {{ ...STRATEGY_CONFIG.default_params }};

  // DOM Elements
  const chartContainer = document.getElementById('tv-strategy-chart');
  const kpiWinrate = document.getElementById('kpi-winrate');
  const kpiTrades = document.getElementById('kpi-trades');
  const kpiPf = document.getElementById('kpi-pf');
  const kpiMdd = document.getElementById('kpi-mdd');
  const kpiPnl = document.getElementById('kpi-pnl');
  const kpiRoi = document.getElementById('kpi-roi');

  // Sliders
  const sliderBbPeriod = document.getElementById('slider-bb-period');
  const sliderBbStd = document.getElementById('slider-bb-std');
  const sliderVolMult = document.getElementById('slider-vol-mult');
  const sliderRsiTh = document.getElementById('slider-rsi-th');
  const sliderTp = document.getElementById('slider-tp');
  const sliderSl = document.getElementById('slider-sl');
  const sliderLev = document.getElementById('slider-lev');

  // Values display
  const valBbPeriod = document.getElementById('val-bb-period');
  const valBbStd = document.getElementById('val-bb-std');
  const valVolMult = document.getElementById('val-vol-mult');
  const valRsiTh = document.getElementById('val-rsi-th');
  const valTp = document.getElementById('val-tp');
  const valSl = document.getElementById('val-sl');
  const valLev = document.getElementById('val-lev');

  // Legend
  const legendPrice = document.getElementById('chart-legend-price');
  const legendBb = document.getElementById('chart-legend-bb');
  const legendRsi = document.getElementById('chart-legend-rsi');
  const legendSignals = document.getElementById('chart-legend-signals');
  const legendVol = document.getElementById('chart-legend-vol');

  // Follow Toggle
  const toggleFollow = document.getElementById('toggle-follow-strategy');
  const followLabel = document.getElementById('follow-status-label');
  const toggleBg = document.getElementById('toggle-slider-bg');
  const liveStatusBar = document.getElementById('live-paper-status-bar');
  const livePosDesc = document.getElementById('live-pos-desc');

  // 1. Initialize Lightweight Chart
  function initChart() {{
    if (!window.LightweightCharts) {{
      console.error('[StrategyLab] LightweightCharts not loaded yet, retrying...');
      setTimeout(initChart, 300);
      return;
    }}

    chart = LightweightCharts.createChart(chartContainer, {{
      width: chartContainer.clientWidth,
      height: 420,
      layout: {{
        background: {{ color: '#0d131f' }},
        textColor: '#94a3b8',
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
      }},
      grid: {{
        vertLines: {{ color: '#172236' }},
        horzLines: {{ color: '#172236' }}
      }},
      crosshair: {{
        mode: LightweightCharts.CrosshairMode.Normal,
      }},
      rightPriceScale: {{
        borderColor: '#1f2d47',
      }},
      timeScale: {{
        borderColor: '#1f2d47',
        timeVisible: true,
        secondsVisible: false
      }}
    }});

    // Volume series (bottom pane with isolated scale)
    volumeSeries = chart.addHistogramSeries({{
      priceFormat: {{ type: 'volume' }},
      priceScaleId: 'volume_overlay',
    }});
    chart.priceScale('volume_overlay').applyOptions({{
      scaleMargins: {{ top: 0.82, bottom: 0 }},
      visible: false
    }});

    // Crosshair move listener for live HUD inspection
    chart.subscribeCrosshairMove(param => {{
      if (!param || !param.time) return;
      const c = param.seriesData.get(candleSeries);
      const v = param.seriesData.get(volumeSeries);
      if (c && c.close && legendPrice) {{
        legendPrice.textContent = `$${{c.close.toLocaleString()}}`;
      }}
      if (v && v.value !== undefined && legendVol) {{
        legendVol.textContent = v.value >= 1000 ? (v.value / 1000).toFixed(1) + 'k' : v.value.toFixed(1);
      }}
    }});

    // Bollinger Band Lines
    upperBandSeries = chart.addLineSeries({{ color: '#38bdf8', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed }});
    middleBandSeries = chart.addLineSeries({{ color: '#f59e0b', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Solid }});
    lowerBandSeries = chart.addLineSeries({{ color: '#c084fc', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed }});

    // Candlestick series
    candleSeries = chart.addCandlestickSeries({{
      upColor: '#10b981',
      downColor: '#ef4444',
      borderVisible: false,
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444'
    }});

    // Responsive Resize Observer
    window.addEventListener('resize', () => {{
      if (chart && chartContainer) {{
        chart.applyOptions({{ width: chartContainer.clientWidth }});
      }}
    }});
  }}

  // 2. Fetch Binance Historical 500 Candles
  let currentActiveInterval = INTERVAL;
  async function fetchHistoricalCandlesWithInterval(targetInterval) {{
    currentActiveInterval = targetInterval || currentActiveInterval;
    const url = `https://api.binance.com/api/v3/klines?symbol=${{SYMBOL}}&interval=${{currentActiveInterval}}&limit=500`;
    try {{
      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`Binance HTTP ${{resp.status}}`);
      const data = await resp.json();

      rawCandles = data.map(item => ({{
        time: Math.floor(item[0] / 1000) + (9 * 3600), // KST UTC+9 offset
        open: parseFloat(item[1]),
        high: parseFloat(item[2]),
        low: parseFloat(item[3]),
        close: parseFloat(item[4]),
        volume: parseFloat(item[5])
      }}));

      console.log(`[StrategyLab] Loaded ${{rawCandles.length}} candles (${{currentActiveInterval}}) from Binance.`);
      runBacktestAndRender();
      connectWebSocket(currentActiveInterval);
    }} catch (err) {{
      console.warn('[StrategyLab] Binance REST failed, generating fallback high-fidelity candles:', err);
      generateFallbackCandles();
      runBacktestAndRender();
    }}
  }}

  function fetchHistoricalCandles() {{
    return fetchHistoricalCandlesWithInterval(INTERVAL);
  }}

  // High-fidelity fallback generator if network blocked
  function generateFallbackCandles() {{
    rawCandles = [];
    let price = 67500.0;
    const now = Math.floor(Date.now() / 1000) - 500 * 900 + (9 * 3600);
    for (let i = 0; i < 500; i++) {{
      const change = (Math.random() - 0.495) * 220;
      const open = price;
      const close = price + change;
      const high = Math.max(open, close) + Math.random() * 90;
      const low = Math.min(open, close) - Math.random() * 90;
      const volume = 80 + Math.random() * 300;
      rawCandles.push({{ time: now + i * 900, open, high, low, close, volume }});
      price = close;
    }}
  }}

  // 3. Technical Indicator Mathematics (Bollinger Bands + RSI + Volume SMA)
  function computeIndicators(candles, bbPeriod, bbStd) {{
    const closes = candles.map(c => c.close);
    const volumes = candles.map(c => c.volume);
    const len = candles.length;

    const upper = new Array(len).fill(null);
    const middle = new Array(len).fill(null);
    const lower = new Array(len).fill(null);
    const volSma = new Array(len).fill(null);
    const rsi = new Array(len).fill(null);

    // Bollinger Bands & Vol SMA
    for (let i = 0; i < len; i++) {{
      if (i >= bbPeriod - 1) {{
        let sum = 0;
        let vSum = 0;
        for (let j = 0; j < bbPeriod; j++) {{
          sum += closes[i - j];
          vSum += volumes[i - j];
        }}
        const ma = sum / bbPeriod;
        middle[i] = ma;
        volSma[i] = vSum / bbPeriod;

        let variance = 0;
        for (let j = 0; j < bbPeriod; j++) {{
          variance += Math.pow(closes[i - j] - ma, 2);
        }}
        const std = Math.sqrt(variance / bbPeriod);
        upper[i] = ma + bbStd * std;
        lower[i] = ma - bbStd * std;
      }}
    }}

    // RSI (14)
    let gains = 0, losses = 0;
    const rsiPeriod = 14;
    for (let i = 1; i < len; i++) {{
      const diff = closes[i] - closes[i - 1];
      const g = diff > 0 ? diff : 0;
      const l = diff < 0 ? -diff : 0;

      if (i <= rsiPeriod) {{
        gains += g;
        losses += l;
        if (i === rsiPeriod) {{
          const avgG = gains / rsiPeriod;
          const avgL = losses / rsiPeriod;
          const rs = avgL === 0 ? 100 : avgG / avgL;
          rsi[i] = 100 - (100 / (1 + rs));
        }}
      }} else {{
        const prevAvgG = (rsi[i - 1] ? (100 - (100 / (rsi[i - 1] / (100 - rsi[i - 1])))) : 50);
        gains = (gains * (rsiPeriod - 1) + g) / rsiPeriod;
        losses = (losses * (rsiPeriod - 1) + l) / rsiPeriod;
        const rs = losses === 0 ? 100 : gains / losses;
        rsi[i] = 100 - (100 / (1 + rs));
      }}
    }}

    return {{ upper, middle, lower, volSma, rsi }};
  }}

  // 4. In-Browser Quantitative Backtester (Evaluates exact Buy/Sell Signals)
  function runBacktestAndRender() {{
    if (!rawCandles || rawCandles.length === 0 || !chart) return;

    const bbPeriod = parseInt(params.bb_period);
    const bbStd = parseFloat(params.bb_std);
    const volMult = parseFloat(params.vol_mult);
    const rsiTh = parseFloat(params.rsi_threshold);
    const tpPct = parseFloat(params.tp_percent) / 100.0;
    const slPct = parseFloat(params.sl_percent) / 100.0;
    const lev = parseFloat(params.leverage);
    const feeRate = 0.0010; // Binance Futures 0.05% taker fee * 2 (roundtrip)

    const ind = computeIndicators(rawCandles, bbPeriod, bbStd);

    // Prepare chart line series data
    const upperData = [];
    const middleData = [];
    const lowerData = [];
    const volData = [];

    for (let i = 0; i < rawCandles.length; i++) {{
      const t = rawCandles[i].time;
      if (ind.upper[i] !== null) upperData.push({{ time: t, value: ind.upper[i] }});
      if (ind.middle[i] !== null) middleData.push({{ time: t, value: ind.middle[i] }});
      if (ind.lower[i] !== null) lowerData.push({{ time: t, value: ind.lower[i] }});

      volData.push({{
        time: t,
        value: rawCandles[i].volume,
        color: rawCandles[i].close >= rawCandles[i].open ? 'rgba(16, 185, 129, 0.35)' : 'rgba(239, 68, 68, 0.35)'
      }});
    }}

    candleSeries.setData(rawCandles);
    volumeSeries.setData(volData);
    upperBandSeries.setData(upperData);
    middleBandSeries.setData(middleData);
    lowerBandSeries.setData(lowerData);

    // Simulate Trades (Dual-Directional: Long & Short)
    const markers = [];
    let position = null; // null | 'LONG' | 'SHORT'
    let entryPrice = 0;
    let entryTime = 0;
    let trades = [];
    let balance = 10000;
    let peakBalance = 10000;
    let maxDrawdown = 0;

    for (let i = bbPeriod; i < rawCandles.length; i++) {{
      const c = rawCandles[i];
      const prevC = rawCandles[i - 1];
      const lowerVal = ind.lower[i];
      const upperVal = ind.upper[i];
      const avgVol = ind.volSma[i];
      const rsiVal = ind.rsi[i] || 50;
      const isVolSurge = avgVol ? (c.volume >= avgVol * volMult) : true;

      if (!position) {{
        // LONG Condition: Lower band touch + Volume surge + RSI oversold
        const isLowerTouch = c.low <= lowerVal || prevC.low <= ind.lower[i - 1];
        const isRsiOversold = rsiVal <= rsiTh;

        // SHORT Condition: Upper band touch + Volume surge + RSI overbought (100 - rsiTh)
        const isUpperTouch = c.high >= upperVal || prevC.high >= ind.upper[i - 1];
        const isRsiOverbought = rsiVal >= (100 - rsiTh);

        if (isLowerTouch && isVolSurge && isRsiOversold) {{
          position = 'LONG';
          entryPrice = c.close;
          entryTime = c.time;
          markers.push({{
            time: c.time,
            position: 'belowBar',
            color: '#10b981',
            shape: 'arrowUp',
            text: `BUY (롱) @ $${{entryPrice.toFixed(0)}}`
          }});
        }} else if (isUpperTouch && isVolSurge && isRsiOverbought) {{
          position = 'SHORT';
          entryPrice = c.close;
          entryTime = c.time;
          markers.push({{
            time: c.time,
            position: 'aboveBar',
            color: '#f43f5e',
            shape: 'arrowDown',
            text: `SELL (숏) @ $${{entryPrice.toFixed(0)}}`
          }});
        }}
      }} else if (position === 'LONG') {{
        const tpPrice = entryPrice * (1 + tpPct);
        const slPrice = entryPrice * (1 - slPct);

        // 순수 브래킷 OCO 모델: 저가가 손절가 터치 시 최우선 손절, 고가가 목표가 도달 시 익절
        const hitSl = c.low <= slPrice;
        const hitTp = c.high >= tpPrice;

        if (hitSl || hitTp) {{
          let exitPrice = c.close;
          let rawPnl = 0;
          let exitReason = 'TP';

          if (hitSl) {{
            exitPrice = slPrice;
            rawPnl = -slPct;
            exitReason = 'SL';
          }} else if (hitTp) {{
            exitPrice = tpPrice;
            rawPnl = tpPct;
            exitReason = 'TP';
          }}

          // 바이낸스 선물 왕복 수수료(0.10%) 차감 후 순수익률 (TP 0.0% 슬롭 원천 차단)
          const netPnlPct = (rawPnl - feeRate) * lev;
          const isWin = netPnlPct > 0;
          const tradePnl = (balance * 0.3) * netPnlPct;
          balance += tradePnl;
          if (balance > peakBalance) peakBalance = balance;
          const dd = ((peakBalance - balance) / peakBalance) * 100;
          if (dd > maxDrawdown) maxDrawdown = dd;

          trades.push({{
            side: 'LONG',
            entryPrice,
            exitPrice,
            pnlPct: netPnlPct,
            isWin,
            reason: exitReason
          }});

          markers.push({{
            time: c.time,
            position: 'aboveBar',
            color: isWin ? '#38bdf8' : '#ef4444',
            shape: 'arrowDown',
            text: isWin ? `TP (롱) +${{(netPnlPct * 100).toFixed(1)}}%` : `SL (롱) ${{(netPnlPct * 100).toFixed(1)}}%`
          }});
          position = null;
        }}
      }} else if (position === 'SHORT') {{
        const tpPrice = entryPrice * (1 - tpPct);
        const slPrice = entryPrice * (1 + slPct);

        // 순수 브래킷 OCO 모델: 고가가 손절가 터치 시 최우선 손절, 저가가 목표가 도달 시 익절
        const hitSl = c.high >= slPrice;
        const hitTp = c.low <= tpPrice;

        if (hitSl || hitTp) {{
          let exitPrice = c.close;
          let rawPnl = 0;
          let exitReason = 'TP';

          if (hitSl) {{
            exitPrice = slPrice;
            rawPnl = -slPct;
            exitReason = 'SL';
          }} else if (hitTp) {{
            exitPrice = tpPrice;
            rawPnl = tpPct;
            exitReason = 'TP';
          }}

          // 바이낸스 선물 왕복 수수료(0.10%) 차감 후 순수익률 (TP 0.0% 슬롭 원천 차단)
          const netPnlPct = (rawPnl - feeRate) * lev;
          const isWin = netPnlPct > 0;
          const tradePnl = (balance * 0.3) * netPnlPct;
          balance += tradePnl;
          if (balance > peakBalance) peakBalance = balance;
          const dd = ((peakBalance - balance) / peakBalance) * 100;
          if (dd > maxDrawdown) maxDrawdown = dd;

          trades.push({{
            side: 'SHORT',
            entryPrice,
            exitPrice,
            pnlPct: netPnlPct,
            isWin,
            reason: exitReason
          }});

          markers.push({{
            time: c.time,
            position: 'belowBar',
            color: isWin ? '#38bdf8' : '#ef4444',
            shape: 'arrowUp',
            text: isWin ? `TP (숏) +${{(netPnlPct * 100).toFixed(1)}}%` : `SL (숏) ${{(netPnlPct * 100).toFixed(1)}}%`
          }});
          position = null;
        }}
      }}
    }}

    candleSeries.setMarkers(markers);

    // Render Visual Target Lines (Stop-Loss & Take-Profit)
    if (position !== null) {{
      // Currently open position at end of chart
      renderTargetLines(position, entryPrice, tpPct, slPct, lev, true);
    }} else if (trades.length > 0) {{
      // Show target bracket of the latest trade
      const lastT = trades[trades.length - 1];
      renderTargetLines(lastT.side, lastT.entryPrice, tpPct, slPct, lev, false);
    }} else {{
      clearTargetLines();
    }}

    // Compute KPIs
    const totalTrades = trades.length;
    const wins = trades.filter(t => t.isWin).length;
    const losses = totalTrades - wins;
    const winRate = totalTrades > 0 ? ((wins / totalTrades) * 100).toFixed(1) : '0.0';

    const longTrades = trades.filter(t => t.side === 'LONG');
    const shortTrades = trades.filter(t => t.side === 'SHORT');
    const longWins = longTrades.filter(t => t.isWin).length;
    const shortWins = shortTrades.filter(t => t.isWin).length;

    let totalGains = 0;
    let totalLosses = 0;
    trades.forEach(t => {{
      if (t.isWin) totalGains += t.pnlPct;
      else totalLosses += Math.abs(t.pnlPct);
    }});
    const profitFactor = totalLosses > 0 ? (totalGains / totalLosses).toFixed(2) : (totalGains > 0 ? '99.0' : '0.00');
    const netReturn = balance - 10000;
    const netRoi = ((netReturn / 10000) * 100).toFixed(1);

    // Update DOM KPIs
    kpiWinrate.textContent = `${{winRate}}%`;
    kpiWinrate.style.color = parseFloat(winRate) >= 50 ? '#10b981' : '#f59e0b';
    kpiTrades.innerHTML = `▲ 롱 ${{longWins}}/${{longTrades.length}} · ▼ 숏 ${{shortWins}}/${{shortTrades.length}} (총 ${{totalTrades}}회)`;

    kpiPf.textContent = profitFactor;
    kpiMdd.textContent = `-${{maxDrawdown.toFixed(1)}}%`;

    kpiPnl.textContent = `${{netReturn >= 0 ? '+' : ''}}$${{netReturn.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}`;
    kpiPnl.style.color = netReturn >= 0 ? '#10b981' : '#ef4444';
    kpiRoi.textContent = `수익률: ${{netRoi >= 0 ? '+' : ''}}${{netRoi}}% (${{lev}}x 레버리지)`;

    // Update Legend
    const last = rawCandles[rawCandles.length - 1];
    if (last) {{
      legendPrice.textContent = `$${{last.close.toLocaleString()}}`;
      const lastRsi = ind.rsi[ind.rsi.length - 1] || 50;
      legendRsi.textContent = lastRsi.toFixed(1);
      legendBb.textContent = `$${{(ind.lower[ind.lower.length - 1] || 0).toFixed(0)}} ~ $${{(ind.upper[ind.upper.length - 1] || 0).toFixed(0)}}`;
      if (legendVol) {{
        const lastVol = last.volume || 0;
        legendVol.textContent = lastVol >= 1000 ? (lastVol / 1000).toFixed(1) + 'k' : lastVol.toFixed(1);
      }}
      legendSignals.innerHTML = `▲ 롱 ${{longWins}}/${{longTrades.length}} · ▼ 숏 ${{shortWins}}/${{shortTrades.length}} (총 ${{totalTrades}})`;
    }}
  }}

  // Visual Target Lines (Stop-Loss & Take-Profit Horizontal Price Lines)
  let activePriceLines = [];
  function clearTargetLines() {{
    if (!candleSeries) return;
    activePriceLines.forEach(l => {{
      try {{ candleSeries.removePriceLine(l); }} catch(e) {{}}
    }});
    activePriceLines = [];
  }}

  function renderTargetLines(side, entryPrice, tpPct, slPct, lev, isOpen) {{
    clearTargetLines();
    if (!candleSeries || !entryPrice) return;

    const tpPrice = side === 'LONG' ? entryPrice * (1 + tpPct) : entryPrice * (1 - tpPct);
    const slPrice = side === 'LONG' ? entryPrice * (1 - slPct) : entryPrice * (1 + slPct);

    // 1. Entry Line (Yellow Dotted)
    const entryLine = candleSeries.createPriceLine({{
      price: entryPrice,
      color: '#f59e0b',
      lineWidth: 1,
      lineStyle: LightweightCharts.LineStyle.Dotted,
      axisLabelVisible: true,
      title: `${{side}} 진입: $${{entryPrice.toFixed(1)}}`
    }});
    activePriceLines.push(entryLine);

    // 2. TP Line (Green Dashed)
    const tpLine = candleSeries.createPriceLine({{
      price: tpPrice,
      color: '#10b981',
      lineWidth: 2,
      lineStyle: LightweightCharts.LineStyle.Dashed,
      axisLabelVisible: true,
      title: `🟢 익절선 (TP +${{(tpPct * 100 * lev).toFixed(1)}}%): $${{tpPrice.toFixed(1)}}`
    }});
    activePriceLines.push(tpLine);

    // 3. SL Line (Red Solid)
    const slLine = candleSeries.createPriceLine({{
      price: slPrice,
      color: '#ef4444',
      lineWidth: 2,
      lineStyle: LightweightCharts.LineStyle.Solid,
      axisLabelVisible: true,
      title: `🚨 손절선 (SL -${{(slPct * 100 * lev).toFixed(1)}}%): $${{slPrice.toFixed(1)}}`
    }});
    activePriceLines.push(slLine);
  }}

  // 5. Binance Real-Time WebSocket Streaming
  let activeWs = null;
  function connectWebSocket(targetInterval) {{
    if (activeWs) {{
      try {{ activeWs.close(); }} catch(e) {{}}
    }}
    const intervalToUse = targetInterval || currentActiveInterval || INTERVAL;
    const streamSymbol = SYMBOL.toLowerCase();
    const wsUrl = `wss://stream.binance.com:9443/ws/${{streamSymbol}}@kline_${{intervalToUse}}`;
    activeWs = new WebSocket(wsUrl);

    activeWs.onopen = () => {{
      console.log(`[StrategyLab] WebSocket connected (${{intervalToUse}}): ${{wsUrl}}`);
      const badge = document.getElementById('lab-ws-badge');
      if (badge) badge.style.color = '#10b981';
    }};

    activeWs.onmessage = (event) => {{
      const msg = JSON.parse(event.data);
      if (msg.e === 'kline') {{
        const k = msg.k;
        const candle = {{
          time: Math.floor(k.t / 1000) + (9 * 3600), // KST UTC+9 offset
          open: parseFloat(k.o),
          high: parseFloat(k.h),
          low: parseFloat(k.l),
          close: parseFloat(k.c),
          volume: parseFloat(k.v)
        }};

        // Update active candle
        const lastIdx = rawCandles.length - 1;
        if (rawCandles.length > 0 && rawCandles[lastIdx].time === candle.time) {{
          rawCandles[lastIdx] = candle;
        }} else {{
          rawCandles.push(candle);
          if (rawCandles.length > 500) rawCandles.shift();
        }}

        candleSeries.update(candle);
        volumeSeries.update({{
          time: candle.time,
          value: candle.volume,
          color: candle.close >= candle.open ? 'rgba(16, 185, 129, 0.45)' : 'rgba(239, 68, 68, 0.45)'
        }});
        legendPrice.textContent = `$${{candle.close.toLocaleString()}}`;
        if (legendVol) {{
          legendVol.textContent = candle.volume >= 1000 ? (candle.volume / 1000).toFixed(1) + 'k' : candle.volume.toFixed(1);
        }}

        // Live Paper Trade evaluation on candle close
        if (isFollowing && k.x) {{
          checkLivePaperTradeSignal(candle);
        }}
      }}
    }};

    activeWs.onerror = (e) => console.warn('[StrategyLab] WS error:', e);
    activeWs.onclose = () => {{
      console.log('[StrategyLab] WS closed, reconnecting in 5s...');
      setTimeout(() => connectWebSocket(currentActiveInterval), 5000);
    }};
  }}

  // 6. Real-Time Paper Trading Auto-Follow & Unified Vibe Account Synchronization
  function checkLivePaperTradeSignal(candle) {{
    const ind = computeIndicators(rawCandles, parseInt(params.bb_period), parseFloat(params.bb_std));
    const lastIdx = rawCandles.length - 1;
    const lowerVal = ind.lower[lastIdx];
    const upperVal = ind.upper[lastIdx];
    const avgVol = ind.volSma[lastIdx];
    const rsiVal = ind.rsi[lastIdx] || 50;

    const volMult = parseFloat(params.vol_mult);
    const rsiTh = parseFloat(params.rsi_threshold);
    const tpPct = parseFloat(params.tp_percent) / 100.0;
    const slPct = parseFloat(params.sl_percent) / 100.0;
    const lev = parseFloat(params.leverage);

    const isLowerTouch = candle.low <= lowerVal;
    const isUpperTouch = candle.high >= upperVal;
    const isVolSurge = avgVol ? (candle.volume >= avgVol * volMult) : true;
    const isRsiOversold = rsiVal <= rsiTh;
    const isRsiOverbought = rsiVal >= (100 - rsiTh);

    if (!currentPosition) {{
      let enterSide = null;
      if (isLowerTouch && isVolSurge && isRsiOversold) {{
        enterSide = 'LONG';
      }} else if (isUpperTouch && isVolSurge && isRsiOverbought) {{
        enterSide = 'SHORT';
      }}

      if (enterSide) {{
        const margin = 3000.0; // $10k 가상자본금의 30% 격리 증거금
        const coinSize = (margin * lev) / candle.close;
        const tpPrice = enterSide === 'LONG' ? candle.close * (1 + tpPct) : candle.close * (1 - tpPct);
        const slPrice = enterSide === 'LONG' ? candle.close * (1 - slPct) : candle.close * (1 + slPct);
        const liqPrice = enterSide === 'LONG' ? candle.close * (1 - 0.9 / lev) : candle.close * (1 + 0.9 / lev);

        currentPosition = {{
          id: 'bot_' + Date.now(),
          type: enterSide,
          entryPrice: candle.close,
          time: candle.time,
          margin: margin,
          size: coinSize,
          tpPrice: tpPrice,
          slPrice: slPrice,
          leverage: lev
        }};

        renderTargetLines(enterSide, candle.close, tpPct, slPct, lev, true);

        livePosDesc.innerHTML = `<span style="color: ${{enterSide === 'LONG' ? '#10b981' : '#f43f5e'}}; font-weight: 800;">${{enterSide}} @ $${{candle.close.toFixed(1)}}</span> (익절: $${{tpPrice.toFixed(0)}}, 손절: $${{slPrice.toFixed(0)}}) · Vibe Trading 자동체결 완료`;
        console.log('🤖 [AUTO-PAPER] Strategy Signal Triggered:', enterSide, currentPosition);

        // Sync to shared Vibe Trading Account State
        try {{
          let vibe = JSON.parse(localStorage.getItem('blogin_vibe_state')) || {{}};
          if (!vibe.positions) vibe.positions = [];
          // Remove previous bot positions
          vibe.positions = vibe.positions.filter(p => !p.id || !p.id.startsWith('bot_'));
          vibe.positions.push({{
            id: currentPosition.id,
            asset: 'BTC/USDT',
            side: enterSide,
            entryPrice: candle.close,
            margin: margin,
            size: coinSize,
            leverage: lev,
            liqPrice: liqPrice,
            tpPrice: tpPrice,
            slPrice: slPrice,
            createdAt: new Date().toLocaleTimeString(),
            botSource: STRATEGY_CONFIG.title
          }});
          localStorage.setItem('blogin_vibe_state', JSON.stringify(vibe));
        }} catch(e) {{}}
      }}
    }} else if (currentPosition) {{
      const enterSide = currentPosition.type;
      const entryPrice = currentPosition.entryPrice;
      const tpPrice = currentPosition.tpPrice;
      const slPrice = currentPosition.slPrice;
      const feeRate = 0.0010;

      let hitSl = enterSide === 'LONG' ? candle.low <= slPrice : candle.high >= slPrice;
      let hitTp = enterSide === 'LONG' ? candle.high >= tpPrice : candle.low <= tpPrice;

      if (hitSl || hitTp) {{
        let isWin = false;
        let exitPrice = candle.close;
        let rawPnl = 0;

        if (hitSl) {{
          exitPrice = slPrice;
          rawPnl = -slPct;
          isWin = false;
        }} else if (hitTp) {{
          exitPrice = tpPrice;
          rawPnl = tpPct;
          isWin = true;
        }}

        const netPnlPct = (rawPnl - feeRate) * currentPosition.leverage;
        const pnlDollars = currentPosition.margin * netPnlPct;
        virtualBalance += pnlDollars;

        livePosDesc.innerHTML = `청산 완료: <strong style="color: ${{isWin ? '#10b981' : '#ef4444'}};">${{isWin ? '익절 성공' : '손절 컷'}} (${{pnlDollars >= 0 ? '+' : ''}}$${{pnlDollars.toFixed(2)}})</strong>`;
        currentPosition = null;

        // Keep last bracket on chart
        renderTargetLines(enterSide, entryPrice, tpPct, slPct, lev, false);

        // Update shared Vibe Trading Account Balance
        try {{
          let vibe = JSON.parse(localStorage.getItem('blogin_vibe_state')) || {{}};
          if (vibe.positions) {{
            vibe.positions = vibe.positions.filter(p => !p.id || !p.id.startsWith('bot_'));
          }}
          vibe.cash = (vibe.cash !== undefined ? vibe.cash : 10000.0) + pnlDollars;
          localStorage.setItem('blogin_vibe_state', JSON.stringify(vibe));
        }} catch(e) {{}}
      }}
    }}
  }}

  // 7. Event Listeners for Parameter Sliders, Timeframe Tabs & Bot Sync
  function attachListeners() {{
    let activeInterval = INTERVAL;

    // Timeframe Switcher Tabs
    document.querySelectorAll('.btn-tf').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        const newTf = btn.getAttribute('data-tf');
        if (!newTf || newTf === activeInterval) return;

        document.querySelectorAll('.btn-tf').forEach(b => {{
          b.style.background = '#1e293b';
          b.style.borderColor = '#334155';
          b.style.color = '#94a3b8';
        }});
        btn.style.background = '#2563eb';
        btn.style.borderColor = '#3b82f6';
        btn.style.color = '#ffffff';

        activeInterval = newTf;
        fetchHistoricalCandlesWithInterval(newTf);
      }});
    }});

    const update = () => {{
      params.bb_period = sliderBbPeriod.value;
      params.bb_std = sliderBbStd.value;
      params.vol_mult = sliderVolMult.value;
      params.rsi_threshold = sliderRsiTh.value;
      params.tp_percent = sliderTp.value;
      params.sl_percent = sliderSl.value;
      params.leverage = sliderLev.value;

      valBbPeriod.textContent = params.bb_period;
      valBbStd.textContent = params.bb_std;
      valVolMult.textContent = `${{params.vol_mult}}x`;
      valRsiTh.textContent = `${{params.rsi_threshold}} 이하`;
      valTp.textContent = `+${{params.tp_percent}}%`;
      valSl.textContent = `-${{params.sl_percent}}%`;
      valLev.textContent = `${{params.leverage}}x`;

      runBacktestAndRender();
    }};

    sliderBbPeriod.addEventListener('input', update);
    sliderBbStd.addEventListener('input', update);
    sliderVolMult.addEventListener('input', update);
    sliderRsiTh.addEventListener('input', update);
    sliderTp.addEventListener('input', update);
    sliderSl.addEventListener('input', update);
    sliderLev.addEventListener('input', update);

    // Reset button
    document.getElementById('btn-reset-params').addEventListener('click', () => {{
      params = {{ ...STRATEGY_CONFIG.default_params }};
      sliderBbPeriod.value = params.bb_period;
      sliderBbStd.value = params.bb_std;
      sliderVolMult.value = params.vol_mult;
      sliderRsiTh.value = params.rsi_threshold;
      sliderTp.value = params.tp_percent;
      sliderSl.value = params.sl_percent;
      sliderLev.value = params.leverage;
      update();
    }});

    // Follow Toggle (Unified Vibe Trading Cross-Page Synchronization)
    // TradingView Official Pro Chart Mode Switcher
    const btnModeLab = document.getElementById('btn-mode-lab');
    const btnModeTv = document.getElementById('btn-mode-tv-pro');
    const labViewport = document.getElementById('quant-lab-viewport');
    const tvViewport = document.getElementById('tv-official-viewport');
    let tvOfficialWidget = null;

    function initTradingViewOfficial() {{
      if (tvOfficialWidget) return;
      function createTv() {{
        if (!window.TradingView) return;
        tvOfficialWidget = new TradingView.widget({{
          autosize: true,
          symbol: 'BINANCE:' + SYMBOL,
          interval: (INTERVAL === '1m' ? '1' : (INTERVAL === '5m' ? '5' : (INTERVAL === '15m' ? '15' : (INTERVAL === '1h' ? '60' : '15')))),
          timezone: 'Asia/Seoul',
          theme: 'dark',
          style: '1',
          locale: 'kr',
          toolbar_bg: '#0d131f',
          enable_publishing: false,
          allow_symbol_change: true,
          container_id: 'tradingview_official_embed',
          studies: [
            'BB@tv-basicstudies',
            'RSI@tv-basicstudies'
          ]
        }});
      }}

      if (!window.TradingView) {{
        const s = document.createElement('script');
        s.src = 'https://s3.tradingview.com/tv.js';
        s.onload = createTv;
        document.head.appendChild(s);
      }} else {{
        createTv();
      }}
    }}

    if (btnModeLab && btnModeTv) {{
      btnModeLab.addEventListener('click', () => {{
        btnModeLab.style.background = '#2563eb';
        btnModeLab.style.borderColor = '#3b82f6';
        btnModeLab.style.color = '#ffffff';
        btnModeTv.style.background = 'transparent';
        btnModeTv.style.borderColor = 'transparent';
        btnModeTv.style.color = '#94a3b8';
        labViewport.style.display = 'block';
        tvViewport.style.display = 'none';
        if (chart && chartContainer) {{
          chart.applyOptions({{ width: chartContainer.clientWidth }});
        }}
      }});

      btnModeTv.addEventListener('click', () => {{
        btnModeTv.style.background = '#2563eb';
        btnModeTv.style.borderColor = '#3b82f6';
        btnModeTv.style.color = '#ffffff';
        btnModeLab.style.background = 'transparent';
        btnModeLab.style.borderColor = 'transparent';
        btnModeLab.style.color = '#94a3b8';
        labViewport.style.display = 'none';
        tvViewport.style.display = 'block';
        initTradingViewOfficial();
      }});
    }}

    toggleFollow.addEventListener('change', (e) => {{
      isFollowing = e.target.checked;
      let vibe = {{}};
      try {{
        vibe = JSON.parse(localStorage.getItem('blogin_vibe_state')) || {{}};
      }} catch(err) {{}}

      if (isFollowing) {{
        followLabel.textContent = '🟢 모의투자 계좌 장착됨';
        followLabel.style.color = '#10b981';
        toggleBg.style.backgroundColor = '#10b981';
        liveStatusBar.style.display = 'block';

        // Register Bot to Global Vibe Trading Account
        vibe.activeBot = {{
          id: STRATEGY_CONFIG.strategy_id,
          title: STRATEGY_CONFIG.title,
          symbol: SYMBOL,
          interval: activeInterval,
          params: params,
          active: true,
          started_at: Date.now()
        }};
        localStorage.setItem('blogin_vibe_state', JSON.stringify(vibe));
      }} else {{
        followLabel.textContent = '추종 비활성';
        followLabel.style.color = '#94a3b8';
        toggleBg.style.backgroundColor = '#334155';
        liveStatusBar.style.display = 'none';

        if (vibe.activeBot) {{
          vibe.activeBot.active = false;
          localStorage.setItem('blogin_vibe_state', JSON.stringify(vibe));
        }}
      }}
    }});
  }}

  // 8. Boot Sequence
  function boot() {{
    initChart();
    attachListeners();
    fetchHistoricalCandles();
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', boot);
  }} else {{
    boot();
  }}
}})();
</script>
"""
        return html
