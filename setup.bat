@echo off

rem Check if Python 3.11 is installed
python --version | findstr /C:"Python 3.11" >nul
if %errorlevel% equ 0 (
    echo Python 3.11 is installed.
    
    rem Create virtual environment
    python -m venv .venv
    
    rem Activate virtual environment
    call .venv\Scripts\activate
    
    rem Install requirements
    pip install -r requirements.txt
) else (
    echo Python 3.11 is not installed.
)