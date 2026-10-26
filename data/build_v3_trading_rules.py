# -*- coding: utf-8 -*-
"""
data/build_v3_trading_rules.py
-------------------------------
20대 핵심 자산 프로그래매틱 Micro-SaaS 정형 DB (v3.0) 빌더
"""

import os
import sys
import json

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "trading_rules_db.json")

# 기존 8개 룰 로드
with open(DB_PATH, "r", encoding="utf-8") as f:
    existing_db = json.load(f)

rules = existing_db.get("rules", {})

# 20대 자산 특화 룰셋 추가
asset_rules = {
    # [미국 주식 10종]
    "nvda_stock_tax": {
        "id": "nvda_stock_tax",
        "ticker": "NVDA",
        "name": "엔비디아(NVDA) 2026 해외주식 양도소득세 및 분할매도 시뮬레이터",
        "category": "US Tech Stock Tax",
        "english_slug": "nvda-overseas-stock-tax-calculator",
        "law_reference": "소득세법 제94조, 제104조 (국외주식 양도)",
        "formula_badge": "양도세 = Max(0, NVDA 실현수익 - 250만) × 22%",
        "key_stat": "NVDA 250만 비과세 한도 | 실효세율 0~21.45%",
        "sub_label": "엔비디아 실현손익 및 절세 시뮬레이션",
        "benchmark_price_usd": 140.0,
        "constants": {"basic_deduction_krw": 2500000, "total_tax_rate": 0.22},
        "tax_matrix_brackets": [
            {"gain_krw": 2500000, "tax_base_krw": 0, "total_tax_krw": 0, "effective_rate": "0.00%"},
            {"gain_krw": 10000000, "tax_base_krw": 7500000, "total_tax_krw": 1650000, "effective_rate": "16.50%"},
            {"gain_krw": 50000000, "tax_base_krw": 47500000, "total_tax_krw": 10450000, "effective_rate": "20.90%"},
            {"gain_krw": 100000000, "tax_base_krw": 97500000, "total_tax_krw": 21450000, "effective_rate": "21.45%"}
        ]
    },
    "tsla_water_averaging": {
        "id": "tsla_water_averaging",
        "ticker": "TSLA",
        "name": "테슬라(TSLA) 물타기 평단가 및 본전 탈출 역산 시뮬레이터",
        "category": "US Stock DCA",
        "english_slug": "tsla-water-averaging-dca-calculator",
        "formula_badge": "신규평단 = (기존금액 + 추가매수금액) / 총수량",
        "key_stat": "테슬라 손익분기점(BEP) 및 목표 평단 역산",
        "sub_label": "TSLA 변동성 대응 DCA 모델",
        "benchmark_price_usd": 220.0,
        "averaging_matrix_samples": [
            {"drop_rate": "-20%", "extra_ratio": "1:1", "new_drop_rate": "-10.00%", "required_rebound": "+11.11%"},
            {"drop_rate": "-40%", "extra_ratio": "1:1", "new_drop_rate": "-20.00%", "required_rebound": "+25.00%"},
            {"drop_rate": "-50%", "extra_ratio": "1:2", "new_drop_rate": "-16.67%", "required_rebound": "+20.00%"}
        ]
    },
    "aapl_stock_tax": {
        "id": "aapl_stock_tax",
        "ticker": "AAPL",
        "name": "애플(AAPL) 해외주식 양도소득세 및 기본공제 250만원 절세 계산기",
        "category": "US Bluechip Tax",
        "english_slug": "aapl-overseas-stock-tax-calculator",
        "formula_badge": "양도세 = Max(0, AAPL 순익 - 250만) × 22%",
        "key_stat": "애플 장기보유 양도세 손익통산 계산",
        "sub_label": "소득세법 제94조 기준",
        "benchmark_price_usd": 230.0
    },
    "msft_stock_tax": {
        "id": "msft_stock_tax",
        "ticker": "MSFT",
        "name": "마이크로소프트(MSFT) 해외주식 양도소득세 및 분할실현 시뮬레이터",
        "category": "US Tech Stock Tax",
        "english_slug": "msft-overseas-stock-tax-calculator",
        "formula_badge": "양도세 = Max(0, MSFT 순익 - 250만) × 22%",
        "key_stat": "MSFT 250만 한도 분할실현 절세",
        "sub_label": "2026 해외주식 손익통산",
        "benchmark_price_usd": 430.0
    },
    "pltr_water_averaging": {
        "id": "pltr_water_averaging",
        "ticker": "PLTR",
        "name": "팔란티어(PLTR) 물타기 평단가 및 본전 탈출 손익분기점 계산기",
        "category": "US Stock DCA",
        "english_slug": "pltr-dca-break-even-calculator",
        "formula_badge": "목표수량 = 기존수량 × (기존가 - 목표가) / (목표가 - 추가매수가)",
        "key_stat": "팔란티어 고변동성 본전 탈출 반등률 도출",
        "sub_label": "DCA 포지션 회복 시뮬레이션",
        "benchmark_price_usd": 44.0
    },
    "soxl_leverage_decay": {
        "id": "soxl_leverage_decay",
        "ticker": "SOXL",
        "name": "SOXL 반도체 3배 레버리지 음의 복리 및 청산 위험 시뮬레이터",
        "category": "Leveraged ETF",
        "english_slug": "soxl-3x-leverage-decay-calculator",
        "formula_badge": "복리손실 = (1 + 3×일일수익률)^n - 1",
        "key_stat": "3배 레버리지 횡보장 롤오버 음의 복리 감별",
        "sub_label": "레버리지 ETF 위험관리 수학 모델",
        "benchmark_price_usd": 35.0
    },
    "tqqq_water_averaging": {
        "id": "tqqq_water_averaging",
        "ticker": "TQQQ",
        "name": "TQQQ 나스닥 3배 레버리지 분할매수(DCA) 및 본전 회복 계산기",
        "category": "Leveraged ETF DCA",
        "english_slug": "tqqq-3x-dca-recovery-calculator",
        "formula_badge": "신규평단 = (기존총액 + 신규총액) / 총수량",
        "key_stat": "TQQQ MDD 낙폭별 필요 반등률 도출",
        "sub_label": "3배수 레버리지 적립식 DCA 모델",
        "benchmark_price_usd": 75.0
    },
    "ionq_water_averaging": {
        "id": "ionq_water_averaging",
        "ticker": "IONQ",
        "name": "아이온큐(IONQ) 양자컴퓨터 물타기 평단가 및 본전 회복 계산기",
        "category": "US Growth Stock DCA",
        "english_slug": "ionq-stock-dca-bep-calculator",
        "formula_badge": "BEP회복률 = (신규평단 × 1.002) / 현재가 - 1",
        "key_stat": "아이온큐 추가매수 수수료 포함 실제 BEP",
        "sub_label": "성장주 리스크 관리 모델",
        "benchmark_price_usd": 18.0
    },
    "coin_stock_tax": {
        "id": "coin_stock_tax",
        "ticker": "COIN",
        "name": "코인베이스(COIN) 해외주식 양도소득세 및 가상자산 관련주 절세 계산기",
        "category": "Crypto Proxy Stock Tax",
        "english_slug": "coinbase-overseas-stock-tax-calculator",
        "formula_badge": "양도세 = Max(0, COIN 순수익 - 250만) × 22%",
        "key_stat": "비트코인 연동주 양도세 22% 시뮬레이션",
        "sub_label": "미국 가상자산 관련주 세무 기준",
        "benchmark_price_usd": 210.0
    },
    "o_dividend_compound": {
        "id": "o_dividend_compound",
        "ticker": "O",
        "name": "리얼티인컴(O) 월배당 복리 재투자 및 금융소득종합과세 시뮬레이터",
        "category": "Monthly Dividend Stock",
        "english_slug": "realty-income-monthly-dividend-calculator",
        "formula_badge": "월배당 = 원금 × (연배당률 5.5% / 12) × (1 - 15.4%)",
        "key_stat": "월 100만 배당 필요 주수 & 종합과세 분기점",
        "sub_label": "리얼티인컴 배당 복리 성장 모델",
        "benchmark_price_usd": 54.0,
        "default_dividend_yield": 5.5
    },

    # [크립토 6종]
    "btc_futures_liquidation": {
        "id": "btc_futures_liquidation",
        "ticker": "BTC",
        "name": "비트코인(BTC) 바이낸스 선물 레버리지 청산가 및 켈리 공식 계산기",
        "category": "Crypto Futures & Quant",
        "english_slug": "btc-futures-leverage-liquidation-calculator",
        "formula_badge": "Liq = Entry × (1 - 1/Lev + MMR 0.4%)",
        "key_stat": "BTC 격리/교차 강제청산가 및 Half-Kelly 비중",
        "sub_label": "바이낸스 Tier-1 마진 공식 기준",
        "benchmark_price_usd": 68000.0,
        "mmr_rate": 0.004
    },
    "eth_futures_liquidation": {
        "id": "eth_futures_liquidation",
        "ticker": "ETH",
        "name": "이더리움(ETH) 선물 레버리지 강제청산가 및 포지션 사이징 계산기",
        "category": "Crypto Futures & Quant",
        "english_slug": "eth-futures-liquidation-position-calculator",
        "formula_badge": "Liq = Entry × (1 - 1/Lev + MMR 0.5%)",
        "key_stat": "ETH 롱/숏 격리 청산가 및 파산확률 0% 포지션",
        "sub_label": "이더리움 선물 리스크 관리 모델",
        "benchmark_price_usd": 2600.0,
        "mmr_rate": 0.005
    },
    "xrp_water_averaging": {
        "id": "xrp_water_averaging",
        "ticker": "XRP",
        "name": "리플(XRP) 코인 물타기 평단가 및 본전 탈출 반등률 계산기",
        "category": "Crypto DCA",
        "english_slug": "xrp-coin-dca-break-even-calculator",
        "formula_badge": "신규평단 = (기존총액 + 신규매수액) / 총수량",
        "key_stat": "리플 낙폭별 본전 탈출 필요 반등률 도출",
        "sub_label": "업비트 0.05% 수수료 반영 DCA 모델",
        "benchmark_price_krw": 750.0
    },
    "sol_futures_liquidation": {
        "id": "sol_futures_liquidation",
        "ticker": "SOL",
        "name": "솔라나(SOL) 선물 레버리지 청산가 및 리스크 관리 시뮬레이터",
        "category": "Crypto Futures",
        "english_slug": "solana-futures-liquidation-calculator",
        "formula_badge": "Liq = Entry × (1 - 1/Lev + MMR 1.0%)",
        "key_stat": "SOL 고변동성 청산가 안전마진 도출",
        "sub_label": "솔라나 선물 마진 엔진 기준",
        "benchmark_price_usd": 175.0,
        "mmr_rate": 0.010
    },
    "doge_water_averaging": {
        "id": "doge_water_averaging",
        "ticker": "DOGE",
        "name": "도지코인(DOGE) 밈코인 물타기 평단가 및 본전 회복 시뮬레이터",
        "category": "Meme Coin DCA",
        "english_slug": "dogecoin-dca-break-even-calculator",
        "formula_badge": "신규평단 = (기존총액 + 신규총액) / 총수량",
        "key_stat": "도지코인 손익분기점(BEP) 역산",
        "sub_label": "DOGE 분할매수 리스크 관리",
        "benchmark_price_krw": 190.0
    },
    "sei_water_averaging": {
        "id": "sei_water_averaging",
        "ticker": "SEI",
        "name": "세이(SEI) 코인 분할매수 평단가 역산 및 탈출 시뮬레이터",
        "category": "Altcoin DCA",
        "english_slug": "sei-coin-dca-recovery-calculator",
        "formula_badge": "필요수량 = 기존수량 × (기존가 - 목표가) / (목표가 - 현재가)",
        "key_stat": "세이 코인 목표 평단가 도달 필요 자금 역산",
        "sub_label": "알트코인 포지션 회복 모델",
        "benchmark_price_krw": 550.0
    },

    # [절세 & 은퇴 4종]
    "isa_tax_saving": {
        "id": "isa_tax_saving",
        "name": "2026 중개형 ISA 비과세 한도(200만/400만) 및 9.9% 분리과세 비교 계산기",
        "category": "Tax Saving Account",
        "english_slug": "isa-tax-saving-exemption-calculator",
        "law_reference": "조세특례제한법 제91조의18",
        "formula_badge": "비과세: 일반 200만/서민 400만 + 초과 9.9% 분리과세",
        "key_stat": "일반 200만·서민 400만 비과세 | 건보료 합산 제외",
        "sub_label": "조특법 제91조의18 ISA 절세 기준",
        "constants": {"general_limit_krw": 2000000, "low_income_limit_krw": 4000000, "separate_tax_rate": 0.099, "regular_tax_rate": 0.154}
    },
    "pension_savings_tax": {
        "id": "pension_savings_tax",
        "name": "2026 연금저축펀드 세액공제(연 600만) 및 과세이연 복리 시뮬레이터",
        "category": "Retirement Tax Saving",
        "english_slug": "pension-savings-tax-deduction-calculator",
        "law_reference": "소득세법 제59조의3 (연금계좌세액공제)",
        "formula_badge": "환급세액 = 납입원금(최대 600만) × 13.2% 또는 16.5%",
        "key_stat": "연 최대 99만 원 연말정산 세액환급 도출",
        "sub_label": "소득세법 제59조의3 세액공제 기준",
        "constants": {"max_deduction_limit_krw": 6000000, "general_rebate_rate": 0.132, "low_income_rebate_rate": 0.165}
    },
    "irp_retirement_tax": {
        "id": "irp_retirement_tax",
        "name": "2026 개인형 IRP 퇴직연금 세액공제(연 900만) 및 16.5% 환급 계산기",
        "category": "IRP Tax Saving",
        "english_slug": "irp-retirement-tax-saving-calculator",
        "law_reference": "근로자퇴직급여보장법 및 소득세법 제59조의3",
        "formula_badge": "환급세액 = 납입원금(최대 900만) × 16.5%",
        "key_stat": "연 최대 148.5만 원 세액환급 & 과세이연 복리",
        "sub_label": "IRP 퇴직연금 절세 기준",
        "constants": {"max_deduction_limit_krw": 9000000, "rebate_rate": 0.165}
    },
    "ipo_allotment_profit": {
        "id": "ipo_allotment_profit",
        "name": "2026 공모주 청약 증거금 및 균등·비례 배정 기대수익 계산기",
        "category": "IPO Investment",
        "english_slug": "ipo-subscription-equal-proportional-allotment-calculator",
        "formula_badge": "배정주수 = 균등배정 + (내증거금 / 비례경쟁률증거금)",
        "key_stat": "청약 증거금(50%) 및 비례 1주 단가(5사6입) 역산",
        "sub_label": "2026 자본시장법 공모주 배정 기준",
        "constants": {"margin_ratio": 0.50, "commission_fee_krw": 2000}
    }
}

# 룰셋 병합
rules.update(asset_rules)

v3_db = {
    "version": "2026.3.0",
    "updated_at": "2026-10-25",
    "domain": "FinTech, Quant Trading, Tax & Investment Utilities (20 Asset-Specific Matrix)",
    "rules": rules
}

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(v3_db, f, ensure_ascii=False, indent=2)

print(f"✅ [SUCCESS] trading_rules_db.json v3.0 빌드 완료! 총 {len(rules)}개 룰셋 등록됨.")
