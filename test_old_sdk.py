import os
from dotenv import load_dotenv
load_dotenv('d:/SEO AD/SEO.env')

try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    print("Testing old SDK with imagen-3.0-generate-001")
    result = genai.generate_image(
        model="models/imagen-3.0-generate-001",
        prompt="A cute cat"
    )
    print("Success:", result)
except ImportError:
    print("google-generativeai is not installed in this environment.")
except Exception as e:
    print(f"Error: {e}")
