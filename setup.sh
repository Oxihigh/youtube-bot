#!/usr/bin/env bash
set -e

echo "======================================================"
echo " AutoShorts AI - Automated System Setup (Linux / Mac)"
echo "======================================================"
echo ""

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found. Please install Python 3.10+."
    exit 1
fi

# 2. Virtual Environment
if [ ! -d "venv" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[OK] Virtual environment exists."
fi

# 3. Install requirements
echo "[*] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create .env
if [ ! -f ".env" ]; then
    echo "[*] Creating .env from template..."
    cp .env.example .env
fi

# 5. Create directories
mkdir -p output temp assets/music assets/fonts

echo ""
echo "======================================================"
echo " Setup Complete! Run ./start.sh to launch dashboard."
echo "======================================================"
