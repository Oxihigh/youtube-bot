@echo off
echo ======================================================
echo  AutoShorts AI - Automated System Setup
echo ======================================================
echo.

:: 1. Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 2. Create virtual environment if not exists
if not exist "venv" (
    echo [*] Creating Python virtual environment (venv)...
    python -m venv venv
) else (
    echo [OK] Virtual environment already exists.
)

:: 3. Upgrade pip and install requirements
echo [*] Installing dependencies into virtual environment...
call .\venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. Create .env if not exists
if not exist ".env" (
    echo [*] Creating .env file from template...
    copy .env.example .env
    echo [NOTICE] Please edit .env to add your GEMINI_API_KEY if desired.
) else (
    echo [OK] .env configuration file found.
)

:: 5. Create necessary directories
if not exist "output" mkdir output
if not exist "temp" mkdir temp
if not exist "assets\music" mkdir assets\music
if not exist "assets\fonts" mkdir assets\fonts

echo.
echo ======================================================
echo  Setup Complete! You are ready to run AutoShorts AI.
echo ======================================================
echo.
echo To launch the Web Dashboard:
echo   Double-click start.bat   (or run: .\venv\Scripts\python main.py)
echo.
pause
