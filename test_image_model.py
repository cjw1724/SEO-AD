import os
import requests
from dotenv import load_dotenv

load_dotenv('SEO.env')

url = "https://openrouter.ai/api/v1/images"
headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/crewai",
    "X-Title": "AI Media Empire"
}

models_to_test = [
    "black-forest-labs/flux-1-schnell",
    "black-forest-labs/flux-schnell",
    "neversleep/flux-1-schnell",
    "neversleep/flux-schnell",
    "black-forest-labs/flux-schnell:free",
    "black-forest-labs/flux-1-schnell:free"
]

for model in models_to_test:
    payload = {
        "model": model,
        "prompt": "A cute cat",
        "n": 1,
        "response_format": "b64_json"
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Testing {model} -> Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Model {model} works.")
        break
    else:
        print(response.text)
