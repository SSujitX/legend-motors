@echo off
REM Legend Scrapers Scheduler - Windows Batch File
REM This batch file starts the scheduler for daily execution at 2 PM Bangladesh time

echo ============================================================
echo LEGEND SCRAPERS SCHEDULER
echo ============================================================
echo Starting scheduler for daily execution at 2:00 PM Bangladesh time...
echo Press Ctrl+C to stop the scheduler
echo ============================================================

REM Change to the script directory
cd /d "%~dp0"

REM Run the scheduler using uv (preferred) or fallback to python
where uv >nul 2>nul
if %errorlevel% == 0 (
    echo Using UV package manager...
    uv run scheduler.py
) else (
    echo UV not found, using Python directly...
    python scheduler.py
)

echo.
echo Scheduler stopped.
pause