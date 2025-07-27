# Legend Scrapers Scheduler - PowerShell Script
# This script starts the scheduler for daily execution at 2 PM Bangladesh time

param(
    [switch]$Once,
    [switch]$Help,
    [switch]$AsciiSafe
)

# Set console encoding to UTF-8 for better Unicode support
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
} catch {
    Write-Warning "Could not set UTF-8 encoding, using ASCII-safe mode"
    $AsciiSafe = $true
}

# Set console title
$Host.UI.RawUI.WindowTitle = "Legend Scrapers Scheduler"

# Display banner
if ($AsciiSafe) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "LEGEND SCRAPERS SCHEDULER (ASCII-SAFE)" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Cyan
} else {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "🏆 LEGEND SCRAPERS SCHEDULER" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Cyan
}

if ($AsciiSafe) {
    Write-Host "Scheduled execution: Daily at 2:00 PM Bangladesh time (UTC+6)" -ForegroundColor Green
    Write-Host "Target platforms: Kavak, AutoMall, Cars24, Dubizzle" -ForegroundColor White
} else {
    Write-Host "📅 Scheduled execution: Daily at 2:00 PM Bangladesh time (UTC+6)" -ForegroundColor Green
    Write-Host "🎯 Target platforms: Kavak, AutoMall, Cars24, Dubizzle" -ForegroundColor White
}
Write-Host "============================================================" -ForegroundColor Cyan

# Change to script directory
Set-Location $PSScriptRoot

# Check if help is requested
if ($Help) {
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\start_scheduler.ps1              # Start the scheduler" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -Once        # Run scrapers immediately" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -AsciiSafe   # Use ASCII-safe version" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -Help        # Show this help" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\start_scheduler.ps1               # Normal scheduled mode" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -Once         # Test run" -ForegroundColor White
    Write-Host "  .\start_scheduler.ps1 -AsciiSafe    # Compatibility mode" -ForegroundColor White
    exit 0
}

try {
    # Check if UV is available
    $uvAvailable = Get-Command uv -ErrorAction SilentlyContinue
    
    # Determine which scheduler to use
    $schedulerScript = if ($AsciiSafe) { "scheduler_ascii.py" } else { "scheduler.py" }
    
    if ($uvAvailable) {
        if ($AsciiSafe) {
            Write-Host "✓ Using UV package manager with ASCII-safe scheduler..." -ForegroundColor Green
        } else {
            Write-Host "✅ Using UV package manager..." -ForegroundColor Green
        }
        
        if ($Once) {
            if ($AsciiSafe) {
                Write-Host "Running scrapers immediately (ASCII-safe mode)..." -ForegroundColor Yellow
            } else {
                Write-Host "🔧 Running scrapers immediately..." -ForegroundColor Yellow
            }
            
            # Try Unicode version first, fallback to ASCII if it fails
            if (-not $AsciiSafe) {
                try {
                    uv run scheduler.py --once
                } catch {
                    Write-Host "Unicode version failed, trying ASCII-safe version..." -ForegroundColor Yellow
                    uv run scheduler_ascii.py --once
                }
            } else {
                uv run scheduler_ascii.py --once
            }
        } else {
            if ($AsciiSafe) {
                Write-Host "Starting scheduler (ASCII-safe mode)..." -ForegroundColor Green
                Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
            } else {
                Write-Host "⏰ Starting scheduler..." -ForegroundColor Green
                Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
            }
            
            # Try Unicode version first, fallback to ASCII if it fails
            if (-not $AsciiSafe) {
                try {
                    uv run scheduler.py
                } catch {
                    Write-Host "Unicode version failed, trying ASCII-safe version..." -ForegroundColor Yellow
                    uv run scheduler_ascii.py
                }
            } else {
                uv run scheduler_ascii.py
            }
        }
    } else {
        Write-Host "⚠️  UV not found, using Python directly..." -ForegroundColor Yellow
        
        if ($Once) {
            if ($AsciiSafe) {
                Write-Host "Running scrapers immediately (ASCII-safe mode)..." -ForegroundColor Yellow
            } else {
                Write-Host "🔧 Running scrapers immediately..." -ForegroundColor Yellow
            }
            
            # Try Unicode version first, fallback to ASCII if it fails
            if (-not $AsciiSafe) {
                try {
                    python scheduler.py --once
                } catch {
                    Write-Host "Unicode version failed, trying ASCII-safe version..." -ForegroundColor Yellow
                    python scheduler_ascii.py --once
                }
            } else {
                python scheduler_ascii.py --once
            }
        } else {
            if ($AsciiSafe) {
                Write-Host "Starting scheduler (ASCII-safe mode)..." -ForegroundColor Green
                Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
            } else {
                Write-Host "⏰ Starting scheduler..." -ForegroundColor Green
                Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
            }
            
            # Try Unicode version first, fallback to ASCII if it fails
            if (-not $AsciiSafe) {
                try {
                    python scheduler.py
                } catch {
                    Write-Host "Unicode version failed, trying ASCII-safe version..." -ForegroundColor Yellow
                    python scheduler_ascii.py
                }
            } else {
                python scheduler_ascii.py
            }
        }
    }
} catch {
    Write-Host "❌ Error occurred: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Python and required dependencies are installed." -ForegroundColor Yellow
    Write-Host "Try using the -AsciiSafe parameter if you have encoding issues." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Scheduler stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"