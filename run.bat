@echo off
title MatchPortal - Job and Internship Portal with Recommendation Engine
echo ====================================================================
echo    MatchPortal: Job and Internship Portal with AI Recommendation
echo ====================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PY_CMD=python
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set PY_CMD=py
    ) else (
        echo [ERROR] Python is not found in your system PATH.
        echo Please install Python 3.8+ from https://www.python.org/
        pause
        exit /b 1
    )
)

echo [1/3] Using Python: %PY_CMD%
%PY_CMD% --version
echo.

echo [2/3] Checking and installing dependencies...
%PY_CMD% -m pip install -r requirements.txt
echo.

echo [3/3] Launching Web Portal at http://127.0.0.1:5000 ...
start "" http://127.0.0.1:5000

%PY_CMD% app.py

pause
