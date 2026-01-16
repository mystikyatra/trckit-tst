#!/usr/bin/env python3
"""
Demo script to generate sample test data for the dashboard.

This script creates sample HTML reports, logs, and screenshots
to demonstrate the dashboard functionality.
"""

import os
import json
from datetime import datetime, timedelta
import random

def create_sample_report(report_path, execution_date, passed=5, failed=2, total=7):
    """Create a sample HTML report"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report - {execution_date.strftime('%Y-%m-%d %H:%M')}</title>
</head>
<body>
    <h1>Test Results</h1>
    <div id="summary">
        <p>{total} tests ran</p>
        <p>{passed} passed</p>
        <p>{failed} failed</p>
        <p>0 skipped</p>
        <p>0 error</p>
    </div>
    <table>
        <tr><th>Test Name</th><th>Status</th><th>Duration</th><th>Message</th></tr>
"""

    # Add test results
    test_names = [
        "test_quote_flow_with_negative_login",
        "test_home_page_loading",
        "test_location_selection",
        "test_freight_details",
        "test_quote_submission",
        "test_login_validation",
        "test_error_handling"
    ]

    for i, name in enumerate(test_names[:total]):
        status = "passed" if i < passed else "failed"
        duration = f"{random.uniform(1.5, 8.5):.2f}s"
        message = "Test passed successfully" if status == "passed" else "Element not found or timeout"
        html_content += f"        <tr><td>{name}</td><td>{status}</td><td>{duration}</td><td>{message}</td></tr>\n"

    html_content += """    </table>
</body>
</html>"""

    with open(report_path, 'w') as f:
        f.write(html_content)

def create_sample_log(log_path, execution_date):
    """Create a sample log file"""
    log_content = f"""2024-01-16 10:00:00,000 - INFO - ============================================================
2024-01-16 10:00:00,000 - INFO - TRUCKIT AUTOMATION FRAMEWORK STARTED
2024-01-16 10:00:00,000 - INFO - ============================================================
2024-01-16 10:00:00,001 - INFO - Loading test configuration from config.json
2024-01-16 10:00:00,002 - INFO - Starting test: Complete quote flow with negative login
2024-01-16 10:00:00,003 - INFO - Test data loaded: Origin=New York, NY, Destination=Los Angeles, CA
2024-01-16 10:00:00,004 - INFO - Step 1: Navigating to home page and selecting category
2024-01-16 10:00:00,005 - INFO - Step 2: Entering origin and destination locations
2024-01-16 10:00:00,006 - INFO - Step 3: Clicking 'Get Quote' button
2024-01-16 10:00:00,007 - INFO - Step 4: Filling freight details
2024-01-16 10:00:00,008 - INFO - Step 5: Configuring sender/receiver and facilities
2024-01-16 10:00:00,009 - INFO - Step 6: Selecting collection and delivery dates
2024-01-16 10:00:00,010 - INFO - Step 7: Proceeding to authentication
2024-01-16 10:00:00,011 - INFO - Step 8: Attempting negative login with invalid credentials
2024-01-16 10:00:00,012 - INFO - Step 9: Verifying negative login result
2024-01-16 10:00:00,013 - INFO - [PASS] Negative login test PASSED: Error message displayed as expected
2024-01-16 10:00:00,014 - INFO - Test execution completed successfully
2024-01-16 10:00:00,015 - INFO - ============================================================
"""

    with open(log_path, 'w') as f:
        f.write(log_content)

def generate_demo_data():
    """Generate sample data for dashboard demonstration"""
    print("🎯 Generating demo data for Truckit Test Dashboard")
    print("=" * 50)

    # Create directories if they don't exist
    os.makedirs('reports', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('screenshots', exist_ok=True)

    # Generate sample reports for the last 7 days
    base_date = datetime.now()

    for i in range(7):
        execution_date = base_date - timedelta(days=i)

        # Create sample report
        report_filename = f"report_{execution_date.strftime('%Y%m%d_%H%M')}.html"
        report_path = os.path.join('reports', report_filename)

        # Vary the results slightly for each day
        passed = random.randint(3, 6)
        failed = random.randint(0, 2)
        total = passed + failed

        create_sample_report(report_path, execution_date, passed, failed, total)
        print(f"✓ Created report: {report_filename} ({passed} passed, {failed} failed)")

        # Create sample log for the day
        if i == 0:  # Only create today's log
            log_filename = f"automation_test_{execution_date.strftime('%Y%m%d')}.log"
            log_path = os.path.join('logs', log_filename)
            create_sample_log(log_path, execution_date)
            print(f"✓ Created log: {log_filename}")

    # Create a few sample screenshots
    screenshot_files = [
        "FAILED_test_quote_flow_with_negative_login_20240116_100000.png",
        "FAILED_test_login_validation_20240115_140000.png",
        "FAILED_test_error_handling_20240114_160000.png"
    ]

    for screenshot in screenshot_files:
        screenshot_path = os.path.join('screenshots', screenshot)
        # Create a placeholder image file (just empty for demo)
        with open(screenshot_path, 'wb') as f:
            f.write(b'')  # Empty file as placeholder
        print(f"✓ Created screenshot placeholder: {screenshot}")

    print("\n✅ Demo data generation complete!")
    print("🚀 You can now run the dashboard with: python run_dashboard.py")
    print("📊 Dashboard will show sample metrics, trends, and visualizations")

if __name__ == "__main__":
    generate_demo_data()