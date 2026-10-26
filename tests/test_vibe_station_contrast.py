import sys
import os
sys.path.insert(0, "d:/SEO AD")
sys.stdout.reconfigure(encoding="utf-8")
from engine.fintech.vibe_trading_station import VibeTradingStation
from engine.crew.editorial_inspector import EditorialInspector

station = VibeTradingStation()
html = station.generate_station_html()

inspector = EditorialInspector()
res = inspector.inspect(html, is_url=False)
print(f"Vibe Station Inspection: passed={res['passed']}")
for vp, s in res["stats"].items():
    print(f"[{vp}] elements: {s['tested_elements']} | min: {s['min_contrast']}:1 | avg: {s['avg_contrast']}:1 | defects: {s['defect_count']}")

if res["defects"]:
    print(f"Total defects: {len(res['defects'])}")
    for d in res["defects"][:5]:
        print(f" - [{d['viewport']}] <{d['tag']}> {d['fg']} on {d['bg']} ({d['ratio']}:1): {d['text']}")
else:
    print("✨ ALL ELEMENTS PASSED WCAG AAA CONTRAST GATE!")
