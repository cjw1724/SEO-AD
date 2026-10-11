import os
import requests

url = "https://openrouter.ai/api/v1/models"
response = requests.get(url)
models = response.json().get('data', [])

keywords = ['flux', 'schnell', 'dall', 'midjourney', 'stable', 'image', 'picture', 'vision']

found = []
for m in models:
    name = m['id'].lower()
    if any(k in name for k in keywords):
        found.append(m['id'])

print("Found models:")
for f in found:
    print(f)
