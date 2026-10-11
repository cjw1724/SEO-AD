import os
import re
import sys
import urllib.request

# Ensure UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.abspath(__file__))
blogs_dir = os.path.join(root_dir, "blogs")
if blogs_dir not in sys.path:
    sys.path.insert(0, blogs_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(root_dir, "SEO.env"))

from blogs.agents.writer_agent import WriterAgent
from blogs.agents.publisher_agent import PublisherAgent
from blogs.tools import generate_thumbnail_tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def main():
    target_post_id = "1998634516459680663"
    topic = "2026 고금리 파킹통장 & 복리 적금 수익률 시뮬레이터: 토스 / 케이뱅크 / 시중은행 종결 비교"
    
    print(f"=== Starting Showcase Post Update (ID: {target_post_id}) ===")
    writer = WriterAgent()
    article = writer.write_article(topic)
    
    print(f"Title: {article['title']}")
    print(f"Content Length: {len(article['content'])} chars")
    
    # Generate thumbnail
    try:
        thumb_prompt = "modern fintech toss bank smartphone app neon gradient 3d render clean futuristic"
        thumbnail_html = generate_thumbnail_tool.run(prompt=thumb_prompt)
        if thumbnail_html:
            article["content"] = thumbnail_html + "\n\n" + article["content"]
            print("Thumbnail generated and prepended.")
    except Exception as e:
        print(f"Thumbnail generation warning: {e}")
        
    publisher = PublisherAgent()
    updated_url = publisher.update(target_post_id, article)
    print(f"Update Result URL: {updated_url}")
    assert updated_url, "Failed to update showcase post!"
    
    # Fetch from Blogger API to verify
    blog_id = os.getenv("BLOGGER_BLOG_ID")
    token_path = os.path.join(root_dir, "token.json")
    creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/blogger'])
    service = build('blogger', 'v3', credentials=creds)
    fetched = service.posts().get(blogId=blog_id, postId=target_post_id).execute()
    
    fetched_title = fetched.get('title', '')
    fetched_content = fetched.get('content', '')
    
    print("\n=== Verifying Blogger API Post Content ===")
    print(f"Fetched Title: {fetched_title}")
    
    # 1. Check for unrendered entities
    banned_entities = ['&#10003;', '&#10005;', '&#9662;', '&#183;', '&amp;#10003;', '&amp;#183;']
    for entity in banned_entities:
        count = fetched_content.count(entity)
        print(f"Entity check '{entity}': {count} occurrences")
        assert count == 0, f"Found banned entity {entity} in post content!"
        
    # Check title for entities
    for entity in banned_entities:
        assert entity not in fetched_title, f"Found banned entity {entity} in post title!"
        
    # 2. Check for pastel classes
    banned_classes = ['pros-box', 'cons-box', 'box-title-green', 'box-title-red']
    for cls in banned_classes:
        assert cls not in fetched_content, f"Found banned pastel class {cls} in post content!"
    print("[PASS] Zero pastel classes found")
    
    # 3. Check for core Wall Street editorial components
    required_components = [
        'article-editorial-container',
        'hero-editorial-card',
        'editorial-h2',
        'editorial-calculator-card',
        'calc-range-slider',
        '10,359,550원',
        'editorial-table',
        'editorial-analysis-grid',
        'analysis-panel-strength',
        'analysis-panel-risk',
        'editorial-faq-group',
        'faq-chevron',
        'editorial-sticky-bar'
    ]
    for comp in required_components:
        assert comp in fetched_content, f"Required component '{comp}' missing from post content!"
        print(f"[PASS] Component '{comp}' verified")
        
    h2_count = len(re.findall(r'<h2\b', fetched_content, re.IGNORECASE))
    print(f"Total H2 Headings: {h2_count}")
    assert h2_count >= 5, f"Expected at least 5 H2 headings, found {h2_count}!"
    
    print("\nALL API POST VERIFICATIONS PASSED SUCCESSFULLY!")
    
    # 4. Fetch Live Public HTML
    live_url = "https://blogin365ai.blogspot.com/2026/10/2026-2026_01493596745.html"
    print(f"\n=== Fetching Live Public Webpage: {live_url} ===")
    req = urllib.request.Request(
        live_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    with urllib.request.urlopen(req) as response:
        live_html = response.read().decode('utf-8')
        
    print(f"Live HTML length: {len(live_html)} chars")
    
    # Check live HTML for entities
    for entity in ['&#10003;', '&#10005;', '&#9662;']:
        assert entity not in live_html, f"Found raw entity {entity} in public webpage HTML!"
    print("[PASS] Zero raw &#10003;, &#10005;, &#9662; in public webpage HTML")
    
    assert "editorial-calculator-card" in live_html, "editorial-calculator-card missing in public HTML!"
    assert "editorial-table" in live_html, "editorial-table missing in public HTML!"
    assert "editorial-sticky-bar" in live_html, "editorial-sticky-bar missing in public HTML!"
    print("[PASS] Masterclass editorial design components verified in public webpage HTML!")
    print("\n=== SHOWCASE UPDATE & VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    main()
