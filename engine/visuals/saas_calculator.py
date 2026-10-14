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
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
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

      <!-- Input Controls Grid -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
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
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
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

      <!-- Input Controls Grid -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
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
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
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

      <!-- Input Controls Grid -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
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
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
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
        <span style="font-size:0.78rem; font-weight:700; color:#475569; margin-right:8px;">항목별 평균 견적:</span>
        <button type="button" onclick="setMedicalPreset(1800000, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">라식/라섹 (180만)</button>
        <button type="button" onclick="setMedicalPreset(2600000, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">스마일라식 (260만)</button>
        <button type="button" onclick="setMedicalPreset(1300000, 70)" style="padding:4px 10px; font-size:0.75rem; font-weight:700; background:#ffffff; color:#334155; border:1px solid #cbd5e1; border-radius:6px; cursor:pointer; margin:2px;">임플란트 1대 (130만)</button>
      </div>

      <!-- Input Controls Grid -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
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
      setMedicalPreset(2400000, 70);
    }}
    </script>
    """


def _render_career_calc(clean_kw: str) -> str:
    """직장인 국비지원(내일배움카드) 실부담금 & 연봉 ROI 계산기 (Omni Benchmark)"""
    return f"""
    <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 24px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
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

      <!-- Input Controls Grid -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:22px;">
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


def get_calculator_by_category(category_code: str, keyword: str = "") -> str:
    """
    5대 황금 니치에 맞춤화된 고체류 인터랙티브 Micro-SaaS Omni Calculator를 반환합니다.
    - SAVINGS: 알뜰폰/통신비 절감
    - SUBSIDY: 정부지원금/환급/청년도약계좌
    - TECH: 스마트 가전/테크 일할 커피값 계산기
    - MEDICAL: 비급여 의료/실손보험 환급 계산기
    - CAREER: 국비지원/내일배움카드 ROI 계산기
    """
    clean_kw = _clean_keyword(keyword)
    cat = (category_code or "TECH").upper()

    if cat in ["SAVINGS", "CASHFLOW"]:
        return _render_savings_calc(clean_kw)
    elif cat in ["SUBSIDY", "REFUND", "GOVERNMENT"]:
        return _render_subsidy_calc(clean_kw)
    elif cat in ["MEDICAL", "WELLNESS", "CLINIC"]:
        return _render_medical_calc(clean_kw)
    elif cat in ["CAREER", "EDUCATION", "CERT"]:
        return _render_career_calc(clean_kw)
    else:
        # Default TECH
        return _render_tech_calc(clean_kw)


def render_saas_calculator(category_code: str = "TECH", keyword: str = "") -> str:
    """하위 호환성을 유지하며 최신 Omni Calculator 마이크로 SaaS HTML/JS를 생성합니다."""
    return get_calculator_by_category(category_code, keyword)


if __name__ == "__main__":
    for cat in ["SAVINGS", "SUBSIDY", "TECH", "MEDICAL", "CAREER"]:
        html = render_saas_calculator(cat, f"2026 {cat} 테스트")
        print(f"[{cat}] Calculator Generated: {len(html)} chars | Has JS: {'<script>' in html} | Has Breakdown Bar: {'bar-' in html}")
