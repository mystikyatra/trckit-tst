#!/usr/bin/env python3
"""
Log Cleanup Utility for Truckit Automation Framework

This script removes log files older than 7 days to prevent disk space issues.
Keeps only the most recent 7 days of log files.

Usage:
    python log_cleanup.py                    # Run cleanup manually
    python log_cleanup.py --dry-run         # Show what would be deleted
    python log_cleanup.py --days 30         # Keep 30 days instead of 7
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
import argparse

# Setup basic logging for the cleanup script itself
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('log_cleanup')

def get_log_directory():
    """Get the absolute path to the logs directory"""
    script_dir = Path(__file__).parent
    logs_dir = script_dir / 'logs'
    return logs_dir

def parse_log_filename(filename):
    """
    Parse log filename to extract date
    Expected formats: automation_test_YYYYMMDD.log or automation_test_YYYYMMDD_HHMMSS.log
    """
    try:
        # Remove 'automation_test_' prefix and '.log' suffix
        date_str = filename.replace('automation_test_', '').replace('.log', '')
        
        # Try new format first (with time)
        try:
            log_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
            return log_date
        except ValueError:
            # Try old format (date only)
            log_date = datetime.strptime(date_str, '%Y%m%d')
            return log_date
    except ValueError as e:
        logger.warning(f"Could not parse date from filename: {filename}. Error: {e}")
        return None

def get_log_files_to_delete(logs_dir, days_to_keep=7, dry_run=False):
    """
    Get list of log files that should be deleted
    Returns: List of (filepath, file_date) tuples for files older than cutoff_date
    """
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    files_to_delete = []

    if not logs_dir.exists():
        logger.warning(f"Logs directory does not exist: {logs_dir}")
        return files_to_delete

    logger.info(f"Scanning logs directory: {logs_dir}")
    logger.info(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Keeping logs from last {days_to_keep} days")

    for log_file in logs_dir.glob('automation_test_*.log'):
        if log_file.is_file():
            file_date = parse_log_filename(log_file.name)
            if file_date:
                if file_date < cutoff_date:
                    files_to_delete.append((log_file, file_date))
                    if dry_run:
                        logger.info(f"WOULD DELETE: {log_file.name} (created: {file_date.strftime('%Y-%m-%d %H:%M:%S')})")
                else:
                    logger.debug(f"KEEPING: {log_file.name} (created: {file_date.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                logger.warning(f"Skipping file with unparseable name: {log_file.name}")

    return files_to_delete

def delete_old_logs(files_to_delete, dry_run=False):
    """Delete the specified log files"""
    if not files_to_delete:
        logger.info("No old log files to delete")
        return 0

    deleted_count = 0
    total_size_freed = 0

    logger.info(f"Found {len(files_to_delete)} log files to delete")

    for log_file, file_date in sorted(files_to_delete, key=lambda x: x[1]):
        try:
            file_size = log_file.stat().st_size
            if dry_run:
                logger.info(f"WOULD DELETE: {log_file.name} ({file_size} bytes)")
            else:
                log_file.unlink()
                logger.info(f"DELETED: {log_file.name} ({file_size} bytes)")
                deleted_count += 1
                total_size_freed += file_size
        except Exception as e:
            logger.error(f"Failed to delete {log_file.name}: {e}")

    if not dry_run and deleted_count > 0:
        logger.info(f"Cleanup completed: {deleted_count} files deleted, {total_size_freed} bytes freed")

    return deleted_count

def get_logs_summary(logs_dir):
    """Get summary of current log files"""
    if not logs_dir.exists():
        return "Logs directory does not exist"

    log_files = list(logs_dir.glob('automation_test_*.log'))
    total_files = len(log_files)
    total_size = sum(f.stat().st_size for f in log_files if f.is_file())

    if log_files:
        # Get date range
        file_dates = []
        for log_file in log_files:
            file_date = parse_log_filename(log_file.name)
            if file_date:
                file_dates.append(file_date)

        if file_dates:
            oldest = min(file_dates)
            newest = max(file_dates)
            date_range = f"from {oldest.strftime('%Y-%m-%d')} to {newest.strftime('%Y-%m-%d')}"
        else:
            date_range = "unknown date range"
    else:
        date_range = "no log files"

    return f"{total_files} log files ({total_size} bytes) {date_range}"

def main():
    parser = argparse.ArgumentParser(description='Clean up old automation log files')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days of logs to keep (default: 7)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deleted without actually deleting')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=" * 60)
    logger.info("TRUCKIT AUTOMATION LOG CLEANUP UTILITY")
    logger.info("=" * 60)

    logs_dir = get_log_directory()

    # Show current status
    logger.info(f"Current logs status: {get_logs_summary(logs_dir)}")

    # Get files to delete
    files_to_delete = get_log_files_to_delete(logs_dir, args.days, args.dry_run)

    # Delete files
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be deleted")
        delete_old_logs(files_to_delete, dry_run=True)
        logger.info(f"Would delete {len(files_to_delete)} files")
    else:
        deleted_count = delete_old_logs(files_to_delete, dry_run=False)
        logger.info(f"Cleanup completed successfully. Deleted {deleted_count} files.")

    # Show final status
    logger.info(f"Final logs status: {get_logs_summary(logs_dir)}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()