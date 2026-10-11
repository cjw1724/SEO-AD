@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0unregister_scheduler.ps1"
if errorlevel 1 (
    schtasks /Delete /F /TN "Blogin365AI_AutonomousCompany"
)
pause
