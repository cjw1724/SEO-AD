# -*- coding: utf-8 -*-
"""
engine/agents/human_voice_engine.py
-----------------------------------
Human Voice & Conversational Copy Engine (Humanization Architecture Phase 3).
Injects authentic human rhythm, burstiness, colloquial transitions, and first-person
experiential anecdotes to break robotic AI writing patterns:
1. Personal Persona Engine (체험형 실측 내러티브 & 감정 소제목).
2. Burstiness & Colloquialization (어휘적 불규칙성, 단문-장문 리듬 교차, 구어체 최적화).
"""

import os
import sys
import re
import random
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class HumanVoiceEngine:
    """
    Transforms rigid, robotic AI text into natural, rhythmic human conversational prose.
    """

    HUMAN_TRANSITIONAL_PARTICLES = [
        "솔직히 말씀드리면,",
        "그런데 말이죠,",
        "의외로 많은 분들이 여기서 놓치는데,",
        "막상 직접 해보니까,",
        "처음에는 저도 반신반의했습니다.",
        "결론부터 짚고 넘어가자면,",
        "여기서 아주 중요한 팁이 하나 있습니다.",
        "생각보다 차이가 꽤 컸습니다."
    ]

    SHORT_BURST_PUNCHLINES = [
        "진짜였습니다.",
        "결론부터 말하면 확실합니다.",
        "이건 정말 의외였습니다.",
        "솔직히 좀 놀랐습니다.",
        "놓치면 무조건 손해입니다.",
        "여기가 핵심입니다."
    ]

    def __init__(self):
        pass

    def inject_burstiness_to_paragraphs(self, paragraph: str) -> str:
        """
        Injects rhythmic sentence-length variance (Burstiness):
        Combines ultra-short punchlines (10~15 chars) with thorough empirical explanations (55~85 chars)
        to prevent flat, monotonous AI sentence structures.
        """
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', paragraph) if s.strip()]
        if not sentences:
            return paragraph

        modified_sentences = []
        if len(sentences) >= 2:
            punch = random.choice(self.SHORT_BURST_PUNCHLINES)
            transition = random.choice(self.HUMAN_TRANSITIONAL_PARTICLES)

            for i, sent in enumerate(sentences):
                if i == 0:
                    modified_sentences.append(sent)
                    modified_sentences.append(f"<strong>{punch}</strong>")
                elif i == 1 and not sent.startswith(("하지만", "그러나", "그리고", "솔직히", "그런데")):
                    modified_sentences.append(f"{transition} {sent}")
                else:
                    modified_sentences.append(sent)
            return " ".join(modified_sentences)

        return paragraph

    def humanize_subheaders(self, sub_keyword: str, base_heading: str, index: int = 1) -> str:
        """
        Transforms dry subheaders into lively, curiosity-inducing casual headings
        while strictly preserving the 1:1 sub-keyword placement rule.
        """
        templates = [
            f"1달간 직접 겪어보고 알게 된 {sub_keyword}, 솔직한 실측 포인트",
            f"막상 해보니 여기서 다들 막힙니다: {sub_keyword} 핵심 체크",
            f"실제로 계산해보고 깜짝 놀란 {sub_keyword} 반전 결과",
            f"여기가 진짜 차별점이에요! {sub_keyword} 알짜배기 가이드",
            f"아무도 미리 안 알려줬던 {sub_keyword} 필수 주의사항"
        ]
        
        # Pick template that safely contains sub_keyword
        chosen = templates[(index - 1) % len(templates)]
        if sub_keyword not in chosen:
            chosen = f"{sub_keyword} - 에디토리얼 팀 실측 및 솔직 후기"
        return chosen

    def humanize_editorial_content(
        self,
        editorial_data: Dict[str, Any],
        sentiment_data: Optional[Dict[str, Any]] = None,
        factset_data: Optional[Dict[str, Any]] = None,
        sub_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Performs full humanization upgrade on agency editorial output:
        - Injects experiential 1st-person anecdotes
        - Injects real community raw quotes
        - Injects sentence-length burstiness
        - Upgrades subheaders with conversational curiosity hooks
        """
        sections = editorial_data.get("sections", [])
        humanized_sections = []

        raw_opinions = sentiment_data.get("raw_opinions", []) if sentiment_data else []
        anecdote = factset_data.get("failure_anecdote", "") if factset_data else ""
        pros = factset_data.get("pros_real", []) if factset_data else []
        cons = factset_data.get("cons_unfiltered", []) if factset_data else []

        for idx, sec in enumerate(sections):
            heading = sec.get("heading", "")
            sub_kw = sec.get("sub_keyword") or (sub_keywords[idx] if sub_keywords and idx < len(sub_keywords) else "")
            body = sec.get("content") or sec.get("body", "")

            # 1. Transform Subheader with conversational human tone (while keeping sub_kw)
            if sub_kw and sub_kw in heading:
                new_heading = self.humanize_subheaders(sub_kw, heading, index=idx + 1)
            else:
                new_heading = heading

            # 2. Inject Burstiness & colloquial transitions to paragraph
            new_body = self.inject_burstiness_to_paragraphs(body)

            # 3. In Section 1: Inject real-world community voice
            if idx == 0 and raw_opinions:
                quote_box = f"""
                <div style="margin: 16px 0; padding: 14px 18px; background: #f8fafc; border-left: 4px solid #64748b; border-radius: 6px; font-size: 13.5px; color: #334155; line-height: 1.6;">
                  💬 <strong>커뮤니티 실제 이용자들의 솔직한 반응:</strong><br>
                  <em>"{raw_opinions[0]}"</em>
                </div>
                """
                new_body = new_body + quote_box

            # 4. In Section 2: Inject team failure anecdote
            if idx == 1 and anecdote:
                anecdote_box = f"""
                <div style="margin: 16px 0; padding: 14px 18px; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 6px; font-size: 13.5px; color: #92400e; line-height: 1.6;">
                  ⚠️ <strong>에디토리얼 팀의 실제 시행착오:</strong> {anecdote}
                </div>
                """
                new_body = new_body + anecdote_box

            humanized_sections.append({
                **sec,
                "heading": new_heading,
                "sub_keyword": sub_kw,
                "body": new_body,
                "content": new_body
            })

        # Upgrade Subtitle / Lead
        old_subtitle = editorial_data.get("subtitle", "")
        if not old_subtitle and editorial_data.get("keyword"):
            old_subtitle = f"{editorial_data.get('keyword')} 공식 데이터 및 핵심 기준 대조 분석 보고서입니다."

        lead_burst = f"직접 3주간 테스트해본 결론부터 말씀드립니다. {old_subtitle}"

        return {
            **editorial_data,
            "subtitle": lead_burst,
            "sections": humanized_sections,
            "humanized": True
        }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    engine = HumanVoiceEngine()
    sample_paragraph = "청년도약계좌는 정부 기여금을 매칭해주는 정책 금융 상품입니다. 매월 최대 70만원을 납입할 수 있으며 연 6퍼센트 상당의 우대 금리를 제공합니다. 5년 만기 시 최대 5천만원의 목돈을 수령할 수 있습니다."
    upgraded = engine.inject_burstiness_to_paragraphs(sample_paragraph)
    print("=== Human Voice Engine Test ===")
    print("Original:", sample_paragraph)
    print("\nUpgraded:", upgraded)
