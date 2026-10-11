import requests
import json

response = requests.get("https://openrouter.ai/api/v1/models")
if response.status_code == 200:
    data = response.json()
    flux_models = []
    for model in data.get("data", []):
        if "flux" in model["id"].lower():
            flux_models.append(model["id"])
    print("Flux models found:")
    for m in flux_models:
        print("-", m)
else:
    print("Failed to get models:", response.status_code, response.text)
