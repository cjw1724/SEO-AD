import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv("SEO.env")

blog_id = os.getenv("BLOGGER_BLOG_ID")
creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/blogger"])
service = build("blogger", "v3", credentials=creds)

post = service.posts().get(blogId=blog_id, postId="1998634516459680663").execute()
content = post.get("content", "")

idx = 0
while True:
    pos = content.find("editorial-author-box", idx)
    if pos == -1:
        break
    start = max(0, pos - 100)
    end = min(len(content), pos + 200)
    print("Found around pos:", pos)
    print("Snippet:", repr(content[start:end]))
    idx = pos + 20
