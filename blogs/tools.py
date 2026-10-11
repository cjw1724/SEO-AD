import os
import base64
from crewai.tools import tool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']

@tool("Publish to Blogger")
def publish_to_blogger(title: str, content: str) -> str:
    """
    Publishes an HTML article to Google Blogger.
    Args:
        title (str): The title of the blog post.
        content (str): The HTML content of the blog post.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    token_path = os.path.join(base_dir, 'token.json')
    creds_path = os.path.join(base_dir, 'credentials.json')
    blog_id = os.getenv("BLOGGER_BLOG_ID")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(creds_path):
                    return "Error: credentials.json not found."
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
    except Exception as e:
        return f"Error during Google authentication: {e}"

    if not blog_id:
        return "Error: BLOGGER_BLOG_ID not set in environment."

    import re
    
    content = content.strip()
    content = re.sub(r"^```(?:html)?\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"```\s*$", "", content)
    content = content.strip()

    # Clean entities and obsolete pastel classes
    replacements = [
        ("&#10003;", ""),
        ("&#10004;", ""),
        ("&#10005;", ""),
        ("&#10006;", ""),
        ("&#9660;", ""),
        ("&#9662;", ""),
        ("&amp;#10003;", ""),
        ("&amp;#10004;", ""),
        ("&amp;#10005;", ""),
        ("&amp;#10006;", ""),
        ("&amp;#9660;", ""),
        ("&amp;#9662;", ""),
        ("pros-box", "analysis-panel analysis-panel-strength"),
        ("cons-box", "analysis-panel analysis-panel-risk"),
        ("box-title-green", "panel-title"),
        ("box-title-red", "panel-title"),
    ]
    for bad, good in replacements:
        content = content.replace(bad, good)

    try:
        service = build('blogger', 'v3', credentials=creds)
        body = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
        }
        
        posts = service.posts()
        result = posts.insert(blogId=blog_id, body=body, isDraft=False).execute()
        return f"Successfully published! URL: {result.get('url')}"
        
    except Exception as e:
        return f"Error publishing to Blogger: {e}"

@tool("Generate Thumbnail")
def generate_thumbnail_tool(prompt: str) -> str:
    """
    Generates a high-quality thumbnail image using Flux AI based on the provided prompt,
    and returns an HTML img tag with modern responsive card styling.
    """
    if isinstance(prompt, dict):
        prompt = prompt.get("prompt", str(prompt))
        
    try:
        import requests
        import urllib.parse
        import base64
        
        # Clean prompt for URL query
        clean_prompt = prompt.replace(" ", "-")[:120]
        encoded_prompt = urllib.parse.quote(clean_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true"
        
        response = requests.get(url, timeout=12)
        if response.status_code == 200 and len(response.content) > 1000:
            b64_img = base64.b64encode(response.content).decode("utf-8")
            return f'<div class="editorial-hero-thumbnail" style="max-width:760px; margin:0 auto 32px auto; border-radius:16px; overflow:hidden; box-shadow:0 4px 20px -4px rgba(15,23,42,0.08);"><img src="data:image/jpeg;base64,{b64_img}" alt="{prompt}" style="width:100%; height:auto; display:block; border-radius:16px;" /></div>'
        else:
            return f'<div class="editorial-hero-thumbnail" style="max-width:760px; margin:0 auto 32px auto; border-radius:16px; overflow:hidden; box-shadow:0 4px 20px -4px rgba(15,23,42,0.08);"><img src="{url}" alt="{prompt}" style="width:100%; height:auto; display:block; border-radius:16px;" /></div>'
            
    except Exception as e:
        print(f"\n[WARNING] Failed to fetch thumbnail via Pollinations: {e}")
        # Elegant vector fallback banner
        return '<div class="editorial-hero-thumbnail" style="max-width:760px; margin:0 auto 32px auto; background:linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%); border-radius:16px; padding:44px 30px; color:#ffffff; text-align:center; box-shadow:0 4px 20px -4px rgba(15,23,42,0.12);"><h2 style="font-size:1.75rem; font-weight:800; margin:0 0 10px 0; color:#ffffff;">Blogin 365 AI Insights</h2><p style="font-size:0.95rem; opacity:0.85; margin:0;">World-Class Tech & Fintech Automation Intelligence</p></div>'

@tool("Analyze Korean Trends and Ads")
def analyze_korean_trends_and_ads(query: str = "") -> str:
    """Analyze real-time Google Korean search trends and calculate PVS based on traffic and CPC multipliers."""
    import json
    import feedparser
    
    url = "https://trends.google.com/trending/rss?geo=KR"
    try:
        feed = feedparser.parse(url)
        results = []
        high_cpc_keywords = ['대출', '주식', '보험', '부동산', '투자', '청약', '자격증', '최신 전자기기']
        
        for entry in feed.entries:
            title = entry.get('title', '')
            traffic_str = entry.get('ht_approx_traffic', '0')
            traffic_clean = traffic_str.replace(',', '').replace('+', '').strip()
            try:
                traffic_vol = int(traffic_clean)
            except ValueError:
                traffic_vol = 0
                
            cpc_multiplier = 1.0
            for kw in high_cpc_keywords:
                if kw in title:
                    cpc_multiplier = 5.0
                    break
                    
            expected_ctr = 0.05
            pvs = traffic_vol * expected_ctr * cpc_multiplier
            
            results.append({
                "keyword": title,
                "Traffic_Volume": traffic_vol,
                "Expected_CTR": expected_ctr,
                "Estimated_CPC_Multiplier": cpc_multiplier,
                "PVS": pvs
            })
            
        results.sort(key=lambda x: x["PVS"], reverse=True)
        top_5 = results[:5]
        return json.dumps(top_5, ensure_ascii=False)
    except Exception as e:
        return f"Error analyzing trends: {e}"

@tool("Search Financial Data")
def search_financial_data(query: str) -> str:
    """Mock tool to search financial data."""
    return f"Mock financial data for {query}"

@tool("Search Affiliate Products")
def search_affiliate_products(query: str) -> str:
    """Mock tool to search affiliate products."""
    return f"Mock affiliate products for {query}"

@tool("Search Code Snippets")
def search_code_snippets(query: str) -> str:
    """Mock tool to search code snippets."""
    return f"Mock code snippets for {query}"

@tool("Naver Shopping API Scanner")
def naver_shopping_api_scanner(query: str = "") -> str:
    """Scan trending shopping keywords from Naver Shopping API."""
    pass
    return "[]"

@tool("Community Best Crawler")
def community_best_crawler(query: str = "") -> str:
    """Crawl best posts from Korean communities like DC Inside, FM Korea."""
    pass
    return "[]"

@tool("Google Ads Keyword Planner")
def google_ads_keyword_planner(keyword: str) -> str:
    """Analyze high-CPC potential for keywords via Google Ads Keyword Planner."""
    pass
    return "{}"


