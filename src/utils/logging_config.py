import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

def setup_logging():
    """Setup logging configuration for the automation framework"""

    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Generate daily log filename (YYYYMMDD format)
    today = datetime.now().strftime("%Y%m%d")
    log_filename = f"automation_test_{today}.log"
    log_filepath = os.path.join(logs_dir, log_filename)

    # Configure logging with file append mode
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath, mode='a'),  # Append mode
            logging.StreamHandler()  # Also log to console
        ]
    )

    # Create logger for the framework
    logger = logging.getLogger('truckit_automation')
    logger.info("=" * 80)
    logger.info("TRUCKIT AUTOMATION FRAMEWORK - TEST EXECUTION STARTED")
    logger.info(f"Log file: {log_filename}")
    logger.info("=" * 80)

    # Run log cleanup after setting up logging (keep 7 days)
    cleanup_old_logs(logs_dir, days_to_keep=7, verbose=True)

    return logger

def cleanup_old_logs(logs_dir=None, days_to_keep=7, verbose=False):
    """
    Clean up old log files, keeping only the specified number of days

    Args:
        logs_dir (str): Path to logs directory. If None, uses default.
        days_to_keep (int): Number of days of logs to keep
        verbose (bool): Whether to log cleanup operations
    """
    if logs_dir is None:
        logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')

    logs_path = Path(logs_dir)
    if not logs_path.exists():
        if verbose:
            logging.getLogger('truckit_automation').warning(f"Logs directory does not exist: {logs_dir}")
        return 0

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0

    logger = logging.getLogger('truckit_automation')

    for log_file in logs_path.glob('automation_test_*.log'):
        if log_file.is_file():
            # Parse filename to get creation date
            try:
                filename = log_file.name
                date_str = filename.replace('automation_test_', '').replace('.log', '')
                file_date = datetime.strptime(date_str, '%Y%m%d')

                if file_date < cutoff_date:
                    file_size = log_file.stat().st_size
                    log_file.unlink()
                    deleted_count += 1
                    if verbose:
                        logger.info(f"Deleted old log file: {filename} ({file_size} bytes)")
            except (ValueError, OSError) as e:
                if verbose:
                    logger.warning(f"Could not process log file {log_file.name}: {e}")

    if deleted_count > 0 and verbose:
        logger.info(f"Log cleanup completed: {deleted_count} old files removed")

    return deleted_count