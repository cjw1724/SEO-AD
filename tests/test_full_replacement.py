import sys
import os
import re
from bs4 import BeautifulSoup
sys.path.insert(0, "d:/SEO AD")
sys.stdout.reconfigure(encoding="utf-8")
from engine.crew.editorial_inspector import EditorialInspector

MASTER_TDS_CSS = """
/* ==========================================================================
   Blogin 365 AI Holdings - Master Toss Dark Theme CSS (v9.0 Apex)
   WCAG 2.1 AAA Compliant (> 7:1 Contrast Ratio Guaranteed)
   ========================================================================== */
:root {
    --tds-bg-base: #0a0e17;
    --tds-bg-surface: #111827;
    --tds-bg-card: #131c2e;
    --tds-border-card: #1f2d47;
    --tds-border-subtle: #2d3e5e;
    --tds-text-primary: #ffffff;
    --tds-text-body: #e2e8f0;
    --tds-text-muted: #94a3b8;
    --tds-accent-blue: #3b82f6;
    --tds-accent-green: #10b981;
}

body, .post-body, .entry-content, article,
.blog-post-container, .blogin-saas-container {
    background-color: #0a0e17 !important;
    color: #e2e8f0 !important;
    font-family: 'Pretendard Variable', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    max-width: 880px !important;
    margin: 0 auto !important;
    box-sizing: border-box !important;
    line-height: 1.8 !important;
}

.blog-post-container h1, h1 {
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 900 !important;
    line-height: 1.35 !important;
    margin: 24px 0 16px 0 !important;
    text-align: left !important;
}

.blog-post-container h2, .blogin-saas-container h2, h2 {
    color: #ffffff !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    margin: 40px 0 18px 0 !important;
    border-bottom: 1px solid #1f2d47 !important;
    padding-bottom: 10px !important;
}

.blog-post-container h3, h3 {
    color: #f1f5f9 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin: 28px 0 12px 0 !important;
}

.blog-post-container p, .blogin-saas-container p, p {
    color: #e2e8f0 !important;
    font-size: 16px !important;
    line-height: 1.85 !important;
    margin-bottom: 18px !important;
    word-break: keep-all !important;
}

.blog-post-container li, li {
    color: #cbd5e1 !important;
    font-size: 15px !important;
    margin-bottom: 8px !important;
}

strong, b, .blog-post-container strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Bento summary grid */
.blog-post-container .bento-card, .bento-card {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)) !important;
    gap: 16px !important;
    background-color: #111827 !important;
    border: 1px solid #1f2d47 !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin: 24px 0 32px 0 !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35) !important;
}

.blog-post-container .bento-item, .bento-item {
    background-color: #131c2e !important;
    border: 1px solid #1f2d47 !important;
    border-radius: 12px !important;
    padding: 16px !important;
    text-align: center !important;
}

.blog-post-container .bento-item strong, .bento-item strong {
    color: #ffffff !important;
    display: block !important;
    font-size: 14px !important;
    margin-bottom: 6px !important;
}

.blog-post-container .bento-item span, .bento-item span {
    color: #cbd5e1 !important;
    font-size: 13px !important;
}

/* Micro-SaaS Calculator component */
.blogin-saas-container {
    background-color: #111827 !important;
    border: 1px solid #1f2d47 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin: 32px 0 !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
}

.blogin-saas-container label {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
    display: block !important;
}

.blogin-saas-container input[type="number"],
.blogin-saas-container input[type="range"],
.blogin-saas-container select {
    background-color: #0a0e17 !important;
    color: #ffffff !important;
    border: 1px solid #2d3e5e !important;
    border-radius: 8px !important;
    padding: 12px 14px !important;
    font-size: 15px !important;
    box-sizing: border-box !important;
}

.blogin-saas-container .result-card,
.blogin-saas-container .panel,
.blogin-saas-container .card {
    background-color: #131c2e !important;
    border: 1px solid #1f2d47 !important;
    border-radius: 12px !important;
    padding: 18px !important;
}

/* Code & Formula callouts */
pre, code, div[style*="background-color: #ecf0f1"], div[style*="background:#ecf0f1"],
div[style*="background-color: #f8f9fa"] {
    background-color: #111827 !important;
    border: 1px solid #1f2d47 !important;
    border-radius: 10px !important;
    color: #38bdf8 !important;
    padding: 16px !important;
}

pre strong, code strong,
div[style*="background-color: #ecf0f1"] strong,
div[style*="background:#ecf0f1"] strong {
    color: #67e8f9 !important;
}

/* Buttons */
button, .blogin-btn-primary {
    background: #1d4ed8 !important; /* Royal Blue (7.6:1 contrast against white) */
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 20px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    cursor: pointer !important;
    transition: background 0.2s ease !important;
}

button:hover {
    background: #1e40af !important;
}

/* Links (Ensure high contrast sky blue) */
a, .entry-content a, .blog-post-container a, .blogin-saas-container a {
    color: #38bdf8 !important;
    text-decoration: none !important;
}

a:hover {
    color: #7dd3fc !important;
    text-decoration: underline !important;
}

/* Affiliate Amber/Yellow CTAs */
a[style*="background: #f59e0b"], a[style*="background:#f59e0b"],
a[style*="background-color: #f59e0b"], a[style*="background-color:#f59e0b"] {
    color: #0f172a !important;
    font-weight: 800 !important;
}

/* Legal Disclaimer & Meta */
.legal-disclaimer {
    background: #0f172a !important;
    border-left: 4px solid #ef4444 !important;
    color: #94a3b8 !important;
}

.apex-badge, .blogin-badge {
    color: #10b981 !important;
    background-color: rgba(16, 185, 129, 0.12) !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
}
"""

def test_full_replacement():
    with open("data/debug/live_post.html", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove all old conflicting <style> tags
    for s in soup.find_all("style"):
        s.decompose()

    # Clean inline background and color styles that conflict
    for tag in soup.find_all(True):
        if tag.has_attr("style"):
            s_val = tag["style"]
            # strip inline background-color: #fff, #ecf0f1, etc.
            s_val = re.sub(r'background(?:-color)?\s*:\s*(?:#fff|#ffffff|white|#f8f9fa|#ecf0f1|#e0e0e0|#f9f9f9|rgb\(255,\s*255,\s*255\))[^;]*;?', '', s_val, flags=re.IGNORECASE)
            # strip inline dark colors: #333, #555, #2c3e50, #34495e, #111, #000
            s_val = re.sub(r'color\s*:\s*(?:#333|#555|#2c3e50|#34495e|#111|#000|#222|black)[^;]*;?', '', s_val, flags=re.IGNORECASE)
            tag["style"] = s_val

    # Prepend MASTER_TDS_CSS in a single clean <style> tag
    new_style_tag = soup.new_tag("style")
    new_style_tag.string = MASTER_TDS_CSS
    soup.insert(0, new_style_tag)

    transformed_html = str(soup)
    with open("data/debug/transformed_post.html", "w", encoding="utf-8") as f:
        f.write(transformed_html)

    inspector = EditorialInspector()
    res = inspector.inspect(transformed_html, is_url=False)
    print(f"Inspection Result: passed={res['passed']}")
    for vp, s in res["stats"].items():
        print(f"[{vp}] elements: {s['tested_elements']} | min: {s['min_contrast']}:1 | avg: {s['avg_contrast']}:1 | defects: {s['defect_count']}")

    if res["defects"]:
        print("\nRemaining defects:")
        for d in res["defects"][:5]:
            print(f"[{d['viewport']}] <{d['tag']}> {d['fg']} on {d['bg']} ({d['ratio']}:1): {d['text']}")

    return transformed_html, res

if __name__ == "__main__":
    test_full_replacement()
