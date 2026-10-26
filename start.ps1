# ==============================================================================
# Blogin 365 AI Holdings - Autonomous Enterprise Control Center (v6.0)
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUNBUFFERED = "1"

$ProjectDir = $PSScriptRoot
Set-Location $ProjectDir

$PythonExe = Join-Path $ProjectDir "venv\Scripts\python.exe"
$RuntimeScript = Join-Path $ProjectDir "engine\company_runtime.py"
$MicroSaaSScript = Join-Path $ProjectDir "engine\crew\crew.py"

if (-not (Test-Path $PythonExe)) {
    Write-Host "[ERROR] Python 가상환경이 발견되지 않았습니다: $PythonExe" -ForegroundColor Red
    Read-Host "엔터 키를 누르면 종료합니다..."
    exit 1
}

# Display Executive Dashboard
& $PythonExe $RuntimeScript --dashboard

Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
Write-Host " [실행 옵션 선택 - FinTech Micro-SaaS Master Controller]" -ForegroundColor Yellow
Write-Host "  1. 1회 즉시 완전 자율 실행 (FinTech Micro-SaaS LIVE 실제 발행)"
Write-Host "  2. 안전 테스트 모드 (FinTech Micro-SaaS DRY-RUN 모의 발행)"
Write-Host "  3. 20대 핵심 자산 매트릭스 일괄 배포 (Programmatic Matrix Batch)"
Write-Host "  4. 기존 4대 라이브 포스트 덮어쓰기 (In-Place Update & 실시간 환율 결합)"
Write-Host "  5. 3대 뷰포트 & 18개 무인 품질 검증 테스트 (Playwright & Unit Tests)"
Write-Host "  6. Google Blogger OAuth2 인증 갱신 (Browser Re-Auth)"
Write-Host "  7. 24/7 상시 백그라운드 무인 데몬 가동 (09:00, 15:00, 21:00)"
Write-Host "  8. 종료"
Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan

$choice = Read-Host "실행할 번호를 선택하십시오 (1-8) [기본: 1]"
if ([string]::IsNullOrWhiteSpace($choice)) { 
    $choice = "1" 
} else {
    $choice = $choice.Trim()
}

switch ($choice) {
    "1" {
        Write-Host "`n[INFO] FinTech Micro-SaaS 1회 완전 자율 사이클을 LIVE 실제 발행 모드로 가동합니다..." -ForegroundColor Green
        & $PythonExe $MicroSaaSScript --once
    }
    "2" {
        Write-Host "`n[INFO] FinTech Micro-SaaS 안전 테스트(DRY-RUN) 모드로 가동합니다..." -ForegroundColor Green
        & $PythonExe $MicroSaaSScript --dry-run
    }
    "3" {
        Write-Host "`n[INFO] 20대 핵심 자산 프로그래매틱 매트릭스 일괄 배포를 가동합니다..." -ForegroundColor Green
        & $PythonExe $MicroSaaSScript --matrix
    }
    "4" {
        Write-Host "`n[INFO] 기존 4대 라이브 포스트 제자리 덮어쓰기(In-Place Update)를 가동합니다..." -ForegroundColor Green
        & $PythonExe $MicroSaaSScript --update
    }
    "5" {
        Write-Host "`n[INFO] Playwright 3대 뷰포트 및 18개 단위 테스트 무인 전수 검증을 가동합니다..." -ForegroundColor Green
        & $PythonExe -m unittest tests.test_market_oracle tests.test_trading_fintech_pipeline tests.test_microsaas_crew_pipeline tests.test_playwright_3viewports
    }
    "6" {
        Write-Host "`n[INFO] Google Blogger OAuth2 브라우저 재인증을 수행합니다..." -ForegroundColor Yellow
        & $PythonExe -c "from engine.crew.publisher import MicroSaaSBloggerPublisher; MicroSaaSBloggerPublisher().authenticate(force_browser=True)"
    }
    "7" {
        Write-Host "`n[INFO] 24/7 상시 무인 데몬을 백그라운드로 가동합니다..." -ForegroundColor Green
        & $PythonExe $RuntimeScript --daemon
    }
    "8" {
        Write-Host "`n[INFO] 제어 센터를 종료합니다." -ForegroundColor Gray
        exit 0
    }
    Default {
        Write-Host "`n[INFO] 기본 모드 (1회 LIVE 실제 발행)로 가동합니다..." -ForegroundColor Green
        & $PythonExe $MicroSaaSScript --once
    }
}

Write-Host "`n작업이 완료되었습니다." -ForegroundColor Green
if ([Environment]::UserInteractive -and -not [Console]::IsInputRedirected) {
    Read-Host "계속하려면 엔터 키를 누르십시오..."
}
