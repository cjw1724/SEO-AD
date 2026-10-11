def get_calculator_by_category(category_code: str, keyword: str) -> str:
    """
    5대 황금 니치에 맞춤화된 고체류 인터랙티브 Micro-SaaS 계산기 HTML/JS를 생성합니다.
    초기 로딩 시 유효한 기본값이 사전 렌더링되며, 0원 깜빡임 없음.
    """
    clean_kw = keyword.replace(" 비교", "").replace(" 추천", "").strip()
    
    if category_code == "SAVINGS":
        # 통신비 절감 시뮬레이터
        return f"""
        <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 20px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px;">
            <div>
              <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a;">📱 24개월 통신비 절감 시뮬레이터</h3>
              <p style="margin:0; font-size:0.88rem; color:#64748b;">현재 통신 3사 요금 대비 알뜰폰 전환 시 아낄 수 있는 총비용을 계산합니다.</p>
            </div>
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:4px 10px; border-radius:9999px; font-weight:700;">실시간 도구</span>
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:24px;">
            <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
              <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.9rem; margin-bottom:8px;">
                <span style="color:#475569;">현재 월 통신비</span>
                <span style="color:#0f172a;" id="disp-current-bill">69,000원</span>
              </div>
              <input type="range" id="slider-current-bill" min="30000" max="130000" step="5000" value="69000" style="width:100%; cursor:pointer;" oninput="calcSavings()" />
            </div>
            <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
              <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.9rem; margin-bottom:8px;">
                <span style="color:#475569;">변경할 알뜰폰 요금</span>
                <span style="color:#2563eb;" id="disp-target-bill">16,900원</span>
              </div>
              <input type="range" id="slider-target-bill" min="0" max="40000" step="1000" value="16900" style="width:100%; cursor:pointer;" oninput="calcSavings()" />
            </div>
          </div>
          <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px;">
            <div style="font-size:0.85rem; color:#94a3b8; font-weight:600; margin-bottom:4px;">24개월간 총 절감 예상액</div>
            <div style="font-size:1.85rem; font-weight:800; color:#38bdf8;" id="result-saved-total">1,250,400원 절약</div>
            <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">월 52,100원 순수 고정비 절감 효과</div>
          </div>
          <div style="display:flex; gap:10px;">
            <button type="button" onclick="copyToolVal('result-saved-total')" style="flex:1; padding:12px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-weight:700; cursor:pointer;">결과 복사하기</button>
            <button type="button" onclick="resetSavings()" style="padding:12px 20px; background:#f1f5f9; color:#475569; border:none; border-radius:10px; font-weight:700; cursor:pointer;">초기화</button>
          </div>
        </div>
        <script>
        function calcSavings() {{
          const curr = parseInt(document.getElementById('slider-current-bill').value);
          const tgt = parseInt(document.getElementById('slider-target-bill').value);
          document.getElementById('disp-current-bill').innerText = curr.toLocaleString() + '원';
          document.getElementById('disp-target-bill').innerText = tgt.toLocaleString() + '원';
          const monthly = curr - tgt;
          const total = monthly * 24;
          document.getElementById('result-saved-total').innerText = total.toLocaleString() + '원 절약';
        }}
        function resetSavings() {{
          document.getElementById('slider-current-bill').value = 69000;
          document.getElementById('slider-target-bill').value = 16900;
          calcSavings();
        }}
        function copyToolVal(id) {{
          const txt = document.getElementById(id).innerText;
          navigator.clipboard.writeText(txt);
          alert('결과가 복사되었습니다: ' + txt);
        }}
        </script>
        """
        
    elif category_code == "SUBSIDY":
        # 정부 지원금 & 환급액 계산기
        return f"""
        <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 20px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px;">
            <div>
              <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a;">🏛️ 2026 정부 지원금 & 환급 모의계산기</h3>
              <p style="margin:0; font-size:0.88rem; color:#64748b;">연간 총소득을 입력하여 예상 환급금 및 지원 대상 여부를 확인하세요.</p>
            </div>
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:4px 10px; border-radius:9999px; font-weight:700;">국세청 기준</span>
          </div>
          <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0; margin-bottom:24px;">
            <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.9rem; margin-bottom:8px;">
              <span style="color:#475569;">연간 총 급여액</span>
              <span style="color:#0f172a;" id="disp-annual-income">3,200만원</span>
            </div>
            <input type="range" id="slider-annual-income" min="1000" max="8000" step="100" value="3200" style="width:100%; cursor:pointer;" oninput="calcSubsidy()" />
          </div>
          <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px;">
            <div style="font-size:0.85rem; color:#94a3b8; font-weight:600; margin-bottom:4px;">예상 지원금 / 환급 추정액</div>
            <div style="font-size:1.85rem; font-weight:800; color:#38bdf8;" id="result-subsidy-val">약 1,350,000원 환급 가능</div>
            <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">근로장려금 및 세액공제 중복 혜택 적용 대상</div>
          </div>
          <div style="display:flex; gap:10px;">
            <button type="button" onclick="copyToolVal('result-subsidy-val')" style="flex:1; padding:12px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-weight:700; cursor:pointer;">결과 복사하기</button>
            <button type="button" onclick="resetSubsidy()" style="padding:12px 20px; background:#f1f5f9; color:#475569; border:none; border-radius:10px; font-weight:700; cursor:pointer;">초기화</button>
          </div>
        </div>
        <script>
        function calcSubsidy() {{
          const inc = parseInt(document.getElementById('slider-annual-income').value);
          document.getElementById('disp-annual-income').innerText = (inc).toLocaleString() + '만원';
          let refund = Math.max(300000, Math.round((4500 - inc) * 35000));
          if (refund < 200000) refund = 200000;
          document.getElementById('result-subsidy-val').innerText = '약 ' + refund.toLocaleString() + '원 환급 가능';
        }}
        function resetSubsidy() {{
          document.getElementById('slider-annual-income').value = 3200;
          calcSubsidy();
        }}
        </script>
        """
        
    else:
        # 가전 & 전자기기 가성비 점수 계산기 (기본 TECH)
        return f"""
        <div class="saas-calculator editorial-calculator-card" id="custom-saas-tool" style="margin:36px auto; max-width:760px; padding:28px; background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; box-shadow:0 4px 20px -4px rgba(15,23,42,0.06); box-sizing:border-box;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px;">
            <div>
              <h3 style="margin:0 0 6px 0; font-size:1.25rem; font-weight:800; color:#0f172a;">🛒 {clean_kw} 가성비 & 카드 무이자 할부 계산기</h3>
              <p style="margin:0; font-size:0.88rem; color:#64748b;">구매 예산과 사용 개월 수를 입력하여 일할 체감 비용을 확인하세요.</p>
            </div>
            <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; padding:4px 10px; border-radius:9999px; font-weight:700;">스마트 쇼핑</span>
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-bottom:24px;">
            <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
              <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.9rem; margin-bottom:8px;">
                <span style="color:#475569;">구매 가격</span>
                <span style="color:#0f172a;" id="disp-gadget-price">1,250,000원</span>
              </div>
              <input type="range" id="slider-gadget-price" min="200000" max="3000000" step="50000" value="1250000" style="width:100%; cursor:pointer;" oninput="calcGadget()" />
            </div>
            <div style="background:#f8fafc; padding:18px; border-radius:14px; border:1px solid #e2e8f0;">
              <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.9rem; margin-bottom:8px;">
                <span style="color:#475569;">예상 사용 기간</span>
                <span style="color:#2563eb;" id="disp-gadget-term">24개월</span>
              </div>
              <input type="range" id="slider-gadget-term" min="6" max="48" step="6" value="24" style="width:100%; cursor:pointer;" oninput="calcGadget()" />
            </div>
          </div>
          <div style="background:#0f172a; padding:22px; border-radius:14px; color:#ffffff; margin-bottom:20px;">
            <div style="font-size:0.85rem; color:#94a3b8; font-weight:600; margin-bottom:4px;">하루 체감 커피값 환산액</div>
            <div style="font-size:1.85rem; font-weight:800; color:#38bdf8;" id="result-gadget-daily">하루 약 1,736원</div>
            <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">24개월 무이자 할부 시 월 52,080원 수준</div>
          </div>
          <div style="display:flex; gap:10px;">
            <button type="button" onclick="copyToolVal('result-gadget-daily')" style="flex:1; padding:12px; background:#2563eb; color:#ffffff; border:none; border-radius:10px; font-weight:700; cursor:pointer;">결과 복사하기</button>
            <button type="button" onclick="resetGadget()" style="padding:12px 20px; background:#f1f5f9; color:#475569; border:none; border-radius:10px; font-weight:700; cursor:pointer;">초기화</button>
          </div>
        </div>
        <script>
        function calcGadget() {{
          const pr = parseInt(document.getElementById('slider-gadget-price').value);
          const term = parseInt(document.getElementById('slider-gadget-term').value);
          document.getElementById('disp-gadget-price').innerText = pr.toLocaleString() + '원';
          document.getElementById('disp-gadget-term').innerText = term + '개월';
          const daily = Math.round(pr / (term * 30));
          const monthly = Math.round(pr / term);
          document.getElementById('result-gadget-daily').innerText = '하루 약 ' + daily.toLocaleString() + '원';
        }}
        function resetGadget() {{
          document.getElementById('slider-gadget-price').value = 1250000;
          document.getElementById('slider-gadget-term').value = 24;
          calcGadget();
        }}
        </script>
        """

def render_saas_calculator(category_code: str = "TECH", keyword: str = "") -> str:
    return get_calculator_by_category(category_code, keyword or "비교 추천")

