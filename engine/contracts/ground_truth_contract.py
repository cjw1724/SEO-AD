# -*- coding: utf-8 -*-
"""
engine/contracts/ground_truth_contract.py
-----------------------------------------
HIRA 공공데이터 및 비정형 커뮤니티 센티먼트 정규화를 위한 엔터프라이즈 Data Contract (v9.0 Apex).
[Patch 1 적용] ALLOWED_GENERIC_HOSPITALS 화이트리스트 기반 오탐지(False Positive) 방어.
"""

import re
from typing import List, Optional, Literal, Set
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator


# [Patch 1] 일반 명사 병원 화이트리스트 (법적 처벌 대상 아닌 일반 명사)
ALLOWED_GENERIC_HOSPITALS: Set[str] = {
    "대학병원",
    "종합병원",
    "상급종합병원",
    "전문병원",
    "개인병원",
    "동네의원",
    "일반의원",
    "해당병원",
    "인근병원",
    "협력병원",
    "지정병원",
    "국공립병원"
}


class HospitalPriceItem(BaseModel):
    """심평원 1차 공시 수가 정량 데이터"""
    procedure_code: str = Field(..., description="비급여 행위 코드 (예: MZ001)")
    procedure_name: str = Field(..., description="행위 명칭 (예: 모발이식술-비절개)")
    unit: Literal["모", "모낭", "부위", "회"] = Field(..., description="과금 단위")
    min_price_krw: int = Field(..., ge=0, description="최저 공시가")
    median_price_krw: int = Field(..., ge=0, description="중앙 공시가 (기준값)")
    max_price_krw: int = Field(..., ge=0, description="최고 공시가")
    source_agency: str = Field(default="건강보험심사평가원", description="공시 기관")
    effective_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="고시 기준일")

    @model_validator(mode="after")
    def validate_price_order(self):
        if not (self.min_price_krw <= self.median_price_krw <= self.max_price_krw):
            raise ValueError(
                f"수가 범위 오류: min({self.min_price_krw}) <= median({self.median_price_krw}) <= max({self.max_price_krw}) 조건을 만족해야 합니다."
            )
        return self


class CommunitySentimentFact(BaseModel):
    """디시/대다모 비정형 텍스트 정제 및 익명화 데이터"""
    platform: Literal["DCINSIDE", "DAEDAMO", "PPOMPPU"] = Field(..., description="수집 채널")
    post_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="작성일자 (최근 30일 이내)")
    extracted_expense_krw: Optional[int] = Field(None, ge=0, description="실제 영수증 결제 금액")
    graft_or_count: Optional[int] = Field(None, ge=0, description="시술 수량 (예: 3000)")
    raw_pain_point: str = Field(..., min_length=5, max_length=200, description="소비자의 날것 질문/불만")
    sanitized_text: str = Field(..., description="병원명 및 실명이 마스킹된 본문 요약")

    @field_validator("sanitized_text")
    @classmethod
    def mask_private_entities(cls, v: str) -> str:
        """
        의료법 제56조 준수: 특정 병원명 및 원장 실명 정규식 마스킹.
        [Patch 1] ALLOWED_GENERIC_HOSPITALS 화이트리스트에 포함된 단어는 마스킹에서 제외하여 오탐지 방어.
        """
        def _replace_clinic(match):
            full_match = match.group(0)
            if full_match in ALLOWED_GENERIC_HOSPITALS:
                return full_match
            suffix = match.group(2)
            return f"OO{suffix}"

        # 1. 병원명 마스킹 (화이트리스트 통과 필터 적용)
        v = re.sub(r'([가-힣]{1,4})(성형외과|피부과|의원|병원)', _replace_clinic, v)
        # 2. 원장 실명 마스킹
        v = re.sub(r'([가-힣]{1})(원장|선생님|의사)', r'X\2', v)
        # 3. 전화번호 마스킹
        v = re.sub(r'\b010-\d{4}-\d{4}\b', '[연락처 마스킹]', v)
        v = re.sub(r'\b02-\d{3,4}-\d{4}\b', '[대표번호 마스킹]', v)
        return v


class StatutoryFramework(BaseModel):
    """국가법령 및 학회 가이드라인 표준 메타데이터"""
    statute_name: str = Field(..., description="법령명 (예: 소득세법 제59조의4)")
    clause_title: str = Field(..., description="조항 조문 (예: 의료비 세액공제)")
    legal_limitation: str = Field(..., description="적격/부적격 판정 기준 (예: 미용 목적 시술 공제 불가)")
    academic_guideline: str = Field(..., description="공식 학회 권고 수칙 (예: ISHRS 2주간 혈압 상승 운동 금지)")


class StandardizedFactsetContract(BaseModel):
    """
    [SSOT Data Contract]
    Market Researcher(03) -> UI/Dev(04/05) 및 Editorial로 주입되는 유일무이한 표준 데이터 계약
    """
    niche_id: str = Field(..., pattern=r"^[a-z_]+$", description="니치 식별자")
    cluster_pillar_keyword: str = Field(..., description="토픽 클러스터 기둥 키워드")
    target_keyword: str = Field(..., description="선정된 롱테일 키워드")
    target_intent: Literal["CALC", "COMPARE", "INFO"] = Field(..., description="격리된 검색 의도")
    hira_baseline: HospitalPriceItem = Field(..., description="심평원 기준 단가")
    community_voices: List[CommunitySentimentFact] = Field(..., min_length=1, max_length=5, description="커뮤니티 검증 보이스")
    legal_anchor: StatutoryFramework = Field(..., description="법령/학회 원천 데이터")
    contract_created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        frozen = True
