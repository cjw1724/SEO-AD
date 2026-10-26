# -*- coding: utf-8 -*-
"""
engine/crew/dataset_resolver.py
---------------------------------
최상위 0.000001% pSEO 타이탄(Pieter Levels, Ian Nuttall, Wise, NerdWallet) 역공학 리졸버.
- SSOT 정형 데이터베이스(data/trading_rules_db.json 및 data/hardware_specs_db.json) 기반 무결점 매핑
- LLM의 환각(Hallucination) 및 NaN/부동소수점 버그 원천 차단
- 0ms 반응형 Single-File FinTech Micro-SaaS 위젯 및 데이터 밀도 매트릭스(Data Density Matrix) 자동 생성
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
from engine.fintech.market_oracle import MarketDataOracle, DEFAULT_USD_KRW_RATE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HARDWARE_DB_PATH = os.path.join(BASE_DIR, "data", "hardware_specs_db.json")
TRADING_DB_PATH = os.path.join(BASE_DIR, "data", "trading_rules_db.json")


def load_hardware_db() -> Dict[str, Any]:
    if not os.path.exists(HARDWARE_DB_PATH):
        raise FileNotFoundError(f"SSOT Hardware Specs Database not found: {HARDWARE_DB_PATH}")
    with open(HARDWARE_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_trading_db() -> Dict[str, Any]:
    if not os.path.exists(TRADING_DB_PATH):
        raise FileNotFoundError(f"SSOT Trading Rules Database not found: {TRADING_DB_PATH}")
    with open(TRADING_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# [Domain 1] FinTech & Quant Micro-SaaS 리졸버 (Primary Engine)
# ==============================================================================
class TradingDatasetResolver:
    """
    투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터 SSOT 리졸버
    - 소득세법 제94조 해외주식 양도소득세 22% (지방소득세 포함, 250만 원 기본공제)
    - 0ms 무결점 Vanilla JS 시뮬레이터 및 데이터 대조표 생성
    """
    def __init__(self):
        self.db = load_trading_db()
        self.rules = self.db.get("rules", {})
        self.oracle = MarketDataOracle()
        self.rules = self.db.get("rules", {})

    def resolve_topic(self, topic_hint: str = "") -> Dict[str, Any]:
        """주제 힌트를 바탕으로 가장 적합한 금융 계산 규칙 도출 (20대 핵심 자산 자동 매핑)"""
        hint_lower = (topic_hint or "").lower().strip()

        # 1. DB 직접 매칭
        if topic_hint in self.rules:
            rule_key = topic_hint
        elif any(k in hint_lower for k in ["nvda", "엔비디아"]):
            rule_key = "nvda_stock_tax"
        elif any(k in hint_lower for k in ["tsla", "테슬라"]):
            rule_key = "tsla_water_averaging"
        elif any(k in hint_lower for k in ["aapl", "애플"]):
            rule_key = "aapl_stock_tax"
        elif any(k in hint_lower for k in ["msft", "마이크로소프트"]):
            rule_key = "msft_stock_tax"
        elif any(k in hint_lower for k in ["pltr", "팔란티어"]):
            rule_key = "pltr_water_averaging"
        elif "soxl" in hint_lower:
            rule_key = "soxl_leverage_decay"
        elif "tqqq" in hint_lower:
            rule_key = "tqqq_water_averaging"
        elif any(k in hint_lower for k in ["ionq", "아이온큐"]):
            rule_key = "ionq_water_averaging"
        elif any(k in hint_lower for k in ["coin", "코인베이스"]):
            rule_key = "coin_stock_tax"
        elif any(k in hint_lower for k in ["리얼티인컴", "o 배당", "o_dividend"]):
            rule_key = "o_dividend_compound"
        elif any(k in hint_lower for k in ["btc", "비트코인"]):
            rule_key = "btc_futures_liquidation"
        elif any(k in hint_lower for k in ["eth", "이더리움"]):
            rule_key = "eth_futures_liquidation"
        elif any(k in hint_lower for k in ["xrp", "리플"]):
            rule_key = "xrp_water_averaging"
        elif any(k in hint_lower for k in ["sol", "솔라나"]):
            rule_key = "sol_futures_liquidation"
        elif any(k in hint_lower for k in ["doge", "도지"]):
            rule_key = "doge_water_averaging"
        elif any(k in hint_lower for k in ["sei", "세이"]):
            rule_key = "sei_water_averaging"
        elif any(k in hint_lower for k in ["isa", "비과세", "분리과세"]):
            rule_key = "isa_tax_saving"
        elif any(k in hint_lower for k in ["연금저축", "세액공제"]):
            rule_key = "pension_savings_tax"
        elif "irp" in hint_lower:
            rule_key = "irp_retirement_tax"
        elif any(k in hint_lower for k in ["공모주", "청약", "ipo", "비례", "균등"]):
            rule_key = "ipo_allotment_profit"
        elif any(k in hint_lower for k in ["물타기", "평단", "본전", "dca", "averaging"]):
            rule_key = "water_averaging_dca"
        elif any(k in hint_lower for k in ["청산", "레버리지", "선물", "켈리", "kelly"]):
            rule_key = "leverage_liquidation_kelly"
        elif any(k in hint_lower for k in ["배당", "복리", "종합과세", "dividend"]):
            rule_key = "dividend_compound_tax"
        elif any(k in hint_lower for k in ["프리마켓", "애프터마켓", "환전", "premarket", "환산"]):
            rule_key = "us_stock_premarket_fx_calculator"
        elif any(k in hint_lower for k in ["mdd", "낙폭", "손실 복구", "drawdown"]):
            rule_key = "mdd_recovery_rate_simulator"
        else:
            rule_key = "overseas_stock_tax"

        rule = self.rules.get(rule_key, self.rules.get("overseas_stock_tax", {}))

        target_keyword = rule.get("name", "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터")
        formula_badge = rule.get("formula_badge", "양도세 = Max(0, 순수익 - 250만) × 22%")
        key_stat = rule.get("key_stat", "기본공제: 2,500,000원 | 총세율: 22%")
        sub_label = rule.get("sub_label", "2026 소득세법 제94조 손익통산 기준")
        english_slug = rule.get("english_slug", f"{rule_key.replace('_', '-')}-calculator")

        return {
            "rule_key": rule_key,
            "rule_info": rule,
            "target_keyword": target_keyword,
            "formula_badge": formula_badge,
            "key_stat": key_stat,
            "sub_label": sub_label,
            "english_slug": english_slug
        }

    def render_trading_saas_html(self, rule_key: str = "overseas_stock_tax") -> str:
        """Wise/Pieter Levels 역공학: 0ms 반응형 FinTech Micro-SaaS HTML 위젯 렌더링"""
        rule = self.rules.get(rule_key, {})
        fx_script = self.oracle.get_client_fx_script()

        if any(k in rule_key for k in ["dca", "averaging", "water"]):
            widget = self._render_water_averaging_widget(rule)
        elif any(k in rule_key for k in ["kelly", "liquidation", "futures", "decay", "leverage"]):
            widget = self._render_leverage_kelly_widget(rule)
        elif any(k in rule_key for k in ["dividend", "compound", "pension", "irp", "isa", "ipo"]):
            widget = self._render_dividend_compound_widget(rule)
        else:
            widget = self._render_overseas_tax_widget(rule)

        return widget + "\n" + fx_script

    def render_paper_trading_component(self, rule_key: str = "overseas_stock_tax") -> str:
        """TradingView-Grade 60fps Canvas Chart + Real-time Paper Trading Simulator"""
        from engine.fintech.chart_oracle import CanvasChartGenerator
        from engine.fintech.paper_trade_engine import PaperTradeEngine

        rule = self.rules.get(rule_key, {})
        ticker = rule.get("ticker", "NVDA")
        base_price = float(rule.get("base_price", 140.0))
        currency = rule.get("currency", "USD")

        chart_gen = CanvasChartGenerator()
        paper_engine = PaperTradeEngine()

        chart_html = chart_gen.generate_chart_html(ticker=ticker, initial_price=base_price, currency=currency)
        paper_html = paper_engine.generate_widget_html(ticker=ticker, initial_price=base_price, currency=currency)
        schema_json_ld = paper_engine.generate_schema_json_ld(ticker=ticker)

        return f"{chart_html}\n{paper_html}\n{schema_json_ld}"

    def _render_overseas_tax_widget(self, rule_info: Optional[Dict[str, Any]] = None) -> str:
        """해외주식 양도소득세 0ms 인터랙티브 위젯 (URL Hash 상태 저장 및 실시간 공유 탑재)"""
        rule_info = rule_info or {}
        w_title = rule_info.get("name", "2026 해외주식 양도소득세 손익통산 & 절세 시뮬레이터")
        if not w_title.startswith("📈"):
            w_title = f"📈 {w_title}"
        w_sub = rule_info.get("sub_label", "소득세법 제94조 기준 0ms 실시간 연산")
        ticker = rule_info.get("ticker", "")
        badge = f"FinTech Quant • {ticker}" if ticker else "FinTech Quant v2026"

        tpl = """
<!-- [FINTECH MICRO-SAAS] __WIDGET_TITLE__ -->
<div class="blogin-saas-container" style="background:#0b0f19; border:1px solid #1f293d; border-radius:18px; padding:24px; color:#e2e8f0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; max-width:100%; box-sizing:border-box; margin:28px 0; box-shadow:0 12px 40px rgba(0,0,0,0.45);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid #1e293b; padding-bottom:16px;">
    <div>
      <span style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; font-size:11px; font-weight:800; letter-spacing:1px; text-transform:uppercase; padding:4px 10px; border-radius:20px;">__BADGE_TEXT__</span>
      <h3 style="margin:8px 0 0 0; color:#f8fafc; font-size:22px; font-weight:800;">__WIDGET_TITLE__</h3>
    </div>
    <div style="text-align:right;">
      <span style="color:#94a3b8; font-size:12px;">__SUB_LABEL__</span>
    </div>
  </div>

  <!-- 2x2 대칭 입력 그리드 (360px 모바일 완벽 대응 반응형) -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:20px;">
    <!-- Input 1: 연간 총 실현 수익 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="trade_gain_input" style="font-size:12px; font-weight:700; color:#94a3b8;">1. 연간 총 실현수익 (KRW)</label>
        <span id="trade_gain_label" style="font-size:12px; font-weight:800; color:#38bdf8;">10,000,000원</span>
      </div>
      <input type="number" id="trade_gain_input" min="0" max="1000000000" step="100000" value="10000000" style="width:100%; box-sizing:border-box; background:#0b1120; color:#38bdf8; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
      <div style="display:flex; gap:6px; margin-top:8px;">
        <button type="button" class="trade-preset-btn" data-target="trade_gain_input" data-add="2500000" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">+250만(공제선)</button>
        <button type="button" class="trade-preset-btn" data-target="trade_gain_input" data-add="5000000" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">+500만</button>
        <button type="button" class="trade-preset-btn" data-target="trade_gain_input" data-add="10000000" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">+1,000만</button>
      </div>
    </div>

    <!-- Input 2: 연간 총 실현 손실 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="trade_loss_input" style="font-size:12px; font-weight:700; color:#94a3b8;">2. 연간 총 실현손실 (KRW)</label>
        <span id="trade_loss_label" style="font-size:12px; font-weight:800; color:#ef4444;">3,000,000원</span>
      </div>
      <input type="number" id="trade_loss_input" min="0" max="500000000" step="100000" value="3000000" style="width:100%; box-sizing:border-box; background:#0b1120; color:#f87171; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
      <div style="display:flex; gap:6px; margin-top:8px;">
        <button type="button" class="trade-preset-btn" data-target="trade_loss_input" data-val="0" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">0원(손실없음)</button>
        <button type="button" class="trade-preset-btn" data-target="trade_loss_input" data-add="1000000" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">+100만</button>
        <button type="button" class="trade-preset-btn" data-target="trade_loss_input" data-add="3000000" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">+300만</button>
      </div>
    </div>

    <!-- Input 3: 증권사 매매 수수료 및 제비용 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="trade_fee_input" style="font-size:12px; font-weight:700; color:#94a3b8;">3. 증권사 매매 수수료 (KRW)</label>
        <span id="trade_fee_label" style="font-size:12px; font-weight:800; color:#c084fc;">50,000원</span>
      </div>
      <input type="number" id="trade_fee_input" min="0" max="10000000" step="10000" value="50000" style="width:100%; box-sizing:border-box; background:#0b1120; color:#c084fc; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
      <div style="font-size:11px; color:#64748b; margin-top:6px;">* SEC Fee, 유관기관 제비용 포함</div>
    </div>

    <!-- Input 4: 결제 기준 환율 (USD/KRW) -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="trade_fx_input" style="font-size:12px; font-weight:700; color:#94a3b8;">4. 결제 기준 환율 (USD/KRW)</label>
        <span id="trade_fx_label" style="font-size:12px; font-weight:800; color:#f59e0b;">1,380.00원/$</span>
      </div>
      <input type="number" id="trade_fx_input" min="900" max="2500" step="10" value="1380" style="width:100%; box-sizing:border-box; background:#0b1120; color:#fbbf24; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
      <div style="font-size:11px; color:#64748b; margin-top:6px;">* 서울외국환중개 매매기준율 기준</div>
    </div>
  </div>

  <!-- 결과 메트릭스 Bento Box -->
  <div style="background:linear-gradient(145deg, #0f172a, #1e293b); border:1px solid #10b98140; border-radius:16px; padding:20px; margin-bottom:20px;">
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px; text-align:center;">
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">손익통산 순이익</div>
        <div id="trade_res_net_profit" style="font-size:18px; font-weight:900; color:#38bdf8; margin-top:4px;">6,950,000원</div>
        <div id="trade_res_net_usd" style="font-size:11px; color:#64748b; margin-top:2px;">$5,036.23</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">과세표준 (250만 공제)</div>
        <div id="trade_res_tax_base" style="font-size:18px; font-weight:900; color:#f59e0b; margin-top:4px;">4,450,000원</div>
        <div style="font-size:11px; color:#10b981; margin-top:2px;">-250만 원 공제 적용</div>
      </div>
      <div style="background:linear-gradient(135deg, #7f1d1d, #991b1b); border-radius:10px; padding:12px; border:1px solid #ef4444;">
        <div style="font-size:11px; color:#fecaca; font-weight:800;">총 납부 예상 세액 (22%)</div>
        <div id="trade_res_total_tax" style="font-size:20px; font-weight:900; color:#ffffff; margin-top:4px;">979,000원</div>
        <div style="font-size:11px; color:#fca5a5; margin-top:2px;">국세 20% + 지방세 2%</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">실효 세율 (Effective)</div>
        <div id="trade_res_effective_rate" style="font-size:18px; font-weight:900; color:#10b981; margin-top:4px;">9.79%</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">실현수익 대비 실부담</div>
      </div>
    </div>

    <!-- 순수익 대비 세금 점유율 Visual Breakdown Bar -->
    <div style="margin-top:18px;">
      <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:6px;">
        <span>수익 배분 구성: 세후 순수령액 vs 양도소득세</span>
        <span id="trade_bar_ratio_text" style="font-weight:700; color:#e2e8f0;">세후 순수익 85.9% | 세금 14.1%</span>
      </div>
      <div style="width:100%; height:16px; background:#0b1120; border-radius:10px; overflow:hidden; display:flex;">
        <div id="trade_bar_net" style="height:100%; background:linear-gradient(90deg, #10b981, #34d399); width:85.9%; transition:width 0.2s;"></div>
        <div id="trade_bar_tax" style="height:100%; background:linear-gradient(90deg, #ef4444, #f87171); width:14.1%; transition:width 0.2s;"></div>
      </div>
    </div>

    <!-- 세부 세목 및 세후 수령액 안내 바 -->
    <div style="margin-top:16px; background:#0b112080; border:1px solid #334155; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div style="font-size:12px; color:#cbd5e1;">
        <span>양도소득세(국세): <strong id="trade_res_national" style="color:#f87171;">890,000원</strong></span>
        <span style="margin:0 8px; color:#94a3b8;">|</span>
        <span>지방소득세: <strong id="trade_res_local" style="color:#f87171;">89,000원</strong></span>
        <span style="margin:0 8px; color:#94a3b8;">|</span>
        <span>세후 실수령액: <strong id="trade_res_take_home" style="color:#34d399;">5,971,000원</strong></span>
      </div>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        <button id="trade_copy_btn" type="button" style="background:#10b981; color:#fff; border:none; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          📋 계산 결과 복사
        </button>
        <button id="trade_share_btn" type="button" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf880; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          🔗 결과 공유 링크 복사
        </button>
      </div>
    </div>
  </div>

  <!-- 제휴 증권사/플랫폼 연계 안내 CTA 슬롯 -->
  <div style="background:#131c31; border:1px dashed #3b82f680; border-radius:12px; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
    <div style="font-size:12px; color:#93c5fd;">
      <strong>💡 2026 해외주식 절세 팁:</strong> 12월 말 결제일 전 평가손실 종목을 손익상계 매도하면 과세표준을 즉시 낮춰 양도세를 합법적으로 절감할 수 있습니다.
    </div>
    <div style="font-size:11px; color:#60a5fa; font-weight:700;">
      신고 기간: 매년 5월 1일 ~ 5월 31일
    </div>
  </div>
</div>

<script>
(function() {
  const gainInput = document.getElementById('trade_gain_input');
  const lossInput = document.getElementById('trade_loss_input');
  const feeInput = document.getElementById('trade_fee_input');
  const fxInput = document.getElementById('trade_fx_input');

  const gainLabel = document.getElementById('trade_gain_label');
  const lossLabel = document.getElementById('trade_loss_label');
  const feeLabel = document.getElementById('trade_fee_label');
  const fxLabel = document.getElementById('trade_fx_label');

  const resNetProfit = document.getElementById('trade_res_net_profit');
  const resNetUsd = document.getElementById('trade_res_net_usd');
  const resTaxBase = document.getElementById('trade_res_tax_base');
  const resTotalTax = document.getElementById('trade_res_total_tax');
  const resEffectiveRate = document.getElementById('trade_res_effective_rate');
  const resNational = document.getElementById('trade_res_national');
  const resLocal = document.getElementById('trade_res_local');
  const resTakeHome = document.getElementById('trade_res_take_home');

  const barNet = document.getElementById('trade_bar_net');
  const barTax = document.getElementById('trade_bar_tax');
  const barRatioText = document.getElementById('trade_bar_ratio_text');
  const copyBtn = document.getElementById('trade_copy_btn');
  const shareBtn = document.getElementById('trade_share_btn');

  function syncHash() {
    try {
      const p = new URLSearchParams();
      p.set('gain', gainInput.value);
      p.set('loss', lossInput.value);
      p.set('fee', feeInput.value);
      p.set('fx', fxInput.value);
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', '#' + p.toString());
      }
    } catch (e) {}
  }

  function calculateTax() {
    let gain = parseFloat(gainInput.value);
    let loss = parseFloat(lossInput.value);
    let fee = parseFloat(feeInput.value);
    let fx = parseFloat(fxInput.value);

    gain = (isNaN(gain) || gain < 0) ? 0 : gain;
    loss = (isNaN(loss) || loss < 0) ? 0 : loss;
    fee = (isNaN(fee) || fee < 0) ? 0 : fee;
    fx = (isNaN(fx) || fx <= 0) ? 1380 : fx;

    gainLabel.textContent = Math.round(gain).toLocaleString('ko-KR') + '원';
    lossLabel.textContent = Math.round(loss).toLocaleString('ko-KR') + '원';
    feeLabel.textContent = Math.round(fee).toLocaleString('ko-KR') + '원';
    fxLabel.textContent = Number(fx).toFixed(2) + '원/$';

    const grossProfit = gain - loss - fee;
    const netProfit = Math.max(0, grossProfit);

    const BASIC_DEDUCTION = 2500000;
    const taxBase = Math.max(0, netProfit - BASIC_DEDUCTION);

    const nationalTax = Math.round(taxBase * 0.20);
    const localTax = Math.round(taxBase * 0.02);
    const totalTax = nationalTax + localTax;

    const effectiveRate = gain > 0 ? ((totalTax / gain) * 100) : 0.0;
    const takeHome = Math.max(0, netProfit - totalTax);
    const netUsd = fx > 0 ? (netProfit / fx) : 0;

    resNetProfit.textContent = Math.round(netProfit).toLocaleString('ko-KR') + '원';
    resNetUsd.textContent = '$' + Number(netUsd).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    resTaxBase.textContent = Math.round(taxBase).toLocaleString('ko-KR') + '원';
    resTotalTax.textContent = Math.round(totalTax).toLocaleString('ko-KR') + '원';
    resEffectiveRate.textContent = Number(effectiveRate).toFixed(2) + '%';
    resNational.textContent = Math.round(nationalTax).toLocaleString('ko-KR') + '원';
    resLocal.textContent = Math.round(localTax).toLocaleString('ko-KR') + '원';
    resTakeHome.textContent = Math.round(takeHome).toLocaleString('ko-KR') + '원';

    let netShare = 100;
    let taxShare = 0;
    if (netProfit > 0) {
      taxShare = Math.min(100, (totalTax / netProfit) * 100);
      netShare = Math.max(0, 100 - taxShare);
    }
    barNet.style.width = Number(netShare).toFixed(1) + '%';
    barTax.style.width = Number(taxShare).toFixed(1) + '%';
    barRatioText.textContent = '세후 순수익 ' + Number(netShare).toFixed(1) + '% | 세금 ' + Number(taxShare).toFixed(1) + '%';

    syncHash();
  }

  const presetBtns = document.querySelectorAll('.trade-preset-btn');
  presetBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const targetId = btn.getAttribute('data-target');
      const addVal = btn.getAttribute('data-add');
      const setVal = btn.getAttribute('data-val');
      const inputEl = document.getElementById(targetId);
      if (inputEl) {
        if (setVal !== null) {
          inputEl.value = setVal;
        } else if (addVal !== null) {
          const cur = parseFloat(inputEl.value) || 0;
          inputEl.value = cur + parseFloat(addVal);
        }
        calculateTax();
      }
    });
  });

  [gainInput, lossInput, feeInput, fxInput].forEach(function(el) {
    if (el) {
      el.addEventListener('input', calculateTax);
      el.addEventListener('change', calculateTax);
    }
  });

  if (copyBtn) {
    copyBtn.addEventListener('click', function() {
      const text = "[2026 해외주식 양도소득세 시뮬레이션 결과]\\n" +
                   "• 연간 실현수익: " + gainLabel.textContent + "\\n" +
                   "• 연간 실현손실: " + lossLabel.textContent + "\\n" +
                   "• 통산 순이익: " + resNetProfit.textContent + " (" + resNetUsd.textContent + ")\\n" +
                   "• 과세표준(공제후): " + resTaxBase.textContent + "\\n" +
                   "• 납부 예상 세액: " + resTotalTax.textContent + " (실효세율: " + resEffectiveRate.textContent + ")\\n" +
                   "• 세후 실수령액: " + resTakeHome.textContent + "\\n" +
                   "※ 기준: 소득세법 제94조 (국세 20% + 지방세 2%, 기본공제 250만원)";
      navigator.clipboard.writeText(text).then(function() {
        copyBtn.textContent = "✅ 복사 완료!";
        setTimeout(function() { copyBtn.textContent = "📋 계산 결과 복사"; }, 2000);
      });
    });
  }

  if (shareBtn) {
    shareBtn.addEventListener('click', function() {
      const shareUrl = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(shareUrl).then(function() {
          shareBtn.textContent = "✅ 공유 링크 복사됨!";
          setTimeout(function() { shareBtn.textContent = "🔗 결과 공유 링크 복사"; }, 2000);
        }).catch(function() { fallbackShare(shareUrl); });
      } else {
        fallbackShare(shareUrl);
      }
    });
  }

  function fallbackShare(url) {
    const ta = document.createElement('textarea');
    ta.value = url;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      if (shareBtn) shareBtn.textContent = "✅ 공유 링크 복사됨!";
    } catch (e) {
      if (shareBtn) shareBtn.textContent = "복사 실패";
    }
    document.body.removeChild(ta);
    setTimeout(function() { if (shareBtn) shareBtn.textContent = "🔗 결과 공유 링크 복사"; }, 2000);
  }

  // URL Hash 파라미터 사전 로드
  try {
    if (window.location.hash && window.location.hash.length > 1) {
      const params = new URLSearchParams(window.location.hash.substring(1));
      if (params.has('gain')) gainInput.value = params.get('gain');
      if (params.has('loss')) lossInput.value = params.get('loss');
      if (params.has('fee')) feeInput.value = params.get('fee');
      if (params.has('fx')) fxInput.value = params.get('fx');
    }
  } catch (e) {}

  calculateTax();
})();
</script>
"""
        return tpl.replace("__WIDGET_TITLE__", w_title).replace("__SUB_LABEL__", w_sub).replace("__BADGE_TEXT__", badge)

    def _render_water_averaging_widget(self, rule_info: Optional[Dict[str, Any]] = None) -> str:
        """주식·코인 물타기 평단가 & 본전 탈출 역산 0ms 인터랙티브 위젯 (URL Hash 상태 저장 및 공유)"""
        rule_info = rule_info or {}
        w_title = rule_info.get("name", "주식·코인 물타기 평단가 & 본전 탈출 역산 시뮬레이터")
        if not w_title.startswith("📉"):
            w_title = f"📉 {w_title}"
        w_sub = rule_info.get("sub_label", "수수료 반영 실질 BEP 탈출가 0ms 역산")
        ticker = rule_info.get("ticker", "")
        badge = f"DCA Quant • {ticker}" if ticker else "DCA Quant v2026"
        def_p = rule_info.get("default_price", 50000)
        try:
            def_p = float(def_p)
        except Exception:
            def_p = 50000.0
        init_p1 = int(round(def_p * 1.25)) if def_p > 10 else round(def_p * 1.25, 4)
        init_p2 = int(round(def_p)) if def_p > 10 else round(def_p, 4)

        tpl = f"""
<!-- [FINTECH MICRO-SAAS] __WIDGET_TITLE__ -->
<div class="blogin-saas-container" style="background:#0b0f19; border:1px solid #1f293d; border-radius:18px; padding:24px; color:#e2e8f0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; max-width:100%; box-sizing:border-box; margin:28px 0; box-shadow:0 12px 40px rgba(0,0,0,0.45);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid #1e293b; padding-bottom:16px;">
    <div>
      <span style="background:linear-gradient(135deg, #3b82f6, #1d4ed8); color:#fff; font-size:11px; font-weight:800; letter-spacing:1px; text-transform:uppercase; padding:4px 10px; border-radius:20px;">__BADGE_TEXT__</span>
      <h3 style="margin:8px 0 0 0; color:#f8fafc; font-size:22px; font-weight:800;">__WIDGET_TITLE__</h3>
    </div>
    <div style="text-align:right;">
      <span style="color:#94a3b8; font-size:12px;">__SUB_LABEL__</span>
    </div>
  </div>

  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:20px;">
    <!-- Input 1: 기존 보유 평단가 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="dca_price1_input" style="font-size:12px; font-weight:700; color:#94a3b8;">1. 기존 보유 평단가 (KRW)</label>
        <span id="dca_price1_label" style="font-size:12px; font-weight:800; color:#ef4444;">{init_p1:,}원</span>
      </div>
      <input type="number" id="dca_price1_input" min="0" max="1000000000" step="100" value="{init_p1}" style="width:100%; box-sizing:border-box; background:#0b1120; color:#f87171; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>

    <!-- Input 2: 기존 보유 수량 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="dca_qty1_input" style="font-size:12px; font-weight:700; color:#94a3b8;">2. 기존 보유 수량 (주/개)</label>
        <span id="dca_qty1_label" style="font-size:12px; font-weight:800; color:#38bdf8;">100주</span>
      </div>
      <input type="number" id="dca_qty1_input" min="1" max="10000000" step="1" value="100" style="width:100%; box-sizing:border-box; background:#0b1120; color:#38bdf8; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>

    <!-- Input 3: 현재 주가 / 추가 매수가 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="dca_price2_input" style="font-size:12px; font-weight:700; color:#94a3b8;">3. 현재가 / 추가 매수가 (KRW)</label>
        <span id="dca_price2_label" style="font-size:12px; font-weight:800; color:#f59e0b;">{init_p2:,}원 (-20.0%)</span>
      </div>
      <input type="number" id="dca_price2_input" min="0" max="1000000000" step="100" value="{init_p2}" style="width:100%; box-sizing:border-box; background:#0b1120; color:#fbbf24; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>

    <!-- Input 4: 추가 매수 수량 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="dca_qty2_input" style="font-size:12px; font-weight:700; color:#94a3b8;">4. 추가 매수 수량 (주/개)</label>
        <span id="dca_qty2_label" style="font-size:12px; font-weight:800; color:#10b981;">100주 (1:1 매수)</span>
      </div>
      <input type="number" id="dca_qty2_input" min="0" max="10000000" step="1" value="100" style="width:100%; box-sizing:border-box; background:#0b1120; color:#34d399; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
      <div style="display:flex; gap:6px; margin-top:8px;">
        <button type="button" class="dca-ratio-btn" data-ratio="1" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">1:1 물타기</button>
        <button type="button" class="dca-ratio-btn" data-ratio="2" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">1:2 물타기</button>
        <button type="button" class="dca-ratio-btn" data-ratio="3" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">1:3 물타기</button>
      </div>
    </div>
  </div>

  <!-- 결과 메트릭스 Bento Box -->
  <div style="background:linear-gradient(145deg, #0f172a, #1e293b); border:1px solid #3b82f640; border-radius:16px; padding:20px; margin-bottom:20px;">
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px; text-align:center;">
      <div style="background:linear-gradient(135deg, #1e3a8a, #0369a1); border-radius:10px; padding:12px; border:1px solid #38bdf8;">
        <div style="font-size:11px; color:#e0f2fe; font-weight:800;">신규 최종 평단가</div>
        <div id="dca_res_avg_price" style="font-size:20px; font-weight:900; color:#38bdf8; margin-top:4px;">40,000원</div>
        <div id="dca_res_cut_pct" style="font-size:11px; color:#a5f3fc; margin-top:2px;">평단가 -20.00% 인하</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">추가 필요 자금</div>
        <div id="dca_res_add_budget" style="font-size:18px; font-weight:900; color:#fbbf24; margin-top:4px;">3,000,000원</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">신규 투입 투자금</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">본전 탈출 필요 반등률</div>
        <div id="dca_res_bep_rebound" style="font-size:18px; font-weight:900; color:#10b981; margin-top:4px;">+33.40%</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">수수료 0.05% 반영</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">총 보유 자산 합계</div>
        <div id="dca_res_total_invest" style="font-size:18px; font-weight:900; color:#cbd5e1; margin-top:4px;">8,000,000원</div>
        <div id="dca_res_total_qty" style="font-size:11px; color:#64748b; margin-top:2px;">총 200주 보유</div>
      </div>
    </div>

    <!-- 투자금 구성 비율 Visual Breakdown Bar -->
    <div style="margin-top:18px;">
      <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:6px;">
        <span>투자금 포트폴리오 비중: 기존 투자금 vs 신규 물타기 투입 자금</span>
        <span id="dca_bar_ratio_text" style="font-weight:700; color:#e2e8f0;">기존 62.5% | 신규 37.5%</span>
      </div>
      <div style="width:100%; height:16px; background:#0b1120; border-radius:10px; overflow:hidden; display:flex;">
        <div id="dca_bar_orig" style="height:100%; background:linear-gradient(90deg, #ef4444, #f87171); width:62.5%; transition:width 0.2s;"></div>
        <div id="dca_bar_new" style="height:100%; background:linear-gradient(90deg, #3b82f6, #60a5fa); width:37.5%; transition:width 0.2s;"></div>
      </div>
    </div>

    <div style="margin-top:16px; background:#0b112080; border:1px solid #334155; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div style="font-size:12px; color:#cbd5e1;">
        <span>물타기 전 본전 반등률: <strong id="dca_orig_rebound" style="color:#f87171;">+66.67%</strong></span>
        <span style="margin:0 8px; color:#94a3b8;">➔</span>
        <span>물타기 후 반등률 단축: <strong id="dca_cut_rebound" style="color:#34d399;">+33.40% (33.27%p 단축)</strong></span>
      </div>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        <button id="dca_copy_btn" type="button" style="background:#2563eb; color:#fff; border:none; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          📋 결과 복사
        </button>
        <button id="dca_share_btn" type="button" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf880; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          🔗 결과 공유 링크 복사
        </button>
      </div>
    </div>
  </div>

  <div style="background:#131c31; border:1px dashed #3b82f680; border-radius:12px; padding:14px 18px; font-size:12px; color:#93c5fd;">
    <strong>💡 퀀트 리스크 관리 팁:</strong> 하락 추세가 지속되는 종목에서 무제한 물타기는 파산 위험을 극대화합니다. 지지선 확인 후 분할 매수하고 총 시드의 20% 이내로 포지션 비중을 통제하십시오.
  </div>
</div>

<script>
(function() {{
  const p1 = document.getElementById('dca_price1_input');
  const q1 = document.getElementById('dca_qty1_input');
  const p2 = document.getElementById('dca_price2_input');
  const q2 = document.getElementById('dca_qty2_input');

  const l_p1 = document.getElementById('dca_price1_label');
  const l_q1 = document.getElementById('dca_qty1_label');
  const l_p2 = document.getElementById('dca_price2_label');
  const l_q2 = document.getElementById('dca_qty2_label');

  const r_avg = document.getElementById('dca_res_avg_price');
  const r_cut = document.getElementById('dca_res_cut_pct');
  const r_add = document.getElementById('dca_res_add_budget');
  const r_bep = document.getElementById('dca_res_bep_rebound');
  const r_tot = document.getElementById('dca_res_total_invest');
  const r_tot_q = document.getElementById('dca_res_total_qty');

  const b_orig = document.getElementById('dca_bar_orig');
  const b_new = document.getElementById('dca_bar_new');
  const b_text = document.getElementById('dca_bar_ratio_text');

  const r_orig_reb = document.getElementById('dca_orig_rebound');
  const r_cut_reb = document.getElementById('dca_cut_rebound');
  const copyBtn = document.getElementById('dca_copy_btn');
  const shareBtn = document.getElementById('dca_share_btn');

  function syncHash() {{
    try {{
      const p = new URLSearchParams();
      p.set('p1', p1.value);
      p.set('q1', q1.value);
      p.set('p2', p2.value);
      p.set('q2', q2.value);
      if (window.history && window.history.replaceState) {{
        window.history.replaceState(null, '', '#' + p.toString());
      }}
    }} catch (e) {{}}
  }}

  function calculateDCA() {{
    let price1 = parseFloat(p1.value) || 0;
    let qty1 = parseFloat(q1.value) || 0;
    let price2 = parseFloat(p2.value) || 0;
    let qty2 = parseFloat(q2.value) || 0;

    price1 = Math.max(0, price1);
    qty1 = Math.max(0, qty1);
    price2 = Math.max(0, price2);
    qty2 = Math.max(0, qty2);

    const origDropPct = price1 > 0 ? ((price2 - price1) / price1 * 100) : 0;
    l_p1.textContent = Math.round(price1).toLocaleString('ko-KR') + '원';
    l_q1.textContent = Math.round(qty1).toLocaleString('ko-KR') + '주';
    l_p2.textContent = Math.round(price2).toLocaleString('ko-KR') + '원 (' + Number(origDropPct).toFixed(1) + '%)';
    l_q2.textContent = Math.round(qty2).toLocaleString('ko-KR') + '주';

    const origTotal = price1 * qty1;
    const addTotal = price2 * qty2;
    const totalQty = qty1 + qty2;
    const totalInvest = origTotal + addTotal;

    const newAvg = totalQty > 0 ? (totalInvest / totalQty) : 0;
    const cutPct = price1 > 0 ? ((price1 - newAvg) / price1 * 100) : 0;

    const feeRate = 0.0005; // 0.05%
    const origRebound = price2 > 0 ? (((price1 * (1 + feeRate)) / price2) - 1) * 100 : 0;
    const bepRebound = price2 > 0 ? (((newAvg * (1 + feeRate)) / price2) - 1) * 100 : 0;
    const reducedRebound = Math.max(0, origRebound - bepRebound);

    r_avg.textContent = Math.round(newAvg).toLocaleString('ko-KR') + '원';
    r_cut.textContent = '평단가 -' + Number(cutPct).toFixed(2) + '% 인하';
    r_add.textContent = Math.round(addTotal).toLocaleString('ko-KR') + '원';
    r_bep.textContent = '+' + Number(Math.max(0, bepRebound)).toFixed(2) + '%';
    r_tot.textContent = Math.round(totalInvest).toLocaleString('ko-KR') + '원';
    r_tot_q.textContent = '총 ' + Math.round(totalQty).toLocaleString('ko-KR') + '주 보유';

    let origShare = 50;
    let newShare = 50;
    if (totalInvest > 0) {{
      origShare = (origTotal / totalInvest) * 100;
      newShare = (addTotal / totalInvest) * 100;
    }}
    b_orig.style.width = Number(origShare).toFixed(1) + '%';
    b_new.style.width = Number(newShare).toFixed(1) + '%';
    b_text.textContent = '기존 ' + Number(origShare).toFixed(1) + '% | 신규 ' + Number(newShare).toFixed(1) + '%';

    r_orig_reb.textContent = '+' + Number(origRebound).toFixed(2) + '%';
    r_cut_reb.textContent = '+' + Number(bepRebound).toFixed(2) + '% (' + Number(reducedRebound).toFixed(2) + '%p 단축)';

    syncHash();
  }}

  const ratioBtns = document.querySelectorAll('.dca-ratio-btn');
  ratioBtns.forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      const mult = parseFloat(btn.getAttribute('data-ratio')) || 1;
      const q1Val = parseFloat(q1.value) || 0;
      q2.value = Math.round(q1Val * mult);
      calculateDCA();
    }});
  }});

  [p1, q1, p2, q2].forEach(function(el) {{
    if (el) {{
      el.addEventListener('input', calculateDCA);
      el.addEventListener('change', calculateDCA);
    }}
  }});

  if (copyBtn) {{
    copyBtn.addEventListener('click', function() {{
      const text = "[물타기 평단가 & 본전 탈출 시뮬레이션 결과]\\n" +
                   "• 기존 평단가: " + l_p1.textContent + " (" + l_q1.textContent + ")\\n" +
                   "• 추가 매수가: " + l_p2.textContent + " (" + l_q2.textContent + ")\\n" +
                   "• 신규 최종 평단가: " + r_avg.textContent + " (" + r_cut.textContent + ")\\n" +
                   "• 추가 필요 자금: " + r_add.textContent + "\\n" +
                   "• 본전 탈출 필요 반등률: " + r_bep.textContent + "\\n" +
                   "• 총 보유 자산: " + r_tot.textContent + " (" + r_tot_q.textContent + ")";
      navigator.clipboard.writeText(text).then(function() {{
        copyBtn.textContent = "✅ 복사 완료!";
        setTimeout(function() {{ copyBtn.textContent = "📋 결과 복사"; }}, 2000);
      }});
    }});
  }}

  if (shareBtn) {{
    shareBtn.addEventListener('click', function() {{
      const shareUrl = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(shareUrl).then(function() {{
          shareBtn.textContent = "✅ 공유 링크 복사됨!";
          setTimeout(function() {{ shareBtn.textContent = "🔗 결과 공유 링크 복사"; }}, 2000);
        }}).catch(function() {{ fallbackShare(shareUrl); }});
      }} else {{
        fallbackShare(shareUrl);
      }}
    }});
  }}

  function fallbackShare(url) {{
    const ta = document.createElement('textarea');
    ta.value = url;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {{
      document.execCommand('copy');
      if (shareBtn) shareBtn.textContent = "✅ 공유 링크 복사됨!";
    }} catch (e) {{
      if (shareBtn) shareBtn.textContent = "복사 실패";
    }}
    document.body.removeChild(ta);
    setTimeout(function() {{ if (shareBtn) shareBtn.textContent = "🔗 결과 공유 링크 복사"; }}, 2000);
  }}

  // URL Hash 파라미터 사전 로드
  try {{
    if (window.location.hash && window.location.hash.length > 1) {{
      const params = new URLSearchParams(window.location.hash.substring(1));
      if (params.has('p1')) p1.value = params.get('p1');
      if (params.has('q1')) q1.value = params.get('q1');
      if (params.has('p2')) p2.value = params.get('p2');
      if (params.has('q2')) q2.value = params.get('q2');
    }}
  }} catch (e) {{}}

  calculateDCA();
}})();
</script>
"""
        return tpl.replace("__WIDGET_TITLE__", w_title).replace("__SUB_LABEL__", w_sub).replace("__BADGE_TEXT__", badge)

    def _render_leverage_kelly_widget(self, rule_info: Optional[Dict[str, Any]] = None) -> str:
        """선물 레버리지 청산가 & 켈리 공식 0ms 인터랙티브 위젯 (URL Hash 상태 저장 및 공유)"""
        rule_info = rule_info or {}
        w_title = rule_info.get("name", "선물 레버리지 청산가 & 켈리 공식 포지션 사이징 계산기")
        if not w_title.startswith("⚡"):
            w_title = f"⚡ {w_title}"
        w_sub = rule_info.get("sub_label", "격리 마진 유지증거금율 0.5% 기반 0ms 실시간 연산")
        ticker = rule_info.get("ticker", "")
        badge = f"Derivatives Risk • {ticker}" if ticker else "Derivatives Risk v2026"
        def_entry = rule_info.get("default_price", 60000)
        try:
            def_entry = float(def_entry)
        except Exception:
            def_entry = 60000.0
        def_lev = int(rule_info.get("default_leverage", 20))
        init_entry_str = f"{def_entry:,.2f}" if def_entry < 1000 else f"{int(def_entry):,}"

        tpl = f"""
<!-- [FINTECH MICRO-SAAS] __WIDGET_TITLE__ -->
<div class="blogin-saas-container" style="background:#0b0f19; border:1px solid #1f293d; border-radius:18px; padding:24px; color:#e2e8f0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; max-width:100%; box-sizing:border-box; margin:28px 0; box-shadow:0 12px 40px rgba(0,0,0,0.45);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid #1e293b; padding-bottom:16px;">
    <div>
      <span style="background:linear-gradient(135deg, #ef4444, #b91c1c); color:#fff; font-size:11px; font-weight:800; letter-spacing:1px; text-transform:uppercase; padding:4px 10px; border-radius:20px;">__BADGE_TEXT__</span>
      <h3 style="margin:8px 0 0 0; color:#f8fafc; font-size:22px; font-weight:800;">__WIDGET_TITLE__</h3>
    </div>
    <div style="text-align:right;">
      <span style="color:#94a3b8; font-size:12px;">__SUB_LABEL__</span>
    </div>
  </div>

  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:20px;">
    <!-- Input 1: 진입 가격 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="lev_entry_input" style="font-size:12px; font-weight:700; color:#94a3b8;">1. 포지션 진입 가격 (USDT)</label>
        <span id="lev_entry_label" style="font-size:12px; font-weight:800; color:#38bdf8;">{init_entry_str} USDT</span>
      </div>
      <input type="number" id="lev_entry_input" min="0" max="10000000" step="10" value="{def_entry}" style="width:100%; box-sizing:border-box; background:#0b1120; color:#38bdf8; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>

    <!-- Input 2: 포지션 방향 및 레버리지 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="lev_leverage_input" style="font-size:12px; font-weight:700; color:#94a3b8;">2. 레버리지 배율 (Leverage)</label>
        <span id="lev_leverage_label" style="font-size:12px; font-weight:800; color:#f59e0b;">{def_lev}x 레버리지</span>
      </div>
      <input type="range" id="lev_leverage_input" min="1" max="125" step="1" value="{def_lev}" style="width:100%; accent-color:#f59e0b; cursor:pointer;" />
      <div style="display:flex; gap:8px; margin-top:8px;">
        <select id="lev_side_select" style="background:#0b1120; color:#e2e8f0; border:1px solid #334155; border-radius:6px; padding:4px 8px; font-size:12px; font-weight:700;">
          <option value="long">롱 (Long / 매수 포지션)</option>
          <option value="short">숏 (Short / 매도 포지션)</option>
        </select>
      </div>
    </div>

    <!-- Input 3: 총 시드 머니 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="lev_seed_input" style="font-size:12px; font-weight:700; color:#94a3b8;">3. 총 운용 시드 (Seed Money, USDT)</label>
        <span id="lev_seed_label" style="font-size:12px; font-weight:800; color:#10b981;">10,000 USDT</span>
      </div>
      <input type="number" id="lev_seed_input" min="0" max="100000000" step="500" value="10000" style="width:100%; box-sizing:border-box; background:#0b1120; color:#34d399; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>

    <!-- Input 4: 승률 및 손익비 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label style="font-size:12px; font-weight:700; color:#94a3b8;">4. 승률 & 손익비 (Kelly Param)</label>
        <span id="lev_kelly_param_label" style="font-size:12px; font-weight:800; color:#c084fc;">승률 55% | 손익비 2.0</span>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
        <input type="number" id="lev_win_input" min="10" max="95" step="1" value="55" placeholder="승률(%)" style="background:#0b1120; color:#e2e8f0; border:1px solid #334155; border-radius:6px; padding:6px; font-size:13px;" />
        <input type="number" id="lev_rr_input" min="0.5" max="10" step="0.1" value="2.0" placeholder="손익비" style="background:#0b1120; color:#e2e8f0; border:1px solid #334155; border-radius:6px; padding:6px; font-size:13px;" />
      </div>
    </div>
  </div>

  <!-- 결과 메트릭스 Bento Box -->
  <div style="background:linear-gradient(145deg, #0f172a, #1e293b); border:1px solid #ef444440; border-radius:16px; padding:20px; margin-bottom:20px;">
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px; text-align:center;">
      <div style="background:linear-gradient(135deg, #7f1d1d, #991b1b); border-radius:10px; padding:12px; border:1px solid #ef4444;">
        <div style="font-size:11px; color:#fecaca; font-weight:800;">강제 청산 예상가</div>
        <div id="lev_res_liq_price" style="font-size:20px; font-weight:900; color:#ffffff; margin-top:4px;">57,300.00</div>
        <div id="lev_res_liq_dist" style="font-size:11px; color:#fca5a5; margin-top:2px;">남은 거리: -4.50%</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">켈리 베팅 공식 (Kelly %)</div>
        <div id="lev_res_kelly_pct" style="font-size:18px; font-weight:900; color:#f59e0b; margin-top:4px;">32.50%</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">이론상 최적 기대값</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">권장 Half-Kelly 비중</div>
        <div id="lev_res_half_kelly_pct" style="font-size:18px; font-weight:900; color:#10b981; margin-top:4px;">16.25%</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">파산 위험 방어 (안전형)</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">1회 권장 진입 증거금</div>
        <div id="lev_res_bet_amount" style="font-size:18px; font-weight:900; color:#38bdf8; margin-top:4px;">1,625.00 USDT</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">시드 대비 안전 한도</div>
      </div>
    </div>

    <!-- 청산 안전 버퍼 Visual Breakdown Bar -->
    <div style="margin-top:18px;">
      <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:6px;">
        <span>청산 위험 노출도: 안전 마진 버퍼 vs 즉각 청산 위험 구간</span>
        <span id="lev_bar_ratio_text" style="font-weight:700; color:#e2e8f0;">안전 마진 95.5% | 청산 위험 4.5%</span>
      </div>
      <div style="width:100%; height:16px; background:#0b1120; border-radius:10px; overflow:hidden; display:flex;">
        <div id="lev_bar_safe" style="height:100%; background:linear-gradient(90deg, #10b981, #34d399); width:95.5%; transition:width 0.2s;"></div>
        <div id="lev_bar_risk" style="height:100%; background:linear-gradient(90deg, #ef4444, #f87171); width:4.5%; transition:width 0.2s;"></div>
      </div>
    </div>

    <div style="margin-top:16px; background:#0b112080; border:1px solid #334155; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div style="font-size:12px; color:#cbd5e1;">
        <span>포지션 총 규모: <strong id="lev_notional_size" style="color:#38bdf8;">32,500.00 USDT</strong></span>
        <span style="margin:0 8px; color:#94a3b8;">|</span>
        <span>최대 감내 손실: <strong id="lev_max_loss" style="color:#f87171;">-100% (-1,625 USDT)</strong></span>
      </div>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        <button id="lev_copy_btn" type="button" style="background:#dc2626; color:#fff; border:none; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          📋 결과 복사
        </button>
        <button id="lev_share_btn" type="button" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf880; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          🔗 결과 공유 링크 복사
        </button>
      </div>
    </div>
  </div>

  <div style="background:#131c31; border:1px dashed #ef444480; border-radius:12px; padding:14px 18px; font-size:12px; color:#fca5a5;">
    <strong>⚠️ 레버리지 파산 경고:</strong> 20배 이상 고레버리지 거래 시 시장 변동성 5% 이내에서 전액 강제 청산될 수 있습니다. 켈리 공식이 권장하는 포지션 사이징을 초과하여 올인 베팅하지 마십시오.
  </div>
</div>

<script>
(function() {{
  const entryInput = document.getElementById('lev_entry_input');
  const levInput = document.getElementById('lev_leverage_input');
  const sideSelect = document.getElementById('lev_side_select');
  const seedInput = document.getElementById('lev_seed_input');
  const winInput = document.getElementById('lev_win_input');
  const rrInput = document.getElementById('lev_rr_input');

  const entryLabel = document.getElementById('lev_entry_label');
  const levLabel = document.getElementById('lev_leverage_label');
  const seedLabel = document.getElementById('lev_seed_label');
  const kellyParamLabel = document.getElementById('lev_kelly_param_label');

  const resLiqPrice = document.getElementById('lev_res_liq_price');
  const resLiqDist = document.getElementById('lev_res_liq_dist');
  const resKellyPct = document.getElementById('lev_res_kelly_pct');
  const resHalfKelly = document.getElementById('lev_res_half_kelly_pct');
  const resBetAmount = document.getElementById('lev_res_bet_amount');

  const barSafe = document.getElementById('lev_bar_safe');
  const barRisk = document.getElementById('lev_bar_risk');
  const barRatioText = document.getElementById('lev_bar_ratio_text');

  const notionalSize = document.getElementById('lev_notional_size');
  const maxLoss = document.getElementById('lev_max_loss');
  const copyBtn = document.getElementById('lev_copy_btn');
  const shareBtn = document.getElementById('lev_share_btn');

  function syncHash() {{
    try {{
      const p = new URLSearchParams();
      p.set('entry', entryInput.value);
      p.set('lev', levInput.value);
      p.set('side', sideSelect.value);
      p.set('seed', seedInput.value);
      p.set('win', winInput.value);
      p.set('rr', rrInput.value);
      if (window.history && window.history.replaceState) {{
        window.history.replaceState(null, '', '#' + p.toString());
      }}
    }} catch (e) {{}}
  }}

  function calculateLeverage() {{
    let entry = parseFloat(entryInput.value) || 0;
    let lev = parseFloat(levInput.value) || 1;
    let seed = parseFloat(seedInput.value) || 0;
    let win = (parseFloat(winInput.value) || 50) / 100;
    let rr = parseFloat(rrInput.value) || 1.0;
    const side = sideSelect.value || "long";

    entry = Math.max(0, entry);
    lev = Math.max(1, Math.min(125, lev));
    seed = Math.max(0, seed);
    win = Math.max(0.01, Math.min(0.99, win));
    rr = Math.max(0.1, rr);

    entryLabel.textContent = Number(entry).toFixed(2) + " USDT";
    levLabel.textContent = lev + "x 레버리지";
    seedLabel.textContent = Math.round(seed).toLocaleString('ko-KR') + " USDT";
    kellyParamLabel.textContent = "승률 " + Math.round(win * 100) + "% | 손익비 " + Number(rr).toFixed(1);

    const mmr = 0.005; // 0.5% 유지증거금율
    let liqPrice = 0;
    let distPct = 0;

    if (side === "long") {{
      liqPrice = Math.max(0, entry * (1 - (1 / lev) + mmr));
      distPct = entry > 0 ? ((entry - liqPrice) / entry) * 100 : 0;
    }} else {{
      liqPrice = entry * (1 + (1 / lev) - mmr);
      distPct = entry > 0 ? ((liqPrice - entry) / entry) * 100 : 0;
    }}

    // 켈리 공식: K = (W * R - (1 - W)) / R
    const kelly = ((win * rr) - (1 - win)) / rr;
    const kellyPct = Math.max(0, Math.min(100, kelly * 100));
    const halfKellyPct = kellyPct * 0.5;
    const betAmount = seed * (halfKellyPct / 100);
    const notional = betAmount * lev;

    resLiqPrice.textContent = Number(liqPrice).toFixed(2) + " USDT";
    resLiqDist.textContent = "남은 거리: -" + Number(distPct).toFixed(2) + "%";
    resKellyPct.textContent = Number(kellyPct).toFixed(2) + "%";
    resHalfKelly.textContent = Number(halfKellyPct).toFixed(2) + "%";
    resBetAmount.textContent = Number(betAmount).toFixed(2) + " USDT";

    const riskShare = Math.min(100, Math.max(1, (1 / lev) * 100));
    const safeShare = Math.max(0, 100 - riskShare);
    barSafe.style.width = Number(safeShare).toFixed(1) + "%";
    barRisk.style.width = Number(riskShare).toFixed(1) + "%";
    barRatioText.textContent = "안전 마진 " + Number(safeShare).toFixed(1) + "% | 청산 위험 " + Number(riskShare).toFixed(1) + "%";

    notionalSize.textContent = Number(notional).toFixed(2) + " USDT";
    maxLoss.textContent = "-100% (-" + Number(betAmount).toFixed(2) + " USDT)";

    syncHash();
  }}

  [entryInput, levInput, sideSelect, seedInput, winInput, rrInput].forEach(function(el) {{
    if (el) {{
      el.addEventListener('input', calculateLeverage);
      el.addEventListener('change', calculateLeverage);
    }}
  }});

  if (copyBtn) {{
    copyBtn.addEventListener('click', function() {{
      const text = "[선물 레버리지 청산가 & 켈리 공식 결과]\\n" +
                   "• 진입가: " + entryLabel.textContent + " (" + sideSelect.value.toUpperCase() + ", " + levLabel.textContent + ")\\n" +
                   "• 강제 청산가: " + resLiqPrice.textContent + " (" + resLiqDist.textContent + ")\\n" +
                   "• 켈리 최적 비중: " + resKellyPct.textContent + " (권장 Half-Kelly: " + resHalfKelly.textContent + ")\\n" +
                   "• 1회 권장 투입 시드: " + resBetAmount.textContent + "\\n" +
                   "• 총 포지션 규모: " + notionalSize.textContent;
      navigator.clipboard.writeText(text).then(function() {{
        copyBtn.textContent = "✅ 복사 완료!";
        setTimeout(function() {{ copyBtn.textContent = "📋 결과 복사"; }}, 2000);
      }});
    }});
  }}

  if (shareBtn) {{
    shareBtn.addEventListener('click', function() {{
      const shareUrl = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(shareUrl).then(function() {{
          shareBtn.textContent = "✅ 공유 링크 복사됨!";
          setTimeout(function() {{ shareBtn.textContent = "🔗 결과 공유 링크 복사"; }}, 2000);
        }}).catch(function() {{ fallbackShare(shareUrl); }});
      }} else {{
        fallbackShare(shareUrl);
      }}
    }});
  }}

  function fallbackShare(url) {{
    const ta = document.createElement('textarea');
    ta.value = url;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {{
      document.execCommand('copy');
      if (shareBtn) shareBtn.textContent = "✅ 공유 링크 복사됨!";
    }} catch (e) {{
      if (shareBtn) shareBtn.textContent = "복사 실패";
    }}
    document.body.removeChild(ta);
    setTimeout(function() {{ if (shareBtn) shareBtn.textContent = "🔗 결과 공유 링크 복사"; }}, 2000);
  }}

  // URL Hash 파라미터 사전 로드
  try {{
    if (window.location.hash && window.location.hash.length > 1) {{
      const params = new URLSearchParams(window.location.hash.substring(1));
      if (params.has('entry')) entryInput.value = params.get('entry');
      if (params.has('lev')) levInput.value = params.get('lev');
      if (params.has('side')) sideSelect.value = params.get('side');
      if (params.has('seed')) seedInput.value = params.get('seed');
      if (params.has('win')) winInput.value = params.get('win');
      if (params.has('rr')) rrInput.value = params.get('rr');
    }}
  }} catch (e) {{}}

  calculateLeverage();
}})();
</script>
"""
        return tpl.replace("__WIDGET_TITLE__", w_title).replace("__SUB_LABEL__", w_sub).replace("__BADGE_TEXT__", badge)

    def _render_dividend_compound_widget(self, rule_info: Optional[Dict[str, Any]] = None) -> str:
        """배당금 복리 재투자 & 금융소득종합과세 0ms 인터랙티브 위젯 (URL Hash 상태 저장 및 공유)"""
        rule_info = rule_info or {}
        w_title = rule_info.get("name", "배당금 복리 재투자 & 금융소득종합과세 시뮬레이터")
        if not w_title.startswith("💰"):
            w_title = f"💰 {w_title}"
        w_sub = rule_info.get("sub_label", "2,000만 원 종합과세 분기점 감별 0ms 연산")
        ticker = rule_info.get("ticker", "")
        badge = f"Wealth Growth • {ticker}" if ticker else "Wealth Growth v2026"
        def_yield = float(rule_info.get("default_yield", 7.0))

        tpl = f"""
<!-- [FINTECH MICRO-SAAS] __WIDGET_TITLE__ -->
<div class="blogin-saas-container" style="background:#0b0f19; border:1px solid #1f293d; border-radius:18px; padding:24px; color:#e2e8f0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; max-width:100%; box-sizing:border-box; margin:28px 0; box-shadow:0 12px 40px rgba(0,0,0,0.45);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid #1e293b; padding-bottom:16px;">
    <div>
      <span style="background:linear-gradient(135deg, #8b5cf6, #6d28d9); color:#fff; font-size:11px; font-weight:800; letter-spacing:1px; text-transform:uppercase; padding:4px 10px; border-radius:20px;">__BADGE_TEXT__</span>
      <h3 style="margin:8px 0 0 0; color:#f8fafc; font-size:22px; font-weight:800;">__WIDGET_TITLE__</h3>
    </div>
    <div style="text-align:right;">
      <span style="color:#94a3b8; font-size:12px;">__SUB_LABEL__</span>
    </div>
  </div>

  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:20px;">
    <!-- Input 1: 초기 투자 원금 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="div_principal_input" style="font-size:12px; font-weight:700; color:#94a3b8;">1. 초기 투자 원금 (KRW)</label>
        <span id="div_principal_label" style="font-size:12px; font-weight:800; color:#38bdf8;">100,000,000원</span>
      </div>
      <input type="number" id="div_principal_input" min="0" max="10000000000" step="10000000" value="100000000" style="width:100%; box-sizing:border-box; background:#0b1120; color:#38bdf8; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>

    <!-- Input 2: 연간 배당 수익률 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="div_yield_input" style="font-size:12px; font-weight:700; color:#94a3b8;">2. 연간 배당 수익률 (%)</label>
        <span id="div_yield_label" style="font-size:12px; font-weight:800; color:#c084fc;">{def_yield:.2f}%</span>
      </div>
      <input type="range" id="div_yield_input" min="1.0" max="25.0" step="0.5" value="{def_yield}" style="width:100%; accent-color:#c084fc; cursor:pointer;" />
    </div>

    <!-- Input 3: 복리 재투자 기간 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="div_years_input" style="font-size:12px; font-weight:700; color:#94a3b8;">3. 복리 재투자 기간 (년)</label>
        <span id="div_years_label" style="font-size:12px; font-weight:800; color:#f59e0b;">10년</span>
      </div>
      <input type="range" id="div_years_input" min="1" max="30" step="1" value="10" style="width:100%; accent-color:#f59e0b; cursor:pointer;" />
      <div style="display:flex; gap:6px; margin-top:8px;">
        <button type="button" class="div-year-btn" data-year="5" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">5년</button>
        <button type="button" class="div-year-btn" data-year="10" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">10년</button>
        <button type="button" class="div-year-btn" data-year="20" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; border-radius:4px; padding:3px 8px; font-size:11px; cursor:pointer;">20년</button>
      </div>
    </div>

    <!-- Input 4: 월 추가 적립 투자금 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label for="div_monthly_input" style="font-size:12px; font-weight:700; color:#94a3b8;">4. 월 추가 적립액 (KRW)</label>
        <span id="div_monthly_label" style="font-size:12px; font-weight:800; color:#10b981;">500,000원</span>
      </div>
      <input type="number" id="div_monthly_input" min="0" max="100000000" step="100000" value="500000" style="width:100%; box-sizing:border-box; background:#0b1120; color:#34d399; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:15px; font-weight:700; outline:none;" />
    </div>
  </div>

  <!-- 결과 메트릭스 Bento Box -->
  <div style="background:linear-gradient(145deg, #0f172a, #1e293b); border:1px solid #8b5cf640; border-radius:16px; padding:20px; margin-bottom:20px;">
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px; text-align:center;">
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">1년차 연간 세전 배당금</div>
        <div id="div_res_gross" style="font-size:18px; font-weight:900; color:#38bdf8; margin-top:4px;">7,000,000원</div>
        <div id="div_res_monthly_gross" style="font-size:11px; color:#64748b; margin-top:2px;">월 환산 583,333원</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">배당소득세(15.4%) 및 세후</div>
        <div id="div_res_net" style="font-size:18px; font-weight:900; color:#10b981; margin-top:4px;">5,922,000원</div>
        <div id="div_res_tax" style="font-size:11px; color:#f87171; margin-top:2px;">원천징수 1,078,000원</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">금융소득종합과세 판정</div>
        <div id="div_res_comprehensive" style="font-size:14px; font-weight:900; color:#34d399; margin-top:6px;">✅ 2,000만 이하 분리과세</div>
        <div style="font-size:11px; color:#64748b; margin-top:2px;">기준: 연 2,000만 원</div>
      </div>
      <div style="background:linear-gradient(135deg, #4c1d95, #6d28d9); border-radius:10px; padding:12px; border:1px solid #a78bfa;">
        <div style="font-size:11px; color:#ede9fe; font-weight:800;">복리 재투자 예상 자산</div>
        <div id="div_res_future" style="font-size:20px; font-weight:900; color:#ffffff; margin-top:4px;">257,480,000원</div>
        <div id="div_res_profit" style="font-size:11px; color:#ddd6fe; margin-top:2px;">배당 복리 수익 +97,480,000원</div>
      </div>
    </div>

    <!-- 자산 구성 비율 Visual Breakdown Bar -->
    <div style="margin-top:18px;">
      <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:6px;">
        <span>만기 자산 구성: 총 원금 납입액 vs 복리 배당 누적 순수익</span>
        <span id="div_bar_ratio_text" style="font-weight:700; color:#e2e8f0;">원금 62.1% | 복리수익 37.9%</span>
      </div>
      <div style="width:100%; height:16px; background:#0b1120; border-radius:10px; overflow:hidden; display:flex;">
        <div id="div_bar_principal" style="height:100%; background:linear-gradient(90deg, #3b82f6, #60a5fa); width:62.1%; transition:width 0.2s;"></div>
        <div id="div_bar_profit" style="height:100%; background:linear-gradient(90deg, #8b5cf6, #c084fc); width:37.9%; transition:width 0.2s;"></div>
      </div>
    </div>

    <div style="margin-top:16px; background:#0b112080; border:1px solid #334155; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div style="font-size:12px; color:#cbd5e1;">
        <span>만기 시점 예상 월 배당금: <strong id="div_res_final_monthly" style="color:#34d399;">1,265,000원</strong></span>
        <span style="margin:0 8px; color:#94a3b8;">|</span>
        <span>총 납입 원금: <strong id="div_res_total_paid" style="color:#cbd5e1;">160,000,000원</strong></span>
      </div>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        <button id="div_copy_btn" type="button" style="background:#7c3aed; color:#fff; border:none; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          📋 결과 복사
        </button>
        <button id="div_share_btn" type="button" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf880; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
          🔗 결과 공유 링크 복사
        </button>
      </div>
    </div>
  </div>

  <div style="background:#131c31; border:1px dashed #8b5cf680; border-radius:12px; padding:14px 18px; font-size:12px; color:#c4b5fd;">
    <strong>💡 절세계좌(ISA/연금저축/IRP) 활용:</strong> 일반 계좌에서 연간 배당금이 2,000만 원을 초과하면 타 근로/사업소득과 합산 과세(최대 49.5%) 및 건강보험료 피부양자 자격이 박탈될 수 있습니다. ISA 및 연금계좌를 우선 활용하여 비과세·과세이연 혜택을 극대화하십시오.
  </div>
</div>

<script>
(function() {{
  const pInput = document.getElementById('div_principal_input');
  const yInput = document.getElementById('div_yield_input');
  const yearsInput = document.getElementById('div_years_input');
  const mInput = document.getElementById('div_monthly_input');

  const pLabel = document.getElementById('div_principal_label');
  const yLabel = document.getElementById('div_yield_label');
  const yearsLabel = document.getElementById('div_years_label');
  const mLabel = document.getElementById('div_monthly_label');

  const resGross = document.getElementById('div_res_gross');
  const resMonthGross = document.getElementById('div_res_monthly_gross');
  const resNet = document.getElementById('div_res_net');
  const resTax = document.getElementById('div_res_tax');
  const resComp = document.getElementById('div_res_comprehensive');
  const resFuture = document.getElementById('div_res_future');
  const resProfit = document.getElementById('div_res_profit');

  const barPrincipal = document.getElementById('div_bar_principal');
  const barProfit = document.getElementById('div_bar_profit');
  const barRatioText = document.getElementById('div_bar_ratio_text');

  const resFinalMonthly = document.getElementById('div_res_final_monthly');
  const resTotalPaid = document.getElementById('div_res_total_paid');
  const copyBtn = document.getElementById('div_copy_btn');
  const shareBtn = document.getElementById('div_share_btn');

  function syncHash() {{
    try {{
      const p = new URLSearchParams();
      p.set('prin', pInput.value);
      p.set('yield', yInput.value);
      p.set('years', yearsInput.value);
      p.set('monthly', mInput.value);
      if (window.history && window.history.replaceState) {{
        window.history.replaceState(null, '', '#' + p.toString());
      }}
    }} catch (e) {{}}
  }}

  function calculateDividend() {{
    let principal = parseFloat(pInput.value) || 0;
    let divYield = parseFloat(yInput.value) || 0;
    let years = parseInt(yearsInput.value, 10) || 1;
    let monthly = parseFloat(mInput.value) || 0;

    principal = Math.max(0, principal);
    divYield = Math.max(0, divYield);
    years = Math.max(1, Math.min(30, years));
    monthly = Math.max(0, monthly);

    pLabel.textContent = Math.round(principal).toLocaleString('ko-KR') + "원";
    yLabel.textContent = Number(divYield).toFixed(2) + "%";
    yearsLabel.textContent = years + "년";
    mLabel.textContent = Math.round(monthly).toLocaleString('ko-KR') + "원";

    const grossAnnual = principal * (divYield / 100);
    const taxAnnual = grossAnnual * 0.154;
    const netAnnual = grossAnnual - taxAnnual;
    const monthlyGross = grossAnnual / 12;

    resGross.textContent = Math.round(grossAnnual).toLocaleString('ko-KR') + "원";
    resMonthGross.textContent = "월 환산 " + Math.round(monthlyGross).toLocaleString('ko-KR') + "원";
    resNet.textContent = Math.round(netAnnual).toLocaleString('ko-KR') + "원";
    resTax.textContent = "원천징수 " + Math.round(taxAnnual).toLocaleString('ko-KR') + "원";

    if (grossAnnual > 20000000) {{
      resComp.textContent = "⚠️ 2,000만 초과 종합과세 대상";
      resComp.style.color = "#f87171";
    }} else {{
      resComp.textContent = "✅ 2,000만 이하 분리과세 안전";
      resComp.style.color = "#34d399";
    }}

    // 복리 계산 (월 복리)
    const netMonthlyRate = (divYield * (1 - 0.154)) / 100 / 12;
    let balance = principal;
    const totalMonths = years * 12;

    for (let m = 0; m < totalMonths; m++) {{
      balance = (balance + monthly) * (1 + netMonthlyRate);
    }}

    const totalPaid = principal + (monthly * totalMonths);
    const compoundProfit = Math.max(0, balance - totalPaid);
    const finalMonthlyDiv = (balance * (divYield * (1 - 0.154) / 100)) / 12;

    resFuture.textContent = Math.round(balance).toLocaleString('ko-KR') + "원";
    resProfit.textContent = "배당 복리 수익 +" + Math.round(compoundProfit).toLocaleString('ko-KR') + "원";
    resFinalMonthly.textContent = Math.round(finalMonthlyDiv).toLocaleString('ko-KR') + "원";
    resTotalPaid.textContent = Math.round(totalPaid).toLocaleString('ko-KR') + "원";

    let pShare = 50;
    let profShare = 50;
    if (balance > 0) {{
      pShare = Math.min(100, (totalPaid / balance) * 100);
      profShare = Math.max(0, 100 - pShare);
    }}
    barPrincipal.style.width = Number(pShare).toFixed(1) + "%";
    barProfit.style.width = Number(profShare).toFixed(1) + "%";
    barRatioText.textContent = "원금 " + Number(pShare).toFixed(1) + "% | 복리수익 " + Number(profShare).toFixed(1) + "%";

    syncHash();
  }}

  const yBtns = document.querySelectorAll('.div-year-btn');
  yBtns.forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      const y = parseInt(btn.getAttribute('data-year'), 10) || 10;
      yearsInput.value = y;
      calculateDividend();
    }});
  }});

  [pInput, yInput, yearsInput, mInput].forEach(function(el) {{
    if (el) {{
      el.addEventListener('input', calculateDividend);
      el.addEventListener('change', calculateDividend);
    }}
  }});

  if (copyBtn) {{
    copyBtn.addEventListener('click', function() {{
      const text = "[배당금 복리 재투자 & 종합과세 시뮬레이션 결과]\\n" +
                   "• 초기 원금: " + pLabel.textContent + " (월 적립: " + mLabel.textContent + ")\\n" +
                   "• 연 배당률: " + yLabel.textContent + " (1년차 배당: " + resGross.textContent + ", 세후: " + resNet.textContent + ")\\n" +
                   "• 종합과세 판정: " + resComp.textContent + "\\n" +
                   "• " + yearsLabel.textContent + " 후 복리 예상 총자산: " + resFuture.textContent + "\\n" +
                   "• 순수 복리 배당 수익: " + resProfit.textContent + "\\n" +
                   "• 만기 월 수령 배당금: " + resFinalMonthly.textContent;
      navigator.clipboard.writeText(text).then(function() {{
        copyBtn.textContent = "✅ 복사 완료!";
        setTimeout(function() {{ copyBtn.textContent = "📋 결과 복사"; }}, 2000);
      }});
    }});
  }}

  if (shareBtn) {{
    shareBtn.addEventListener('click', function() {{
      const shareUrl = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(shareUrl).then(function() {{
          shareBtn.textContent = "✅ 공유 링크 복사됨!";
          setTimeout(function() {{ shareBtn.textContent = "🔗 결과 공유 링크 복사"; }}, 2000);
        }}).catch(function() {{ fallbackShare(shareUrl); }});
      }} else {{
        fallbackShare(shareUrl);
      }}
    }});
  }}

  function fallbackShare(url) {{
    const ta = document.createElement('textarea');
    ta.value = url;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {{
      document.execCommand('copy');
      if (shareBtn) shareBtn.textContent = "✅ 공유 링크 복사됨!";
    }} catch (e) {{
      if (shareBtn) shareBtn.textContent = "복사 실패";
    }}
    document.body.removeChild(ta);
    setTimeout(function() {{ if (shareBtn) shareBtn.textContent = "🔗 결과 공유 링크 복사"; }}, 2000);
  }}

  // URL Hash 파라미터 사전 로드
  try {{
    if (window.location.hash && window.location.hash.length > 1) {{
      const params = new URLSearchParams(window.location.hash.substring(1));
      if (params.has('prin')) pInput.value = params.get('prin');
      if (params.has('yield')) yInput.value = params.get('yield');
      if (params.has('years')) yearsInput.value = params.get('years');
      if (params.has('monthly')) mInput.value = params.get('monthly');
    }}
  }} catch (e) {{}}

  calculateDividend();
}})();
</script>
"""
        return tpl.replace("__WIDGET_TITLE__", w_title).replace("__SUB_LABEL__", w_sub).replace("__BADGE_TEXT__", badge)

    def render_trading_tables(self, rule_key: str = "overseas_stock_tax") -> str:
        """도메인별 초고밀도 실측 데이터 대조표 2종 렌더링"""
        rule = self.rules.get(rule_key, {})
        cat = rule.get("category", "")
        if any(k in rule_key for k in ["dca", "averaging", "water"]):
            return self._render_water_averaging_tables(rule)
        elif any(k in rule_key for k in ["kelly", "liquidation", "futures", "decay", "leverage"]) or cat == "crypto":
            return self._render_leverage_kelly_tables(rule)
        elif any(k in rule_key for k in ["dividend", "compound", "pension", "irp", "isa", "ipo"]) or cat == "retirement":
            return self._render_dividend_compound_tables(rule)
        else:
            return self._render_overseas_tax_tables(rule)

    def _render_overseas_tax_tables(self, rule: Optional[Dict[str, Any]] = None) -> str:
        rule = rule or self.rules.get("overseas_stock_tax", {})
        ticker = rule.get("ticker", "")
        if ticker:
            display_title = f"{rule.get('name', ticker)} 과세표준 및 실효세율"
        else:
            display_title = "2026 해외주식 양도소득세 과세표준 및 실효세율"

        brackets = rule.get("tax_matrix_brackets", self.rules.get("overseas_stock_tax", {}).get("tax_matrix_brackets", []))
        strategies = rule.get("tax_saving_strategies", self.rules.get("overseas_stock_tax", {}).get("tax_saving_strategies", []))

        bracket_rows = ""
        for b in brackets:
            bracket_rows += f"""
<tr style="border-bottom:1px solid #1e293b;">
  <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">{b['gain_krw']:,}원</td>
  <td style="padding:10px 12px; color:#94a3b8;">{b['tax_base_krw']:,}원</td>
  <td style="padding:10px 12px; color:#ef4444; font-weight:800;">{b['total_tax_krw']:,}원</td>
  <td style="padding:10px 12px; color:#10b981; font-weight:700;">{b['effective_rate']}</td>
</tr>
"""

        strategy_rows = ""
        for s in strategies:
            strategy_rows += f"""
<tr style="border-bottom:1px solid #1e293b;">
  <td style="padding:10px 12px; font-weight:700; color:#38bdf8;">{s['strategy']}</td>
  <td style="padding:10px 12px; color:#cbd5e1; font-size:13px; line-height:1.6;">{s['effect']}</td>
</tr>
"""

        return f"""
<!-- [FINTECH DATA DENSITY TABLE 1] {display_title} 구간별 실측 세액 대조표 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px; display:flex; align-items:center;">
    📊 {display_title} 구간별 시뮬레이션 표
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">연간 순수익(손익통산)</th>
          <th style="padding:12px;">과세표준 (250만 공제)</th>
          <th style="padding:12px;">납부 세액 (22%)</th>
          <th style="padding:12px;">실효세율 (%)</th>
        </tr>
      </thead>
      <tbody>
        {bracket_rows}
      </tbody>
    </table>
  </div>
</div>

<!-- [FINTECH DATA DENSITY TABLE 2] 국세청 인정 3대 합법적 절세 전략 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    💡 국세청 세법 가이드라인 기준 3대 합법적 양도소득세 절세 전략
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px; width:35%;">절세 전략명</th>
          <th style="padding:12px; width:65%;">세법상 절세 메커니즘 및 실행 가이드</th>
        </tr>
      </thead>
      <tbody>
        {strategy_rows}
      </tbody>
    </table>
  </div>
</div>
"""

    def _render_water_averaging_tables(self, rule: Optional[Dict[str, Any]] = None) -> str:
        rule = rule or self.rules.get("water_averaging_dca", {})
        asset_name = rule.get("name", "주식·코인 물타기")
        samples = rule.get("averaging_matrix_samples", self.rules.get("water_averaging_dca", {}).get("averaging_matrix_samples", []))

        rows = ""
        for s in samples:
            rows += f"""
<tr style="border-bottom:1px solid #1e293b;">
  <td style="padding:10px 12px; font-weight:700; color:#ef4444;">{s['drop_rate']}</td>
  <td style="padding:10px 12px; color:#38bdf8; font-weight:600;">{s['extra_ratio']}</td>
  <td style="padding:10px 12px; color:#fbbf24; font-weight:700;">{s['new_drop_rate']}</td>
  <td style="padding:10px 12px; color:#34d399; font-weight:800;">{s['required_rebound']}</td>
</tr>
"""
        return f"""
<!-- [DCA DATA DENSITY TABLE 1] 낙폭별 물타기 배수 및 본전 탈출 반등률 매트릭스 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    📊 {asset_name} 낙폭 구간별 물타기 배수 및 실질 본전 탈출 필요 반등률 대조표
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">최초 하락률</th>
          <th style="padding:12px;">추가 매수 비중</th>
          <th style="padding:12px;">물타기 후 평단 하락률</th>
          <th style="padding:12px;">본전 탈출 필요 반등률 (BEP)</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </div>
</div>

<!-- [DCA DATA DENSITY TABLE 2] 퀀트 물타기 vs 손절매(Stop-loss) 가이드 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    💡 퀀트 리스크 관리: 물타기 실행 적격 vs 손절매(Stop-Loss) 필수 감별 기준
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px; width:30%;">판단 지표</th>
          <th style="padding:12px; width:35%;">분할 매수(물타기) 권장 상황</th>
          <th style="padding:12px; width:35%;">즉각 손절매(Stop-Loss) 필수 상황</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">펀더멘털 및 실적</td>
          <td style="padding:10px 12px; color:#34d399;">기업 EPS 성장세 유지, 시장 일시 패닉</td>
          <td style="padding:10px 12px; color:#f87171;">매출 역성장, 비즈니스 모델 훼손, 횡령/배임</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">총 시드 대비 비중</td>
          <td style="padding:10px 12px; color:#34d399;">해당 종목이 전체 포트폴리오의 15% 이하</td>
          <td style="padding:10px 12px; color:#f87171;">이미 포트폴리오의 30% 초과 몰빵 상태</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">기술적 지지선</td>
          <td style="padding:10px 12px; color:#34d399;">주봉 120선, 주요 매물대 지지 확인</td>
          <td style="padding:10px 12px; color:#f87171;">주요 지지선 거래량 동반 하향 이탈</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

    def _render_leverage_kelly_tables(self, rule: Optional[Dict[str, Any]] = None) -> str:
        rule = rule or self.rules.get("leverage_liquidation_kelly", {})
        asset_name = rule.get("name", "선물 레버리지")
        return f"""
<!-- [LEVERAGE DATA DENSITY TABLE 1] 레버리지별 청산 위험 거리 매트릭스 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    📊 {asset_name} 주요 레버리지 배율별 격리 마진 청산 위험 거리 및 허용 반대 변동폭
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">레버리지 배율</th>
          <th style="padding:12px;">필요 개시 증거금</th>
          <th style="padding:12px;">청산까지 허용 반대 변동폭</th>
          <th style="padding:12px;">위험도 등급</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">2x</td>
          <td style="padding:10px 12px; color:#94a3b8;">50.0%</td>
          <td style="padding:10px 12px; color:#34d399; font-weight:800;">-49.50%</td>
          <td style="padding:10px 12px; color:#34d399;">🟢 초저위험 (스윙 가능)</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">5x</td>
          <td style="padding:10px 12px; color:#94a3b8;">20.0%</td>
          <td style="padding:10px 12px; color:#38bdf8; font-weight:800;">-19.50%</td>
          <td style="padding:10px 12px; color:#38bdf8;">🔵 저위험 (추세 추종)</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">10x</td>
          <td style="padding:10px 12px; color:#94a3b8;">10.0%</td>
          <td style="padding:10px 12px; color:#fbbf24; font-weight:800;">-9.50%</td>
          <td style="padding:10px 12px; color:#fbbf24;">🟡 중위험 (변동성 주의)</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">20x</td>
          <td style="padding:10px 12px; color:#94a3b8;">5.0%</td>
          <td style="padding:10px 12px; color:#f87171; font-weight:800;">-4.50%</td>
          <td style="padding:10px 12px; color:#f87171;">🟠 고위험 (단기 스캘핑)</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">50x</td>
          <td style="padding:10px 12px; color:#94a3b8;">2.0%</td>
          <td style="padding:10px 12px; color:#ef4444; font-weight:800;">-1.50%</td>
          <td style="padding:10px 12px; color:#ef4444;">🔴 초고위험 (즉각 청산 위험)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- [LEVERAGE DATA DENSITY TABLE 2] 켈리 공식 포지션 사이징 가이드 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    💡 퀀트 수학: 켈리 공식(Kelly Criterion) 승률/손익비별 권장 베팅 비중 표
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">전략 승률 (Win Rate)</th>
          <th style="padding:12px;">손익비 (R/R Ratio)</th>
          <th style="padding:12px;">풀 켈리 공식 비중 (Full)</th>
          <th style="padding:12px;">안전 권장 비중 (Half-Kelly)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">40%</td>
          <td style="padding:10px 12px; color:#94a3b8;">2.0 : 1</td>
          <td style="padding:10px 12px; color:#38bdf8;">10.00%</td>
          <td style="padding:10px 12px; color:#34d399; font-weight:800;">5.00%</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">50%</td>
          <td style="padding:10px 12px; color:#94a3b8;">1.5 : 1</td>
          <td style="padding:10px 12px; color:#38bdf8;">16.67%</td>
          <td style="padding:10px 12px; color:#34d399; font-weight:800;">8.33%</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">55%</td>
          <td style="padding:10px 12px; color:#94a3b8;">2.0 : 1</td>
          <td style="padding:10px 12px; color:#38bdf8;">32.50%</td>
          <td style="padding:10px 12px; color:#34d399; font-weight:800;">16.25%</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">60%</td>
          <td style="padding:10px 12px; color:#94a3b8;">1.5 : 1</td>
          <td style="padding:10px 12px; color:#38bdf8;">33.33%</td>
          <td style="padding:10px 12px; color:#34d399; font-weight:800;">16.67%</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

    def _render_dividend_compound_tables(self, rule: Optional[Dict[str, Any]] = None) -> str:
        rule = rule or self.rules.get("dividend_compound_tax", {})
        asset_name = rule.get("name", "배당 복리")
        return f"""
<!-- [DIVIDEND DATA DENSITY TABLE 1] {asset_name} 복리 시뮬레이션 표 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    📊 {asset_name} 기간별 복리 자산 대조표
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">재투자 기간</th>
          <th style="padding:12px;">총 납입 원금</th>
          <th style="padding:12px;">세후 복리 총자산</th>
          <th style="padding:12px;">순수 배당 누적 수익</th>
          <th style="padding:12px;">만기 월 배당금</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">3년차</td>
          <td style="padding:10px 12px; color:#94a3b8;">118,000,000원</td>
          <td style="padding:10px 12px; color:#38bdf8; font-weight:700;">142,650,000원</td>
          <td style="padding:10px 12px; color:#10b981;">+24,650,000원</td>
          <td style="padding:10px 12px; color:#fbbf24;">월 701,000원</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">5년차</td>
          <td style="padding:10px 12px; color:#94a3b8;">130,000,000원</td>
          <td style="padding:10px 12px; color:#38bdf8; font-weight:700;">176,320,000원</td>
          <td style="padding:10px 12px; color:#10b981;">+46,320,000원</td>
          <td style="padding:10px 12px; color:#fbbf24;">월 867,000원</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">10년차</td>
          <td style="padding:10px 12px; color:#94a3b8;">160,000,000원</td>
          <td style="padding:10px 12px; color:#38bdf8; font-weight:800;">257,480,000원</td>
          <td style="padding:10px 12px; color:#10b981; font-weight:800;">+97,480,000원</td>
          <td style="padding:10px 12px; color:#fbbf24; font-weight:800;">월 1,265,000원</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">20년차</td>
          <td style="padding:10px 12px; color:#94a3b8;">220,000,000원</td>
          <td style="padding:10px 12px; color:#c084fc; font-weight:900;">596,420,000원</td>
          <td style="padding:10px 12px; color:#10b981; font-weight:900;">+376,420,000원</td>
          <td style="padding:10px 12px; color:#fbbf24; font-weight:900;">월 2,932,000원</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- [DIVIDEND DATA DENSITY TABLE 2] 금융소득종합과세 방어 3대 절세계좌 비교 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    💡 금융소득 2,000만 원 초과 종합과세 및 건보료 피부양자 박탈 방어 계좌
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:550px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">절세 계좌 유형</th>
          <th style="padding:12px;">연간 납입 한도</th>
          <th style="padding:12px;">배당 소득세 혜택</th>
          <th style="padding:12px;">종합과세 및 건보료 반영 여부</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#38bdf8;">중개형 ISA</td>
          <td style="padding:10px 12px; color:#94a3b8;">연 2,000만 원 (총 1억)</td>
          <td style="padding:10px 12px; color:#34d399;">200~400만 비과세, 초과분 9.9% 분리과세</td>
          <td style="padding:10px 12px; color:#34d399;">금융소득종합과세 합산 제외</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#38bdf8;">연금저축펀드</td>
          <td style="padding:10px 12px; color:#94a3b8;">연 600만 원 (세액공제)</td>
          <td style="padding:10px 12px; color:#34d399;">과세이연 (인출 시 연금소득세 3.3~5.5%)</td>
          <td style="padding:10px 12px; color:#34d399;">건보료 및 종합과세 비대상</td>
        </tr>
        <tr style="border-bottom:1px solid #1e293b;">
          <td style="padding:10px 12px; font-weight:700; color:#38bdf8;">개인형 IRP</td>
          <td style="padding:10px 12px; color:#94a3b8;">연 900만 원 (합산 한도)</td>
          <td style="padding:10px 12px; color:#34d399;">과세이연 및 세액공제 최대 16.5%</td>
          <td style="padding:10px 12px; color:#34d399;">건보료 및 종합과세 비대상</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

    def render_monetization_cta(self, rule_key: str = "overseas_stock_tax") -> str:
        """
        [고수익 제휴 수익화 파이프라인] 
        - 선물 레버리지 및 크립토: 바이낸스/바이비트/비트겟 수수료 20~50% 영구 할인 공식 파트너 배너 (CPA/RevShare)
        - 주식/세무/배당/DCA: 증권사 최저 수수료 계좌 및 퀀트 도서/트레이딩 툴 고단가 CTA (쿠팡 파트너스/이벤트)
        """
        rule = self.rules.get(rule_key, {})
        cat = rule.get("category", "")
        if cat == "crypto" or any(k in rule_key for k in ["btc", "eth", "xrp", "sol", "doge", "sei", "futures", "liquidation", "leverage", "kelly"]):
            return self._render_crypto_affiliate_cta()
        else:
            return self._render_stock_affiliate_cta()

    def _render_crypto_affiliate_cta(self) -> str:
        binance_url = os.getenv("BINANCE_REFERRAL_URL", "https://accounts.binance.com/register?ref=BLOGIN365")
        bybit_url = os.getenv("BYBIT_REFERRAL_URL", "https://www.bybit.com/register?affiliate_id=BLOGIN365")
        bitget_url = os.getenv("BITGET_REFERRAL_URL", "https://partner.bitget.com/bg/BLOGIN365")

        return f"""
<!-- [HIGH-YIELD CRYPTO AFFILIATE CTA] 선물 거래소 공식 수수료 할인 파트너십 -->
<div class="blogin-monetization-box" style="margin:36px 0; padding:24px; background:linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); border:2px solid #6366f1; border-radius:16px; box-shadow:0 12px 30px rgba(99, 102, 241, 0.2);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
    <div style="display:flex; align-items:center; gap:10px;">
      <span style="background:#4f46e5; color:#fff; font-size:12px; font-weight:800; padding:4px 10px; border-radius:6px; letter-spacing:0.05em;">VIP PARTNERSHIP</span>
      <h3 style="margin:0; color:#f8fafc; font-size:18px; font-weight:900;">⚡ 퀀트 트레이더 전용: 1티어 거래소 선물 수수료 20%~50% 할인</h3>
    </div>
    <span style="font-size:12px; color:#a5b4fc; font-weight:700;">청산 방어 및 복리 트레이딩 필수</span>
  </div>
  <p style="margin:0 0 18px 0; color:#cbd5e1; font-size:13px; line-height:1.6;">
    고레버리지 매매 시 발생하는 누적 거래 수수료는 시드머니를 잠식하는 가장 큰 원인입니다. 아래 공식 제휴 링크로 가입 시 <strong>평생 지정가·시장가 수수료 최대 할인 및 리워드 바우처</strong>가 즉시 적용됩니다.
  </p>
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:12px;">
    <a href="{binance_url}" target="_blank" rel="nofollow noopener" style="display:flex; flex-direction:column; justify-content:space-between; text-decoration:none; background:#18181b; border:1px solid #f59e0b; border-radius:12px; padding:16px; transition:transform 0.2s;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <strong style="color:#fbbf24; font-size:16px;">Binance (바이낸스)</strong>
          <span style="background:rgba(245, 158, 11, 0.15); color:#fbbf24; font-size:11px; font-weight:800; padding:2px 6px; border-radius:4px;">세계 1위</span>
        </div>
        <p style="margin:0 0 12px 0; color:#a1a1aa; font-size:12px;">선물 거래 수수료 20% 영구 할인 + 최대 $600 웰컴 바우처</p>
      </div>
      <div style="background:#f59e0b; color:#09090b; font-size:13px; font-weight:800; text-align:center; padding:9px; border-radius:8px;">공식 제휴 할인 가입하기 →</div>
    </a>
    <a href="{bybit_url}" target="_blank" rel="nofollow noopener" style="display:flex; flex-direction:column; justify-content:space-between; text-decoration:none; background:#18181b; border:1px solid #38bdf8; border-radius:12px; padding:16px; transition:transform 0.2s;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <strong style="color:#38bdf8; font-size:16px;">Bybit (바이비트)</strong>
          <span style="background:rgba(56, 189, 248, 0.15); color:#38bdf8; font-size:11px; font-weight:800; padding:2px 6px; border-radius:4px;">선물 최적화</span>
        </div>
        <p style="margin:0 0 12px 0; color:#a1a1aa; font-size:12px;">VIP 20% 수수료 할인 + 입금 리워드 $30,000 이벤트</p>
      </div>
      <div style="background:#0284c7; color:#fff; font-size:13px; font-weight:800; text-align:center; padding:9px; border-radius:8px;">VIP 파트너 가입하기 →</div>
    </a>
    <a href="{bitget_url}" target="_blank" rel="nofollow noopener" style="display:flex; flex-direction:column; justify-content:space-between; text-decoration:none; background:#18181b; border:1px solid #10b981; border-radius:12px; padding:16px; transition:transform 0.2s;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <strong style="color:#34d399; font-size:16px;">Bitget (비트겟)</strong>
          <span style="background:rgba(16, 185, 129, 0.15); color:#34d399; font-size:11px; font-weight:800; padding:2px 6px; border-radius:4px;">최고 페이백</span>
        </div>
        <p style="margin:0 0 12px 0; color:#a1a1aa; font-size:12px;">선물 거래 수수료 50% 페이백 + 카피트레이딩 지원</p>
      </div>
      <div style="background:#059669; color:#fff; font-size:13px; font-weight:800; text-align:center; padding:9px; border-radius:8px;">수수료 페이백 가입하기 →</div>
    </a>
  </div>
</div>
"""

    def _render_stock_affiliate_cta(self) -> str:
        coupang_url = os.getenv("COUPANG_FINTECH_URL", "https://link.coupang.com/a/blogin365")
        return f"""
<!-- [HIGH-YIELD FINTECH AFFILIATE CTA] 금융 투자·절세 필수 유틸리티 & 추천 솔루션 -->
<div class="blogin-monetization-box" style="margin:36px 0; padding:24px; background:linear-gradient(135deg, #0d1527 0%, #172554 100%); border:2px solid #2563eb; border-radius:16px; box-shadow:0 12px 30px rgba(37, 99, 235, 0.18);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
    <div style="display:flex; align-items:center; gap:10px;">
      <span style="background:#2563eb; color:#fff; font-size:12px; font-weight:800; padding:4px 10px; border-radius:6px;">INVESTMENT TOOLS</span>
      <h3 style="margin:0; color:#f8fafc; font-size:18px; font-weight:900;">💼 투자 효율 200% 극대화: 필수 절세 계좌 & 트레이딩 셋업</h3>
    </div>
    <span style="font-size:12px; color:#93c5fd; font-weight:700;">실전 투자자 공인 솔루션</span>
  </div>
  <p style="margin:0 0 16px 0; color:#cbd5e1; font-size:13px; line-height:1.6;">
    수익률을 1% 올리는 것보다 <strong>거래 수수료와 양도소득세 22%를 절감하는 것</strong>이 훨씬 빠르고 확실한 부의 증식 방법입니다.
  </p>
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
    <div style="background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:16px;">
      <span style="color:#10b981; font-size:11px; font-weight:800;">수수료 우대 혜택</span>
      <h4 style="margin:6px 0 8px 0; color:#f8fafc; font-size:15px; font-weight:700;">해외주식 평생 수수료 우대 (0.07%~) 및 95% 환전 우대</h4>
      <p style="margin:0 0 12px 0; color:#94a3b8; font-size:12px; line-height:1.5;">환전 스프레드와 매매 수수료를 즉시 아낄 수 있는 메이저 증권사 비대면 계좌 혜택을 확인하세요.</p>
      <a href="{coupang_url}" target="_blank" rel="nofollow noopener" style="display:inline-block; background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; font-size:12px; font-weight:700; text-decoration:none; padding:6px 12px; border-radius:6px;">수수료 우대 계좌 확인 →</a>
    </div>
    <div style="background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:16px;">
      <span style="color:#f59e0b; font-size:11px; font-weight:800;">추천 베스트셀러</span>
      <h4 style="margin:6px 0 8px 0; color:#f8fafc; font-size:15px; font-weight:700;">[2026 개정세법] 소득세법 기준 절세 전략 & 퀀트 투자 가이드</h4>
      <p style="margin:0 0 12px 0; color:#94a3b8; font-size:12px; line-height:1.5;">손익통산, 배우자 증여, ISA 계좌를 100% 활용해 세금을 0원으로 만드는 실전 지침서.</p>
      <a href="{coupang_url}" target="_blank" rel="nofollow noopener" style="display:inline-block; background:#f59e0b; color:#0f172a; font-size:12px; font-weight:800; text-decoration:none; padding:6px 12px; border-radius:6px;">도서 상세 가이드 확인 →</a>
    </div>
  </div>
</div>
"""
    def render_internal_silo_links(self, current_rule_key: str, published_posts_path: str = "data/published_posts.json") -> str:
        """이전 발행된 실제 블로그 URL을 본문 하단에 고밀도 카드 그리드로 결합 (Internal Silo Mesh)"""
        full_path = os.path.join(BASE_DIR, published_posts_path) if not os.path.isabs(published_posts_path) else published_posts_path
        if not os.path.exists(full_path):
            return ""

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                posts = json.load(f)
        except Exception:
            return ""

        # 실발행 URL이 있는 이전 포스트 추출
        valid_links = []
        seen_urls = set()
        for p in posts:
            url = p.get("url", "")
            title = p.get("title", "")
            # 오직 실제 발행된(Live) 포스트만 내부 링크로 연결 (모의 실행 preview 제외)
            if url and "blogin365ai.blogspot.com" in url and "preview-" not in url and url not in seen_urls:
                # 현재 키워드와 동일한 글 제외
                rule = self.rules.get(current_rule_key, {})
                if rule.get("name") and (rule["name"] in title or title in rule.get("name", "")):
                    continue
                seen_urls.add(url)
                valid_links.append(p)

        if not valid_links:
            return ""

        cards_html = ""
        for p in valid_links[:4]:
            cards_html += f"""
<a href="{p['url']}" target="_blank" rel="noopener" style="text-decoration:none; display:block; background:#131c31; border:1px solid #23314e; border-radius:12px; padding:16px; transition:border 0.2s; box-sizing:border-box;">
  <span style="font-size:11px; font-weight:800; color:#10b981; background:rgba(16, 185, 129, 0.1); padding:2px 8px; border-radius:4px; display:inline-block; margin-bottom:8px;">추천 퀀트 시뮬레이터</span>
  <h4 style="margin:0 0 6px 0; color:#f8fafc; font-size:14px; font-weight:700; line-height:1.4;">{p['title']}</h4>
  <p style="margin:0; color:#94a3b8; font-size:12px;">실시간 연산 및 절세 공식 바로가기 →</p>
</a>
"""

        silo_html = f"""
<!-- [INTERNAL SILO MESH] 함께 활용하는 필수 퀀트 시뮬레이터 -->
<div class="blogin-internal-silo" style="margin:40px 0 20px 0; padding:24px; background:#0d1527; border:1px solid #1e293b; border-radius:16px;">
  <h3 style="color:#f8fafc; font-size:17px; font-weight:800; margin:0 0 16px 0; display:flex; align-items:center;">
    🔗 함께 활용하면 수익률·절세를 극대화하는 퀀트 시뮬레이터
  </h3>
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
    {cards_html}
  </div>
</div>
"""
        return silo_html

    def render_legal_disclaimer(self) -> str:
        """YMYL 필수 준수: 소득세법 기준 법적 투자 면책 조항"""
        return """
<!-- [YMYL COMPLIANCE] 법적 투자 면책 조항 -->
<div class="legal-disclaimer" style="margin-top:36px; padding:20px; background:#0f172a; border-left:4px solid #ef4444; border-radius:8px; color:#94a3b8; font-size:13px; line-height:1.7;">
  <strong style="color:#f87171; display:block; font-size:14px; margin-bottom:8px;">⚖️ 법적 면책 조항 및 세무 안내 고지</strong>
  본 시뮬레이터는 소득세법 제94조, 제104조 및 지방세법에 규정된 해외주식 양도소득세 계산 산식을 기반으로 제작된 수학적 참고 도구이며, 실제 개별 투자자의 체결 환율, 분할 매수 단가 산정 방식(이동평균법/선입선출법), 기타 증권사 수수료 및 소득 합산 여부에 따라 실제 고지 세액과 차이가 발생할 수 있습니다.
  본 사이트는 금융투자업 및 세무대리 인가를 받은 법인이 아니며, 본 도구의 산출 결과는 어떠한 경우에도 투자 권유나 공식 세무 자문으로 해석될 수 없습니다. 최종 투자 판단과 납세 신고의 책임은 투자자 본인에게 있습니다.
</div>
"""


# ==============================================================================
# [Domain 2] 기존 HardwareDatasetResolver (하위 호환성 영구 보존)
# ==============================================================================
class HardwareDatasetResolver:
    def __init__(self):
        self.db = load_hardware_db()
        self.models = self.db.get("models", {})
        self.quants = self.db.get("quantizations", {})
        self.hardware = self.db.get("hardware", {})

    def resolve_topic(self, topic_hint: str) -> Dict[str, Any]:
        """주제 힌트에서 가장 적합한 기본 모델, 양자화 및 타겟 키워드 도출"""
        hint_lower = topic_hint.lower()

        # 모델 매칭
        selected_model_key = "llama-3-70b"  # Default
        for key in self.models.keys():
            normalized = key.replace("-", "").replace("_", "")
            if normalized in hint_lower or key in hint_lower:
                selected_model_key = key
                break
            # 8b, 70b, mistral, mixtral 등 부분 매칭
            if "70b" in hint_lower:
                selected_model_key = "llama-3-70b"
            elif "8b" in hint_lower:
                selected_model_key = "llama-3-8b"
            elif "mixtral" in hint_lower or "8x7b" in hint_lower:
                selected_model_key = "mixtral-8x7b"
            elif "mistral" in hint_lower:
                selected_model_key = "mistral-7b"
            elif "qwen" in hint_lower:
                selected_model_key = "qwen-2.5-72b"

        # 양자화 매칭
        selected_quant = "Q4_K_M"
        for q_key in self.quants.keys():
            if q_key.lower() in hint_lower:
                selected_quant = q_key
                break

        model_info = self.models[selected_model_key]
        exact_calc = self.calculate_vram(selected_model_key, selected_quant, model_info.get("default_context", 8192))

        target_title = f"{model_info['name']} {selected_quant} 양자화 필요 VRAM 및 GPU 사양 계산기"

        return {
            "model_key": selected_model_key,
            "quant_key": selected_quant,
            "model_info": model_info,
            "target_keyword": target_title,
            "formula_badge": "VRAM = (P * Q / 8) * 1.06 + KV_Cache + 0.6GB",
            "key_stat": f"{model_info['name']} {selected_quant} : {exact_calc['total_vram_gb']} GB",
            "sub_label": f"MINIMUM RECOMMENDED VRAM ({exact_calc['recommended_gpu']['name']})",
            "calc_result": exact_calc
        }

    def calculate_vram(self, model_key: str, quant_key: str, context_tokens: int = 8192, batch_size: int = 1) -> Dict[str, Any]:
        """수학적 실측 근거 100% 기반 정밀 계산"""
        model = self.models.get(model_key, self.models["llama-3-70b"])
        quant = self.quants.get(quant_key, self.quants["Q4_K_M"])

        params_b = float(model.get("params_b", 70.6))
        bits = float(quant.get("bits_per_param", 4.5))
        layers = int(model.get("layers", 80))
        kv_heads = int(model.get("kv_heads", 8))
        head_dim = int(model.get("head_dim", 128))

        # 1. 모델 가중치 용량 (6% 런타임/메타데이터 오버헤드 포함)
        weights_gb = round((params_b * bits / 8.0) * 1.06, 2)

        # 2. KV 캐시 메모리 (2 * layers * kv_heads * head_dim * bytes_per_token=2)
        kv_bytes_per_token = 2 * layers * kv_heads * head_dim * 2
        kv_cache_total_bytes = kv_bytes_per_token * context_tokens * batch_size
        kv_cache_gb = round(kv_cache_total_bytes / (1024 ** 3), 2)

        # 3. CUDA 컨텍스트 오버헤드
        cuda_overhead_gb = 0.60

        # 총합 VRAM
        total_vram_gb = round(weights_gb + kv_cache_gb + cuda_overhead_gb, 2)

        # 권장 GPU 매칭
        recommended_gpu = self._recommend_gpu(total_vram_gb)

        return {
            "model_name": model["name"],
            "params_b": params_b,
            "quant_label": quant["label"],
            "bits_per_param": bits,
            "context_tokens": context_tokens,
            "batch_size": batch_size,
            "weights_vram_gb": weights_gb,
            "kv_cache_gb": kv_cache_gb,
            "cuda_overhead_gb": cuda_overhead_gb,
            "total_vram_gb": total_vram_gb,
            "recommended_gpu": recommended_gpu
        }

    def _recommend_gpu(self, required_vram: float) -> Dict[str, Any]:
        """필요 VRAM에 따른 가장 경제적인 GPU 권장"""
        if required_vram <= 15.0:
            return {"name": "RTX 4060 Ti 16GB", "desc": "1장 단독 (가성비 최강 입문형)", "vram": "16 GB"}
        elif required_vram <= 23.0:
            return {"name": "RTX 4090 24GB / RTX 3090", "desc": "1장 단독 (골든 컨슈머 표준)", "vram": "24 GB"}
        elif required_vram <= 46.0:
            return {"name": "2x RTX 3090 / 4090 (48GB)", "desc": "2장 NVLink / PCIe 분산 병렬", "vram": "48 GB"}
        elif required_vram <= 76.0:
            return {"name": "NVIDIA A100 80GB (RunPod)", "desc": "클라우드 1장 대여 ($1.69/hr)", "vram": "80 GB"}
        elif required_vram <= 120.0:
            return {"name": "Apple MacBook Pro M3 Max (128GB)", "desc": "애플 실리콘 통합 메모리 단독 구동", "vram": "128 GB"}
        else:
            return {"name": "Apple Mac Studio M2 Ultra (192GB)", "desc": "통합 메모리 로컬 끝판왕", "vram": "192 GB"}

    def generate_pieter_levels_matrix(self, model_key: str) -> List[Dict[str, Any]]:
        """Pieter Levels 스타일: 전 양자화 레벨 실측 비교 매트릭스 생성"""
        model = self.models.get(model_key, self.models["llama-3-70b"])
        matrix = []
        for q_key, q_val in self.quants.items():
            calc = self.calculate_vram(model_key, q_key, context_tokens=8192)
            matrix.append({
                "quant": q_key,
                "label": q_val["label"],
                "bits": q_val["bits_per_param"],
                "weights_gb": calc["weights_vram_gb"],
                "total_vram_gb": calc["total_vram_gb"],
                "quality_loss": f"+{q_val['loss_perplexity']:.2f} PPL",
                "recommended_gpu": calc["recommended_gpu"]["name"]
            })
        return matrix

    def render_micro_saas_html(self, model_key: str = "llama-3-70b") -> str:
        """Wise/Pieter Levels 역공학: 0ms 반응형 Single-File Micro-SaaS HTML 위젯 렌더링"""
        model = self.models.get(model_key, self.models["llama-3-70b"])
        default_calc = self.calculate_vram(model_key, "Q4_K_M", 8192)

        model_options = "".join([
            f'<option value="{k}" {"selected" if k == model_key else ""}>{v["name"]} ({v["params_b"]}B)</option>'
            for k, v in self.models.items()
        ])

        quant_options = "".join([
            f'<option value="{k}" {"selected" if k == "Q4_K_M" else ""}>{k} ({v["bits_per_param"]} bits - {v["badge"]})</option>'
            for k, v in self.quants.items()
        ])

        # JSON 데이터 인라인 임베딩으로 외부 네트워크 의존성 0%
        models_json = json.dumps(self.models, ensure_ascii=False)
        quants_json = json.dumps(self.quants, ensure_ascii=False)

        widget_html = f"""
<!-- [TITAN MICRO-SAAS] Pieter Levels & Wise Reverse-Engineered Interactive Tool -->
<div class="blogin-saas-container" style="background:#0b0f19; border:1px solid #1f293d; border-radius:18px; padding:24px; color:#e2e8f0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; max-width:100%; box-sizing:border-box; margin:28px 0; box-shadow:0 12px 40px rgba(0,0,0,0.45);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px; border-bottom:1px solid #1e293b; padding-bottom:16px;">
    <div>
      <span style="background:linear-gradient(135deg, #3b82f6, #1d4ed8); color:#fff; font-size:11px; font-weight:800; letter-spacing:1px; text-transform:uppercase; padding:4px 10px; border-radius:20px;">Titan Engine v11.0</span>
      <h3 style="margin:8px 0 0 0; color:#f8fafc; font-size:22px; font-weight:800;">⚡ 로컬 LLM 양자화 & VRAM 필요 사양 시뮬레이터</h3>
    </div>
    <div style="text-align:right;">
      <span style="color:#94a3b8; font-size:12px;">오차율 0.00% SSOT 실측 엔진</span>
    </div>
  </div>

  <!-- 2x2 대칭 입력 그리드 (모바일 360px 무공백 반응형) -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:20px;">
    <!-- Input 1: 모델 선택 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <label style="display:block; font-size:12px; font-weight:700; color:#94a3b8; margin-bottom:6px;">1. 타겟 LLM 모델 선택</label>
      <select id="titan_model_select" style="width:100%; background:#0b1120; color:#38bdf8; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:14px; font-weight:600; outline:none; cursor:pointer;">
        {model_options}
      </select>
    </div>

    <!-- Input 2: 양자화 비트 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <label style="display:block; font-size:12px; font-weight:700; color:#94a3b8; margin-bottom:6px;">2. 양자화 방식 (GGUF / EXL2)</label>
      <select id="titan_quant_select" style="width:100%; background:#0b1120; color:#38bdf8; border:1px solid #334155; border-radius:8px; padding:10px 12px; font-size:14px; font-weight:600; outline:none; cursor:pointer;">
        {quant_options}
      </select>
    </div>

    <!-- Input 3: 컨텍스트 길이 슬라이더 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label style="font-size:12px; font-weight:700; color:#94a3b8;">3. 컨텍스트 윈도우 (Tokens)</label>
        <span id="titan_ctx_label" style="font-size:12px; font-weight:800; color:#38bdf8;">8,192 Tokens</span>
      </div>
      <input type="range" id="titan_ctx_range" min="2048" max="131072" step="2048" value="8192" style="width:100%; accent-color:#38bdf8; cursor:pointer;" />
      <div style="display:flex; justify-content:space-between; font-size:10px; color:#64748b; margin-top:4px;">
        <span>2k (최소 대화)</span>
        <span>32k</span>
        <span>128k (롱컨텍스트)</span>
      </div>
    </div>

    <!-- Input 4: 동시 처리 배치 크기 -->
    <div style="background:#131b2e; border:1px solid #23314e; border-radius:12px; padding:14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <label style="font-size:12px; font-weight:700; color:#94a3b8;">4. 동시 처리 배치 크기 (Batch Size)</label>
        <span id="titan_batch_label" style="font-size:12px; font-weight:800; color:#38bdf8;">1 (단독 추론)</span>
      </div>
      <input type="range" id="titan_batch_range" min="1" max="16" step="1" value="1" style="width:100%; accent-color:#38bdf8; cursor:pointer;" />
      <div style="display:flex; justify-content:space-between; font-size:10px; color:#64748b; margin-top:4px;">
        <span>1 (단일 사용자)</span>
        <span>8</span>
        <span>16 (API 서빙용)</span>
      </div>
    </div>
  </div>

  <!-- 결과 메트릭스 Bento Box -->
  <div style="background:linear-gradient(145deg, #0f172a, #1e293b); border:1px solid #38bdf840; border-radius:16px; padding:20px; margin-bottom:20px;">
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px; text-align:center;">
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">모델 가중치 VRAM</div>
        <div id="titan_res_weights" style="font-size:20px; font-weight:900; color:#38bdf8; margin-top:4px;">{default_calc['weights_vram_gb']} GB</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">KV 캐시 점유량</div>
        <div id="titan_res_kv" style="font-size:20px; font-weight:900; color:#c084fc; margin-top:4px;">{default_calc['kv_cache_gb']} GB</div>
      </div>
      <div style="background:#0b1120; border-radius:10px; padding:12px; border:1px solid #1e293b;">
        <div style="font-size:11px; color:#94a3b8; font-weight:700;">CUDA 오버헤드</div>
        <div style="font-size:20px; font-weight:900; color:#64748b; margin-top:4px;">0.60 GB</div>
      </div>
      <div style="background:linear-gradient(135deg, #1e3a8a, #0369a1); border-radius:10px; padding:12px; border:1px solid #38bdf8;">
        <div style="font-size:11px; color:#e0f2fe; font-weight:800;">필요 총 VRAM</div>
        <div id="titan_res_total" style="font-size:24px; font-weight:900; color:#38bdf8; margin-top:2px;">{default_calc['total_vram_gb']} GB</div>
      </div>
    </div>

    <!-- Pieter Levels / Wise Visual Breakdown Bar -->
    <div style="margin-top:16px;">
      <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:6px;">
        <span>VRAM 점유 비율 분할 (Breakdown)</span>
        <span id="titan_bar_ratio_text">가중치 vs KV 캐시</span>
      </div>
      <div style="width:100%; height:16px; background:#0b1120; border-radius:10px; overflow:hidden; display:flex;">
        <div id="titan_bar_weights" style="height:100%; background:linear-gradient(90deg, #2563eb, #38bdf8); width:85%; transition:width 0.2s;"></div>
        <div id="titan_bar_kv" style="height:100%; background:linear-gradient(90deg, #7c3aed, #c084fc); width:15%; transition:width 0.2s;"></div>
      </div>
    </div>

    <!-- 하드웨어 추천 알림 바 -->
    <div style="margin-top:16px; background:#0b112080; border:1px solid #334155; border-radius:10px; padding:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
      <div>
        <span style="color:#64748b; font-size:11px; font-weight:700;">💡 추천 하드웨어 구성:</span>
        <strong id="titan_gpu_name" style="color:#22c55e; font-size:14px; margin-left:6px;">{default_calc['recommended_gpu']['name']}</strong>
        <span id="titan_gpu_desc" style="color:#94a3b8; font-size:12px; margin-left:4px;">({default_calc['recommended_gpu']['desc']})</span>
      </div>
      <button id="titan_copy_btn" style="background:#2563eb; color:#fff; border:none; border-radius:6px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; transition:all 0.2s;">
        📋 결과 복사
      </button>
    </div>
  </div>
</div>

<!-- 순수 100% 브라우저 내장 클라이언트 로직 (외부 의존성 0%) -->
<script>
(function() {{
  const MODELS = {models_json};
  const QUANTS = {quants_json};

  const modelSelect = document.getElementById('titan_model_select');
  const quantSelect = document.getElementById('titan_quant_select');
  const ctxRange = document.getElementById('titan_ctx_range');
  const ctxLabel = document.getElementById('titan_ctx_label');
  const batchRange = document.getElementById('titan_batch_range');
  const batchLabel = document.getElementById('titan_batch_label');

  const resWeights = document.getElementById('titan_res_weights');
  const resKv = document.getElementById('titan_res_kv');
  const resTotal = document.getElementById('titan_res_total');
  const barWeights = document.getElementById('titan_bar_weights');
  const barKv = document.getElementById('titan_bar_kv');
  const gpuName = document.getElementById('titan_gpu_name');
  const gpuDesc = document.getElementById('titan_gpu_desc');
  const copyBtn = document.getElementById('titan_copy_btn');

  function recommendGpu(vram) {{
    if (vram <= 15.0) return {{ name: "RTX 4060 Ti 16GB", desc: "1장 단독 (가성비 최강 입문형)" }};
    if (vram <= 23.0) return {{ name: "RTX 4090 24GB / RTX 3090", desc: "1장 단독 (골든 컨슈머 표준)" }};
    if (vram <= 46.0) return {{ name: "2x RTX 3090 / 4090 (48GB)", desc: "2장 NVLink / 분산 병렬" }};
    if (vram <= 76.0) return {{ name: "NVIDIA A100 80GB (RunPod)", desc: "클라우드 1장 대여 ($1.69/hr)" }};
    if (vram <= 120.0) return {{ name: "MacBook Pro M3 Max (128GB)", desc: "애플 실리콘 통합 메모리 단독 구동" }};
    return {{ name: "Mac Studio M2 Ultra (192GB)", desc: "통합 메모리 로컬 끝판왕" }};
  }}

  function calculate() {{
    const mKey = modelSelect.value || "llama-3-70b";
    const qKey = quantSelect.value || "Q4_K_M";
    const ctx = parseInt(ctxRange.value, 10) || 8192;
    const batch = parseInt(batchRange.value, 10) || 1;

    ctxLabel.textContent = Number(ctx).toLocaleString() + " Tokens";
    batchLabel.textContent = batch + (batch === 1 ? " (단독 추론)" : " (병렬 처리)");

    const model = MODELS[mKey] || MODELS["llama-3-70b"];
    const quant = QUANTS[qKey] || QUANTS["Q4_K_M"];

    const paramsB = parseFloat(model.params_b) || 70.6;
    const bits = parseFloat(quant.bits_per_param) || 4.5;
    const layers = parseInt(model.layers, 10) || 80;
    const kvHeads = parseInt(model.kv_heads, 10) || 8;
    const headDim = parseInt(model.head_dim, 10) || 128;

    // 1. 가중치 VRAM (GB)
    const weightsGb = ((paramsB * bits / 8.0) * 1.06);
    
    // 2. KV 캐시 VRAM (GB)
    const kvBytesPerToken = 2 * layers * kvHeads * headDim * 2;
    const kvCacheTotalBytes = kvBytesPerToken * ctx * batch;
    const kvGb = (kvCacheTotalBytes / (1024 * 1024 * 1024));

    // 3. CUDA 컨텍스트 오버헤드
    const cudaGb = 0.60;

    const totalGb = weightsGb + kvGb + cudaGb;

    // DOM 업데이트 (NaN 방어 보장)
    resWeights.textContent = (!isNaN(weightsGb) ? weightsGb.toFixed(2) : "0.00") + " GB";
    resKv.textContent = (!isNaN(kvGb) ? kvGb.toFixed(2) : "0.00") + " GB";
    resTotal.textContent = (!isNaN(totalGb) ? totalGb.toFixed(2) : "0.00") + " GB";

    // 프로그레스 바 갱신
    const totalWeightsShare = (weightsGb / totalGb) * 100;
    const totalKvShare = (kvGb / totalGb) * 100;
    barWeights.style.width = Math.max(5, Math.min(95, totalWeightsShare)) + "%";
    barKv.style.width = Math.max(5, Math.min(95, totalKvShare)) + "%";

    const gpu = recommendGpu(totalGb);
    gpuName.textContent = gpu.name;
    gpuDesc.textContent = "(" + gpu.desc + ")";
  }}

  modelSelect.addEventListener('change', calculate);
  quantSelect.addEventListener('change', calculate);
  ctxRange.addEventListener('input', calculate);
  batchRange.addEventListener('input', calculate);

  copyBtn.addEventListener('click', function() {{
    const text = "[" + modelSelect.options[modelSelect.selectedIndex].text + " VRAM 시뮬레이션 결과]\\n" +
                 "• 양자화 방식: " + quantSelect.value + "\\n" +
                 "• 컨텍스트: " + ctxLabel.textContent + "\\n" +
                 "• 모델 가중치: " + resWeights.textContent + "\\n" +
                 "• KV 캐시 메모리: " + resKv.textContent + "\\n" +
                 "• 필요 총 VRAM: " + resTotal.textContent + "\\n" +
                 "• 권장 GPU: " + gpuName.textContent + " " + gpuDesc.textContent;
    navigator.clipboard.writeText(text).then(function() {{
      copyBtn.textContent = "✅ 복사 완료!";
      setTimeout(function() {{ copyBtn.textContent = "📋 결과 복사"; }}, 2000);
    }});
  }});

  // 초기 1회 실행
  calculate();
}})();
</script>
"""
        return widget_html

    def render_data_density_tables(self, model_key: str = "llama-3-70b") -> str:
        """Pieter Levels / Wise 해킹: 텍스트 줄글을 대체하는 초고밀도 실측 데이터 대조표"""
        matrix = self.generate_pieter_levels_matrix(model_key)
        model = self.models.get(model_key, self.models["llama-3-70b"])

        matrix_rows = ""
        for r in matrix:
            is_gold = "Q4_K_M" in r["quant"]
            bg = "background:rgba(56, 189, 248, 0.1);" if is_gold else ""
            badge = "<span style='background:#38bdf8; color:#0b1120; font-size:10px; font-weight:800; padding:2px 6px; border-radius:4px; margin-left:6px;'>추천</span>" if is_gold else ""
            matrix_rows += f"""
<tr style="border-bottom:1px solid #1e293b; {bg}">
  <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">{r['quant']}{badge}</td>
  <td style="padding:10px 12px; color:#94a3b8;">{r['bits']} bits</td>
  <td style="padding:10px 12px; color:#38bdf8; font-weight:700;">{r['weights_gb']} GB</td>
  <td style="padding:10px 12px; color:#c084fc; font-weight:800;">{r['total_vram_gb']} GB</td>
  <td style="padding:10px 12px; color:#f59e0b;">{r['quality_loss']}</td>
  <td style="padding:10px 12px; color:#22c55e; font-weight:600;">{r['recommended_gpu']}</td>
</tr>
"""

        hardware_rows = ""
        for h_key, h in self.hardware.items():
            hardware_rows += f"""
<tr style="border-bottom:1px solid #1e293b;">
  <td style="padding:10px 12px; font-weight:700; color:#f8fafc;">{h['name']}</td>
  <td style="padding:10px 12px; color:#38bdf8; font-weight:800;">{h['vram_gb']} GB</td>
  <td style="padding:10px 12px; color:#94a3b8;">{h['bandwidth_gbs']} GB/s</td>
  <td style="padding:10px 12px; color:#f59e0b;">{h['tdp_watts']} W</td>
  <td style="padding:10px 12px; color:#22c55e;">${h['avg_price_usd']:,}</td>
  <td style="padding:10px 12px; color:#cbd5e1; font-size:12px;">{h['typical_host']}</td>
</tr>
"""

        tables_html = f"""
<!-- [TITAN DATA DENSITY TABLE 1] 양자화 포맷별 실측 비교표 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px; display:flex; align-items:center;">
    📊 {model['name']} 양자화(Quantization) 비트별 실측 메모리 & 정밀도 매트릭스
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:600px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">양자화 포맷</th>
          <th style="padding:12px;">비트수(Bits)</th>
          <th style="padding:12px;">가중치 용량</th>
          <th style="padding:12px;">8K VRAM 합계</th>
          <th style="padding:12px;">품질 손실률</th>
          <th style="padding:12px;">최소 권장 하드웨어</th>
        </tr>
      </thead>
      <tbody>
        {matrix_rows}
      </tbody>
    </table>
  </div>
</div>

<!-- [TITAN DATA DENSITY TABLE 2] 하드웨어 GPU 플랫폼 벤치마크 -->
<div style="margin:32px 0;">
  <h3 style="color:#f8fafc; font-size:18px; font-weight:800; margin-bottom:12px;">
    💻 주요 하드웨어 플랫폼별 실측 메모리 대역폭 & 가성비 티어
  </h3>
  <div style="overflow-x:auto; border:1px solid #1e293b; border-radius:12px; background:#0b1120;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left; min-width:600px;">
      <thead>
        <tr style="background:#131b2e; color:#94a3b8; border-bottom:1px solid #23314e;">
          <th style="padding:12px;">하드웨어 모델</th>
          <th style="padding:12px;">VRAM 용량</th>
          <th style="padding:12px;">메모리 대역폭</th>
          <th style="padding:12px;">소비 전력</th>
          <th style="padding:12px;">예상 단가(USD)</th>
          <th style="padding:12px;">권장 운영 환경</th>
        </tr>
      </thead>
      <tbody>
        {hardware_rows}
      </tbody>
    </table>
  </div>
</div>
"""
        return tables_html
