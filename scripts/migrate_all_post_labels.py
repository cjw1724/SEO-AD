# -*- coding: utf-8 -*-
"""
scripts/migrate_all_post_labels.py
----------------------------------
Migrates all published Blogger posts to the 4 Canonical Authority Pillars:
1. 💰 경제·금융 (Finance & Economy)
2. 🏥 생활·건강 (Health & Medical)
3. 🏛️ 정책·복지 (Policy & Welfare)
4. 💡 생활·소비 (Smart Living & Savings)
"""

import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.publisher.blogger_gateway import BloggerGateway
from engine.matcher.universal_topic_engine import resolve_canonical_pillar

def run_migration():
    gw = BloggerGateway()
    posts = gw.list_all_posts(max_posts=100)
    print(f"==================================================")
    print(f"🚀 [카테고리 마이그레이션] 총 {len(posts)}개 포스트 전수 검사 개시")
    print(f"==================================================")

    updated_count = 0
    skipped_count = 0
    pillar_counts = {}

    for i, p in enumerate(posts, start=1):
        pid = p["id"]
        title = p["title"]
        old_labels = p.get("labels", [])

        # Determine canonical pillar
        combined_text = title + " " + " ".join(old_labels)
        pillar = resolve_canonical_pillar("", combined_text)
        pillar_counts[pillar] = pillar_counts.get(pillar, 0) + 1

        # Clean legacy internal codes
        cleaned_labels = [l for l in old_labels if l.upper() not in ["HAIR", "MEDICAL", "SUBSIDY", "SAVINGS", "TECH", "CAREER"]]

        # Prepend canonical pillar
        new_labels = [pillar] + [l for l in cleaned_labels if l != pillar]

        if old_labels == new_labels:
            print(f"[{i:02d}/{len(posts)}] ⏭️ 이미 최신 상태: [{pillar}] {title[:35]}...")
            skipped_count += 1
            continue

        print(f"[{i:02d}/{len(posts)}] 🔄 패치 중: [{pillar}] {title[:35]}...")
        print(f"       이전: {old_labels[:4]}")
        print(f"       신규: {new_labels[:4]}")

        res = gw.patch_labels(pid, new_labels)
        if res.get("success"):
            print(f"       ✅ 성공 (시도: {res.get('attempts')})")
            updated_count += 1
        else:
            print(f"       ❌ 실패: {res.get('error')}")

        time.sleep(0.5)

    print("\n==================================================")
    print(f"🎉 [마이그레이션 완료] 갱신: {updated_count}건 | 유지: {skipped_count}건")
    print(f"--- 4대 필라별 최종 포스트 분포 ---")
    for k, v in pillar_counts.items():
        print(f"  - {k}: {v}건")
    print(f"==================================================")

if __name__ == "__main__":
    run_migration()
