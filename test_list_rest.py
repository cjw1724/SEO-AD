import os
import requests
from dotenv import load_dotenv
load_dotenv('d:/SEO AD/SEO.env')

api_key = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

models = response.json().get('models', [])
for m in models:
    if 'image' in m.get('name', '').lower() or 'imagen' in m.get('name', '').lower():
        print(f"Name: {m['name']}")
        print(f"Supported methods: {m.get('supportedGenerationMethods', [])}")
