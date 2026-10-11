import os
import re
from dotenv import load_dotenv

load_dotenv("SEO.env")
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

blog_id = os.getenv("BLOGGER_BLOG_ID")
creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/blogger"])
service = build("blogger", "v3", credentials=creds)

posts = service.posts().list(blogId=blog_id).execute().get("items", [])
for p in posts:
    c = p.get("content", "")
    if "editorial-author-box" in c or "김재현" in c:
        print(f"Purging fake author from post {p['id']}: {p['title']}")
        # Remove the author box completely
        clean_c = re.sub(r'<div class=["\']editorial-author-box["\'].*?</div>(\s*</div>)?', '</div>', c, flags=re.DOTALL)
        if "김재현" in clean_c:
            clean_c = re.sub(r'<div class=["\']editorial-author-box["\'].*?</div>', '', clean_c, flags=re.DOTALL)
        
        # In case the text is outside the div or in another container
        clean_c = re.sub(r'<p class=["\']author-name["\']>.*?</p>', '', clean_c, flags=re.DOTALL)
        clean_c = re.sub(r'<p class=["\']author-title["\']>.*?</p>', '', clean_c, flags=re.DOTALL)
        clean_c = re.sub(r'<p class=["\']author-bio["\']>.*?</p>', '', clean_c, flags=re.DOTALL)
        clean_c = re.sub(r'김재현.*?제공합니다\.', '', clean_c)
        clean_c = clean_c.replace("김재현", "").replace("금융 전문 기자", "")

        body = {"content": clean_c, "title": p["title"]}
        updated = service.posts().patch(blogId=blog_id, postId=p["id"], body=body).execute()
        print(f"Successfully purged! Check for 김재현: {'김재현' in updated.get('content', '')}")
