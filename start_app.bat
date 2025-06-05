@echo off
setlocal enabledelayedexpansion

echo Starting Website Uptime Monitor...

:: Change to the script's directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate

:: Check if requirements are installed
echo Checking requirements...
pip freeze > temp_requirements.txt
findstr /i "flask requests python-dotenv" temp_requirements.txt > nul
if errorlevel 1 (
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements
        pause
        exit /b 1
    )
)
del temp_requirements.txt

:: Start the Flask application in a new window
start "Website Uptime Monitor" cmd /c "python app.py"

:: Wait a moment for the server to start
timeout /t 2 /nobreak > nul

:: Open the browser
start http://localhost:5000

echo.
echo Application is running!
echo Press Ctrl+C in the server window to stop the application.
echo.

:: Keep the window open
pause 