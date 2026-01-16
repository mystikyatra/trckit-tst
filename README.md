# Truckit Automation Framework

This repository contains a scalable Selenium-based automation framework for testing the Truckit website. The framework follows Page Object Model (POM) design pattern and uses pytest for test execution.

## Purpose
- Automate the quote request flow on https://www.truckit.net/.
- Demonstrate form interactions, Google Places autocomplete selection, dropdown handling, and authentication testing.
- Provide a maintainable and scalable structure for adding more test cases.

## Architecture
- **Page Object Model (POM)**: Separates page logic from test logic.
- **Configuration Management**: Centralized config for URLs, test data, and settings.
- **Utilities**: Reusable components for driver management and helpers.
- **Test Framework**: Uses pytest with fixtures for setup/teardown.
- **Reporting**: HTML reports generated after test runs.

## Prerequisites
- Python 3.8+
- Chrome browser installed
- Virtual environment (recommended)

## Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Project Structure
```
trkit/
├── README.md
├── requirements.txt
├── pytest.ini
├── config/
│   └── config.json          # Configuration file
├── src/
│   ├── locators/            # Page locators organized by page
│   │   ├── __init__.py
│   │   ├── home_page_locators.py    # Home page element locators
│   │   ├── quote_page_locators.py   # Quote page element locators
│   │   └── login_page_locators.py   # Login page element locators
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py     # Base page class with common methods
│   │   ├── home_page.py     # Home page interactions
│   │   ├── quote_page.py    # Quote form interactions
│   │   └── login_page.py    # Login page interactions
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── driver_manager.py # WebDriver setup
│   │   ├── helpers.py       # Configuration loading
│   │   └── logging_config.py # Logging configuration
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   └── test_truckit.py      # Test cases
├── logs/                    # Test execution logs (generated)
├── reports/                 # Test reports (generated)
├── screenshots/             # Failure screenshots (generated)
├── log_cleanup.py           # Log cleanup utility script
├── log_cleanup.bat          # Windows batch script for cleanup
└── setup_log_cleanup_task.bat # Setup script for scheduled cleanup```

## Logging and Debugging

The framework includes comprehensive logging to help you track test execution and troubleshoot issues:

### Log Files
- **Daily log files**: `automation_test_YYYYMMDD.log` (one file per day)
- **Append mode**: All test runs on the same day append to the same log file
- **Automatic cleanup**: Keeps only 7 days of recent logs, deletes older ones
- **Location**: `logs/` directory

### Log Levels
- **INFO**: Test steps, successful operations, test results
- **DEBUG**: Detailed element interactions, locator information
- **ERROR**: Failures, exceptions, troubleshooting information

### Running Tests with Logging
```bash
# Run tests with detailed logging
pytest -v

# Run specific test with logging
pytest tests/test_truckit.py::TestTruckitQuoteFlow::test_quote_flow_with_negative_login -v

# Generate HTML report with logs
pytest --html=reports/report.html
```

### Log Content
Each daily log file contains:
- Framework startup information
- All test executions for that day
- Step-by-step test progress
- Element interactions
- Error details and troubleshooting suggestions
- Test results (pass/fail)

### Screenshots on Failure
When tests fail, screenshots are automatically captured:
- **Location**: `screenshots/` directory
- **Naming**: `FAILED_{TestClass}_{test_name}_{timestamp}.png`
- **HTML Reports**: Screenshots are embedded in HTML test reports
- **Automatic**: No manual intervention required

### Troubleshooting Failed Tests
When a test fails, the logs will show:
1. **Which test failed** and at which step
2. **Detailed error messages** and stack traces
3. **Locator information** for failed element interactions
4. **Screenshot path** for visual debugging
5. **Troubleshooting suggestions** specific to the failure type

### Common Issues and Solutions
Based on logged errors, check:
- **ChromeDriver issues**: Update `src/utils/driver_manager.py`
- **Locator failures**: Update files in `src/locators/`
- **Network issues**: Check internet connection
- **UI changes**: Verify website hasn't changed
- **reCAPTCHA timeout**: Solve captcha within 5 minutes

## Log Management

The framework includes automatic log cleanup to prevent disk space issues:

### Manual Cleanup
```bash
# Clean up logs manually (keeps 7 days by default)
python log_cleanup.py

# Dry run to see what would be deleted
python log_cleanup.py --dry-run

# Keep 30 days of logs instead of 7
python log_cleanup.py --days 30

# Verbose output
python log_cleanup.py --verbose
```

### Scheduled Cleanup (Windows)
1. **Run the setup script** (requires Administrator privileges):
   ```bash
   setup_log_cleanup_task.bat
   ```

2. **Or manually create a Windows Task Scheduler task**:
   - Open Task Scheduler (`taskschd.msc`)
   - Create new task: "Truckit_Log_Cleanup"
   - Set trigger: Daily at 2:00 AM
   - Set action: Run `log_cleanup.bat` from project directory

### Cleanup Details
- **File pattern**: `automation_test_YYYYMMDD.log` (daily format)
- **Retention**: 7 days by default
- **Automatic**: Runs after each test execution
- **Safe operation**: Only deletes files older than retention period

## Running Tests
- Run all tests: `pytest`
- Run with verbose output: `pytest -v`
- Run specific test: `pytest tests/test_truckit.py::TestTruckitQuoteFlow::test_quote_flow_with_negative_login`
- Generate HTML report: `pytest --html=reports/report.html`

## Configuration
Edit `config/config.json` to modify:
- Base URL
- Browser settings
- Test data (locations, freight details, credentials)
- Wait times

## Locator Organization
Locators are organized in separate files under `src/locators/` for easy maintenance:

- `home_page_locators.py`: All locators for the home page
- `quote_page_locators.py`: All locators for the quote form page  
- `login_page_locators.py`: All locators for the login page

When UI elements change, you only need to update the corresponding locator file instead of searching through multiple page classes.

## Test Results Dashboard

The framework includes a comprehensive web-based dashboard for visualizing test results, metrics, trends, and failure analysis.

### Dashboard Features
- **📊 Summary Metrics**: Total executions, pass/fail rates, test counts
- **📈 Trends & Charts**: Execution trends over time, status distribution
- **🔥 Failure Analysis**: Most failed tests, failure categorization, heatmaps
- **📸 Screenshots Gallery**: Visual debugging with failed test screenshots
- **📋 Logs Viewer**: Access to all log files with download options
- **📄 Reports Browser**: View HTML test reports directly in browser
- **🏥 Health Overview**: Test health metrics, recent performance, failure rates

### Starting the Dashboard
```bash
# Run the dashboard (automatically installs dependencies if needed)
python run_dashboard.py
```

The dashboard will be available at: **http://localhost:5000**

### Dashboard Sections

#### Overview Tab
- **Key Metrics Cards**: Total executions, tests, pass/fail counts
- **Execution Trends Chart**: Line chart showing pass/fail trends over time
- **Status Distribution**: Pie chart of test status breakdown
- **Most Failed Tests**: Bar chart of frequently failing tests
- **Recent Results**: Table of latest test executions
- **Health Metrics**: Failure rate, 7-day pass rate, average tests per execution

#### Failed Screenshots Tab
- **Screenshot Gallery**: Grid view of all failure screenshots
- **Click to Enlarge**: Full-size screenshot viewing
- **Timestamp Information**: When each screenshot was captured
- **Test Context**: Screenshot names include test class and method

#### Logs Tab
- **Log Files Table**: List of all available log files
- **File Information**: Size, last modified timestamp
- **Download Links**: Direct download of log files
- **Size Display**: File sizes in KB for storage awareness

#### Reports Tab
- **HTML Reports Table**: List of all generated test reports
- **Test Summary**: Pass/fail counts per report
- **Timestamps**: When each report was generated
- **Direct Viewing**: Open HTML reports in new tabs

### Dashboard Data Sources
The dashboard automatically reads from:
- `reports/report.html` and other HTML reports
- `screenshots/` directory for failure images
- `logs/` directory for log files
- Real-time metrics calculation from all available data

### Dashboard Requirements
The dashboard requires additional Python packages:
```bash
pip install flask plotly pandas requests
```

These are automatically installed when running `python run_dashboard.py`.

### Dashboard Benefits
- **Quick Insights**: Instantly see test health and trends
- **Visual Debugging**: Screenshots help identify UI issues
- **Historical Analysis**: Track performance over time
- **Failure Patterns**: Identify consistently failing tests
- **Stakeholder Friendly**: Easy to understand visualizations
- **No Setup Required**: Runs locally with existing test data

## Adding New Tests
1. Create new page classes in `src/pages/` if needed
2. Add test methods in `tests/test_truckit.py` or create new test files
3. Use fixtures from `conftest.py` for driver and config

## Important Notes
- The script uses explicit waits to avoid brittle sleeps.
- Google reCAPTCHA requires manual solving; the script waits for completion.
- Selectors may need updates if the site changes.
- For CI/CD, consider headless mode and reCAPTCHA bypass solutions.

## Running the script
1. Create and activate a virtual environment (Windows example):

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt  # or `pip install selenium webdriver-manager`
```

2. Run the script:

```powershell
python tests\truckit.py
```

## Customization
- Change `URL` at the top of `tests/truckit.py` to point to another environment (staging).
- Update location text passed to `select_first_google_place` to test different origin/destination pairs.
- Replace hard-coded values (weights, heights, descriptions) with parameterized data or fixtures.

## Limitations and next steps
- Captcha requires manual intervention; consider using test-mode endpoints or mocks for automated CI.
- Add logging and exception handling for clearer diagnostics.
- Convert the script to a pytest test function and add fixtures for driver setup/teardown.
