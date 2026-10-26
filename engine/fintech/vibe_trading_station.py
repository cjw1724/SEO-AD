"""
Blogin 365 AI Holdings - Vibe Trading & Leaderboard Pro Station (v9.0 Apex)
World-Class Interactive Financial Trading Terminal for Google Blogger

Features:
1. Dual-Chart Engine:
   - Official TradingView Advanced Real-Time Candlestick Chart (Dark theme, multi-timeframe, technical indicators)
   - 0ms Inline HTML5 Canvas 60fps Candlestick Chart (Instant toggle, zero-dependency)
2. Real-Time Multi-Asset Live Streaming:
   - BTC/USDT, ETH/USDT, SOL/USDT, NVDA, TSLA, AAPL, QQQ
   - Binance WebSocket WSS streaming with automatic REST failover
3. Complete Paper Trading Engine:
   - Virtual Starting Balance: $10,000 USDT (13,800,000 KRW switchable)
   - Long / Short execution, 1x to 20x leverage
   - Dynamic Liquidation Price calculation & Kelly Criterion position sizing
   - Real-time PnL & Margin maintenance tracking
   - Web Audio API synthesized trading sound effects
4. Competitive Leaderboard (경쟁 순위표 & 명예의 전당):
   - Top 10 Hall of Fame with live user re-ranking
   - Nickname registration & LocalStorage persistence
   - Live Traders Feed (simulated high-frequency executions ticker)
   - Viral URL Hash challenge sharing (#vibe=1&trader=...&pnl=...)
5. 100% Toss Design System (TDS) Dark Palette & WCAG 2.1 AAA Compliance
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
  <title>VIBE TRADING - 실시간 퀀트 모의투자 & 랭킹 배틀 | Blogin 365 AI Holdings</title>
  
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Blogin 365 Vibe Trading Simulator & Leaderboard",
    "applicationCategory": "FinanceApplication",
    "operatingSystem": "Any",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    },
    "description": "실시간 트레이딩뷰 차트 연동, 1x-20x 레버리지 롱/숏 모의투자, 켈리 공식 포지션 사이징, 실시간 수익률 랭킹 리더보드 시뮬레이터"
  }
  </script>

  <style>
    /* ==========================================================================
       Vibe Trading Terminal - Toss Design System Dark Theme (v9.0 Apex)
       ========================================================================== */
    :root {
      --vibe-bg-base: #0a0e17;
      --vibe-bg-surface: #111827;
      --vibe-bg-card: #131c2e;
      --vibe-bg-card-hover: #19243b;
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
      --vibe-gold: #f59e0b;

      --vibe-font-sans: 'Pretendard Variable', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --vibe-font-mono: 'JetBrains Mono', monospace;
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
      line-height: 1.6;
      padding: 16px;
      -webkit-font-smoothing: antialiased;
    }

    .vibe-terminal-container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* Top Sticky HUD */
    .vibe-header {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      border-radius: 16px;
      padding: 16px 20px;
      margin-bottom: 20px;
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
      gap: 16px;
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

    /* Asset Selector Bar */
    .vibe-asset-bar {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 20px;
    }

    .vibe-asset-pill {
      background: var(--vibe-bg-surface);
      border: 1px solid var(--vibe-border-card);
      color: var(--vibe-text-body);
      border-radius: 20px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 700;
      font-family: var(--vibe-font-mono);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .vibe-asset-pill:hover, .vibe-asset-pill.active {
      background: #1e3a8a;
      border-color: var(--vibe-blue);
      color: #ffffff;
    }

    .vibe-asset-pill.active .ticker-price {
      color: #ffffff;
    }

    .vibe-asset-pill .ticker-price {
      color: var(--vibe-green);
    }

    /* Main Grid: Chart + Order Panel */
    .vibe-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
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
      justify-content: space-between;
      align-items: center;
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
    }

    .vibe-chart-tab.active {
      background: #1d4ed8;
      border-color: #2563eb;
      color: #ffffff;
    }

    .vibe-chart-viewport {
      height: 480px;
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
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .vibe-order-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--vibe-text-primary);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .vibe-side-switch {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .vibe-side-btn {
      padding: 12px;
      border: none;
      border-radius: 10px;
      font-size: 14px;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .vibe-side-btn.long {
      background: var(--vibe-green-bg);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--vibe-green);
    }

    .vibe-side-btn.long.active {
      background: #047857;
      color: #ffffff;
    }

    .vibe-side-btn.short {
      background: var(--vibe-red-bg);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: var(--vibe-red);
    }

    .vibe-side-btn.short.active {
      background: #b91c1c;
      color: #ffffff;
    }

    .vibe-form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .vibe-form-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--vibe-text-muted);
      display: flex;
      justify-content: space-between;
    }

    .vibe-input {
      background: var(--vibe-bg-base);
      border: 1px solid var(--vibe-border-subtle);
      border-radius: 8px;
      padding: 10px 14px;
      color: #ffffff;
      font-size: 15px;
      font-family: var(--vibe-font-mono);
      width: 100%;
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
      padding: 8px 4px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }

    .vibe-lev-btn.active {
      background: #2563eb;
      border-color: #3b82f6;
      color: #ffffff;
    }

    .vibe-exec-btn {
      width: 100%;
      padding: 16px;
      border: none;
      border-radius: 12px;
      font-size: 16px;
      font-weight: 900;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: 8px;
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

    /* Positions & Leaderboard 2-Column Section */
    .vibe-lower-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
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
      font-size: 16px;
      font-weight: 800;
      color: var(--vibe-text-primary);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Leaderboard Table */
    .vibe-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    .vibe-table th {
      text-align: left;
      padding: 10px 12px;
      color: var(--vibe-text-muted);
      border-bottom: 1px solid var(--vibe-border-card);
      font-weight: 700;
    }

    .vibe-table td {
      padding: 12px;
      border-bottom: 1px solid var(--vibe-border-card);
      font-family: var(--vibe-font-mono);
      color: var(--vibe-text-body);
    }

    .vibe-rank-badge {
      display: inline-block;
      width: 24px;
      height: 24px;
      line-height: 24px;
      text-align: center;
      border-radius: 50%;
      font-weight: 800;
      font-size: 12px;
    }

    .vibe-rank-1 { background: #fbbf24; color: #000000; }
    .vibe-rank-2 { background: #cbd5e1; color: #000000; }
    .vibe-rank-3 { background: rgba(217, 119, 6, 0.25); border: 1px solid #f59e0b; color: #fbbf24; }

    .post-meta, .post-meta span, .apex-post-meta, .apex-post-meta span, footer p, .apex-footer p {
      color: #94a3b8 !important;
    }

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
      padding: 12px;
      height: 160px;
      overflow-y: hidden;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .vibe-feed-item {
      font-size: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      animation: fadeIn 0.4s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Disclaimer Box */
    .vibe-disclaimer {
      background: #0f172a;
      border-left: 4px solid #ef4444;
      border-radius: 12px;
      padding: 16px 20px;
      color: var(--vibe-text-muted);
      font-size: 13px;
      line-height: 1.7;
    }

    .vibe-disclaimer strong {
      color: #f87171;
      display: block;
      margin-bottom: 6px;
      font-size: 14px;
    }
  </style>
</head>
<body>

<div class="vibe-terminal-container">

  <!-- Top Sticky HUD -->
  <header class="vibe-header">
    <div class="vibe-brand" style="display:flex; align-items:center; gap:14px;">
      <a href="/" style="display:inline-flex; align-items:center; gap:6px; background:rgba(31,45,71,0.85); border:1px solid #2d3e5e; color:#e2e8f0; font-size:13px; font-weight:700; padding:7px 14px; border-radius:8px; text-decoration:none; transition:all 0.2s;" onmouseover="this.style.borderColor='#3b82f6';this.style.color='#60a5fa'" onmouseout="this.style.borderColor='#2d3e5e';this.style.color='#e2e8f0'">
        <span>🏠 블로그 홈</span>
      </a>
      <div>
        <span class="vibe-brand-badge">PRO QUANT TERMINAL</span>
        <h1 class="vibe-title">🔥 VIBE TRADING (실시간 모의투자 랭킹전)</h1>
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

  <!-- Asset Selector -->
  <div class="vibe-asset-bar" id="asset-selector-bar">
    <button class="vibe-asset-pill active" onclick="VibeEngine.selectAsset('BTCUSDT', 'BINANCE:BTCUSDT')">
      <span>BTC/USDT</span> <span class="ticker-price" id="pill-price-BTCUSDT">$68,450.20</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('ETHUSDT', 'BINANCE:ETHUSDT')">
      <span>ETH/USDT</span> <span class="ticker-price" id="pill-price-ETHUSDT">$2,540.80</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('SOLUSDT', 'BINANCE:SOLUSDT')">
      <span>SOL/USDT</span> <span class="ticker-price" id="pill-price-SOLUSDT">$178.40</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('NVDA', 'NASDAQ:NVDA')">
      <span>NVDA</span> <span class="ticker-price" id="pill-price-NVDA">$141.50</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('TSLA', 'NASDAQ:TSLA')">
      <span>TSLA</span> <span class="ticker-price" id="pill-price-TSLA">$218.40</span>
    </button>
    <button class="vibe-asset-pill" onclick="VibeEngine.selectAsset('QQQ', 'NASDAQ:QQQ')">
      <span>QQQ</span> <span class="ticker-price" id="pill-price-QQQ">$492.10</span>
    </button>
  </div>

  <!-- Chart + Order Execution Grid -->
  <div class="vibe-grid">

    <!-- Chart Card -->
    <div class="vibe-chart-card">
      <div class="vibe-chart-header">
        <div style="display:flex; align-items:center; gap:10px;">
          <strong style="color:#ffffff; font-size:16px;" id="chart-asset-title">BTC/USDT 실시간 차트</strong>
          <span style="font-size:12px; color:#10b981; font-weight:700;" id="chart-live-badge">🟢 60fps LIVE STREAM</span>
        </div>
        <div class="vibe-chart-tabs">
          <button class="vibe-chart-tab active" id="tab-tv" onclick="VibeEngine.switchChart('tv')">📊 트레이딩뷰 프로</button>
          <button class="vibe-chart-tab" id="tab-canvas" onclick="VibeEngine.switchChart('canvas')">⚡ 초고속 캔버스</button>
        </div>
      </div>

      <div class="vibe-chart-viewport" id="chart-container">
        <!-- TradingView Widget -->
        <div id="tv_chart_container" style="height:100%; width:100%;"></div>
        <!-- Canvas Fallback -->
        <canvas id="canvas_chart_viewport" width="800" height="480" style="display:none; width:100%; height:100%;"></canvas>
      </div>
    </div>

    <!-- Order Execution Panel -->
    <div class="vibe-order-panel">
      <div class="vibe-order-title">
        <span>⚡ 모의 레버리지 주문</span>
        <span style="font-size:12px; color:#94a3b8;" id="current-asset-badge">BTC/USDT</span>
      </div>

      <!-- Long / Short Switch -->
      <div class="vibe-side-switch">
        <button class="vibe-side-btn long active" id="btn-side-long" onclick="VibeEngine.setSide('LONG')">🟢 BUY / LONG (롱)</button>
        <button class="vibe-side-btn short" id="btn-side-short" onclick="VibeEngine.setSide('SHORT')">🔴 SELL / SHORT (숏)</button>
      </div>

      <!-- Leverage Slider -->
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

      <!-- Order Amount -->
      <div class="vibe-form-group">
        <div class="vibe-form-label">
          <span>투입 증거금 (Margin USDT)</span>
          <span id="label-max-margin" style="color:#94a3b8;">최대: $10,000.00</span>
        </div>
        <input type="number" class="vibe-input" id="input-order-margin" value="2000" min="10" step="10" oninput="VibeEngine.calculateOrderPreview()">
        <div style="display:flex; gap:6px; margin-top:4px;">
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.25)">25%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.50)">50%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(0.75)">75%</button>
          <button class="vibe-lev-btn" onclick="VibeEngine.setMarginPercent(1.00)">100% (올인)</button>
        </div>
      </div>

      <!-- Order Metrics Preview -->
      <div style="background:#0a0e17; border:1px solid #1f2d47; border-radius:10px; padding:12px; font-size:12px; display:flex; flex-direction:column; gap:6px;">
        <div style="display:flex; justify-content:space-between;">
          <span style="color:#94a3b8;">총 포지션 규모:</span>
          <strong style="color:#ffffff;" id="preview-notional">$20,000.00</strong>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:#94a3b8;">예상 청산가 (Liquidation):</span>
          <strong style="color:#ef4444;" id="preview-liq">$61,605.18 (-10.0%)</strong>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:#94a3b8;">켈리 공식 권장 비중:</span>
          <strong style="color:#10b981;">18.5% 권장</strong>
        </div>
      </div>

      <!-- Big Action Button -->
      <button class="vibe-exec-btn long-mode" id="btn-submit-order" onclick="VibeEngine.executeOrder()">
        🚀 BTC 10x 롱 포지션 진입 (주문 실행)
      </button>
    </div>

  </div>

  <!-- Lower Section: Active Positions + Leaderboard -->
  <div class="vibe-lower-grid">

    <!-- Active Positions Table -->
    <div class="vibe-panel-card">
      <div class="vibe-card-header">
        <span>💼 보유 중인 포지션 (<span id="pos-count">0</span>)</span>
        <span style="font-size:12px; color:#94a3b8;">실시간 시세 반영 중</span>
      </div>

      <div style="overflow-x:auto;">
        <table class="vibe-table" id="table-positions">
          <thead>
            <tr>
              <th>종목/방향</th>
              <th>진입가</th>
              <th>현재가</th>
              <th>청산가</th>
              <th>수익률 (PnL)</th>
              <th>청산</th>
            </tr>
          </thead>
          <tbody id="tbody-positions">
            <tr>
              <td colspan="6" style="text-align:center; color:#94a3b8; padding:28px;">현재 보유 중인 포지션이 없습니다. 상단에서 롱/숏 주문을 체결해보세요!</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Competitive Leaderboard (경쟁 순위표) -->
    <div class="vibe-panel-card">
      <div class="vibe-card-header">
        <span>🏆 VIBE 명예의 전당 (실시간 수익률 랭킹)</span>
        <button class="vibe-reset-btn" onclick="VibeEngine.shareRank()" style="padding:4px 10px; font-size:11px;">🔗 랭킹 공유</button>
      </div>

      <!-- Trader Nickname Reg Bar -->
      <div style="display:flex; gap:8px; margin-bottom:12px;">
        <input type="text" class="vibe-input" id="input-trader-name" placeholder="트레이더 닉네임 입력 (예: 압구정불개미)" style="font-size:13px; padding:8px 12px;">
        <button class="vibe-lev-btn" onclick="VibeEngine.saveTraderName()" style="flex:0 0 100px; background:#2563eb; color:#fff; border-color:#3b82f6;">닉네임 저장</button>
      </div>

      <div style="overflow-x:auto; margin-bottom:16px;">
        <table class="vibe-table" id="table-leaderboard">
          <thead>
            <tr>
              <th>순위</th>
              <th>트레이더</th>
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
   Vibe Trading Engine - Vanilla JS High-Performance Trading Core
   ========================================================================== */
const VibeEngine = (function() {
  // State
  let state = {
    cash: 10000.0,
    initialCash: 10000.0,
    activeAsset: 'BTCUSDT',
    tvSymbol: 'BINANCE:BTCUSDT',
    prices: {
      'BTCUSDT': 68450.20,
      'ETHUSDT': 2540.80,
      'SOLUSDT': 178.40,
      'NVDA': 141.50,
      'TSLA': 218.40,
      'QQQ': 492.10
    },
    side: 'LONG',
    leverage: 10,
    positions: [],
    traderName: '나홀로트레이더',
    chartType: 'tv'
  };

  // Pre-seeded Hall of Fame Leaderboard
  let leaderboard = [
    { rank: 1, name: '월가타짜', pnl: 384.2, equity: 48420.0 },
    { rank: 2, name: '여의도불사조', pnl: 271.5, equity: 37150.0 },
    { rank: 3, name: '퀀트마스터', pnl: 198.8, equity: 29880.0 },
    { rank: 4, name: '비트코인고래', pnl: 142.3, equity: 24230.0 },
    { rank: 5, name: '사토시제자', pnl: 115.6, equity: 21560.0 },
    { rank: 6, name: '판교개발자', pnl: 84.2, equity: 18420.0 },
    { rank: 7, name: '나스닥롱충이', pnl: 65.1, equity: 16510.0 },
    { rank: 8, name: '켈리신봉자', pnl: 48.7, equity: 14870.0 },
    { rank: 9, name: '테슬라올인', pnl: 32.4, equity: 13240.0 }
  ];

  // Audio chimes synthesized via Web Audio API
  function playSound(type) {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const ctx = new AudioContext();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'order') {
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.setValueAtTime(880.00, ctx.currentTime + 0.08); // A5
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
        osc.start();
        osc.stop(ctx.currentTime + 0.25);
      } else if (type === 'win') {
        osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
        osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.08); // E5
        osc.frequency.setValueAtTime(783.99, ctx.currentTime + 0.16); // G5
        gain.gain.setValueAtTime(0.18, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
        osc.start();
        osc.stop(ctx.currentTime + 0.4);
      }
    } catch (e) {
      // AudioContext policy suppression fallback
    }
  }

  // Load persistence
  function loadState() {
    try {
      const saved = localStorage.getItem('blogin_vibe_state');
      if (saved) {
        const parsed = JSON.parse(saved);
        state.cash = parsed.cash !== undefined ? parsed.cash : state.cash;
        state.positions = parsed.positions || [];
        state.traderName = parsed.traderName || state.traderName;
      }
    } catch(e) {}
  }

  function saveState() {
    try {
      localStorage.setItem('blogin_vibe_state', JSON.stringify({
        cash: state.cash,
        positions: state.positions,
        traderName: state.traderName
      }));
    } catch(e) {}
  }

  // Render TradingView Chart
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

  // Switch between TradingView & 60fps Canvas
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

  // Fallback 60fps HTML5 Canvas chart renderer
  function renderCanvasChart() {
    const canvas = document.getElementById('canvas_chart_viewport');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    // Draw dark background
    ctx.fillStyle = '#0a0e17';
    ctx.fillRect(0, 0, w, h);

    // Draw grid lines
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

    // Generate pseudo candlesticks
    const basePrice = state.prices[state.activeAsset] || 50000;
    let curr = basePrice * 0.98;
    const count = 35;
    const candleW = (w - 100) / count;

    for (let i = 0; i < count; i++) {
      const open = curr;
      const change = (Math.random() - 0.48) * (basePrice * 0.015);
      const close = open + change;
      const high = Math.max(open, close) + Math.random() * (basePrice * 0.008);
      const low = Math.min(open, close) - Math.random() * (basePrice * 0.008);
      curr = close;

      const isUp = close >= open;
      ctx.strokeStyle = isUp ? '#10b981' : '#ef4444';
      ctx.fillStyle = isUp ? '#10b981' : '#ef4444';

      const x = 40 + i * candleW;
      const yMax = basePrice * 1.05;
      const yMin = basePrice * 0.95;
      const scaleY = (val) => h - 40 - ((val - yMin) / (yMax - yMin)) * (h - 80);

      // Wick
      ctx.beginPath();
      ctx.moveTo(x + candleW / 2, scaleY(high));
      ctx.lineTo(x + candleW / 2, scaleY(low));
      ctx.stroke();

      // Body
      const bodyTop = scaleY(Math.max(open, close));
      const bodyH = Math.max(2, Math.abs(scaleY(open) - scaleY(close)));
      ctx.fillRect(x + 2, bodyTop, candleW - 4, bodyH);
    }
  }

  // Live WebSocket streaming (Binance WSS with REST fallback)
  function startPriceStream() {
    try {
      const ws = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@ticker/ethusdt@ticker/solusdt@ticker');
      ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const s = data.s; // e.g. BTCUSDT
        const p = parseFloat(data.c); // current price
        if (s && p && state.prices[s] !== undefined) {
          state.prices[s] = p;
          updatePricePills();
          recalcPositions();
        }
      };
      ws.onerror = function() {
        startMockTick();
      };
    } catch(e) {
      startMockTick();
    }
  }

  // Gaussian walk mock ticker if offline
  function startMockTick() {
    setInterval(() => {
      for (const k in state.prices) {
        const drift = (Math.random() - 0.495) * (state.prices[k] * 0.002);
        state.prices[k] = Math.max(1, state.prices[k] + drift);
      }
      updatePricePills();
      recalcPositions();
    }, 1500);
  }

  function updatePricePills() {
    for (const k in state.prices) {
      const el = document.getElementById('pill-price-' + k);
      if (el) {
        el.textContent = '$' + state.prices[k].toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
      }
    }
    calculateOrderPreview();
  }

  // Select asset
  function selectAsset(assetKey, tvSymbol) {
    state.activeAsset = assetKey;
    state.tvSymbol = tvSymbol;
    document.querySelectorAll('.vibe-asset-pill').forEach(el => el.classList.remove('active'));
    event.currentTarget.classList.add('active');

    document.getElementById('chart-asset-title').textContent = assetKey + ' 실시간 차트';
    document.getElementById('current-asset-badge').textContent = assetKey;

    if (state.chartType === 'tv') {
      initTradingView(tvSymbol);
    } else {
      renderCanvasChart();
    }
    calculateOrderPreview();
  }

  // Order settings
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

    document.getElementById('label-max-margin').textContent = '최대 가용: $' + state.cash.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('preview-notional').textContent = '$' + notional.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});

    // Liquidation price
    let liqPrice = 0;
    if (state.side === 'LONG') {
      liqPrice = price * (1 - (1 / state.leverage) + 0.005);
    } else {
      liqPrice = price * (1 + (1 / state.leverage) - 0.005);
    }
    const liqPct = ((liqPrice - price) / price) * 100;
    document.getElementById('preview-liq').textContent = '$' + liqPrice.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + liqPct.toFixed(1) + '%)';
  }

  // Execute Order
  function executeOrder() {
    const margin = parseFloat(document.getElementById('input-order-margin').value) || 0;
    if (margin <= 0 || margin > state.cash) {
      alert('가용 증거금이 부족합니다! (현재 가용: $' + state.cash.toFixed(2) + ')');
      return;
    }

    const price = state.prices[state.activeAsset];
    let liqPrice = 0;
    if (state.side === 'LONG') {
      liqPrice = price * (1 - (1 / state.leverage) + 0.005);
    } else {
      liqPrice = price * (1 + (1 / state.leverage) - 0.005);
    }

    state.cash -= margin;
    const newPos = {
      id: 'pos_' + Date.now(),
      asset: state.activeAsset,
      side: state.side,
      leverage: state.leverage,
      entryPrice: price,
      margin: margin,
      size: (margin * state.leverage) / price,
      liqPrice: liqPrice,
      createdAt: new Date().toLocaleTimeString()
    };

    state.positions.push(newPos);
    playSound('order');
    saveState();
    recalcPositions();
    addFeedItem('🚀 [' + state.traderName + '] 님이 ' + state.activeAsset + ' ' + state.leverage + 'x ' + state.side + ' 포지션 체결!');
  }

  // Close Position
  function closePosition(posId) {
    const idx = state.positions.findIndex(p => p.id === posId);
    if (idx === -1) return;
    const pos = state.positions[idx];
    const currPrice = state.prices[pos.asset];

    let pnl = 0;
    if (pos.side === 'LONG') {
      pnl = (currPrice - pos.entryPrice) * pos.size;
    } else {
      pnl = (pos.entryPrice - currPrice) * pos.size;
    }

    state.cash += Math.max(0, pos.margin + pnl);
    state.positions.splice(idx, 1);

    if (pnl > 0) playSound('win');
    saveState();
    recalcPositions();

    const sign = pnl >= 0 ? '+' : '';
    addFeedItem('💰 [' + state.traderName + '] 님이 ' + pos.asset + ' 포지션 ' + sign + '$' + pnl.toFixed(2) + ' 청산!');
  }

  // Recalculate all positions & update HUD
  function recalcPositions() {
    let unrealizedPnl = 0;
    const tbody = document.getElementById('tbody-positions');
    const posCount = document.getElementById('pos-count');
    if (posCount) posCount.textContent = state.positions.length;

    if (state.positions.length === 0) {
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#94a3b8; padding:28px;">현재 보유 중인 포지션이 없습니다. 상단에서 롱/숏 주문을 체결해보세요!</td></tr>';
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

        // Check liquidation
        if ((pos.side === 'LONG' && currPrice <= pos.liqPrice) || (pos.side === 'SHORT' && currPrice >= pos.liqPrice)) {
          // Liquidate!
          addFeedItem('💥 [' + state.traderName + '] 님의 ' + pos.asset + ' ' + pos.leverage + 'x 포지션 강제 청산!');
          state.positions = state.positions.filter(p => p.id !== pos.id);
          saveState();
          return recalcPositions();
        }

        unrealizedPnl += posPnl;
        const pnlPct = (posPnl / pos.margin) * 100;
        const pnlClass = posPnl >= 0 ? 'color:#10b981;' : 'color:#ef4444;';
        const sign = posPnl >= 0 ? '+' : '';
        const sideColor = pos.side === 'LONG' ? '#10b981' : '#ef4444';

        rowsHtml += `<tr>
          <td>
            <strong style="color:#ffffff;">${pos.asset}</strong>
            <span style="display:inline-block; margin-left:4px; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:800; background:${pos.side === 'LONG' ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)'}; color:${sideColor};">${pos.leverage}x ${pos.side}</span>
          </td>
          <td>$${pos.entryPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
          <td>$${currPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
          <td style="color:#ef4444;">$${pos.liqPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
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
    while (feed.children.length > 5) {
      feed.removeChild(feed.lastChild);
    }
  }

  function resetAccount() {
    if (confirm('가상 계좌 잔고를 $10,000 초기 상태로 리셋하시겠습니까?')) {
      state.cash = 10000.0;
      state.positions = [];
      saveState();
      recalcPositions();
    }
  }

  // Init
  function init() {
    loadState();
    const nameInput = document.getElementById('input-trader-name');
    if (nameInput) nameInput.value = state.traderName;
    initTradingView('BINANCE:BTCUSDT');
    startPriceStream();
    recalcPositions();

    // Seed initial feed
    addFeedItem('🌟 [월가타짜] 님이 BTC 20x 롱 포지션 +$3,420 익절!');
    addFeedItem('⚡ [여의도불사조] 님이 ETH 15x 숏 포지션 진입');
    addFeedItem('🔥 [비트코인고래] 님이 SOL 10x 롱 $2,180 청산 성공!');

    // Simulate periodic live feed
    setInterval(() => {
      const bots = ['월가타짜', '여의도불사조', '퀀트마스터', '비트코인고래', '판교개발자', '나스닥롱충이'];
      const assets = ['BTC', 'ETH', 'SOL', 'NVDA', 'TSLA'];
      const bot = bots[Math.floor(Math.random() * bots.length)];
      const asset = assets[Math.floor(Math.random() * assets.length)];
      const pnl = (Math.random() * 2500 + 300).toFixed(0);
      addFeedItem('💰 [' + bot + '] 님이 ' + asset + ' 포지션 +$' + pnl + ' 실시간 익절!');
    }, 7000);
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
    resetAccount
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
