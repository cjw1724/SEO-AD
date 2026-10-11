# 🏢 Blogin 365 AI Holdings (v6.0)

> **24/7 완전자동화 고수익 미디어 파이프라인 & AI 자율 기업 운영 체계**  
> Google Blogger (`blogin365ai.blogspot.com`) 기반 트렌드 수집, PVS v2.0 상업성 분석, 마이크로 SaaS 계산기 조립, 57개 게이트 무인 검수 및 바이럴 SNS 루프 통합 엔진.

---

## 🌟 핵심 특징 (Key Highlights)

1. **삼각 수익화 모델 (Tri-Monetization Model)**:
   - **Method A (AdSense)**: 반응형 Micro-SaaS JS 계산기와 Bento 시각화로 체류 시간(Dwell Time) 2분 이상 확보 & 황금 4슬롯 노출.
   - **Method B (CPA/CPS)**: 쿠팡 파트너스 및 공식 환급 시스템 네이티브 CTA 연동.
   - **Method C (SNS Viral Loop)**: 15초 릴스 대본 및 "댓글에 10 남기시면 자동 발송" DM 트리거로 당일 대량 PV 유입.
2. **7단계 골든 키워드 판정 & 1:1 H2 소제목 배치**:
   - `비율 = 월간 검색량 ÷ 블로그 문서 수` 공식을 통한 7-Tier 경쟁도 필터링 (`최적`, `가능`, `과열`, `어려움`, `벽`, `허수`, `포화`).
   - 메인 키워드 제목 맨 앞단 1회 배치 & 서브 키워드 H2 소제목 1:1 전담 매핑으로 롱테일 유입 극대화.
3. **절대 엄수 운영 3대 원칙 (Zero-Slop Policy)**:
   - **Zero-Persona**: 가상 인물 및 기자 명의 날조 절대 금지 (공식 에디토리얼 팀 명의 발행).
   - **Zero Broken Entity**: 깨지는 특수문자 전면 배제 및 순수 CSS 토글 아코디언 적용.
   - **Anti-Slop Gates**: 기계적 AI 상투어 100% 필터링.
4. **365일 무인 자율 데몬 & 윈도우 스케줄러**:
   - 윈도우 작업 스케줄러 연동으로 매일 정해진 시각(09:00, 15:00, 21:00)에 절전 모드 자동 기상(`WakeToRun`) 및 비대화형 OAuth 토큰 자가 갱신.

---

## 🏛️ 8인 AI 직원 조직도 (Org Chart)

| 직책 (Role) | 파일 / 모듈 | 주요 임무 |
|---|---|---|
| **01 Chief of Staff** | `engine/main.py` | 6단계 파이프라인 총괄 하네스 조율 |
| **02 Product Planner** | `engine/matcher/demand_matcher.py` | PVS v2.0 수익성 산출 및 5대 황금 니치 매칭 |
| **03 Market Researcher**| `engine/radar/trend_scout.py` | 구글 트렌드 KR RSS 및 네이버 자동완성 실시간 분석 |
| **04 UI Designer** | `engine/visuals/canvas_renderer.py` | Bento Bar 차트 및 시각 컴포넌트 렌더링 |
| **05 Developer** | `engine/visuals/saas_calculator.py` | 카테고리별 반응형 JS 계산기 위젯 개발 |
| **06 QA Tester** | `engine/qa/gstack_auditor.py` | 57개 Slop-Test 게이트 무인 검수 및 발행 차단 |
| **07 Marketer** | `engine/growth/viral_hook_maker.py` | 15초 릴스 대본 및 ManyChat 자동 DM 큐 생성 |
| **08 CS & Publisher** | `engine/publisher/blogger_gateway.py` | Schema JSON-LD 주입 및 Google Blogger v3 안전 발행 |

---

## 🚀 빠른 시작 (Quick Start)

### 1. 환경 설정
```bash
git clone https://github.com/cjw1724/SEO-AD.git
cd SEO-AD

# 가상환경 생성 및 의존성 설치
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

### 2. 환경 변수 구성
`.env.example`을 복사하여 `SEO.env`를 생성하고 본인의 API 키를 입력합니다:
```bash
cp .env.example SEO.env
```
- Google Blogger API용 `credentials.json`을 프로젝트 루트에 배치합니다.

### 3. 실행 방법
- **대화형 제어 센터 (원클릭)**:
  `start.bat` 더블 클릭
- **대시보드 헬스체크**:
  ```powershell
  python engine/company_runtime.py --dashboard
  ```
- **1회 즉시 발행**:
  ```powershell
  python engine/company_runtime.py --once
  ```
- **365일 무인 스케줄러 등록**:
  `setup_scheduler.bat` 우클릭 후 관리자 권한으로 실행

---

## 🔒 보안 및 라이선스 (Security Note)
본 저장소에는 일체의 개인정보, OAuth 토큰(`token.json`), 클라이언트 비밀키(`credentials.json`), API 환경변수(`*.env`)가 포함되지 않으며 `.gitignore`를 통해 엄격하게 차단됩니다.
