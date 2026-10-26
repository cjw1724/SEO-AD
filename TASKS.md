# TASKS.md - Blogin 365 AI Holdings (v9.0 Apex) 무인 자율 미디어 운영 체계 구축

## 📌 목표
1. **Tier 1 (플래그십)**: `https://blogin365ai.blogspot.com/p/vibe-trading.html` 상설 독립 웹앱 100% 무결점 유지
2. **Tier 2 (포털 피드)**: 블로그 홈 피드의 중복 테스트 포스트 정리 및 4대 핵심 핀테크 유틸리티(해외주식 세금, 물타기 평단가, 레버리지 청산가, 배당 복리과세) 전면 배치
3. **Tier 3 (무인 자동화)**: `engine/company_runtime.py`에 `EditorialInspector` 완전 결합 및 Windows Task Scheduler 스크립트 작성으로 매일 무인 자율 발행 체계 완성
4. **품질 검증**: Playwright 3대 뷰포트(데스크톱, 모바일) 시각 검증 및 유닛 테스트(Exit Code 0) 완료

---

### [Phase 1] 블로그 홈 및 피드 정돈 (중복 테스트 글 정리)
- [x] **Task 1.1**: 마스터 구현 계획서(`implementation_plan.md`) 및 8인 AI 조직도(`prompt_draft.md`) 작성 완료
- [x] **Task 1.2**: 테스트 과정에서 생성된 중복 포스트 4건을 Draft로 전환하여, 홈 피드에 고유 4대 시뮬레이터가 깔끔하게 노출되도록 정리 완료
- [x] **Task 1.3**: 홈 화면 및 개별 포스트 최상단 네비게이션이 `🔥 VIBE TRADING (모의투자 랭킹전)`과 홈 피드로 매끄럽게 연결되는 양방향 네비게이션 확인 완료

---

### [Phase 2] 무인 24/7 자동화 체계 수립 (`/automation`)
- [x] **Task 2.1**: `engine/company_runtime.py`에 `EditorialInspector`를 정식 파이프라인 단계로 통합 완료 (발행 전 Playwright 비주얼 렌더링 및 폰트/배경색 명도비 자동 검증·치유)
- [x] **Task 2.2**: Windows Task Scheduler 자동 등록 스크립트(`scripts/setup_windows_scheduler.ps1`) 제작 및 시스템 등록 완료 (`Blogin365_Autonomous_Publisher`, State: Ready)
- [x] **Task 2.3**: 수동 실행 없이도 1회 자동 실행(`company_runtime.py --once`)이 결함(Exit Code 0) 없이 성공함을 검증 완료 (Task 4076 성공 완주)

---

### [Phase 3] 다중 뷰포트 시각 검증 및 슬롭 영구 박멸 (`/browser`)
- [x] **Task 3.1**: 데스크톱(1280px) 및 모바일(375px)에서 메인 홈, Vibe Trading 웹앱, 개별 포스트 3대 영역 스크린샷 캡처 및 아티팩트 저장 완료
- [x] **Task 3.2**: 글자 안 보임(투명화), 흰색 박스 번짐, 텍스트 깨짐, 레이아웃 뭉개짐 0건 기계적 증명 완료 (글자 투명도 결함 0건, 전 페이지 HTTP 200 통과)

---

### [Phase 4] 마스터 핸드오버 및 최종 보고
- [x] **Task 4.1**: 전체 통합 테스트 스위트(`tests/test_v9_apex_architecture.py`) 전수 패스 확인 (Exit Code 0, 15/15 tests passed)
- [x] **Task 4.2**: 최종 완료 보고서 작성 및 사용자 승인 (`<!-- GOAL_COMPLETE -->`)

---

### [Phase 5] Vibe Strategy Lab: 인터랙티브 트레이딩뷰 전략 백테스팅 & 실시간 모의투자 추종 엔진
- [x] **Task 5.1**: `engine/visuals/strategy_lab_renderer.py` 엔진 구축 (TradingView Lightweight Charts v4.1 + 바이낸스 500개 캔들 REST + 1분봉 실시간 웹소켓 + 인-브라우저 0.01초 팩트체크 백테스터 + 차트 위 매수/매도 시그널 마커 + 실시간 가상 매매 추종 토글)
- [x] **Task 5.2**: 단위 테스트 `tests/test_strategy_lab_renderer.py` 작성 및 실행 (Exit Code 0 확인)
- [x] **Task 5.3**: 1호 킬러 파일럿 포스트 [워뇨띠 Q&A 기반 볼린저밴드 이탈 반등 매매법] 풀스택 아티클 및 전략 위젯 결합 생성
- [x] **Task 5.4**: 로컬 Playwright 인터랙티브 E2E 검증 (차트 렌더링, 시그널 마커 생성, 슬라이더 조작 시 승률 재계산, WCAG AAA 명도비)
- [x] **Task 5.5**: Blogger API v3 실제 라이브 발행 및 실물 캡처 증빙 (https://blogin365ai.blogspot.com/2026/10/2026-q.html)
- [x] **Task 5.6**: 메인 홈 피드 및 VIBE TRADING 프로 스테이션 간의 유기적 네비게이션 연동 및 최종 보고서 작성

---

### [Phase 6] 100% 무인 24/7 데일리 자율 포스팅 파이프라인 완성 & 실시간 기계적 증명
- [x] **Task 6.1**: `engine/crew/strategy_pipeline.py`에 큐 자동 보충기(`auto_replenish_queue()`) 탑재 (대기열 소진 시 10대 유명 퀀트 전략 자동 충전) 및 dry_run 큐 오염 방지 버그 수정
- [x] **Task 6.2**: `data/strategy_topics_queue.json`에서 `supertrend_rsi_scalping` 상태를 `PENDING`으로 정상화하여 다음 자율 실행 대기열 장착
- [x] **Task 6.3**: `engine/company_runtime.py`에 `StrategyLabPipeline`을 자율 런타임 디스패처로 직결 통합 (`--once` 실행 시 자동으로 대기열 전략 발굴·검증·배포 완주)
- [x] **Task 6.4**: 터미널에서 `company_runtime.py --once`를 무인 실행하여 2호 전략(슈퍼트렌드+RSI 1분봉 스캘핑)을 100% 자율 발행하고 실시간 블로거 URL 및 큐 업데이트 검증
- [x] **Task 6.5**: Playwright 실물 시각 검증 및 통합 테스트 스위트 실행 (Exit Code 0 확인) 후 사용자에게 완전 무인 운영 체계 기계적 증명 보고

---

### [Phase 7] GitHub Actions 100% 무료 클라우드 무인 자동화 구축 (PC 영구 종료 가능)
- [x] **Task 7.1**: `.gitignore` 업데이트 (`!data/strategy_topics_queue.json`, `!data/company_logs.json` 허용하여 상태 영구 지속성 확보)
- [x] **Task 7.2**: `requirements.txt` 최적화 정리 (Playwright, Google Auth, requests, pydantic 등 CI 런타임 패키지 명시)
- [x] **Task 7.3**: `scripts/bootstrap_ci_secrets.py` 구축 (CI 환경에서 GitHub Secrets로부터 `credentials.json`, `token.json`, `SEO.env` 무결점 복원)
- [x] **Task 7.4**: `.github/workflows/autonomous_publisher.yml` 워크플로우 제작 (Cron 09:00/15:00/21:00 KST + workflow_dispatch + Auto Commit/Push state)
- [x] **Task 7.5**: `scripts/export_github_secrets.py` 제작 (GitHub 저장소 `Settings -> Secrets`에 등록할 5대 비밀키 원클릭 출력 도구)
- [x] **Task 7.6**: CI 부트스트랩 및 로컬 시뮬레이션 무결점 검증 (Exit Code 0)
- [x] **Task 7.7**: Git 커밋 & 원격 저장소(`origin main`) 푸시 및 사용자 등록 가이드 제공

---

### [Phase 8] 트레이딩뷰 롱/숏(Long & Short) 양방향 퀀트 엔진 전면 업그레이드 및 실시간 배포
- [x] **Task 8.1**: `engine/visuals/strategy_lab_renderer.py`에 롱(BUY) 및 숏(SELL) 양방향 타점 탐지/청산 알고리즘 및 마커(`BUY (롱) @ $xxx`, `SELL (숏) @ $xxx`, `TP (롱)`, `TP (숏)`, `SL`) 완전 구현
- [x] **Task 8.2**: 상단 HUD 범례(`▲ 롱 / ▼ 숏`) 및 4대 Bento KPI(롱/숏 통합 승률, 손익비, MDD) 동기화
- [x] **Task 8.3**: 단위 테스트 `tests/test_strategy_lab_renderer.py` 양방향 로직 검증 및 통과 (Exit Code 0)
- [x] **Task 8.4**: 라이브 발행된 포스트 2건(워뇨띠 1호, 슈퍼트렌드 2호)에 새 양방향 롱/숏 엔진 즉시 Blogger API 라이브 패치 배포
- [x] **Task 8.5**: Playwright E2E 시각 검증 실행하여 `SELL (숏)` 마커 및 양방향 시그널 렌더링 스크린샷 캡처 및 최종 완료 보고

---

### [Phase 10] 기관급 보수적 퀀트 백테스팅 수학 엔진 전면 개편 (리얼리스틱 체결 & 수수료 반영 & 조작 의혹 영구 박멸)
- [x] **Task 10.1**: 4대 치명적 계산 왜곡 요인(장중 저가 무시, 밴드 상단 스침 시 무조건 100% TP 인정, SL/TP 동시 발생 시 TP 우선 편향, 수수료 0% 무비용 가정) 분석 및 TASKS.md 수립
- [x] **Task 10.2**: `engine/visuals/strategy_lab_renderer.py` 백테스팅 엔진 리팩토링 (Intra-bar High/Low 기반 체결, 최악 상황(SL 우선) 체결 원칙, 바이낸스 선물 왕복 수수료 0.10% + 슬리피지 0.02% 반영, 정밀 순수익 계산)
- [x] **Task 10.3**: 단위 테스트 `tests/test_strategy_lab_renderer.py` 실행 및 통과 (Exit Code 0)
- [x] **Task 10.4**: 라이브 포스트 2건(워뇨띠 1호, 슈퍼트렌드 2호)에 정통 퀀트 엔진 Blogger API 라이브 패치 배포
- [x] **Task 10.5**: Playwright 헤드리스 검증으로 라이브 블로그에서 비현실적인 100% 승률 대신 정밀하고 현실적인 승률/손실 거래/PF/MDD 렌더링 확인 및 스크린샷 증빙
- [x] **Task 10.6**: 사용자에게 계산 결함 원인 및 개선 결과 투명하게 최종 보고

---

### [Phase 11] 차트 위 실시간 손절선(SL)/익절선(TP) 시각화 & VIBE TRADING 모의투자 100% 자동매매 연동
- [x] **Task 11.1**: `engine/visuals/strategy_lab_renderer.py`에 TradingView `createPriceLine` 기반 손절선(🔴 SL -0.5%), 익절선(🟢 TP +0.8%), 진입선(🟡 Entry) 실시간 수평 가격선 동적 렌더러 탑재
- [x] **Task 11.2**: 실시간 모의투자 추종 엔진(`checkLivePaperTradeSignal`)에 롱/숏 양방향 진입 로직 및 VIBE TRADING 표준 스키마(`asset: BTC/USDT`, `margin`, `size`, `botSource`) 완전 결합
- [x] **Task 11.3**: `engine/fintech/vibe_trading_station.py`에 전략 봇 자동 체결 포지션(`bot_`) 감지 및 UI 뱃지(`🤖 [AI 전략봇]`) 표시 지원
- [x] **Task 11.4**: 단위 테스트 실행 및 라이브 블로그 포스트 2건 & Vibe Trading 독립 페이지 Blogger API 라이브 배포
- [x] **Task 11.5**: Playwright E2E 검증 (차트 위 손절선 시각 표시 및 Vibe Trading 모의투자 자동매매 연동 실측 캡처) 및 사용자 보고

---

### [Phase 12] `TP 0.0%` 슬롭 영구 박멸 & TradingView 공식 프로 차트 듀얼 탭 탑재
- [x] **Task 12.1**: `hitBand` 제거 및 순수 브래킷 OCO(고정 TP vs SL) 모델로 리팩토링하여 `TP 0.0%` 마커 영구 박멸
- [x] **Task 12.2**: 차트 상단에 `🌐 트레이딩뷰 공식 프로 차트` (TradingView Advanced Real-Time Widget) 탭 장착하여 듀얼 엔진 체계 구축
- [x] **Task 12.3**: 단위 테스트 실행 및 통과 (Exit Code 0)
- [x] **Task 12.4**: 라이브 블로그 포스트 2건에 Blogger API 라이브 패치 배포
- [x] **Task 12.5**: Playwright E2E 검증 (`TP 0.0%` 부재 확인, 깔끔한 마커 렌더링, 트레이딩뷰 공식 위젯 전환 확인) 및 최종 보고

---

### [Phase 13] 타임프레임(1분봉/15분봉) 일관성 100% 동기화 & 하드코딩 슬롭 영구 박멸
- [x] **Task 13.1**: `StrategyLabRenderer.render()`에서 4대 타임프레임 버튼 스타일(`btn_1m`, `btn_5m`, `btn_15m`, `btn_1h`)을 전략의 `interval`에 따라 동적 주입 및 설명문 텍스트(`{interval_kor}`) 동적 치환
- [x] **Task 13.2**: TradingView 공식 프로 위젯 `interval` 매개변수를 전략 기준 타임프레임(`tvInterval`)으로 1:1 동기화
- [x] **Task 13.3**: 단위 테스트 실행 및 라이브 블로그 포스트 2건 Blogger API 라이브 재배포
- [x] **Task 13.4**: Playwright E2E 검증 (슈퍼트렌드 포스트에서 `1분봉` 버튼 활성화 및 설명문 100% 일치 실측 캡처) 및 사용자 보고

---

### [Phase 14] 다형성 퀀트 엔진: 슈퍼트렌드(Supertrend) + RSI 1분봉 실체화 & 전략 로직 불일치 영구 종결
- [x] **Task 14.1**: `data/strategy_topics_queue.json`에서 `supertrend_rsi_scalping` 파라미터를 슈퍼트렌드 규격(`st_period: 10, st_mult: 3.0, rsi_threshold: 40, tp_percent: 0.8, sl_percent: 0.5`)으로 정규화 완료
- [x] **Task 14.2**: `engine/visuals/strategy_lab_renderer.py`에 `computeSupertrend()` 알고리즘 및 전략별 다형성 지표/차트선/진입시그널/슬라이더 분기 탑재 완료 (본문 설명과 100% 일치: 슈퍼트렌드 강세 전환 + RSI 40 이상 돌파 + 거래량 1.2배 시 BUY 진입, 약세 전환 + RSI 60 이하 돌파 시 SELL 진입)
- [x] **Task 14.3**: 단위 테스트 `tests/test_strategy_lab_renderer.py`에 슈퍼트렌드 전용 렌더링 검증 추가 및 전수 통과 (Exit Code 0, 4/4 passed)
- [x] **Task 14.4**: 라이브 블로그 포스트 2건 Blogger API 라이브 재배포 완료
- [x] **Task 14.5**: Playwright E2E 검증 (슈퍼트렌드 추세선 렌더링, HUD 슈퍼트렌드 지지/저항 표시, 손절선 SL -0.5% / ROE -2.5% 투명화, 본문 설명과 100% 일치하는 타점 마킹 실측) 및 최종 보고 완료
