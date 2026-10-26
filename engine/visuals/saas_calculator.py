# -*- coding: utf-8 -*-
"""
engine/visuals/saas_calculator.py
---------------------------------
Omni Calculator (옴니 칼큘레이터) & NerdWallet 벤치마크 기반 고체류 인터랙티브 Micro-SaaS 계산기 모듈.
1. Instant Reactive pure JavaScript calculation (0-latency, 슬라이더 & 숫자 실시간 양방향 연동)
2. Omni Visual Breakdown Bar (원금 vs 이자 vs 지원금 / 신규지출 vs 순수절감액 시각화 바)
3. 5대 골든 니치 전용 계산기:
   - SAVINGS: 24개월 통신비 & 알뜰폰 고정비 절감 시뮬레이터
   - SUBSIDY: 2026 정부 지원금 & 청년도약계좌/근로장려금 실수령액 모의계산기
   - TECH: 스마트 가전 & IT 테크 가성비 / 할부 vs 일시불 & 하루 커피값 시뮬레이터
   - MEDICAL: 비급여 의료 & 실손보험 본인부담금 계산기
   - CAREER: 직장인 국비지원(내일배움카드) 실부담금 & 연봉 상승 ROI 계산기
4. Zero-Broken-Entity, Zero-Persona, Anti-Slop 엄격 준수
"""

import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from engine.matcher.domain_router import (
    classify_domain,
    DOMAIN_AUTO_INSURANCE,
    DOMAIN_HEALTH_INSURANCE,
    DOMAIN_SUBSIDY,
    DOMAIN_TELECOM,
    DOMAIN_CARDS_TRAVEL,
    DOMAIN_SAVINGS,
    DOMAIN_MEDICAL,
    DOMAIN_HAIR_TRANSPLANT,
    DOMAIN_CAREER,
    DOMAIN_TECH
)
from engine.agents.prompts_chat_pack import APEX_STAFF_PROMPTS, get_staff_prompt

DEVELOPER_PROMPT = get_staff_prompt("05_Developer")

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def _clean_keyword(keyword: str) -> str:
    if not keyword:
        return "스마트 금융 & 소비"
    return keyword.replace(" 비교", "").replace(" 추천", "").strip()


def _render_savings_calc(clean_kw: str) -> str:
    """통신비 및 고정비 절감 시뮬레이터 (Omni Calculator Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">실시간 모의계산</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">📱 {clean_kw} 24개월 통신비 절감 시뮬레이터</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">현재 통신 3사 요금 대비 알뜰폰 전환 시 아낄 수 있는 24개월 누적 순수 목돈을 산출합니다.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">빠른 기본값 선택:</span>
        <button type="button" onclick="setSavingsPreset(69000, 16900)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">통신3사 표준 (6.9만 → 1.69만)</button>
        <button type="button" onclick="setSavingsPreset(89000, 25900)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">무제한 요금제 (8.9만 → 2.59만)</button>
        <button type="button" onclick="setSavingsPreset(110000, 33000)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">VIP 요금제 (11만 → 3.3만)</button>
      </div>

      <!-- Input Controls Grid: 2-Column Balanced Grid -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; margin-bottom:22px;">
        <!-- Control 1: Current Bill -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-current-bill" style="font-size:0.88rem; font-weight:700; color:#475569;">현재 월 납부 통신비</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-current-bill">69,000원</span>
          </div>
          <input type="range" id="slider-current-bill" min="30000" max="130000" step="1000" value="69000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcSavings()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>30,000원</span>
            <span>130,000원</span>
          </div>
        </div>

        <!-- Control 2: Target Bill -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-target-bill" style="font-size:0.88rem; font-weight:700; color:#475569;">전환할 알뜰폰 요금</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-target-bill">16,900원</span>
          </div>
          <input type="range" id="slider-target-bill" min="0" max="45000" step="1000" value="16900" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcSavings()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>0원 (프로모션)</span>
            <span>45,000원</span>
          </div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">24개월간 총 순수 절감 예상액</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-savings-ratio">절감율 75.5%</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-saved-total">1,250,400원 절약</div>
        
        <!-- Omni Visual Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span>새 요금제 지출 (<span id="txt-bar-cost">405,600원</span>)</span>
            <span style="color:#34d399; font-weight:700;">아낀 순수 목돈 (<span id="txt-bar-save">1,250,400원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-plan-cost" style="background:#3b82f6; width:24.5%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-plan-save" style="background:#10b981; width:75.5%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-savings-monthly">월 52,100원 순수 고정비 절감 효과 (제주도 왕복 항공권 2회분 상당)</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-savings" onclick="copyToolVal('result-saved-total', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetSavings()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-savings" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 금액 혜택 바로 조회하기</a>
    </div>

    <script>
    function calcSavings() {{
      const curr = parseInt(document.getElementById('slider-current-bill').value);
      const tgt = parseInt(document.getElementById('slider-target-bill').value);
      document.getElementById('disp-current-bill').innerText = curr.toLocaleString() + '원';
      document.getElementById('disp-target-bill').innerText = tgt.toLocaleString() + '원';
      const monthly = Math.max(0, curr - tgt);
      const total = monthly * 24;
      const totalCurr = curr * 24;
      const totalTgt = tgt * 24;
      const savePercent = totalCurr > 0 ? Math.round((total / totalCurr) * 100) : 0;
      const costPercent = Math.max(5, 100 - savePercent);

      document.getElementById('result-saved-total').innerText = total.toLocaleString() + '원 절약';
      document.getElementById('badge-savings-ratio').innerText = '절감율 ' + savePercent + '%';
      document.getElementById('txt-bar-cost').innerText = totalTgt.toLocaleString() + '원';
      document.getElementById('txt-bar-save').innerText = total.toLocaleString() + '원';
      document.getElementById('bar-plan-cost').style.width = costPercent + '%';
      document.getElementById('bar-plan-save').style.width = savePercent + '%';
      document.getElementById('desc-savings-monthly').innerText = '월 ' + monthly.toLocaleString() + '원 순수 고정비 절감 효과 (연간 약 ' + (monthly * 12).toLocaleString() + '원 절약)';

      const ctaBtn = document.getElementById('btn-calc-cta-savings');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 ' + total.toLocaleString() + '원 절약 혜택 바로 조회하기';
      }}
    }}
    function setSavingsPreset(curr, tgt) {{
      document.getElementById('slider-current-bill').value = curr;
      document.getElementById('slider-target-bill').value = tgt;
      calcSavings();
    }}
    function resetSavings() {{
      setSavingsPreset(69000, 16900);
    }}
    function copyToolVal(targetId, btn) {{
      const txt = document.getElementById(targetId).innerText;
      if (navigator.clipboard) {{
        navigator.clipboard.writeText(txt).then(() => {{
          const oldTxt = btn.innerText;
          btn.innerText = '✓ 복사 완료!';
          btn.style.background = '#10b981';
          setTimeout(() => {{
            btn.innerText = oldTxt;
            btn.style.background = '#2563eb';
          }}, 2000);
        }}).catch(() => {{
          alert('결과: ' + txt);
        }});
      }} else {{
        alert('결과: ' + txt);
      }}
    }}
    </script>
    """


def _render_subsidy_calc(clean_kw: str) -> str:
    """정부 지원금 및 청년도약계좌/근로장려금 실수령액 모의계산기 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">2026 정부 고시 기준</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">🏛️ {clean_kw} 정부 지원금 & 만기 실수령액 모의계산기</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">연소득 구간과 월 저축액을 기반으로 정부 기여금 매칭액과 비과세 만기 수령액을 즉시 계산합니다.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">소득 구간 프리셋:</span>
        <button type="button" onclick="setSubsidyPreset(2400, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">연 2,400만 이하 (최대 기여금 6.0%)</button>
        <button type="button" onclick="setSubsidyPreset(3600, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">연 3,600만 이하 (기여금 4.6%)</button>
        <button type="button" onclick="setSubsidyPreset(4800, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">연 4,800만 이하 (기여금 3.7%)</button>
      </div>

      <!-- Input Controls Grid: 2-Column Balanced Grid -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; margin-bottom:22px;">
        <!-- Control 1: Annual Income -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-annual-income" style="font-size:0.88rem; font-weight:700; color:#475569;">연간 총 급여액</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-annual-income">3,200만원</span>
          </div>
          <input type="range" id="slider-annual-income" min="1200" max="7500" step="100" value="3200" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcSubsidy()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>1,200만원</span>
            <span>7,500만원</span>
          </div>
        </div>

        <!-- Control 2: Monthly Deposit -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-monthly-deposit" style="font-size:0.88rem; font-weight:700; color:#475569;">월 저축 납입액</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-monthly-deposit">70만원</span>
          </div>
          <input type="range" id="slider-monthly-deposit" min="10" max="70" step="5" value="70" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcSubsidy()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>10만원</span>
            <span>70만원 (최대한도)</span>
          </div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">5년 만기 예상 실수령액 (원금 + 이자 + 정부지원)</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-subsidy-rate">실질 수익률 연 8.9% 상당</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-subsidy-val">약 50,280,000원 수령</div>
        
        <!-- Omni Visual 3-Way Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span style="color:#60a5fa;">원금: <span id="txt-sub-principal">4,200만</span></span>
            <span style="color:#c084fc;">은행이자: <span id="txt-sub-interest">612만</span></span>
            <span style="color:#34d399; font-weight:700;">정부기여금: <span id="txt-sub-grant">216만</span></span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-sub-principal" style="background:#3b82f6; width:83.5%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-sub-interest" style="background:#a855f7; width:12.2%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-sub-grant" style="background:#10b981; width:4.3%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-subsidy-benefit">정부기여금 216만원 + 비과세 이자 혜택 전액 수령 대상 (중위소득 100% 충족)</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-subsidy" onclick="copyToolVal('result-subsidy-val', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetSubsidy()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-subsidy" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 금액 혜택 바로 조회하기</a>
    </div>

    <script>
    function calcSubsidy() {{
      const inc = parseInt(document.getElementById('slider-annual-income').value);
      const dep = parseInt(document.getElementById('slider-monthly-deposit').value);
      document.getElementById('disp-annual-income').innerText = inc.toLocaleString() + '만원';
      document.getElementById('disp-monthly-deposit').innerText = dep + '만원';

      // 5-Year Principal: dep * 10,000 * 60
      const principal = dep * 10000 * 60;

      // Government Grant Rate by income bracket
      let grantRate = 0.030;
      if (inc <= 2400) grantRate = 0.060;
      else if (inc <= 3600) grantRate = 0.046;
      else if (inc <= 4800) grantRate = 0.037;
      else if (inc <= 6000) grantRate = 0.030;
      else grantRate = 0.0;

      // Monthly Grant (up to 33,000 KRW/month)
      const monthlyGrant = Math.min(33000, Math.round(dep * 10000 * grantRate));
      const totalGrant = monthlyGrant * 60;

      // Approximate Bank Interest (approx 5.5% annual average compounding / simple tax-exempt equivalent)
      const totalInterest = Math.round(principal * 0.145);
      const totalSum = principal + totalInterest + totalGrant;

      const pPct = Math.round((principal / totalSum) * 100);
      const gPct = Math.max(2, Math.round((totalGrant / totalSum) * 100));
      const iPct = Math.max(2, 100 - pPct - gPct);

      document.getElementById('result-subsidy-val').innerText = '약 ' + Math.round(totalSum / 10000).toLocaleString() + '만원 수령';
      document.getElementById('txt-sub-principal').innerText = Math.round(principal / 10000).toLocaleString() + '만';
      document.getElementById('txt-sub-interest').innerText = Math.round(totalInterest / 10000).toLocaleString() + '만';
      document.getElementById('txt-sub-grant').innerText = Math.round(totalGrant / 10000).toLocaleString() + '만';

      document.getElementById('bar-sub-principal').style.width = pPct + '%';
      document.getElementById('bar-sub-interest').style.width = iPct + '%';
      document.getElementById('bar-sub-grant').style.width = gPct + '%';

      const apr = inc <= 2400 ? '9.4%' : (inc <= 3600 ? '8.9%' : '7.8%');
      document.getElementById('badge-subsidy-rate').innerText = '실질 수익률 연 ' + apr + ' 상당';
      document.getElementById('desc-subsidy-benefit').innerText = '정부기여금 ' + Math.round(totalGrant / 10000) + '만원 + 비과세 은행이자 ' + Math.round(totalInterest / 10000) + '만원 전액 수령 대상';

      const ctaBtn = document.getElementById('btn-calc-cta-subsidy');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 약 ' + Math.round(totalSum / 10000).toLocaleString() + '만원 혜택 바로 조회하기';
      }}
    }}
    function setSubsidyPreset(inc, dep) {{
      document.getElementById('slider-annual-income').value = inc;
      document.getElementById('slider-monthly-deposit').value = dep;
      calcSubsidy();
    }}
    function resetSubsidy() {{
      setSubsidyPreset(3200, 70);
    }}
    </script>
    """


def _render_tech_calc(clean_kw: str) -> str:
    """스마트 테크 및 가전 가성비 / 할부 체감비용 계산기 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">스마트 테크 소비</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">🛒 {clean_kw} 가성비 & 카드 무이자 할부 계산기</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">구매 예산과 사용 개월 수를 입력하여 일할 체감 비용(커피값 환산)과 중고 잔존가치를 확인하세요.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">기기별 대표 견적:</span>
        <button type="button" onclick="setGadgetPreset(1590000, 24)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">맥북 에어 / 159만</button>
        <button type="button" onclick="setGadgetPreset(1700000, 24)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">플래그십 스마트폰 / 170만</button>
        <button type="button" onclick="setGadgetPreset(1200000, 36)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">올인원 로봇청소기 / 120만</button>
      </div>

      <!-- Input Controls Grid: 2-Column Balanced Grid -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; margin-bottom:22px;">
        <!-- Control 1: Price -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-gadget-price" style="font-size:0.88rem; font-weight:700; color:#475569;">구매 가격</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-gadget-price">1,250,000원</span>
          </div>
          <input type="range" id="slider-gadget-price" min="200000" max="3500000" step="50000" value="1250000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcGadget()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>200,000원</span>
            <span>3,500,000원</span>
          </div>
        </div>

        <!-- Control 2: Term -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-gadget-term" style="font-size:0.88rem; font-weight:700; color:#475569;">예상 사용 기간</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-gadget-term">24개월</span>
          </div>
          <input type="range" id="slider-gadget-term" min="6" max="48" step="6" value="24" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcGadget()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>6개월</span>
            <span>48개월 (4년)</span>
          </div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">하루 체감 비용 (커피값 환산)</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-gadget-coffee">아메리카노 1/3잔 수준</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-gadget-daily">하루 약 1,736원</div>
        
        <!-- Omni Visual Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span>일할 체감 사용비용 (<span id="txt-gadget-use">750,000원</span>)</span>
            <span style="color:#34d399; font-weight:700;">중고 잔존가치 회수분 (<span id="txt-gadget-resale">500,000원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-gadget-use" style="background:#3b82f6; width:60%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-gadget-resale" style="background:#10b981; width:40%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-gadget-monthly">24개월 무이자 할부 시 월 52,080원 수준 (사용 후 약 40% 중고가 회수 가능)</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-gadget" onclick="copyToolVal('result-gadget-daily', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetGadget()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-gadget" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 금액 혜택 바로 조회하기</a>
    </div>

    <script>
    function calcGadget() {{
      const pr = parseInt(document.getElementById('slider-gadget-price').value);
      const term = parseInt(document.getElementById('slider-gadget-term').value);
      document.getElementById('disp-gadget-price').innerText = pr.toLocaleString() + '원';
      document.getElementById('disp-gadget-term').innerText = term + '개월';

      const daily = Math.round(pr / (term * 30));
      const monthly = Math.round(pr / term);
      const resaleRate = term <= 12 ? 0.55 : (term <= 24 ? 0.40 : 0.25);
      const resaleVal = Math.round(pr * resaleRate);
      const netConsume = pr - resaleVal;
      const netDaily = Math.round(netConsume / (term * 30));

      const usePct = Math.round((netConsume / pr) * 100);
      const resalePct = Math.max(10, 100 - usePct);

      document.getElementById('result-gadget-daily').innerText = '하루 약 ' + daily.toLocaleString() + '원';
      document.getElementById('txt-gadget-use').innerText = netConsume.toLocaleString() + '원';
      document.getElementById('txt-gadget-resale').innerText = resaleVal.toLocaleString() + '원';
      document.getElementById('bar-gadget-use').style.width = usePct + '%';
      document.getElementById('bar-gadget-resale').style.width = resalePct + '%';

      const coffeeRate = daily < 2000 ? '아메리카노 1/2잔 미만' : (daily < 4000 ? '아메리카노 1잔 수준' : '라떼 1잔 상당');
      document.getElementById('badge-gadget-coffee').innerText = coffeeRate;
      document.getElementById('desc-gadget-monthly').innerText = term + '개월 무이자 할부 시 월 ' + monthly.toLocaleString() + '원 (중고 방어율 고려 실질 하루 ' + netDaily.toLocaleString() + '원)';

      const ctaBtn = document.getElementById('btn-calc-cta-gadget');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 하루 ' + daily.toLocaleString() + '원 최저가 바로 조회하기';
      }}
    }}
    function setGadgetPreset(pr, term) {{
      document.getElementById('slider-gadget-price').value = pr;
      document.getElementById('slider-gadget-term').value = term;
      calcGadget();
    }}
    function resetGadget() {{
      setGadgetPreset(1250000, 24);
    }}
    </script>
    """


def _render_medical_calc(clean_kw: str) -> str:
    """비급여 의료비 및 실손보험 본인부담금 계산기 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">심평원 비급여 기준</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">🏥 {clean_kw} 실손보험 환급액 & 본인부담금 계산기</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">예상 비급여 진료비와 실손보험 세대별 공제율을 대조하여 실제 환자 부담금을 산출합니다.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">치료 목적 비급여 예시:</span>
        <button type="button" onclick="setMedicalPreset(1500000, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">도수치료 10회 (150만)</button>
        <button type="button" onclick="setMedicalPreset(600000, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">MRI 정밀검사 (60만)</button>
        <button type="button" onclick="setMedicalPreset(300000, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">체외충격파 (30만)</button>
      </div>
      <div style="font-size:0.78rem; color:#b91c1c; background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:8px 12px; margin-bottom:16px;">
        ⚠️ <strong>면책 유의사항:</strong> 치과 비급여(임플란트·보철), 시력교정술(라식·라섹), 단순 미용 치료는 실손보험 표준약관상 보상 제외(면책) 항목입니다.
      </div>

      <!-- Input Controls Grid: 2-Column Balanced Grid -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; margin-bottom:22px;">
        <!-- Control 1: Medical Expense -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-med-cost" style="font-size:0.88rem; font-weight:700; color:#475569;">총 예상 비급여 치료비</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-med-cost">2,400,000원</span>
          </div>
          <input type="range" id="slider-med-cost" min="300000" max="8000000" step="100000" value="2400000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcMedical()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>300,000원</span>
            <span>8,000,000원</span>
          </div>
        </div>

        <!-- Control 2: Coverage Rate -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-med-rate" style="font-size:0.88rem; font-weight:700; color:#475569;">실손보험 환급 보장율</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-med-rate">70% (4세대 실손)</span>
          </div>
          <input type="range" id="slider-med-rate" min="60" max="100" step="10" value="70" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcMedical()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>4세대 (70%)</span>
            <span>1세대 구실손 (100%)</span>
          </div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">최종 환자 본인 실부담금 (환급 후)</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-med-reduction">비용 70% 절감</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-med-outpocket">720,000원 부담</div>
        
        <!-- Omni Visual Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span style="color:#34d399; font-weight:700;">실손보험 환급액 (<span id="txt-med-refund">1,680,000원</span>)</span>
            <span>본인 실부담금 (<span id="txt-med-pay">720,000원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-med-refund" style="background:#10b981; width:70%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-med-pay" style="background:#3b82f6; width:30%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-med-detail">보험 청구 시 1,680,000원 수령 가능 (진료비 세부내역서 및 영수증 필수)</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-med" onclick="copyToolVal('result-med-outpocket', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetMedical()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-med" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 금액 혜택 바로 조회하기</a>
    </div>

    <script>
    function calcMedical() {{
      const cost = parseInt(document.getElementById('slider-med-cost').value);
      const rate = parseInt(document.getElementById('slider-med-rate').value);
      document.getElementById('disp-med-cost').innerText = cost.toLocaleString() + '원';
      const genText = rate >= 95 ? '1세대 (100%)' : (rate >= 85 ? '2세대 (90%)' : (rate >= 75 ? '3세대 (80%)' : '4세대 (70%)'));
      document.getElementById('disp-med-rate').innerText = rate + '% (' + genText + ')';

      const refund = Math.round(cost * (rate / 100));
      const outpocket = Math.max(0, cost - refund);

      document.getElementById('result-med-outpocket').innerText = outpocket.toLocaleString() + '원 부담';
      document.getElementById('txt-med-refund').innerText = refund.toLocaleString() + '원';
      document.getElementById('txt-med-pay').innerText = outpocket.toLocaleString() + '원';
      document.getElementById('bar-med-refund').style.width = rate + '%';
      document.getElementById('bar-med-pay').style.width = (100 - rate) + '%';
      document.getElementById('badge-med-reduction').innerText = '비용 ' + rate + '% 절감';
      document.getElementById('desc-med-detail').innerText = '보험 청구 시 약 ' + refund.toLocaleString() + '원 환급 (진료비 세부내역서 및 영수증 필수 지참)';

      const ctaBtn = document.getElementById('btn-calc-cta-med');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 ' + refund.toLocaleString() + '원 환급 혜택 바로 조회하기';
      }}
    }}
    function setMedicalPreset(cost, rate) {{
      document.getElementById('slider-med-cost').value = cost;
      document.getElementById('slider-med-rate').value = rate;
      calcMedical();
    }}
    function resetMedical() {{
      setMedicalPreset(1500000, 70);
    }}
    </script>
    """


def _render_hair_transplant_calc(clean_kw: str) -> str:
    """
    모발이식 실측 견적 & 1~3년 숨은 비용 시뮬레이터 (v8.0 Apex).
    [철칙 3-6] 견적서에 없는 숨은 비용(수술비, 1~3년 약값, 교통비, 세액공제 한도액) 1원 단위 시뮬레이션.
    """
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">심평원 비급여 공시 & 법령 기준</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">💇 {clean_kw} 견적서에 없는 1~3년 숨은 총비용 시뮬레이터</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">수술 기법별 기본 수술비 외에 1~3년 약값, 마취비, 교통비 및 세액공제(소득세법 제59조의4) 유무를 1원 단위까지 정밀 산출합니다.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">빠른 견적 프리셋:</span>
        <button type="button" onclick="setHairPreset(3000, 'fue', 2, 'cosmetic')" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">3,000모 비절개 FUE (2년 약값)</button>
        <button type="button" onclick="setHairPreset(2000, 'fue', 1, 'cosmetic')" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">2,000모 M자 초기 (1년 약값)</button>
        <button type="button" onclick="setHairPreset(3000, 'fut', 2, 'cosmetic')" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">3,000모 절개 FUT (가성비)</button>
      </div>

      <div style="font-size:0.78rem; color:#1e3a8a; background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:8px 12px; margin-bottom:16px;">
        📌 <strong>모수 vs 모낭수 공식 기준:</strong> 한국인 평균 1모낭당 약 2.14개의 모발이 자랍니다. (예: 3,000모 이식 = 약 1,400모낭 환산)
      </div>

      <!-- Input Controls Grid: 2x2 완벽 대칭 균형 그리드 (빈 공간 0% 완전 제거) -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:16px; margin-bottom:20px;">
        <!-- Control 1: Total Hairs -->
        <div data-calc-card="true" style="background:#f8fafc; padding:18px 20px; border-radius:14px; border:1px solid #e2e8f0; display:flex; flex-direction:column; justify-content:space-between; min-height:124px; box-sizing:border-box;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <label for="slider-hair-count" style="font-size:0.85rem; font-weight:700; color:#475569;">이식 모수 (Hair Count)</label>
            <span style="font-size:1rem; font-weight:800; color:#0f172a;" id="disp-hair-count">3,000모 (약 1,400모낭)</span>
          </div>
          <input type="range" id="slider-hair-count" min="1000" max="5000" step="100" value="3000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcHairTransplant()" />
          <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:#94a3b8; margin-top:4px;">
            <span>1,000모 (밀도보강)</span>
            <span>5,000모 (대량이식)</span>
          </div>
        </div>

        <!-- Control 2: Technique -->
        <div data-calc-card="true" style="background:#f8fafc; padding:18px 20px; border-radius:14px; border:1px solid #e2e8f0; display:flex; flex-direction:column; justify-content:space-between; min-height:124px; box-sizing:border-box;">
          <label style="font-size:0.85rem; font-weight:700; color:#475569; display:block; margin-bottom:8px;">수술 기법 (심평원 공시 기준)</label>
          <select id="select-hair-method" onchange="calcHairTransplant()" style="width:100%; padding:10px 12px; border-radius:8px; border:1px solid #cbd5e1; font-size:0.88rem; font-weight:700; color:#0f172a; background:#ffffff;">
            <option value="fue" selected>비절개 (FUE) - 1모낭당 4,500원 (흉터 최소)</option>
            <option value="fut">절개 (FUT) - 1모낭당 3,200원 (가성비 최우선)</option>
            <option value="non_shaven">무삭발 비절개 - 1모낭당 7,200원 (티 안 남)</option>
          </select>
          <div style="font-size:0.72rem; color:#64748b; margin-top:4px;">대표원장 직접 집도 및 슬릿(Slit) 방식 기준 공시가</div>
        </div>

        <!-- Control 3: Medication Years -->
        <div data-calc-card="true" style="background:#f8fafc; padding:18px 20px; border-radius:14px; border:1px solid #e2e8f0; display:flex; flex-direction:column; justify-content:space-between; min-height:124px; box-sizing:border-box;">
          <label style="font-size:0.85rem; font-weight:700; color:#475569; display:block; margin-bottom:8px;">탈모약 복용 유지 기간</label>
          <select id="select-hair-years" onchange="calcHairTransplant()" style="width:100%; padding:10px 12px; border-radius:8px; border:1px solid #cbd5e1; font-size:0.88rem; font-weight:700; color:#0f172a; background:#ffffff;">
            <option value="1">1년 복용 (약값 연 28만원)</option>
            <option value="2" selected>2년 복용 (약값 누적 56만원)</option>
            <option value="3">3년 복용 (약값 누적 84만원)</option>
          </select>
          <div style="font-size:0.72rem; color:#64748b; margin-top:4px;">피나스테리드/두타스테리드 정품 처방 기준</div>
        </div>

        <!-- Control 4: Tax Deductible Status -->
        <div data-calc-card="true" style="background:#f8fafc; padding:18px 20px; border-radius:14px; border:1px solid #e2e8f0; display:flex; flex-direction:column; justify-content:space-between; min-height:124px; box-sizing:border-box;">
          <label style="font-size:0.85rem; font-weight:700; color:#475569; display:block; margin-bottom:8px;">소득세법 제59조의4 세액공제</label>
          <select id="select-hair-tax" onchange="calcHairTransplant()" style="width:100%; padding:10px 12px; border-radius:8px; border:1px solid #cbd5e1; font-size:0.88rem; font-weight:700; color:#0f172a; background:#ffffff;">
            <option value="cosmetic" selected>미용 목적 (세액공제 0원 제외 팩트)</option>
            <option value="medical">외상·화상 재건 치료 (15% 세액공제 대상)</option>
          </select>
          <div style="font-size:0.72rem; color:#dc2626; margin-top:4px; font-weight:600;">국세청 홈택스 공식 유권해석 기준 적용</div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">견적서 밖 숨은 비용 포함 3개년 실부담 총액</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-hair-breakdown">수술비 + 2년 유지비 합산</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-hair-total">7,060,000원 (1원 단위)</div>

        <!-- Omni Visual Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span style="color:#60a5fa; font-weight:700;">기본 수술비 (<span id="txt-hair-surgery">6,300,000원</span>)</span>
            <span style="color:#f59e0b; font-weight:700;">숨은 유지비·약값 (<span id="txt-hair-hidden">760,000원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-hair-surgery" style="background:#3b82f6; width:89%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-hair-hidden" style="background:#f59e0b; width:11%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px; line-height:1.5;" id="desc-hair-detail">
          기본 수술비 6,300,000원 + 2년 약값 560,000원 + 마취·교통·관리비 200,000원 (미용 목적으로 세액공제 0원)
        </div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-hair" onclick="copyToolVal('result-hair-total', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetHairTransplant()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-hair" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 3개년 총비용 상세 견적서 비교하기</a>
    </div>

    <script>
    function calcHairTransplant() {{
      const hairs = parseInt(document.getElementById('slider-hair-count').value);
      const method = document.getElementById('select-hair-method').value;
      const years = parseInt(document.getElementById('select-hair-years').value);
      const taxType = document.getElementById('select-hair-tax').value;

      const grafts = Math.round(hairs / 2.14);
      document.getElementById('disp-hair-count').innerText = hairs.toLocaleString() + '모 (약 ' + grafts.toLocaleString() + '모낭)';

      let unitPrice = 4500;
      if (method === 'fut') unitPrice = 3200;
      if (method === 'non_shaven') unitPrice = 7200;

      const surgeryCost = grafts * unitPrice;
      const medCost = years * 280000;
      const hiddenMiscCost = 200000;

      let taxDeduction = 0;
      if (taxType === 'medical') {{
        taxDeduction = Math.round((surgeryCost + medCost) * 0.15);
      }}

      const totalOutpocket = Math.max(0, surgeryCost + medCost + hiddenMiscCost - taxDeduction);

      document.getElementById('result-hair-total').innerText = totalOutpocket.toLocaleString() + '원 (1원 단위)';
      document.getElementById('txt-hair-surgery').innerText = surgeryCost.toLocaleString() + '원';
      document.getElementById('txt-hair-hidden').innerText = (medCost + hiddenMiscCost - taxDeduction).toLocaleString() + '원';

      const surgeryPct = Math.round((surgeryCost / Math.max(1, surgeryCost + medCost + hiddenMiscCost)) * 100);
      const hiddenPct = 100 - surgeryPct;
      document.getElementById('bar-hair-surgery').style.width = surgeryPct + '%';
      document.getElementById('bar-hair-hidden').style.width = hiddenPct + '%';

      let taxNote = taxType === 'medical' ? ' (외상 재건 15% 세액공제 -' + taxDeduction.toLocaleString() + '원 반영)' : ' (소득세법 제59조의4 미용 목적으로 세액공제 0원)';
      document.getElementById('desc-hair-detail').innerText = '기본 수술비 ' + surgeryCost.toLocaleString() + '원 + ' + years + '년 약값 ' + medCost.toLocaleString() + '원 + 부대비용 ' + hiddenMiscCost.toLocaleString() + '원' + taxNote;

      const ctaBtn = document.getElementById('btn-calc-cta-hair');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 ' + totalOutpocket.toLocaleString() + '원 총비용 견적서 비교하기';
      }}
    }}

    function setHairPreset(hairs, method, years, taxType) {{
      document.getElementById('slider-hair-count').value = hairs;
      document.getElementById('select-hair-method').value = method;
      document.getElementById('select-hair-years').value = years;
      document.getElementById('select-hair-tax').value = taxType;
      calcHairTransplant();
    }}

    function resetHairTransplant() {{
      setHairPreset(3000, 'fue', 2, 'cosmetic');
    }}

    // Auto-eject any alien ad elements injected by theme scripts
    function ejectCalcAliens() {{
      var grid = document.querySelector('.b365-calc-input-grid');
      if (grid) {{
        Array.from(grid.children).forEach(function(c) {{
          if ((c.id && c.id.indexOf('HTML') === 0) || c.classList.contains('widget') || (c.classList.contains('mb-4') && !c.hasAttribute('data-calc-card'))) {{
            c.remove();
          }}
        }});
      }}
    }}
    ejectCalcAliens();
    var gridEl = document.querySelector('.b365-calc-input-grid');
    if (gridEl) {{
      var obs = new MutationObserver(function() {{ ejectCalcAliens(); }});
      obs.observe(gridEl, {{ childList: true, subtree: false }});
    }}
    window.addEventListener('load', ejectCalcAliens);
    setTimeout(ejectCalcAliens, 400);
    setTimeout(ejectCalcAliens, 1200);
    </script>
    """


def _render_career_calc(clean_kw: str) -> str:
    """직장인 국비지원(내일배움카드) 실부담금 & 연봉 ROI 계산기 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">고용노동부 HRD-Net 기준</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">🎓 {clean_kw} 국비지원 자부담금 & 투자 회수 ROI 계산기</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">교육비 정가와 국비지원율을 대조하여 실제 자부담금과 취업/이직 후 투자금 회수 기간을 산출합니다.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">자격 과정별 견적:</span>
        <button type="button" onclick="setCareerPreset(1500000, 75, 30)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">데이터분석 / 150만 (75% 지원)</button>
        <button type="button" onclick="setCareerPreset(2500000, 85, 45)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">K-디지털 트레이닝 (85% 지원)</button>
        <button type="button" onclick="setCareerPreset(850000, 70, 20)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">전기/산업안전기사 (70% 지원)</button>
      </div>

      <!-- Input Controls Grid: 2-Column Balanced Grid -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; margin-bottom:22px;">
        <!-- Control 1: Course Tuition -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-tuition" style="font-size:0.88rem; font-weight:700; color:#475569;">교육과정 정가</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-tuition">1,800,000원</span>
          </div>
          <input type="range" id="slider-tuition" min="300000" max="4500000" step="50000" value="1800000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcCareer()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>300,000원</span>
            <span>4,500,000원</span>
          </div>
        </div>

        <!-- Control 2: Support Rate -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-support-rate" style="font-size:0.88rem; font-weight:700; color:#475569;">국비지원율 (유형별)</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-support-rate">75% (일반근로자)</span>
          </div>
          <input type="range" id="slider-support-rate" min="50" max="100" step="5" value="75" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcCareer()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>50%</span>
            <span>100% (취성패 1유형)</span>
          </div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">최종 교육생 실부담 수강료</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-career-roi">투자 회수: 1.5개월</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-career-pay">450,000원 부담</div>
        
        <!-- Omni Visual Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span style="color:#34d399; font-weight:700;">정부 국비 지원금 (<span id="txt-career-grant">1,350,000원</span>)</span>
            <span>본인 부담금 (<span id="txt-career-self">450,000원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-career-grant" style="background:#10b981; width:75%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-career-self" style="background:#3b82f6; width:25%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-career-detail">정부 지원금 1,350,000원 즉시 할인 (내일배움카드 300~500만원 한도 내 차감)</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-career" onclick="copyToolVal('result-career-pay', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetCareer()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-career" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 금액 혜택 바로 조회하기</a>
    </div>

    <script>
    function calcCareer() {{
      const t = parseInt(document.getElementById('slider-tuition').value);
      const r = parseInt(document.getElementById('slider-support-rate').value);
      document.getElementById('disp-tuition').innerText = t.toLocaleString() + '원';
      document.getElementById('disp-support-rate').innerText = r + '%';

      const grant = Math.round(t * (r / 100));
      const selfPay = Math.max(0, t - grant);

      document.getElementById('result-career-pay').innerText = selfPay.toLocaleString() + '원 부담';
      document.getElementById('txt-career-grant').innerText = grant.toLocaleString() + '원';
      document.getElementById('txt-career-self').innerText = selfPay.toLocaleString() + '원';
      document.getElementById('bar-career-grant').style.width = r + '%';
      document.getElementById('bar-career-self').style.width = (100 - r) + '%';

      const paybackMonths = Math.max(0.5, (selfPay / 300000)).toFixed(1);
      document.getElementById('badge-career-roi').innerText = '투자 회수 약 ' + paybackMonths + '개월';
      document.getElementById('desc-career-detail').innerText = '정부 지원금 ' + grant.toLocaleString() + '원 즉시 혜택 (월 급여 30만원 상승 시 단 ' + paybackMonths + '개월 만에 자부담 전액 회수)';

      const ctaBtn = document.getElementById('btn-calc-cta-career');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 ' + grant.toLocaleString() + '원 국비 혜택 바로 조회하기';
      }}
    }}
    function setCareerPreset(t, r, inc) {{
      document.getElementById('slider-tuition').value = t;
      document.getElementById('slider-support-rate').value = r;
      calcCareer();
    }}
    function resetCareer() {{
      setCareerPreset(1800000, 75, 30);
    }}
    </script>
    """


def render_cost_spec_comparison_table(clean_kw: str, category_code: str = "MEDICAL") -> str:
    """
    [Patch 3] 실제 견적 및 비용 항목별 상세 비교표 (비급여 시술 및 비공식 산정 주제 대체용).
    임플란트, 라식 등 정형화된 공제율 산정이 불가한 주제에서 억지 계산기 대신
    현실적인 세부 견적 대조표와 실시간 비용 모의 시뮬레이션을 제공합니다.
    """
    return f"""
    <div class="saas-calculator editorial-calculator-card cost-comparison-table" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">2026 시장 실측치</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">📊 {clean_kw} 실제 견적 및 항목별 비용 상세 비교표</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">심평원 및 시장 실측 가격을 바탕으로 옵션별 평균 견적과 지원 기준을 산출합니다.</p>
        </div>
      </div>

      <!-- Quick Option Buttons -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">대표 선택 옵션:</span>
        <button type="button" onclick="setCostTableOption(1150000, '국산 보급형 (오스템/덴티움)')" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">국산 표준 (115만/대)</button>
        <button type="button" onclick="setCostTableOption(1850000, '외산 프리미엄 (스트라우만)')" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">외산 프리미엄 (185만/대)</button>
        <button type="button" onclick="setCostTableOption(400000, '만 65세 이상 건보 30% 적용')" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">만 65세 건보 (약 40만/대)</button>
      </div>

      <!-- Interactive Cost Slider -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-cost-unit-price" style="font-size:0.88rem; font-weight:700; color:#475569;">1대당 기준 단가</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-cost-unit-price">1,150,000원</span>
          </div>
          <input type="range" id="slider-cost-unit-price" min="400000" max="2500000" step="50000" value="1150000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcCostTable()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>400,000원 (건보적용)</span>
            <span>2,500,000원 (최고급)</span>
          </div>
        </div>

        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-cost-count" style="font-size:0.88rem; font-weight:700; color:#475569;">예상 시술 / 적용 수량</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-cost-count">1대 (기본)</span>
          </div>
          <input type="range" id="slider-cost-count" min="1" max="4" step="1" value="1" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcCostTable()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>1대</span>
            <span>4대 (다수 치아)</span>
          </div>
        </div>
      </div>

      <!-- Real Cost Comparison Table -->
      <div style="margin-bottom:20px; overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; min-width:500px; font-size:13px; text-align:left;">
          <thead>
            <tr style="background:#f1f5f9; color:#1e293b; border-bottom:2px solid #cbd5e1;">
              <th style="padding:10px 12px; font-weight:800;">구분 / 사양</th>
              <th style="padding:10px 12px; font-weight:800;">평균 실측 비용</th>
              <th style="padding:10px 12px; font-weight:800;">핵심 특징 및 보험 적용</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:10px 12px; font-weight:700;">국산 표준 (오스템/덴티움)</td>
              <td style="padding:10px 12px; color:#2563eb; font-weight:800;">100만 ~ 125만원</td>
              <td style="padding:10px 12px; color:#475569;">국내 최다 임상, 부품 교체 및 사후 관리 용이</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:10px 12px; font-weight:700;">외산 프리미엄 (스트라우만)</td>
              <td style="padding:10px 12px; color:#2563eb; font-weight:800;">160만 ~ 210만원</td>
              <td style="padding:10px 12px; color:#475569;">조기 골유착 표면 처리, 고령·골질 취약층 유리</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:10px 12px; font-weight:700;">만 65세 건강보험 적용</td>
              <td style="padding:10px 12px; color:#10b981; font-weight:800;">약 38만 ~ 42만원 (본인 30%)</td>
              <td style="padding:10px 12px; color:#475569;">평생 2개 한도 지원 (단, 완전 무치악 제외)</td>
            </tr>
            <tr style="background:#f8fafc;">
              <td style="padding:10px 12px; font-weight:700;">뼈이식 (치조골 이식 추가)</td>
              <td style="padding:10px 12px; color:#d97706; font-weight:800;">30만 ~ 50만원 별도</td>
              <td style="padding:10px 12px; color:#475569;">잇몸뼈 흡수 심할 때 필수 (비급여)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">선택 조건 기준 총 예상 비용</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-cost-option">국산 표준 기준</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-cost-total">1,150,000원 예상</div>
        
        <!-- Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span>기준 식립 비용 (<span id="txt-bar-base">1,150,000원</span>)</span>
            <span style="color:#38bdf8; font-weight:700;">적용 수량 (<span id="txt-bar-units">1대</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-cost-base" style="background:#3b82f6; width:75%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-cost-extra" style="background:#10b981; width:25%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-cost-detail">치과 비급여 항목은 실손보험 보상 제외 대상이며, 뼈이식 여부에 따라 추가 비용이 발생할 수 있습니다.</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-cost" onclick="copyToolVal('result-cost-total', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">견적 결과 복사하기</button>
        <button type="button" onclick="resetCostTable()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA Button -->
      <a href="#article-search-nav" id="btn-calc-cta-cost" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 견적 및 맞춤 조건 바로 조회하기</a>
    </div>

    <script>
    function calcCostTable() {{
      const price = parseInt(document.getElementById('slider-cost-unit-price').value);
      const count = parseInt(document.getElementById('slider-cost-count').value);
      const total = price * count;

      document.getElementById('disp-cost-unit-price').innerText = price.toLocaleString() + '원';
      document.getElementById('disp-cost-count').innerText = count + '대';

      document.getElementById('result-cost-total').innerText = total.toLocaleString() + '원 예상';
      document.getElementById('txt-bar-base').innerText = total.toLocaleString() + '원';
      document.getElementById('txt-bar-units').innerText = count + '대';

      const ctaBtn = document.getElementById('btn-calc-cta-cost');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 계산된 ' + total.toLocaleString() + '원 견적 세부 조건 바로 조회하기';
      }}
    }}
    function setCostTableOption(price, name) {{
      document.getElementById('slider-cost-unit-price').value = price;
      const badge = document.getElementById('badge-cost-option');
      if (badge) badge.innerText = name;
      calcCostTable();
    }}
    function resetCostTable() {{
      setCostTableOption(1150000, '국산 보급형 (오스템/덴티움)');
      document.getElementById('slider-cost-count').value = 1;
      calcCostTable();
    }}
    </script>
    """


def _render_auto_insurance_calc(clean_kw: str) -> str:
    """자동차보험 및 다이렉트 보험료 절감 & 특약 할인 시뮬레이터 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:32px 0; width:100%; max-width:100%; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <!-- Header -->
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">실시간 견적 모의계산</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">🚗 {clean_kw} 연간 보험료 절감 & 특약 할인 시뮬레이터</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">오프라인 설계사 대비 다이렉트 전환 + 마일리지/안전운전 특약 적용 시 연간 절감액을 산출합니다.</p>
        </div>
      </div>

      <!-- Quick Presets -->
      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">차량 차급별 기본 견적:</span>
        <button type="button" onclick="setAutoInsurancePreset(650000, 35)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">준중형/경차 (연 65만 기준)</button>
        <button type="button" onclick="setAutoInsurancePreset(950000, 35)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">표준 중형차 (연 95만 기준)</button>
        <button type="button" onclick="setAutoInsurancePreset(1350000, 35)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">대형 / SUV (연 135만 기준)</button>
      </div>

      <!-- Input Controls Grid: 2-Column Balanced Grid -->
      <div class="b365-calc-input-grid" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; margin-bottom:22px;">
        <!-- Control 1: Current Premium -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-auto-premium" style="font-size:0.88rem; font-weight:700; color:#475569;">오프라인/현재 연간 보험료</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-auto-premium">950,000원</span>
          </div>
          <input type="range" id="slider-auto-premium" min="300000" max="2500000" step="10000" value="950000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcAutoInsurance()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>300,000원</span>
            <span>2,500,000원</span>
          </div>
        </div>

        <!-- Control 2: Discount Rate -->
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-auto-discount" style="font-size:0.88rem; font-weight:700; color:#475569;">다이렉트 + 특약 할인 합산율</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-auto-discount">35%</span>
          </div>
          <input type="range" id="slider-auto-discount" min="10" max="50" step="1" value="35" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcAutoInsurance()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>10% (다이렉트 기본)</span>
            <span>50% (마일리지+티맵 최대)</span>
          </div>
        </div>
      </div>

      <!-- Result Hero Card -->
      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">연간 총 순수 절감 예상액</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-auto-ratio">절감율 35.0%</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-auto-saved">332,500원 절약</div>
        
        <!-- Omni Visual Breakdown Bar -->
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span>최종 예상 납부액 (<span id="txt-bar-auto-pay">617,500원</span>)</span>
            <span style="color:#34d399; font-weight:700;">아낀 순수 절감액 (<span id="txt-bar-auto-save">332,500원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-auto-pay" style="background:#3b82f6; width:65%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-auto-save" style="background:#10b981; width:35%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-auto-monthly">월 약 27,700원 고정비 세이브 효과 (다이렉트 15.6% 기본할인 + 주행거리 마일리지 환급 기준)</div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-auto" onclick="copyToolVal('result-auto-saved', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">절감 결과 복사하기</button>
        <button type="button" onclick="resetAutoInsurance()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <!-- Real-Time CTA / CSE Dynamic Button -->
      <a href="#article-search-nav" id="btn-calc-cta-auto" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 다이렉트 최저가 견적 조회하기</a>
    </div>

    <script>
    function calcAutoInsurance() {{
      const premium = parseInt(document.getElementById('slider-auto-premium').value);
      const discountRate = parseInt(document.getElementById('slider-auto-discount').value);
      const saved = Math.round(premium * (discountRate / 100));
      const finalPay = premium - saved;
      const monthly = Math.round(saved / 12);

      document.getElementById('disp-auto-premium').innerText = premium.toLocaleString() + '원';
      document.getElementById('disp-auto-discount').innerText = discountRate + '%';

      document.getElementById('result-auto-saved').innerText = saved.toLocaleString() + '원 절약';
      document.getElementById('badge-auto-ratio').innerText = '절감율 ' + discountRate + '%';
      document.getElementById('txt-bar-auto-pay').innerText = finalPay.toLocaleString() + '원';
      document.getElementById('txt-bar-auto-save').innerText = saved.toLocaleString() + '원';

      const payPercent = 100 - discountRate;
      document.getElementById('bar-auto-pay').style.width = payPercent + '%';
      document.getElementById('bar-auto-save').style.width = discountRate + '%';

      document.getElementById('desc-auto-monthly').innerText = '월 약 ' + monthly.toLocaleString() + '원 고정비 세이브 효과 (다이렉트 기본할인 + 주행거리 마일리지 환급 기준)';

      const ctaBtn = document.getElementById('btn-calc-cta-auto');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 연 ' + saved.toLocaleString() + '원 절감 다이렉트 견적 바로 조회하기';
      }}
    }}
    function setAutoInsurancePreset(prem, disc) {{
      document.getElementById('slider-auto-premium').value = prem;
      document.getElementById('slider-auto-discount').value = disc;
      calcAutoInsurance();
    }}
    function resetAutoInsurance() {{
      setAutoInsurancePreset(950000, 35);
    }}
    </script>
    """


def _render_general_savings_calc(clean_kw: str) -> str:
    """고정비 및 생활비 절감 시뮬레이터 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:3px 10px; border-radius:9999px; font-weight:800; letter-spacing:0.02em;">OMNI SIMULATOR</span>
            <span style="font-size:0.75rem; background:#ecfdf5; color:#10b981; padding:3px 10px; border-radius:9999px; font-weight:800;">실시간 모의계산</span>
          </div>
          <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">💰 {clean_kw} 연간 고정비 절감 시뮬레이터</h3>
          <p style="margin:0; font-size:0.88rem; color:#64748b; line-height:1.5;">매월 고정 지출 항목 최적화 시 12개월간 축적되는 순수 목돈을 산출합니다.</p>
        </div>
      </div>

      <div style="margin-bottom:20px; padding:12px 16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">지출 규모 프리셋:</span>
        <button type="button" onclick="setGeneralSavingsPreset(300000, 20)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">소액 지출 (월 30만)</button>
        <button type="button" onclick="setGeneralSavingsPreset(600000, 25)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">표준 가구 (월 60만)</button>
        <button type="button" onclick="setGeneralSavingsPreset(1200000, 30)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">다인 가구 (월 120만)</button>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-gen-spend" style="font-size:0.88rem; font-weight:700; color:#475569;">현재 월 고정 지출액</label>
            <span style="font-size:1.05rem; font-weight:800; color:#0f172a;" id="disp-gen-spend">600,000원</span>
          </div>
          <input type="range" id="slider-gen-spend" min="100000" max="2000000" step="10000" value="600000" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcGeneralSavings()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>100,000원</span>
            <span>2,000,000원</span>
          </div>
        </div>

        <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <label for="slider-gen-ratio" style="font-size:0.88rem; font-weight:700; color:#475569;">목표 절감율</label>
            <span style="font-size:1.05rem; font-weight:800; color:#2563eb;" id="disp-gen-ratio">25%</span>
          </div>
          <input type="range" id="slider-gen-ratio" min="5" max="50" step="1" value="25" style="width:100%; accent-color:#2563eb; cursor:pointer;" oninput="calcGeneralSavings()" />
          <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#94a3b8; margin-top:4px;">
            <span>5%</span>
            <span>50%</span>
          </div>
        </div>
      </div>

      <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px; box-shadow:0 8px 24px -4px rgba(15,23,42,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">12개월간 총 순수 절감 예상액</span>
          <span style="font-size:0.75rem; background:#1e293b; color:#38bdf8; padding:3px 8px; border-radius:6px; font-weight:700;" id="badge-gen-ratio">절감율 25.0%</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#38bdf8; letter-spacing:-0.02em; margin:6px 0;" id="result-gen-saved">1,800,000원 절약</div>
        
        <div style="margin:16px 0 10px 0;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
            <span>최적화 후 지출 (<span id="txt-bar-gen-pay">5,400,000원</span>)</span>
            <span style="color:#34d399; font-weight:700;">아낀 순수 목돈 (<span id="txt-bar-gen-save">1,800,000원</span>)</span>
          </div>
          <div style="background:#334155; height:12px; border-radius:6px; overflow:hidden; display:flex; width:100%;">
            <div id="bar-gen-pay" style="background:#3b82f6; width:75%; height:100%; transition:width 0.2s ease;"></div>
            <div id="bar-gen-save" style="background:#10b981; width:25%; height:100%; transition:width 0.2s ease;"></div>
          </div>
        </div>

        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;" id="desc-gen-monthly">월 150,000원 순수 고정비 절감 효과</div>
      </div>

      <div style="display:flex; gap:10px;">
        <button type="button" id="btn-copy-gen" onclick="copyToolVal('result-gen-saved', this)" style="flex:1; padding:13px 20px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-size:0.92rem; font-weight:800; cursor:pointer; transition:background 0.15s ease;">결과 복사하기</button>
        <button type="button" onclick="resetGeneralSavings()" style="padding:13px 22px; background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; border-radius:10px; font-size:0.92rem; font-weight:700; cursor:pointer;">공식 기준 초기화</button>
      </div>

      <a href="#article-search-nav" id="btn-calc-cta-gen" class="calc-dynamic-cta-btn" style="display:block; width:100%; margin-top:14px; padding:15px 20px; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:#ffffff; font-weight:800; font-size:1rem; text-align:center; text-decoration:none; border-radius:12px; box-shadow:0 4px 14px rgba(37,99,235,0.25); box-sizing:border-box; transition:transform 0.15s ease;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='translateY(0)'">👉 계산된 절약 혜택 바로 조회하기</a>
    </div>

    <script>
    function calcGeneralSavings() {{
      const spend = parseInt(document.getElementById('slider-gen-spend').value);
      const ratio = parseInt(document.getElementById('slider-gen-ratio').value);
      const monthlySaved = Math.round(spend * (ratio / 100));
      const yearlySaved = monthlySaved * 12;
      const yearlySpend = (spend - monthlySaved) * 12;

      document.getElementById('disp-gen-spend').innerText = spend.toLocaleString() + '원';
      document.getElementById('disp-gen-ratio').innerText = ratio + '%';

      document.getElementById('result-gen-saved').innerText = yearlySaved.toLocaleString() + '원 절약';
      document.getElementById('badge-gen-ratio').innerText = '절감율 ' + ratio + '%';
      document.getElementById('txt-bar-gen-pay').innerText = yearlySpend.toLocaleString() + '원';
      document.getElementById('txt-bar-gen-save').innerText = yearlySaved.toLocaleString() + '원';

      const payPercent = 100 - ratio;
      document.getElementById('bar-gen-pay').style.width = payPercent + '%';
      document.getElementById('bar-gen-save').style.width = ratio + '%';

      document.getElementById('desc-gen-monthly').innerText = '월 ' + monthlySaved.toLocaleString() + '원 순수 고정비 절감 효과';

      const ctaBtn = document.getElementById('btn-calc-cta-gen');
      if (ctaBtn) {{
        ctaBtn.innerText = '👉 연 ' + yearlySaved.toLocaleString() + '원 절약 플랜 바로 조회하기';
      }}
    }}
    function setGeneralSavingsPreset(sp, r) {{
      document.getElementById('slider-gen-spend').value = sp;
      document.getElementById('slider-gen-ratio').value = r;
      calcGeneralSavings();
    }}
    function resetGeneralSavings() {{
      setGeneralSavingsPreset(600000, 25);
    }}
    </script>
    """


def get_calculator_by_category(category_code: str, keyword: str = "") -> str:
    """
    5대 황금 니치에 맞춤화된 고체류 인터랙티브 Micro-SaaS Omni Calculator를 반환합니다.
    도메인 라우터를 기반으로 100% 안전하게 도메인별 계산기를 라우팅합니다.
    """
    clean_kw = _clean_keyword(keyword)
    cat = (category_code or "TECH").upper()
    domain = classify_domain(clean_kw, cat)

    # 1. AUTO INSURANCE ONLY
    if domain == DOMAIN_AUTO_INSURANCE:
        return _render_auto_insurance_calc(clean_kw)

    # 2. HAIR TRANSPLANT & HAIR RESTORATION (Dedicated Micro-SaaS)
    if domain == DOMAIN_HAIR_TRANSPLANT or cat in ["HAIR", "HAIR_TRANSPLANT"]:
        return _render_hair_transplant_calc(clean_kw)

    # 3. MEDICAL / PROCEDURES / DENTAL
    if domain == DOMAIN_MEDICAL:
        procedure_keywords = ["임플란트", "라식", "라섹", "스마일라식", "치과", "치아", "보철", "성형", "백내장", "견적"]
        if any(k in clean_kw.lower() for k in procedure_keywords):
            return render_cost_spec_comparison_table(clean_kw, cat)
        return _render_medical_calc(clean_kw)

    # 3. HEALTH / INDEMNITY INSURANCE
    if domain == DOMAIN_HEALTH_INSURANCE:
        return _render_medical_calc(clean_kw)

    # 4. SUBSIDY / GOVERNMENT
    if domain == DOMAIN_SUBSIDY:
        return _render_subsidy_calc(clean_kw)

    # 5. EXPLICIT TELECOM
    if domain == DOMAIN_TELECOM:
        return _render_savings_calc(clean_kw)

    # 6. CARDS / TRAVEL / FOREIGN EXCHANGE
    if domain == DOMAIN_CARDS_TRAVEL:
        return _render_general_savings_calc(clean_kw)

    # 7. CAREER / EDUCATION
    if domain == DOMAIN_CAREER:
        return _render_career_calc(clean_kw)

    # 8. SAVINGS / CASHFLOW (General fixed costs)
    if domain == DOMAIN_SAVINGS:
        return _render_general_savings_calc(clean_kw)

    # 9. DEFAULT TECH
    return _render_tech_calc(clean_kw)


def render_saas_calculator(category_code: str = "TECH", keyword: str = "") -> str:
    """하위 호환성을 유지하며 최신 Omni Calculator 마이크로 SaaS HTML/JS를 생성합니다."""
    return get_calculator_by_category(category_code, keyword)


if __name__ == "__main__":
    for cat in ["SAVINGS", "SUBSIDY", "TECH", "MEDICAL", "CAREER"]:
        html = render_saas_calculator(cat, f"2026 {cat} 테스트")
        print(f"[{cat}] Calculator Generated: {len(html)} chars | Has JS: {'<script>' in html} | Has Breakdown Bar: {'bar-' in html}")
    # Test procedure dynamic switching
    implant_html = render_saas_calculator("MEDICAL", "임플란트 비용 비교")
    assert "cost-comparison-table" in implant_html
    assert "라식/라섹" not in implant_html
    assert "스마일라식" not in implant_html
    print("[IMPLANT] Dynamic cost table switched successfully without fake presets!")
