#!/usr/bin/env python3
"""
Legend Scrapers Scheduler (ASCII-Safe Version)
==============================================

This is an ASCII-safe version of the scheduler that avoids Unicode characters
for environments that have encoding issues.

Usage:
    python scheduler_ascii.py          - Start the scheduler
    python scheduler_ascii.py --once   - Run scrapers immediately
    python scheduler_ascii.py --help   - Show help message
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

# Import the scraper functions from app.py
from app import run_kavak, run_automall, run_cars24, run_dubizzle, process_wrapper

# Configure logging (ASCII-safe)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Bangladesh timezone (UTC+6)
BANGLADESH_TZ = pytz.timezone('Asia/Dhaka')


def get_bangladesh_time():
    """Get current time in Bangladesh timezone."""
    return datetime.now(BANGLADESH_TZ)


def run_all_scrapers():
    """Run all scrapers concurrently with error handling and logging."""
    start_time = get_bangladesh_time()
    logger.info(f"[START] Starting Legend Scrapers at {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    scrapers = [run_kavak, run_automall, run_cars24, run_dubizzle]
    
    try:
        with mp.Pool(processes=len(scrapers)) as pool:
            pool.map(process_wrapper, scrapers)
        
        end_time = get_bangladesh_time()
        duration = end_time - start_time
        logger.info(f"[SUCCESS] All scrapers completed successfully in {duration}")
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] Error during scraping: {str(e)}")
        return False


def scheduled_job():
    """Wrapper function for scheduled execution."""
    try:
        logger.info("[SCHEDULE] Scheduled scraping job started")
        success = run_all_scrapers()
        if success:
            logger.info("[SCHEDULE] Scheduled scraping job completed successfully")
        else:
            logger.error("[SCHEDULE] Scheduled scraping job completed with errors")
    except Exception as e:
        logger.error(f"[SCHEDULE] Scheduled job failed: {str(e)}")


def run_scheduler():
    """Run the scheduler that executes scrapers daily at 2 PM Bangladesh time."""
    # Clear any existing scheduled jobs
    schedule.clear()
    
    # Schedule the job for 2:00 PM Bangladesh time (UTC+6)
    schedule.every().day.at("14:00").do(scheduled_job)
    
    current_time = get_bangladesh_time()
    next_run = schedule.next_run()
    
    logger.info("[SCHEDULER] Legend Scrapers Scheduler Started")
    logger.info(f"[TIME] Current Bangladesh time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info("[SCHEDULE] Daily at 2:00 PM Bangladesh time (UTC+6)")
    
    if next_run:
        # Convert UTC time to Bangladesh time for display
        next_run_bd = next_run.replace(tzinfo=pytz.UTC).astimezone(BANGLADESH_TZ)
        logger.info(f"[NEXT] Next scheduled run: {next_run_bd.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    logger.info("[RUNNING] Scheduler is running... Press Ctrl+C to stop")
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("[STOP] Scheduler stopped by user")
    except Exception as e:
        logger.error(f"[ERROR] Scheduler error: {str(e)}")
        logger.info("[RESTART] Restarting scheduler in 60 seconds...")
        time.sleep(60)
        run_scheduler()  # Restart scheduler


def run_once():
    """Run scrapers immediately (for testing or manual execution)."""
    logger.info("[MANUAL] Running scrapers immediately (manual execution)")
    success = run_all_scrapers()
    if success:
        logger.info("[SUCCESS] Manual execution completed successfully")
    else:
        logger.error("[ERROR] Manual execution completed with errors")
    return success


def show_help():
    """Display help information."""
    help_text = """
Legend Scrapers Scheduler (ASCII-Safe Version) - Help

DESCRIPTION:
    This scheduler runs the Legend Scrapers automatically every day at 2:00 PM 
    Bangladesh/Dhaka time (UTC+6). This is the ASCII-safe version that avoids
    Unicode characters for better compatibility.

USAGE:
    python scheduler_ascii.py [OPTIONS]
    uv run scheduler_ascii.py [OPTIONS]

OPTIONS:
    (no arguments)    Start the scheduler (default behavior)
    --once           Run all scrapers immediately
    --help           Show this help message

EXAMPLES:
    python scheduler_ascii.py          # Start the scheduler
    python scheduler_ascii.py --once   # Run scrapers now
    uv run scheduler_ascii.py          # Start with uv
    uv run scheduler_ascii.py --once   # Run once with uv

FEATURES:
    * Automatic daily execution at 2:00 PM Bangladesh time
    * Comprehensive logging to file and console
    * Error handling and recovery
    * Concurrent execution of all scrapers
    * Graceful shutdown with Ctrl+C
    * ASCII-safe output for compatibility

LOG FILE:
    scraper_scheduler.log - Contains all execution logs

TIMEZONE:
    All times are in Bangladesh/Dhaka timezone (UTC+6)
    """
    print(help_text)


def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Legend Scrapers Scheduler (ASCII-Safe) - Runs scrapers daily at 2 PM Bangladesh time",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--once', 
        action='store_true', 
        help='Run scrapers immediately instead of scheduling'
    )
    
    parser.add_argument(
        '--help-detailed', 
        action='store_true', 
        help='Show detailed help information'
    )
    
    args = parser.parse_args()
    
    if args.help_detailed:
        show_help()
        return
    
    # Display startup banner (ASCII-safe)
    print("=" * 60)
    print("LEGEND SCRAPERS SCHEDULER (ASCII-SAFE)")
    print("=" * 60)
    print(f"Current Bangladesh time: {get_bangladesh_time().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("Target platforms: Kavak, AutoMall, Cars24, Dubizzle")
    print("=" * 60)
    
    if args.once:
        # Run scrapers immediately
        print("Manual execution mode")
        success = run_once()
        sys.exit(0 if success else 1)
    else:
        # Start the scheduler
        print("Scheduler mode - Daily execution at 2:00 PM Bangladesh time")
        run_scheduler()


if __name__ == "__main__":
    main()