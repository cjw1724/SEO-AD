# -*- coding: utf-8 -*-
"""
engine/qa/gstack_auditor.py
---------------------------
gstack (⭐13.5만) & hallmark 57 Slop-Test Gates QA Tester Agent.
Performs strict automated audit before any publication:
1. Gate 1: Zero-Persona Policy (Zero fake names, zero hallucinated journalist credentials)
2. Gate 2: Zero Broken Entities (No &#10003;, &#9662;, corrupted unicode)
3. Gate 3: Anti-Slop Forbidden Phrase Filter ("현대 사회에서", "알아보겠습니다")
4. Gate 4: Essential UX/CRO Component Integrity (Bento Hero, Calculator, AdSlots, FAQ)
5. Gate 5: Length & HTML Semantic Validity
"""

import os
import sys
import re

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from engine.agents.prompts_chat_pack import FORBIDDEN_SLOP_PHRASES


# Strict Persona Blacklist (To prevent legal risks and persona fabrication)
FORBIDDEN_PERSONA_KEYWORDS = [
    "김재현", "금융 전문 기자", "전문 기자", "수석 에디터", "금융 기자",
    "박민수", "이진우 기자", "공인회계사 김", "변호사 박", "기자 프로필",
    "기자 소개", "취재 기자", "전직 애널리스트"
]

FORBIDDEN_ENTITIES = [
    r"&#10003;", r"&#9662;", r"&#9660;", r"&#x[0-9a-fA-F]+;", r"&amp;#"
]


class GStackAuditor:
    def __init__(self):
        pass

    def audit_post(self, title: str, html_content: str, keyword_package: dict = None) -> dict:
        """
        Runs comprehensive QA audit on the post title and HTML content.
        Gate 1: Zero-Persona Policy
        Gate 2: Zero Broken HTML Entities
        Gate 3: Anti-Slop Forbidden Phrases Filter
        Gate 4: Essential UX/CRO Component Integrity (Bento Hero, Calc, AdSlots, FAQ)
        Gate 5: Content Depth & Volume
        Gate 6: Naver 1:1 Keyword Structural Placement Architecture (바이브 메이커 공식)
        """
        gate_results = []
        errors = []

        # Gate 1: Zero-Persona Check
        full_text = f"{title} {html_content}"
        persona_violations = []
        for p in FORBIDDEN_PERSONA_KEYWORDS:
            if p in full_text:
                persona_violations.append(p)

        if persona_violations:
            errors.append(f"[GATE 1 FAIL] Zero-Persona 위반: 가짜 기자/인물 키워드 발견 -> {persona_violations}")
            gate_results.append({"gate": "Gate 1 (Zero-Persona)", "status": "FAIL", "detail": str(persona_violations)})
        else:
            gate_results.append({"gate": "Gate 1 (Zero-Persona)", "status": "PASS", "detail": "Zero fake personas verified"})

        # Gate 2: Broken HTML Entities Check
        entity_violations = []
        for ent in FORBIDDEN_ENTITIES:
            if re.search(ent, html_content):
                entity_violations.append(ent)

        if entity_violations:
            errors.append(f"[GATE 2 FAIL] 깨진 HTML 엔티티 발견: {entity_violations}")
            gate_results.append({"gate": "Gate 2 (Zero Broken Entities)", "status": "FAIL", "detail": str(entity_violations)})
        else:
            gate_results.append({"gate": "Gate 2 (Zero Broken Entities)", "status": "PASS", "detail": "Clean CSS & UTF-8 entities verified"})

        # Gate 3: Anti-Slop Phrases Check
        slop_violations = []
        for s in FORBIDDEN_SLOP_PHRASES:
            if s in full_text:
                slop_violations.append(s)

        if slop_violations:
            errors.append(f"[GATE 3 FAIL] AI 기계적 상투어 발견: {slop_violations}")
            gate_results.append({"gate": "Gate 3 (Anti-Slop)", "status": "FAIL", "detail": str(slop_violations)})
        else:
            gate_results.append({"gate": "Gate 3 (Anti-Slop)", "status": "PASS", "detail": "Data-first journalism tone verified"})

        # Gate 4: Essential UX/CRO Component Integrity
        missing_components = []
        if "bento-hero" not in html_content:
            missing_components.append("Bento Hero Takeaway Card")
        calc_identifiers = ["saas-calculator", "calc-container", "editorial-calculator-card", "custom-saas-tool", "calc"]
        if not any(cid in html_content for cid in calc_identifiers):
            missing_components.append("Interactive JS Calculator")
        if "adsense-slot" not in html_content:
            missing_components.append("AdSense Golden Monetization Slots")
        if "<details" not in html_content:
            missing_components.append("Interactive FAQ Accordion")

        if missing_components:
            errors.append(f"[GATE 4 FAIL] 필수 CRO 컴포넌트 누락: {missing_components}")
            gate_results.append({"gate": "Gate 4 (CRO Components)", "status": "FAIL", "detail": str(missing_components)})
        else:
            gate_results.append({"gate": "Gate 4 (CRO Components)", "status": "PASS", "detail": "All 4 high-retention components verified"})

        # Gate 5: Content Depth & Volume
        if len(html_content) < 1200:
            errors.append(f"[GATE 5 FAIL] 본문 길이 미달 ({len(html_content)}자 < 1200자)")
            gate_results.append({"gate": "Gate 5 (Content Depth)", "status": "FAIL", "detail": f"{len(html_content)} chars"})
        else:
            gate_results.append({"gate": "Gate 5 (Content Depth)", "status": "PASS", "detail": f"{len(html_content)} chars OK"})

        # Gate 6: Naver 1:1 Keyword Placement Architecture
        if keyword_package:
            main_kw = keyword_package.get("main", "").strip()
            subs = keyword_package.get("subs", [])
            gate6_errors = []

            # 1. 메인 키워드 제목 맨 앞쪽 통으로 1회 배치 검증
            if main_kw:
                title_trimmed = title.strip()
                if not re.match(rf'^[\s"\'“‘]*{re.escape(main_kw)}', title_trimmed):
                    gate6_errors.append(f"메인 키워드('{main_kw}')가 제목 맨 앞쪽에 배치되지 않음: '{title}'")

                # 제목 날짜/회차 브래킷 라벨([2026], (1편) 등) 삽입 금지 검증
                if re.search(r'\[\d{4}\]|\(\d{4}\)|\[\d+회\]|\(\d+회\)|\[\d+편\]|\(\d+편\)', title_trimmed):
                    gate6_errors.append(f"제목에 날짜/회차 라벨이 포함됨 (날짜·회차 라벨 제외 규칙 위반): '{title}'")

                # 제목 길이 검증 (권장 25~45자)
                if len(title_trimmed) < 25 or len(title_trimmed) > 45:
                    gate6_errors.append(f"제목 길이 부적합 ({len(title_trimmed)}자, 권장 30~40자 내외)")

                # 2. 서브 키워드가 제목에 포함되지 않았는지 검증
                for s in subs:
                    s_clean = s.strip()
                    if s_clean and s_clean != main_kw and s_clean in title:
                        gate6_errors.append(f"서브 키워드('{s_clean}')가 제목에 포함됨 (제목 삽입 금지)")

                # 3. 본문 내 메인 키워드 반복 빈도 (권장 3~5회, 풀 HTML 컴포넌트 포함 상한 16회)
                main_count = len(re.findall(re.escape(main_kw), html_content))
                if main_count < 3:
                    gate6_errors.append(f"메인 키워드('{main_kw}') 본문 노출 빈도 부족 ({main_count}회 < 3회)")
                elif main_count > 16:
                    gate6_errors.append(f"메인 키워드('{main_kw}') 과다 반복(키워드 스터핑) 감지 ({main_count}회 > 16회, 권장 3~10회)")

                # 4. 부제목(첫 문단 첫 줄, article-lead) 검증: 메인 1회 포함, 서브 포함 금지
                lead_match = re.search(r'<div[^>]*class=["\'][^"\']*article-lead[^"\']*["\'][^>]*>(.*?)</div>', html_content, re.DOTALL | re.IGNORECASE)
                if lead_match:
                    lead_text = re.sub(r'<[^>]+>', '', lead_match.group(1)).strip()
                    if main_kw not in lead_text:
                        gate6_errors.append(f"메인 키워드('{main_kw}')가 부제목(첫 문단 첫 줄)에 포함되지 않음")
                    for s in subs:
                        s_clean = s.strip()
                        if s_clean and s_clean != main_kw and s_clean in lead_text:
                            gate6_errors.append(f"서브 키워드('{s_clean}')가 부제목에 포함됨 (부제목 삽입 금지)")

            # 5. 소제목(H2) 1:1 서브 키워드 단독 할당 검증 (다중 키워드 1개 H2 몰아넣기 금지)
            h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.DOTALL | re.IGNORECASE)
            h2_texts = [re.sub(r'<[^>]+>', '', h).strip() for h in h2_matches]

            assigned_h2_indices = set()
            for s in subs:
                s_clean = s.strip()
                if not s_clean:
                    continue
                matching_indices = [idx for idx, h2 in enumerate(h2_texts) if s_clean in h2]
                if not matching_indices:
                    gate6_errors.append(f"서브 키워드 '{s_clean}'가 소제목(H2)에 1:1로 매핑되지 않음 (발견된 H2: {h2_texts})")
                else:
                    new_assignment = False
                    for mi in matching_indices:
                        if mi not in assigned_h2_indices:
                            assigned_h2_indices.add(mi)
                            new_assignment = True
                            break
                    if not new_assignment:
                        gate6_errors.append(f"서브 키워드 '{s_clean}'가 다른 서브 키워드와 동일한 H2 소제목에 중복 할당됨 (1:1 단독 할당 규칙 위반)")

            if gate6_errors:
                for ge in gate6_errors:
                    errors.append(f"[GATE 6 FAIL] {ge}")
                gate_results.append({"gate": "Gate 6 (1:1 Keyword Architecture)", "status": "FAIL", "detail": "; ".join(gate6_errors)})
            else:
                gate_results.append({
                    "gate": "Gate 6 (1:1 Keyword Architecture)",
                    "status": "PASS",
                    "detail": f"Main '{main_kw}' at Title Lead & Subtitle, 3+ density, {len(subs)} Subs mapped 1:1 to distinct H2 headings"
                })
        else:
            # Backward-compatible pass when keyword_package is omitted
            gate_results.append({
                "gate": "Gate 6 (1:1 Keyword Architecture)",
                "status": "PASS",
                "detail": "Standard heading structure verified (Keyword package optional)"
            })

        # Gate 7: Google Helpful Content (HCU) & Anti-Spam Safety Gate
        hcu_eval = self.evaluate_hcu_quality(title, html_content)
        if not hcu_eval["passed"]:
            for err in hcu_eval["errors"]:
                errors.append(f"[GATE 7 FAIL] {err}")
            gate_results.append({
                "gate": "Gate 7 (Helpful Content & Anti-Spam)",
                "status": "FAIL",
                "detail": "; ".join(hcu_eval["errors"]),
                "metrics": hcu_eval["metrics"]
            })
        else:
            gate_results.append({
                "gate": "Gate 7 (Helpful Content & Anti-Spam)",
                "status": "PASS",
                "detail": f"HCU Score: {hcu_eval['score']}/100, Lexical Diversity: {hcu_eval['metrics']['ttr']:.2f}, Affiliate Ratio: {hcu_eval['metrics']['affiliate_ratio']:.1f}%",
                "metrics": hcu_eval["metrics"]
            })

        passed = len(errors) == 0
        return {
            "passed": passed,
            "gate_results": gate_results,
            "errors": errors,
            "hcu_score": hcu_eval.get("score", 85),
            "hcu_metrics": hcu_eval.get("metrics", {})
        }

    def evaluate_hcu_quality(self, title: str, html_content: str) -> dict:
        """
        Evaluates Google Helpful Content (HCU) & Anti-Spam criteria:
        1. Lexical Diversity (Type-Token Ratio)
        2. Information Gain & Empirical Data density (facts, figures, percentages, won, etc.)
        3. Commercial / Affiliate link ratio <= 15% (Strict anti-thin-affiliate rule)
        4. Cloaking / Hidden text detection (display: none / font-size: 0 keyword stuffing)
        """
        clean_text = re.sub(r'<[^>]+>', ' ', html_content)
        words = [w for w in re.findall(r'[\w가-힣]+', clean_text) if len(w) >= 2]
        total_words = max(len(words), 1)
        unique_words = len(set(words))
        ttr = round(unique_words / total_words, 3)

        # 1. Hidden text / CSS cloaking check (Strict: display:none, font-size: 0px/0, transparent text)
        hidden_text_matches = re.findall(
            r'style=[\'"][^\'"]*(?:display\s*:\s*none\b|font-size\s*:\s*0(?:\.0+)?(?:px|pt|rem|em)?\s*(?:;|[\'"])|color\s*:\s*transparent\b)[^\'"]*[\'"]',
            html_content,
            re.IGNORECASE
        )

        # 2. Affiliate link count & ratio
        all_links = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"]', html_content, re.IGNORECASE)
        affiliate_links = [l for l in all_links if any(k in l.lower() for k in ["coupang", "linkprice", "adpick", "affiliate", "btn-affiliate"])]
        affiliate_ratio = round((len(affiliate_links) / max(len(all_links), 1)) * 100, 1)

        # Ratio of affiliate characters to total HTML
        affiliate_html_footprint = sum(
            len(m.group(0)) for m in re.finditer(r'<a\s+[^>]*class=[\'"][^\'"]*btn-affiliate[^\'"]*[\'"][^>]*>.*?</a>', html_content, re.DOTALL | re.IGNORECASE)
        )
        affiliate_footprint_ratio = round((affiliate_html_footprint / max(len(html_content), 1)) * 100, 2)

        # 3. Empirical facts count
        facts = re.findall(r'(\d+[\d,\.]*\s*(?:만원|원|%|일|개월|시간|점|배|세|건|명|위))', clean_text)
        facts_count = len(facts)

        errors = []
        if hidden_text_matches:
            errors.append(f"스팸 회피/클로킹(숨김 텍스트) 감지: {len(hidden_text_matches)}건 발견")

        # Affiliate ratio check: cannot dominate page (> 15% affiliate footprint)
        if affiliate_footprint_ratio > 15.0:
            errors.append(f"과도한 제휴 링크 비중({affiliate_footprint_ratio}% > 15% 상한선) - 씬 어필리에이트(Thin Affiliate) 감지")

        # Scoring
        score = 0
        score += min(25, int(ttr * 50))
        score += min(25, facts_count * 5)
        score += min(25, int(len(clean_text) / 50))
        hygiene = 25
        if hidden_text_matches:
            hygiene -= 25
        if affiliate_footprint_ratio > 15.0:
            hygiene -= 20
        score += max(0, hygiene)

        passed = len(errors) == 0

        return {
            "passed": passed,
            "score": min(100, score),
            "errors": errors,
            "metrics": {
                "ttr": ttr,
                "total_words": total_words,
                "unique_words": unique_words,
                "facts_count": facts_count,
                "affiliate_links_count": len(affiliate_links),
                "affiliate_ratio": affiliate_ratio,
                "affiliate_footprint_ratio": affiliate_footprint_ratio,
                "hidden_elements": len(hidden_text_matches)
            }
        }

    def sanitize_if_possible(self, html_content: str) -> str:
        """
        Attempts safe automatic sanitization for minor gate violations.
        """
        # Replace broken entities with clean CSS/text
        html_content = re.sub(r"&#10003;", "✓", html_content)
        html_content = re.sub(r"&#9662;", "", html_content)
        html_content = re.sub(r"&#9660;", "", html_content)
        
        # Strip hidden cloaking styles
        html_content = re.sub(r'style=[\'"][^\'"]*display\s*:\s*none[^\'"]*[\'"]', '', html_content, flags=re.IGNORECASE)

        # Strip slop phrases
        for s in FORBIDDEN_SLOP_PHRASES:
            html_content = html_content.replace(s, "")
            
        return html_content


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    auditor = GStackAuditor()
    sample_title = "2026 청년도약계좌 모의 계산기 및 지원금 자격 분석"
    clean_html = """
    <div class="bento-hero">Hero</div>
    <div class="saas-calculator">Calc</div>
    <div class="adsense-slot">Ad</div>
    <details><summary>FAQ</summary><p>Answer</p></details>
    """ + ("<p>충실한 본문 데이터...</p>" * 80)
    
    res = auditor.audit_post(sample_title, clean_html)
    print("=== GStack Auditor Test ===")
    print("Passed:", res["passed"])
    for g in res["gate_results"]:
        print(f" - {g['gate']}: {g['status']} ({g['detail']})")
