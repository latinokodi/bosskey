@echo off
echo ============================================
echo  BossKey - Environment Setup
echo ============================================
echo.

:: Create virtual environment
echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create venv. Is Python installed?
    pause
    exit /b 1
)

:: Activate and install dependencies
echo [2/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo [3/3] Done!
echo.
echo ============================================
echo  Setup complete! Run: run.bat
echo ============================================
pause
