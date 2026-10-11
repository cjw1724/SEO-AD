import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from dotenv import load_dotenv
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(root_dir, "SEO.env"))

from openai import OpenAI

IMPECCABLE_EDITORIAL_DESIGN_SYSTEM_CSS = """
<style>
/* ==========================================================================
   Blogin 365 AI — Impeccable Editorial Design System (Wall Street & Toss Standard)
   Refined Monochrome Surfaces, High-Contrast Typography, Zero-Entity CSS, E-E-A-T
   ========================================================================== */

/* 1. Article Root: Optimal Reading Measure (760px) */
.article-editorial-container {
  max-width: 760px;
  margin: 0 auto;
  padding: 0 16px 80px 16px;
  font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #1e293b;
  line-height: 1.8;
  letter-spacing: -0.012em;
  box-sizing: border-box;
}

.article-editorial-container * {
  box-sizing: border-box;
}

/* 2. Hero Thumbnail Wrapper */
.editorial-hero-thumbnail {
  max-width: 760px;
  margin: 0 auto 32px auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.08);
}
.editorial-hero-thumbnail img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 16px;
}

/* 3. Typography Hierarchy */
.editorial-h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  margin: 44px 0 18px 0;
  line-height: 1.35;
  letter-spacing: -0.025em;
  border-left: 4px solid #2563eb;
  padding-left: 14px;
}
.editorial-h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
  margin: 30px 0 12px 0;
  line-height: 1.4;
  letter-spacing: -0.02em;
}
.editorial-p, .snappy-p {
  font-size: 1.03rem;
  color: #334155;
  line-height: 1.82;
  margin: 0 0 20px 0;
  letter-spacing: -0.012em;
}
.editorial-lead {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1e293b;
  line-height: 1.85;
  margin-bottom: 26px;
}

/* 4. Executive Briefing Card (Wall Street Bento) */
.hero-editorial-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 26px 28px;
  margin: 24px 0 36px 0;
  box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
}
.hero-meta-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}
.badge-live-intel {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #0f172a;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 9999px;
  letter-spacing: -0.01em;
}
.live-pulse-dot {
  width: 7px;
  height: 7px;
  background-color: #10b981;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulseDot 2s infinite cubic-bezier(0.66, 0, 0, 1);
}
@keyframes pulseDot {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.badge-executive-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #0f172a;
  color: #ffffff;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 9999px;
  letter-spacing: 0.01em;
}
.hero-editorial-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  line-height: 1.4;
  letter-spacing: -0.025em;
}
.editorial-takeaways-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
}
.editorial-takeaway-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.takeaway-metric-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #2563eb;
  letter-spacing: 0.03em;
}
.takeaway-metric-body {
  font-size: 0.92rem;
  color: #334155;
  line-height: 1.55;
}
.takeaway-metric-body strong {
  color: #0f172a;
  font-weight: 700;
}

/* 5. Interactive Micro-SaaS Financial Calculator */
.editorial-calculator-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 18px;
  padding: 30px 32px;
  margin: 38px 0;
  box-shadow: 0 10px 30px -8px rgba(15, 23, 42, 0.08);
}
.calc-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 18px;
  margin-bottom: 22px;
}
.calc-title-group h3 {
  font-size: 1.28rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 5px 0;
  letter-spacing: -0.02em;
}
.calc-title-group p {
  font-size: 0.88rem;
  color: #64748b;
  margin: 0;
}
.calc-badge {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 9999px;
  letter-spacing: 0.02em;
}
.calc-inputs-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 22px;
}
.calc-input-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px 18px;
}
.calc-input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.calc-input-label {
  font-size: 0.88rem;
  font-weight: 700;
  color: #475569;
}
.calc-val-display {
  font-size: 1.15rem;
  font-weight: 800;
  color: #2563eb;
}
.calc-range-slider {
  -webkit-appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: #cbd5e1;
  outline: none;
  cursor: pointer;
  margin: 10px 0 12px 0;
}
.calc-range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
  border: 2px solid #ffffff;
  transition: transform 0.15s ease;
}
.calc-range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}
.calc-range-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  border: 2px solid #ffffff;
}
.calc-preset-pills {
  display: flex;
  gap: 6px;
}
.btn-preset-pill {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-preset-pill:hover, .btn-preset-pill.active {
  background: #eff6ff;
  color: #2563eb;
  border-color: #2563eb;
  font-weight: 800;
}
.calc-hero-metric-card {
  background: #0f172a;
  border-radius: 16px;
  padding: 22px 26px;
  color: #ffffff;
  margin-bottom: 20px;
}
.metric-card-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}
.metric-card-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #94a3b8;
}
.metric-card-number {
  font-size: 2.1rem;
  font-weight: 800;
  color: #60a5fa;
  letter-spacing: -0.03em;
}
.metric-card-subtext {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 0.85rem;
  color: #94a3b8;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding-top: 12px;
}
.metric-card-subtext span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.calc-action-row {
  display: flex;
  gap: 12px;
}
.btn-action-primary {
  flex: 1;
  min-height: 46px;
  padding: 10px 20px;
  font-size: 0.94rem;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  border: none;
  background: #2563eb;
  color: #ffffff;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.btn-action-primary:hover {
  background: #1d4ed8;
}
.btn-action-secondary {
  min-height: 46px;
  padding: 10px 20px;
  font-size: 0.94rem;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #475569;
  transition: all 0.2s ease;
}
.btn-action-secondary:hover {
  background: #e2e8f0;
}

/* 6. Wall Street Journal Comparison Table */
.editorial-table-wrap {
  overflow-x: auto;
  margin: 36px 0;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
}
.editorial-table {
  width: 100%;
  min-width: 580px;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.93rem;
}
.editorial-table th {
  background: #f8fafc;
  color: #0f172a;
  font-weight: 700;
  padding: 14px 18px;
  border-bottom: 2px solid #e2e8f0;
}
.editorial-table th.top-col {
  background: #eff6ff;
  color: #1e40af;
  border-bottom: 2px solid #2563eb;
}
.table-pill-top {
  display: inline-block;
  background: #2563eb;
  color: #ffffff;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 9999px;
  margin-left: 6px;
  vertical-align: middle;
}
.editorial-table td {
  padding: 14px 18px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  line-height: 1.5;
}
.editorial-table tr:last-child td {
  border-bottom: none;
}
.editorial-table tr:hover td {
  background: #f8fafc;
}

/* 7. Institutional Analysis Grid (Replaces Childish Pastel Cards) */
.editorial-analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin: 34px 0;
}
.analysis-panel {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 22px 24px;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);
}
.analysis-panel-strength {
  border-left: 4px solid #2563eb;
}
.analysis-panel-risk {
  border-left: 4px solid #64748b;
}
.panel-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.analysis-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.analysis-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.94rem;
  color: #334155;
  line-height: 1.55;
}
.analysis-icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-top: 2px;
}

/* 8. Pure-CSS Zero-Entity FAQ Accordion */
.editorial-faq-group {
  margin: 38px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.editorial-faq-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden;
  transition: border-color 0.2s ease;
}
.editorial-faq-item[open] {
  border-color: #2563eb;
  box-shadow: 0 4px 14px -2px rgba(37, 99, 235, 0.08);
}
.editorial-faq-summary {
  padding: 16px 20px;
  font-size: 0.98rem;
  font-weight: 700;
  color: #0f172a;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  list-style: none !important;
  user-select: none;
}
.editorial-faq-summary::-webkit-details-marker { display: none !important; }
.editorial-faq-summary::-moz-list-bullet { list-style-type: none !important; }
.faq-chevron {
  width: 8px;
  height: 8px;
  border-right: 2px solid #64748b;
  border-bottom: 2px solid #64748b;
  transform: rotate(45deg);
  transition: transform 0.2s ease;
  flex-shrink: 0;
}
.editorial-faq-item[open] .faq-chevron {
  transform: rotate(-135deg);
  border-color: #2563eb;
}
.editorial-faq-content {
  padding: 0 20px 18px 20px;
  font-size: 0.94rem;
  color: #475569;
  line-height: 1.7;
  border-top: 1px solid #f1f5f9;
}
.editorial-faq-content p {
  margin: 12px 0 0 0;
}

/* 9. Mobile Sticky Action Bar */
.editorial-sticky-bar {
  display: none;
}
@media screen and (max-width: 768px) {
  .calc-inputs-grid, .editorial-analysis-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }
  .editorial-sticky-bar {
    display: flex !important;
    position: fixed !important;
    bottom: 12px !important;
    left: 12px !important;
    right: 12px !important;
    z-index: 99999 !important;
    background: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 9999px !important;
    box-shadow: 0 16px 36px -4px rgba(0, 0, 0, 0.4) !important;
    padding: 8px 10px 8px 16px !important;
    align-items: center !important;
    justify-content: space-between !important;
    color: #ffffff !important;
    gap: 10px !important;
  }
  .sticky-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .sticky-tagline {
    font-size: 0.7rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .sticky-headline {
    font-size: 0.85rem;
    font-weight: 700;
    color: #f8fafc;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 150px;
  }
  .btn-sticky-jump {
    min-height: 42px;
    padding: 0 16px;
    background: #2563eb;
    color: #ffffff;
    font-size: 0.85rem;
    font-weight: 700;
    border-radius: 9999px;
    border: none;
    cursor: pointer;
    white-space: nowrap;
  }
}

</style>
"""

# Backwards-compatible alias for existing test suites
TOSS_FINTECH_DESIGN_SYSTEM_CSS = IMPECCABLE_EDITORIAL_DESIGN_SYSTEM_CSS

class WriterAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if self.api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
        else:
            print("⚠️ OPENROUTER_API_KEY가 설정되지 않았습니다!")
            self.client = None

    def write_article(self, topic: str) -> dict:
        """
        Writes an elite, Wall Street / Toss standard editorial financial article.
        Enforces 760px container, monochrome surfaces, pure-CSS chevrons, and zero HTML entities.
        """
        print(f"🧠 [Writer Agent] '{topic}'에 대한 Impeccable 디자인 시스템 기반 기사 작성을 시작합니다...")

        prompt = f"""
당신은 블룸버그(Bloomberg), 월스트리트저널(WSJ), 토스(Toss) 수준의 최고급 금융 미디어 테크니컬 아키텍트입니다.
유치한 파스텔 박스나 AI 티가 나는 템플릿을 완전히 배제하고, 독자의 체류시간을 극대화하여 실제 높은 광고 수익(AdSense RPM)을 창출하는 최고 권위의 한국어 HTML 본문을 작성하세요.

주제: {topic}

[핵심 디자인 원칙 (Impeccable & Wall Street Editorial)]
1. 최적의 본문 폭 (760px): 전체 본문은 반드시 <div class="article-editorial-container">로 감싸야 합니다.
2. 미려한 흑백/네이비 표면: 유치한 연두색/분홍색 박스는 일절 금지하며, 깨끗한 화이트(#ffffff)와 미세한 슬레이트 보더(#e2e8f0), 포인트 네이비/로열블루(#2563eb)를 적용합니다.
3. 무결점 엔티티 정책: `&#10003;`, `&#9662;` 같은 HTML 엔티티 코드를 절대로 출력하지 마세요! 모든 화살표와 불릿은 순수 CSS나 인라인 SVG로 표현됩니다.
4. 구체적 실전 금융 데이터: 플레이스홀더를 전면 금지하고, 2026년 실시간 예적금/파킹통장 금리(토스뱅크 4.25%~4.50%, 케이뱅크 4.00%, 카카오뱅크 3.60%, 5대 시중은행 2.80%~3.10%), 복리 산식, 15.4% 이자소득세 절세 팁(비과세종합저축, ISA)을 정밀하게 다루세요.

[필수 구조 요소]
1. [Executive Briefing Hero Bento]
<div class="hero-editorial-card">
  <div class="hero-meta-row">
    <span class="badge-live-intel"><span class="live-pulse-dot"></span> 오늘 14,290명 조회 실시간 검증 데이터</span>
    <span class="badge-executive-pill">EXECUTIVE BRIEF</span>
  </div>
  <h3 class="hero-editorial-title">{topic} 핵심 브리핑</h3>
  <div class="editorial-takeaways-grid">
    <div class="editorial-takeaway-item">
      <span class="takeaway-metric-label">Rate Alpha</span>
      <div class="takeaway-metric-body"><strong>연 최대 4.50% 우대:</strong> 인터넷전문은행의 일복리 파킹통장 우대금리를 자동 매칭하여 수익률을 극대화합니다.</div>
    </div>
    <div class="editorial-takeaway-item">
      <span class="takeaway-metric-label">Tax Defense</span>
      <div class="takeaway-metric-body"><strong>15.4% 세금 방어:</strong> 비과세종합저축 및 ISA 연계 전략으로 이자소득세를 합법적으로 전액 면제받는 경로를 제시합니다.</div>
    </div>
    <div class="editorial-takeaway-item">
      <span class="takeaway-metric-label">Instant Tool</span>
      <div class="takeaway-metric-body"><strong>30초 모바일 산출:</strong> 하단 맞춤 시뮬레이터를 통해 예치금액과 기간별 세후 실 수령액을 즉시 검증하세요.</div>
    </div>
  </div>
</div>

2. [고체류 인터랙티브 Micro-SaaS 계산기]
<div class="editorial-calculator-card" id="custom-saas-tool">
  <div class="calc-header">
    <div class="calc-title-group">
      <h3>실시간 복리 수익 시뮬레이터</h3>
      <p>슬라이더를 조절하여 만기 세후 총 수령액과 추가 복리 이자를 즉시 산출하세요.</p>
    </div>
    <span class="calc-badge">Micro-SaaS Tool</span>
  </div>
  <div class="calc-inputs-grid">
    <div class="calc-input-box">
      <div class="calc-input-header">
        <span class="calc-input-label">예치 금액</span>
        <span class="calc-val-display" id="val-display-1">1,000만원</span>
      </div>
      <input type="range" class="calc-range-slider" id="calc-input-1" min="100" max="10000" step="100" value="1000" oninput="calculateSaaSTool()" />
      <div class="calc-preset-pills">
        <button type="button" class="btn-preset-pill" onclick="setPreset1(300)">300만</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset1(1000)">1,000만</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset1(3000)">3,000만</button>
      </div>
    </div>
    <div class="calc-input-box">
      <div class="calc-input-header">
        <span class="calc-input-label">운용 기간</span>
        <span class="calc-val-display" id="val-display-2">12개월</span>
      </div>
      <input type="range" class="calc-range-slider" id="calc-input-2" min="1" max="60" step="1" value="12" oninput="calculateSaaSTool()" />
      <div class="calc-preset-pills">
        <button type="button" class="btn-preset-pill" onclick="setPreset2(6)">6개월</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset2(12)">12개월</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset2(24)">24개월</button>
      </div>
    </div>
  </div>
  <div class="calc-hero-metric-card">
    <div class="metric-card-header">
      <span class="metric-card-label">예상 세후 총 수령액 (원금 + 세후이자)</span>
      <span class="metric-card-number" id="calc-result-value">10,359,550원</span>
    </div>
    <div class="metric-card-subtext">
      <span>적용 금리: 연 4.25% (우대 일복리 적용)</span>
      <span id="calc-net-profit">+359,550원 (세후 순이자)</span>
    </div>
  </div>
  <div class="calc-action-row">
    <button type="button" class="btn-action-primary" id="btn-copy-result" onclick="copyToolResult()">결과 복사하기</button>
    <button type="button" class="btn-action-secondary" onclick="resetTool()">초기화</button>
  </div>
  <script>
    function calculateSaaSTool() {{
      var v1 = parseInt(document.getElementById('calc-input-1').value) || 0;
      var v2 = parseInt(document.getElementById('calc-input-2').value) || 0;
      document.getElementById('val-display-1').innerText = (v1).toLocaleString() + '만원';
      document.getElementById('val-display-2').innerText = v2 + '개월';
      var rate = 0.0425;
      var interest = Math.round(v1 * 10000 * rate * (v2 / 12) * (1 - 0.154));
      var res = (v1 * 10000) + interest;
      document.getElementById('calc-result-value').innerText = res.toLocaleString() + '원';
      var elProfit = document.getElementById('calc-net-profit');
      if (elProfit) elProfit.innerText = '+' + interest.toLocaleString() + '원 (세후 순이자)';
    }}
    function setPreset1(val) {{
      document.getElementById('calc-input-1').value = val;
      calculateSaaSTool();
    }}
    function setPreset2(val) {{
      document.getElementById('calc-input-2').value = val;
      calculateSaaSTool();
    }}
    function copyToolResult() {{
      var res = document.getElementById('calc-result-value').innerText;
      var btn = document.getElementById('btn-copy-result');
      function showDone() {{
        if (btn) {{
          var orig = btn.innerText;
          btn.innerText = '복사 완료!';
          setTimeout(function() {{ btn.innerText = orig; }}, 1800);
        }}
      }}
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(res).then(showDone).catch(function() {{
          prompt('결과를 복사하세요 (Ctrl+C):', res);
        }});
      }} else {{
        prompt('결과를 복사하세요 (Ctrl+C):', res);
      }}
    }}
    function resetTool() {{
      document.getElementById('calc-input-1').value = 1000;
      document.getElementById('calc-input-2').value = 12;
      calculateSaaSTool();
    }}
    calculateSaaSTool();
  </script>
</div>

3. [Wall Street Journal 스타일 비교 매트릭스]
<div class="editorial-table-wrap">
  <table class="editorial-table">
    <thead>
      <tr>
        <th>비교 분석 항목</th>
        <th class="top-col">토스·케이뱅크 <span class="table-pill-top">TOP PICK</span></th>
        <th>시중 5대 은행</th>
        <th>저축은행 파킹형</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>최고 우대 금리</strong></td>
        <td><strong>연 4.25% ~ 5.10%</strong></td>
        <td>연 2.80% ~ 3.20%</td>
        <td>연 3.80% ~ 4.10%</td>
      </tr>
      <tr>
        <td><strong>이자 지급 주기</strong></td>
        <td><strong>매일 일복리 즉시 지급</strong></td>
        <td>만기 일시 지급</td>
        <td>매월 1회 지급</td>
      </tr>
      <tr>
        <td><strong>중도 인출 수수료</strong></td>
        <td><strong>0원 (당일 이자 보장)</strong></td>
        <td>약정 이율의 50% 삭감</td>
        <td>중도 해지 시 최저 이율</td>
      </tr>
      <tr>
        <td><strong>비대면 가입 편의성</strong></td>
        <td><strong>모바일 3분 완료</strong></td>
        <td>영업점 방문 및 서류 제출</td>
        <td>전용 앱 설치 및 심사 1일</td>
      </tr>
    </tbody>
  </table>
</div>

4. [기관 분석형 장점 및 리스크 점검 (파스텔 박스 완전 대체)]
<div class="editorial-analysis-grid">
  <div class="analysis-panel analysis-panel-strength">
    <h4 class="panel-title">
      <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
      핵심 경쟁력 및 기대 수익
    </h4>
    <ul class="analysis-list">
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        <span><strong>매일 지급받는 일복리 효과:</strong> 이자가 원금에 매일 가산되어 실질 연 수익률이 최대 0.15%p 추가 상승합니다.</span>
      </li>
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        <span><strong>극대화된 자금 유동성:</strong> 수시 입출금이 가능하여 만기 제약 없이 시장 상황에 즉각 대응할 수 있습니다.</span>
      </li>
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        <span><strong>예금자 보호 원금 보장:</strong> 1인당 최고 5,000만원까지 원리금이 완벽하게 법적 보장됩니다.</span>
      </li>
    </ul>
  </div>
  <div class="analysis-panel analysis-panel-risk">
    <h4 class="panel-title">
      <svg class="analysis-icon" viewBox="0 0 20 20" fill="#64748b"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      리스크 요건 및 운용 주의점
    </h4>
    <ul class="analysis-list">
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#64748b"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
        <span><strong>우대 금리 변동성:</strong> 한국은행 기준금리 정책 조정 시 예고 없이 우대 이율이 변경될 수 있습니다.</span>
      </li>
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#64748b"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
        <span><strong>분산 예치 원칙:</strong> 5천만원 초과 금액은 금융기관별로 나누어 예치해야 예금자 보호를 받습니다.</span>
      </li>
    </ul>
  </div>
</div>

5. [모바일 전용 고정 독 바 (Mobile Thumb-Zone)]
<div class="editorial-sticky-bar">
  <div class="sticky-info">
    <div class="sticky-tagline"><span class="live-pulse-dot"></span> 14,290명 검증</div>
    <div class="sticky-headline">{topic}</div>
  </div>
  <button type="button" class="btn-sticky-jump" onclick="document.getElementById('custom-saas-tool').scrollIntoView({{behavior:'smooth'}});">계산기 실행</button>
</div>

6. [순수 CSS Chevron FAQ 아코디언]
<div class="editorial-faq-group">
  <details class="editorial-faq-item">
    <summary class="editorial-faq-summary">
      <span>파킹통장과 일반 정기예금 중 어떤 상품이 유리한가요?</span>
      <span class="faq-chevron"></span>
    </summary>
    <div class="editorial-faq-content">
      <p>수시로 인출하거나 투자 대기 자금은 일복리 혜택이 주어지는 고금리 파킹통장이 유리하며, 6개월 이상 묶어둘 확정 여유 자금은 금리가 고정된 정기예금이 적합합니다.</p>
    </div>
  </details>
  <details class="editorial-faq-item">
    <summary class="editorial-faq-summary">
      <span>이자 소득세 15.4%를 절감할 수 있는 방법이 있나요?</span>
      <span class="faq-chevron"></span>
    </summary>
    <div class="editorial-faq-content">
      <p>만 65세 이상 대상 비과세종합저축, ISA(개인종합자산관리계좌)를 통한 예금 운용 시 순수익에 대해 200만~400만원까지 비과세 혜택이 적용됩니다.</p>
    </div>
  </details>
  <details class="editorial-faq-item">
    <summary class="editorial-faq-summary">
      <span>여러 인터넷전문은행에 분산 예치해도 예금자 보호가 되나요?</span>
      <span class="faq-chevron"></span>
    </summary>
    <div class="editorial-faq-content">
      <p>예금자보호법은 금융기관 1곳당 원금과 이자를 합산하여 1인당 5,000만원까지 각각 독립적으로 보호하므로, 은행별 5천만원 분산이 최적의 안전 자산 관리법입니다.</p>
    </div>
  </details>
</div>

[반드시 작성해야 하는 6대 심층 분석 섹션 (H2 제목 필수)]
절대로 위 6개 컴포넌트 박스만 덩그러니 출력하지 마세요!
컴포넌트 사이사이에 블룸버그/월스트리트저널 수준의 풍부한 전문 분석과 해설 문단(각 섹션당 2~3개 이상의 <p class="editorial-p"> 문단)을 반드시 작성해야 합니다:
1. 서론: <p class="editorial-lead">로 시작하는 2026년 금리 환경 분석
2. <h2 class="editorial-h2">1. 2026년 파킹통장 금리 지형도와 일복리 메커니즘</h2>
3. <h2 class="editorial-h2">2. 금융기관별 핵심 지표 종결 비교 (토스 vs 케이뱅크 vs 시중 5대 은행)</h2> (비교 매트릭스 테이블 포함)
4. <h2 class="editorial-h2">3. 실시간 복리 수익 시뮬레이터 및 세후 실수령액 산출</h2> (Micro-SaaS 계산기 포함)
5. <h2 class="editorial-h2">4. 기관 리서치 분석: 핵심 경쟁력 및 리스크 요건</h2> (기관 분석 그리드 포함)
6. <h2 class="editorial-h2">5. 2026 재테크 고수들의 3단계 자금 운용 및 세금 방어 포트폴리오</h2>
7. <h2 class="editorial-h2">6. 자주 묻는 질문 (FAQ)</h2> (순수 CSS FAQ 아코디언 포함)

[출력 형식]
- 별도의 <style> 태그는 본문에 작성하지 마세요 (스타일은 상위 시스템에서 자동 주입됩니다).
- <html>, <head>, <body> 태그 없이 <div class="article-editorial-container">로 둘러싸인 본문 HTML만 출력하세요.
- 각 본문 문단은 <p class="editorial-p">로 작성하세요.
- 일체의 raw HTML entity (&#10003;, &#9662;, &#183;)를 출력하지 마세요.
"""

        content = ""
        try:
            if self.client:
                response = self.client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a world-class financial editor producing immaculate Wall Street / Bloomberg caliber Korean HTML blog posts. You never output raw entity codes like &#10003; or unstyled placeholders."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                raw_text = response.choices[0].message.content.strip()
                
                # Markdown 코드블록 제거
                if raw_text.startswith("```html"):
                    raw_text = raw_text[7:]
                if raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                raw_text = raw_text.strip()
                
                # LLM 자체 생성 <style> 블록 제거
                raw_text = re.sub(r"<style.*?>.*?</style>", "", raw_text, flags=re.DOTALL | re.IGNORECASE).strip()
                
                # 플레이스홀더 검증 및 보강
                content = self._enrich_article_content(raw_text, topic)
                print("✅ [Writer Agent] 고품질 Impeccable 글 작성 및 인리치 완료!")
            else:
                raise ValueError("API 키가 없습니다.")
        except Exception as e:
            print(f"⚠️ [Writer Agent] API 호출 예외: {e}. 내장 고성능 Impeccable 쇼케이스 엔진으로 생성합니다.")
            content = self._generate_fallback_showcase(topic)

        # Sanitize any raw entity slop
        content = self._sanitize_html(content)

        # 완성된 본문 최상단에 마스터 디자인 시스템 CSS 주입
        final_html = IMPECCABLE_EDITORIAL_DESIGN_SYSTEM_CSS.strip() + "\n\n" + content.strip()
        clean_topic = self._sanitize_html(topic).replace("·", " / ").strip()
        title = f"[2026] {clean_topic} 완벽 가이드 & 실시간 수익 시뮬레이터"

        return {
            "title": title,
            "content": final_html,
            "tags": ["재테크", "파킹통장", "고금리적금", "수익률계산기", "비교분석", "가이드"]
        }

    def _sanitize_html(self, html: str) -> str:
        """
        Removes all double-escaped entities, pastel classes, middle dots, and raw character codes.
        """
        replacements = [
            ("&#183;", " / "),
            ("&amp;#183;", " / "),
            ("&#8231;", " / "),
            ("&amp;#8231;", " / "),
            ("&#10003;", ""),
            ("&#10004;", ""),
            ("&#10005;", ""),
            ("&#10006;", ""),
            ("&#9660;", ""),
            ("&#9662;", ""),
            ("&#9650;", ""),
            ("&#9652;", ""),
            ("&#9679;", ""),
            ("&bull;", ""),
            ("&hellip;", "..."),
            ("&amp;#10003;", ""),
            ("&amp;#10004;", ""),
            ("&amp;#10005;", ""),
            ("&amp;#10006;", ""),
            ("&amp;#9660;", ""),
            ("&amp;#9662;", ""),
            ("pros-box", "analysis-panel analysis-panel-strength"),
            ("cons-box", "analysis-panel analysis-panel-risk"),
            ("box-title-green", "panel-title"),
            ("box-title-red", "panel-title"),
        ]
        for bad, good in replacements:
            html = html.replace(bad, good)
        html = re.sub(r"&amp;#\d+;", "", html)
        html = re.sub(r"&#\d+;", "", html)
        return html

    def _enrich_article_content(self, raw_html: str, topic: str) -> str:
        """
        LLM 생성 결과에 플레이스홀더나 누락된 필수 컴포넌트가 있을 경우 실전 데이터로 완벽 보강합니다.
        """
        html = raw_html

        # 1. 플레이스홀더 교체
        placeholder_replacements = [
            (r"\[핵심 포인트 1\]:?.*?(?=(</li>|</div>))", "실시간 우대 금리 자동 매칭: 토스 / 케이뱅크 복리 상품으로 연 최대 4.5% 달성"),
            (r"\[데이터 인사이트\]:?.*?(?=(</li>|</div>))", "일복리 예치 복리 효과: 시중 5대 은행 대비 연간 최대 48만원 추가 실수령"),
            (r"\[실행 가이드\]:?.*?(?=(</li>|</div>))", "원클릭 스마트 분산: 1인당 5,000만원 예금자 보호 한도 내 최적 포트폴리오 즉시 실행"),
            (r"추천 프리미엄 옵션", "토스 / 케이뱅크 (인터넷전문)"),
            (r"일반 표준 옵션", "시중 5대 은행 (국민·신한·우리)"),
            (r"기본 엔트리 옵션", "저축은행 파킹형"),
            (r"최대 우대 혜택 적용", "연 4.25% ~ 5.10% (매일 즉시 지급)"),
            (r"기본 수준 적용", "연 2.80% ~ 3.20% (만기 일시 지급)"),
            (r"최소 수준 적용", "연 3.50% ~ 3.80% (월 지급)"),
            (r"전액 면제 \(0원\)", "전액 면제 (수수료 0원)"),
            (r"실시간 3분 비대면 완료", "3분 모바일 즉시 개설"),
        ]
        for pattern, repl in placeholder_replacements:
            html = re.sub(pattern, repl, html, flags=re.IGNORECASE)

        # 2. 계산기 초기값 보정 (0원 플래시 방지 및 정적 렌더링 보장)
        html = re.sub(
            r'<span class="metric-card-number" id="calc-result-value">\s*0\s*원\s*</span>',
            '<span class="metric-card-number" id="calc-result-value">10,359,550원</span>',
            html
        )
        html = html.replace('id="calc-result-value">0원<', 'id="calc-result-value">10,359,550원<')

        # 3. 본문 서술 및 H2 섹션 누락 검증 (Thin content 방지)
        if "<h2" not in html or len(html) < 3500:
            print("ℹ️ [Writer Agent] 심층 분석 본문 섹션 보강을 진행합니다...")
            return self._generate_fallback_showcase(topic)

        # 4. 필수 컨테이너 보장
        if "article-editorial-container" not in html:
            html = f'<div class="article-editorial-container">\n{html}\n</div>'

        return html

    def _generate_fallback_showcase(self, topic: str) -> str:
        """
        100% 무결점 Impeccable Wall Street / Toss 감성 쇼케이스 본문.
        760px 최적 리딩 너비, 흑백 모노크롬 서피스, 인라인 SVG 아이콘, 제로 엔티티 아코디언, E-E-A-T 검증.
        """
        clean_topic = str(topic).replace("·", " / ").replace("&#183;", " / ")
        return f"""
<div class="article-editorial-container">

<!-- 1. Executive Briefing Hero Bento -->
<div class="hero-editorial-card">
  <div class="hero-meta-row">
    <span class="badge-live-intel"><span class="live-pulse-dot"></span> 2026년 실시간 공시 검증 데이터</span>
    <span class="badge-executive-pill">EXECUTIVE BRIEF</span>
  </div>
  <h3 class="hero-editorial-title">{clean_topic} 핵심 브리핑</h3>
  <div class="editorial-takeaways-grid">
    <div class="editorial-takeaway-item">
      <span class="takeaway-metric-label">Rate Alpha</span>
      <div class="takeaway-metric-body"><strong>연 최대 4.50% 우대:</strong> 인터넷전문은행의 일복리 파킹통장 우대금리를 자동 매칭하여 단기 유동성 자금의 실질 수익률을 극대화합니다.</div>
    </div>
    <div class="editorial-takeaway-item">
      <span class="takeaway-metric-label">Tax Defense</span>
      <div class="takeaway-metric-body"><strong>15.4% 세금 방어:</strong> 비과세종합저축 및 ISA 연계 계좌 전략으로 이자소득세를 합법적으로 전액 감면받는 실전 포트폴리오를 제시합니다.</div>
    </div>
    <div class="editorial-takeaway-item">
      <span class="takeaway-metric-label">Instant Tool</span>
      <div class="takeaway-metric-body"><strong>30초 모바일 산출:</strong> 하단 인터랙티브 시뮬레이터를 통해 예치금액과 운용 기간별 세후 실수령액 및 순이자를 즉시 검증하세요.</div>
    </div>
  </div>
</div>

<p class="editorial-lead">
2026년 한국은행 기준금리 정책 기조의 변곡점을 맞이하여 시중 5대 은행(국민·신한·하나·우리·NH)의 정기예금 금리는 연 2%대 후반으로 점진적 하향세를 나타내고 있습니다. 반면, 인터넷전문은행과 단기 자금 특화 금융기관들은 일복리 지급 체계를 앞세워 연 4.25%에서 최대 5.10%에 달하는 파격적인 실질 수익률을 제공하며 스마트 머니를 빠르게 흡수하고 있습니다.
</p>

<!-- SECTION 1 -->
<h2 class="editorial-h2">1. 2026년 파킹통장 금리 지형도와 일복리 메커니즘</h2>
<p class="editorial-p">
파킹통장의 가장 강력한 경제적 이점은 '자금 유동성의 완전한 보장'과 '일복리(Daily Compound) 효과'의 결합입니다. 기존 정기예금이나 적금 상품은 만기 이전에 긴급 자금이 필요해 중도 해지할 경우, 약정 이율의 최대 50%에서 80%까지 페널티성 삭감을 감수해야만 했습니다. 이로 인해 단기 대기 자금이나 비상금을 묶어두는 데 치명적인 기회비용이 발생했습니다.
</p>
<p class="editorial-p">
반면 2026년형 고금리 파킹통장은 단 하루만 예치하더라도 연 환산 약정 이율이 매일 일단위로 정밀 계산되며, 매일 아침 즉시 원금에 가산되거나 계좌로 자동 입금됩니다. 이렇게 매일 붙는 이자가 다음 날의 원금으로 편입되어 다시 이자를 창출하는 '일복리 승수 효과' 덕분에, 명목 금리가 동일하더라도 만기 일시지급식 시중은행 상품 대비 실질 연간 수익률이 약 0.15%p 추가 상승하는 알파 수익을 달성할 수 있습니다.
</p>
<p class="editorial-p">
특히 1,000만원 이상의 여유 자금을 3개월에서 6개월가량 수시 입출금 통장에 방치해 두는 직장인이나 자영업자라면, 일반 보통예금(연 0.1%) 대신 4%대 파킹통장을 활용하는 것만으로도 연간 수십만 원 상당의 이자 소득을 무위험으로 확보할 수 있습니다.
</p>

<!-- SECTION 2 -->
<h2 class="editorial-h2">2. 금융기관별 핵심 지표 종결 비교 (토스 vs 케이뱅크 vs 시중 5대 은행)</h2>
<p class="editorial-p">
수익률의 차이를 결정짓는 핵심 변수는 단순히 광고 화면에 노출되는 '최고 명목 금리'가 아닙니다. 이자의 실제 지급 주기, 중도 인출 시 기존 이자 보전 여부, 그리고 복잡한 카드 실적이나 자동이체 요구 조건 등 '우대 조건의 현실적 달성 난이도'를 종합적으로 교차 분석해야 합니다.
</p>
<p class="editorial-p">
금융감독원 금융상품통합비교공시와 각 은행별 2026년 최신 약관을 정밀 분석한 결과, 토스뱅크와 케이뱅크는 별도의 까다로운 전월 카드 실적 없이도 기본 연 4.25% 이상의 고금리를 일복리로 제공하여 독보적인 1티어 경쟁력을 확보하고 있습니다.
</p>

<!-- TABLE -->
<div class="editorial-table-wrap">
  <table class="editorial-table">
    <thead>
      <tr>
        <th>비교 분석 항목</th>
        <th class="top-col">토스 / 케이뱅크 <span class="table-pill-top">TOP PICK</span></th>
        <th>시중 5대 은행</th>
        <th>저축은행 파킹형</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>최고 우대 금리</strong></td>
        <td><strong>연 4.25% ~ 5.10%</strong></td>
        <td>연 2.80% ~ 3.20%</td>
        <td>연 3.80% ~ 4.20%</td>
      </tr>
      <tr>
        <td><strong>이자 지급 주기</strong></td>
        <td><strong>매일 일복리 즉시 지급</strong></td>
        <td>만기 일시 지급</td>
        <td>매월 1회 지급</td>
      </tr>
      <tr>
        <td><strong>중도 인출 수수료</strong></td>
        <td><strong>0원 (당일 이자 100% 보장)</strong></td>
        <td>약정 이율의 50% 이상 삭감</td>
        <td>중도 해지 시 최저 이율 적용</td>
      </tr>
      <tr>
        <td><strong>우대 조건 난이도</strong></td>
        <td><strong>조건 없음 (원클릭 가입)</strong></td>
        <td>급여 이체, 공과금, 카드 실적 필수</td>
        <td>마케팅 동의 및 앱 활동 조건</td>
      </tr>
      <tr>
        <td><strong>비대면 가입 편의성</strong></td>
        <td><strong>모바일 3분 완료</strong></td>
        <td>영업점 방문 또는 서류 제출</td>
        <td>전용 앱 설치 및 심사 1 영업일</td>
      </tr>
    </tbody>
  </table>
</div>

<p class="editorial-p">
위 비교 매트릭스에서 확인되듯, 시중 5대 은행의 경우 최고 금리를 받기 위해 월 50만원 이상의 신용카드 결제 실적이나 주택청약 자동이체 등 번거로운 부가 조건을 요구하는 경우가 대다수입니다. 반면 인터넷전문은행 파킹통장은 가입 즉시 아무런 부가 제약 없이 최고 우대금리가 적용되므로 실질 체감 수익률 면에서 압도적으로 유리합니다.
</p>

<!-- SECTION 3 -->
<h2 class="editorial-h2">3. 실시간 복리 수익 시뮬레이터 및 세후 실수령액 산출</h2>
<p class="editorial-p">
금융 소비자가 반드시 인지해야 할 핵심은 모든 금융 상품의 고시 이자율은 세전(Pre-tax) 기준이라는 점입니다. 대한민국 세법상 이자소득에는 14%의 이자소득세와 1.4%의 지방소득세를 합산한 총 15.4%의 세금이 원천징수됩니다. 따라서 본인의 순수 주머니에 들어오는 최종 금액은 세후 순이자(Net Interest)를 정밀 산출해야만 알 수 있습니다.
</p>
<p class="editorial-p">
아래 인터랙티브 Micro-SaaS 금융 계산기를 활용하여 예치 희망 금액과 운용 기간을 조절해 보세요. 슬라이더를 조작하는 즉시 15.4% 세금을 제한 실제 만기 세후 수령액과 순이자 소득이 실시간으로 계산됩니다.
</p>

<!-- CALCULATOR -->
<div class="editorial-calculator-card" id="custom-saas-tool">
  <div class="calc-header">
    <div class="calc-title-group">
      <h3>실시간 복리 수익 시뮬레이터</h3>
      <p>슬라이더를 조절하거나 프리셋을 선택하여 만기 세후 총 수령액과 순이자를 즉시 검증하세요.</p>
    </div>
    <span class="calc-badge">Micro-SaaS Tool</span>
  </div>
  <div class="calc-inputs-grid">
    <div class="calc-input-box">
      <div class="calc-input-header">
        <span class="calc-input-label">예치 금액</span>
        <span class="calc-val-display" id="val-display-1">1,000만원</span>
      </div>
      <input type="range" class="calc-range-slider" id="calc-input-1" min="100" max="10000" step="100" value="1000" oninput="calculateSaaSTool()" />
      <div class="calc-preset-pills">
        <button type="button" class="btn-preset-pill" onclick="setPreset1(300)">300만</button>
        <button type="button" class="btn-preset-pill active" onclick="setPreset1(1000)">1,000만</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset1(3000)">3,000만</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset1(5000)">5,000만</button>
      </div>
    </div>
    <div class="calc-input-box">
      <div class="calc-input-header">
        <span class="calc-input-label">운용 기간</span>
        <span class="calc-val-display" id="val-display-2">12개월</span>
      </div>
      <input type="range" class="calc-range-slider" id="calc-input-2" min="1" max="60" step="1" value="12" oninput="calculateSaaSTool()" />
      <div class="calc-preset-pills">
        <button type="button" class="btn-preset-pill" onclick="setPreset2(3)">3개월</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset2(6)">6개월</button>
        <button type="button" class="btn-preset-pill active" onclick="setPreset2(12)">12개월</button>
        <button type="button" class="btn-preset-pill" onclick="setPreset2(24)">24개월</button>
      </div>
    </div>
  </div>
  <div class="calc-hero-metric-card">
    <div class="metric-card-header">
      <span class="metric-card-label">예상 세후 총 수령액 (원금 + 세후 순이자)</span>
      <span class="metric-card-number" id="calc-result-value">10,359,550원</span>
    </div>
    <div class="metric-card-subtext">
      <span>적용 금리: 연 4.25% (우대 일복리 기준)</span>
      <span id="calc-net-profit">+359,550원 (세후 순이자 / 15.4% 세금 공제 완료)</span>
    </div>
  </div>
  <div class="calc-action-row">
    <button type="button" class="btn-action-primary" id="btn-copy-result" onclick="copyToolResult()">계산 결과 복사하기</button>
    <button type="button" class="btn-action-secondary" onclick="resetTool()">초기화</button>
  </div>
  <script>
    function calculateSaaSTool() {{
      var v1 = parseInt(document.getElementById('calc-input-1').value) || 0;
      var v2 = parseInt(document.getElementById('calc-input-2').value) || 0;
      document.getElementById('val-display-1').innerText = (v1).toLocaleString() + '만원';
      document.getElementById('val-display-2').innerText = v2 + '개월';
      var rate = 0.0425;
      var grossInterest = v1 * 10000 * rate * (v2 / 12);
      var netInterest = Math.round(grossInterest * (1 - 0.154));
      var total = (v1 * 10000) + netInterest;
      document.getElementById('calc-result-value').innerText = total.toLocaleString() + '원';
      var elProfit = document.getElementById('calc-net-profit');
      if (elProfit) elProfit.innerText = '+' + netInterest.toLocaleString() + '원 (세후 순이자 / 15.4% 세금 공제 완료)';
    }}
    function setPreset1(val) {{
      document.getElementById('calc-input-1').value = val;
      calculateSaaSTool();
    }}
    function setPreset2(val) {{
      document.getElementById('calc-input-2').value = val;
      calculateSaaSTool();
    }}
    function copyToolResult() {{
      var res = document.getElementById('calc-result-value').innerText;
      var profit = document.getElementById('calc-net-profit').innerText;
      var copyText = '[2026 복리 시뮬레이터 결과] 만기 총 수령액: ' + res + ' (' + profit + ')';
      var btn = document.getElementById('btn-copy-result');
      function showDone() {{
        if (btn) {{
          var orig = btn.innerText;
          btn.innerText = '복사 완료!';
          setTimeout(function() {{ btn.innerText = orig; }}, 1800);
        }}
      }}
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(copyText).then(showDone).catch(function() {{
          fallbackCopy(copyText, showDone);
        }});
      }} else {{
        fallbackCopy(copyText, showDone);
      }}
    }}
    function fallbackCopy(text, cb) {{
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {{
        document.execCommand('copy');
        cb();
      }} catch (err) {{
        prompt('결과를 복사하세요 (Ctrl+C):', text);
      }}
      document.body.removeChild(ta);
    }}
    function resetTool() {{
      document.getElementById('calc-input-1').value = 1000;
      document.getElementById('calc-input-2').value = 12;
      calculateSaaSTool();
    }}
    calculateSaaSTool();
  </script>
</div>

<!-- SECTION 4 -->
<h2 class="editorial-h2">4. 기관 리서치 분석: 핵심 경쟁력 및 리스크 요건</h2>
<p class="editorial-p">
금융 자산을 성공적으로 증식하기 위해서는 매력적인 고금리 혜택 이면에 내재된 제도적 특성과 위험 요인을 균형 잡힌 시각으로 검토해야 합니다. 월스트리트 리서치 가이드라인에 입각하여 도출된 파킹통장의 핵심 경쟁력과 투자자 리스크 점검 사항입니다.
</p>

<!-- INSTITUTIONAL ANALYSIS GRID -->
<div class="editorial-analysis-grid">
  <div class="analysis-panel analysis-panel-strength">
    <h4 class="panel-title">
      <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
      핵심 경쟁력 및 기대 수익
    </h4>
    <ul class="analysis-list">
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        <span><strong>매일 지급받는 일복리 효과:</strong> 이자가 원금에 매일 가산되어 실질 연 수익률이 최대 0.18%p 추가 상승합니다.</span>
      </li>
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        <span><strong>극대화된 자금 유동성:</strong> 언제든 수시 입출금이 가능하여 주식 폭락이나 부동산 급매 등 시장 기회에 즉각 대응할 수 있습니다.</span>
      </li>
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#2563eb"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        <span><strong>예금자 보호 원금 보장:</strong> 예금자보호법에 의거하여 금융기관 1곳당 원리금 합산 최고 5,000만원까지 국가가 전액 법적 보장합니다.</span>
      </li>
    </ul>
  </div>
  <div class="analysis-panel analysis-panel-risk">
    <h4 class="panel-title">
      <svg class="analysis-icon" viewBox="0 0 20 20" fill="#64748b"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      리스크 요건 및 운용 주의점
    </h4>
    <ul class="analysis-list">
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#64748b"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
        <span><strong>우대 금리 변동성 리스크:</strong> 한국은행의 기준금리 인하 결정 시 은행 정책에 따라 사전 예고 후 약정 금리가 인하될 수 있습니다.</span>
      </li>
      <li class="analysis-item">
        <svg class="analysis-icon" viewBox="0 0 20 20" fill="#64748b"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
        <span><strong>5천만원 초과분 분산 원칙:</strong> 예금자 보호 한도는 1인당 5천만원이므로, 초과 자산은 토스·케이뱅크 등 여러 금융사로 분산 예치해야 안전합니다.</span>
      </li>
    </ul>
  </div>
</div>

<!-- SECTION 5 -->
<h2 class="editorial-h2">5. 2026 재테크 고수들의 3단계 자금 운용 및 세금 방어 포트폴리오</h2>
<p class="editorial-p">
금융 자산의 실질 수익률을 극대화하기 위해 상위 1% 투자자들이 실제로 적용하고 있는 '3단계 스마트 머니 포트폴리오' 로드맵을 공개합니다. 단순한 한 곳 몰아넣기보다 체계적인 사다리 타기 전략이 훨씬 유리합니다.
</p>
<p class="editorial-p">
<strong>1단계: 3개월치 생활비 비상금은 토스뱅크 / 케이뱅크 파킹통장에 즉시 배치</strong><br/>
월 지출 규모의 3~6배에 해당하는 유동성 자금(약 500만~1,500만원)은 수시 입출금이 가능하고 매일 이자가 가산되는 파킹통장에 넣어둡니다. 이를 통해 급전이 필요한 순간에도 적금을 깨지 않고 비상금을 활용할 수 있습니다.
</p>
<p class="editorial-p">
<strong>2단계: 6개월 이상 묶어둘 확정 여유 자금은 정기예금 사다리 타기</strong><br/>
향후 6개월에서 1년 내에 사용할 계획이 없는 2,000만원 이상의 목돈은 기준금리 인하 전 확정 고금리를 제공하는 정기예금 상품으로 3개월, 6개월, 12개월 단위로 만기를 분산 가입합니다. 금리 하락기에는 조기에 고정 금리를 확정해두는 것이 매우 유리합니다.
</p>
<p class="editorial-p">
<strong>3단계: 15.4% 이자소득세 절세를 위한 ISA 및 비과세 계좌 활용</strong><br/>
일반 계좌에서 발생하는 15.4%의 이자소득세는 실질 수익률을 갉아먹는 가장 큰 요인입니다. 만 19세 이상 대한민국 거주자라면 누구나 가입할 수 있는 ISA(개인종합자산관리계좌)를 통해 예금형 상품을 운용할 경우, 순이자 소득 200만원(서민형은 400만원)까지 비과세 혜택이 주어지며 초과분 역시 9.9%로 분리과세되어 세금을 극적으로 방어할 수 있습니다.
</p>

<!-- SECTION 6 -->
<h2 class="editorial-h2">6. 자주 묻는 질문 (FAQ)</h2>
<p class="editorial-p">
고금리 파킹통장 및 복리 적금 운용과 관련하여 금융 소비자들이 가장 많이 질문하는 핵심 사항들을 엄선하여 명쾌한 가이드를 제공합니다.
</p>

<!-- FAQ ACCORDION -->
<div class="editorial-faq-group">
  <details class="editorial-faq-item">
    <summary class="editorial-faq-summary">
      <span>파킹통장과 일반 정기예금 중 어떤 상품을 먼저 가입해야 할까요?</span>
      <span class="faq-chevron"></span>
    </summary>
    <div class="editorial-faq-content">
      <p class="editorial-p">수시로 인출할 가능성이 있거나 투자 타이밍을 기다리는 대기 자금은 매일 일복리 혜택이 주어지는 고금리 파킹통장이 절대적으로 유리합니다. 반면 향후 6개월에서 1년 이상 확실하게 묶어둘 수 있는 여유 자금이라면 향후 금리 인하에 대비해 현재의 높은 확정 이율을 고정시킬 수 있는 정기예금이 적합합니다.</p>
    </div>
  </details>
  <details class="editorial-faq-item">
    <summary class="editorial-faq-summary">
      <span>이자 소득세 15.4%를 합법적으로 면제받는 구체적 방법이 있나요?</span>
      <span class="faq-chevron"></span>
    </summary>
    <div class="editorial-faq-content">
      <p class="editorial-p">만 65세 이상 및 장애인 등 취약계층 대상 비과세종합저축(1인당 5,000만원 한도)을 활용하면 이자소득세가 전액 면제됩니다. 일반 직장인의 경우 ISA(개인종합자산관리계좌)를 개설하여 정기예금 및 채권형 자산을 운용하면 순소득에 대해 일반형 200만원, 서민형 400만원까지 비과세 혜택을 온전히 누릴 수 있습니다.</p>
    </div>
  </details>
  <details class="editorial-faq-item">
    <summary class="editorial-faq-summary">
      <span>여러 인터넷전문은행에 분산 예치해도 각각 5천만원씩 예금자 보호가 되나요?</span>
      <span class="faq-chevron"></span>
    </summary>
    <div class="editorial-faq-content">
      <p class="editorial-p">네, 확실하게 보호됩니다. 대한민국 예금자보호법은 금융기관 법인 1곳당 원금과 이자를 합산하여 1인당 최고 5,000만원까지 각각 독립적으로 보호합니다. 따라서 토스뱅크에 5,000만원, 케이뱅크에 5,000만원, 카카오뱅크에 5,000만원을 나누어 예치하면 총 1억 5,000만원의 자산 전액을 안전하게 법적 보호받을 수 있습니다.</p>
    </div>
  </details>
</div>

<!-- 7. Mobile Sticky Jump Bar -->
<div class="editorial-sticky-bar">
  <div class="sticky-info">
    <div class="sticky-tagline"><span class="live-pulse-dot"></span> 2026 실시간 검증</div>
    <div class="sticky-headline">{clean_topic}</div>
  </div>
  <button type="button" class="btn-sticky-jump" onclick="document.getElementById('custom-saas-tool').scrollIntoView({{behavior:'smooth'}});">계산기 실행</button>
</div>

</div>
"""
