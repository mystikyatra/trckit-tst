@echo off
REM Windows Task Scheduler Setup Script for Log Cleanup
REM This script creates a scheduled task to run log cleanup daily

echo Setting up Windows Task Scheduler for Truckit Log Cleanup...
echo.

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "TASK_NAME=Truckit_Log_Cleanup"

REM Remove existing task if it exists
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
if %errorlevel% equ 0 (
    echo Removed existing task: %TASK_NAME%
)

REM Create new daily task
schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_DIR%log_cleanup.bat\"" /sc daily /st 02:00 /ru "%USERNAME%" /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Scheduled task created!
    echo Task Name: %TASK_NAME%
    echo Schedule: Daily at 2:00 AM
    echo Command: %SCRIPT_DIR%log_cleanup.bat
    echo.
    echo You can modify this task in Task Scheduler (taskschd.msc)
    echo or run 'schtasks /query /tn "%TASK_NAME%"' to check status
) else (
    echo.
    echo ERROR: Failed to create scheduled task.
    echo You may need to run this script as Administrator.
    echo.
    echo Alternative: Manually create a task in Task Scheduler:
    echo 1. Open Task Scheduler (taskschd.msc)
    echo 2. Create new task
    echo 3. Set trigger to Daily at 2:00 AM
    echo 4. Set action to run: %SCRIPT_DIR%log_cleanup.bat
)

echo.
pause