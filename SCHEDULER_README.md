# 📅 Legend Scrapers Scheduler

A comprehensive scheduling system for the Legend Scrapers project that automatically runs all scrapers daily at **2:00 PM Bangladesh/Dhaka time (UTC+6)**.

## 🌟 Features

- ⏰ **Automatic Daily Execution** - Runs every day at 2:00 PM Bangladesh time
- 🕐 **Timezone Aware** - Properly handles Bangladesh/Dhaka timezone (UTC+6)
- 📝 **Comprehensive Logging** - Logs to both file and console
- 🔄 **Error Recovery** - Handles errors gracefully and continues operation
- 🚀 **Concurrent Processing** - Runs all scrapers simultaneously for maximum efficiency
- ⏹️ **Graceful Shutdown** - Clean exit with Ctrl+C
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 🎯 **Multiple Execution Modes** - Scheduled or immediate execution

## 📋 Prerequisites

- **Python 3.13+**
- **UV Package Manager** (recommended) or pip
- **Required Dependencies:**
  - `schedule>=1.2.0`
  - `pytz>=2023.3`
  - All Legend Scrapers dependencies

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Start the Scheduler

```powershell
# Method 1: Direct Python execution
python scheduler.py

# Method 2: Using UV
uv run scheduler.py

# Method 3: Windows Batch File
start_scheduler.bat

# Method 4: PowerShell Script
.\start_scheduler.ps1
```

### 3. Test Run (Immediate Execution)

```powershell
# Run scrapers immediately for testing
python scheduler.py --once

# Using UV
uv run scheduler.py --once

# Using PowerShell script
.\start_scheduler.ps1 -Once
```

## 📁 File Structure

```
Legend Scrapers/
├── scheduler.py              # Main scheduler script
├── start_scheduler.bat       # Windows batch file
├── start_scheduler.ps1       # PowerShell script
├── scraper_scheduler.log     # Log file (auto-created)
├── app.py                    # Original scrapers
└── requirements.txt          # Updated with scheduler deps
```

## ⚙️ Configuration

### Schedule Settings

- **Execution Time:** 2:00 PM Bangladesh time (UTC+6)
- **Frequency:** Daily
- **Timezone:** Asia/Dhaka (UTC+6)

### Logging Configuration

- **Log File:** `scraper_scheduler.log`
- **Log Level:** INFO
- **Format:** Timestamp - Level - Message
- **Output:** Both file and console

## 🎮 Usage Options

### Command Line Arguments

```bash
# Start scheduler (default)
python scheduler.py

# Run immediately
python scheduler.py --once

# Show detailed help
python scheduler.py --help-detailed
```

### Windows Scripts

```powershell
# Batch file execution
start_scheduler.bat

# PowerShell execution
.\start_scheduler.ps1          # Start scheduler
.\start_scheduler.ps1 -Once    # Run immediately
.\start_scheduler.ps1 -Help    # Show help
```

## 📊 Execution Flow

1. **Scheduler Startup**
   - Initialize logging system
   - Set Bangladesh timezone
   - Display startup banner
   - Schedule daily job at 2:00 PM

2. **Daily Execution**
   - Log execution start time
   - Run all scrapers concurrently:
     - Kavak Scraper
     - AutoMall Scraper
     - Cars24 Scraper
     - Dubizzle Scraper
   - Log completion status and duration

3. **Error Handling**
   - Catch and log any errors
   - Continue scheduler operation
   - Provide detailed error information

## 📈 Performance Metrics

- **Concurrent Execution:** All 4 scrapers run simultaneously
- **Check Interval:** Every 60 seconds
- **Startup Time:** < 5 seconds
- **Memory Usage:** Optimized for long-running operation
- **Log Rotation:** Automatic (handled by logging system)

## 🔧 Development

### Adding New Scrapers

1. Add scraper function to `app.py`
2. Import in `scheduler.py`
3. Add to `scrapers` list in `run_all_scrapers()`

### Customizing Schedule

```python
# Change execution time (24-hour format)
schedule.every().day.at("14:00").do(scheduled_job)  # 2:00 PM
schedule.every().day.at("09:30").do(scheduled_job)  # 9:30 AM

# Change frequency
schedule.every().monday.at("14:00").do(scheduled_job)     # Weekly
schedule.every(2).days.at("14:00").do(scheduled_job)      # Every 2 days
```

### Custom Timezone

```python
# Change timezone
CUSTOM_TZ = pytz.timezone('America/New_York')  # EST/EDT
CUSTOM_TZ = pytz.timezone('Europe/London')     # GMT/BST
CUSTOM_TZ = pytz.timezone('Asia/Tokyo')        # JST
```

## 📝 Logging Details

### Log File Location
- **File:** `scraper_scheduler.log`
- **Location:** Same directory as scheduler.py
- **Format:** `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

### Log Levels
- **INFO:** Normal operation, start/stop events
- **ERROR:** Errors and exceptions
- **WARNING:** Non-critical issues

### Sample Log Output
```
2024-01-15 14:00:00,123 - INFO - 📅 Scheduled scraping job started
2024-01-15 14:00:01,456 - INFO - 🚀 Starting Legend Scrapers at 2024-01-15 14:00:01 +06
2024-01-15 14:05:30,789 - INFO - ✅ All scrapers completed successfully in 0:05:29.333000
2024-01-15 14:05:30,790 - INFO - 📅 Scheduled scraping job completed successfully
```

## 🛠️ Troubleshooting

### Common Issues

**1. Scheduler Not Starting**
```bash
# Check Python installation
python --version

# Check dependencies
pip list | grep schedule
pip list | grep pytz
```

**2. Import Errors**
```bash
# Install missing dependencies
uv sync
# or
pip install schedule pytz
```

**3. Timezone Issues**
```bash
# Verify timezone
python -c "import pytz; print(pytz.timezone('Asia/Dhaka'))"
```

**4. Permission Issues (Windows)**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Debug Mode

Enable detailed logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security & Privacy

- **No Sensitive Data Logging:** Credentials and API keys are not logged
- **Local Execution:** All processing happens locally
- **File Permissions:** Log files use default system permissions
- **Network Security:** Inherits security from individual scrapers

## 📊 Monitoring

### Health Checks

Monitor scheduler health by checking:
- Log file updates
- Process status
- Memory usage
- Network connectivity

### Performance Monitoring

```bash
# Check if scheduler is running
tasklist | findstr python

# Monitor log file
Get-Content scraper_scheduler.log -Tail 10 -Wait
```

## 🚨 Important Notes

- **System Time:** Ensure system clock is accurate for proper scheduling
- **Dependencies:** Keep `schedule` and `pytz` libraries updated
- **Long Running:** Designed for 24/7 operation
- **Resource Usage:** Monitor system resources during execution
- **Backup:** Regularly backup log files and configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This scheduler is part of the Legend Scrapers project and follows the same licensing terms.

---

**🎯 Ready to automate your scraping workflow? Start the scheduler and let it handle the daily execution!**