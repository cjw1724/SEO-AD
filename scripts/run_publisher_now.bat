@echo off
chcp 65001 >nul
echo [Blogin 365 AI Holdings] 1회 완전 자율 사이클 즉시 실행 중...
cd /d "d:\SEO AD"
"d:\SEO AD\venv\Scripts\python.exe" "d:\SEO AD\engine\company_runtime.py" --once
pause
