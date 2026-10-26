"""
Blogin 365 AI Holdings - Deploy Vibe Trading Station Page to Blogger (v9.0 Apex)
Deploys or updates the permanent static page for Vibe Trading & Leaderboard.
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from googleapiclient.discovery import build
from engine.publisher.blogger_gateway import BloggerGateway
from engine.fintech.vibe_trading_station import VibeTradingStation

sys.stdout.reconfigure(encoding="utf-8")

def deploy_vibe_station_page():
    print("=" * 78)
    print("🚀 [VIBE TRADING] Blogger 상설 프로 트레이딩 스테이션 페이지 배포 시작")
    print("=" * 78)

    station = VibeTradingStation()
    station_html = station.generate_station_html()
    print(f" -> Vibe Trading Station HTML 생성 완료 ({len(station_html)} bytes)")

    gw = BloggerGateway()
    creds = gw._get_authenticated_credentials()
    service = build("blogger", "v3", credentials=creds)

    page_title = "VIBE TRADING - 실시간 퀀트 모의투자 & 랭킹 배틀"

    # Check if page already exists
    pages_list = service.pages().list(blogId=gw.blog_id).execute().get("items", [])
    existing_page = next((p for p in pages_list if "VIBE TRADING" in p.get("title", "")), None)

    if existing_page:
        page_id = existing_page.get("id")
        print(f" -> 기존 Vibe Trading 페이지 감지 (ID: {page_id}). 원격 패치(Update) 수행...")
        body = {
            "title": page_title,
            "content": station_html
        }
        res = service.pages().patch(blogId=gw.blog_id, pageId=page_id, body=body).execute()
        page_url = res.get("url")
        print(f" -> [성공] 기존 페이지 원격 업데이트 완료: {page_url}")
    else:
        print(" -> 신규 Vibe Trading 상설 페이지 생성(Insert) 수행...")
        res = gw.publish_page(title=page_title, html_content=station_html, is_draft=False)
        if not res.get("success"):
            raise RuntimeError(f"Blogger 페이지 발행 실패: {res.get('error')}")
        page_url = res.get("url")
        page_id = res.get("id")
        print(f" -> [성공] 신규 상설 페이지 발행 완료: {page_url}")

    # Also record in data/vibe_trading_meta.json
    meta = {
        "page_id": page_id,
        "page_title": page_title,
        "page_url": page_url,
        "deployed_at": "2026-10-26"
    }
    meta_path = os.path.join(BASE_DIR, "data", "vibe_trading_meta.json")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print("\n" + "═" * 78)
    print("✨ [VIBE TRADING DEPLOYED] 실시간 모의투자 & 랭킹 배틀 상설 개장 완료!")
    print(f"• 상설 페이지 URL : {page_url}")
    print(f"• 페이지 ID       : {page_id}")
    print("═" * 78)

    return res

if __name__ == "__main__":
    deploy_vibe_station_page()
