import os
from dotenv import load_dotenv

load_dotenv("SEO.env")

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blogs.tools import generate_thumbnail_tool

def test_tool():
    print("Running generate_thumbnail_tool...")
    result = generate_thumbnail_tool.run(prompt="A beautiful sunset over the mountains")
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    test_tool()
