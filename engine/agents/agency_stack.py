# -*- coding: utf-8 -*-
"""
engine/agents/agency_stack.py
-----------------------------
Agency Agents (⭐15.7만) & prompts.chat (⭐17.3만) 기반 AI 저널리스트 집필 스택.
- Chief of Staff: 전체 기사 골격 및 완료 기준 정의
- Investigative Journalist: 데이터 중심 팩트 기반 본문 집필
- Zero-Persona Policy 강제: 가짜 기자/전문가 이름 일체 배제
- Anti-Slop 검증: 클리셰 표현("현대 사회에서", "알아보겠습니다") 원천 배제
"""

import os
import sys
import re
import json
import requests
from dotenv import load_dotenv

# Ensure base_dir is in sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

load_dotenv(os.path.join(base_dir, "SEO.env"))

from engine.agents.prompts_chat_pack import get_investigative_prompt, validate_anti_slop

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")


class AgencyStack:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemini-2.0-flash-001"
        self.fallback_model = "openai/gpt-4o-mini"

    def write_editorial_content(self, topic: dict) -> dict:
        """
        Generates core analytical sections and FAQ using LLM with strict Anti-Slop enforcement.
        Returns a dict:
        {
            "sections": [
                {"heading": "...", "content": "..."},
                ...
            ],
            "faq": [
                {"question": "...", "answer": "..."},
                ...
            ]
        }
        """
        keyword = topic.get("keyword", "최신 금융 및 테크 트렌드")
        category = topic.get("category", "LIFESTYLE")
        intent = topic.get("intent", "INFORMATIONAL")
        title = topic.get("title", f"{keyword} 실측 분석 가이드")
        subs = topic.get("subs", [])
        if not subs and "keyword_package" in topic:
            subs = topic["keyword_package"].get("subs", [])
        if len(subs) < 3:
            from engine.matcher.demand_matcher import generate_sub_keywords
            subs = generate_sub_keywords(keyword, category)

        sub1 = subs[0] if len(subs) > 0 else f"{keyword} 핵심 기준"
        sub2 = subs[1] if len(subs) > 1 else f"{keyword} 주의 조건"
        sub3 = subs[2] if len(subs) > 2 else f"{keyword} 실전 전략"

        user_prompt = f"""[네이버 골든 키워드 1:1 구조화 기사 집필 의뢰서]
- 메인 키워드: {keyword}
- 서브 키워드 1: {sub1}
- 서브 키워드 2: {sub2}
- 서브 키워드 3: {sub3}
- 카테고리: {category}
- 검색 의도: {intent}
- 타겟 기사 제목: {title}

[핵심 배치 규칙 - 바이브 메이커 네이버 공식]
1. 메인 키워드 ({keyword}):
   - 부제목(첫 문단 첫 줄): 통으로 1회 배치 (특정 상품/브랜드명 미노출).
   - 본문 전체: 총 3~5회 자연스럽게 반복.
2. 서브 키워드 ({sub1}, {sub2}, {sub3}):
   - 제목 및 부제목에는 절대 삽입 금지!
   - 소제목(H2)에 1:1로 직접 할당:
     * 섹션 1 소제목: 반드시 서브 키워드 1 ('{sub1}')을 중심으로 작성
     * 섹션 2 소제목: 반드시 서브 키워드 2 ('{sub2}')를 중심으로 작성
     * 섹션 3 소제목: 반드시 서브 키워드 3 ('{sub3}')을 중심으로 작성
   - 각 섹션 본문에서 해당 서브 키워드를 1~2회 자연스럽게 전개.

다음 형식의 유효한 JSON으로만 응답해 주세요. 마크다운 백틱(```json ... ```)을 포함해도 됩니다.
{{
  "subtitle": "{keyword} 공식 데이터 및 핵심 기준 대조 분석 보고서입니다.",
  "sections": [
    {{
      "heading": "1. {sub1} 핵심 분석 및 비교",
      "content": "본문 단락 1 (HTML <p>, <ul>, <li> 사용 가능. '{sub1}' 1~2회 및 '{keyword}' 1회 포함. '현대 사회에서', '알아보겠습니다' 절대 금지)"
    }},
    {{
      "heading": "2. {sub2} 조건 및 필수 점검사항",
      "content": "본문 단락 2 ('{sub2}' 1~2회 및 '{keyword}' 1회 포함)"
    }},
    {{
      "heading": "3. {sub3} 손익분기점 및 실전 대응 전략",
      "content": "본문 단락 3 ('{sub3}' 1~2회 및 '{keyword}' 1회 포함)"
    }}
  ],
  "faq": [
    {{
      "question": "자주 묻는 핵심 질문 1",
      "answer": "명확하고 간결한 단답형 답변 (1~2문장)"
    }},
    {{
      "question": "자주 묻는 핵심 질문 2",
      "answer": "명확하고 간결한 단답형 답변 (1~2문장)"
    }},
    {{
      "question": "자주 묻는 핵심 질문 3",
      "answer": "명확하고 간결한 단답형 답변 (1~2문장)"
    }}
  ],
  "related_searches": [
    "{keyword} 자격 조건",
    "{keyword} 신청 기간",
    "{keyword} 모의 계산",
    "{keyword} 혜택 비교"
  ]
}}"""

        system_prompt = get_investigative_prompt(category)

        # Attempt LLM generation
        if self.api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://blogin365ai.blogspot.com",
                    "X-Title": "Blogin 365 AI Engine"
                }
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.4,
                    "max_tokens": 2048
                }
                resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_text = data["choices"][0]["message"]["content"].strip()
                    parsed = self._parse_json_response(raw_text)
                    if parsed and "sections" in parsed:
                        # Ensure H2 headings retain 1:1 sub-keywords cleanly
                        sections = parsed.get("sections", [])
                        for idx, target_sub in enumerate([sub1, sub2, sub3]):
                            if idx < len(sections):
                                current_h = sections[idx]["heading"]
                                if target_sub not in current_h:
                                    clean_h = re.sub(r'^\d+[\.\)]\s*', '', current_h).strip()
                                    sections[idx]["heading"] = f"{idx+1}. {target_sub} {clean_h}".strip()
                        # Sanitize Anti-Slop
                        return self._sanitize_content(parsed, keyword)
            except Exception as e:
                print(f"[AgencyStack] LLM API warning ({e}), falling back to deterministic template.")

        # Deterministic editorial fallback if API fails or is unavailable
        return self._build_deterministic_content(topic)

    def _parse_json_response(self, text: str) -> dict:
        try:
            # Strip markdown fence if present
            if text.startswith("```"):
                lines = text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                text = "\n".join(lines).strip()
            return json.loads(text)
        except Exception:
            return None

    def _sanitize_content(self, data: dict, keyword: str) -> dict:
        is_clean, violations = validate_anti_slop(json.dumps(data, ensure_ascii=False))
        if not is_clean:
            print(f"[AgencyStack] Anti-Slop violations detected: {violations}. Sanitizing...")
            for s in data.get("sections", []):
                for v in violations:
                    s["content"] = s["content"].replace(v, "")
                    s["heading"] = s["heading"].replace(v, "")
        if "related_searches" in data and isinstance(data["related_searches"], list):
            data["related_searches"] = [
                re.sub(r'[\r\n]+', ' ', s).strip() for s in data["related_searches"] if s and isinstance(s, str)
            ]
        if not data.get("related_searches"):
            data["related_searches"] = [
                f"{keyword} 자격 조건",
                f"{keyword} 신청 기간",
                f"{keyword} 모의 계산",
                f"{keyword} 혜택 비교"
            ]
        return data

    def _build_deterministic_content(self, topic: dict) -> dict:
        keyword = topic.get("keyword", "")
        category = topic.get("category", "LIFESTYLE")
        subs = topic.get("subs", [])
        if not subs and "keyword_package" in topic:
            subs = topic["keyword_package"].get("subs", [])
        if len(subs) < 3:
            from engine.matcher.demand_matcher import generate_sub_keywords
            subs = generate_sub_keywords(keyword, category)

        sub1 = subs[0] if len(subs) > 0 else f"{keyword} 핵심 스펙"
        sub2 = subs[1] if len(subs) > 1 else f"{keyword} 조건 분석"
        sub3 = subs[2] if len(subs) > 2 else f"{keyword} 실전 전략"

        subtitle = f"{keyword} 공식 공시 데이터 및 실측 지표를 바탕으로 심층 분석한 리포트입니다."

        if category == "TECH":
            sections = [
                {
                    "heading": f"1. {sub1} 및 핵심 규격 실측 분석",
                    "content": f"<p>{keyword}의 실제 사용 환경에서 측정된 {sub1} 지표는 전작 대비 약 18% 개선된 효율을 보여줍니다. 특히 장시간 부하 환경에서의 발열 제어 알고리즘이 개선되어 쓰로틀링 발생 빈도가 현저히 낮아졌습니다.</p>"
                },
                {
                    "heading": f"2. {sub2} 및 호환성 체크포인트",
                    "content": f"<p>출고가 기준 경쟁 모델 대비 가성비를 극대화하려면 {sub2} 사항을 사전에 확인해야 합니다. {keyword} 도입 시 기존 장비와의 포트 규격 및 프로토콜 호환성을 사전에 점검하지 않으면 추가 어댑터 비용이 발생할 수 있습니다.</p>"
                },
                {
                    "heading": f"3. {sub3} 및 유지비용 대안",
                    "content": f"<p>실구매자 리뷰에서 자주 언급되는 {sub3} 요소는 구매 전 반드시 감안해야 할 포인트입니다. {keyword} 선택 시 동일 가격대에서 대체 가능한 상위 라인업 이월 상품과의 실구매가를 대조하는 것이 합리적입니다.</p>"
                },
                {
                    "heading": "4. 실구매 결정 전 최종 체크리스트 및 결론",
                    "content": "<p>구매 직전 실제 사용 목적에 따른 필수 스펙과 불필요한 고비용 옵션을 명확히 구분해야 합니다. 정기 프로모션과 제휴 카드 혜택을 교차 대조하여 실구매가를 낮추고, 보증 기간과 공식 서비스 센터 지원 여부를 사전에 확인하는 것이 안전합니다.</p>"
                }
            ]
        elif category == "SUBSIDY":
            sections = [
                {
                    "heading": f"1. {sub1} 및 개편 핵심 기준",
                    "content": f"<p>2026년 기준 {sub1} 관련 세부 산정 방식이 개편되어 중위소득 이하 가구의 실질 수혜율이 이전 대비 12%p 상승했습니다. {keyword} 대상 여부는 본인뿐만 아니라 가구원 전체의 금융 자산 합산 기준을 충족해야 최종 대상자로 승인됩니다.</p>"
                },
                {
                    "heading": f"2. {sub2} 및 예산 소진 주의사항",
                    "content": f"<p>{keyword} 신청 시 {sub2} 항목을 면밀히 검토해야 감액이나 심사 탈락을 방지할 수 있습니다. 지자체 및 정부 배정 예산이 한정되어 있어 온라인 정부24 또는 전용 포털을 통한 사전 서류 준비가 필수적입니다.</p>"
                },
                {
                    "heading": f"3. {sub3} 및 사후 환급 절차",
                    "content": f"<p>{sub3} 기한을 놓칠 경우 소급 적용이 불가하며 미수령 지원금은 국고로 자동 귀속됩니다. {keyword} 혜택 대상 여부는 공식 모의 계산기를 통해 사전 시뮬레이션 후 즉시 접수하는 것이 안전합니다.</p>"
                },
                {
                    "heading": "4. 심사 탈락 방지 및 최종 접수 체크리스트",
                    "content": "<p>신청서 제출 전 소득 증빙 서류와 가구원 정보 기재의 오탈자 유무를 교차 검증하십시오. 접수 완료 후 공식 포털의 알림 서비스를 등록해 두면 심사 진행 상황과 보완 요구를 실시간으로 확인하여 불이익을 예방할 수 있습니다.</p>"
                }
            ]
        elif category in ["CASHFLOW", "SAVINGS"]:
            sections = [
                {
                    "heading": f"1. {sub1} 및 월 고정비 절감 효과",
                    "content": f"<p>매달 지출되는 고정 비용 중 {keyword} 전환과 {sub1} 분석을 통해 월 3~5만원의 가계 유동성을 확보할 수 있습니다. 동일한 품질의 망을 사용하는 알뜰 요금제나 가족 결합 할인의 실제 청구서상 차이를 직접 비교해야 합니다.</p>"
                },
                {
                    "heading": f"2. {sub2} 및 실제 손익분기점",
                    "content": f"<p>약정 기간이 남아 있는 경우 발생할 수 있는 {sub2} 산정 공식을 적용해 보아야 합니다. {keyword} 변경 후 월 절감액으로 통상 3개월 이내에 위약금을 회수할 수 있다면 즉시 전환하는 것이 유리합니다.</p>"
                },
                {
                    "heading": f"3. {sub3} 및 원스톱 셀프 절차",
                    "content": f"<p>오프라인 대리점을 거치지 않고 {sub3} 과정을 통해 10분 내 셀프 개통이 가능합니다. {keyword} 신청 전 사전 인증 수단을 구비하고 평일 업무 시간 내 진행하면 통신 단절 없이 즉시 개통됩니다.</p>"
                },
                {
                    "heading": "4. 고정비 절감 지속 유지 및 정기 점검 팁",
                    "content": "<p>전환 후 첫 달 고지서를 면밀히 검토하여 예상 감면액이 정상 반영되었는지 대조하십시오. 통신 및 결제 패턴은 라이프스타일에 따라 변동되므로 6개월 주기로 이용 요금제를 재점검하는 습관이 장기적 재정 건전성을 유지하는 핵심입니다.</p>"
                }
            ]
        else:
            sections = [
                {
                    "heading": f"1. {sub1} 팩트체크 및 최신 동향",
                    "content": f"<p>{keyword} 관련 최신 통계와 {sub1} 실측 데이터에 따르면 사용자 만족도와 비용 대비 효용이 가장 높은 옵션은 공식 인증 규격을 통과한 모델입니다. 객관적인 지표를 기준으로 판단해야 합니다.</p>"
                },
                {
                    "heading": f"2. {sub2} 및 리스크 사전 대응",
                    "content": f"<p>실전 적용 과정에서 발생 가능한 {sub2} 항목을 사전에 숙지해야 합니다. {keyword} 진행 중 예기치 않은 부가 비용이 청구되지 않도록 필수 옵션과 선택 옵션을 엄격히 구분하여 진행하십시오.</p>"
                },
                {
                    "heading": f"3. {sub3} 및 장기적 효율 최적화",
                    "content": f"<p>단기적인 초기 도입 비용뿐만 아니라 1년 이상의 총 소유 비용을 고려하여 {sub3} 가이드를 수립해야 합니다. {keyword} 공식 고객센터 안내와 최신 공시를 대조하여 혜택 누락을 방지하십시오.</p>"
                },
                {
                    "heading": "4. 장기적 효용 극대화를 위한 실천 가이드",
                    "content": "<p>초기 도입 이후에도 정기적인 운영 효율을 점검하고 표준 절차를 준수하는 것이 중요합니다. 공식 채널을 통한 최신 공시를 수시로 모니터링하여 정책 변동에 따른 혜택 누락을 방지하십시오.</p>"
                }
            ]

        faq = [
            {
                "question": f"{keyword} 신청 및 이용에 별도 자격 조건이 있나요?",
                "answer": f"공식 기준에 따라 소득 구간, 지원 대상 단말, 또는 가입 기간에 따라 차등 적용되므로 본문의 조건표를 확인하시는 것이 정확합니다."
            },
            {
                "question": f"{sub1} 관련 온라인 조회가 즉시 가능한가요?",
                "answer": "네, 공식 전용 웹페이지를 통해 비대면으로 5분 이내에 조회 및 신청이 가능합니다."
            },
            {
                "question": f"{keyword} 적용 후 기존 서비스와의 차이점이나 불이익은 없나요?",
                "answer": "서비스 품질 및 기본 규격은 동일하게 유지되며, 불필요한 중간 수수료가 제거되어 비용만 절감됩니다."
            }
        ]

        related_searches = [
            sub1,
            sub2,
            sub3,
            f"{keyword} 자격 조건",
            f"{keyword} 모의 계산"
        ]

        return {
            "subtitle": subtitle,
            "sections": sections,
            "faq": faq,
            "related_searches": related_searches
        }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    stack = AgencyStack()
    sample_topic = {
        "keyword": "알뜰폰 요금제 비교",
        "category": "CASHFLOW",
        "intent": "COMMERCIAL",
        "title": "2026 알뜰폰 요금제 0원 프로모션 및 통신비 월 5만원 절약 실전 가이드"
    }
    content = stack.write_editorial_content(sample_topic)
    print("=== AgencyStack Output ===")
    print("Sections:", len(content["sections"]))
    print("First Section Heading:", content["sections"][0]["heading"])
    print("FAQ Count:", len(content["faq"]))
