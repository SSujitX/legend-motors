#!/usr/bin/env python3
"""
Legend Scrapers Scheduler
========================

This script schedules the Legend Scrapers to run automatically every day at 2:00 PM 
Bangladesh/Dhaka time (UTC+6).

Usage:
    python scheduler.py          - Start the scheduler
    python scheduler.py --once   - Run scrapers immediately
    python scheduler.py --help   - Show help message

Requirements:
    - schedule>=1.2.0
    - pytz>=2023.3
"""

import asyncio
import multiprocessing as mp
import schedule
import time
import logging
import argparse
from datetime import datetime
import pytz
import sys
import os

# Configure UTF-8 encoding for Windows console
if sys.platform.startswith("win"):
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Import the scraper functions from app.py
from app import run_kavak, run_automall, run_cars24, run_dubizzle, process_wrapper


# Configure logging with UTF-8 encoding
class UTF8StreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            # Use safe encoding for console output
            if hasattr(self.stream, "buffer"):
                self.stream.buffer.write(msg.encode("utf-8") + b"\n")
                self.stream.buffer.flush()
            else:
                # Fallback: replace problematic characters
                safe_msg = msg.encode("ascii", "replace").decode("ascii")
                self.stream.write(safe_msg + "\n")
                self.stream.flush()
        except Exception:
            self.handleError(record)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper_scheduler.log", encoding="utf-8"),
        UTF8StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Bangladesh timezone (UTC+6)
BANGLADESH_TZ = pytz.timezone("Asia/Dhaka")


# Safe logging functions for Unicode compatibility
def safe_log_info(message):
    """Log info message with Unicode fallback."""
    try:
        logger.info(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        safe_message = message.encode("ascii", "replace").decode("ascii")
        logger.info(safe_message)


def safe_log_error(message):
    """Log error message with Unicode fallback."""
    try:
        logger.error(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        safe_message = message.encode("ascii", "replace").decode("ascii")
        logger.error(safe_message)


def safe_print(message):
    """Print message with Unicode fallback."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        safe_message = message.encode("ascii", "replace").decode("ascii")
        print(safe_message)


def get_bangladesh_time():
    """Get current time in Bangladesh timezone."""
    return datetime.now(BANGLADESH_TZ)


def run_all_scrapers():
    """Run all scrapers concurrently with error handling and logging."""
    start_time = get_bangladesh_time()
    safe_log_info(
        f"🚀 Starting Legend Scrapers at {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )

    scrapers = [run_kavak, run_automall, run_cars24, run_dubizzle]

    try:
        with mp.Pool(processes=len(scrapers)) as pool:
            pool.map(process_wrapper, scrapers)

        end_time = get_bangladesh_time()
        duration = end_time - start_time
        safe_log_info(f"✅ All scrapers completed successfully in {duration}")
        return True

    except Exception as e:
        safe_log_error(f"❌ Error during scraping: {str(e)}")
        return False


def scheduled_job():
    """Wrapper function for scheduled execution."""
    try:
        safe_log_info("📅 Scheduled scraping job started")
        success = run_all_scrapers()
        if success:
            safe_log_info("📅 Scheduled scraping job completed successfully")
        else:
            safe_log_error("📅 Scheduled scraping job completed with errors")
    except Exception as e:
        safe_log_error(f"❌ Scheduled job failed: {str(e)}")


def run_scheduler():
    """Run the scheduler that executes scrapers daily at 2 PM Bangladesh time."""
    # Clear any existing scheduled jobs
    schedule.clear()

    # Schedule the job for 2:00 PM Bangladesh time (UTC+6)
    schedule.every().day.at("14:00").do(scheduled_job)

    current_time = get_bangladesh_time()
    next_run = schedule.next_run()

    safe_log_info("⏰ Legend Scrapers Scheduler Started")
    safe_log_info(
        f"🕐 Current Bangladesh time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    safe_log_info("📋 Schedule: Daily at 2:00 PM Bangladesh time (UTC+6)")

    if next_run:
        # Convert UTC time to Bangladesh time for display
        next_run_bd = next_run.replace(tzinfo=pytz.UTC).astimezone(BANGLADESH_TZ)
        safe_log_info(
            f"⏭️  Next scheduled run: {next_run_bd.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )

    safe_log_info("🔄 Scheduler is running... Press Ctrl+C to stop")

    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        safe_log_info("🛑 Scheduler stopped by user")
    except Exception as e:
        safe_log_error(f"❌ Scheduler error: {str(e)}")
        safe_log_info("🔄 Restarting scheduler in 60 seconds...")
        time.sleep(60)
        run_scheduler()  # Restart scheduler


def run_once():
    """Run scrapers immediately (for testing or manual execution)."""
    safe_log_info("🔧 Running scrapers immediately (manual execution)")
    success = run_all_scrapers()
    if success:
        safe_log_info("✅ Manual execution completed successfully")
    else:
        safe_log_error("❌ Manual execution completed with errors")
    return success


def show_help():
    """Display help information."""
    help_text = """
🔧 Legend Scrapers Scheduler - Help

DESCRIPTION:
    This scheduler runs the Legend Scrapers automatically every day at 2:00 PM 
    Bangladesh/Dhaka time (UTC+6).

USAGE:
    python scheduler.py [OPTIONS]
    uv run scheduler.py [OPTIONS]

OPTIONS:
    (no arguments)    Start the scheduler (default behavior)
    --once           Run all scrapers immediately
    --help           Show this help message

EXAMPLES:
    python scheduler.py          # Start the scheduler
    python scheduler.py --once   # Run scrapers now
    uv run scheduler.py          # Start with uv
    uv run scheduler.py --once   # Run once with uv

FEATURES:
    ⏰ Automatic daily execution at 2:00 PM Bangladesh time
    📝 Comprehensive logging to file and console
    🔄 Error handling and recovery
    🚀 Concurrent execution of all scrapers
    ⏹️  Graceful shutdown with Ctrl+C

LOG FILE:
    scraper_scheduler.log - Contains all execution logs

TIMEZONE:
    All times are in Bangladesh/Dhaka timezone (UTC+6)
    """
    print(help_text)


def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Legend Scrapers Scheduler - Runs scrapers daily at 2 PM Bangladesh time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Run scrapers immediately instead of scheduling",
    )

    parser.add_argument(
        "--help-detailed", action="store_true", help="Show detailed help information"
    )

    args = parser.parse_args()

    if args.help_detailed:
        show_help()
        return

    # Display startup banner
    safe_print("=" * 60)
    safe_print("🏆 LEGEND SCRAPERS SCHEDULER")
    safe_print("=" * 60)
    safe_print(
        f"📅 Current Bangladesh time: {get_bangladesh_time().strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    safe_print("🎯 Target platforms: Kavak, AutoMall, Cars24, Dubizzle")
    safe_print("=" * 60)

    if args.once:
        # Run scrapers immediately
        safe_print("🔧 Manual execution mode")
        success = run_once()
        sys.exit(0 if success else 1)
    else:
        # Start the scheduler
        safe_print("⏰ Scheduler mode - Daily execution at 2:00 PM Bangladesh time")
        run_scheduler()


if __name__ == "__main__":
    main()
