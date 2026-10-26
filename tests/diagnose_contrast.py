import sys
import os
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

def diagnose():
    with open("data/debug/live_post.html", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    print(f"Total HTML size: {len(html)} bytes")

    # Find style blocks
    style_tags = soup.find_all("style")
    print(f"Found {len(style_tags)} <style> tags")
    for i, tag in enumerate(style_tags):
        print(f"--- Style Block {i+1} (length: {len(tag.text)}) ---")
        for line in tag.text.splitlines()[:25]:
            line_s = line.strip()
            if any(k in line_s for k in ["background", "color", "body", "container", ".blogin"]):
                print("  ", line_s[:100])

    # Find elements with inline style containing background or color
    print("\n--- Inline styled elements with background/color ---")
    styled_elements = soup.find_all(lambda el: el.has_attr("style") and ("background" in el["style"] or "color" in el["style"]))
    for el in styled_elements[:20]:
        tag_name = el.name
        class_name = el.get("class", [])
        style = el.get("style", "")
        text_preview = el.get_text(strip=True)[:40]
        print(f"<{tag_name} class='{class_name}' style='{style[:80]}'> text: '{text_preview}'")

if __name__ == "__main__":
    diagnose()
