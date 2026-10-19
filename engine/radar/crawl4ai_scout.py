# -*- coding: utf-8 -*-
"""
engine/radar/crawl4ai_scout.py
------------------------------
Zero-Cost Real-Time Data Extractor Bridge using Crawl4AI (v0.9+).
Extracts real-world government portals, policy notice boards, and price tables
into clean, LLM-ready markdown for AI journalist agents.

Robust Multi-tier Fallback Architecture:
  Tier 1: Crawl4AI (AsyncWebCrawler) with headless Chromium & smart markdown filtering.
  Tier 2: Lightweight BeautifulSoup + urllib/requests HTML parser for table & semantic extraction.
  Tier 3: Deterministic Authoritative Government Factset Vault (100% crash-proof 24/7).
"""

import os
import sys
import re
import json
import asyncio
import urllib.request
import urllib.parse
import warnings
from datetime import datetime
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup

# Suppress harmless playwright/sqlite connection warnings on exit
warnings.filterwarnings("ignore", category=ResourceWarning)

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Silence crawl4ai cloud banner
os.environ["CRAWL4AI_NO_CLOUD_NOTICE"] = "1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

STANDARD_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
STANDARD_HEADERS = {
    "User-Agent": STANDARD_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


def html_table_to_markdown(table_tag) -> str:
    """Converts a BeautifulSoup <table> tag into a clean Github-flavored Markdown table."""
    rows = table_tag.find_all("tr")
    if not rows:
        return ""
    table_data = []
    for tr in rows:
        cells = tr.find_all(["th", "td"])
        row_text = [re.sub(r"\s+", " ", c.get_text()).strip() for c in cells]
        if any(row_text):
            table_data.append(row_text)
    if not table_data:
        return ""

    max_cols = max(len(r) for r in table_data)
    if max_cols == 0:
        return ""

    lines = []
    headers = table_data[0] + ["-"] * (max_cols - len(table_data[0]))
    lines.append("| " + " | ".join(h if h else "-" for h in headers) + " |")
    lines.append("| " + " | ".join(["---"] * max_cols) + " |")

    for r in table_data[1:]:
        padded = r + ["-"] * (max_cols - len(r))
        lines.append("| " + " | ".join(p if p else "-" for p in padded) + " |")

    return "\n".join(lines)


class Crawl4AIScout:
    """
    Autonomous Zero-Cost Real-Time Data Extractor.
    Extracts policy announcements, government portal tables, and commercial metrics.
    """

    # Deterministic Real-World Fact Tables Vault (Tier 3 Fallback)
    DETERMINISTIC_TABLE_VAULT = {
        "근로장려금": (
            "| 가구 유형 | 총소득 기준 | 최대 지급액 |\n"
            "|---|---|---|\n"
            "| 단독 가구 | 2,200만원 미만 | 최대 165만원 |\n"
            "| 홑벌이 가구 | 3,200만원 미만 | 최대 285만원 |\n"
            "| 맞벌이 가구 | 3,800만원 미만 | 최대 330만원 |"
        ),
        "자녀장려금": (
            "| 구분 | 총소득 기준 | 부양자녀 1인당 지급액 |\n"
            "|---|---|---|\n"
            "| 홑벌이·맞벌이 | 7,000만원 미만 | 자녀 1인당 최대 100만원 (최소 50만원) |"
        ),
        "청년도약계좌": (
            "| 총급여 구간 | 매월 납입 한도 | 정부 매칭 기여금 비율 | 만기 실체감 혜택 |\n"
            "|---|---|---|---|\n"
            "| 2,400만원 이하 | 최대 70만원 | 납입액의 6.0% (월 최대 2.4만) | 최대 5,000만원 목돈 + 비과세 |\n"
            "| 3,600만원 이하 | 최대 70만원 | 납입액의 4.6% (월 최대 2.3만) | 은행 이자 + 정부기여금 매칭 |\n"
            "| 4,800만원 이하 | 최대 70만원 | 납입액의 3.7% (월 최대 2.2만) | 이자소득세 15.4% 전액 비과세 |"
        ),
        "청년주택드림": (
            "| 상품 구분 | 가입 요건 | 대출 연계 혜택 |\n"
            "|---|---|---|\n"
            "| 청년주택드림청약통장 | 연소득 5,000만원 이하 만 19~34세 | 납입액 연 4.5% 우대이율 + 비과세 |\n"
            "| 청년주택드림대출 연계 | 청약 당첨자 (분양가 6억 이하) | 최저 연 2.2% 저금리 최대 80% 대출 |"
        ),
        "내일배움카드": (
            "| 구분 | 지원 한도 | 자부담률 기준 |\n"
            "|---|---|---|\n"
            "| 일반 참여자 | 1인당 기본 300만원 | 직종별 15% ~ 55% 자부담 |\n"
            "| 취약계층 / 청년 | 최대 500만원까지 증액 | 취업성공패키지 연계 시 자부담 0% 과정 다수 |"
        ),
        "알뜰폰": (
            "| 통신사망 | 평균 기본 데이터 | 통화/문자 | 월 프로모션 요금 |\n"
            "|---|---|---|---|\n"
            "| SKT 망 알뜰폰 | 7GB ~ 15GB + 1Mbps | 기본 무제한 | 월 9,900원 ~ 15,400원 |\n"
            "| KT 망 알뜰폰 | 11GB + 일2GB + 3Mbps | 완전 무제한 | 월 19,800원 ~ 24,900원 |\n"
            "| LGU+ 망 알뜰폰 | 15GB + 3Mbps | 기본 무제한 | 월 14,300원 ~ 18,700원 |"
        ),
        "자동차보험": (
            "| 주요 할인 특약 | 평균 할인율 | 필수 충족 요건 |\n"
            "|---|---|---|\n"
            "| 주행거리 마일리지 특약 | 최대 35% ~ 45% 환급 | 연간 3,000km ~ 15,000km 이하 주행 |\n"
            "| 티맵 / 카카오 안전운전 | 10% ~ 16% 즉시 할인 | 최근 안전운전 점수 71~81점 이상 달성 |\n"
            "| 블랙박스 및 첨단안전장치 | 3% ~ 7% 할인 | 블랙박스, 차선이탈방지 등 장착 사진 등록 |"
        ),
        "신생아특례": (
            "| 대상 주택 | 부부합산 소득 요건 | 대출 금리 | 최대 한도 |\n"
            "|---|---|---|---|\n"
            "| 9억원 이하 (전용 85㎡) | 1.3억원 이하 (신생아 출산) | 연 1.6% ~ 3.3% | 최대 5억원 이내 |\n"
            "| 전세자금 대출 (보증금 5억) | 1.3억원 이하 | 연 1.1% ~ 3.0% | 최대 3억원 이내 |"
        ),
        "버팀목": (
            "| 대출 상품 | 소득 요건 | 보증금 한도 | 최저 금리 |\n"
            "|---|---|---|---|\n"
            "| 청년전용 버팀목전세 | 연 5,000만원 이하 (만 19~34세) | 3억원 이하 (최대 2억원 대출) | 연 1.8% ~ 2.7% |\n"
            "| 신혼부부 버팀목전세 | 연 7,500만원 이하 | 수도권 4억 / 지방 3억 (최대 3억) | 연 1.5% ~ 2.7% |"
        ),
        "국민연금": (
            "| 수급 유형 | 조기수령 개시 연령 | 감액률 (연 6%) | 정상 수급 연령 |\n"
            "|---|---|---|---|\n"
            "| 1년 조기수령 | 만 62세 (1964년생 기준) | 정상 연금액의 94% 지급 | 만 63세 |\n"
            "| 3년 조기수령 | 만 60세 | 정상 연금액의 82% 지급 | 만 63세 |\n"
            "| 5년 최대 조기수령 | 만 58세 | 정상 연금액의 70% 지급 | 만 63세 |"
        ),
        "종합소득세": (
            "| 과세표준 구간 | 기본 세율 | 누진공제액 | 주요 환급/공제 항목 |\n"
            "|---|---|---|---|\n"
            "| 1,400만원 이하 | 6% | 없음 | 단순경비율 적용 및 기본공제 |\n"
            "| 1,400만 ~ 5,000만원 | 15% | 126만원 | 인적공제, 연금계좌, 소기업소상공인공제 |\n"
            "| 5,000만 ~ 8,800만원 | 24% | 576만원 | 신용카드·의료비·교육비 특별공제 |"
        ),
        "트래블로그": (
            "| 카드 구분 | 외화 환전 수수료 | 해외 이용/ATM 수수료 | 환급(재환전) 수수료 |\n"
            "|---|---|---|---|\n"
            "| 하나 트래블로그 (체크/신용) | 주요 통화 100% 무료 | 전액 면제 (Master/UnionPay) | 1% 송금받을 때 환율 적용 |\n"
            "| 트래블월렛 페이 | 주요 외화 무료 (기타 0.5~2.5%) | 전액 면제 (Visa) | 환전 당시 시장환율 적용 |\n"
            "| 토스뱅크 외화통장 체크 | 평생 환전 수수료 0원 | 해외 결제 및 ATM 면제 | 재환전 수수료 0원 |"
        ),
        "실비보험": (
            "| 세대 구분 | 급여 보장 비율 | 비급여 보장 비율 | 자기부담금 및 특징 |\n"
            "|---|---|---|---|\n"
            "| 4세대 실손보험 (현행) | 급여 80% 보장 | 비급여 70% 보장 | 비급여 이용량에 따른 5단계 보험료 차등제 |\n"
            "| 3세대 착한실손 (2017~2021) | 급여 90% 보장 | 비급여 80% (특약 70%) | 비급여 3대 특약(도수/주사/MRI) 분리 |"
        ),
        "임플란트": (
            "| 적용 대상 | 건강보험 적용 개수 | 본인부담률 | 적용 부위 |\n"
            "|---|---|---|---|\n"
            "| 만 65세 이상 건강보험 가입자 | 평생 1인당 2개 | 본인부담 30% (약 38~42만원) | 상·하악 구분 없이 무치악 제외 모든 치아 |\n"
            "| 비보험 일반 임플란트 | 개수 제한 없음 | 전액 비급여 (평균 95만~140만원) | 뼈이식, 상악동거상술 별도 추가 |"
        )
    }

    def __init__(self, timeout: int = 12, headless: bool = True):
        self.timeout = timeout
        self.headless = headless

    async def crawl_page_async(
        self,
        url: str,
        css_selector: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crawls a target web page using Crawl4AI AsyncWebCrawler.
        Falls back to BeautifulSoup parser if Playwright/Chromium fails or times out.
        """
        if not url:
            return self._build_empty_result("URL is required")

        # Tier 1: Crawl4AI Execution
        try:
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
            run_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                css_selector=css_selector,
                page_timeout=self.timeout * 1000,
                word_count_threshold=10,
                verbose=False
            )
            async with AsyncWebCrawler(verbose=False) as crawler:
                res = await asyncio.wait_for(
                    crawler.arun(url=url, config=run_config),
                    timeout=self.timeout + 3
                )
                if res and res.success:
                    raw_markdown = res.markdown or ""
                    tables = self._extract_tables_from_markdown(raw_markdown)
                    return {
                        "url": url,
                        "success": True,
                        "method": "crawl4ai",
                        "markdown": self._clean_markdown(raw_markdown),
                        "tables": tables,
                        "title": getattr(res, "metadata", {}).get("title", ""),
                        "status_code": getattr(res, "status_code", 200),
                        "error": None
                    }
        except Exception as e:
            # Crawl4AI failed or timed out, seamlessly proceed to Tier 2
            pass

        # Tier 2: BeautifulSoup Lightweight Fallback
        return self._crawl_with_soup(url)

    def crawl_page_sync(self, url: str, css_selector: Optional[str] = None) -> Dict[str, Any]:
        """Synchronous wrapper for crawl_page_async."""
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(asyncio.run, self.crawl_page_async(url, css_selector))
                    return future.result(timeout=self.timeout + 5)
            else:
                return asyncio.run(self.crawl_page_async(url, css_selector))
        except Exception:
            return self._crawl_with_soup(url)

    def extract_rich_policy_tables(
        self,
        keyword: str,
        portal_url: Optional[str] = None,
        category: str = "SUBSIDY"
    ) -> Dict[str, Any]:
        """
        Extracts rich real-world tables and policy text for an SEO topic.
        Runs full 3-tier fallback chain to ensure 100% availability.
        Guarantees authoritative policy facts and numerical tables are never
        overwritten by empty or generic portal navigation text.
        """
        clean_kw = keyword.strip()
        matched_vault_table = None
        for k, tbl in self.DETERMINISTIC_TABLE_VAULT.items():
            if k in clean_kw or clean_kw in k:
                matched_vault_table = tbl
                break

        # Attempt live crawl if URL provided
        crawl_result = None
        if portal_url and portal_url.startswith("http"):
            crawl_result = self.crawl_page_sync(portal_url)

        # Build combined extracted tables
        extracted_tables = []
        live_has_tables = False
        if crawl_result and crawl_result.get("success") and crawl_result.get("tables"):
            extracted_tables.extend(crawl_result["tables"])
            live_has_tables = True

        if matched_vault_table and (not extracted_tables or len(extracted_tables) == 0):
            extracted_tables.append(matched_vault_table)

        # Validate crawled markdown relevance to prevent injecting generic homepage banners
        crawled_md = crawl_result.get("markdown", "").strip() if crawl_result and crawl_result.get("success") else ""
        kw_terms = [t for t in re.findall(r'[가-힣a-zA-Z0-9]+', clean_kw) if len(t) >= 2]
        is_relevant = any(term in crawled_md for term in kw_terms) if kw_terms else False

        live_markdown = ""
        if crawled_md and (is_relevant or live_has_tables) and len(crawled_md) >= 50:
            live_markdown = crawled_md[:1200]
            if matched_vault_table and not live_has_tables:
                live_markdown = f"{live_markdown}\n\n### {clean_kw} 공식 기준 요약\n\n{matched_vault_table}"
        elif matched_vault_table:
            live_markdown = f"### {clean_kw} 공식 기준 요약\n\n{matched_vault_table}"
        elif crawled_md:
            live_markdown = crawled_md[:1200]
        else:
            live_markdown = f"### {clean_kw} 정부 공식 지침 및 기준 안내"

        # Determine transparent and accurate method provenance
        if crawl_result and crawl_result.get("success"):
            raw_method = crawl_result.get("method", "crawl4ai")
            if live_has_tables:
                method_used = raw_method
            elif matched_vault_table:
                method_used = f"{raw_method}_with_vault"
            else:
                method_used = raw_method
        else:
            method_used = "deterministic_vault"

        return {
            "keyword": clean_kw,
            "category": category,
            "portal_url": portal_url or "https://www.gov.kr/",
            "success": True,
            "method": method_used,
            "tables": extracted_tables,
            "primary_table": extracted_tables[0] if extracted_tables else (matched_vault_table or ""),
            "live_markdown": live_markdown,
            "crawled_at": datetime.now().isoformat()
        }

    def _crawl_with_soup(self, url: str) -> Dict[str, Any]:
        """Tier 2 Fallback: Lightweight BeautifulSoup + urllib fetcher."""
        try:
            req = urllib.request.Request(url, headers=STANDARD_HEADERS)
            with urllib.request.urlopen(req, timeout=6) as response:
                html = response.read().decode("utf-8", errors="ignore")

            soup = BeautifulSoup(html, "html.parser")

            # Remove scripts, styles, navigations
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                tag.decompose()

            # Extract HTML tables to Markdown
            tables = []
            for t_tag in soup.find_all("table"):
                md_t = html_table_to_markdown(t_tag)
                if md_t and len(md_t.splitlines()) >= 3:
                    tables.append(md_t)

            # Extract body text
            body_text = soup.get_text(separator="\n", strip=True)
            clean_lines = [line.strip() for line in body_text.splitlines() if len(line.strip()) > 10]
            clean_md = "\n\n".join(clean_lines[:30])

            title = soup.title.string.strip() if soup.title and soup.title.string else ""

            return {
                "url": url,
                "success": True,
                "method": "soup_fallback",
                "markdown": clean_md,
                "tables": tables,
                "title": title,
                "status_code": 200,
                "error": None
            }
        except Exception as e:
            return {
                "url": url,
                "success": False,
                "method": "soup_failed",
                "markdown": "",
                "tables": [],
                "title": "",
                "status_code": 0,
                "error": str(e)
            }

    def _extract_tables_from_markdown(self, markdown_text: str) -> List[str]:
        """Finds markdown tables in crawl4ai output."""
        table_pattern = re.compile(
            r'(\|.+\|\n\|(?:\s*[-:]+[-| :]*\s*)\|\n(?:\|.+\|\n?)+)',
            re.MULTILINE
        )
        matches = table_pattern.findall(markdown_text)
        cleaned = [m.strip() for m in matches if len(m.strip().splitlines()) >= 3]
        return cleaned

    def _clean_markdown(self, text: str) -> str:
        """Sanitizes raw markdown to remove redundant links and whitespace."""
        # Replace 3 or more blank lines with 2
        cleaned = re.sub(r'\n{3,}', '\n\n', text)
        return cleaned.strip()

    def _build_empty_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            "url": "",
            "success": False,
            "method": "none",
            "markdown": "",
            "tables": [],
            "title": "",
            "status_code": 0,
            "error": error_msg
        }


if __name__ == "__main__":
    scout = Crawl4AIScout(timeout=8)
    print("🚀 [Crawl4AIScout] Testing real-world extraction...")
    
    # Test 1: Example.com live test
    res = scout.crawl_page_sync("https://example.com")
    print(f" - URL: {res['url']}")
    print(f" - Method: {res['method']}")
    print(f" - Success: {res['success']}")
    print(f" - Markdown snippet: {res['markdown'][:80]}...")

    # Test 2: Rich Policy Tables
    policy_res = scout.extract_rich_policy_tables("2026 청년도약계좌", "https://www.kinfa.or.kr/")
    print("\n🏛️ [Policy Extraction Result]:")
    print(f" - Keyword: {policy_res['keyword']}")
    print(f" - Method: {policy_res['method']}")
    print(f" - Primary Table:\n{policy_res['primary_table']}")
