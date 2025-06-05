@echo off
echo Stopping Website Uptime Monitor...

:: Find and kill the Flask process
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do (
    taskkill /F /PID %%a
    if not errorlevel 1 (
        echo Application stopped successfully.
    ) else (
        echo No application found running on port 5000.
    )
)

:: Wait a moment
timeout /t 2 /nobreak > nul

echo Done!
pause 