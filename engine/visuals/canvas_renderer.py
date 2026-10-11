def generate_spec_comparison_svg(item_a: str, item_b: str, score_a: int, score_b: int, metric_name: str) -> str:
    """
    [Canvas Design ⭐17.9만 오픈소스 이식]
    Blogger 및 모든 브라우저에서 절대 축소/붕괴되지 않는 반응형 Pure HTML/CSS 벤치마크 바 차트.
    """
    score_a = max(10, min(100, score_a))
    score_b = max(10, min(100, score_b))
    
    return f"""
    <div class="editorial-visual-card" style="margin:28px 0; padding:22px; background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; box-shadow:0 4px 16px -2px rgba(15,23,42,0.05); box-sizing:border-box;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <span style="font-size:12px; font-weight:700; color:#2563eb; letter-spacing:0.04em; text-transform:uppercase;">SPEC COMPARISON MATRIX</span>
        <span style="font-size:11px; background:#eff6ff; color:#1d4ed8; padding:3px 10px; border-radius:9999px; font-weight:700;">실시간 벤치마크</span>
      </div>
      <h4 style="margin:0 0 18px 0; font-size:16px; font-weight:800; color:#0f172a; letter-spacing:-0.01em;">📊 {metric_name} 실사용 지표 비교</h4>
      
      <div style="display:flex; flex-direction:column; gap:16px;">
        <!-- Row 1: Item A -->
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-size:13px; font-weight:700;">
            <span style="color:#0f172a;">{item_a}</span>
            <span style="color:#2563eb; font-weight:800;">{score_a}점 (우수)</span>
          </div>
          <div style="background:#f1f5f9; height:18px; border-radius:9px; overflow:hidden; width:100%; box-sizing:border-box;">
            <div style="background:linear-gradient(90deg, #3b82f6, #2563eb); width:{score_a}%; height:100%; border-radius:9px;"></div>
          </div>
        </div>

        <!-- Row 2: Item B -->
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-size:13px; font-weight:700;">
            <span style="color:#64748b;">{item_b}</span>
            <span style="color:#64748b; font-weight:800;">{score_b}점 (기준)</span>
          </div>
          <div style="background:#f1f5f9; height:18px; border-radius:9px; overflow:hidden; width:100%; box-sizing:border-box;">
            <div style="background:#94a3b8; width:{score_b}%; height:100%; border-radius:9px;"></div>
          </div>
        </div>
      </div>
    </div>
    """

def generate_process_stepper_svg(steps: list) -> str:
    """
    3단계 신청 및 절차 인포그래픽을 인라인 SVG로 생성합니다.
    """
    cards_html = ""
    for i, step in enumerate(steps, 1):
        cards_html += f"""
        <div style="flex:1; min-width:180px; padding:16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;">
          <div style="font-size:0.75rem; font-weight:800; color:#2563eb; margin-bottom:4px;">STEP 0{i}</div>
          <div style="font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:4px;">{step.get('title', '')}</div>
          <div style="font-size:0.8rem; color:#64748b; line-height:1.4;">{step.get('desc', '')}</div>
        </div>
        """
        
    return f"""
    <div class="editorial-process-flow" style="margin:32px auto; max-width:760px; box-sizing:border-box;">
      <h4 style="margin:0 0 14px 0; font-size:1.1rem; font-weight:800; color:#0f172a;">⚡ 3분 안에 끝나는 단계별 핵심 절차</h4>
      <div style="display:flex; flex-wrap:wrap; gap:12px;">
        {cards_html}
      </div>
    </div>
    """

def render_spec_comparison_chart(keyword: str, category: str = "TECH") -> str:
    clean_kw = keyword.replace(" 비교", "").replace(" 추천", "").strip()
    return generate_spec_comparison_svg(clean_kw, "경쟁 표준 모델", 94, 78, f"{clean_kw} 종합 벤치마크")

def render_process_stepper(steps: list = None) -> str:
    if not steps:
        steps = [
            {"title": "자격 및 스펙 확인", "desc": "공식 기준 대조 및 적합성 점검"},
            {"title": "모의 시뮬레이션", "desc": "절감액 및 혜택 수치 계산"},
            {"title": "공식 접수 및 혜택 수령", "desc": "전용 링크를 통한 온라인 즉시 완료"}
        ]
    return generate_process_stepper_svg(steps)

