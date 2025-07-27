@echo off
REM Legend Scrapers Scheduler - Windows Batch File
REM This batch file starts the scheduler for daily execution at 2 PM Bangladesh time

REM Set UTF-8 encoding for better Unicode support
chcp 65001 >nul 2>&1

echo ============================================================
echo LEGEND SCRAPERS SCHEDULER
echo ============================================================
echo Starting scheduler for daily execution at 2:00 PM Bangladesh time...
echo Press Ctrl+C to stop the scheduler
echo ============================================================

REM Change to the script directory
cd /d "%~dp0"

REM Try to run the Unicode version first, fallback to ASCII version if it fails
where uv >nul 2>nul
if %errorlevel% == 0 (
    echo Using UV package manager...
    echo Trying Unicode version first...
    uv run scheduler.py
    if %errorlevel% neq 0 (
        echo Unicode version failed, trying ASCII-safe version...
        uv run scheduler_ascii.py
    )
) else (
    echo UV not found, using Python directly...
    echo Trying Unicode version first...
    python scheduler.py
    if %errorlevel% neq 0 (
        echo Unicode version failed, trying ASCII-safe version...
        python scheduler_ascii.py
    )
)

echo.
echo Scheduler stopped.
pause