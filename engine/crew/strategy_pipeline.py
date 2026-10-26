# -*- coding: utf-8 -*-
"""
engine/crew/strategy_pipeline.py
---------------------------------
Autonomous Strategy Lab Pipeline Orchestrator (v9.0 Apex)

Automates the end-to-end production of interactive FinTech Strategy Lab posts:
1. Picks the next pending strategy from data/strategy_topics_queue.json
2. Generates the TradingView Lightweight Charts (v4.1) backtester widget
3. Synthesizes an institutional-grade Apolia 8-Block editorial article
4. Validates visual rendering & WCAG 2.1 AAA contrast via EditorialInspector
5. Deploys live to Google Blogger via BloggerGateway (API v3)
6. Updates queue database and company logs
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

from engine.visuals.strategy_lab_renderer import StrategyLabRenderer
from engine.publisher.blogger_gateway import BloggerGateway
from engine.crew.editorial_inspector import EditorialInspector


class StrategyLabPipeline:
    """
    Orchestrates daily autonomous strategy lab article publishing.
    """

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.queue_file = os.path.join(self.base_dir, "data", "strategy_topics_queue.json")
        self.gateway = BloggerGateway(base_dir=self.base_dir)
        self.inspector = EditorialInspector()

    def load_queue(self) -> list:
        if not os.path.exists(self.queue_file):
            return []
        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[StrategyLabPipeline] Error loading queue: {e}")
            return []

    def save_queue(self, queue: list) -> None:
        try:
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(queue, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[StrategyLabPipeline] Error saving queue: {e}")

    EVERGREEN_STRATEGIES = [
        {
            "strategy_id": "macd_divergence_scalping",
            "title": "2026 해외 100만 트레이더들의 MACD 다이버전스 반전 매매법: 실시간 바이낸스 캔들 백테스팅 팩트체크",
            "subtitle": "가격과 보조지표의 괴리를 이용한 추세 반전 매매법의 실제 승률과 손익비를 바이낸스 캔들 위에서 0.01초 만에 검증합니다.",
            "target_keyword": "MACD 다이버전스 매매법 백테스팅",
            "symbol": "BTCUSDT",
            "interval": "15m",
            "category": "FINTECH_QUANT",
            "labels": ["FINTECH", "QUANT", "MACD", "DIVERGENCE", "TRADINGVIEW", "VIBE_TRADING"],
            "trader_name": "전설의 월가 차티스트",
            "default_params": {
                "bb_period": 20,
                "bb_std": 2.0,
                "vol_mult": 1.4,
                "rsi_threshold": 38,
                "tp_percent": 2.2,
                "sl_percent": 1.1,
                "leverage": 3
            },
            "strategy_description": "주가는 신저점을 경신하나 MACD 히스토그램은 저점을 높이는 상승 다이버전스 출현 시, 거래량이 실린 반등 캔들에서 롱 진입. 2.2% 익절 및 1.1% 칼손절.",
            "callout_text": "다이버전스 매매의 가장 큰 함정은 '과매도 국면에서의 섣부른 조기 진입'입니다. 반드시 거래량이 동반되며 직전 캔들의 저가를 방어하는 양봉 확인 캔들이 종가 마감된 이후에만 진입해야 휩소(Whipsaw)를 피할 수 있습니다.",
            "status": "PENDING",
            "published_url": None,
            "published_at": None
        },
        {
            "strategy_id": "ema_golden_cross_trend",
            "title": "2026 지수이동평균(EMA) 20/50/200 정배열 골든크로스 추세추종: 실시간 비트코인 캔들 백테스팅",
            "subtitle": "추세추종의 정석 EMA 정배열과 눌림목 지지선 반등 타점의 실시간 승률 및 최대 손실폭(MDD)을 투명하게 팩트체크합니다.",
            "target_keyword": "EMA 골든크로스 추세추종 매매법 백테스팅",
            "symbol": "BTCUSDT",
            "interval": "1h",
            "category": "FINTECH_QUANT",
            "labels": ["FINTECH", "QUANT", "EMA", "TREND_FOLLOWING", "TRADINGVIEW", "VIBE_TRADING"],
            "trader_name": "정통 테크니컬 애널리스트",
            "default_params": {
                "bb_period": 20,
                "bb_std": 2.0,
                "vol_mult": 1.5,
                "rsi_threshold": 45,
                "tp_percent": 3.5,
                "sl_percent": 1.8,
                "leverage": 2
            },
            "strategy_description": "20 EMA가 50 EMA를 상향 돌파하고 200 EMA 위에서 대세 상승 추세가 확정될 때, 20 EMA 지지 테스트에서 매수 진입. 3.5% 목표가 분할 익절, 1.8% 이탈 시 칼손절.",
            "callout_text": "대세 상승장에서는 잦은 손절보다 '추세를 길게 발라먹는 손익비(Risk-Reward)'가 전체 수익률을 좌우합니다. 200 EMA 지지선이 깨지지 않는 한 흔들기에 털리지 않고 버티는 것이 퀀트 추세추종의 핵심입니다.",
            "status": "PENDING",
            "published_url": None,
            "published_at": None
        },
        {
            "strategy_id": "keltner_ttm_squeeze",
            "title": "2026 존 카터의 TTM 스퀴즈(Squeeze) & 켈트너 채널 폭발 매매법: 실시간 바이낸스 백테스팅",
            "subtitle": "에너지를 응축한 볼린저 밴드가 켈트너 채널을 뚫고 폭발하는 모멘텀 타점을 실시간 차트 위에서 시뮬레이션합니다.",
            "target_keyword": "TTM 스퀴즈 켈트너 채널 매매법 백테스팅",
            "symbol": "BTCUSDT",
            "interval": "15m",
            "category": "FINTECH_QUANT",
            "labels": ["FINTECH", "QUANT", "TTM_SQUEEZE", "KELTNER", "TRADINGVIEW", "VIBE_TRADING"],
            "trader_name": "존 카터 (John Carter)",
            "default_params": {
                "bb_period": 20,
                "bb_std": 2.0,
                "vol_mult": 1.6,
                "rsi_threshold": 42,
                "tp_percent": 2.5,
                "sl_percent": 1.2,
                "leverage": 3
            },
            "strategy_description": "볼린저 밴드가 켈트너 채널 내부로 수축(Squeeze)된 후 밴드 밖으로 벗어나며 거래량이 폭증할 때 첫 번째 돌파 캔들에서 모멘텀 롱 진입.",
            "callout_text": "변동성이 극도로 축소되는 스퀴즈 구간은 마치 용수철을 꽉 누른 상태와 같습니다. 방향성이 터지기 직전 미리 예측하기보다, 밴드 밖으로 거래량이 실리는 첫 번째 캔들에 즉각 탑승하는 것이 정석입니다.",
            "status": "PENDING",
            "published_url": None,
            "published_at": None
        },
        {
            "strategy_id": "rsi_connors_mean_reversion",
            "title": "2026 전설의 래리 코너스(Larry Connors) RSI 극단 과매도 V자 반등 전략: 실시간 바이낸스 백테스팅",
            "subtitle": "200일선 위 대세 상승장에서 일시적 패닉셀로 폭락한 과매도 공포 구간을 수학적으로 공략하는 고승률 평균회귀 기법.",
            "target_keyword": "코너스 RSI 과매도 반등 매매법 백테스팅",
            "symbol": "BTCUSDT",
            "interval": "5m",
            "category": "FINTECH_QUANT",
            "labels": ["FINTECH", "QUANT", "CONNORS_RSI", "MEAN_REVERSION", "TRADINGVIEW", "VIBE_TRADING"],
            "trader_name": "래리 코너스 (Larry Connors)",
            "default_params": {
                "bb_period": 20,
                "bb_std": 2.0,
                "vol_mult": 1.3,
                "rsi_threshold": 25,
                "tp_percent": 1.5,
                "sl_percent": 0.9,
                "leverage": 4
            },
            "strategy_description": "200 이평선 위의 대세 상승 기조 속에서, 일시적인 패닉셀로 인해 RSI가 25 이하로 극단적으로 폭락했을 때 공포를 역이용하여 단기 V자 반등을 취하는 평균회귀 전략.",
            "callout_text": "모두가 공포에 질려 던질 때 수학적 기대값은 극대화됩니다. 단, 200 이평선 아래의 역배열 하락장에서는 바닥 밑에 지하실이 있으므로 철저하게 상위 이평선 지지 조건이 충족될 때만 가동해야 합니다.",
            "status": "PENDING",
            "published_url": None,
            "published_at": None
        }
    ]

    def auto_replenish_queue(self) -> None:
        queue = self.load_queue()
        existing_ids = {item.get("strategy_id") for item in queue}
        pending_count = sum(1 for item in queue if item.get("status") == "PENDING")
        if pending_count < 2:
            added = False
            for cand in self.EVERGREEN_STRATEGIES:
                if cand["strategy_id"] not in existing_ids:
                    queue.append(cand)
                    existing_ids.add(cand["strategy_id"])
                    added = True
            if added:
                self.save_queue(queue)
                print(f"[StrategyLabPipeline] 큐 자동 보충 완료: 신규 전략 충전됨 (총 {len(queue)}개 전략 보유)")

    def get_next_topic(self, topic_id_override: str = None) -> Optional[Dict[str, Any]]:
        self.auto_replenish_queue()
        queue = self.load_queue()
        if not queue:
            return None

        if topic_id_override:
            for item in queue:
                if item.get("strategy_id") == topic_id_override:
                    return item

        # First find PENDING
        for item in queue:
            if item.get("status") == "PENDING":
                return item

        # If all published, sort by published_at and pick the oldest to refresh
        queue_sorted = sorted(queue, key=lambda x: x.get("published_at") or "")
        return queue_sorted[0] if queue_sorted else None

    def build_article_html(self, item: Dict[str, Any]) -> str:
        """
        Assembles full Apolia 8-Block article for the specific strategy topic.
        """
        widget_html = StrategyLabRenderer.render(item)

        title = item.get("title", "")
        symbol = item.get("symbol", "BTCUSDT")
        interval = item.get("interval", "15m")
        trader_name = item.get("trader_name", "퀀트 트레이더")
        description = item.get("strategy_description", "")
        callout_text = item.get("callout_text", "")
        params = item.get("default_params", {})

        content = f"""<style>
/* Master Toss Dark Theme Scoping */
.strategy-post-container {{
    max-width: 880px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #f8fafc;
    background: #0a0e17;
    line-height: 1.8;
    box-sizing: border-box;
}}

.strategy-post-container h1, .strategy-post-container h2, .strategy-post-container h3 {{
    color: #f8fafc !important;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

.strategy-post-container h2 {{
    font-size: 22px;
    margin-top: 40px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid #1f2d47;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.strategy-post-container p {{
    color: #cbd5e1;
    font-size: 15px;
    margin-bottom: 18px;
}}

.strategy-post-container strong {{
    color: #f8fafc;
}}

/* Bento Grid */
.strategy-bento-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin: 24px 0 28px 0;
}}

.strategy-bento-item {{
    background: #111827;
    border: 1px solid #1f2d47;
    border-radius: 14px;
    padding: 18px;
    text-align: left;
}}

.strategy-bento-item strong {{
    display: block;
    font-size: 12px;
    color: #38bdf8;
    text-transform: uppercase;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}}

.strategy-bento-item span {{
    font-size: 14px;
    color: #f8fafc;
    font-weight: 600;
    line-height: 1.5;
}}

/* Callout Box */
.strategy-callout {{
    background: #111827;
    border-left: 4px solid #10b981;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 20px 0 28px 0;
    font-size: 14px;
    color: #e2e8f0;
    line-height: 1.6;
}}

/* Comparison Table */
.strategy-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    background: #111827;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1f2d47;
    font-size: 13px;
}}

.strategy-table th {{
    background: #172236;
    color: #94a3b8;
    font-weight: 700;
    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid #1f2d47;
}}

.strategy-table td {{
    padding: 14px 16px;
    border-bottom: 1px solid #1f2d47;
    color: #cbd5e1;
}}

.strategy-table tr:last-child td {{
    border-bottom: none;
}}

/* FAQ Details */
.strategy-faq {{
    background: #111827;
    border: 1px solid #1f2d47;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    cursor: pointer;
}}

.strategy-faq summary {{
    font-weight: 700;
    color: #f8fafc;
    font-size: 15px;
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.strategy-faq summary::-webkit-details-marker {{
    display: none;
}}

.strategy-faq p {{
    margin-top: 12px;
    margin-bottom: 0;
    color: #94a3b8;
    font-size: 14px;
}}

/* Global Portal Link Header */
.strategy-portal-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid #1f2d47;
    border-radius: 12px;
    padding: 10px 16px;
    margin-bottom: 24px;
    backdrop-filter: blur(8px);
}}

.strategy-portal-bar a {{
    color: #38bdf8 !important;
    text-decoration: none;
    font-size: 12px;
    font-weight: 700;
}}

.strategy-portal-bar a:hover {{
    text-decoration: underline;
}}
</style>

<div class="strategy-post-container">

  <!-- Global Portal Navigation Bar -->
  <div class="strategy-portal-bar">
    <a href="https://blogin365ai.blogspot.com/">🏠 Blogin 365 AI 홈 포털</a>
    <div style="display: flex; gap: 14px; align-items: center;">
      <span style="font-size: 11px; color: #10b981; font-weight: 700;">● {symbol} 실시간 퀀트 피드</span>
      <a href="https://blogin365ai.blogspot.com/p/vibe-trading.html" style="background: rgba(37,99,235,0.2); border: 1px solid #3b82f6; padding: 4px 10px; border-radius: 6px; color: #93c5fd !important;">🔥 VIBE TRADING 프로</a>
    </div>
  </div>

  <!-- Hero Header & Meta Badges -->
  <div style="margin-bottom: 24px;">
    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
      <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #10b981; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 6px;">
        ✓ Blogin 365 AI Quantitative Lab 검증
      </span>
      <span style="background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
        바이낸스 {symbol} {interval}봉 500개 전수 백테스팅
      </span>
      <span style="background: rgba(192, 132, 252, 0.12); border: 1px solid rgba(192, 132, 252, 0.3); color: #c084fc; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
        Vibe Trading 모의투자 봇 실시간 연동
      </span>
    </div>
    <h1 style="font-size: 26px; font-weight: 900; line-height: 1.35; margin: 0 0 10px 0; color: #f8fafc;">
      {title}
    </h1>
    <div style="font-size: 12px; color: #94a3b8; display: flex; gap: 14px;">
      <span>집필: Blogin 365 AI 퀀트 리서치팀</span>
      <span>대상: {trader_name} 대표 기법</span>
      <span>업데이트: {datetime.now().strftime('%Y년 %m월')} 최신판</span>
    </div>
  </div>

  <!-- 이 글 핵심 3줄 Bento Box -->
  <div class="strategy-bento-grid">
    <div class="strategy-bento-item">
      <strong>01. 진입 알고리즘</strong>
      <span>{description[:80]}...</span>
    </div>
    <div class="strategy-bento-item">
      <strong>02. 리스크 관리</strong>
      <span>익절: +{params.get('tp_percent', 2.0)}% | 손절: -{params.get('sl_percent', 1.0)}% | 레버리지: {params.get('leverage', 3)}x</span>
    </div>
    <div class="strategy-bento-item">
      <strong>03. 실시간 팩트체크</strong>
      <span>바이낸스 과거 500개 실시간 캔들 위에서 승률과 손익비를 0.01초 만에 기계적으로 산출</span>
    </div>
  </div>

  <!-- Blogger Index Pagination Jump Break (홈 화면 피드 경량화 필수 태그) -->
  <!--more-->

  <!-- Psychological Hook Paragraph -->
  <p>
    인터넷과 유튜브에는 하루에도 수백 편의 <strong>"승률 95% 단타 비법"</strong> 영상이 쏟아집니다.
    하지만 화려하게 편집된 수익 인증 스크린샷 뒤에 숨겨진 <strong>진짜 승률과 청산 리스크</strong>를 객관적으로 검증해 본 투자자는 얼마나 될까요?
    감정에 휘둘리는 주관적 매매는 결국 수수료와 슬리피지로 인해 시드를 갉아먹을 뿐입니다.
  </p>

  <p>
    Blogin 365 AI 퀀트 연구팀은 <strong>{trader_name}</strong>의 핵심 트레이딩 룰을 순수 수학적 알고리즘으로 분해하여,
    바이낸스(Binance)의 실제 500개 캔들 위에서 <strong>실시간 시그널 화살표(▲ BUY / ▼ SELL)와 성적표를 차트 위에 직접 렌더링</strong>했습니다.
    유튜버들의 말을 무비판적으로 믿지 마시고, 아래 인터랙티브 전략 랩에서 직접 수치를 튜닝하며 검증해 보십시오.
  </p>

  <!-- Section 1: Interactive Strategy Lab Widget -->
  <h2><span>📈</span> 실시간 전략 랩 & 인-브라우저 캔들 백테스터</h2>
  <p>
    아래 차트는 바이낸스 {symbol}의 실제 시세 데이터입니다.
    조건이 충족된 모든 지점에 <strong>초록색(▲ BUY)</strong>과 <strong>빨간색(▼ SELL)</strong> 화살표가 자동으로 표시됩니다.
    슬라이더를 움직여 최적의 파라미터를 찾아보십시오.
  </p>

  <!-- INLINE WIDGET INJECTION -->
  {widget_html}

  <!-- Section 2: Core Principle Callout & Logic Analysis -->
  <h2><span>🔍</span> {trader_name} 전략의 핵심 승패 법칙</h2>
  
  <div class="strategy-callout">
    <strong>💡 팩트체크 결론 (핵심 1문장):</strong><br>
    {callout_text}
  </div>

  <p>
    수학적 백테스팅 결과, 이 기법이 장기적으로 우상향하기 위한 가장 중요한 요소는 <strong>'손익비(Profit Factor)의 철저한 준수'</strong>였습니다.
    승률이 아무리 70%에 달해도 손절을 미루고 물타기를 한 번 하는 순간 그동안 벌어들인 수익이 단번에 날아가며,
    반대로 손익비를 1.5 이상으로 세팅하고 기계적 칼손절을 지켰을 때만 복리 우상향이 완성되었습니다.
  </p>

  <!-- Section 3: Comparison Table -->
  <h2><span>⚖️</span> 초보 개미의 뇌동매매 vs {trader_name} 퀀트 전략 비교</h2>
  
  <table class="strategy-table">
    <thead>
      <tr>
        <th>비교 항목</th>
        <th>감정에 휘둘리는 뇌동매매</th>
        <th>기계적 퀀트 전략 룰</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>진입 기준</strong></td>
        <td>급등하는 장대양봉을 보고 추격 매수</td>
        <td>사전에 정의된 <strong>수학적 지표 및 거래량 조건 마감</strong> 확인</td>
      </tr>
      <tr>
        <td><strong>손절 실행</strong></td>
        <td>반등을 기도하며 존버 (청산 엔딩)</td>
        <td><strong>설정 손절선(-{params.get('sl_percent', 1.0)}%) 도달 시 0.01초 칼손절</strong></td>
      </tr>
      <tr>
        <td><strong>익절 원칙</strong></td>
        <td>조금 오르면 조급하게 전량 청산</td>
        <td><strong>목표가(+{params.get('tp_percent', 2.0)}%) 도달 시 분할 익절</strong>로 추세 극대화</td>
      </tr>
      <tr>
        <td><strong>레버리지</strong></td>
        <td>한 방을 노린 20x~50x 고배율 몰빵</td>
        <td><strong>{params.get('leverage', 3)}x 적정 배율 분할 진입</strong>으로 생존율 확보</td>
      </tr>
    </tbody>
  </table>

  <!-- Section 4: Real-time Paper Trading Link -->
  <h2><span>🚀</span> 내 모의투자 계좌에 이 봇을 장착하고 랭킹전 참여하는 법</h2>
  <p>
    이 전략이 마음에 드신다면 위 위젯의 <strong>`이 전략으로 실시간 모의투자 추종`</strong> 스위치를 켜보십시오.
    대표님의 브라우저가 열려 있는 동안 바이낸스 실시간 시세를 감시하며, 진입 조건이 맞을 때마다 가상 $10,000 계좌로 자동 매매를 시뮬레이션합니다.
    이 기록은 상설 플래그십 웹앱인 
    <a href="https://blogin365ai.blogspot.com/p/vibe-trading.html" style="color: #38bdf8; font-weight: 800;">🔥 VIBE TRADING 프로 스테이션</a>의 
    내 가상 계좌 및 Top 10 명예의 전당 랭킹전에 실시간으로 합산됩니다.
  </p>

  <!-- Section 5: Accordion FAQ -->
  <h2><span>❓</span> 자주 묻는 질문 (FAQ)</h2>

  <details class="strategy-faq">
    <summary>
      <span>Q1. 이 전략은 하락장(Bear Market)에서도 통하나요?</span>
      <span style="color: #38bdf8;">▼</span>
    </summary>
    <p>
      단기 반등 스캘핑과 변동성 돌파 전략은 시장의 장기 추세와 무관하게 15분~1시간 단위의 급격한 변동성을 취하므로 하락장에서도 유효합니다.
      단, 대세 하락장에서는 롱 포지션의 익절 목표가를 짧게 잡고 손절선을 타이트하게 운영하는 것이 유리합니다.
    </p>
  </details>

  <details class="strategy-faq">
    <summary>
      <span>Q2. 차트에서 분봉을 바꿀 수 있나요?</span>
      <span style="color: #38bdf8;">▼</span>
    </summary>
    <p>
      네, 위 차트 상단의 [1분봉 | 5분봉 | 15분봉 | 1시간봉] 버튼을 누르시면 즉시 바이낸스의 해당 주기 캔들 500개를 실시간으로 불러와 백테스팅을 다시 계산합니다.
    </p>
  </details>

  <details class="strategy-faq">
    <summary>
      <span>Q3. 모의투자 가상 잔고는 저장되나요?</span>
      <span style="color: #38bdf8;">▼</span>
    </summary>
    <p>
      네, 본 Strategy Lab 및 VIBE TRADING의 모든 모의투자 기록과 잔고는 브라우저 로컬스토리지(localStorage)에 안전하게 영구 저장됩니다. 
      새로고침을 하거나 재방문하셔도 본인의 가상 누적 수익률이 그대로 유지됩니다.
    </p>
  </details>

  <!-- Section 6: Legal Disclaimer -->
  <div style="background: #0f172a; border-left: 4px solid #ef4444; border-radius: 8px; padding: 14px 18px; margin: 36px 0 20px 0; font-size: 12px; color: #94a3b8; line-height: 1.6;">
    <strong style="color: #f8fafc;">⚠️ [법적 면책 조항 및 리스크 고지]</strong><br>
    본 시뮬레이터와 분석 리포트는 기술적 분석 학습 및 알고리즘 모의투자를 위해 제공되는 교육용 도구입니다. 
    과거의 백테스트 수익률이 미래의 실제 수익을 보장하지 않으며, 가상자산 및 레버리지 파생상품 거래는 원금 초과 손실 위험이 따릅니다. 
    모든 실전 투자의 최종 결정과 손익의 책임은 투자자 본인에게 있습니다.
  </div>

</div>
"""
        return content

    def run_autonomous_cycle(self, dry_run: bool = False, topic_id_override: str = None) -> Dict[str, Any]:
        """
        Executes one full autonomous cycle:
        Pick topic -> Render widget -> Build article -> QA contrast audit -> Publish live -> Update queue.
        """
        start_time = time.time()
        print("=" * 70)
        print("🏢 [Blogin 365 AI Holdings] Vibe Strategy Lab 전자동 무인 발행 파이프라인 가동")
        print("=" * 70)

        # 1. Pick Next Topic
        topic = self.get_next_topic(topic_id_override)
        if not topic:
            raise RuntimeError("전략 발행 큐(data/strategy_topics_queue.json)에 처리할 주제가 없습니다.")

        print(f"🎯 [Step 1/4] 선택된 전략 주제: '{topic.get('title')}'")
        print(f"   • 전략 ID: {topic.get('strategy_id')}")
        print(f"   • 대상 심볼: {topic.get('symbol')} ({topic.get('interval')})")
        print(f"   • 트레이더: {topic.get('trader_name')}")

        # 2. Build Article HTML with Integrated Lightweight Charts & Backtester
        print("⚙️ [Step 2/4] TradingView 캔들 차트 + 실시간 백테스터 + 에디토리얼 아티클 조립 중...")
        full_html = self.build_article_html(topic)
        print(f"   ✓ 아티클 조립 완료 (총 용량: {len(full_html)} bytes)")

        # 3. QA Contrast & Layout Audit
        print("🔍 [Step 3/4] Editorial Inspector 실물 비주얼 및 WCAG AAA 명도비 감사 실행...")
        qa_res = self.inspector.inspect(full_html, is_url=False)
        print(f"   • QA 통과 여부: {qa_res['passed']}")
        print(f"   • 결함 개수: {len(qa_res['defects'])}건")
        if not qa_res["passed"]:
            raise RuntimeError(f"QA 명도비 감사 실패: {qa_res['defects']}")

        # 4. Publish to Google Blogger
        print(f"🚀 [Step 4/4] Google Blogger 배포 진행 (Mode: {'DRY-RUN' if dry_run else 'LIVE'})...")
        if dry_run:
            pub_res = {
                "success": True,
                "url": f"https://blogin365ai.blogspot.com/dry-run-{topic.get('strategy_id')}.html",
                "id": f"dry-{int(time.time())}",
                "title": topic.get("title")
            }
        else:
            pub_res = self.gateway.publish(
                title=topic.get("title"),
                html_content=full_html,
                labels=["경제·금융"] + [l for l in topic.get("labels", ["FINTECH", "QUANT"]) if l != "경제·금융"],
                is_draft=False,
                category=topic.get("category", "FINTECH_QUANT")
            )

        if not pub_res.get("success"):
            raise RuntimeError(f"Blogger 배포 실패: {pub_res.get('error')}")

        live_url = pub_res.get("url")
        post_id = pub_res.get("id")
        print(f"✅ [배포 완료] LIVE URL: {live_url} (Post ID: {post_id})")

        # 5. Update Queue Status (only on real live publish)
        if not dry_run:
            queue = self.load_queue()
            for q_item in queue:
                if q_item.get("strategy_id") == topic.get("strategy_id"):
                    q_item["status"] = "PUBLISHED"
                    q_item["published_url"] = live_url
                    q_item["published_at"] = datetime.now().isoformat()
            self.save_queue(queue)

        elapsed = round(time.time() - start_time, 2)
        print(f"🎉 [성공] 전자동 사이클 완주 소요시간: {elapsed}초\n")

        return {
            "status": "COMPLETED",
            "strategy_id": topic.get("strategy_id"),
            "title": topic.get("title"),
            "url": live_url,
            "post_id": post_id,
            "execution_time_sec": elapsed,
            "dry_run": dry_run
        }


if __name__ == "__main__":
    pipeline = StrategyLabPipeline()
    res = pipeline.run_autonomous_cycle(dry_run=True)
    print("Test run result:", res)
