import os
from dotenv import load_dotenv

# Load from SEO.env
load_dotenv('d:/SEO AD/SEO.env')

from blogs.tools import generate_thumbnail_tool

print("Running generate_thumbnail_tool...")
result = generate_thumbnail_tool.run("A cute cat")
print("Result:")
print(result)
