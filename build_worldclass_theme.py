import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/SEO AD/jettheme_v2_raw.xml', 'r', encoding='utf-8') as f:
    xml = f.read()

print("Original JetTheme length:", len(xml))

# 1. Colors and Variables
# Change keycolor to Toss/Fintech Royal Blue (#2563EB)
xml = xml.replace('value="#f67938"', 'value="#2563EB"')
xml = xml.replace('default="#f67938"', 'default="#2563EB"')
xml = xml.replace('value="#f46013"', 'value="#1D4ED8"')
xml = xml.replace('default="#f46013"', 'default="#1D4ED8"')

# 2. Typography: Pretendard Font Injection in <b:skin>
pretendard_font_css = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');
:root {
  --bs-font-sans-serif: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, "Helvetica Neue", "Segoe UI", sans-serif !important;
  --font-stack: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, "Helvetica Neue", "Segoe UI", sans-serif !important;
}
body, .h1, .h2, .h3, .h4, .h5, .h6, h1, h2, h3, h4, h5, h6, .navbar-brand, .nav-link {
  font-family: var(--bs-font-sans-serif) !important;
  word-break: keep-all;
  letter-spacing: -0.02em;
}
"""

# Insert Pretendard font at the start of b:skin
xml = xml.replace('<b:skin><![CDATA[', '<b:skin><![CDATA[' + pretendard_font_css)

# 3. Add AdSense Verification & Guarded Script in <head>
adsense_guard = """
  <!-- Google AdSense Official Script (Guarded: Never load on 404, search, archive, or empty screens) -->
  <b:if cond='data:view.isSingleItem and not data:view.isError and not data:view.isArchive and not data:view.isSearch'>
    <script async='async' crossorigin='anonymous' src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2174726915215446'></script>
  </b:if>

  <!-- AdSense Non-Content Screen Killswitch -->
  <b:if cond='data:view.isError or data:view.isArchive or data:view.isSearch'>
    <script type='text/javascript'>
      /* <![CDATA[ */
      window.adsbygoogle = { push: function() { console.log('AdSense suppressed on non-content screen'); } };
      /* ]]> */
    </script>
  </b:if>

  <!-- Smart Search: Google CSE & AdSense for Search (AFS) Token -->
  <script type='text/javascript'>
    /* <![CDATA[ */
    window.B365_CSE_CX = '863c2f0c96b064551';
    /* ]]> */
  </script>
"""
xml = xml.replace('<head>', '<head>\n' + adsense_guard)

# 4. Brand Logo (HTML10)
logo_html = """<![CDATA[<div style="display:flex;align-items:center;gap:8px;"><span style="font-size:22px;font-weight:900;letter-spacing:-0.03em;color:#0F172A;">Blogin <span style="color:#2563EB;">365</span> AI</span><span style="display:inline-block;padding:2px 8px;font-size:11px;font-weight:700;color:#2563EB;background:#EFF6FF;border-radius:12px;border:1px solid #BFDBFE;">SMART MEDIA</span></div>]]>"""

xml = re.sub(
    r"(<b:widget id='HTML10'[^>]*>[\s\S]*?<b:widget-setting name='content'>)[\s\S]*?(</b:widget-setting>)",
    r"\g<1>" + logo_html + r"\2",
    xml
)

# 5. Header Navigation Menu (LinkList11)
menu_items = """
    <b:widget-settings>
      <b:widget-setting name='sorting'>NONE</b:widget-setting>
      <b:widget-setting name='text-0'>홈</b:widget-setting>
      <b:widget-setting name='link-0'>https://blogin365ai.blogspot.com/</b:widget-setting>
      <b:widget-setting name='text-1'>정부지원금</b:widget-setting>
      <b:widget-setting name='link-1'>https://blogin365ai.blogspot.com/search/label/지원금?max-results=10</b:widget-setting>
      <b:widget-setting name='text-2'>통신·알뜰폰</b:widget-setting>
      <b:widget-setting name='link-2'>https://blogin365ai.blogspot.com/search/label/통신?max-results=10</b:widget-setting>
      <b:widget-setting name='text-3'>대출·금융</b:widget-setting>
      <b:widget-setting name='link-3'>https://blogin365ai.blogspot.com/search/label/금융?max-results=10</b:widget-setting>
      <b:widget-setting name='text-4'>보험·절약</b:widget-setting>
      <b:widget-setting name='link-4'>https://blogin365ai.blogspot.com/search/label/보험?max-results=10</b:widget-setting>
      <b:widget-setting name='text-5'>2026 복지정책</b:widget-setting>
      <b:widget-setting name='link-5'>https://blogin365ai.blogspot.com/search/label/정책?max-results=10</b:widget-setting>
    </b:widget-settings>
"""

xml = re.sub(
    r"(<b:widget id='LinkList11'[^>]*>)\s*<b:widget-settings>[\s\S]*?</b:widget-settings>",
    r"\g<1>" + menu_items,
    xml
)

# 6. Korean Search Input Placeholder
xml = xml.replace(
    "placeholder='Search...'",
    "placeholder='정부지원금, 요금제, 대출 금리 비교 검색...'"
)
xml = xml.replace(
    'placeholder="Search..."',
    'placeholder="정부지원금, 요금제, 대출 금리 비교 검색..."'
)

# 7. Card Layout Enhancement in JetArchive (Fallback gradient banner when no thumbnail exists)
# Let's inspect JetArchive thumbnail logic
old_thumb = """<b:if cond='data:post.featuredImage'>

<div class='item-thumbnail'>

<a class='jt-bg-light d-block ratio ratio-16x9' expr:href='data:post.url.canonical' rel='bookmark'>  

<img expr:alt='data:post.title' expr:class='data:post.featuredImage.isYoutube ?  &quot;object-cover lazyload&quot; : &quot;lazyload&quot;' expr:data-src='data:post.featuredImage.isYoutube ? data:post.thumbnailUrl : data:post.featuredImage' loading='lazy' src='data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='/>

</a>

</div>

</b:if>"""

new_thumb = """<b:if cond='data:post.featuredImage'>
<div class='item-thumbnail'>
<a class='jt-bg-light d-block ratio ratio-16x9' expr:href='data:post.url.canonical' rel='bookmark'>  
<img expr:alt='data:post.title' expr:class='data:post.featuredImage.isYoutube ?  &quot;object-cover lazyload&quot; : &quot;lazyload&quot;' expr:data-src='data:post.featuredImage.isYoutube ? data:post.thumbnailUrl : data:post.featuredImage' loading='lazy' src='data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='/>
</a>
</div>
<b:else/>
<!-- Elegant Category Fallback Banner (No empty boxes or star icons!) -->
<div class='item-thumbnail'>
<a class='d-block ratio ratio-16x9' expr:href='data:post.url.canonical' rel='bookmark' style='background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #3B82F6 100%); display: flex; align-items: center; justify-content: center; text-decoration: none;'>
  <div style='position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; text-align: center; color: #FFFFFF;'>
    <div style='font-size: 32px; margin-bottom: 8px;'>📊</div>
    <div style='font-size: 13px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; opacity: 0.9;'>Blogin 365 AI 가이드</div>
  </div>
</a>
</div>
</b:if>"""

if old_thumb in xml:
    xml = xml.replace(old_thumb, new_thumb)
    print("JetArchive thumbnail replacement: SUCCESS!")
else:
    print("JetArchive thumbnail replacement: Fallback pattern matching...")
    xml = re.sub(
        r"<b:if cond='data:post\.featuredImage'>\s*<div class='item-thumbnail'>[\s\S]*?</div>\s*</b:if>",
        new_thumb,
        xml,
        count=1
    )

# 7.5 Polish Items: Editorial Banner, Hide Dummy Social Icons, Zero-Persona Author
# Replace HTML11 placeholder with high-trust official notice banner
editorial_banner_html = """<![CDATA[
<div style="background: linear-gradient(90deg, #EFF6FF 0%, #F8FAFC 100%); border: 1px solid #BFDBFE; border-radius: 12px; padding: 12px 18px; margin: 12px 0 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
  <div style="display: flex; align-items: center; gap: 10px;">
    <span style="display: inline-block; padding: 3px 8px; font-size: 11px; font-weight: 800; background: #2563EB; color: #FFFFFF; border-radius: 6px;">공식 고시</span>
    <span style="font-size: 13px; font-weight: 700; color: #1E3A8A;">2026 대한민국 정부지원금 · 통신비 절약 · 다이렉트 보험 팩트체크 센터</span>
  </div>
  <div style="font-size: 12px; color: #64748B; font-weight: 600;">실시간 공시 약관 기준 검증 완료 ✓</div>
</div>
]]>"""
xml = re.sub(
    r"(<b:widget id='HTML11'[^>]*>[\s\S]*?<b:widget-setting name='content'>)[\s\S]*?(</b:widget-setting>)",
    r"\g<1>" + editorial_banner_html + r"\2",
    xml
)

# Remove all example-ads placeholders across all widgets
xml = xml.replace('<hr class="example-ads"/>', '')

# Hide dummy social icons by adding #Icons to LinkList10 title
xml = xml.replace("title='Icons, Dark, Search'", "title='#Icons, Dark, Search'")
xml = xml.replace('title="Icons, Dark, Search"', 'title="#Icons, Dark, Search"')

# Zero-Persona Policy: Replace Dobby / any author name with official branding
xml = xml.replace("<data:post.author.name/>", "Blogin 365 AI 에디토리얼 팀")

# 8. Footer Widgets - Inject Mandatory AdSense 4 Policy Links
footer_policy_links = """
<!-- Mandatory AdSense Trust & Policy Links -->
<div class='b365-footer-policy-links' style='display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; font-size: 14px; font-weight: 700; align-items: center;'>
  <a href='https://blogin365ai.blogspot.com/p/about-us-blogin-365-ai.html' style='color: #60A5FA; text-decoration: none;'>블로그 소개 (About Us)</a>
  <span style='color: #4B5563;'>|</span>
  <a href='https://blogin365ai.blogspot.com/p/privacy-policy.html' style='color: #60A5FA; text-decoration: none;'>개인정보처리방침 (Privacy Policy)</a>
  <span style='color: #4B5563;'>|</span>
  <a href='https://blogin365ai.blogspot.com/p/terms-of-service.html' style='color: #60A5FA; text-decoration: none;'>이용약관 (Terms of Service)</a>
  <span style='color: #4B5563;'>|</span>
  <a href='https://blogin365ai.blogspot.com/p/contact-us.html' style='color: #60A5FA; text-decoration: none;'>문의하기 (Contact Us)</a>
</div>
<div style='font-size: 13px; line-height: 1.6; color: #9CA3AF; margin-bottom: 14px;'>
  본 블로그(Blogin 365 AI)는 대한민국 국민을 위한 2026 정부지원금, 알뜰폰·통신비 절약, 다이렉트 보험료 비교, 고금리 예적금 및 정책 대출 정보를 신뢰할 수 있는 공공 데이터와 공식 고시를 바탕으로 전문 에디토리얼 팀이 직접 분석하여 제공합니다.
</div>
"""

# Replace HTML21 (About Us) content
xml = re.sub(
    r"(<b:widget id='HTML21'[^>]*>[\s\S]*?<b:widget-setting name='content'>)[\s\S]*?(</b:widget-setting>)",
    r"\g<1><![CDATA[" + footer_policy_links + r"]]>\2",
    xml
)

# Update LinkList13 (Learn More) in Footer
footer_links = """
    <b:widget-settings>
      <b:widget-setting name='sorting'>NONE</b:widget-setting>
      <b:widget-setting name='text-0'>블로그 소개</b:widget-setting>
      <b:widget-setting name='link-0'>https://blogin365ai.blogspot.com/p/about-us-blogin-365-ai.html</b:widget-setting>
      <b:widget-setting name='text-1'>개인정보처리방침</b:widget-setting>
      <b:widget-setting name='link-1'>https://blogin365ai.blogspot.com/p/privacy-policy.html</b:widget-setting>
      <b:widget-setting name='text-2'>이용약관</b:widget-setting>
      <b:widget-setting name='link-2'>https://blogin365ai.blogspot.com/p/terms-of-service.html</b:widget-setting>
      <b:widget-setting name='text-3'>문의하기 (고객센터)</b:widget-setting>
      <b:widget-setting name='link-3'>https://blogin365ai.blogspot.com/p/contact-us.html</b:widget-setting>
    </b:widget-settings>
"""

xml = re.sub(
    r"(<b:widget id='LinkList13'[^>]*>)\s*<b:widget-settings>[\s\S]*?</b:widget-settings>",
    r"\g<1>" + footer_links,
    xml
)

# Copyright notice in HTML23
copyright_html = """<![CDATA[<div>© 2026 <strong>Blogin 365 AI</strong> · 스마트 라이프 에디토리얼 팀. All Rights Reserved.</div>]]>"""
xml = re.sub(
    r"(<b:widget id='HTML23'[^>]*>[\s\S]*?<b:widget-setting name='content'>)[\s\S]*?(</b:widget-setting>)",
    r"\g<1>" + copyright_html + r"\2",
    xml
)

# Save the final customized XML
target_path = 'd:/SEO AD/blogin365_worldclass_theme.xml'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(xml)

print(f"Generated {target_path} successfully! Length: {len(xml)} bytes, {len(xml.splitlines())} lines.")
