import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure project root is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from engine.radar.trend_scout import fetch_google_trends_kr
from engine.matcher.demand_matcher import match_trends_with_demand
from engine.matcher.coupang_link_builder import generate_affiliate_cta_button

def run_phase1_test():
    print("=" * 60)
    print("🧪 [Phase 1 통합 테스트] 실시간 트렌드 수집 & 광고주 일감 매칭 검증")
    print("=" * 60)
    
    # 1. 트렌드 스카우트 실행
    print("\n[Step 1] 구글 트렌드 KR RSS 실시간 수집 중...")
    trends = fetch_google_trends_kr()
    assert len(trends) > 0, "트렌드 수집 결과가 0건입니다."
    print(f"✅ 수집 성공! 총 {len(trends)}개 트렌드 확보.")
    for i, t in enumerate(trends[:3], 1):
        print(f"   {i}. {t['keyword']} (트래픽: {t['traffic_volume']:,})")
        
    # 2. 광고주 일감 & PVS v2.0 매칭
    print("\n[Step 2] 5대 황금 니치 및 광고주 일감(CPA/CPS) 매칭 중...")
    winner = match_trends_with_demand(trends)
    assert winner and "title" in winner, "매칭 결과가 올바르지 않습니다."
    print("✅ 매칭 성공!")
    print(f"   • 최종 선정 제목: {winner['title']}")
    print(f"   • 황금 니치: {winner['niche_name']} ({winner['category_code']})")
    print(f"   • 검색량: {winner['traffic_volume']:,}")
    print(f"   • 예상 제휴 수수료: {winner['avg_payout']:,}원 ({winner['cpa_type']})")
    print(f"   • 예상 애드센스 기본 CPC: {winner['base_cpc']:,}원")
    print(f"   • PVS v2.0 종합 수익성 점수: {winner['PVS_score']:,.2f}점")
    
    # 3. 네이티브 제휴 CTA 버튼 생성 검증
    print("\n[Step 3] 네이티브 제휴 CTA 박스 생성 검증...")
    cta_html = generate_affiliate_cta_button(winner["keyword"], winner["cpa_type"])
    assert "btn-affiliate-action" in cta_html, "CTA 버튼 HTML이 생성되지 않았습니다."
    print(f"✅ CTA 박스 HTML 생성 완료 (길이: {len(cta_html)}자)")
    
    print("\n" + "=" * 60)
    print("🎉 [Phase 1 테스트 100% 통과 완료] 트렌드 레이더와 광고주 일감 매칭이 완벽하게 가동됩니다!")
    print("=" * 60)

if __name__ == "__main__":
    run_phase1_test()
