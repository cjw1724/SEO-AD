# ==============================================================================
# Blogin 365 AI Holdings - Windows Task Scheduler Unregistration Script
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$TaskName = "Blogin365AI_AutonomousCompany"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " 🏢 Blogin 365 AI Holdings - 작업 스케줄러 등록 해제" -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "✅ [$TaskName] 작업이 성공적으로 스케줄러에서 제거되었습니다." -ForegroundColor Green
} else {
    Write-Host "ℹ️ [$TaskName] 작업이 등록되어 있지 않습니다." -ForegroundColor Gray
}
Write-Host "=================================================================`n" -ForegroundColor Cyan
