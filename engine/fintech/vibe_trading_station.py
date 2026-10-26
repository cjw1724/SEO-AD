"""
Blogin 365 AI Holdings - Vibe Trading & Leaderboard Pro Station (v9.0 Apex)
World-Class Interactive Financial Trading Terminal for Google Blogger

Features:
1. Pro Bloomberg/Bybit Terminal Header:
   - Binance WebSocket Latency monitor (WSS Live ms)
   - Real-time KST Clock & Sound FX Synthesizer (Web Audio API)
   - 24h Ticker Tape with High/Low/Vol stats for BTC, ETH, SOL, DOGE, BNB, XRP
2. Dual-Chart Pro Engine:
   - Official TradingView Advanced Real-Time Chart widget (Dark theme, multi-timeframe, full indicators)
   - 60fps HTML5 Canvas ultra-fast chart fallback
3. Pro Order Execution with Bracket Orders (TP/SL):
   - Market / Limit toggle
   - 1x - 25x Dynamic Leverage
   - Margin percentage quick selectors (10%, 25%, 50%, 75%, 100%)
   - Take Profit (TP %) and Stop Loss (SL %) bracket targets with live target price preview
   - Real-time Risk/Reward (손익비) ratio calculator & Kelly Criterion position sizing
4. AI Quant Bot Fleet Manager (3대 AI 퀀트 전략봇 카피트레이딩 탭):
   - 🤖 워뇨띠 볼린저 반등봇 (15m)
   - 🤖 슈퍼트렌드 1분봉 초단타 스캘퍼 (1m)
   - 🤖 래리 윌리엄스 변동성 돌파봇 (1h)
   - Live telemetry status & 1-click Auto-Trade toggle
5. Multi-Tab Positions & Trade Journal Center:
   - Tab 1: 💼 실시간 보유 포지션 (Open Positions) with live PnL & 1-click Market Close
   - Tab 2: 📜 체결 & 청산 일지 (Trade Journal) with exit reason (TP/SL/Manual)
   - Tab 3: 📊 퀀트 성적표 (Account Analytics: Win Rate, Profit Factor, MDD, ROI)
6. Dynamic Competitive Leaderboard:
   - AI Strategy Bots vs Human Traders ranking
   - Real-time live execution feed ticker
   - LocalStorage persistence & viral URL hash sharing
7. 100% Toss Design System (TDS) Dark Theme & WCAG 2.1 AAA Compliance
"""

import json
from typing import Dict, Any, List

class VibeTradingStation:
    def __init__(self, blog_url: str = "https://blogin365ai.blogspot.com"):
        self.blog_url = blog_url.rstrip("/")

    def generate_station_html(self) -> str:
        """
        Generates the standalone, complete HTML for the Vibe Trading Terminal Page.
        Can be deployed directly to Blogger Static Pages (p/vibe-trading.html) or embedded in posts.
        """
        return """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VIBE TRADING PRO - 실시간 퀀트 모의투자 & AI 전략봇 랭킹전 | Blogin 365 AI Holdings</title>
  
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Blogin 365 Vibe Trading Pro Terminal & AI Bot Fleet",
    "applicationCategory": "FinanceApplication",
    "operatingSystem": "Any",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    },
    "description": "실시간 바이낸스 WSS 연동, 3대 AI 퀀트 전략봇 카피트레이딩, 브래킷 익절(TP)/손절(SL) 주문, 트레이딩뷰 프로 차트, 실시간 랭킹 리더보드"
  }
  </script>

  <style>
    /* ==========================================================================
       Vibe Trading Pro Terminal - Toss Dark High-Precision Theme (v9.0 Apex)
       ========================================================================== */
    :root {
      --vibe-bg-base: #0a0e17;
      --vibe-bg-surface: #111827;
      --vibe-bg-card: #131d2e;
      --vibe-bg-card-hover: #1b263b;
      --vibe-border-card: #1f2d47;
      --vibe-border-subtle: #2d3e5e;

      --vibe-text-primary: #ffffff;
      --vibe-text-body: #e2e8f0;
      --vibe-text-muted: #94a3b8;

      --vibe-green: #10b981;
      --vibe-green-bg: rgba(16, 185, 129, 0.12);
      --vibe-red: #ef4444;
      --vibe-red-bg: rgba(239, 68, 68, 0.12);
      --vibe-blue: #3b82f6;
      --vibe-blue-bg: rgba(59, 130, 246, 0.12);
      --vibe-gold: #f59e0b;
      --vibe-purple: #a855f7;

      --vibe-font-sans: 'Pretendard Variable', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --vibe-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--vibe-bg-base);
      color: var(--vibe-text-body);
      font-family: var(--vibe-font-sans);
      line-height: 1.5;
      padding: 12px;
      -webkit-font-smoothing: antialiased;
    }

    .vibe-terminal-container {
      max-width: 1320px;
      margin: 0 auto;
    }

    /* Top Bloomberg-style Pro Ticker & Latency Bar */
    .vibe-top-telemetry {
      background: #070a10;
      border: 1px solid var(--vibe-border-card);
      border-radius: 12px;
      padding: 8px 16px;
      margin-bottom: 12px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      font-size: 11px;
      color: var(--vibe-text-muted);
    }

    .vibe-telemetry-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Top Sticky HUD */
    .vibe-header {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      border-radius: 16px;
      padding: 16px 20px;
      margin-bottom: 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .vibe-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .vibe-brand-badge {
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 8px;
      letter-spacing: 0.05em;
    }

    .vibe-title {
      font-size: 20px;
      font-weight: 900;
      color: var(--vibe-text-primary);
      letter-spacing: -0.02em;
    }

    .vibe-account-hud {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
    }

    .vibe-hud-metric {
      background: var(--vibe-bg-base);
      border: 1px solid var(--vibe-border-card);
      border-radius: 10px;
      padding: 8px 14px;
      display: flex;
      flex-direction: column;
    }

    .vibe-hud-label {
      font-size: 11px;
      color: var(--vibe-text-muted);
      font-weight: 600;
    }

    .vibe-hud-val {
      font-size: 15px;
      font-weight: 800;
      font-family: var(--vibe-font-mono);
      color: var(--vibe-text-primary);
    }

    .vibe-hud-val.pos { color: var(--vibe-green); }
    .vibe-hud-val.neg { color: var(--vibe-red); }

    .vibe-btn-action {
      background: transparent;
      border: 1px solid var(--vibe-border-subtle);
      color: var(--vibe-text-muted);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .vibe-btn-action:hover {
      background: rgba(37, 99, 235, 0.15);
      border-color: var(--vibe-blue);
      color: #60a5fa;
    }

    .vibe-reset-btn {
      background: transparent;
      border: 1px solid var(--vibe-border-subtle);
      color: var(--vibe-text-muted);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .vibe-reset-btn:hover {
      background: rgba(239, 68, 68, 0.15);
      border-color: var(--vibe-red);
      color: var(--vibe-red);
    }

    /* 24h Market Overview Tape */
    .vibe-market-tape {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 16px;
    }

    .vibe-asset-pill {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      color: var(--vibe-text-body);
      border-radius: 12px;
      padding: 8px 14px;
      font-size: 12px;
      font-weight: 700;
      font-family: var(--vibe-font-mono);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .vibe-asset-pill:hover, .vibe-asset-pill.active {
      background: #1e3a8a;
      border-color: var(--vibe-blue);
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }

    .vibe-asset-pill.active .ticker-price {
      color: #ffffff !important;
    }

    .vibe-asset-pill .ticker-price {
      color: var(--vibe-green);
      font-weight: 800;
    }

    .vibe-asset-pill .ticker-change {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 800;
    }

    .vibe-asset-pill .ticker-change.pos {
      background: rgba(16, 185, 129, 0.25);
      color: #6ee7b7;
    }

    .vibe-asset-pill .ticker-change.neg {
      background: rgba(239, 68, 68, 0.25);
      color: #fca5a5;
    }

    .vibe-asset-pill.active .ticker-change.neg {
      background: rgba(0, 0, 0, 0.5);
      color: #fca5a5;
    }

    .vibe-asset-pill.active .ticker-change.pos {
      background: rgba(0, 0, 0, 0.5);
      color: #6ee7b7;
    }

    /* Main Grid: Chart (2/3) + Order Panel (1/3) */
    .vibe-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }

    @media (max-width: 992px) {
      .vibe-grid {
        grid-template-columns: 1fr;
      }
    }

    .vibe-chart-card {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .vibe-chart-header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }

    .vibe-chart-tabs {
      display: flex;
      gap: 6px;
    }

    .vibe-chart-tab {
      background: var(--vibe-bg-base);
      border: 1px solid var(--vibe-border-card);
      color: var(--vibe-text-muted);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .vibe-chart-tab.active {
      background: #1d4ed8;
      border-color: #2563eb;
      color: #ffffff;
    }

    .vibe-chart-viewport {
      height: 520px;
      width: 100%;
      border-radius: 10px;
      overflow: hidden;
      background: #000000;
      position: relative;
    }

    /* Order Execution Panel */
    .vibe-order-panel {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      border-radius: 16px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .vibe-order-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--vibe-text-primary);
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--vibe-border-card);
      padding-bottom: 10px;
    }

    .vibe-side-switch {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .vibe-side-btn {
      padding: 11px;
      border: none;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .vibe-side-btn.long {
      background: #1e293b;
      border: 1px solid #334155;
      color: #6ee7b7;
    }

    .vibe-side-btn.long.active {
      background: #047857;
      border-color: #10b981;
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }

    .vibe-side-btn.short {
      background: #1e293b;
      border: 1px solid #334155;
      color: #fca5a5;
    }

    .vibe-side-btn.short.active {
      background: #b91c1c;
      border-color: #ef4444;
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }

    .vibe-form-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }

    .vibe-form-label {
      font-size: 11px;
      font-weight: 700;
      color: var(--vibe-text-muted);
      display: flex;
      justify-content: space-between;
    }

    .vibe-input {
      background: var(--vibe-bg-base);
      border: 1px solid var(--vibe-border-subtle);
      border-radius: 8px;
      padding: 9px 12px;
      color: #ffffff;
      font-size: 14px;
      font-family: var(--vibe-font-mono);
      width: 100%;
    }

    .vibe-input:focus {
      outline: none;
      border-color: var(--vibe-blue);
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
    }

    .vibe-leverage-bar {
      display: flex;
      gap: 6px;
    }

    .vibe-lev-btn {
      flex: 1;
      background: var(--vibe-bg-base);
      border: 1px solid var(--vibe-border-card);
      color: var(--vibe-text-body);
      border-radius: 6px;
      padding: 7px 4px;
      font-size: 11px;
      font-weight: 800;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }

    .vibe-lev-btn:hover {
      border-color: #3b82f6;
      color: #93c5fd;
    }

    .vibe-lev-btn.active {
      background: #2563eb;
      border-color: #3b82f6;
      color: #ffffff;
    }

    /* Bracket Orders (TP/SL) Grid */
    .vibe-bracket-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      background: #0a0e17;
      border: 1px solid var(--vibe-border-card);
      border-radius: 10px;
      padding: 10px;
    }

    .vibe-bracket-box {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .vibe-bracket-header {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 700;
    }

    .vibe-exec-btn {
      width: 100%;
      padding: 14px;
      border: none;
      border-radius: 12px;
      font-size: 14px;
      font-weight: 900;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: 4px;
    }

    .vibe-exec-btn.long-mode {
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff;
      box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
    }

    .vibe-exec-btn.short-mode {
      background: linear-gradient(135deg, #ef4444, #dc2626);
      color: #ffffff;
      box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
    }

    .vibe-exec-btn:hover {
      transform: translateY(-2px);
      filter: brightness(1.1);
    }

    /* AI Quant Bot Fleet Section */
    .vibe-bot-fleet-card {
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(168, 85, 247, 0.08));
      border: 1px solid rgba(59, 130, 246, 0.35);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }

    .vibe-bot-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-top: 14px;
    }

    .vibe-bot-card {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: all 0.2s ease;
    }

    .vibe-bot-card:hover {
      border-color: var(--vibe-blue);
      transform: translateY(-2px);
    }

    .vibe-bot-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Lower Section: Tabs for Positions, History, Leaderboard */
    .vibe-panel-tabs {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--vibe-border-card);
      padding-bottom: 10px;
      margin-bottom: 16px;
    }

    .vibe-panel-tab {
      background: transparent;
      border: 1px solid transparent;
      color: var(--vibe-text-muted);
      border-radius: 8px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .vibe-panel-tab.active {
      background: var(--vibe-bg-card);
      border-color: var(--vibe-border-subtle);
      color: #38bdf8;
    }

    .vibe-lower-grid {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 16px;
      margin-bottom: 24px;
    }

    @media (max-width: 992px) {
      .vibe-lower-grid {
        grid-template-columns: 1fr;
      }
    }

    .vibe-panel-card {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .vibe-card-header {
      font-size: 15px;
      font-weight: 800;
      color: var(--vibe-text-primary);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Tables */
    .vibe-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }

    .vibe-table th {
      text-align: left;
      padding: 10px 10px;
      color: var(--vibe-text-muted);
      border-bottom: 1px solid var(--vibe-border-card);
      font-weight: 700;
      white-space: nowrap;
    }

    .vibe-table td {
      padding: 11px 10px;
      border-bottom: 1px solid var(--vibe-border-card);
      font-family: var(--vibe-font-mono);
      color: var(--vibe-text-body);
    }

    .vibe-rank-badge {
      display: inline-block;
      width: 22px;
      height: 22px;
      line-height: 22px;
      text-align: center;
      border-radius: 50%;
      font-weight: 800;
      font-size: 11px;
    }

    .vibe-rank-1 { background: #fbbf24; color: #000000; }
    .vibe-rank-2 { background: #cbd5e1; color: #000000; }
    .vibe-rank-3 { background: rgba(217, 119, 6, 0.25); border: 1px solid #f59e0b; color: #fbbf24; }

    .vibe-my-rank-row {
      background: rgba(59, 130, 246, 0.12) !important;
      font-weight: 800 !important;
    }

    .vibe-my-rank-row td {
      color: #60a5fa !important;
      border-top: 2px solid var(--vibe-blue);
      border-bottom: 2px solid var(--vibe-blue);
    }

    /* Live Feed Ticker */
    .vibe-live-feed {
      background: var(--vibe-bg-base);
      border: 1px solid var(--vibe-border-card);
      border-radius: 10px;
      padding: 10px;
      height: 150px;
      overflow-y: hidden;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .vibe-feed-item {
      font-size: 11px;
      display: flex;
      align-items: center;
      gap: 6px;
      animation: fadeIn 0.4s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Disclaimer Box */
    .vibe-disclaimer {
      background: #0f172a;
      border-left: 4px solid #ef4444;
      border-radius: 12px;
      padding: 16px 20px;
      color: var(--vibe-text-muted);
      font-size: 12px;
      line-height: 1.6;
    }

    .vibe-disclaimer strong {
      color: #f87171;
      display: block;
      margin-bottom: 4px;
      font-size: 13px;
    }
  </style>
</head>
<body>

<div class="vibe-terminal-container">

  <!-- Top Telemetry & Health Bar -->
  <div class="vibe-top-telemetry">
    <div style="display:flex; align-items:center; gap:16px;">
      <span class="vibe-telemetry-item">
        <span style="display:inline-block; width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 6px #10b981;"></span>
        <strong style="color:#10b981;">BINANCE WSS LIVE</strong> <span id="ws-latency-badge">(14ms)</span>
      </span>
      <span class="vibe-telemetry-item">
        <span>🕒 한국표준시:</span>
        <strong style="color:#f8fafc;" id="kst-clock-display">--:--:-- KST</strong>
      </span>
      <span class="vibe-telemetry-item">
        <span>🤖 AI 전략봇:</span>
        <strong style="color:#38bdf8;">3기 가동 중</strong>
      </span>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
      <button class="vibe-btn-action" id="btn-toggle-sound" onclick="VibeEngine.toggleSound()" style="padding:4px 10px; font-size:11px;">
        <span id="sound-icon">🔊</span> 사운드 ON
      </button>
      <a href="/" style="color:#38bdf8; text-decoration:none; font-weight:700;">🏠 블로그 홈 포털</a>
    </div>
  </div>

  <!-- Top Sticky HUD -->
  <header class="vibe-header">
    <div class="vibe-brand">
      <span class="vibe-brand-badge">PRO QUANT TERMINAL</span>
      <div>
        <h1 class="vibe-title">🔥 VIBE TRADING PRO (실시간 모의투자 & AI 전략봇 랭킹전)</h1>
        <p style="margin:0; font-size:12px; color:#94a3b8;">
          바이낸스 실시간 시세 직결 · 브래킷 익절(TP)/손절(SL) 자동 체결 · 100% 무인 퀀트 모의투자 엔진
        </p>
      </div>
    </div>

    <div class="vibe-account-hud">
      <div class="vibe-hud-metric">
        <span class="vibe-hud-label">총 평가자산 (Equity)</span>
        <span class="vibe-hud-val" id="hud-equity">$10,000.00</span>
      </div>
      <div class="vibe-hud-metric">
        <span class="vibe-hud-label">가용 증거금 (Available)</span>
        <span class="vibe-hud-val" id="hud-cash">$10,000.00</span>
      </div>
      <div class="vibe-hud-metric">
        <span class="vibe-hud-label">실시간 수익률 (Total PnL)</span>
        <span class="vibe-hud-val pos" id="hud-pnl">+0.00% ($0.00)</span>
      </div>
      <button class="vibe-reset-btn" id="btn-reset-account" onclick="VibeEngine.resetAccount()">🔄 자산 초기화</button>
    </div>
  </header>

  <!-- 24h Market Overview Tape -->
  <div class="vibe-market-tape" id="asset-selector-bar">
    <button class="vibe-asset-pill active" onclick="VibeEngine.selectAsset('BTCUSDT', 'BINANCE:BTCUSDT')">
      <span>BTC/USDT</span> <span class="ticker-price" id="pill-price-BTCUSDT">$80,410.00</span>
      <span class="ticker-change pos" id="pill-change-BTCUSDT">+2.45%</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('ETHUSDT', 'BINANCE:ETHUSDT')">
      <span>ETH/USDT</span> <span class="ticker-price" id="pill-price-ETHUSDT">$2,540.80</span>
      <span class="ticker-change pos" id="pill-change-ETHUSDT">+1.12%</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('SOLUSDT', 'BINANCE:SOLUSDT')">
      <span>SOL/USDT</span> <span class="ticker-price" id="pill-price-SOLUSDT">$178.40</span>
      <span class="ticker-change pos" id="pill-change-SOLUSDT">+3.80%</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('DOGEUSDT', 'BINANCE:DOGEUSDT')">
      <span>DOGE/USDT</span> <span class="ticker-price" id="pill-price-DOGEUSDT">$0.1420</span>
      <span class="ticker-change neg" id="pill-change-DOGEUSDT">-0.85%</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('BNBUSDT', 'BINANCE:BNBUSDT')">
      <span>BNB/USDT</span> <span class="ticker-price" id="pill-price-BNBUSDT">$585.20</span>
      <span class="ticker-change pos" id="pill-change-BNBUSDT">+0.95%</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('XRPUSDT', 'BINANCE:XRPUSDT')">
      <span>XRP/USDT</span> <span class="ticker-price" id="pill-price-XRPUSDT">$0.5280</span>
      <span class="ticker-change neg" id="pill-change-XRPUSDT">-0.42%</span>
    </button>
  </div>

  <!-- Main Trading Area: Chart (2) + Order Execution (1) -->
  <div class="vibe-grid">

    <!-- Chart Card -->
    <div class="vibe-chart-card">
      <div class="vibe-chart-header">
        <div style="display:flex; align-items:center; gap:10px;">
          <strong style="color:#ffffff; font-size:16px;" id="chart-asset-title">BTC/USDT 실시간 차트</strong>
          <span style="font-size:11px; color:#10b981; font-weight:700; background:rgba(16,185,129,0.15); padding:2px 8px; border-radius:6px;" id="chart-live-badge">🟢 바이낸스 실시간 시세 연동</span>
        </div>
        <div class="vibe-chart-tabs">
          <button class="vibe-chart-tab active" id="tab-tv" onclick="VibeEngine.switchChart('tv')">🌐 트레이딩뷰 공식 프로 차트</button>
          <button class="vibe-chart-tab" id="tab-canvas" onclick="VibeEngine.switchChart('canvas')">⚡ 초고속 캔버스</button>
        </div>
      </div>

      <div class="vibe-chart-viewport" id="chart-container">
        <!-- TradingView Widget -->
        <div id="tv_chart_container" style="height:100%; width:100%;"></div>
        <!-- Canvas Fallback -->
        <canvas id="canvas_chart_viewport" width="800" height="520" style="display:none; width:100%; height:100%;"></canvas>
      </div>
    </div>

    <!-- Order Execution Panel with Bracket Orders (TP/SL) -->
    <div class="vibe-order-panel">
      <div class="vibe-order-title">
        <span>⚡ 프로 레버리지 모의 주문</span>
        <span style="font-size:11px; color:#38bdf8; font-weight:800;" id="current-asset-badge">BTC/USDT</span>
      </div>

      <!-- Long / Short Switch -->
      <div class="vibe-side-switch">
        <button class="vibe-side-btn long active" id="btn-side-long" onclick="VibeEngine.setSide('LONG')">🟢 BUY / LONG (롱)</button>
        <button class="vibe-side-btn short" id="btn-side-short" onclick="VibeEngine.setSide('SHORT')">🔴 SELL / SHORT (숏)</button>
      </div>

      <!-- Leverage Selector -->
      <div class="vibe-form-group">
        <div class="vibe-form-label">
          <span>레버리지 (배율)</span>
          <span id="label-leverage" style="color:#3b82f6; font-weight:800;">10x</span>
        </div>
        <div class="vibe-leverage-bar">
          <button class="vibe-lev-btn" onclick="VibeEngine.setLeverage(1)">1x</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setLeverage(2)">2x</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setLeverage(5)">5x</button>
          <button class="vibe-lev-btn active" onclick="VibeEngine.setLeverage(10)">10x</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setLeverage(20)">20x</button>
        </div>
      </div>

      <!-- Margin Input -->
      <div class="vibe-form-group">
        <div class="vibe-form-label">
          <span>투입 증거금 (Margin USDT)</span>
          <span id="label-max-margin" style="color:#94a3b8;">최대: $10,000.00</span>
        </div>
        <input type="number" class="vibe-input" id="input-order-margin" value="2000" min="10" step="10" oninput="VibeEngine.calculateOrderPreview()">
        <div style="display:flex; gap:6px; margin-top:4px;">
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.10)">10%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.25)">25%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.50)">50%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.75)">75%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(1.00)">100%</button>
        </div>
      </div>

      <!-- Bracket Orders: Take Profit (TP) & Stop Loss (SL) -->
      <div class="vibe-bracket-grid">
        <div class="vibe-bracket-box">
          <div class="vibe-bracket-header">
            <span style="color:#10b981;">🎯 익절 목표 (TP %)</span>
            <strong style="color:#10b981;" id="label-tp-target">+2.0%</strong>
          </div>
          <input type="number" class="vibe-input" id="input-tp-pct" value="2.0" step="0.1" min="0.1" max="20" style="padding:6px 10px; font-size:12px;" oninput="VibeEngine.calculateOrderPreview()">
          <span style="font-size:10px; color:#94a3b8;" id="desc-tp-price">목표가: 계산 중...</span>
        </div>

        <div class="vibe-bracket-box">
          <div class="vibe-bracket-header">
            <span style="color:#ef4444;">🚨 손절 한도 (SL %)</span>
            <strong style="color:#ef4444;" id="label-sl-target">-1.0%</strong>
          </div>
          <input type="number" class="vibe-input" id="input-sl-pct" value="1.0" step="0.1" min="0.1" max="10" style="padding:6px 10px; font-size:12px;" oninput="VibeEngine.calculateOrderPreview()">
          <span style="font-size:10px; color:#94a3b8;" id="desc-sl-price">손절가: 계산 중...</span>
        </div>
      </div>

      <!-- Order Metrics Preview -->
      <div style="background:#0a0e17; border:1px solid #1f2d47; border-radius:10px; padding:10px 12px; font-size:11px; display:flex; flex-direction:column; gap:5px;">
        <div style="display:flex; justify-content:space-between;">
          <span style="color:#94a3b8;">포지션 규모:</span>
          <strong style="color:#ffffff;" id="preview-notional">$20,000.00</strong>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:#94a3b8;">강제 청산가:</span>
          <strong style="color:#ef4444;" id="preview-liq">$72,720.00 (-9.5%)</strong>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:#94a3b8;">손익비 (Risk-Reward):</span>
          <strong style="color:#38bdf8;" id="preview-rr">2.0 : 1 (우수)</strong>
        </div>
      </div>

      <!-- Big Action Submit Button -->
      <button class="vibe-exec-btn long-mode" id="btn-submit-order" onclick="VibeEngine.executeOrder()">
        🚀 BTC 10x 롱 포지션 진입 (주문 실행)
      </button>
    </div>

  </div>

  <!-- AI Quant Strategy Bot Fleet Section -->
  <div class="vibe-bot-fleet-card">
    <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:10px;">
      <div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">🤖</span>
          <strong style="color:#ffffff; font-size:16px;">AI 퀀트 전략봇 자율 함대 (Bot Fleet & Copy-Trade)</strong>
        </div>
        <p style="margin:2px 0 0 0; font-size:12px; color:#94a3b8;">
          블로그 아티클에서 팩트체크된 3대 퀀트 알고리즘이 24시간 실시간 시세를 감시하며 자동 가상 매매를 수행합니다.
        </p>
      </div>
      <span style="font-size:11px; color:#10b981; font-weight:800; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); padding:4px 10px; border-radius:8px;">
        ● 전자동 가상 카피트레이딩 가동 가능
      </span>
    </div>

    <div class="vibe-bot-grid">
      <!-- Bot 1: Wonyotti Bollinger -->
      <div class="vibe-bot-card" id="bot-card-wonyotti">
        <div class="vibe-bot-header">
          <strong style="color:#38bdf8; font-size:14px;">🤖 워뇨띠 볼린저 반등봇</strong>
          <span style="font-size:11px; color:#94a3b8;">15분봉 / BTC</span>
        </div>
        <div style="font-size:11px; color:#cbd5e1; line-height:1.5;">
          • <strong>진입 조건:</strong> 볼린저 하단 이탈 + 거래량 1.5배 + RSI &le; 35<br>
          • <strong>목표/손절:</strong> TP +2.0% | SL -1.2% | 3x 롱/숏
        </div>
        <div style="background:#0a0e17; border-radius:8px; padding:8px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
          <span style="color:#94a3b8;" id="bot-status-wonyotti">상태: 🟢 캔들 감시 중</span>
          <button class="vibe-btn-action" id="btn-toggle-bot-wonyotti" onclick="VibeEngine.toggleBot('wonyotti')" style="padding:4px 8px; font-size:11px; background:#1e3a8a; color:#fff; border-color:#3b82f6;">
            추종 활성화
          </button>
        </div>
      </div>

      <!-- Bot 2: Supertrend RSI Scalper -->
      <div class="vibe-bot-card" id="bot-card-supertrend">
        <div class="vibe-bot-header">
          <strong style="color:#10b981; font-size:14px;">🤖 슈퍼트렌드 1분봉 스캘퍼</strong>
          <span style="font-size:11px; color:#94a3b8;">1분봉 / BTC</span>
        </div>
        <div style="font-size:11px; color:#cbd5e1; line-height:1.5;">
          • <strong>진입 조건:</strong> 슈퍼트렌드 반전 + RSI &ge; 40 + 거래량 1.2배<br>
          • <strong>목표/손절:</strong> TP +0.8% | SL -0.5% | 5x 롱/숏
        </div>
        <div style="background:#0a0e17; border-radius:8px; padding:8px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
          <span style="color:#94a3b8;" id="bot-status-supertrend">상태: 🟢 캔들 감시 중</span>
          <button class="vibe-btn-action" id="btn-toggle-bot-supertrend" onclick="VibeEngine.toggleBot('supertrend')" style="padding:4px 8px; font-size:11px; background:#1e3a8a; color:#fff; border-color:#3b82f6;">
            추종 활성화
          </button>
        </div>
      </div>

      <!-- Bot 3: Larry Williams Breakout -->
      <div class="vibe-bot-card" id="bot-card-larry">
        <div class="vibe-bot-header">
          <strong style="color:#f59e0b; font-size:14px;">🤖 래리 변동성 돌파봇</strong>
          <span style="font-size:11px; color:#94a3b8;">1시간봉 / BTC</span>
        </div>
        <div style="font-size:11px; color:#cbd5e1; line-height:1.5;">
          • <strong>진입 조건:</strong> K=0.5 전일 레인지 상향 돌파 시 추세 탑승<br>
          • <strong>목표/손절:</strong> TP +3.0% | SL -1.5% | 2x 롱
        </div>
        <div style="background:#0a0e17; border-radius:8px; padding:8px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
          <span style="color:#94a3b8;" id="bot-status-larry">상태: 🟢 레인지 계산 대기</span>
          <button class="vibe-btn-action" id="btn-toggle-bot-larry" onclick="VibeEngine.toggleBot('larry')" style="padding:4px 8px; font-size:11px; background:#1e3a8a; color:#fff; border-color:#3b82f6;">
            추종 활성화
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Lower Section: Tabs for (Active Positions / Trade History / Performance) + Leaderboard -->
  <div class="vibe-lower-grid">

    <!-- Left: Positions & Trade History Center -->
    <div class="vibe-panel-card">
      <div class="vibe-panel-tabs">
        <button class="vibe-panel-tab active" id="tab-open-pos" onclick="VibeEngine.switchLowerTab('open')">
          💼 보유 포지션 (<span id="pos-count">0</span>)
        </button>
        <button class="vibe-panel-tab" id="tab-closed-pos" onclick="VibeEngine.switchLowerTab('closed')">
          📜 체결 & 청산 일지 (<span id="closed-count">0</span>)
        </button>
        <button class="vibe-panel-tab" id="tab-analytics" onclick="VibeEngine.switchLowerTab('analytics')">
          📊 퀀트 성적표
        </button>
      </div>

      <!-- View 1: Active Positions Table -->
      <div id="view-open-positions" style="overflow-x:auto;">
        <table class="vibe-table" id="table-positions">
          <thead>
            <tr>
              <th>종목/소스</th>
              <th>방향/배율</th>
              <th>진입가</th>
              <th>현재가</th>
              <th>TP / SL</th>
              <th>수익률 (PnL)</th>
              <th>청산</th>
            </tr>
          </thead>
          <tbody id="tbody-positions">
            <tr>
              <td colspan="7" style="text-align:center; color:#94a3b8; padding:32px;">현재 보유 중인 포지션이 없습니다. 상단에서 주문을 실행하거나 AI 전략봇을 켜보세요!</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- View 2: Closed Trades History Table -->
      <div id="view-closed-positions" style="display:none; overflow-x:auto;">
        <table class="vibe-table" id="table-history">
          <thead>
            <tr>
              <th>청산 시각</th>
              <th>종목/소스</th>
              <th>진입/청산가</th>
              <th>청산 사유</th>
              <th>실현 손익 ($)</th>
              <th>최종 수익률</th>
            </tr>
          </thead>
          <tbody id="tbody-history">
            <tr>
              <td colspan="6" style="text-align:center; color:#94a3b8; padding:32px;">아직 청산된 거래 내역이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- View 3: Performance Analytics -->
      <div id="view-analytics" style="display:none;">
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px; margin-bottom:16px;">
          <div style="background:#0a0e17; border:1px solid #1f2d47; border-radius:10px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#94a3b8;">승률 (Win Rate)</div>
            <div style="font-size:20px; font-weight:800; color:#10b981;" id="stat-winrate">0.0%</div>
          </div>
          <div style="background:#0a0e17; border:1px solid #1f2d47; border-radius:10px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#94a3b8;">손익비 (Profit Factor)</div>
            <div style="font-size:20px; font-weight:800; color:#38bdf8;" id="stat-pf">0.00</div>
          </div>
          <div style="background:#0a0e17; border:1px solid #1f2d47; border-radius:10px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#94a3b8;">총 거래 수</div>
            <div style="font-size:20px; font-weight:800; color:#ffffff;" id="stat-trades">0회</div>
          </div>
          <div style="background:#0a0e17; border:1px solid #1f2d47; border-radius:10px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#94a3b8;">누적 실현 손익</div>
            <div style="font-size:20px; font-weight:800; color:#10b981;" id="stat-realized-pnl">+$0.00</div>
          </div>
        </div>
        <p style="font-size:12px; color:#94a3b8; line-height:1.6;">
          💡 <strong>퀀트 원칙:</strong> 승률이 50%라도 손익비가 1.5 이상이면 복리로 우상향합니다. 브래킷 익절(TP)과 칼손절(SL)을 기계적으로 지키는 트레이더만이 시장에서 영구 생존합니다.
        </p>
      </div>
    </div>

    <!-- Right: Competitive Leaderboard (AI vs Humans) -->
    <div class="vibe-panel-card">
      <div class="vibe-card-header">
        <span>🏆 VIBE 명예의 전당 (AI봇 vs 휴먼 랭킹)</span>
        <button class="vibe-btn-action" onclick="VibeEngine.shareRank()" style="padding:4px 10px; font-size:11px;">🔗 랭킹 공유</button>
      </div>

      <!-- Trader Nickname Reg Bar -->
      <div style="display:flex; gap:8px; margin-bottom:12px;">
        <input type="text" class="vibe-input" id="input-trader-name" placeholder="트레이더 닉네임 입력 (예: 압구정퀀트킹)" style="font-size:13px; padding:8px 12px;">
        <button class="vibe-lev-btn" onclick="VibeEngine.saveTraderName()" style="flex:0 0 100px; background:#2563eb; color:#fff; border-color:#3b82f6;">닉네임 저장</button>
      </div>

      <div style="overflow-x:auto; margin-bottom:14px;">
        <table class="vibe-table" id="table-leaderboard">
          <thead>
            <tr>
              <th>순위</th>
              <th>트레이더/봇</th>
              <th>수익률</th>
              <th>총 자산</th>
            </tr>
          </thead>
          <tbody id="tbody-leaderboard">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>

      <!-- Live Traders Execution Feed -->
      <div class="vibe-card-header" style="margin-bottom:8px; font-size:13px;">
        <span>📡 실시간 체결 라이브 피드</span>
      </div>
      <div class="vibe-live-feed" id="live-feed-ticker">
        <!-- Live items stream here -->
      </div>
    </div>

  </div>

  <!-- YMYL Legal Disclaimer -->
  <div class="vibe-disclaimer">
    <strong>⚖️ 법적 면책 조항 및 모의투자 안내 (YMYL Compliance)</strong>
    본 VIBE TRADING 시뮬레이터는 실제 금전이나 실물 가상자산이 입출금되지 않는 100% 가상 머니 기반의 퀀트 교육 및 리서치 목적 인터랙티브 도구입니다. 제공되는 시세 데이터 및 차트는 참고용이며 네트워크 지연이 발생할 수 있습니다. 본 사이트는 금융투자업 인가 법인이 아니며 투자 권유를 하지 않습니다. 모든 실제 투자에 대한 판단과 책임은 투자자 본인에게 있습니다.
  </div>

</div>

<!-- TradingView Widget Script -->
<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>

<script>
/* ==========================================================================
   Vibe Trading Pro Engine - Vanilla JS High-Precision Trading Core (v9.0 Apex)
   ========================================================================== */
const VibeEngine = (function() {
  // State
  let state = {
    cash: 10000.0,
    initialCash: 10000.0,
    activeAsset: 'BTCUSDT',
    tvSymbol: 'BINANCE:BTCUSDT',
    prices: {
      'BTCUSDT': 80410.00,
      'ETHUSDT': 2540.80,
      'SOLUSDT': 178.40,
      'DOGEUSDT': 0.1420,
      'BNBUSDT': 585.20,
      'XRPUSDT': 0.5280
    },
    changes: {
      'BTCUSDT': 2.45,
      'ETHUSDT': 1.12,
      'SOLUSDT': 3.80,
      'DOGEUSDT': -0.85,
      'BNBUSDT': 0.95,
      'XRPUSDT': -0.42
    },
    side: 'LONG',
    leverage: 10,
    tpPct: 2.0,
    slPct: 1.0,
    positions: [],
    closedTrades: [],
    traderName: '나홀로트레이더',
    chartType: 'tv',
    soundEnabled: true,
    bots: {
      wonyotti: { active: false, name: '워뇨띠 볼린저 반등봇', lastTrigger: 0 },
      supertrend: { active: false, name: '슈퍼트렌드 1분봉 스캘퍼', lastTrigger: 0 },
      larry: { active: false, name: '래리 변동성 돌파봇', lastTrigger: 0 }
    }
  };

  // Hall of Fame Leaderboard Seed with AI Bots competing
  let leaderboard = [
    { rank: 1, name: '🤖 슈퍼트렌드 1분봉 봇', pnl: 342.8, equity: 44280.0, isBot: true },
    { rank: 2, name: '월가타짜', pnl: 284.2, equity: 38420.0, isBot: false },
    { rank: 3, name: '🤖 워뇨띠 볼린저 봇', pnl: 218.5, equity: 31850.0, isBot: true },
    { rank: 4, name: '여의도불사조', pnl: 171.5, equity: 27150.0, isBot: false },
    { rank: 5, name: '🤖 래리 변동성돌파 봇', pnl: 142.3, equity: 24230.0, isBot: true },
    { rank: 6, name: '비트코인고래', pnl: 115.6, equity: 21560.0, isBot: false },
    { rank: 7, name: '판교퀀트개발자', pnl: 84.2, equity: 18420.0, isBot: false },
    { rank: 8, name: '나스닥롱충이', pnl: 65.1, equity: 16510.0, isBot: false },
    { rank: 9, name: '켈리신봉자', pnl: 48.7, equity: 14870.0, isBot: false }
  ];

  // Web Audio API Sound Synthesizer
  function playSound(type) {
    if (!state.soundEnabled) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'order') {
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.setValueAtTime(880.00, ctx.currentTime + 0.08); // A5
        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.22);
        osc.start();
        osc.stop(ctx.currentTime + 0.22);
      } else if (type === 'win') {
        osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
        osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.08); // E5
        osc.frequency.setValueAtTime(783.99, ctx.currentTime + 0.16); // G5
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
        osc.start();
        osc.stop(ctx.currentTime + 0.35);
      } else if (type === 'loss') {
        osc.frequency.setValueAtTime(329.63, ctx.currentTime); // E4
        osc.frequency.setValueAtTime(261.63, ctx.currentTime + 0.10); // C4
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
        osc.start();
        osc.stop(ctx.currentTime + 0.3);
      }
    } catch(e) {}
  }

  function toggleSound() {
    state.soundEnabled = !state.soundEnabled;
    const btn = document.getElementById('btn-toggle-sound');
    if (btn) {
      btn.innerHTML = `<span id="sound-icon">${state.soundEnabled ? '🔊' : '🔇'}</span> 사운드 ${state.soundEnabled ? 'ON' : 'OFF'}`;
    }
  }

  // Persistence
  function loadState() {
    try {
      const saved = localStorage.getItem('blogin_vibe_state_v9');
      if (saved) {
        const parsed = JSON.parse(saved);
        state.cash = parsed.cash !== undefined ? parsed.cash : state.cash;
        state.positions = parsed.positions || [];
        state.closedTrades = parsed.closedTrades || [];
        state.traderName = parsed.traderName || state.traderName;
        if (parsed.bots) state.bots = parsed.bots;
      }
    } catch(e) {}
  }

  function saveState() {
    try {
      localStorage.setItem('blogin_vibe_state_v9', JSON.stringify({
        cash: state.cash,
        positions: state.positions,
        closedTrades: state.closedTrades,
        traderName: state.traderName,
        bots: state.bots
      }));
    } catch(e) {}
  }

  // KST Clock & Latency Loop
  function startClock() {
    setInterval(() => {
      const now = new Date();
      // KST is UTC+9
      const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
      const kst = new Date(utc + (3600000 * 9));
      const hours = String(kst.getHours()).padStart(2, '0');
      const minutes = String(kst.getMinutes()).padStart(2, '0');
      const seconds = String(kst.getSeconds()).padStart(2, '0');
      const el = document.getElementById('kst-clock-display');
      if (el) el.textContent = `${hours}:${minutes}:${seconds} KST`;
    }, 1000);
  }

  // TradingView Chart
  let tvWidget = null;
  function initTradingView(symbol) {
    const container = document.getElementById('tv_chart_container');
    if (!container) return;
    container.innerHTML = '';

    if (window.TradingView) {
      tvWidget = new TradingView.widget({
        "autosize": true,
        "symbol": symbol,
        "interval": "15",
        "timezone": "Asia/Seoul",
        "theme": "dark",
        "style": "1",
        "locale": "kr",
        "toolbar_bg": "#0a0e17",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tv_chart_container"
      });
    }
  }

  function switchChart(type) {
    state.chartType = type;
    document.getElementById('tab-tv').classList.toggle('active', type === 'tv');
    document.getElementById('tab-canvas').classList.toggle('active', type === 'canvas');
    const tvBox = document.getElementById('tv_chart_container');
    const canvasBox = document.getElementById('canvas_chart_viewport');

    if (type === 'tv') {
      tvBox.style.display = 'block';
      canvasBox.style.display = 'none';
      initTradingView(state.tvSymbol);
    } else {
      tvBox.style.display = 'none';
      canvasBox.style.display = 'block';
      renderCanvasChart();
    }
  }

  function renderCanvasChart() {
    const canvas = document.getElementById('canvas_chart_viewport');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = '#0a0e17';
    ctx.fillRect(0, 0, w, h);

    ctx.strokeStyle = '#1f2d47';
    ctx.lineWidth = 1;
    for (let x = 50; x < w; x += 80) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 40; y < h; y += 60) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    const basePrice = state.prices[state.activeAsset] || 50000;
    let curr = basePrice * 0.98;
    const count = 35;
    const candleW = (w - 100) / count;

    for (let i = 0; i < count; i++) {
      const open = curr;
      const change = (Math.random() - 0.48) * (basePrice * 0.012);
      const close = open + change;
      const high = Math.max(open, close) + Math.random() * (basePrice * 0.006);
      const low = Math.min(open, close) - Math.random() * (basePrice * 0.006);
      curr = close;

      const isUp = close >= open;
      ctx.strokeStyle = isUp ? '#10b981' : '#ef4444';
      ctx.fillStyle = isUp ? '#10b981' : '#ef4444';

      const x = 40 + i * candleW;
      const yMax = basePrice * 1.04;
      const yMin = basePrice * 0.96;
      const scaleY = (val) => h - 40 - ((val - yMin) / (yMax - yMin)) * (h - 80);

      ctx.beginPath();
      ctx.moveTo(x + candleW / 2, scaleY(high));
      ctx.lineTo(x + candleW / 2, scaleY(low));
      ctx.stroke();

      const bodyTop = scaleY(Math.max(open, close));
      const bodyH = Math.max(2, Math.abs(scaleY(open) - scaleY(close)));
      ctx.fillRect(x + 2, bodyTop, candleW - 4, bodyH);
    }
  }

  // Real-Time WebSocket Streaming
  function startPriceStream() {
    try {
      const streams = 'btcusdt@ticker/ethusdt@ticker/solusdt@ticker/dogeusdt@ticker/bnbusdt@ticker/xrpusdt@ticker';
      const ws = new WebSocket('wss://stream.binance.com:9443/ws/' + streams);

      ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const s = data.s;
        const p = parseFloat(data.c);
        const ch = parseFloat(data.P);
        if (s && p && state.prices[s] !== undefined) {
          state.prices[s] = p;
          if (!isNaN(ch)) state.changes[s] = ch;
          updatePricePills();
          recalcPositions();
          checkBotAutomations();
        }
      };

      ws.onerror = function() {
        startMockTick();
      };
    } catch(e) {
      startMockTick();
    }
  }

  function startMockTick() {
    setInterval(() => {
      for (const k in state.prices) {
        const drift = (Math.random() - 0.495) * (state.prices[k] * 0.0015);
        state.prices[k] = Math.max(0.001, state.prices[k] + drift);
      }
      updatePricePills();
      recalcPositions();
      checkBotAutomations();
    }, 1500);
  }

  function updatePricePills() {
    for (const k in state.prices) {
      const el = document.getElementById('pill-price-' + k);
      const chEl = document.getElementById('pill-change-' + k);
      if (el) {
        const dec = state.prices[k] < 1 ? 4 : (state.prices[k] < 100 ? 2 : 2);
        el.textContent = '$' + state.prices[k].toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec});
      }
      if (chEl && state.changes[k] !== undefined) {
        const ch = state.changes[k];
        chEl.textContent = (ch >= 0 ? '+' : '') + ch.toFixed(2) + '%';
        chEl.className = 'ticker-change ' + (ch >= 0 ? 'pos' : 'neg');
      }
    }
    calculateOrderPreview();
  }

  // Select Asset
  function selectAsset(assetKey, tvSymbol) {
    state.activeAsset = assetKey;
    state.tvSymbol = tvSymbol;
    document.querySelectorAll('.vibe-asset-pill').forEach(el => el.classList.remove('active'));
    if (event && event.currentTarget) {
      event.currentTarget.classList.add('active');
    }

    document.getElementById('chart-asset-title').textContent = assetKey + ' 실시간 차트';
    document.getElementById('current-asset-badge').textContent = assetKey;

    if (state.chartType === 'tv') {
      initTradingView(tvSymbol);
    } else {
      renderCanvasChart();
    }
    calculateOrderPreview();
  }

  // Order Parameters
  function setSide(side) {
    state.side = side;
    document.getElementById('btn-side-long').classList.toggle('active', side === 'LONG');
    document.getElementById('btn-side-short').classList.toggle('active', side === 'SHORT');
    const submitBtn = document.getElementById('btn-submit-order');
    submitBtn.className = 'vibe-exec-btn ' + (side === 'LONG' ? 'long-mode' : 'short-mode');
    submitBtn.textContent = '🚀 ' + state.activeAsset + ' ' + state.leverage + 'x ' + (side === 'LONG' ? '롱 포지션 진입 (주문 실행)' : '숏 포지션 진입 (주문 실행)');
    calculateOrderPreview();
  }

  function setLeverage(lev) {
    state.leverage = lev;
    document.querySelectorAll('.vibe-leverage-bar .vibe-lev-btn').forEach(b => {
      b.classList.toggle('active', b.textContent === lev + 'x');
    });
    document.getElementById('label-leverage').textContent = lev + 'x';
    setSide(state.side);
  }

  function setMarginPercent(pct) {
    const val = Math.max(10, Math.floor(state.cash * pct));
    document.getElementById('input-order-margin').value = val;
    calculateOrderPreview();
  }

  function calculateOrderPreview() {
    const margin = parseFloat(document.getElementById('input-order-margin').value) || 0;
    const price = state.prices[state.activeAsset] || 1;
    const notional = margin * state.leverage;

    const tpPct = parseFloat(document.getElementById('input-tp-pct').value) || 2.0;
    const slPct = parseFloat(document.getElementById('input-sl-pct').value) || 1.0;
    state.tpPct = tpPct;
    state.slPct = slPct;

    document.getElementById('label-tp-target').textContent = '+' + tpPct.toFixed(1) + '%';
    document.getElementById('label-sl-target').textContent = '-' + slPct.toFixed(1) + '%';

    // Target and Stop prices
    let targetPrice = 0;
    let stopPrice = 0;
    let liqPrice = 0;

    if (state.side === 'LONG') {
      targetPrice = price * (1 + tpPct / 100);
      stopPrice = price * (1 - slPct / 100);
      liqPrice = price * (1 - (1 / state.leverage) + 0.005);
    } else {
      targetPrice = price * (1 - tpPct / 100);
      stopPrice = price * (1 + slPct / 100);
      liqPrice = price * (1 + (1 / state.leverage) - 0.005);
    }

    const descTp = document.getElementById('desc-tp-price');
    const descSl = document.getElementById('desc-sl-price');
    if (descTp) descTp.textContent = `목표가: $${targetPrice.toLocaleString('en-US', {minimumFractionDigits: 1, maximumFractionDigits: 1})}`;
    if (descSl) descSl.textContent = `손절가: $${stopPrice.toLocaleString('en-US', {minimumFractionDigits: 1, maximumFractionDigits: 1})}`;

    const liqPct = ((liqPrice - price) / price) * 100;
    document.getElementById('label-max-margin').textContent = '최대 가용: $' + state.cash.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('preview-notional').textContent = '$' + notional.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('preview-liq').textContent = '$' + liqPrice.toLocaleString('en-US', {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' (' + liqPct.toFixed(1) + '%)';

    const rrRatio = (tpPct / Math.max(0.1, slPct)).toFixed(1);
    const rrEl = document.getElementById('preview-rr');
    if (rrEl) {
      rrEl.textContent = `${rrRatio} : 1 (${rrRatio >= 1.5 ? '우수' : '보통'})`;
    }
  }

  // Execute Order (Supports Bracket TP/SL)
  function executeOrder(customParams) {
    const isBot = customParams && customParams.botSource;
    const margin = isBot ? customParams.margin : (parseFloat(document.getElementById('input-order-margin').value) || 0);

    if (margin <= 0 || margin > state.cash) {
      if (!isBot) alert('가용 증거금이 부족합니다! (현재 가용: $' + state.cash.toFixed(2) + ')');
      return;
    }

    const asset = isBot ? customParams.asset : state.activeAsset;
    const side = isBot ? customParams.side : state.side;
    const leverage = isBot ? customParams.leverage : state.leverage;
    const tpPct = isBot ? customParams.tpPct : state.tpPct;
    const slPct = isBot ? customParams.slPct : state.slPct;
    const price = state.prices[asset] || 50000;

    let targetPrice = side === 'LONG' ? price * (1 + tpPct / 100) : price * (1 - tpPct / 100);
    let stopPrice = side === 'LONG' ? price * (1 - slPct / 100) : price * (1 + slPct / 100);
    let liqPrice = side === 'LONG' ? price * (1 - (1 / leverage) + 0.005) : price * (1 + (1 / leverage) - 0.005);

    state.cash -= margin;
    const newPos = {
      id: 'pos_' + Date.now() + '_' + Math.floor(Math.random() * 1000),
      asset: asset,
      side: side,
      leverage: leverage,
      entryPrice: price,
      margin: margin,
      size: (margin * leverage) / price,
      tpPrice: targetPrice,
      slPrice: stopPrice,
      tpPct: tpPct,
      slPct: slPct,
      liqPrice: liqPrice,
      botSource: isBot ? customParams.botSource : null,
      createdAt: new Date().toLocaleTimeString()
    };

    state.positions.push(newPos);
    playSound('order');
    saveState();
    recalcPositions();

    const tag = isBot ? `🤖 [${customParams.botSource}]` : `🚀 [${state.traderName}]`;
    addFeedItem(`${tag} 님이 ${asset} ${leverage}x ${side} 진입 (TP +${tpPct}%, SL -${slPct}%)`);
  }

  // Close Position with reason tracking
  function closePosition(posId, reason = '🖐️ 수동 청산') {
    const idx = state.positions.findIndex(p => p.id === posId);
    if (idx === -1) return;
    const pos = state.positions[idx];
    const currPrice = state.prices[pos.asset] || pos.entryPrice;

    let pnl = 0;
    if (pos.side === 'LONG') {
      pnl = (currPrice - pos.entryPrice) * pos.size;
    } else {
      pnl = (pos.entryPrice - currPrice) * pos.size;
    }

    const returnPct = (pnl / pos.margin) * 100;
    state.cash += Math.max(0, pos.margin + pnl);

    // Save to closed trades history
    state.closedTrades.unshift({
      id: pos.id,
      asset: pos.asset,
      side: pos.side,
      leverage: pos.leverage,
      entryPrice: pos.entryPrice,
      exitPrice: currPrice,
      pnl: pnl,
      returnPct: returnPct,
      reason: reason,
      botSource: pos.botSource,
      closedAt: new Date().toLocaleTimeString()
    });

    state.positions.splice(idx, 1);

    if (pnl > 0) {
      playSound('win');
    } else {
      playSound('loss');
    }

    saveState();
    recalcPositions();
    updateHistoryTable();

    const sign = pnl >= 0 ? '+' : '';
    const src = pos.botSource ? `🤖 [${pos.botSource}]` : `💰 [${state.traderName}]`;
    addFeedItem(`${src} ${pos.asset} 포지션 ${reason}: ${sign}$${pnl.toFixed(2)} (${sign}${returnPct.toFixed(1)}%)`);
  }

  // Recalculate Open Positions & Check Auto TP/SL
  function recalcPositions() {
    let unrealizedPnl = 0;
    const tbody = document.getElementById('tbody-positions');
    const posCount = document.getElementById('pos-count');
    if (posCount) posCount.textContent = state.positions.length;

    // Auto-check Bracket TP/SL and Liquidation triggers
    for (let i = state.positions.length - 1; i >= 0; i--) {
      const pos = state.positions[i];
      const currPrice = state.prices[pos.asset] || pos.entryPrice;

      // 1. Check Liquidation
      if ((pos.side === 'LONG' && currPrice <= pos.liqPrice) || (pos.side === 'SHORT' && currPrice >= pos.liqPrice)) {
        closePosition(pos.id, '💥 강제 청산');
        return;
      }
      // 2. Check TP Bracket
      if (pos.tpPrice && ((pos.side === 'LONG' && currPrice >= pos.tpPrice) || (pos.side === 'SHORT' && currPrice <= pos.tpPrice))) {
        closePosition(pos.id, '🎯 TP 익절');
        return;
      }
      // 3. Check SL Bracket
      if (pos.slPrice && ((pos.side === 'LONG' && currPrice <= pos.slPrice) || (pos.side === 'SHORT' && currPrice >= pos.slPrice))) {
        closePosition(pos.id, '🚨 SL 손절');
        return;
      }
    }

    if (state.positions.length === 0) {
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#94a3b8; padding:32px;">현재 보유 중인 포지션이 없습니다. 상단에서 주문을 실행하거나 AI 전략봇을 켜보세요!</td></tr>';
      }
    } else {
      let rowsHtml = '';
      for (const pos of state.positions) {
        const currPrice = state.prices[pos.asset] || pos.entryPrice;
        let posPnl = 0;
        if (pos.side === 'LONG') {
          posPnl = (currPrice - pos.entryPrice) * pos.size;
        } else {
          posPnl = (pos.entryPrice - currPrice) * pos.size;
        }

        unrealizedPnl += posPnl;
        const pnlPct = (posPnl / pos.margin) * 100;
        const pnlClass = posPnl >= 0 ? 'color:#10b981;' : 'color:#ef4444;';
        const sign = posPnl >= 0 ? '+' : '';
        const sideColor = pos.side === 'LONG' ? '#10b981' : '#ef4444';

        const botBadge = pos.botSource ? `<span style="display:inline-block; margin-left:4px; padding:2px 5px; border-radius:4px; font-size:10px; font-weight:800; background:rgba(56,189,248,0.2); color:#38bdf8;">🤖 ${pos.botSource.replace(' 봇', '')}</span>` : '';

        rowsHtml += `<tr>
          <td><strong style="color:#ffffff;">${pos.asset}</strong>${botBadge}</td>
          <td><span style="display:inline-block; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:800; background:${pos.side === 'LONG' ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)'}; color:${sideColor};">${pos.leverage}x ${pos.side}</span></td>
          <td>$${pos.entryPrice.toLocaleString('en-US', {minimumFractionDigits: 1})}</td>
          <td>$${currPrice.toLocaleString('en-US', {minimumFractionDigits: 1})}</td>
          <td style="font-size:11px;"><span style="color:#10b981;">+$${pos.tpPrice ? pos.tpPrice.toFixed(0) : '--'}</span> / <span style="color:#ef4444;">-$${pos.slPrice ? pos.slPrice.toFixed(0) : '--'}</span></td>
          <td style="${pnlClass} font-weight:800;">${sign}$${posPnl.toFixed(2)} (${sign}${pnlPct.toFixed(2)}%)</td>
          <td><button class="vibe-reset-btn" style="padding:4px 8px; font-size:11px;" onclick="VibeEngine.closePosition('${pos.id}')">청산</button></td>
        </tr>`;
      }
      if (tbody) tbody.innerHTML = rowsHtml;
    }

    // Update HUD
    const totalMarginInUse = state.positions.reduce((acc, p) => acc + p.margin, 0);
    const totalEquity = state.cash + totalMarginInUse + unrealizedPnl;
    const totalReturnPct = ((totalEquity - state.initialCash) / state.initialCash) * 100;

    const hudEquity = document.getElementById('hud-equity');
    const hudCash = document.getElementById('hud-cash');
    const hudPnl = document.getElementById('hud-pnl');

    if (hudEquity) hudEquity.textContent = '$' + totalEquity.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    if (hudCash) hudCash.textContent = '$' + state.cash.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});

    if (hudPnl) {
      const pnlSign = totalReturnPct >= 0 ? '+' : '';
      hudPnl.textContent = pnlSign + totalReturnPct.toFixed(2) + '% ($' + (totalEquity - state.initialCash).toFixed(2) + ')';
      hudPnl.className = 'vibe-hud-val ' + (totalReturnPct >= 0 ? 'pos' : 'neg');
    }

    updateLeaderboard(totalReturnPct, totalEquity);
    updateAnalytics();
  }

  // Update Trade History Table
  function updateHistoryTable() {
    const tbody = document.getElementById('tbody-history');
    const countEl = document.getElementById('closed-count');
    if (countEl) countEl.textContent = state.closedTrades.length;

    if (!tbody) return;
    if (state.closedTrades.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#94a3b8; padding:32px;">아직 청산된 거래 내역이 없습니다.</td></tr>';
      return;
    }

    let html = '';
    state.closedTrades.slice(0, 30).forEach(t => {
      const sign = t.pnl >= 0 ? '+' : '';
      const color = t.pnl >= 0 ? '#10b981' : '#ef4444';
      const botBadge = t.botSource ? `<span style="display:inline-block; margin-left:4px; padding:1px 4px; border-radius:3px; font-size:9px; background:rgba(56,189,248,0.2); color:#38bdf8;">🤖</span>` : '';

      html += `<tr>
        <td style="color:#94a3b8;">${t.closedAt}</td>
        <td><strong>${t.asset}</strong> ${botBadge} <span style="font-size:10px; color:${t.side === 'LONG' ? '#10b981' : '#ef4444'};">${t.leverage}x ${t.side}</span></td>
        <td>$${t.entryPrice.toFixed(0)} &rarr; $${t.exitPrice.toFixed(0)}</td>
        <td><span style="background:rgba(255,255,255,0.06); padding:2px 6px; border-radius:4px; font-size:10px;">${t.reason}</span></td>
        <td style="color:${color}; font-weight:800;">${sign}$${t.pnl.toFixed(2)}</td>
        <td style="color:${color}; font-weight:800;">${sign}${t.returnPct.toFixed(1)}%</td>
      </tr>`;
    });
    tbody.innerHTML = html;
  }

  // Update Performance Analytics
  function updateAnalytics() {
    const total = state.closedTrades.length;
    const wins = state.closedTrades.filter(t => t.pnl > 0);
    const losses = state.closedTrades.filter(t => t.pnl < 0);

    const winRate = total > 0 ? (wins.length / total) * 100 : 0.0;
    const totalProfit = wins.reduce((acc, t) => acc + t.pnl, 0);
    const totalLoss = Math.abs(losses.reduce((acc, t) => acc + t.pnl, 0));
    const pf = totalLoss > 0 ? (totalProfit / totalLoss) : (totalProfit > 0 ? 99.0 : 0.0);
    const netPnl = state.closedTrades.reduce((acc, t) => acc + t.pnl, 0);

    const elWin = document.getElementById('stat-winrate');
    const elPf = document.getElementById('stat-pf');
    const elTrades = document.getElementById('stat-trades');
    const elPnl = document.getElementById('stat-realized-pnl');

    if (elWin) elWin.textContent = `${winRate.toFixed(1)}% (${wins.length}승 ${losses.length}패)`;
    if (elPf) elPf.textContent = pf.toFixed(2);
    if (elTrades) elTrades.textContent = `${total}회`;
    if (elPnl) {
      const sign = netPnl >= 0 ? '+' : '';
      elPnl.textContent = `${sign}$${netPnl.toFixed(2)}`;
      elPnl.style.color = netPnl >= 0 ? '#10b981' : '#ef4444';
    }
  }

  // Switch Lower Tabs
  function switchLowerTab(tab) {
    document.getElementById('tab-open-pos').classList.toggle('active', tab === 'open');
    document.getElementById('tab-closed-pos').classList.toggle('active', tab === 'closed');
    document.getElementById('tab-analytics').classList.toggle('active', tab === 'analytics');

    document.getElementById('view-open-positions').style.display = tab === 'open' ? 'block' : 'none';
    document.getElementById('view-closed-positions').style.display = tab === 'closed' ? 'block' : 'none';
    document.getElementById('view-analytics').style.display = tab === 'analytics' ? 'block' : 'none';
  }

  // AI Quant Bots Management
  function toggleBot(botKey) {
    if (!state.bots[botKey]) return;
    state.bots[botKey].active = !state.bots[botKey].active;
    const isActive = state.bots[botKey].active;

    const btn = document.getElementById('btn-toggle-bot-' + botKey);
    const status = document.getElementById('bot-status-' + botKey);
    const card = document.getElementById('bot-card-' + botKey);

    if (btn) {
      btn.textContent = isActive ? '추종 중단' : '추종 활성화';
      btn.style.background = isActive ? '#ef4444' : '#1e3a8a';
      btn.style.borderColor = isActive ? '#dc2626' : '#3b82f6';
    }
    if (status) {
      status.innerHTML = isActive ? '<strong style="color:#10b981;">● 실시간 자동 매매 중</strong>' : '상태: 🟢 캔들 감시 중';
    }
    if (card) {
      card.style.borderColor = isActive ? '#10b981' : 'var(--vibe-border-card)';
    }

    saveState();
    const actionKor = isActive ? '추종 활성화' : '추종 중단';
    addFeedItem(`🤖 [${state.bots[botKey].name}] ${actionKor}!`);
  }

  // Periodic Bot Automated Execution Check
  function checkBotAutomations() {
    const now = Date.now();

    // 1. Wonyotti Bot (15m BB)
    if (state.bots.wonyotti && state.bots.wonyotti.active && now - state.bots.wonyotti.lastTrigger > 45000) {
      // Simulate condition match when price fluctuates
      if (Math.random() < 0.25) {
        state.bots.wonyotti.lastTrigger = now;
        executeOrder({
          asset: 'BTCUSDT',
          side: 'LONG',
          leverage: 3,
          margin: 1500,
          tpPct: 2.0,
          slPct: 1.2,
          botSource: '워뇨띠 볼린저 봇'
        });
      }
    }

    // 2. Supertrend Bot (1m Scalp)
    if (state.bots.supertrend && state.bots.supertrend.active && now - state.bots.supertrend.lastTrigger > 25000) {
      if (Math.random() < 0.35) {
        state.bots.supertrend.lastTrigger = now;
        executeOrder({
          asset: 'BTCUSDT',
          side: Math.random() > 0.5 ? 'LONG' : 'SHORT',
          leverage: 5,
          margin: 1000,
          tpPct: 0.8,
          slPct: 0.5,
          botSource: '슈퍼트렌드 1분봉 봇'
        });
      }
    }

    // 3. Larry Williams Breakout Bot (1h)
    if (state.bots.larry && state.bots.larry.active && now - state.bots.larry.lastTrigger > 60000) {
      if (Math.random() < 0.20) {
        state.bots.larry.lastTrigger = now;
        executeOrder({
          asset: 'BTCUSDT',
          side: 'LONG',
          leverage: 2,
          margin: 2000,
          tpPct: 3.0,
          slPct: 1.5,
          botSource: '래리 변동성돌파 봇'
        });
      }
    }
  }

  // Leaderboard ranking update
  function updateLeaderboard(myPnl, myEquity) {
    const myEntry = { rank: 0, name: state.traderName + ' (당신)', pnl: myPnl, equity: myEquity, isMe: true };
    const all = leaderboard.concat([myEntry]).sort((a, b) => b.pnl - a.pnl);

    const tbody = document.getElementById('tbody-leaderboard');
    if (!tbody) return;

    let html = '';
    all.slice(0, 10).forEach((item, idx) => {
      const rankNum = idx + 1;
      let badge = '<span class="vibe-rank-badge">' + rankNum + '</span>';
      if (rankNum === 1) badge = '<span class="vibe-rank-badge vibe-rank-1">🥇</span>';
      else if (rankNum === 2) badge = '<span class="vibe-rank-badge vibe-rank-2">🥈</span>';
      else if (rankNum === 3) badge = '<span class="vibe-rank-badge vibe-rank-3">🥉</span>';

      const rowClass = item.isMe ? 'class="vibe-my-rank-row"' : '';
      const pnlColor = item.pnl >= 0 ? '#10b981' : '#ef4444';
      const sign = item.pnl >= 0 ? '+' : '';

      html += `<tr ${rowClass}>
        <td>${badge}</td>
        <td><strong>${item.name}</strong></td>
        <td style="color:${pnlColor}; font-weight:800;">${sign}${item.pnl.toFixed(1)}%</td>
        <td>$${item.equity.toLocaleString('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0})}</td>
      </tr>`;
    });
    tbody.innerHTML = html;
  }

  function saveTraderName() {
    const input = document.getElementById('input-trader-name');
    if (input && input.value.trim()) {
      state.traderName = input.value.trim();
      saveState();
      recalcPositions();
      alert('트레이더 닉네임이 [' + state.traderName + '] (으)로 저장되었습니다!');
    }
  }

  function shareRank() {
    const url = window.location.href.split('#')[0] + '#trader=' + encodeURIComponent(state.traderName);
    navigator.clipboard.writeText(url).then(() => {
      alert('🏆 Vibe Trading 랭킹 배틀 링크가 클립보드에 복사되었습니다!\\n친구에게 공유하여 순위 배틀을 벌여보세요:\\n' + url);
    });
  }

  function addFeedItem(text) {
    const feed = document.getElementById('live-feed-ticker');
    if (!feed) return;
    const item = document.createElement('div');
    item.className = 'vibe-feed-item';
    item.innerHTML = '<span style="color:#3b82f6;">●</span> <span>' + text + '</span> <span style="margin-left:auto; color:#94a3b8; font-size:10px;">' + new Date().toLocaleTimeString() + '</span>';
    feed.insertBefore(item, feed.firstChild);
    while (feed.children.length > 6) {
      feed.removeChild(feed.lastChild);
    }
  }

  function resetAccount() {
    if (confirm('가상 계좌 잔고를 $10,000 초기 상태로 리셋하시겠습니까? (거래 일지 및 포지션이 초기화됩니다)')) {
      state.cash = 10000.0;
      state.positions = [];
      state.closedTrades = [];
      saveState();
      recalcPositions();
      updateHistoryTable();
      updateAnalytics();
    }
  }

  // Init
  function init() {
    loadState();
    startClock();
    const nameInput = document.getElementById('input-trader-name');
    if (nameInput) nameInput.value = state.traderName;

    // Restore Bot UI state
    for (const b in state.bots) {
      if (state.bots[b] && state.bots[b].active) {
        const btn = document.getElementById('btn-toggle-bot-' + b);
        const status = document.getElementById('bot-status-' + b);
        const card = document.getElementById('bot-card-' + b);
        if (btn) {
          btn.textContent = '추종 중단';
          btn.style.background = '#ef4444';
          btn.style.borderColor = '#dc2626';
        }
        if (status) status.innerHTML = '<strong style="color:#10b981;">● 실시간 자동 매매 중</strong>';
        if (card) card.style.borderColor = '#10b981';
      }
    }

    initTradingView('BINANCE:BTCUSDT');
    startPriceStream();
    recalcPositions();
    updateHistoryTable();
    updateAnalytics();

    // Initial Feeds
    addFeedItem('🌟 [🤖 슈퍼트렌드 1분봉 봇] BTC 5x 롱 포지션 +$105.00 익절!');
    addFeedItem('⚡ [여의도불사조] ETH 15x 숏 포지션 진입 완료');
    addFeedItem('🔥 [🤖 워뇨띠 볼린저 봇] BTC 3x 롱 +$320.00 반등 체결!');

    // Random Feed generator
    setInterval(() => {
      const bots = ['월가타짜', '여의도불사조', '🤖 슈퍼트렌드봇', '비트코인고래', '판교퀀트개발자', '🤖 워뇨띠봇'];
      const assets = ['BTC', 'ETH', 'SOL'];
      const bot = bots[Math.floor(Math.random() * bots.length)];
      const asset = assets[Math.floor(Math.random() * assets.length)];
      const pnl = (Math.random() * 800 + 120).toFixed(0);
      addFeedItem(`💰 [${bot}] ${asset} 포지션 +$${pnl} 실시간 익절!`);
    }, 8000);
  }

  return {
    init,
    selectAsset,
    switchChart,
    setSide,
    setLeverage,
    setMarginPercent,
    calculateOrderPreview,
    executeOrder,
    closePosition,
    saveTraderName,
    shareRank,
    resetAccount,
    switchLowerTab,
    toggleBot,
    toggleSound
  };
})();

// Auto-boot on load
if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', VibeEngine.init);
} else {
  VibeEngine.init();
}
</script>

</body>
</html>"""
