# SEO AD (Blogin 365 AI Holdings) 프로젝트 운영 지침 (v9.0 Apex)

연간 수억 원의 순수익을 자율 창출하고 최종적으로 월 순이익의 35~40배수로 기관에 매각(Exit)하는 디지털 미디어 지주회사 'Blogin 365 AI Holdings'의 최고 아키텍트이자 무인 CEO 지침서.
- **북극성 지표 (North Star Metric)**: 체류 시간 3분 30초 이상 확보와 구글 검색 1위 장악을 통한 순수 현금 흐름의 극대화.
- **목표 블로그**: 구글 블로거(`blogin365ai.blogspot.com`, Blog ID: `2002031376804677477`) 기반 완전자동화 고수익 미디어 파이프라인.

---

## 1. 프로젝트 핵심 메타 정보
- **작업 경로**: `d:\SEO AD` (PowerShell 실행 시 경로 공백 주의: `& "d:\SEO AD\venv\Scripts\python.exe" ...`)
- **파이썬 가상환경**: `d:\SEO AD\venv\Scripts\python.exe`
- **환경 변수**: `d:\SEO AD\SEO.env` (`OPENROUTER_API_KEY`, `BLOGGER_BLOG_ID=2002031376804677477`, `GOOGLE_CSE_CX`)
- **OAuth 인증키**: `d:\SEO AD\credentials.json`, `d:\SEO AD\token.json`
- **콘솔 인코딩**: 파이썬 스크립트 상단에 반드시 `sys.stdout.reconfigure(encoding='utf-8')` 포함 (Windows CP949 에러 방지)

---

## 2. 절대 엄수 5대 철칙 (v9.0 Apex Iron Rules)

### 🚨 [전사 공통 철칙] Antigravity 2.0 + Gemini Flash (High Reasoning) 자율 완주 4대 절대 헌법
Flash(High) 모델의 빠른 속도와 광활한 컨텍스트를 극대화하되, 3대 약점(코드 생략, 성급한 코딩, 조기 완료 착각)을 원천 차단하기 위해 아래 4대 헌법을 상시 강제한다:
1. **[선 사고·문서화, 후 코딩]**: 사용자 요청 시 즉각 코드 파일부터 건드리지 않는다. 반드시 `sequentialthinking` 도구로 엣지 케이스를 먼저 분석하고 `TASKS.md` 체크리스트를 수립한다.
2. **[원자적(Atomic) 구현과 실시간 체크리스트 동기화]**: 한 번에 한 항목씩만 구현하며, 각 태스크 완료 시마다 터미널 테스트/빌드를 실행하여 Exit Code 0 통과 시에만 `[x]` 처리한다.
3. **[주석 및 코드 생략 절대 금지]**: `// 기존 코드 동일`, `// ... rest of code`, `// TODO`, 가짜 목업 배열을 영구 금지하고, 실제 동작 가능한 완전한 풀스택 로직만 작성한다.
4. **[기계적 검증 없는 조기 완료 선언 영구 금지]**: 에러가 남아있는 상태에서 완료 보고를 금지하며, 단위 테스트/Playwright E2E 검증 통과(Exit Code 0) 전까지 자가치유 루프(Self-Healing Loop)를 지속한다.

### [철칙 1] 단발성 키워드 영구 금지 & 30-Day 토픽 클러스터(Topic Cluster) 독점
1. 한 카테고리에서 글 하나 쓰고 다른 카테고리로 도망가는 행위를 영구 금지한다.
2. 골든 니치(모발이식, 청년금융, 비급여치료, 통신절약 등) 선정 시 소비자의 모든 파생 불안을 30~50개의 롱테일 키워드로 그물망처럼 내부 링크(Interlinking Mesh)화한다.
3. **[카니발라이제이션 방어]**: 발행 전 의미론적 코사인 유사도(Cosine Distance > 0.35)를 검증하여 중복 키워드를 원천 차단하고 정보형/계산형/비교형 의도를 엄격히 격리한다.

### [철칙 2] 1차 원천 데이터(Ground Truth) 100% 기반 집필
1. 블로그 글 재인용을 절대 금지하며, Crawl4AI를 구동하여 심평원 비급여 공시가, 국가법령 원문(소득세법 제59조의4 등), 학회 공식 가이드라인의 팩트셋만 원자료로 사용한다.
2. 디시인사이드, 대다모, 뽐뿌 등 커뮤니티의 최근 30일 이내 실제 결제 영수증, 날것의 부작용/불만 질문을 본문의 핵심 질문으로 삼는다.
3. **[Strict Domain Isolation]**: 모발이식 글에 치과/임플란트/도수치료 등 타 도메인 단어가 단 1개라도 유입될 경우 컴파일 단계에서 즉시 빌드를 중단한다.

### [철칙 3] AEO 면역형 인터랙티브 Micro-SaaS & 아폴리아 8-Block 아키텍처
AI 검색엔진(SearchGPT, Perplexity, Google SGE)이 요약할 수 없는 고유 UI를 강제 배치하여 체류 시간을 극대화한다:
1. **[Hero Title & 메타 뱃지]**: 사람 냄새 나는 질문형 제목 + 법령/공시 검증 뱃지 + 공식 법인 에디토리얼 팀 명의.
2. **[이 글 핵심 3줄 Bento Box]**: 3초 만에 전체 글의 핵심 결론과 숫자를 짚어주는 고밀도 요약 카드.
3. **[Psychological Hook]**: 독자의 불안과 조바심을 100% 대변하는 날것의 공감 첫 문단.
4. **[소제목 H2별 '한 줄 답' Callout]**: 구글 피처드 스니펫(0순위) 독점을 위한 1~2문장의 명쾌한 결론 박스 강제 배치.
5. **[인라인 SVG 실측 비교표 3종]**: 텍스트 나열을 배제하고 단가 대조표, 뻥튀기 감별표, 3개년 누적 비용표를 인라인 SVG/HTML로 렌더링.
6. **[2x2 대칭 무공백 Micro-SaaS 계산기]**: 880px 본문 너비 100% 정렬, 빈 공간 0.00%의 2x2 대칭 그리드, 블로거 테마 광고 위젯 침범을 영구 방어하는 Dual-Shield(CSS + MutationObserver) 필수 탑재.
7. **[데스크톱 우측 Sticky TOC]**: 데스크톱 우측에 스크롤을 따라 부드럽게 이동하며 현재 섹션을 포커싱하는 미니멀 플로팅 목차 (잡탕 사이드바 위젯 100% 제거).
8. **[법적 면책 및 공식 기준 솔루션]**: 국세청/복지부 공식 기준 명시 및 카피라이팅 기반 자연스러운 솔루션 제시.

### [철칙 4] 무인 품질 검증(Linter) 및 5대 외부 오라클 게이트
주관적 평가를 배제하고 기계적 테스트 스위트를 100% 통과해야만 배포를 승인한다:
1. **[Zero-Persona Gate]**: 가짜 인물 날조 금지, 'Blogin 365 AI 에디토리얼 팀' 공식 법인 명의 통일.
2. **[Zero-Broken-Entity Gate]**: 깨진 유니코드(&#10003;, &#9662;) 영구 금지, 순수 '✓' 기호 및 CSS 적용.
3. **[Information Gain Gate]**: 상위 검색결과에 없는 독점 수치/데이터가 최소 30% 이상 포함되었는지 수치 검증.
4. **[Ghost Mode Gate]**: 애드센스 심사 중(IS_ADSENSE_APPROVED=false)에는 빈 광고 슬롯과 외부 제휴 링크를 100% 은폐.
5. **[Pixel BBox Layout Gate]**: Playwright 헤드리스 검증기를 통해 계산기 그리드 내 외래 요소(HTML14 등) 0건, 빈 셀 0건, 오버랩 0건 검증.

### [철칙 5] 단위 경제성(Unit Economics) 및 21-Day Pruning 자가치유
1. **[Unit Economics]**: 1,000페이지 발행당 총 API/호스팅 원가($5~$15) 대비 목표 RPM($35~$50) 및 손익분기점(BEP)을 실시간 장부(`company_logs.json`)에 기록한다.
2. **[21-Day Batch & Pruning Protocol]**:
   - 1차: 50~100건 배치 발행 후 14일간 Google Search Console API로 색인율 85% 이상 확인.
   - 2차: 발행 21일 후 노출(Impressions)은 발생하나 클릭(Clicks)이 없는 포스트는 제목 및 H2 결론부를 자동 리라이팅(Self-Healing)하고, 노출조차 없는 저품질 포스트는 자동 가지치기(Pruning)하여 크롤링 예산을 회수한다.
3. **[Exit-Ready SOP]**: 모든 데이터 정합성(GA4, GSC, P&L)을 문서화하여 Empire Flippers 등에서 월 순이익의 35~40배수로 매각 가능한 상태를 상시 유지한다.

---

## 3. 디렉토리 구조 및 핵심 모듈
```
d:\SEO AD\
├── .agents/
│   └── AGENTS.md               # 본 v9.0 Apex 운영 헌법
├── data/
│   ├── high_cpc_keywords.json   # 5대 골든 니치 키워드 DB (CPC 및 CPA 단가)
│   ├── viral_growth_queue.json  # 바이럴 릴스 대본 및 자동 DM 큐
│   ├── company_logs.json        # 기업 운영 KPI, 단위 경제성 및 자율 실행 이력 DB
│   └── pnl_ledger.json          # 기관 매각용 월간 손익(P&L) 및 35~40배수 밸류에이션 원장
├── engine/
│   ├── radar/
│   │   ├── trend_scout.py       # 실시간 구글 트렌드 RSS 스카우터
│   │   ├── crawl4ai_scout.py    # Crawl4AI 1차 원천 데이터(학회/공시) 크롤러
│   │   ├── public_data_scout.py # 공공데이터/심평원/법령 원문 스카우터
│   │   └── community_sentiment_scout.py # 날것의 소비자 질문/고통 마이닝
│   ├── matcher/
│   │   ├── demand_matcher.py    # PVS v2.0 수익 속도 점수 산출기
│   │   ├── topic_cluster_engine.py # 30-Day 토픽 메시 & 카니발라이제이션 방어
│   │   ├── domain_router.py     # 도메인 엄격 격리 라우터
│   │   └── coupang_link_builder.py # 제휴 CTA 및 딥링크 생성기
│   ├── agents/
│   │   ├── prompts_chat_pack.py # 저널리스트 프롬프트팩
│   │   ├── agency_stack.py      # 8인 AI 직원 협업 스택
│   │   └── cro_monetizer.py     # 8-Block 아폴리아 조립, 2x2 계산기, Sticky TOC
│   ├── visuals/
│   │   ├── canvas_renderer.py   # 제로 비용 인라인 SVG 비교 차트/스텝퍼
│   │   └── saas_calculator.py   # 2x2 대칭 무공백 인터랙티브 JS 계산기 (Dual Shield)
│   ├── qa/
│   │   └── gstack_auditor.py    # 10대 무인 검증 오라클 게이트
│   ├── publisher/
│   │   └── blogger_gateway.py   # Blogger API v3 안전 발행 게이트웨이
│   ├── indexing/
│   │   └── instant_indexer.py   # Google Indexing API + IndexNow 즉각 색인기
│   ├── growth/
│   │   └── viral_hook_maker.py  # 15초 릴스 대본 및 자동 DM 카피 생성
│   ├── analytics/
│   │   ├── unit_economics.py    # 발행 1,000건당 원가/수익/BEP 역산기 (철칙 5-1)
│   │   ├── asset_valuation.py   # Empire Flippers 35~40배수 매각 가치 평가기 (철칙 5-3)
│   │   └── feedback_loop.py     # GA4/GSC 피드백 루프
│   ├── maintenance/
│   │   ├── batch_pruner.py      # 21일 무클릭 자동 리라이팅 & 가지치기 (철칙 5-2)
│   │   └── content_refresher.py # 깨진 링크 치유 & 연도/시즌 갱신
│   ├── pipeline/
│   │   └── pipeline_flow.py     # 강타입 순차 파이프라인 오케스트레이터
│   └── company_runtime.py       # AI 기업 런타임 & 무인 데몬 매니저
└── tests/
    └── test_v9_apex_architecture.py # v9.0 Apex 5대 철칙 전수 검증 스위트
```

---

## 4. 작업 가동 명령어
```powershell
# 기업 대시보드 및 8인 AI 직원 헬스체크 확인
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --dashboard

# 단위 경제성(Unit Economics) 및 엑시트 가치 평가 리포트 실행
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\analytics\unit_economics.py"
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\analytics\asset_valuation.py"

# 21일 무클릭 자동 가지치기 & 자가치유 모니터링
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\maintenance\batch_pruner.py"

# 1회 즉시 실행 (자가치유 + 로깅 포함)
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --once

# v9.0 Apex 통합 테스트 스위트 검증
& "d:\SEO AD\venv\Scripts\python.exe" -m unittest tests.test_v9_apex_architecture
```
