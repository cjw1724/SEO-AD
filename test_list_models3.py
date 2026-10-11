import os
from dotenv import load_dotenv
load_dotenv('d:/SEO AD/SEO.env')

from google import genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    print("Testing generate_content with imagen-3.0-generate-002")
    response = client.models.generate_content(
        model='imagen-3.0-generate-002',
        contents='A cute cat'
    )
    print("Success:", response)
except Exception as e:
    print(f"Error: {e}")

try:
    print("Testing generate_content with imagen-3.0-generate-001")
    response = client.models.generate_content(
        model='imagen-3.0-generate-001',
        contents='A cute cat'
    )
    print("Success:", response)
except Exception as e:
    print(f"Error: {e}")

