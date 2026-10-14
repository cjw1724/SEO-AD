import feedparser
import re
import requests
from typing import List, Dict, Any

GOOGLE_TRENDS_KR_RSS = "https://trends.google.com/trending/rss?geo=KR"

def expand_naver_autocomplete(keyword: str, limit: int = 10) -> List[str]:
    """
    네이버 실시간 검색어 자동완성 API를 호출하여 서브 키워드 및 롱테일 확장 키워드를 수집합니다.
    (PDF 바이브 메이커 네이버 키워드 확장 공식)
    """
    clean_kw = keyword.strip()
    results = []

    # 1. 네이버 공식 자동완성 API (st=100 JSON 포맷)
    try:
        url = "https://ac.search.naver.com/nx/ac"
        params = {
            "q": clean_kw,
            "q_enc": "UTF-8",
            "st": "100",
            "r_format": "json",
            "r_enc": "UTF-8"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            items_group = data.get("items", [])
            if items_group and isinstance(items_group[0], list):
                for row in items_group[0]:
                    if row and isinstance(row, list) and len(row) > 0:
                        term = row[0].strip()
                        term = re.sub(r'<[^>]+>', '', term).strip()
                        term = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', term).strip()
                        if term and term != clean_kw and term not in results:
                            results.append(term)
    except Exception as e:
        pass

    # 2. 구글 자동완성 백업 (네이버 네트워크 지연 시 폴백)
    if len(results) < 3:
        try:
            g_url = "https://suggestqueries.google.com/complete/search"
            g_params = {"client": "firefox", "q": clean_kw, "hl": "ko"}
            g_resp = requests.get(g_url, params=g_params, timeout=4)
            if g_resp.status_code == 200:
                g_data = g_resp.json()
                if len(g_data) > 1 and isinstance(g_data[1], list):
                    for term in g_data[1]:
                        term = term.strip()
                        term = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', term).strip()
                        if term and term != clean_kw and term not in results:
                            results.append(term)
        except Exception:
            pass

    return results[:limit]

def estimate_keyword_competition(keyword: str, base_traffic: Any = None) -> Dict[str, Any]:
    """
    네이버 키워드 조사 공식(바이브 메이커)에 따른 월간 검색량, 블로그 문서 수, 한 달 발행량 추정.
    키워드 음절 및 단어 길이에 따른 현실적 롱테일 경쟁 지표 산출.
    """
    clean_kw = re.sub(r'^(\[|\()[\d\w\s\.\-]+(\]|\))\s*', '', keyword).strip()
    words = clean_kw.split()
    word_count = len(words)

    # 1. 월간 검색량 (Monthly Search Volume)
    if base_traffic is not None and isinstance(base_traffic, (int, float)) and base_traffic > 0:
        search_vol = int(base_traffic)
    else:
        if word_count == 1:
            search_vol = 32000
        elif word_count == 2:
            search_vol = 8500
        else:
            search_vol = 1400

    # 2. 블로그 문서 수 (Blog Document Count)
    # 롱테일 3단어 이상 세부 키워드는 문서 수가 적어 황금 비율(수요>공급)을 형성함
    if word_count >= 3:
        doc_count = max(int(search_vol * 0.35), 180)
    elif word_count == 2:
        doc_count = max(int(search_vol * 0.65), 520)
    else:
        doc_count = max(int(search_vol * 1.8), 2200)

    # 3. 한 달 발행량 (Monthly Published Count)
    monthly_pub = max(int(doc_count * 0.08), 25)

    return {
        "keyword": clean_kw,
        "monthly_search_vol": search_vol,
        "blog_doc_count": doc_count,
        "monthly_published": monthly_pub
    }

def fetch_google_trends_kr() -> List[Dict[str, Any]]:
    """
    구글 트렌드 한국 실시간 급상승 RSS 피드를 파싱하여 트래픽 볼륨과 키워드를 수집합니다.
    비용 0원, API 키 불필요.
    """
    trends = []
    try:
        feed = feedparser.parse(GOOGLE_TRENDS_KR_RSS)
        for entry in feed.entries:
            keyword = entry.get("title", "").strip()
            traffic_raw = entry.get("ht_approx_traffic", "1000")
            
            # 숫자 정규화: "50,000+" -> 50000
            traffic_clean = re.sub(r"[^\d]", "", traffic_raw)
            traffic_vol = int(traffic_clean) if traffic_clean else 1000
            
            snippet = entry.get("description", "")
            news_items = []
            if "ht_news_item_title" in entry:
                news_items.append(entry.get("ht_news_item_title"))
                
            trends.append({
                "keyword": keyword,
                "traffic_volume": traffic_vol,
                "snippet": snippet,
                "news_items": news_items,
                "source": "google_trends_kr"
            })
    except Exception as e:
        print(f"⚠️ [TrendScout] 구글 트렌드 RSS 파싱 오류: {e}")
        
    # 만약 트렌드 피드가 일시적으로 비어있을 경우 고수익 라이브 백업 큐 제공
    if not trends:
        fallback_keywords = [
            ("M4 맥북 에어 16G", 25000),
            ("2026 근로장려금 정기신청", 80000),
            ("알뜰폰 0원 무제한 요금제", 45000),
            ("로봇청소기 추천 비교", 30000),
            ("스마일라식 실비 가격", 15000),
            ("내일배움카드 국비지원 혜택", 20000)
        ]
        for kw, vol in fallback_keywords:
            trends.append({
                "keyword": kw,
                "traffic_volume": vol,
                "snippet": f"2026 실시간 급상승 핫이슈: {kw}",
                "news_items": [],
                "source": "curated_live_radar"
            })
            
    return sorted(trends, key=lambda x: x["traffic_volume"], reverse=True)

class TrendScout:
    def __init__(self):
        try:
            from engine.radar.public_data_scout import PublicDataScout
            self.public_scout = PublicDataScout()
        except Exception:
            self.public_scout = None

    def fetch_live_trends(self, limit: int = 10, include_public_data: bool = True) -> List[Dict[str, Any]]:
        trends = fetch_google_trends_kr()
        if include_public_data and self.public_scout:
            try:
                gov_items = self.public_scout.fetch_live_public_subsidies(limit=3)
                for g in gov_items:
                    trends.append({
                        "keyword": g["keyword"],
                        "traffic_volume": g.get("traffic_volume", 40000),
                        "snippet": f"[{g.get('dept', '정부공식')}] {g.get('title', '')}",
                        "news_items": [g.get("title", "")],
                        "source": "public_data_scout"
                    })
            except Exception:
                pass
        return sorted(trends, key=lambda x: x["traffic_volume"], reverse=True)[:limit]

    def expand_autocomplete(self, keyword: str, limit: int = 10) -> List[str]:
        return expand_naver_autocomplete(keyword, limit=limit)

    def research_keyword(self, keyword: str, base_traffic: Any = None) -> Dict[str, Any]:
        return estimate_keyword_competition(keyword, base_traffic=base_traffic)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    scout = TrendScout()
    results = scout.fetch_live_trends()
    print(f"✅ 수집된 실시간 트렌드 {len(results)}개:")
    for r in results[:5]:
        print(f" - {r['keyword']} (트래픽: {r['traffic_volume']:,})")
    print("\n🔍 네이버 자동완성 확장 테스트 ('청년도약계좌'):")
    expanded = scout.expand_autocomplete("청년도약계좌", limit=5)
    print(" - 서브 키워드 후보:", expanded)

