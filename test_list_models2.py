import os
from dotenv import load_dotenv
load_dotenv('d:/SEO AD/SEO.env')

from google import genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    print("Testing generate_content with gemini-3.1-flash-image")
    response = client.models.generate_content(
        model='gemini-3.1-flash-image',
        contents='A cute cat'
    )
    print("Success:", response)
    if response.generated_images:
        print("Generated images found.")
except Exception as e:
    print(f"Error: {e}")

