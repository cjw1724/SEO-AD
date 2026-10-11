@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_scheduler.ps1"
if errorlevel 1 (
    echo [ERROR] Task registration failed.
    pause
    exit /b 1
)
pause
