import os
import requests
from dotenv import load_dotenv
load_dotenv('d:/SEO AD/SEO.env')

api_key = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={api_key}"

payload = {
    "instances": [
        {
            "prompt": "A cute cat"
        }
    ],
    "parameters": {
        "sampleCount": 1
    }
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.text)
