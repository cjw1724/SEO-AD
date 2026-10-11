# SEO AD (Blogin 365 AI) 프로젝트 운영 지침

구글 블로거(`blogin365ai.blogspot.com`, Blog ID: `2002031376804677477`) 기반 완전자동화 고수익 미디어 파이프라인.

---

## 1. 프로젝트 핵심 메타 정보
- **작업 경로**: `d:\SEO AD` (PowerShell 실행 시 경로 공백 주의: `& "d:\SEO AD\venv\Scripts\python.exe" ...`)
- **파이썬 가상환경**: `d:\SEO AD\venv\Scripts\python.exe`
- **환경 변수**: `d:\SEO AD\SEO.env` (`OPENROUTER_API_KEY`, `BLOGGER_BLOG_ID=2002031376804677477`)
- **OAuth 인증키**: `d:\SEO AD\credentials.json`, `d:\SEO AD\token.json`
- **콘솔 인코딩**: 파이썬 스크립트 상단에 반드시 `sys.stdout.reconfigure(encoding='utf-8')` 포함 (Windows CP949 에러 방지)

---

## 2. 삼각 수익화 모델 (Tri-Monetization Model)
무지성 회생/파산 등 비선호 주제를 완전히 배제하고 실제 구매/행동 전환이 일어나는 고부가가치 주제 공략:
1. **AdSense (방법 A)**: 반응형 Micro-SaaS 계산기(적금, 지원금, 통신비 절약)로 체류 시간(Dwell Time) 2분 이상 확보 및 황금 4슬롯 노출.
2. **CPA / CPS 제휴마케팅 (방법 B)**: 쿠팡 파트너스 3% 및 링크프라이스/애드픽 고단가 상품(20,000~85,000원) 비교표 및 네이티브 CTA 연동.
3. **바이럴 SNS 루프 (방법 C)**: 인스타그램 릴스/스레드 15초 대본 및 "댓글에 10 남겨주시면 가이드 자동 발송" DM 트리거를 통해 검색 샌드박스 기간 우회 및 당일 수천 PV 유입.

---

## 3. 절대 엄수 운영 3대 원칙 (Zero-Slop Policy)
1. **절대 가짜 인물 날조 금지 (Zero-Persona Policy)**:
   - "금융 전문 기자 김재현"과 같은 가상 기자/전문가 이름 및 경력 날조 절대 불가 (한국 법률 및 실존 인물 명의도용 엄격 금지).
   - 모든 발행물은 브랜드명 `Blogin 365 AI` 또는 `스마트 라이프 에디토리얼 팀` 공식 명의로만 발행.
2. **깨진 HTML 엔티티 금지 (Zero Broken Entity)**:
   - `&#10003;`, `&#9662;` 등 깨지는 엔티티 사용 금지. 체크마크는 SVG/텍스트 `✓`, 토글은 순수 CSS `.faq-chevron` 사용.
3. **클리셰 문구 제거 (Anti-Slop Gates)**:
   - "현대 사회에서", "알아보겠습니다", "총정리해 드립니다" 등 기계적 어투 배제.
   - 첫 문장은 반드시 구체적 수치 또는 핵심 결론(Bento Hero Card)으로 시작.

---

## 4. 디렉토리 구조 및 핵심 모듈
```
d:\SEO AD\
├── .agents/
│   └── AGENTS.md               # 본 운영 매뉴얼
├── data/
│   ├── high_cpc_keywords.json   # 5대 골든 니치 키워드 DB (CPC 및 CPA 단가)
│   ├── viral_growth_queue.json  # 바이럴 릴스 대본 및 자동 DM 큐
│   └── company_logs.json        # 기업 운영 KPI 및 자율 실행 이력 DB
├── engine/
│   ├── radar/
│   │   └── trend_scout.py       # 실시간 구글 트렌드 RSS 스카우터 (Phase 1)
│   ├── matcher/
│   │   ├── demand_matcher.py    # PVS v2.0 수익 속도 점수 산출기 (Phase 1)
│   │   └── coupang_link_builder.py # 제휴 CTA 및 딥링크 생성기
│   ├── agents/
│   │   ├── prompts_chat_pack.py # prompts.chat 기반 저널리스트 프롬프트팩
│   │   ├── agency_stack.py      # AI 직원 협업 스택 (Phase 2)
│   │   └── cro_monetizer.py     # HTML 최종 조립 및 광고 슬롯 배치 (Phase 3)
│   ├── visuals/
│   │   ├── canvas_renderer.py   # 제로 비용 인라인 SVG 비교 차트/스텝퍼
│   │   └── saas_calculator.py   # 카테고리별 인터랙티브 JS 계산기 위젯
│   ├── qa/
│   │   └── gstack_auditor.py    # 57개 Slop-Test + Google HCU 안티스팸 무인 검수기 (Phase 4)
│   ├── publisher/
│   │   └── blogger_gateway.py   # Blogger API v3 안전 발행 게이트웨이 (Phase 5)
│   ├── indexing/
│   │   └── instant_indexer.py   # Google Indexing API + IndexNow 즉각 색인기 (Phase 5 Pillar 1)
│   ├── growth/
│   │   └── viral_hook_maker.py  # 15초 릴스 대본 및 자동 DM 카피 생성 (Phase 6)
│   ├── distribution/
│   │   └── multi_channel_distributor.py # Threads, X, ManyChat 웹훅 배포기 (Phase 6 Pillar 3)
│   ├── analytics/
│   │   └── feedback_loop.py     # GA4/GSC 폐쇄 루프 피드백 & 가중치 튜너 (Phase 7 Pillar 2)
│   ├── maintenance/
│   │   └── content_refresher.py # 404 깨진 링크 치유 & 연도/시즌 콘텐츠 갱신 (Phase 7 Pillar 4)
│   ├── pipeline/
│   │   └── pipeline_flow.py     # 강타입 7단계 순차 파이프라인 오케스트레이터
│   ├── company_runtime.py       # AI 기업 런타임 & 8인 AI 직원 데몬 매니저 (v6.0)
│   └── main.py                  # 일일 정기 자동화 오케스트레이터
├── legacy/
│   └── blogs/                   # 구버전 레거시 시스템 아카이브 (GitDiagram 노드 정돈)
├── setup_scheduler.ps1          # 윈도우 작업 스케줄러 365일 무인 등록 (PowerShell)
├── setup_scheduler.bat          # 윈도우 작업 스케줄러 등록 (배치 파일 원클릭)
├── unregister_scheduler.bat     # 윈도우 작업 스케줄러 제거 배치 파일
├── start.bat                    # 인터랙티브 AI 기업 제어 센터
└── tests/
    ├── test_phase1.py           # 페이즈 1 단위 테스트
    ├── test_company_runtime.py  # 기업 런타임 & 자가치유 단위 테스트
    ├── test_end_to_end.py       # 전체 파이프라인 E2E 검증 테스트
    └── test_advanced_pillars.py # 5대 코어 확장 필러 통합 검증 테스트
```

---

## 5. 작업 재개 시 빠른 명령어
```powershell
# 기업 대시보드 및 8인 AI 직원 헬스체크 확인
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --dashboard

# 1회 즉시 실행 (자가치유 + 로깅 포함)
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --once

# 안전 테스트 모드 (Blogger 실제 발행 제외)
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --once --dry-run

# 24/7 상시 백그라운드 무인 데몬 가동 (09:00, 15:00, 21:00 발행)
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --daemon

# 윈도우 작업 스케줄러 등록 (365일 무인 자동 가동)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "d:\SEO AD\setup_scheduler.ps1"

# 단위 및 E2E 테스트 검증
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\tests\test_company_runtime.py"
& "d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\tests\test_end_to_end.py"
```
