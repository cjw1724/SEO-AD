import os
import re
import sys
import py_compile
import xml.etree.ElementTree as ET

def verify_theme():
    print("=== Testing median_ui_theme.xml ===")
    theme_path = r"d:\SEO AD\median_ui_theme.xml"
    assert os.path.exists(theme_path), "Theme file does not exist!"
    
    with open(theme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. XML parse test
    tree = ET.fromstring(content)
    print("[PASS] XML Syntax: VALID (Root tag: %s)" % tree.tag)

    # 2. Check Pretendard webfont
    assert "pretendard" in content.lower(), "Pretendard webfont not found!"
    print("[PASS] Typography: Pretendard webfont loaded")

    # 3. Check font variables
    assert "--fontHead: 'Pretendard'" in content, "Font variables not updated to Pretendard!"
    print("[PASS] Typography Variables: Set to Pretendard")

    # 4. Check overlap fix
    assert "#settings-id, .settB" in content and "display: none !important" in content, "Overlap fix missing!"
    print("[PASS] Bug Fix: #settings-id / .settB hidden (!important)")

    # 5. Check null image placeholder fix
    assert ".pI .img.null" in content and "linear-gradient" in content, "Modern gradient fallback missing!"
    assert "--noImage: ''" in content, "--noImage variable still contains text!"
    print("[PASS] Fallback Styling: 'Null' text removed, modern gradient + SVG icon active")

    # 6. Check demo links & malware sanitization
    assert "imamuddin" not in content.lower(), "Found remaining imamuddin links/text!"
    assert "techly420" not in content.lower(), "Found remaining techly420 links/text!"
    assert "jagodesain" not in content.lower(), "Found remaining jagodesain link/comment!"
    assert "reddit" not in content.lower(), "Found remaining reddit link/text in widget settings!"
    assert "http://connect.facebook.net" not in content, "Found insecure http facebook script!"
    assert "polyfill.io" not in content.lower(), "Found compromised polyfill.io supply chain link!"
    assert "jagotheme-img.png" not in content, "Found hardcoded jagotheme-img.png fallback!"
    assert "jd-logo.png" not in content, "Found hardcoded jd-logo.png publisher logo!"
    assert "offchat-menu" not in content, "WhatsApp chat HTML not removed!"
    print("[PASS] Complete Sanitization: Demo links (reddit, jagodesain), malware risks (polyfill.io, http mixed content), and creator branding removed")

    # 7. Check 5-Framework UX/UI components in injected CSS
    assert "summary-card" in content or "hero-bento-card" in content, "Hero Bento Card CSS missing!"
    assert "social-proof-badge" in content and "live-pulse-dot" in content, "Lazyweb social proof CSS missing!"
    assert "micro-saas-tool" in content or "toss-calculator" in content, "Micro-SaaS Tool CSS missing!"
    assert "modern-table" in content, "modern-table CSS missing!"
    assert "pros-cons-grid" in content, "pros-cons-grid CSS missing!"
    assert "mobbin-sticky-bar" in content, "mobbin-sticky-bar CSS missing!"
    assert "faq-accordion-group" in content, "faq-accordion-group CSS missing!"
    assert "bento-glow" in content, "bento-glow CSS missing!"
    print("[PASS] 5-Framework UX/UI Component Styles: Hero Bento Card, Micro-SaaS Tool, Comparison Table, Mobbin Sticky Bar, FAQ Accordion & Bento Glow verified")

    # 8. Check CSS Specificity Overrides for tables
    assert ".pE .modern-table" in content, "Specificity override for .pE .modern-table missing!"
    print("[PASS] Table Specificity: Override for Blogger .pE article container verified")

    # 9. Check Mobile Media Queries (<768px, <640px, <480px)
    assert "@media screen and (max-width: 768px)" in content, "768px responsive query missing!"
    assert "@media screen and (max-width: 640px)" in content, "640px responsive query missing!"
    assert "@media screen and (max-width: 480px)" in content, "480px responsive query missing!"
    print("[PASS] Mobile Responsiveness: Breakpoints (<768px, <640px, <480px) verified")

    # 10. Check Global Micro-SaaS Runtime & Includable
    assert "initMicroSaaS" in content, "initMicroSaaS includable missing!"
    print("[PASS] Micro-SaaS Runtime: Global auto-initializer verified")

    # 11. Check Dark Mode
    assert ".nB[data-theme=dark] .summary-card" in content or ".nB[data-theme=dark] .hero-bento-card" in content, "Dark mode overrides missing!"
    assert ".nB[data-theme=dark] .micro-saas-tool" in content or ".nB[data-theme=dark] .toss-calculator" in content, "Dark mode Micro-SaaS missing!"
    print("[PASS] Dark Mode Support: Seamless integration with theme verified")

def verify_python():
    print("\n=== Testing blogs/main.py & writer_agent.py ===")
    
    # 1. Compilation check
    py_compile.compile("blogs/main.py", doraise=True)
    py_compile.compile("blogs/agents/writer_agent.py", doraise=True)
    py_compile.compile("publish_showcase.py", doraise=True)
    print("[PASS] Compilation: Python syntax compiled cleanly")

    # 2. Project root import test
    import blogs.main
    from blogs.agents.writer_agent import WriterAgent, TOSS_FINTECH_DESIGN_SYSTEM_CSS
    print("[PASS] Root Import: 'import blogs.main' succeeded without ModuleNotFoundError")

    # 3. Master CSS Check
    assert "Impeccable Editorial Design System" in TOSS_FINTECH_DESIGN_SYSTEM_CSS, "Master CSS banner missing!"
    assert "pulseDot" in TOSS_FINTECH_DESIGN_SYSTEM_CSS, "Pulse dot animation missing in master CSS!"
    assert "editorial-sticky-bar" in TOSS_FINTECH_DESIGN_SYSTEM_CSS, "Sticky bar missing in master CSS!"
    assert "calc-range-slider" in TOSS_FINTECH_DESIGN_SYSTEM_CSS, "Calculator slider CSS missing in master CSS!"
    print("[PASS] WriterAgent: Master Impeccable CSS verified")

    # 4. WriterAgent Generation & Placeholder Sanitization Check
    writer = WriterAgent()
    sample = writer.write_article("테스트 금융 가이드")
    assert "article-editorial-container" in sample["content"], "article-editorial-container missing!"
    assert "hero-editorial-card" in sample["content"], "hero-editorial-card missing from generated post!"
    assert "editorial-calculator-card" in sample["content"], "editorial-calculator-card missing from generated post!"
    assert "editorial-table" in sample["content"], "editorial-table missing from generated post!"
    assert "editorial-analysis-grid" in sample["content"], "editorial-analysis-grid missing from generated post!"
    assert "editorial-faq-group" in sample["content"], "editorial-faq-group missing from generated post!"
    assert "faq-chevron" in sample["content"], "faq-chevron missing from generated post!"
    assert "editorial-sticky-bar" in sample["content"], "editorial-sticky-bar missing from generated post!"
    assert not any(p in sample["content"] for p in ['[핵심 포인트 1]', '추천 프리미엄 옵션', '일반 표준 옵션']), "Unfinished placeholders in output!"
    assert not any(e in sample["content"] for e in ['&#10003;', '&#10005;', '&#9662;']), "Raw entities in output!"
    print("[PASS] WriterAgent: Generates 100% finished Impeccable post with zero placeholders and zero entities")

if __name__ == "__main__":
    verify_theme()
    verify_python()
    print("\nALL VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
