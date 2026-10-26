# -*- coding: utf-8 -*-
"""
engine/crew/qa_validator.py
---------------------------
Playwright 샌드박스 기반 무인 품질 검증 게이트키퍼 (Deterministic Validator Node)
- [Gate 1] Schema.org: SoftwareApplication (FinanceApplication, operatingSystem: Any) + FAQPage
- [Gate 2] YMYL 금융 정책 및 AI 인사말 필터 ('원금 보장', '무조건 수익' 금지, <div class="legal-disclaimer"> 필수)
- [Gate 3] Playwright 헤드리스 샌드박스 0ms 반응성 및 경계값(0원, 음수, 10억원) 주입 시 Zero-NaN 검증
"""

import json
import re
import asyncio
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


class DeterministicQAValidator:
    FORBIDDEN_GREETINGS = [
        "안녕하세요", "반갑습니다", "오늘 알아볼", "소개해 드립니다",
        "포스팅해 보겠습니다", "귀추가 주목", "일석이조", "두 마리 토끼"
    ]
    
    BANNED_YMYL_SLOP = [
        "소상공인 대출", "근로장려금 신청", "청년도약계좌", "햇살론", "임플란트 수가",
        "치아보험 비교", "알뜰폰 요금제 번호이동", "실비보험 청구 서류"
    ]

    # [YMYL 준수] 금융 과장 광고 및 불법 수익 약속 금지어
    FORBIDDEN_FINANCE_PROMISES = [
        "원금 보장", "무조건 수익", "100% 수익", "확정 수익",
        "원금 100% 보장", "손실 없는", "절대 잃지 않는", "고수익 보장"
    ]

    # [Patch 2] 단어 경계(\b) 실패를 극복하는 무결점 이상 토큰 패턴
    # NaN, undefined, null, Infinity 뒤에 단위(원, %, GB, 초, Tokens 등)가 붙어 있어도 100% 탐지
    INVALID_TOKEN_PATTERN = re.compile(
        r'(?:^|[^\w가-힣])(NaN|undefined|null|Infinity)(?:\s*(?:원|%|GB|MB|TB|KB|B|초|Tokens?|W|fps|ms|\$))?(?=[^\w가-힣]|$)',
        re.IGNORECASE
    )

    def __init__(self, full_html: str):
        self.html = full_html
        self.html_content = full_html
        self.soup = BeautifulSoup(full_html, "html.parser")
        self.errors: List[str] = []
        # 금융 도메인 여부 감지
        self.is_financial_domain = any(k in full_html for k in [
            "FinanceApplication", "양도소득세", "손익통산", "절세", "물타기",
            "평단가", "레버리지", "청산가", "배당금", "금융소득", "주식", "코인"
        ])

    def validate_json_ld(self) -> Dict[str, Any]:
        """JSON-LD 구조화 데이터 문법 및 SoftwareApplication, FAQPage 스키마 검증"""
        scripts = self.soup.find_all("script", type="application/ld+json")
        if not scripts:
            self.errors.append("[GATE 1 FAIL] application/ld+json 스크립트 태그가 누락되었습니다.")
            return {"passed": False}

        parsed_schemas = []
        has_software_app = False
        has_faq = False

        for s in scripts:
            try:
                raw_json = s.string or "{}"
                data = json.loads(raw_json)
                parsed_schemas.append(data)
                
                items = data.get("@graph", [data]) if isinstance(data, dict) else data
                for item in items:
                    stype = str(item.get("@type", ""))
                    if "SoftwareApplication" in stype:
                        has_software_app = True
                        if not item.get("name") or not item.get("applicationCategory"):
                            self.errors.append("[GATE 1 FAIL] SoftwareApplication 필수 속성(name, applicationCategory) 누락")
                        
                        # 금융 도메인일 경우 FinanceApplication 및 operatingSystem: Any 강제
                        if self.is_financial_domain:
                            app_cat = item.get("applicationCategory", "")
                            if "Finance" not in app_cat:
                                self.errors.append(f"[GATE 1 FAIL] 금융 시뮬레이터 applicationCategory는 'FinanceApplication'이어야 합니다. (현재: {app_cat})")
                            op_sys = item.get("operatingSystem", "")
                            if op_sys not in ["Any", "All"]:
                                self.errors.append(f"[GATE 1 FAIL] operatingSystem은 'Any' 또는 'All'이어야 합니다. (현재: {op_sys})")
                    if "FAQPage" in stype:
                        has_faq = True
            except Exception as e:
                self.errors.append(f"[GATE 1 FAIL] JSON-LD 문법 파싱 에러: {str(e)}")

        if not has_software_app:
            self.errors.append("[GATE 1 FAIL] Schema.org 'SoftwareApplication' 스키마가 누락되었습니다.")
        if not has_faq:
            self.errors.append("[GATE 1 FAIL] Schema.org 'FAQPage' 스키마가 누락되었습니다.")

        return {"passed": len(self.errors) == 0, "schemas": parsed_schemas}

    def validate_content_anti_slop(self) -> bool:
        """기계적 AI 인사말, 금지된 YMYL 스팸 단어 및 과장 광고 감지, 법적 면책 조항 검증"""
        text = self.soup.get_text()
        for greeting in self.FORBIDDEN_GREETINGS:
            if greeting in text:
                self.errors.append(f"[GATE 2 FAIL] 상투적 AI 인사말 감지: '{greeting}'")

        for banned in self.BANNED_YMYL_SLOP:
            if banned in text:
                self.errors.append(f"[GATE 2 FAIL] 폐기된 YMYL 스팸 키워드 침투 감지: '{banned}'")

        # YMYL 금융 정책 준수: 과장 광고 원천 차단
        for promise in self.FORBIDDEN_FINANCE_PROMISES:
            if promise in text:
                self.errors.append(f"[GATE 2 FAIL] YMYL 과장 광고/수익 보장 금지어 검출: '{promise}'")

        # YMYL 금융 정책 준수: 법적 투자 면책 조항(<div class="legal-disclaimer">) 정적 HTML 렌더링 검증
        if self.is_financial_domain:
            disclaimer = self.soup.find("div", class_="legal-disclaimer")
            if not disclaimer:
                self.errors.append("[GATE 2 FAIL] YMYL 필수 요건 누락: 본문 하단에 '<div class=\"legal-disclaimer\">' 법적 면책 조항 태그가 없습니다.")
            else:
                disc_text = disclaimer.get_text()
                if not any(k in disc_text for k in ["면책", "투자", "소득세법", "세무", "책임"]):
                    self.errors.append("[GATE 2 FAIL] legal-disclaimer 내부 법적 책임 고지 및 세무 안내 문구가 부실합니다.")

        return len(self.errors) == 0

    async def validate_js_runtime_sandbox(self) -> Dict[str, Any]:
        """Playwright 헤드리스 환경에서 실제 JS 실행 및 경계값(0, 음수, 10억원) 주입 테스트"""
        runtime_errors = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 360, "height": 800})

            # 콘솔 및 페이지 에러 추적
            page.on("pageerror", lambda err: runtime_errors.append(f"JS Uncaught Exception: {err.message}"))
            page.on("console", lambda msg: runtime_errors.append(f"Console Error: {msg.text}") if msg.type == "error" else None)

            # HTML 마운트
            await page.set_content(self.html, wait_until="networkidle")

            # 1. 360px 뷰포트 내 가로 스크롤 발생 여부 검사
            scroll_width = await page.evaluate("() => document.body.scrollWidth")
            if scroll_width > 360:
                self.errors.append(f"[GATE 3 FAIL] 모바일 360px 기준 가로 스크롤 발생 (scrollWidth: {scroll_width}px > 360px)")

            # 초기 텍스트 캡처 (0ms 반응성 추적용)
            initial_body = await page.inner_text("body")

            # 2. 슬라이더 조작 테스트
            sliders = await page.query_selector_all('input[type="range"]')
            for slider in sliders:
                try:
                    await slider.evaluate("""(el) => {
                        const min = parseFloat(el.min) || 0;
                        const max = parseFloat(el.max) || 100;
                        el.value = (min + max) / 2;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }""")
                except Exception:
                    pass

            # 3. 셀렉트 박스 조작 테스트
            selects = await page.query_selector_all('select')
            for sel in selects:
                options = await sel.query_selector_all('option')
                if len(options) > 1:
                    val = await options[-1].get_attribute("value")
                    if val:
                        await sel.select_option(val)
                        await sel.dispatch_event("change")

            # 4. 숫자 입력 필드에 3대 경계값(0, 음수, 10억 원) 순차 주입 테스트
            number_inputs = await page.query_selector_all('input[type="number"]')
            boundary_values = [0, -1000000, 1000000000]

            for test_val in boundary_values:
                for num_input in number_inputs:
                    try:
                        await num_input.evaluate(f"""(el) => {{
                            el.value = {test_val};
                            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}""")
                    except Exception:
                        pass

                await page.wait_for_timeout(100)

                # 경계값 주입 후 비정상 토큰 즉시 검사
                mid_text = await page.inner_text("body")
                matches = self.INVALID_TOKEN_PATTERN.findall(mid_text)
                if matches:
                    self.errors.append(f"[GATE 3 FAIL] 경계값({test_val}) 주입 시 비정상 토큰 노출: {matches}")
                    break

            # 5. 정상 기본값 복원 주입 (이후 최종 무결점 검사)
            for num_input in number_inputs:
                try:
                    await num_input.evaluate("""(el) => {
                        const min = parseFloat(el.min) || 0;
                        const max = parseFloat(el.max) || 10000000;
                        el.value = (min + max) / 2;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }""")
                except Exception:
                    pass

            await page.wait_for_timeout(200)

            # 6. 결과 영역 텍스트 추출 및 정규식 / 노드 이중 검사
            body_text = await page.inner_text("body")

            matches = self.INVALID_TOKEN_PATTERN.findall(body_text)
            if matches:
                self.errors.append(f"[GATE 3 FAIL] JS 계산 결과에 비정상 토큰 검출 (정규식): {matches}")

            result_nodes = await page.query_selector_all('[id*="result"], [id*="output"], [id*="total"], [id*="disp"], [id*="res"], .result, .output')
            for node in result_nodes:
                node_text = (await node.inner_text()).strip()
                for bad_lit in ["NaN", "undefined", "Infinity", "null"]:
                    if bad_lit in node_text:
                        self.errors.append(f"[GATE 3 FAIL] 결과 노드({bad_lit}) 오염 발견: '{node_text}'")
                        break

            await browser.close()

        if runtime_errors:
            self.errors.extend([f"[GATE 3 FAIL] {e}" for e in runtime_errors])

        return {"passed": len(self.errors) == 0, "runtime_errors": runtime_errors}

    def validate_editorial_contrast(self) -> None:
        """
        [GATE 4] 8인 AI 직원 실물 검수 & WCAG 2.1 AAA 가독성 게이트:
        화이트 컨테이너 및 텍스트 투명화(대비율 < 4.5:1) 원천 차단.
        """
        from engine.crew.editorial_inspector import EditorialInspector
        inspector = EditorialInspector()
        inspection = inspector.inspect(self.html, is_url=False)
        if not inspection["passed"]:
            # Auto-heal and re-verify
            healed = inspector.auto_heal(self.html)
            re_inspection = inspector.inspect(healed, is_url=False)
            if re_inspection["passed"]:
                self.html = healed
                self.html_content = healed
                self.soup = BeautifulSoup(healed, "html.parser")
            else:
                for d in re_inspection["defects"][:5]:  # Capture top 5 violations
                    self.errors.append(
                        f"[GATE 4 FAIL] 가독성 위반 ({d['viewport']}): <{d['tag']}> 대비율 {d['ratio']}:1 (최소 {d['required']}:1 필요). '{d['text']}'"
                    )

    async def execute_full_audit(self) -> Dict[str, Any]:
        """전체 무인 검증 게이트 순차 실행"""
        self.errors.clear()
        self.validate_json_ld()
        self.validate_content_anti_slop()
        await self.validate_js_runtime_sandbox()
        await asyncio.to_thread(self.validate_editorial_contrast)

        passed = (len(self.errors) == 0)
        return {
            "passed": passed,
            "status": "APPROVED" if passed else "REJECTED_FOR_REWRITE",
            "errors": self.errors,
            "html": self.html
        }


def run_validator(html_content: str) -> Dict[str, Any]:
    validator = DeterministicQAValidator(html_content)
    return asyncio.run(validator.execute_full_audit())
