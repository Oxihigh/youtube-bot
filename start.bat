@echo off
echo ======================================================
echo  Launching AutoShorts AI Web Studio Dashboard
echo  URL: http://127.0.0.1:8000
echo ======================================================
echo.

if not exist "venv" (
    echo [ERROR] Virtual environment not found. Please run setup.bat first!
    pause
    exit /b 1
)

.\venv\Scripts\python main.py
pause
