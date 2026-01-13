@echo off
REM OpenCSG AgenticHub Test Agent Launcher
REM This script can be run from anywhere

REM Get the directory where this batch file is located
set "BATCH_DIR=%~dp0"
set "PROJECT_ROOT=%BATCH_DIR%.."

REM Change to batch file directory first
cd /d "%BATCH_DIR%"

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo.
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
python -c "import playwright" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo.
        pause
        exit /b 1
    )
    echo [INFO] Installing Playwright browser...
    python -m playwright install chromium
)

REM Start the program
echo.
echo Starting test agent...
echo.

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

REM Run the main program
python testAgent\main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Program exited with error
    pause
)
