# -*- coding: utf-8 -*-
"""
engine/crew/tasks.py
--------------------
CrewAI 태스크 명세: 기획 -> 위젯 개발 -> SEO/Schema 패키징 -> [Patch 1] 자가치유 재작성 태스크
타겟 도메인: 투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터 (FinTech Micro-SaaS)
"""

from crewai import Task
from typing import Dict, Any, List


class MicroSaaSCrewTasks:
    def plan_interactive_keyword_task(self, agent, user_hint: str = "") -> Task:
        return Task(
            description=f"""
1. 타겟 도메인 '투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터' 내에서 가장 수요가 높고 반복 체류율이 극대화되는 롱테일 마이크로 툴 주제를 1개 선정하십시오.
   (사용자 힌트: {user_hint or '2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터'})
2. 반드시 사용자가 조작 가능한 '최소 3개 이상의 입력 파라미터(Inputs)'와 '2개 이상의 동적 산출 결과(Outputs)'를 명시하십시오.
   - 예시 (해외주식 양도세):
     Inputs: 연간 총 실현수익(원), 연간 총 실현손실(원), 증권사 매매 수수료(원), 적용 환율(원/USD)
     Outputs: 손익통산 순이익(원), 과세표준(원), 총 납부세액(원), 실효세율(%), 세후 순수령액(원)
3. 해당 도구의 명확한 공식 계산 수식(Formula)을 도출하십시오.
   - 과세표준 = Max(0, (실현수익 - 실현손실 - 매매수수료) - 기본공제 250만 원)
   - 총 세액 = 과세표준 * 22% (양도세 20% + 지방소득세 2%)
   - 실효세율(%) = (총 세액 / 총 실현수익) * 100

반드시 마크다운 백틱(```json ... ```) 안에 다음 JSON 형식으로만 응답하십시오:
{{
  "target_keyword": "2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터",
  "tool_type": "CALCULATOR",
  "math_formula": "Tax = Max(0, (Gain - Loss - Fees) - 2500000) * 0.22",
  "formula_badge": "양도세 = Max(0, 순수익 - 250만) × 22%",
  "key_stat": "기본공제: 2,500,000원 | 총세율: 22%",
  "sub_label": "2026 소득세법 제94조 손익통산 기준",
  "inputs": [
    {{"id": "gain", "label": "연간 총 실현수익 (KRW)", "type": "number", "min": 0, "max": 1000000000, "step": 100000, "default": 10000000, "unit": "원"}},
    {{"id": "loss", "label": "연간 총 실현손실 (KRW)", "type": "number", "min": 0, "max": 500000000, "step": 100000, "default": 3000000, "unit": "원"}},
    {{"id": "fee", "label": "증권사 매매 수수료 (KRW)", "type": "number", "min": 0, "max": 10000000, "step": 10000, "default": 50000, "unit": "원"}},
    {{"id": "fx", "label": "결제 기준 환율 (USD/KRW)", "type": "number", "min": 900, "max": 2500, "step": 10, "default": 1380, "unit": "원/$"}}
  ],
  "outputs": ["손익통산 순이익 (원)", "과세표준 (원)", "총 납부세액 (원)", "실효세율 (%)", "세후 실수령액 (원)"]
}}
""",
            expected_output="JSON 기획 명세서",
            agent=agent
        )

    def build_micro_saas_widget_task(self, agent) -> Task:
        return Task(
            description="""
이전 태스크에서 기획된 JSON 명세서를 바탕으로 Google Blogger 본문에 삽입될 순수 HTML/JS/CSS 금융 단일 컴포넌트를 작성하십시오.

[엄격한 제약조건]:
1. 외부 CDN, npm, 프레임워크(React/Vue), jQuery 사용 절대 금지. 오직 브라우저 내장 Vanilla JS만 사용.
2. 모바일 반응형: 최대 너비 100%, 360px 모바일 화면에서도 가로 스크롤이 생기지 않도록 `box-sizing: border-box` 및 CSS Grid/Flex 사용.
3. 0ms 반응형 연산: 숫자 입력창(`input type="number"`)과 슬라이더에 `input`, `change` 이벤트 리스너를 바인딩하여 입력 즉시 화면 갱신.
4. 부동소수점 오차 및 비정상 토큰 원천 방어:
   - 원화 금액: `Math.round(val).toLocaleString('ko-KR') + '원'`
   - 달러 및 비율: `Number(val).toFixed(2)`
   - 입력값이 음수이거나 NaN일 경우 `Math.max(0, val)` 및 0 fallback 처리. 'NaN원', 'undefined원', 'Infinity%' 노출 영구 금지.
5. 시각적 요약 게이지 바: 순수익(Net Profit) 대비 세금(Tax) 점유율을 나타내는 동적 CSS 게이지 바(Visual Breakdown Bar) 필수 포함.
6. 결과 복사 버튼(`navigator.clipboard.writeText`) 기능 내장.
7. 제휴 증권사/플랫폼 연계 안내 CTA 슬롯 포함.
8. [Toss Dark UI 스타일링 엄격 준수 - 화이트 배경 영구 금지]:
   - 컨테이너 배경: `#0a0e17` 또는 `#111827` (화이트 `#ffffff`, `#fff` 사용 영구 금지).
   - 카드/패널: `background: #131c2e; border: 1px solid #1f2d47; border-radius: 14px; padding: 20px; color: #f8fafc;`.
   - 입력창(`input`, `select`): `background: #0a0e17; color: #ffffff; border: 1px solid #2d3e5e; border-radius: 8px; padding: 12px 14px; font-size: 15px;`.
   - 텍스트 색상: 메인 제목/수치 `#ffffff`, 본문 및 결과값 `#f8fafc`, 보조 레이블 `#94a3b8` (WCAG AAA 대비율 7:1 이상 확보).
   - 주요 강조 버튼: `background: #3b82f6; color: #ffffff; border: none; border-radius: 10px; font-weight: 700; cursor: pointer;`.

반드시 `<div class="blogin-saas-container"> ... </div>`로 래핑된 완전한 HTML 코드 블록으로만 출력하십시오.
""",
            expected_output="Blogger 임베딩용 완전한 HTML + Vanilla JS 코드 블록",
            agent=agent
        )

    def repair_micro_saas_widget_task(self, agent, original_spec_json: str, error_logs: List[str]) -> Task:
        """
        [Patch 1] 자가치유 루프 컨텍스트 유실 방지 태스크:
        첫 번째 단계의 기획 명세서(JSON)와 QA 실패 에러 로그를 동시에 주입하여 원래 목적에 맞는 코드로 완벽 재작성.
        """
        err_str = "\n".join(error_logs)
        return Task(
            description=f"""
[긴급 버그 수정 - FinTech Micro-SaaS 컴포넌트 재작성]
Playwright 샌드박스 QA 검증에서 다음과 같은 치명적 결함이 감지되었습니다:
--------------------------------------------------
{err_str}
--------------------------------------------------

당신은 첫 번째 단계에서 승인되었던 [원래의 기획 명세서]를 100% 준수하면서, 위 에러를 완벽히 해결한 코드를 다시 작성해야 합니다.
절대 다른 주제로 탈주하거나 입력/출력 인터페이스를 임의로 변경하지 마십시오.

[원래의 기획 명세서 (SSOT)]:
{original_spec_json}

[필수 수정 지침]:
1. JS 계산 결과창에 'NaN원', 'undefined원', 'null', 'Infinity%'가 출력되지 않도록 연산 전 `isNaN(val) ? 0 : val` 방어 코드를 적용하십시오.
2. 원화 금액은 `Math.round(val).toLocaleString('ko-KR') + '원'`, 비율은 `Number(val).toFixed(2) + '%'`로 엄격 포맷팅하십시오.
3. 360px 모바일 뷰포트에서 가로 스크롤(Overflow-X)이 발생하지 않도록 모든 그리드와 컨테이너에 `max-width: 100%; box-sizing: border-box;`를 적용하십시오.
4. Toss Dark UI 스타일링 엄격 준수: 컨테이너 및 카드 배경에 화이트(#ffffff, #fff) 사용 영구 금지. 캔버스 #0a0e17, 카드 #131c2e, 텍스트 #f8fafc.
5. `<div class="blogin-saas-container"> ... </div>` 단일 HTML 블록으로만 출력하십시오.
""",
            expected_output="버그가 수정된 완전한 HTML + Vanilla JS 코드 블록",
            agent=agent
        )

    def package_technical_seo_task(self, agent, published_posts_path: str = "data/published_posts.json") -> Task:
        return Task(
            description=f"""
개발된 금융 웹 툴 상단과 하단에 결합될 고밀도 테크니컬 SEO 가이드와 Schema 구조화 데이터를 완성하십시오.

[필수 작업 내용]:
1. Schema.org 구조화 데이터:
   - `<script type="application/ld+json">` 태그 안에 반드시 다음 3가지 속성이 포함된 `SoftwareApplication` 스키마와 `FAQPage` 스키마를 포함:
     * "@type": "SoftwareApplication"
     * "applicationCategory": "FinanceApplication"
     * "operatingSystem": "Any"
   - 문법 오류(쉼표 누락, 따옴표 에러) 없이 `json.loads()`가 100% 통과하도록 엄격한 JSON-LD 규격 준수.
2. YMYL 금융 정책 준수 및 과장 광고 원천 금지:
   - '원금 보장', '무조건 수익', '100% 수익', '확정 수익' 등 투자 유혹/허위 문구 절대 사용 금지.
3. 법적 투자 면책 조항 필수 포함:
   - 본문 최하단에 반드시 다음 태그를 포함하여 법적 투자 면책 조항을 정적 HTML로 렌더링할 것:
     <div class="legal-disclaimer" style="margin-top:36px; padding:20px; background:#0f172a; border-left:4px solid #ef4444; border-radius:8px; color:#94a3b8; font-size:13px; line-height:1.7;">
       <strong style="color:#f87171; display:block; font-size:14px; margin-bottom:8px;">⚖️ 법적 면책 조항 및 세무 안내 고지</strong>
       본 시뮬레이터는 소득세법 제94조 및 지방세법에 규정된 해외주식 양도소득세 산식을 기반으로 제작된 수학적 참고 도구이며, 실제 개별 투자자의 체결 환율, 제비용, 타 소득 합산 여부에 따라 실제 납부 세액과 차이가 발생할 수 있습니다. 본 사이트는 금융투자업 인가 법인이 아니며 본 도구의 결과는 투자 권유나 세무 자문이 아닙니다. 최종 책임은 투자자 본인에게 있습니다.
     </div>
4. 본문 해설 콘텐츠:
   - 소득세법 제94조 기준 손익통산의 원리(1월 1일 ~ 12월 31일 결제일 기준 손익 상계), 250만 원 기본공제 차감 방식, 합법적 절세 전략(연말 손실 종목 매도, 배우자 증여) 해설.
   - 상투적인 AI 클리셰("안녕하세요", "현대 사회에서", "알아보겠습니다") 엄격 금지.
5. [전체 페이지 조립 및 Toss Dark UI 고대비 가독성 절대 보장]:
   - 최상단: JSON-LD 스키마 (SoftwareApplication: FinanceApplication + FAQPage)
   - 상단: H1 타이틀 + 요약 Bento 카드
   - 중앙: [FRONTEND_WIDGET_CODE] (이전 단계의 Micro-SaaS HTML)
   - 중앙 하단: [VIBE_TRADING_BANNER] 모의투자 랭킹전 참여 CTA 박스:
     <div class="blogin-vibe-banner" style="margin:36px 0; padding:24px; background:linear-gradient(135deg, #0d1527 0%, #172554 100%); border:1px solid #1e3a8a; border-radius:16px; text-align:center;">
       <span style="display:inline-block; background:#2563eb; color:#ffffff; font-size:11px; font-weight:800; padding:4px 10px; border-radius:6px; margin-bottom:10px;">PRO QUANT TRADING BATTLE</span>
       <h3 style="margin:0 0 8px 0; color:#ffffff; font-size:20px; font-weight:900;">🔥 VIBE TRADING: 실시간 모의투자 & 랭킹 배틀</h3>
       <p style="margin:0 0 16px 0; color:#cbd5e1; font-size:14px; line-height:1.6;">트레이딩뷰 실시간 차트로 BTC/ETH/NVDA 1x~20x 레버리지 모의투자에 참여하고, Top 10 명예의 전당 랭킹에 도전하세요! (가상 자금 $10,000 지원)</p>
       <a href="https://blogin365ai.blogspot.com/p/vibe-trading.html" style="display:inline-block; background:#10b981; color:#ffffff !important; font-weight:800; font-size:14px; padding:12px 24px; border-radius:10px; text-decoration:none;">
         🚀 지금 바로 모의투자 랭킹전 참여하기 →
       </a>
     </div>
   - 하단: H2 기반 세무 분석 본문 + FAQ 아코디언(<details>) + <div class="legal-disclaimer">...</div>
   - [디자인 및 가독성 필수 지침 (화이트 박스/투명 글씨 엄격 금지)]:
     * 최상위 래퍼 또는 본문 컨테이너에 `background: #fff`, `#ffffff`, `background-color: white`를 절대 넣지 마십시오.
     * 컨테이너는 투명 또는 블로그 테마 캔버스(`background: transparent` 또는 `background: #0a0e17`)를 사용하십시오.
     * 모든 본문 문단 `<p>`와 목록 `<li>`는 고대비 아이보리/슬레이트(`color: #e2e8f0; font-size: 16px; line-height: 1.8;`)를 사용하여 다크 테마에서 100% 선명하게 읽히도록 하십시오.
     * 소제목 `<h2>`는 선명한 화이트(`color: #ffffff; font-weight: 800; border-bottom: 1px solid #1f2d47; padding-bottom: 8px; margin-top: 36px;`).
     * Bento 카드 및 FAQ `<details>`: `background: #111827; border: 1px solid #1f2d47; border-radius: 14px; padding: 18px; color: #f8fafc;`.
     * 어떤 경우에도 흰색 바탕에 회색 글씨가 렌더링되어 투명해 보이거나 읽을 수 없는 참사를 발생시키지 마십시오.
""",
            expected_output="JSON-LD 및 완성된 전체 블로그 포스트 HTML",
            agent=agent
        )
