@echo off
REM Log Cleanup Batch Script for Windows Task Scheduler
REM This script runs the log cleanup utility to remove old log files

echo Starting Truckit Automation Log Cleanup...
echo %DATE% %TIME%

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python log cleanup script
python log_cleanup.py

echo Log cleanup completed at %DATE% %TIME%
echo.

REM Optional: Log the cleanup operation
echo Log cleanup completed >> cleanup_history.log

pause