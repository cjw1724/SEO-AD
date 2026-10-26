# TASKS.md - 하드코딩 템플릿 및 가짜 검색 지표 영구 박멸 & 100% 실시간 서제스트 레이더 대개혁

## 📌 문제점 및 사용자 지적 분석
1. **하드코딩 템플릿의 잔재 (`fallback_pool`)**:
   - `engine/matcher/demand_matcher.py`에 도메인별로 `비급여 실제 가격 비교`, `실손보험 실비 청구 기준`, `시술 전 필수 주의사항` 등을 뒤에 무조건 덧붙이는 하드코딩 템플릿이 남아있었음.
   - 이로 인해 실제 검색어 분석이 아니라 매드립스(Mad-Libs) 기계적 조합 문자열이 H2 소제목으로 출력되는 심각한 결함 발생.
2. **가짜 지표 날조 로직 (`est_docs = 650`, `ratio = 76.92`)**:
   - `trend_scout.py`에서 단어 수에 따라 `32000`, `8500`, `1400`을 임의로 날조하고,
   - `demand_matcher.py`에서 `est_docs = 650`을 하드코딩하여 `50000 / 650 = 76.92`라는 가짜 '최적 골든비율'을 출력하던 기만 로직 존재.
3. **무작위 더미 추출 (`random.choice`)**:
   - 트렌드 매칭 실패 시 `random.choice(list(niches.keys()))`로 특정 키워드를 무작위로 뽑아내어 실시간성 상실.

---

## 🏗️ 개혁 아키텍처 (100% Real Live Search Radar)
```mermaid
flowchart TD
    RawKW[타겟 키워드 / 실시간 트렌드] --> Decomp[지능적 어절/시드 분해기]
    Decomp --> GSuggest[Google Suggest API 실시간 쿼리]
    Decomp --> NSuggest[Naver Search Suggest API 실시간 쿼리]
    
    GSuggest & NSuggest --> RealQueries[실제 국민 실시간 롱테일 검색어 집계]
    RealQueries --> Filter[의도별 상위 3대 검색어 추출: 비용 / 위험사고 / 실제후기]
    Filter --> H2Alloc[1:1 H2 소제목 할당 (하드코딩 0%)]
    
    RawKW --> CleanEval[정직한 실측 지표 평가: 가짜 650/76.92 날조 완전 제거]
    CleanEval --> PVS[실제 검색 의도 & 도메인 기준 PVS v2.0 산출]
```

---

## 📋 원자적 체크리스트 (Atomic Checklist)

### [Phase 1] `trend_scout.py` 실시간 지능형 서제스트 개편 & 가짜 수식 삭제
- [x] **Task 1.1**: 단어 수 기반 가짜 검색량 조작(`word_count == 1: 32000`) 완전 삭제
- [x] **Task 1.2**: 복합 검색어를 어절/핵심 명사 조합으로 분해하여 Google Suggest & Naver Suggest를 실시간 교차 수집하는 `expand_smart_suggestions()` 구현
- [x] **Task 1.3**: `expand_autocomplete()`를 `expand_smart_suggestions()`로 완전 대체

### [Phase 2] `demand_matcher.py` 하드코딩 `fallback_pool` & 가짜 650/76.92 영구 박멸
- [x] **Task 2.1**: 도메인별 3줄 기계적 문자열 템플릿(`fallback_pool`) 완전 삭제
- [x] **Task 2.2**: `generate_sub_keywords()`가 실시간 Google/Naver 서제스트에서 추출된 실제 검색어(`수면 임플란트 비용`, `수면 임플란트 사고`, `수면 임플란트 후기` 등)를 100% 우선 할당하도록 리팩토링
- [x] **Task 2.3**: `est_docs = 650`, `est_pub = 120` 하드코딩 및 가짜 76.92 비율 날조 제거 -> 실측 의도 및 구글 트렌드 실제 지표 기반으로 정직한 평가 출력
- [x] **Task 2.4**: `random.choice` 더미 키워드 강제 주입 로직 제거

### [Phase 3] 기계적 검증 및 실시간 검색어 할당 증명
- [x] **Task 3.1**: 단위 테스트 스위트 통과 (Exit Code 0)
- [x] **Task 3.2**: `company_runtime.py`를 실행하여 가짜 76.92와 하드코딩 템플릿이 완전히 사라지고, Google/Naver의 실제 실시간 검색어가 H2 소제목으로 1:1 매핑됨을 기계적으로 증명
- [x] **Task 3.3**: 사용자에게 투명하게 원인 고백 및 개혁 결과 보고
