@echo off
REM ==============================================================================
REM run_project.bat - Windows Interactive Runner for Netflix Big Data Micro-Project
REM ==============================================================================
title Netflix Big Data Project (Hadoop & Hive)
cls

echo ===================================================================
echo     Netflix Movies and TV Shows Data Analysis (Hadoop and Hive)
echo ===================================================================
echo.
echo Select Execution Option:
echo   [1] Launch Interactive Web Dashboard (Local Demo + Hadoop Cluster)
echo   [2] Run Complete Automated CLI Pipeline (HDFS + HiveQL + Charts)
echo   [3] Run Hadoop MapReduce Stream Simulation (mapper.py + reducer.py)
echo   [4] Check Hadoop Cluster Diagnostics
echo   [5] Exit
echo.

set /p choice="Enter choice [1-5] (Default: 1): "

if "%choice%"=="" set choice=1
if "%choice%"=="1" goto launch_web
if "%choice%"=="2" goto run_cli
if "%choice%"=="3" goto run_mr
if "%choice%"=="4" goto run_diag
if "%choice%"=="5" goto end

:launch_web
echo.
echo [*] Starting Web Dashboard on http://localhost:5000 ...
IF EXIST ".venv\Scripts\python.exe" (
    start http://localhost:5000
    ".venv\Scripts\python.exe" app.py
) ELSE (
    start http://localhost:5000
    python app.py
)
goto end

:run_cli
echo.
echo [*] Running automated pipeline...
IF EXIST ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_project.py
) ELSE (
    python run_project.py
)
goto end

:run_mr
echo.
echo [*] Running MapReduce simulation...
IF EXIST ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" hadoop/run_local_mapreduce.py
) ELSE (
    python hadoop/run_local_mapreduce.py
)
goto end

:run_diag
echo.
echo [*] Checking cluster diagnostics...
IF EXIST ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_project.py --cluster
) ELSE (
    python run_project.py --cluster
)
goto end

:end
echo.
pause
