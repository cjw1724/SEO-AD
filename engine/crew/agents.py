# -*- coding: utf-8 -*-
"""
engine/crew/agents.py
---------------------
CrewAI 8-Layer Programmatic Micro-SaaS 파이프라인 에이전트 정의
타겟 도메인: 투자/트레이딩 유틸리티 및 퀀트 수익률·세금 시뮬레이터 (FinTech Micro-SaaS)
"""

import os
from crewai import Agent, LLM


def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or "sk-dummy-key"
    base_url = "https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None
    model_name = os.getenv("CREW_MODEL", "openrouter/google/gemini-2.5-flash")
    if not model_name.startswith("openrouter/") and os.getenv("OPENROUTER_API_KEY"):
        model_name = f"openrouter/{model_name}"

    return LLM(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=0.2
    )


class MicroSaaSCrewAgents:
    def __init__(self):
        self.llm = get_llm()

    def keyword_intent_researcher(self) -> Agent:
        return Agent(
            role="Quant & Investment Intent Architect",
            goal="단순 텍스트 설명으로 끝나는 키워드를 전면 배제하고, "
                 "사용자 입력값에 따라 해외주식 양도소득세, 물타기 평단가 역산, 선물 레버리지 청산가, 복리 배당 세액 등이 실시간 연산되는 인터랙티브 금융 툴 키워드를 기획한다.",
            backstory="당신은 퀀트 트레이딩 시스템 및 금융 세무 알고리즘 수석 설계자이자 고밀도 pSEO 전문가입니다. "
                      "포털의 흔한 정보글을 배제하고, '2026 해외주식 양도소득세 손익통산 및 절세 시뮬레이터', "
                      "'주식 코인 물타기 평단가 및 본전 탈출 역산 시뮬레이터', '선물 레버리지 청산가 및 켈리 공식 계산기' 등 "
                      "투자자가 실전 매매 직전 북마크하고 반복 사용할 수밖에 없는 정밀 계산/시뮬레이션 주제만 선정합니다.",
            verbose=True,
            memory=False,
            llm=self.llm
        )

    def frontend_tool_builder(self) -> Agent:
        return Agent(
            role="FinTech Micro-SaaS Frontend Engineer",
            goal="Google Blogger 본문에 직접 삽입 가능한 360px 모바일 완벽 대응 반응형 금융 시뮬레이터를 "
                 "외부 라이브러리 없이 Single-File HTML + Vanilla JS + Scoped CSS로 작성한다.",
            backstory="당신은 순수 바닐라 자바스크립트로 0ms 반응형 금융 계산기를 제작하는 프론트엔드 장인입니다. "
                 "원화 금액은 Math.round(val).toLocaleString('ko-KR') + '원', 비율/달러는 .toFixed(2)로 포맷팅하여 "
                 "부동소수점 오차나 NaN/Infinity 노출을 원천 방어합니다. "
                 "입력값 변경 시 실시간 세액 게이지 바를 동적으로 렌더링하고 결과 클립보드 복사 기능을 구현합니다.",
            verbose=True,
            memory=False,
            llm=self.llm
        )

    def technical_seo_writer(self) -> Agent:
        return Agent(
            role="Financial Tech Writer & Tax Schema Architect",
            goal="소득세법 및 퀀트 공식의 원리를 해설하는 고밀도 SEO 가이드를 작성하고, "
                 "Schema.org FinanceApplication과 FAQPage JSON-LD, 그리고 법적 투자 면책 조항(<div class='legal-disclaimer'>)을 결합한다.",
            backstory="당신은 Google Search Central 및 금융/세무 정책 가이드라인을 완벽히 꿰뚫고 있는 테크니컬 SEO 디렉터입니다. "
                      "과장 광고('원금 보장', '무조건 수익')를 원천 차단하고, 소득세법 제94조 기준과 수학적 공식을 명시하며, "
                      "Googlebot이 도구를 FinanceApplication으로 완벽히 인식하도록 Schema.org 표준 마크업을 생성합니다.",
            verbose=True,
            memory=False,
            llm=self.llm
        )
