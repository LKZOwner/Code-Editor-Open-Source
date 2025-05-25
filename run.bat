@echo off
echo Building and running Code Editor...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Run the editor
python src/main.py

pause 