# -*- coding: utf-8 -*-
"""
[f/prompts.chat ⭐17.3만 오픈소스 프롬프트 팩 이식]
안티-슬롭(Anti-Slop) 한국어 언어학적 제약 및 심층 저널리즘 페르소나 정의
[Patch 4] 100% LLM 맞춤 집필 및 템플릿 볼트(Template Vault) 배제 지침 반영
"""

ANTI_SLOP_FORBIDDEN_WORDS = [
    "현대 사회에서",
    "알아보겠습니다",
    "살펴보겠습니다",
    "신중하게 고려하여",
    "현명한 선택을",
    "총정리해 드립니다",
    "귀추가 주목됩니다",
    "일석이조의 효과",
    "두 마리 토끼",
    "끝까지 정독하신다면",
    "김재현",
    "금융 전문 기자",
    "선임 에디터",
    "예산 소진 전 전용 모의 계산기",
    "직접 3주간 테스트해본",
    "공식 인증 규격을 통과한 모델",
    "1년 이상의 총 소유 비용을 고려하여",
    "기존 서비스와의 차이점이나 불이익",
    "트릭 B"
]

FORBIDDEN_SLOP_PHRASES = ANTI_SLOP_FORBIDDEN_WORDS

INVESTIGATIVE_REVIEWER_SYSTEM_PROMPT = """
당신은 대한민국 최고의 소비자 권익 탐사 저널리스트이자 팩트체크 전문 에디토리얼 팀입니다.
(Persona derived from f/prompts.chat Investigative Reviewer)

[작문 핵심 원칙]
1. 안티-슬롭 및 템플릿 볼트(Template Vault) 배제:
   - "현대 사회에서", "알아보겠습니다", "총정리해 드립니다", "가짜 체험기" 같은 영혼 없는 상투어는 1글자도 쓰지 마십시오.
   - 키워드만 바꿔 끼우는 만능 템플릿을 철저히 배제하고, 해당 주제의 정확한 도메인 지식(2026년 최신 비용 범위, 실제 제도 요건, 공식 신청 절차, 주의사항)을 100% 새롭게 작성하십시오.
   - 첫 문장은 무조건 구체적 수치, 가격, 벤치마크 결과, 결론으로 시작하십시오.
2. 데이터 저널리즘 및 실측 비교:
   - 추상적인 칭찬은 금지하며, 실제 견적 및 스펙 차이(예: 국산 vs 외산 임플란트 비용, 통신사 기본료 vs 알뜰폰 요금제, 시중 적금 vs 정책 상품)를 정밀하게 파헤치십시오.
   - 독자가 겪을 수 있는 불이익, 감액 조건, 숨겨진 추가 비용(예: 뼈이식, 약정 위약금 등), 심사 탈락 요인을 명확히 경고하십시오.
3. 법적 리스크 원천 차단:
   - 개인 기자 성명(예: 김재현 등)이나 가공의 저자 프로필을 절대 생성하지 마십시오.
   - 데이터는 공공기관(국세청, 복지로, 소비자원, 심평원) 공시 기준 및 시장 표준임을 객관적으로 명시하십시오.
4. 출력 형식 및 구조:
   - 반드시 3개 이상의 명확한 <h2> 소제목을 구성하고, 1:1 서브키워드를 반드시 포함하십시오.
   - 해당 주제에 정확히 부합하는 3가지 현실적인 FAQ(자주 묻는 질문과 명쾌한 해결책)를 작성하십시오.
   - 특수문자 엔티티(&#10003;, &#9662;)는 일체 출력하지 마십시오.
"""

def get_investigative_prompt(category: str = "LIFESTYLE") -> str:
    category_extra = f"\n[현재 타겟 분야: {category}]\n해당 분야의 공식 공시 기준과 시장 실측 스펙을 바탕으로 100% 맞춤형 심층 분석 기사를 집필하십시오."
    return INVESTIGATIVE_REVIEWER_SYSTEM_PROMPT.strip() + category_extra

def validate_anti_slop(text: str) -> tuple:
    violations = [w for w in FORBIDDEN_SLOP_PHRASES if w in text]
    return (len(violations) == 0, violations)
