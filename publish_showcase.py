import os
import sys

# Ensure UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure current script directory and blogs are in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
blogs_dir = os.path.join(root_dir, "blogs")
if blogs_dir not in sys.path:
    sys.path.insert(0, blogs_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(root_dir, "SEO.env"))

from blogs.agents.writer_agent import WriterAgent
from blogs.tools import generate_thumbnail_tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def publish_showcase_post():
    print("="*60)
    print("[SHOWCASE PUBLISHER] 5대 디자인 프레임워크 실전 포스팅 시작...")
    print("="*60)
    
    topic = "2026 고금리 파킹통장 & 복리 적금 수익률 시뮬레이터: 토스·케이뱅크·시중은행 종결 비교"
    
    # 1. AI 본문 작성 (5대 프레임워크 탑재)
    writer = WriterAgent()
    article = writer.write_article(topic)
    
    print(f"제목: {article['title']}")
    print(f"본문 길이: {len(article['content'])}자")
    
    # 2. 고화질 AI 썸네일 생성
    print("고화질 AI 썸네일 생성 중...")
    thumb_prompt = "modern fintech toss bank smartphone app neon gradient 3d render clean futuristic"
    thumbnail_html = generate_thumbnail_tool.run(prompt=thumb_prompt)
    if thumbnail_html:
        article["content"] = thumbnail_html + "\n\n" + article["content"]
        print("썸네일 생성 완료 및 본문 상단 결합 완료!")
        
    # 3. 구글 블로거 API를 통해 실제 발행
    blog_id = os.getenv("BLOGGER_BLOG_ID")
    token_path = os.path.join(root_dir, "token.json")
    
    creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/blogger'])
    service = build('blogger', 'v3', credentials=creds)
    
    body = {
        "kind": "blogger#post",
        "title": article['title'],
        "content": article['content'],
        "labels": article.get('tags', ["AI트렌드", "재테크", "계산기", "비교분석", "가이드"])
    }
    
    print(f"구글 블로거({blog_id})로 실시간 발행 전송 중...")
    posts = service.posts()
    result = posts.insert(blogId=blog_id, body=body, isDraft=False).execute()
    
    post_url = result.get('url')
    post_id = result.get('id')
    print("="*60)
    print(f"[발행 완료!] 성공적으로 구글 블로거에 등록되었습니다!")
    print(f"게시글 URL: {post_url}")
    print(f"Post ID: {post_id}")
    print("="*60)
    
    # 4. 검증: 발행된 포스트 확인
    fetched = posts.get(blogId=blog_id, postId=post_id).execute()
    content = fetched.get('content', '')
    
    print("\n[발행 포스트 Impeccable 디자인 시스템 검증]")
    print("1. Reading Container (760px):", "article-editorial-container" in content)
    print("2. Executive Briefing Hero Bento:", "hero-editorial-card" in content)
    print("3. Micro-SaaS 계산기:", "editorial-calculator-card" in content and "calc-range-slider" in content)
    print("4. 비교 매트릭스 & 분석 그리드:", "editorial-table" in content and "editorial-analysis-grid" in content)
    print("5. 모바일 하단 독 바:", "editorial-sticky-bar" in content)
    print("6. 순수 CSS Chevron FAQ 아코디언:", "editorial-faq-group" in content and "faq-chevron" in content)
    print("7. 마스터 Impeccable CSS 주입:", "Impeccable Editorial Design System" in content)
    print("8. 플레이스홀더 잔존 여부 (False여야 함):", any(p in content for p in ['[핵심 포인트 1]', '추천 프리미엄 옵션', '일반 표준 옵션']))
    print("9. 썸네일 이미지 포함:", "<img" in content)
    print("10. 엔티티 슬롭 부재 (False여야 함):", any(e in content for e in ['&#10003;', '&#10005;', '&#9662;']))
    
    assert "article-editorial-container" in content, "article-editorial-container missing!"
    assert "hero-editorial-card" in content, "hero-editorial-card missing!"
    assert "editorial-calculator-card" in content and "calc-range-slider" in content, "Calculator missing!"
    assert "editorial-table" in content and "editorial-analysis-grid" in content, "Comparison table or analysis grid missing!"
    assert "editorial-sticky-bar" in content, "Mobile sticky bar missing!"
    assert "editorial-faq-group" in content and "faq-chevron" in content, "FAQ accordion missing!"
    assert "Impeccable Editorial Design System" in content, "Master Impeccable CSS missing!"
    assert not any(p in content for p in ['[핵심 포인트 1]', '추천 프리미엄 옵션', '일반 표준 옵션']), "Unfinished placeholders detected in post!"
    assert not any(e in content for e in ['&#10003;', '&#10005;', '&#9662;']), "Raw entity slop detected in post!"
    
    return post_url

if __name__ == "__main__":
    url = publish_showcase_post()
    print(f"\nFINAL_URL: {url}")
