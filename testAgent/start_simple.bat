@echo off
echo ========================================
echo OpenCSG AgenticHub Test Agent
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
python -c "import playwright" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    python -m playwright install chromium
)

REM Start program
echo.
echo Starting test agent...
echo.

REM Go to parent directory (project root)
cd /d "%~dp0.."
python testAgent\main.py

pause
