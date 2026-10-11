import os
from dotenv import load_dotenv
load_dotenv('d:/SEO AD/SEO.env')

from google import genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing models that support image generation:")
for model in client.models.list():
    if "image" in model.name or "imagen" in model.name:
        print(f"Name: {model.name}")

print("Testing generate_content with a gemini model for image generation:")
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='A cute cat',
        config={
            "output_mime_type": "image/jpeg"
        }
    )
    print("Success with gemini-2.5-flash")
except Exception as e:
    print(f"Error with gemini-2.5-flash: {e}")

try:
    response = client.models.generate_content(
        model='gemini-3.0-pro-image',
        contents='A cute cat'
    )
    print("Success with gemini-3.0-pro-image")
except Exception as e:
    print(f"Error with gemini-3.0-pro-image: {e}")
