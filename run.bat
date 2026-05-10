@echo off
setlocal

:: ── BossKey Launcher ─────────────────────────────────────────────────────────
:: Creates/updates the venv automatically, then starts the app (no console).

set VENV=venv
set PY=python

:: 1. Create venv if it does not exist
if not exist "%VENV%\Scripts\activate.bat" (
    echo [BossKey] Creating virtual environment...
    %PY% -m venv %VENV%
    if errorlevel 1 (
        echo ERROR: Python not found or venv creation failed.
        pause
        exit /b 1
    )
)

:: 2. Activate
call %VENV%\Scripts\activate.bat

:: 3. Upgrade pip silently
python -m pip install --upgrade pip -q

:: 4. Install / update dependencies silently
pip install -r requirements.txt -q
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

:: 5. Launch without a console window
start "" pythonw bosskey.py

