@echo off
setlocal
cd /d "%~dp0"

if not exist "%~dp0venv\Scripts\python.exe" (
    echo [ERROR] Python virtual environment not found: "%~dp0venv\Scripts\python.exe"
    pause
    exit /b 1
)

"%~dp0venv\Scripts\python.exe" "%~dp0reauth_blogger.py"
pause
