import requests
import os
import re
from dotenv import load_dotenv

load_dotenv("SEO.env")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

def test_chat_completions():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "black-forest-labs/flux-schnell",
        "messages": [{"role": "user", "content": "A cute dog in a park"}],
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Status:", response.status_code)
    data = response.json()
    print("Response JSON:", data)
    
    if response.status_code == 200:
        content = data["choices"][0]["message"]["content"]
        # extract URL using regex
        match = re.search(r"\!\[.*?\]\((.*?)\)", content)
        if match:
            print("Extracted URL:", match.group(1))
        else:
            print("Could not extract URL from:", content)

test_chat_completions()
