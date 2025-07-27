# Legend Scrapers Scheduler - PowerShell Script
# This script starts the scheduler for daily execution at 2 PM Bangladesh time

param(
    [switch]$Once,
    [switch]$Help
)

# Set console title
$Host.UI.RawUI.WindowTitle = "Legend Scrapers Scheduler"

# Display banner
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🏆 LEGEND SCRAPERS SCHEDULER" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📅 Scheduled execution: Daily at 2:00 PM Bangladesh time (UTC+6)" -ForegroundColor Green
Write-Host "🎯 Target platforms: Kavak, AutoMall, Cars24, Dubizzle" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan

# Change to script directory
Set-Location $PSScriptRoot

# Check if help is requested
if ($Help) {
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\start_scheduler.ps1          # Start the scheduler" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -Once    # Run scrapers immediately" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -Help    # Show this help" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\start_scheduler.ps1           # Normal scheduled mode" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -Once     # Test run" -ForegroundColor White
    exit 0
}

try {
    # Check if UV is available
    $uvAvailable = Get-Command uv -ErrorAction SilentlyContinue
    
    if ($uvAvailable) {
        Write-Host "✅ Using UV package manager..." -ForegroundColor Green
        
        if ($Once) {
            Write-Host "🔧 Running scrapers immediately..." -ForegroundColor Yellow
            uv run scheduler.py --once
        } else {
            Write-Host "⏰ Starting scheduler..." -ForegroundColor Green
            Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
            uv run scheduler.py
        }
    } else {
        Write-Host "⚠️  UV not found, using Python directly..." -ForegroundColor Yellow
        
        if ($Once) {
            Write-Host "🔧 Running scrapers immediately..." -ForegroundColor Yellow
            python scheduler.py --once
        } else {
            Write-Host "⏰ Starting scheduler..." -ForegroundColor Green
            Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
            python scheduler.py
        }
    }
} catch {
    Write-Host "❌ Error occurred: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Python and required dependencies are installed." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Scheduler stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"