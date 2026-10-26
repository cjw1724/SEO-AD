import sys
import os
sys.path.insert(0, "d:/SEO AD")
sys.stdout.reconfigure(encoding="utf-8")
from engine.crew.editorial_inspector import EditorialInspector

inspector = EditorialInspector()
res = inspector.inspect("https://blogin365ai.blogspot.com/2026/10/overseas-stock-capital-gains-tax_0871534011.html", is_url=True)
print(f"Total defects: {len(res['defects'])}")
for d in res['defects'][:20]:
    print(f"[{d['viewport']}] <{d['tag']}> fg:{d['fg']} bg:{d['bg']} ratio:{d['ratio']}:1 | text: '{d['text'][:40]}'")
