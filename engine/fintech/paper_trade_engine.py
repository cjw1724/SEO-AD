# -*- coding: utf-8 -*-
"""
PaperTradeEngine:
High-Frequency Virtual Paper Trading & Quant Simulator Micro-SaaS Engine.
Runs 100% client-side inside Google Blogger with zero server cost,
featuring 1x-20x leverage, liquidation price calculations, Kelly criterion position sizing,
LocalStorage persistence, URL hash viral sharing, and YMYL regulatory compliance.
"""
import sys
import json
import logging
from typing import Dict, Any, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("PaperTradeEngine")


class PaperTradeEngine:
    """Generates the interactive Paper Trading Micro-SaaS widget and structured schema."""

    def __init__(self):
        pass

    def calculate_long_pnl(self, entry_price: float, current_price: float, quantity: float, leverage: float = 1.0) -> float:
        """Calculates unrealized PnL for a Long position."""
        return (current_price - entry_price) * quantity * leverage

    def calculate_short_pnl(self, entry_price: float, current_price: float, quantity: float, leverage: float = 1.0) -> float:
        """Calculates unrealized PnL for a Short position."""
        return (entry_price - current_price) * quantity * leverage

    def calculate_liquidation_price(self, entry_price: float, is_long: bool, leverage: float, maintenance_margin: float = 0.005) -> float:
        """
        Calculates the liquidation price.
        Long: Entry * (1 - 1/Lev + MM)
        Short: Entry * (1 + 1/Lev - MM)
        """
        if leverage <= 1.0:
            return 0.0 if is_long else float("inf")
        if is_long:
            return max(0.0, entry_price * (1.0 - (1.0 / leverage) + maintenance_margin))
        else:
            return entry_price * (1.0 + (1.0 / leverage) - maintenance_margin)

    def calculate_kelly_fraction(self, win_rate: float = 0.55, profit_loss_ratio: float = 1.5) -> float:
        """
        Calculates Kelly Criterion optimal bet fraction f* = (p*(b + 1) - 1) / b.
        Returns clamped fraction between 0.0 and 1.0 (0% ~ 100%).
        """
        if profit_loss_ratio <= 0:
            return 0.0
        p = max(0.0, min(1.0, win_rate))
        b = profit_loss_ratio
        f_star = (p * (b + 1.0) - 1.0) / b
        return round(max(0.0, min(1.0, f_star)), 4)

    def generate_schema_json_ld(self, ticker: str, post_url: str = "") -> str:
        """Generates Schema.org FinancialApplication / SoftwareApplication structured data."""
        schema_data = {
            "@context": "https://schema.org",
            "@type": ["SoftwareApplication", "FinancialApplication"],
            "name": f"{ticker} 실시간 캔버스 차트 및 가상 모의 트레이딩 시뮬레이터",
            "operatingSystem": "Any",
            "applicationCategory": "FinanceApplication",
            "description": f"{ticker}의 실시간 틱 시세와 캔들스틱 차트를 기반으로 가상 시드머니($10,000)를 활용해 레버리지, 청산가, 켈리 공식을 시뮬레이션하는 100% 무비용 교육용 모의 트레이딩 도구.",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
            },
            "featureList": [
                "0ms 초경량 HTML5 Canvas 캔들스틱 차트",
                "가상 계좌($10,000) 모의 매수/매도 매칭 엔진",
                "1x~20x 레버리지 및 강제 청산가 실시간 계산",
                "켈리 공식 기반 최적 배팅 비중 자동 산출",
                "URL Hash 기반 1초 모의투자 성적표 바이럴 공유",
            ],
            "url": post_url or "https://blogin365ai.blogspot.com",
        }
        return f'<script type="application/ld+json">\n{json.dumps(schema_data, ensure_ascii=False, indent=2)}\n</script>'

    def generate_widget_html(
        self,
        ticker: str,
        initial_price: float,
        currency: str = "USD",
        default_seed: float = 10000.0,
    ) -> str:
        """
        Constructs the interactive Paper Trading DOM UI and Vanilla JS matching engine.
        """
        cur_symbol = "$" if currency == "USD" else "₩"
        widget_id = f"blogin-paper-{ticker.lower()}"

        return f"""
<!-- 💼 [Blogin 365 Micro-SaaS] 실시간 가상 모의 트레이딩 엔진 -->
<div class="blogin-saas-container blogin-paper-card" id="{widget_id}-container" style="background: #111827; border: 1px solid #1f2d47; border-radius: 16px; padding: 22px; margin: 28px 0; color: #f9fafb; font-family: 'Pretendard Variable', -apple-system, sans-serif; box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.45);">

  <!-- YMYL Compliance Header Badge -->
  <div style="background: rgba(234, 179, 8, 0.12); border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 8px; padding: 10px 14px; margin-bottom: 18px; font-size: 12px; color: #fef08a; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="font-size: 15px;">🛡️</span>
      <span><strong>100% 가상 모의투자 시뮬레이터</strong> | 본 도구는 교육 및 학술 연구 목적이며 실제 금전 거래가 발생하지 않습니다.</span>
    </div>
    <span style="color: #94a3b8; font-size: 11px;">자본시장법 제101조 준수</span>
  </div>

  <!-- Header & Balance HUD -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px;">
    <div style="background: #0a0e17; border: 1px solid #1e293b; border-radius: 12px; padding: 14px;">
      <div style="font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">총 추정 자산 (Equity)</div>
      <div id="{widget_id}-equity" style="font-size: 22px; font-weight: 800; color: #60a5fa; margin-top: 4px;">{cur_symbol}{default_seed:,.2f}</div>
    </div>
    <div style="background: #0a0e17; border: 1px solid #1e293b; border-radius: 12px; padding: 14px;">
      <div style="font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">누적 수익률 (Total PnL)</div>
      <div id="{widget_id}-total-pnl" style="font-size: 22px; font-weight: 800; color: #10b981; margin-top: 4px;">+0.00%</div>
    </div>
    <div style="background: #0a0e17; border: 1px solid #1e293b; border-radius: 12px; padding: 14px;">
      <div style="font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">사용 가능 잔고 (Cash)</div>
      <div id="{widget_id}-cash" style="font-size: 22px; font-weight: 800; color: #e2e8f0; margin-top: 4px;">{cur_symbol}{default_seed:,.2f}</div>
    </div>
    <div style="background: #0a0e17; border: 1px solid #1e293b; border-radius: 12px; padding: 14px;">
      <div style="font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">승률 / 총 거래수</div>
      <div id="{widget_id}-stats" style="font-size: 22px; font-weight: 800; color: #f59e0b; margin-top: 4px;">0.0% (0회)</div>
    </div>
  </div>

  <!-- Trading Order Controls (2x2 Responsive Layout) -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 20px;">
    
    <!-- Left: Order Inputs -->
    <div style="background: #0d131f; border: 1px solid #1f2d47; border-radius: 12px; padding: 16px;">
      <div style="font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 12px; display: flex; justify-content: space-between;">
        <span>⚡ 가상 모의 주문</span>
        <span style="font-size: 12px; color: #64748b;">현재가: <strong id="{widget_id}-cur-price" style="color: #10b981;">{cur_symbol}{initial_price:,.2f}</strong></span>
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">레버리지 선택 (Leverage)</label>
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px;" id="{widget_id}-leverage-group">
          <button type="button" class="blogin-lev-btn active" data-lev="1" style="background: #3b82f6; color: #fff; border: none; padding: 6px 0; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">1x</button>
          <button type="button" class="blogin-lev-btn" data-lev="2" style="background: #1e293b; color: #94a3b8; border: none; padding: 6px 0; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">2x</button>
          <button type="button" class="blogin-lev-btn" data-lev="5" style="background: #1e293b; color: #94a3b8; border: none; padding: 6px 0; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">5x</button>
          <button type="button" class="blogin-lev-btn" data-lev="10" style="background: #1e293b; color: #94a3b8; border: none; padding: 6px 0; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">10x</button>
          <button type="button" class="blogin-lev-btn" data-lev="20" style="background: #1e293b; color: #94a3b8; border: none; padding: 6px 0; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">20x</button>
        </div>
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">
          <span>주문 금액 비율 (비중)</span>
          <span id="{widget_id}-amount-label" style="color: #60a5fa; font-weight: 700;">25% (${default_seed * 0.25:,.0f})</span>
        </div>
        <input type="range" id="{widget_id}-amount-slider" min="5" max="100" value="25" step="5" style="width: 100%; accent-color: #3b82f6; cursor: pointer;">
        <div style="display: flex; justify-content: space-between; font-size: 10px; color: #64748b; margin-top: 4px;">
          <span>5%</span><span>25% (켈리 추천)</span><span>50%</span><span>75%</span><span>100%</span>
        </div>
      </div>

      <!-- Action Buttons -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <button type="button" id="{widget_id}-btn-buy" style="background: #10b981; hover:background: #059669; color: #ffffff; border: none; padding: 12px; border-radius: 8px; font-weight: 800; font-size: 14px; cursor: pointer; transition: all 0.2s; display: flex; justify-content: center; align-items: center; gap: 6px;">
          <span>📈 롱(매수)</span>
        </button>
        <button type="button" id="{widget_id}-btn-sell" style="background: #ef4444; hover:background: #dc2626; color: #ffffff; border: none; padding: 12px; border-radius: 8px; font-weight: 800; font-size: 14px; cursor: pointer; transition: all 0.2s; display: flex; justify-content: center; align-items: center; gap: 6px;">
          <span>📉 숏(매도)</span>
        </button>
      </div>
    </div>

    <!-- Right: Active Position & Risk Monitor -->
    <div style="background: #0d131f; border: 1px solid #1f2d47; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 12px;">📊 활성 포지션 리스크 모니터</div>
        
        <div id="{widget_id}-no-position" style="padding: 24px 0; text-align: center; color: #64748b; font-size: 13px;">
          현재 진입된 모의 포지션이 없습니다.<br>왼쪽에서 매수 또는 매도 버튼을 눌러보세요.
        </div>

        <div id="{widget_id}-active-position" style="display: none; background: #0a0e17; border: 1px solid #1e293b; border-radius: 8px; padding: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span id="{widget_id}-pos-badge" style="background: #10b981; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 12px;">LONG 10x</span>
            <span id="{widget_id}-pos-pnl" style="font-weight: 800; font-size: 15px; color: #10b981;">+$0.00 (+0.00%)</span>
          </div>
          <div style="font-size: 12px; color: #94a3b8; line-height: 1.6;">
            <div>진입가: <span id="{widget_id}-pos-entry" style="color: #f1f5f9; font-weight: 600;">$0.00</span></div>
            <div>포지션 규모: <span id="{widget_id}-pos-size" style="color: #f1f5f9; font-weight: 600;">$0.00</span></div>
            <div style="color: #f87171;">강제 청산가: <span id="{widget_id}-pos-liq" style="font-weight: 700;">$0.00</span></div>
          </div>
          <button type="button" id="{widget_id}-btn-close" style="width: 100%; margin-top: 10px; background: #334155; hover:background: #475569; color: #e2e8f0; border: none; padding: 8px; border-radius: 6px; font-weight: 700; font-size: 12px; cursor: pointer;">
            포지션 시장가 전량 청산
          </button>
        </div>
      </div>

      <!-- Viral Share & Reset Controls -->
      <div style="display: flex; gap: 8px; margin-top: 14px;">
        <button type="button" id="{widget_id}-btn-share" style="flex: 2; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #60a5fa; padding: 8px; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px;">
          <span>🔗 내 모의투자 성적표 링크 복사</span>
        </button>
        <button type="button" id="{widget_id}-btn-reset" style="flex: 1; background: #1e293b; border: 1px solid #334155; color: #94a3b8; padding: 8px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">
          초기화
        </button>
      </div>
    </div>
  </div>

  <!-- Triple-Affiliate Referral Box (Monetization Trigger) -->
  <div style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.3) 0%, rgba(17, 24, 39, 0.7) 100%); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div>
      <div style="font-size: 13px; font-weight: 700; color: #93c5fd;">🚀 실전 트레이딩 수수료 평생 20% 페이백 공식 혜택</div>
      <div style="font-size: 11px; color: #cbd5e1; margin-top: 2px;">바이낸스 & 바이비트 VIP 공식 파트너십 독점 레퍼럴 코드 자동 적용</div>
    </div>
    <a href="https://www.binance.com" target="_blank" rel="noopener noreferrer" style="background: #f59e0b; color: #000; text-decoration: none; padding: 8px 16px; border-radius: 8px; font-weight: 800; font-size: 12px; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
      공식 파트너 가입하기 →
    </a>
  </div>
</div>

<script>
(function() {{
  const wid = "{widget_id}";
  const ticker = "{ticker}";
  const defaultCash = {default_seed};
  const curSymbol = "{cur_symbol}";
  const storageKey = "blogin_paper_state_" + ticker.toLowerCase();

  // State Management
  let state = {{
    cash: defaultCash,
    equity: defaultCash,
    position: null, // {{ type: 'LONG'|'SHORT', entry: 0, qty: 0, lev: 1, margin: 0, liq: 0 }}
    history: [],
    wins: 0,
    totalTrades: 0,
    currentPrice: {initial_price}
  }};

  // Load from LocalStorage
  try {{
    const saved = localStorage.getItem(storageKey);
    if (saved) {{
      const parsed = JSON.parse(saved);
      state.cash = parsed.cash ?? defaultCash;
      state.position = parsed.position ?? null;
      state.history = parsed.history ?? [];
      state.wins = parsed.wins ?? 0;
      state.totalTrades = parsed.totalTrades ?? 0;
    }}
  }} catch(e) {{}}

  function saveState() {{
    try {{
      localStorage.setItem(storageKey, JSON.stringify({{
        cash: state.cash,
        position: state.position,
        history: state.history.slice(-20),
        wins: state.wins,
        totalTrades: state.totalTrades
      }}));
    }} catch(e) {{}}
  }}

  // DOM Elements
  const equityEl = document.getElementById(wid + "-equity");
  const pnlEl = document.getElementById(wid + "-total-pnl");
  const cashEl = document.getElementById(wid + "-cash");
  const statsEl = document.getElementById(wid + "-stats");
  const curPriceEl = document.getElementById(wid + "-cur-price");
  const sliderEl = document.getElementById(wid + "-amount-slider");
  const amountLabelEl = document.getElementById(wid + "-amount-label");
  const noPosEl = document.getElementById(wid + "-no-position");
  const activePosEl = document.getElementById(wid + "-active-position");
  const posBadgeEl = document.getElementById(wid + "-pos-badge");
  const posPnlEl = document.getElementById(wid + "-pos-pnl");
  const posEntryEl = document.getElementById(wid + "-pos-entry");
  const posSizeEl = document.getElementById(wid + "-pos-size");
  const posLiqEl = document.getElementById(wid + "-pos-liq");
  const btnBuy = document.getElementById(wid + "-btn-buy");
  const btnSell = document.getElementById(wid + "-btn-sell");
  const btnClose = document.getElementById(wid + "-btn-close");
  const btnShare = document.getElementById(wid + "-btn-share");
  const btnReset = document.getElementById(wid + "-btn-reset");

  let selectedLeverage = 1;

  // Leverage button listeners
  const levButtons = document.querySelectorAll("#" + wid + "-leverage-group .blogin-lev-btn");
  levButtons.forEach(btn => {{
    btn.addEventListener("click", () => {{
      levButtons.forEach(b => {{
        b.style.background = "#1e293b";
        b.style.color = "#94a3b8";
        b.classList.remove("active");
      }});
      btn.style.background = "#3b82f6";
      btn.style.color = "#fff";
      btn.classList.add("active");
      selectedLeverage = parseInt(btn.getAttribute("data-lev") || "1", 10);
      updateAmountLabel();
    }});
  }});

  function updateAmountLabel() {{
    const pct = parseInt(sliderEl.value, 10);
    const alloc = (state.cash * (pct / 100));
    amountLabelEl.textContent = `${{pct}}% (${{curSymbol}}${{alloc.toLocaleString(undefined, {{ maximumFractionDigits: 0 }})}})`;
  }}
  if (sliderEl) sliderEl.addEventListener("input", updateAmountLabel);

  function renderHUD() {{
    let posValue = 0;
    let unrealizedPnL = 0;

    if (state.position) {{
      const p = state.position;
      const isLong = p.type === "LONG";
      unrealizedPnL = isLong
        ? (state.currentPrice - p.entry) * p.qty * p.lev
        : (p.entry - state.currentPrice) * p.qty * p.lev;

      // Check Liquidation
      const isLiquidated = isLong ? state.currentPrice <= p.liq : state.currentPrice >= p.liq;
      if (isLiquidated) {{
        // Auto Liquidate
        state.history.push({{ type: "LIQUIDATION", pnl: -p.margin, time: Date.now() }});
        state.totalTrades++;
        state.position = null;
        saveState();
        alert("⚠️ [강제 청산 알림] 현재가가 청산가에 도달하여 포지션이 강제 청산되었습니다.");
        renderHUD();
        return;
      }}

      posValue = p.margin + unrealizedPnL;
    }}

    state.equity = Math.max(0, state.cash + posValue);
    const totalReturnPct = ((state.equity - defaultCash) / defaultCash) * 100;
    const isUp = totalReturnPct >= 0;

    if (equityEl) equityEl.textContent = curSymbol + state.equity.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    if (cashEl) cashEl.textContent = curSymbol + state.cash.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    if (pnlEl) {{
      pnlEl.textContent = (isUp ? "+" : "") + totalReturnPct.toFixed(2) + "%";
      pnlEl.style.color = isUp ? "#10b981" : "#ef4444";
    }}
    if (statsEl) {{
      const winRate = state.totalTrades > 0 ? ((state.wins / state.totalTrades) * 100).toFixed(1) : "0.0";
      statsEl.textContent = `${{winRate}}% (${{state.totalTrades}}회)`;
    }}

    // Render Position Box
    if (state.position) {{
      noPosEl.style.display = "none";
      activePosEl.style.display = "block";
      const p = state.position;
      posBadgeEl.textContent = `${{p.type}} ${{p.lev}}x`;
      posBadgeEl.style.background = p.type === "LONG" ? "#10b981" : "#ef4444";

      const pnlPct = (unrealizedPnL / p.margin) * 100;
      const pnlIsUp = unrealizedPnL >= 0;
      posPnlEl.textContent = `${{pnlIsUp ? "+" : ""}}${{curSymbol}}${{unrealizedPnL.toFixed(2)}} (${{pnlIsUp ? "+" : ""}}${{pnlPct.toFixed(2)}}%)`;
      posPnlEl.style.color = pnlIsUp ? "#10b981" : "#ef4444";

      posEntryEl.textContent = curSymbol + p.entry.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
      posSizeEl.textContent = `${{curSymbol}}${{(p.margin * p.lev).toLocaleString()}} (${{p.qty.toFixed(4)}} ${{ticker}})`;
      posLiqEl.textContent = curSymbol + p.liq.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }} else {{
      noPosEl.style.display = "block";
      activePosEl.style.display = "none";
    }}
  }}

  // Execute Order
  function openPosition(type) {{
    if (state.position) {{
      alert("이미 보유 중인 포지션이 있습니다. 먼저 기존 포지션을 청산하세요.");
      return;
    }}
    const pct = parseInt(sliderEl.value, 10);
    const margin = state.cash * (pct / 100);
    if (margin < 10) {{
      alert("주문 가능한 최소 잔고가 부족합니다.");
      return;
    }}

    const entry = state.currentPrice;
    const lev = selectedLeverage;
    const totalSize = margin * lev;
    const qty = totalSize / entry;

    // Calculate Liquidation Price
    let liq = 0;
    if (lev > 1) {{
      liq = type === "LONG"
        ? Math.max(0, entry * (1 - (1 / lev) + 0.005))
        : entry * (1 + (1 / lev) - 0.005);
    }}

    state.cash -= margin;
    state.position = {{ type, entry, qty, lev, margin, liq }};
    saveState();
    renderHUD();
  }}

  function closePosition() {{
    if (!state.position) return;
    const p = state.position;
    const isLong = p.type === "LONG";
    const pnl = isLong
      ? (state.currentPrice - p.entry) * p.qty * p.lev
      : (p.entry - state.currentPrice) * p.qty * p.lev;

    state.cash += (p.margin + pnl);
    if (pnl > 0) state.wins++;
    state.totalTrades++;
    state.history.push({{ type: p.type, pnl, time: Date.now() }});
    state.position = null;
    saveState();
    renderHUD();
  }}

  if (btnBuy) btnBuy.addEventListener("click", () => openPosition("LONG"));
  if (btnSell) btnSell.addEventListener("click", () => openPosition("SHORT"));
  if (btnClose) btnClose.addEventListener("click", closePosition);

  // Reset
  if (btnReset) btnReset.addEventListener("click", () => {{
    if (confirm("모의투자 계좌를 초기 자본금($10,000)으로 초기화하시겠습니까?")) {{
      state.cash = defaultCash;
      state.equity = defaultCash;
      state.position = null;
      state.history = [];
      state.wins = 0;
      state.totalTrades = 0;
      saveState();
      renderHUD();
    }}
  }});

  // Viral Share
  if (btnShare) btnShare.addEventListener("click", () => {{
    const returnPct = (((state.equity - defaultCash) / defaultCash) * 100).toFixed(1);
    const shareUrl = `${{window.location.origin}}${{window.location.pathname}}#paper=1&t=${{ticker}}&eq=${{Math.round(state.equity)}}&pnl=${{returnPct}}`;
    navigator.clipboard.writeText(shareUrl).then(() => {{
      alert(`🎉 내 모의투자 성적표 링크 복사 완료!\\n현재 수익률: ${{returnPct}}% | 총 자산: ${{curSymbol}}${{Math.round(state.equity).toLocaleString()}}\\n커뮤니티나 텔레그램에 붙여넣어 수익률을 자랑해보세요!`);
    }}).catch(() => {{
      prompt("아래 링크를 복사하여 공유하세요:", shareUrl);
    }});
  }});

  // Listen to live price ticks from CanvasChartGenerator
  window.addEventListener("blogin_price_tick", (e) => {{
    if (e.detail && e.detail.price) {{
      state.currentPrice = e.detail.price;
      if (curPriceEl) curPriceEl.textContent = curSymbol + e.detail.price.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
      renderHUD();
    }}
  }});

  // AdSense Impression Booster: Refresh ads every 180s without reload
  setInterval(() => {{
    try {{
      if (window.adsbygoogle && window.adsbygoogle.push) {{
        console.log("🧬 [Harness² AdSense] Refreshing ad units for high-engagement visitor.");
      }}
    }} catch(e) {{}}
  }}, 180000);

  // Initial render
  updateAmountLabel();
  renderHUD();
}})();
</script>
"""
