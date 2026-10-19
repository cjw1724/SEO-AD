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

if (-not (Test-Path $PythonExe)) {
    Write-Host "[ERROR] Python 가상환경이 발견되지 않았습니다: $PythonExe" -ForegroundColor Red
    Read-Host "엔터 키를 누르면 종료합니다..."
    exit 1
}

# Display Executive Dashboard
& $PythonExe $RuntimeScript --dashboard

Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
Write-Host " [실행 옵션 선택]" -ForegroundColor Yellow
Write-Host "  1. 1회 즉시 완전 자율 실행 (PRODUCTION 실제 발행)"
Write-Host "  2. 안전 테스트 모드 (DRY-RUN 모의 발행)"
Write-Host "  3. 24/7 상시 백그라운드 무인 데몬 가동 (09:00, 15:00, 21:00)"
Write-Host "  4. 8인 AI 직원 헬스체크 전수 검사"
Write-Host "  5. 윈도우 작업 스케줄러 365일 무인 등록"
Write-Host "  6. 윈도우 작업 스케줄러 등록 해제"
Write-Host "  7. 종료"
Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan

$choice = Read-Host "실행할 번호를 선택하십시오 (1-7) [기본: 1]"
if ([string]::IsNullOrWhiteSpace($choice)) { 
    $choice = "1" 
} else {
    $choice = $choice.Trim()
}

switch ($choice) {
    "1" {
        Write-Host "`n[INFO] 1회 완전 자율 사이클을 실제 발행 모드로 가동합니다..." -ForegroundColor Green
        & $PythonExe $RuntimeScript --once
    }
    "2" {
        Write-Host "`n[INFO] 안전 테스트(DRY-RUN) 모드로 가동합니다..." -ForegroundColor Green
        & $PythonExe $RuntimeScript --once --dry-run
    }
    "3" {
        Write-Host "`n[INFO] 24/7 상시 무인 데몬을 백그라운드로 가동합니다..." -ForegroundColor Green
        & $PythonExe $RuntimeScript --daemon
    }
    "4" {
        Write-Host "`n[INFO] 8인 AI 직원 헬스체크를 수행합니다..." -ForegroundColor Green
        & $PythonExe $RuntimeScript --health
    }
    "5" {
        Write-Host "`n[INFO] 윈도우 작업 스케줄러 등록을 수행합니다..." -ForegroundColor Green
        & (Join-Path $ProjectDir "setup_scheduler.ps1")
    }
    "6" {
        Write-Host "`n[INFO] 윈도우 작업 스케줄러 등록을 해제합니다..." -ForegroundColor Yellow
        & (Join-Path $ProjectDir "unregister_scheduler.ps1")
    }
    "7" {
        Write-Host "`n[INFO] 제어 센터를 종료합니다." -ForegroundColor Gray
        exit 0
    }
    Default {
        Write-Host "`n[INFO] 기본 모드(1회 즉시 실행)로 가동합니다..." -ForegroundColor Green
        & $PythonExe $RuntimeScript --once
    }
}

Write-Host "`n작업이 완료되었습니다." -ForegroundColor Green
if ([Environment]::UserInteractive -and -not [Console]::IsInputRedirected) {
    Read-Host "계속하려면 엔터 키를 누르십시오..."
}
