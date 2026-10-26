# ==============================================================================
# Blogin 365 AI Holdings - Windows Task Scheduler 24/7 Autonomous Setup (v9.0 Apex)
# 완전히 사람의 개입 없이 매일 정해진 시각(09:00, 15:00, 21:00 KST)에 
# 고수익 핀테크 Micro-SaaS 유틸리티 및 분석글을 자동 발행하는 윈도우 스케줄러 등록 스크립트
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$TaskName = "Blogin365_Autonomous_Publisher"
$WorkingDir = "d:\SEO AD"
$PythonExe = "d:\SEO AD\venv\Scripts\python.exe"
$ScriptPath = "d:\SEO AD\engine\company_runtime.py"
$Arguments = "`"d:\SEO AD\engine\company_runtime.py`" --once"

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  🏢 BLOGIN 365 AI HOLDINGS - WINDOWS TASK SCHEDULER 24/7 SETUP" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan

# 1. Check Python executable & script existence
if (-Not (Test-Path $PythonExe)) {
    Write-Error "Python 실행 파일을 찾을 수 없습니다: $PythonExe"
    exit 1
}

if (-Not (Test-Path $ScriptPath)) {
    Write-Error "런타임 스크립트를 찾을 수 없습니다: $ScriptPath"
    exit 1
}

# 2. Check if Task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "[INFO] 기존 스케줄러 태스크 [$TaskName] 감지됨. 최신 설정으로 갱신합니다..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# 3. Create Daily Triggers (09:00, 15:00, 21:00 KST)
$TriggerMorning = New-ScheduledTaskTrigger -Daily -At "09:00"
$TriggerAfternoon = New-ScheduledTaskTrigger -Daily -At "15:00"
$TriggerNight = New-ScheduledTaskTrigger -Daily -At "21:00"

# 4. Create Scheduled Task Action
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $Arguments -WorkingDirectory $WorkingDir

# 5. Create Settings (Execution limit 2 hours, wake to run if sleeping, restart on fail)
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# 6. Register Task under current user
try {
    $RegisteredTask = Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger @($TriggerMorning, $TriggerAfternoon, $TriggerNight) `
        -Settings $Settings `
        -Description "Blogin 365 AI Holdings - 24/7 무인 자율 미디어 발행 엔진 (매일 09:00, 15:00, 21:00)"

    Write-Host "`n✅ [SUCCESS] 윈도우 스케줄러 태스크가 성공적으로 등록되었습니다!" -ForegroundColor Green
    Write-Host "• 태스크 이름 : $TaskName"
    Write-Host "• 실행 파일   : $PythonExe"
    Write-Host "• 인자값     : $Arguments"
    Write-Host "• 실행 시각   : 매일 09:00, 15:00, 21:00 KST (1일 3회 완전 자율 가동)"
    Write-Host "• 상태       : Ready"
} catch {
    Write-Error "스케줄러 등록 중 오류 발생: $_"
    exit 1
}

Write-Host "`n[명령어 안내]" -ForegroundColor Cyan
Write-Host "  - 태스크 즉시 1회 시험 실행 : Start-ScheduledTask -TaskName `"$TaskName`""
Write-Host "  - 태스크 상태 확인          : Get-ScheduledTask -TaskName `"$TaskName`""
Write-Host "  - 태스크 삭제               : Unregister-ScheduledTask -TaskName `"$TaskName`" -Confirm:`$false"
Write-Host "==============================================================================`n" -ForegroundColor Cyan
