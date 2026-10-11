import os
import sys

# Ensure d:\SEO AD is in path so we can import blogs.tools
sys.path.append(r"d:\SEO AD")

from blogs.tools import generate_thumbnail_tool

os.environ["GEMINI_API_KEY"] = "DUMMY_KEY_FOR_TEST"

print("Calling generate_thumbnail_tool...")
res = generate_thumbnail_tool.run({"prompt": "A small dog"})
print("Result:")
print(res)
