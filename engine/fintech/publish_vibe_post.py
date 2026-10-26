"""
Blogin 365 AI Holdings - Flagship Vibe Trading Post Publisher (v9.0 Apex)
Publishes the flagship VIBE TRADING post to the top of the blog homepage.
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.publisher.blogger_gateway import BloggerGateway
from engine.crew.publisher import MicroSaaSBloggerPublisher
from engine.crew.thumbnail_generator import create_thumbnail_sync
from engine.crew.image_uploader import ImageUploader
from engine.crew.editorial_inspector import EditorialInspector
from engine.fintech.vibe_trading_station import VibeTradingStation

sys.stdout.reconfigure(encoding="utf-8")

def build_flagship_post_html() -> str:
    station = VibeTradingStation()
    station_html = station.generate_station_html()

    # Extract body content from station_html
    body_start = station_html.find("<body>")
    body_end = station_html.find("</body>")
    if body_start != -1 and body_end != -1:
        inner_content = station_html[body_start + 6:body_end]
    else:
        inner_content = station_html

    full_html = f"""
<div class="blogin-vibe-flagship-wrapper" style="max-width:960px; margin:0 auto; font-family:'Pretendard Variable', -apple-system, sans-serif;">

  <!-- Hero Header Box -->
  <div style="background:linear-gradient(135deg, #0d1527 0%, #172554 100%); border:1px solid #1e3a8a; border-radius:20px; padding:32px 28px; margin-bottom:32px; box-shadow:0 12px 36px rgba(0,0,0,0.45); text-align:center;">
    <span style="display:inline-block; background:#2563eb; color:#ffffff; font-size:12px; font-weight:800; padding:5px 12px; border-radius:8px; letter-spacing:0.05em; margin-bottom:12px;">FLAGSHIP FINTECH RELEASE</span>
    <h1 style="color:#ffffff; font-size:28px; font-weight:900; margin:0 0 12px 0; letter-spacing:-0.03em; word-break:keep-all;">
      🔥 [공식 개장] VIBE TRADING: 실시간 트레이딩뷰 차트 & 1x~20x 모의투자 랭킹 배틀
    </h1>
    <p style="color:#cbd5e1; font-size:16px; line-height:1.7; max-width:760px; margin:0 auto 20px auto; word-break:keep-all;">
      실제 자본 손실 없이 가상 자금 <strong>$10,000 USDT (약 1,380만 원)</strong>로 BTC, ETH, SOL, NVDA 1x~20x 레버리지 롱/숏 실전 모의투자를 즐기세요. 실시간으로 갱신되는 <strong>Top 10 명예의 전당</strong>에서 전 세계 트레이더들과 수익률 랭킹전을 벌일 수 있습니다!
    </p>
    <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
      <a href="https://blogin365ai.blogspot.com/p/vibe-trading.html" target="_blank" style="display:inline-flex; align-items:center; gap:8px; background:#10b981; color:#ffffff !important; font-weight:800; font-size:14px; padding:12px 24px; border-radius:12px; text-decoration:none; box-shadow:0 4px 14px rgba(16,185,129,0.4);">
        🖥️ 전체 화면 전용 스테이션 열기 →
      </a>
      <a href="#vibe-terminal-anchor" style="display:inline-flex; align-items:center; gap:8px; background:#1e293b; color:#38bdf8 !important; border:1px solid #38bdf8; font-weight:800; font-size:14px; padding:12px 24px; border-radius:12px; text-decoration:none;">
        ⚡ 본문에서 바로 트레이딩 시작 ↓
      </a>
    </div>
  </div>

  <!-- Anchor to Interactive Terminal -->
  <div id="vibe-terminal-anchor">
    {inner_content}
  </div>

  <!-- Educational Quant Guide & Strategies -->
  <div style="margin-top:48px; padding:28px; background:#111827; border:1px solid #1f2d47; border-radius:16px;">
    <h2 style="color:#ffffff; font-size:22px; font-weight:800; border-bottom:1px solid #1f2d47; padding-bottom:10px; margin-bottom:18px;">
      💡 퀀트 트레이더를 위한 레버리지 & 켈리 공식 리스크 관리 가이드
    </h2>

    <p style="color:#e2e8f0; font-size:15px; line-height:1.8; margin-bottom:16px;">
      레버리지 트레이딩은 기대 수익을 수 배로 증폭시키지만, 동시에 청산 리스크를 기하급수적으로 키웁니다. VIBE TRADING 시뮬레이터는 수학적 확률 모델인 <strong>켈리 공식(Kelly Criterion)</strong>을 내장하여 트레이더의 계좌 파산을 원천 방어합니다.
    </p>

    <div style="background:#0a0e17; border:1px solid #2d3e5e; border-radius:12px; padding:18px; margin-bottom:20px;">
      <strong style="color:#38bdf8; display:block; font-size:15px; margin-bottom:8px;">📐 실시간 청산가(Liquidation Price) 계산 원리</strong>
      <p style="color:#cbd5e1; font-size:13px; line-height:1.7; margin:0;">
        • <strong>롱(Long) 청산가</strong> = 진입가 × (1 - 1/레버리지 + 유지증거금률 0.5%)<br>
        • <strong>숏(Short) 청산가</strong> = 진입가 × (1 + 1/레버리지 - 유지증거금률 0.5%)<br>
        10배 레버리지 진입 시 진입가 대비 약 -9.5% 변동 시 전액 강제 청산되므로, 분할 진입과 손절 라인 준수가 핵심입니다.
      </p>
    </div>

    <div style="background:#0a0e17; border:1px solid #2d3e5e; border-radius:12px; padding:18px;">
      <strong style="color:#10b981; display:block; font-size:15px; margin-bottom:8px;">🏆 Top 10 리더보드 공략법</strong>
      <p style="color:#cbd5e1; font-size:13px; line-height:1.7; margin:0;">
        1. 닉네임 입력창에 본인의 트레이더 핸들(예: 압구정불개미)을 등록하세요.<br>
        2. 시세 흐름에 맞춰 롱/숏 포지션을 체결하고 목표 수익 도달 시 '청산' 버튼을 누릅니다.<br>
        3. 실현 수익률이 갱신되는 즉시 Top 10 명예의 전당 순위가 실시간으로 재배열됩니다.<br>
        4. '랭킹 공유' 버튼을 눌러 친구들에게 도전장 링크를 보내보세요!
      </p>
    </div>
  </div>

</div>
"""
    return full_html

def publish_flagship_vibe_post():
    print("=" * 78)
    print("🏢 [Blogin 365 AI Holdings] VIBE TRADING 홈 피드 1위 플래그십 포스트 발행 시작")
    print("=" * 78)

    title = "🔥 [공식 개장] VIBE TRADING: 실시간 트레이딩뷰 차트 & 1x~20x 모의투자 랭킹 배틀"
    slug = "vibe-trading-live-simulator"
    labels = ["Vibe Trading", "모의투자", "트레이딩뷰", "비트코인", "FinTech", "투자랭킹"]

    print("\n[Step 1/4] 고해상도 WebP 썸네일 생성 중...")
    thumb_dir = os.path.join(BASE_DIR, "data", "thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)
    thumb_path = create_thumbnail_sync(
        filename="thumb_vibe_trading",
        title="VIBE TRADING 모의투자 랭킹전",
        formula_badge="PRO QUANT TERMINAL",
        key_stat="가상자금 $10,000 | 1x-20x",
        sub_label="실시간 트레이딩뷰 & Top 10 리더보드 배틀",
        output_dir=thumb_dir
    )
    print(f" -> 로컬 썸네일 캡처 완료: {thumb_path}")

    print("\n[Step 2/4] 썸네일 이미지 외부 호스팅 업로드...")
    uploader = ImageUploader()
    upload_res = uploader.upload_image(thumb_path)
    thumb_url = upload_res.get("url")
    print(f" -> 호스팅된 썸네일 URL: {thumb_url}")

    print("\n[Step 3/4] 플래그십 포스트 HTML 조립 및 실물 가독성 검수...")
    post_html = build_flagship_post_html()
    inspector = EditorialInspector()
    post_html, review = inspector.inspect_and_heal(post_html)
    print(f" -> 8인 AI 직원 실물 검수 완료 (자가치유 여부: {review.get('healed', False)})")

    print("\n[Step 4/4] Blogger API v3로 실제 LIVE 포스트 발행 집행 (홈 화면 1순위 등록)...")
    publisher = MicroSaaSBloggerPublisher()
    record = publisher.publish_post(
        title=title,
        html_content=post_html,
        thumbnail_url=thumb_url,
        keyword="Vibe Trading 모의투자 랭킹전",
        labels=labels,
        dry_run=False,
        english_slug=slug
    )

    print("\n" + "═" * 78)
    print("✨ [SUCCESS] VIBE TRADING 플래그십 포스트 홈 화면 1위 등록 완료!")
    print(f"• 포스트 제목 : {record.get('title')}")
    print(f"• 발행 URL   : {record.get('url')}")
    print(f"• 포스트 ID   : {record.get('post_id')}")
    print("═" * 78 + "\n")

    return record

if __name__ == "__main__":
    publish_flagship_vibe_post()
