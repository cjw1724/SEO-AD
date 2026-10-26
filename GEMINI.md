# SEO AD Workspace Rules (GEMINI.md)
# Antigravity 2.0 + Gemini Flash (High Reasoning) 전용 자율 완주 규칙

## 1. Flash 모델 3대 약점 방어 헌법
- **코드 생략 금지 (No Lazy Coding)**: `// ... rest of code`, `# 기존 코드 동일`, `// TODO`, 가짜 목업 배열 영구 금지.
- **선 사고 후 코딩 (Sequential Thinking First)**: 코딩 전 `sequentialthinking` 도구로 사고 분기 및 엣지 케이스 분석 후 `TASKS.md` 수립.
- **기계적 검증 전 완료 선언 금지 (Strict Exit Gate)**: 테스트(Exit Code 0) 및 Playwright E2E 검증 통과 전까지 완료라 하지 않고 자가치유 루프 지속.

## 2. 작업 표준 프로토콜
1. 작업 착수 시 `TASKS.md` 체크리스트를 생성하고 진행 상황을 `[ ]` -> `[x]`로 실시간 갱신한다.
2. 단위별 원자적 구현(One task at a time) 후 터미널 테스트(`python -m unittest`)를 실행한다.
3. 무결점이 확인된 시점에만 사용자에게 완료를 보고한다.
