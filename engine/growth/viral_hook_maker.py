# -*- coding: utf-8 -*-
"""
engine/growth/viral_hook_maker.py
---------------------------------
Every AI Marketer Role & Lazyowen Growth Loop Generator.
Generates:
1. 15-second high-hook viral Short/Reel script.
2. Instagram / Threads caption with ManyChat DM trigger ("댓글 10 남기시면 가이드 발송").
3. Auto-DM copy linking directly to the published post to bypass the 3-6 month Google sandbox.
"""

import os
import re
import json
from datetime import datetime


class ViralHookMaker:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
        else:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.queue_file = os.path.join(self.output_dir, "viral_growth_queue.json")

    def generate_hooks(self, topic: dict, post_url: str = "") -> dict:
        """
        Creates the complete social growth package for a published article.
        topic dict contains: keyword, category, title, pain_point, hook_summary, etc.
        """
        keyword = topic.get("keyword", "")
        category = topic.get("category", "LIFESTYLE")
        title = topic.get("title", f"{keyword} 핵심 가이드")
        
        kw_clean = re.sub(r'^(20\d\d년?|\d{4}년?)\s*', '', keyword).strip()
        kw_display = f"2026년 {kw_clean}" if not keyword.startswith("20") else keyword

        # Category-tailored hooks
        if category == "TECH":
            hook_lead = f"아직도 {keyword} 제값 다 주고 구매하시나요?"
            savings_stat = "체감 할인율 최대 28%"
            action_desc = "스펙 비교표와 최저가 혜택 조합"
        elif category == "SUBSIDY":
            hook_lead = f"{kw_display}, 신청 안 하면 전액 소멸됩니다."
            savings_stat = "1인당 평균 42만원 환급"
            action_desc = "30초 간편 자격 모의 조회기"
        elif category == "CASHFLOW":
            hook_lead = f"매달 새어나가는 고정비, {keyword} 하나로 월 10만원 아낍니다."
            savings_stat = "연간 고정비 120만원 절감"
            action_desc = "통신비·구독료 즉시 최적화 계산표"
        elif category == "WELLNESS":
            hook_lead = f"약국 가기 전 {keyword} 실구매자 후기부터 꼭 보세요."
            savings_stat = "핵심 성분 함량 대조 완료"
            action_desc = "식약처 기준 부작용 체크리스트"
        else:
            hook_lead = f"{kw_display}, 지금 모르면 손해 보는 3가지."
            savings_stat = "비용 절감 및 효율 극대화"
            action_desc = "공식 기준 대조 분석 보고서"

        reel_script = {
            "0-3초_후킹": f"[화면: 붉은 경고 뱃지 + 볼드 텍스트]\n🎙️ \"{hook_lead}\"",
            "3-10초_핵심내용": f"[화면: 인터랙티브 표와 시각 자료 빠르게 전개]\n🎙️ \"복잡한 약관 뒤질 필요 없이, {action_desc}로 {savings_stat} 결과를 바로 확인할 수 있습니다.\"",
            "10-15초_행동유도(CTA)": f"[화면: 댓글창 애니메이션 + '10' 입력 효과]\n🎙️ \"댓글에 숫자 '10'만 남겨주시면, 이 계산기와 상세 비교표 링크를 1초 만에 DM으로 보내드립니다!\""
        }

        sns_caption = f"""{hook_lead}

매번 찾으려면 번거롭고 어려운 {keyword}, 핵심만 압축해서 인터랙티브 계산기와 대조표로 정리했습니다.

📌 이번 가이드에 포함된 내용:
• {savings_stat} 실측 비교
• {action_desc}
• 공식 기관 및 실구매자 검증 기준

🎁 [가이드 & 계산기 즉시 받는 법]
댓글에 "10" 남겨주시면 설치나 가입 없이 바로 확인 가능한 링크를 DM으로 자동 발송해 드립니다.

#정보공유 #{keyword.replace(' ', '')} #생활꿀팁 #스마트라이프 #절약팁"""

        dm_copy = f"""안녕하세요! 요청하신 [{keyword}] 핵심 가이드와 모의 계산기 링크 보내드립니다.

🔗 즉시 확인하기:
{post_url or "https://blogin365ai.blogspot.com"}

(본 계산기는 복잡한 설치 없이 브라우저에서 바로 사용 가능합니다.)"""

        growth_package = {
            "keyword": keyword,
            "category": category,
            "title": title,
            "post_url": post_url,
            "created_at": datetime.now().isoformat(),
            "reel_script": reel_script,
            "sns_caption": sns_caption,
            "dm_copy": dm_copy
        }

        self._save_to_queue(growth_package)
        return growth_package

    def _save_to_queue(self, package: dict):
        current_data = []
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, "r", encoding="utf-8") as f:
                    current_data = json.load(f)
            except Exception:
                current_data = []
        
        current_data.insert(0, package)
        # Keep last 50 items
        current_data = current_data[:50]
        
        with open(self.queue_file, "w", encoding="utf-8") as f:
            json.dump(current_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    maker = ViralHookMaker()
    sample = {
        "keyword": "2026 청년도약계좌",
        "category": "SUBSIDY",
        "title": "2026 청년도약계좌 정부기여금 개편안 및 실제 만기 수령액 모의계산"
    }
    pkg = maker.generate_hooks(sample, "https://blogin365ai.blogspot.com/test-post.html")
    print("=== Marketer Growth Hook Generated ===")
    print("Reel Hook:", pkg["reel_script"]["0-3초_후킹"])
    print("DM Trigger:", "댓글에 10 남기시면 자동 발송")
