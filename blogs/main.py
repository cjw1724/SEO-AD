import os
import sys
import time
import traceback
import schedule

# Ensure current script directory is in sys.path so 'tools' can be imported reliably
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools import (
    publish_to_blogger, 
    generate_thumbnail_tool, 
    analyze_korean_trends_and_ads,
    search_financial_data,
    search_affiliate_products,
    search_code_snippets,
    naver_shopping_api_scanner,
    community_best_crawler,
    google_ads_keyword_planner
)
from agents.writer_agent import WriterAgent
from agents.publisher_agent import PublisherAgent

# Load environment variables
env_path = os.path.abspath(os.path.join(current_dir, "..", "SEO.env"))
load_dotenv(env_path)

def run_blog_automation():
    print("[START] AI 미디어 제국 v3.0 (5대 프레임워크: Mobbin, Nicelydone, Refero, Lazyweb, InspoAI)")

    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # Set up OpenRouter LLM for workers and manager
    llm = LLM(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.7
    )

    manager_llm = LLM(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.7
    )

    # 1. Trend Scanner Agent (레이더 전위대)
    trend_scanner = Agent(
        role="Trend Scanner",
        goal="Scan real-time portals and communities to gather the top 20 hottest issues right now.",
        backstory="An AI specialized in detecting viral trends before they peak. Uses Google Trends, Naver Shopping, and Communities to scrape raw data.",
        verbose=True,
        llm=llm,
        tools=[analyze_korean_trends_and_ads, naver_shopping_api_scanner, community_best_crawler]
    )

    # 2. Financial/CPC Analyst Agent (수익성 레이더 본체)
    cpc_analyst = Agent(
        role="Financial and CPC Analyst",
        goal="Calculate the PVS (Profitability Velocity Score) of trending keywords using Google Ads / Naver Keyword data and select the single most profitable keyword.",
        backstory="A ruthless financial analyst who cross-references trending keywords with AdSense CPC and CPA payout rates. Discards high-volume but low-paying keywords.",
        verbose=True,
        llm=llm,
        tools=[google_ads_keyword_planner]
    )

    # 3. High-Value SEO Writer Agent (Impeccable & Wall Street Editorial Design System)
    seo_writer = Agent(
        role="World-Class Revenue Blog Writer & Financial UX Architect",
        goal=(
            "Write an elite-level Korean HTML blog post formatted like the world's #1 financial media "
            "(Bloomberg, Wall Street Journal, Toss, Bankrate) strictly incorporating the Impeccable editorial system: "
            "(1) Optimal 760px reading container (<div class='article-editorial-container'>), "
            "(2) Executive Briefing Hero Bento (<div class='hero-editorial-card'>) with live metric badges, "
            "(3) Interactive Micro-SaaS calculator tool (<div class='editorial-calculator-card'>), "
            "(4) Wall Street Journal comparison table (<table class='editorial-table'>), "
            "(5) Institutional analysis grid (<div class='editorial-analysis-grid'>) with inline SVG icons (zero childish pastel cards), "
            "(6) Pure-CSS chevron FAQ accordion (<details class='editorial-faq-item'>), and "
            "(7) Mobile-first sticky action dock (<div class='editorial-sticky-bar'>)."
        ),
        backstory=(
            "A master monetization architect and senior financial editor who produces authoritative content that ranks #1. "
            "You create interactive digital assets that captivate readers, maximizing dwell time and AdSense RPM. "
            "You avoid all amateurish AI tropes such as garish pastel cards or raw HTML entities. "
            "You use clean semantic HTML, inline vector SVGs, and pure vanilla JavaScript."
        ),
        verbose=True,
        llm=llm,
        tools=[search_financial_data, search_affiliate_products, search_code_snippets]
    )

    # 4. Publisher Agent
    publisher_agent = Agent(
        role="Publisher and Designer",
        goal="Generate a click-bait thumbnail image and publish the final HTML article to Google Blogger.",
        backstory="A meticulous editor who ensures the layout is perfect, generates high-quality thumbnails using AI, and publishes flawlessly.",
        verbose=True,
        tools=[generate_thumbnail_tool, publish_to_blogger],
        llm=llm
    )

    # Sequential Task Workflow
    main_task = Task(
        description="""
        You are executing the ultimate AI Media Empire workflow to build a world-class profitable Korean blog post.
        
        Step 1 (Radar Scanner):
        Use the 'Trend Scanner' to gather real-time trending topics and queries.
        
        Step 2 (PVS & Revenue Radar Analysis):
        Use the 'Financial and CPC Analyst' to evaluate those trends, calculate the PVS (Profitability Velocity Score), and select the single most profitable, high-paying keyword.
        
        Step 3 (World-Class Revenue Blog Writing with Impeccable Architecture):
        Delegate to the 'High-Value SEO Writer'. The writer MUST produce a complete, premium Korean HTML article adhering strictly to the Impeccable editorial design system:
        
        [MANDATORY COMPONENT 1: Executive Briefing Hero Bento]
        <div class="hero-editorial-card">
          <div class="hero-meta-row">
            <span class="badge-live-intel"><span class="live-pulse-dot"></span> 오늘 14,290명 조회 실시간 검증 데이터</span>
            <span class="badge-executive-pill">EXECUTIVE BRIEF</span>
          </div>
          <h3 class="hero-editorial-title">[핵심 주제 요약 타이틀]</h3>
          <div class="editorial-takeaways-grid">
            <div class="editorial-takeaway-item">
              <span class="takeaway-metric-label">Rate Alpha</span>
              <div class="takeaway-metric-body"><strong>[핵심 포인트 1]:</strong> 간결하고 명확한 수치 기반 설명</div>
            </div>
            <div class="editorial-takeaway-item">
              <span class="takeaway-metric-label">Tax Defense</span>
              <div class="takeaway-metric-body"><strong>[데이터 인사이트]:</strong> 이자소득세 절세 및 분석 내용</div>
            </div>
            <div class="editorial-takeaway-item">
              <span class="takeaway-metric-label">Instant Tool</span>
              <div class="takeaway-metric-body"><strong>[실행 가이드]:</strong> 즉시 실행 가능한 액션 플랜</div>
            </div>
          </div>
        </div>
        
        [MANDATORY COMPONENT 2: Interactive Micro-SaaS Financial Calculator]
        <div class="editorial-calculator-card" id="custom-saas-tool">
          <div class="calc-header">
            <div class="calc-title-group">
              <h3>실시간 복리 수익 시뮬레이터</h3>
              <p>수치를 입력하거나 슬라이더를 움직여 실시간 결과를 확인하세요.</p>
            </div>
            <span class="calc-badge">Micro-SaaS Tool</span>
          </div>
          <div class="calc-inputs-grid">
            <div class="calc-input-box">
              <div class="calc-input-header">
                <span class="calc-input-label">예치 금액</span>
                <span class="calc-val-display" id="val-display-1">1,000만원</span>
              </div>
              <input type="range" class="calc-range-slider" id="calc-input-1" min="100" max="10000" step="100" value="1000" oninput="calculateSaaSTool()" />
            </div>
            <div class="calc-input-box">
              <div class="calc-input-header">
                <span class="calc-input-label">운용 기간</span>
                <span class="calc-val-display" id="val-display-2">12개월</span>
              </div>
              <input type="range" class="calc-range-slider" id="calc-input-2" min="1" max="60" step="1" value="12" oninput="calculateSaaSTool()" />
            </div>
          </div>
          <div class="calc-hero-metric-card">
            <div class="metric-card-header">
              <span class="metric-card-label">예상 세후 총 수령액 (원금 + 이자)</span>
              <span class="metric-card-number" id="calc-result-value">0원</span>
            </div>
            <div class="metric-card-subtext">
              <span>적용 금리: 연 4.25%</span>
              <span id="calc-net-profit">+359,550원 (세후 순이자)</span>
            </div>
          </div>
          <div class="calc-action-row">
            <button class="btn-action-primary" id="btn-copy-result" onclick="copyToolResult()">결과 복사하기</button>
            <button class="btn-action-secondary" onclick="resetTool()">초기화</button>
          </div>
        </div>
        
        [MANDATORY COMPONENT 3: Wall Street Journal Comparison Table & Institutional Analysis Grid]
        <div class="editorial-table-wrap">
          <table class="editorial-table">
            <thead>
              <tr>
                <th>비교 항목</th>
                <th class="top-col">추천 옵션 A <span class="table-pill-top">TOP PICK</span></th>
                <th>대안 옵션 B</th>
                <th>대안 옵션 C</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>주요 특징</strong></td>
                <td>최대 혜택 및 수수료 면제</td>
                <td>기본 혜택 적용</td>
                <td>제한적 지원</td>
              </tr>
              <tr>
                <td><strong>비용 / 금리</strong></td>
                <td>연 4.25% ~ 5.10%</td>
                <td>연 2.80% ~ 3.20%</td>
                <td>연 3.80% ~ 4.10%</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="editorial-analysis-grid">
          <div class="analysis-panel analysis-panel-strength">
            <h4 class="panel-title">핵심 경쟁력 및 기대 수익</h4>
            <ul class="analysis-list">
              <li class="analysis-item"><span>실시간 데이터 기반의 탁월한 정확도 및 신뢰성</span></li>
              <li class="analysis-item"><span>복잡한 절차 없이 3분 내 즉시 적용 가능</span></li>
            </ul>
          </div>
          <div class="analysis-panel analysis-panel-risk">
            <h4 class="panel-title">리스크 요건 및 운용 주의점</h4>
            <ul class="analysis-list">
              <li class="analysis-item"><span>시장 상황 및 정책 변동에 따른 세부 조건 차이 가능성</span></li>
              <li class="analysis-item"><span>개인 신용도 및 자격 요건에 따른 차등 적용 주의</span></li>
            </ul>
          </div>
        </div>
        
        [MANDATORY COMPONENT 4: Mobile Sticky Action Bar]
        <div class="editorial-sticky-bar">
          <div class="sticky-info">
            <div class="sticky-tagline"><span class="live-pulse-dot"></span> 14,290명 검증</div>
            <div class="sticky-headline">실시간 핵심 시뮬레이션</div>
          </div>
          <button type="button" class="btn-sticky-jump" onclick="document.getElementById('custom-saas-tool').scrollIntoView({behavior:'smooth'});">계산기 실행</button>
        </div>
        
        [MANDATORY COMPONENT 5: Pure-CSS Chevron FAQ Accordion]
        <div class="editorial-faq-group">
          <details class="editorial-faq-item">
            <summary class="editorial-faq-summary">
              <span>Q. 가장 먼저 확인해야 할 핵심 기준은 무엇인가요?</span>
              <span class="faq-chevron"></span>
            </summary>
            <div class="editorial-faq-content">
              <p>기본 조건과 함께 숨겨진 부가 수수료나 우대 조건을 반드시 교차 검증해야 합니다.</p>
            </div>
          </details>
        </div>
        
        [MANDATORY FORMATTING GUIDELINES]
        - 전체 본문은 반드시 <div class="article-editorial-container">로 감싸야 합니다.
        - 절대로 raw HTML entities (&#10003;, &#9662;)를 출력하지 마세요.
        - Structure content with clear <h2> and <h3> subheadings.
        - Ensure engaging, high-retention Korean copywriting that provides immense practical value.
        
        Step 4 (Publishing):
        Delegate to the 'Publisher and Designer' to generate an English-prompt thumbnail using Flux Schnell, prepend the <img> tag at the very top, and publish the final HTML article directly to Google Blogger.
        
        Return the final Blogger URL.
        
        [MANDATORY FORMATTING GUIDELINES]
        - Output pure, semantic HTML for the article body with an embedded <style> block at top for instant breathtaking styling.
        - Structure content with clear <h2> and <h3> subheadings.
        - Ensure engaging, high-retention Korean copywriting that provides immense practical value and drives maximum dwell time.
        
        Step 4 (Publishing):
        Delegate to the 'Publisher and Designer' to generate an English-prompt thumbnail using Flux Schnell, prepend the <img> tag at the very top, and publish the final HTML article directly to Google Blogger.
        
        Return the final Blogger URL.
        """,
        expected_output="The final successfully published blog post URL from Blogger.",
    )

    try:
        crew = Crew(
            agents=[trend_scanner, cpc_analyst, seo_writer, publisher_agent],
            tasks=[main_task],
            process=Process.hierarchical,
            manager_llm=manager_llm,
            verbose=True
        )

        result = crew.kickoff()
        print("[SUCCESS] CrewAI 자동화 프로세스 완료!")
        print(result)
        return str(result)
    except Exception as crew_err:
        print(f"⚠️ [CrewAI Execution Notice] {crew_err}. 다이렉트 고속 파이프라인으로 즉시 발행합니다.")
        return run_direct_publish_pipeline()

def run_direct_publish_pipeline(topic: str = "2026 고금리 파킹통장 및 적금 금리 비교 추천", post_id: str = None):
    """
    Direct, 100% resilient pipeline combining WriterAgent and PublisherAgent.
    Guarantees publishing of the Impeccable editorial masterpiece without any coordination bottlenecks.
    """
    print(f"🚀 [Direct Pipeline] '{topic}' 쇼케이스 글 작성 및 발행/업데이트 시작...")
    writer = WriterAgent()
    article = writer.write_article(topic)
    
    # Generate high-res AI thumbnail
    thumbnail_html = generate_thumbnail_tool.run(prompt="modern fintech toss bank smartphone app neon gradient 3d render")
    if thumbnail_html:
        article["content"] = thumbnail_html + "\n\n" + article["content"]
        
    publisher = PublisherAgent()
    if post_id:
        result = publisher.update(post_id, article)
    else:
        result = publisher.publish(article)
    if result:
        print(f"🎉 [Direct Pipeline] 성공 완료! URL: {result}")
    return result

def safe_run_blog_automation():
    try:
        run_blog_automation()
    except Exception as e:
        print(f"[ERROR] 자동화 오류 발생: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting blog automation v3.0 (5-Framework Powered)...")
    
    # Run once immediately
    safe_run_blog_automation()
    
    # Schedule to run every day at 09:00 AM
    schedule.every().day.at("09:00").do(safe_run_blog_automation)
    print("Scheduled to run daily at 09:00 AM. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nExiting schedule loop...")
        sys.exit(0)
