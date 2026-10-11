import re

with open(r'd:\SEO AD\blogs\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix finance_agent
content = re.sub(
    r'goal="Write high-CPC finance/insurance blog posts focused on maximizing AdSense clicks\.",',
    'goal="Write high-CPC finance/insurance blog posts focused on maximizing AdSense clicks. Naver/Google SEO optimized formatting, high dwell-time structure, and click-inducing copywriting.",',
    content
)

# Fix commerce_agent
content = re.sub(
    r'goal="Write compelling product reviews and insert Coupang/Amazon affiliate links to drive sales commissions\.",',
    'goal="Write compelling product reviews and insert Coupang/Amazon affiliate links to drive sales commissions. Naver/Google SEO optimized formatting, high dwell-time structure, and click-inducing copywriting.",',
    content
)

# Fix saas_agent
content = re.sub(
    r'goal="Write blog posts that include interactive HTML/JS widgets to trap users and maximize dwell time\.",',
    'goal="Write blog posts that include interactive HTML/JS widgets to trap users and maximize dwell time. Naver/Google SEO optimized formatting, high dwell-time structure, and click-inducing copywriting.",',
    content
)

# Fix main_task description
new_task_desc = '''        description="""
        You are the ruthless CEO of a Korean AI Media Empire. You will receive today's trending search volumes and high-paying ad keywords. Your job is to choose the most profitable keyword and delegate it to the correct department (Finance, Commerce, or SaaS) to maximize Google AdSense and CPA revenue in Korea.
        
        Step 1: Delegate to the 'Korean Market Trend & Ads Analyst' to use the 'Analyze Korean Trends and Ads' tool. Find out what the highest-paying, most searched topic is right now.
        Step 2: Based on the findings, decide which department is best suited for the topic (Finance, Commerce, or SaaS).
        Step 3: Delegate the writing task to that specific department. Instruct them to write an SEO-optimized HTML blog post in Korean. The post MUST contain a catchy title and content clearly separated.
        Step 4: Once the content is ready, delegate to the Publisher and Designer agent to generate a thumbnail (English prompt) and insert the <img> tag at the top of the HTML content.
        Step 5: Finally, delegate to the Publisher and Designer agent to publish the post to Blogger using the 'Publish to Blogger' tool.
        
        Return the final Blogger URL.
        """,'''

content = re.sub(r'description="""\s*You are the CEO.*?Return the final Blogger URL.\s*""",', new_task_desc, content, flags=re.DOTALL)

with open(r'd:\SEO AD\blogs\main.py', 'w', encoding='utf-8') as f:
    f.write(content)
