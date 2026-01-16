@echo off
REM Truckit Test Dashboard Launcher
REM This batch file starts the test results dashboard

echo ========================================
echo   🚀 Truckit Test Dashboard
echo ========================================
echo.

cd /d "%~dp0"

echo 📦 Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo 🔧 Installing/Checking dependencies...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies ready
echo.

echo 🎯 Starting dashboard...
echo 📊 Dashboard will be available at: http://localhost:5000
echo 🔄 Press Ctrl+C in the terminal to stop
echo.

python run_dashboard.py

echo.
echo 👋 Dashboard stopped
pause