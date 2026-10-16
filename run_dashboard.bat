@echo off
REM ==============================================================================
REM run_dashboard.bat - Windows 1-Click Runner for Netflix Big Data Web Dashboard
REM ==============================================================================
title Netflix Big Data Dashboard (Local Demo & Hadoop Cluster)
cls

echo ===================================================================
echo   Netflix Big Data Platform: Local Demo & Hadoop Cluster Engine
echo ===================================================================
echo.
echo [*] Starting Web Dashboard on http://localhost:5000 ...
echo [*] Supports Local Demo Mode and Hadoop Cluster Mode
echo.

IF EXIST ".venv\Scripts\python.exe" (
    start http://localhost:5000
    ".venv\Scripts\python.exe" app.py
) ELSE (
    start http://localhost:5000
    python app.py
)

pause
