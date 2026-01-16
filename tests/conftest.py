import pytest
import os
from datetime import datetime
from src.utils.driver_manager import DriverManager
from src.utils.helpers import load_config
from src.utils.logging_config import setup_logging
import logging

try:
    import pytest_html
except ImportError:
    pytest_html = None

# Setup logging at module level
logger = setup_logging()

@pytest.fixture(scope="session")
def config():
    logger.info("Loading test configuration from config.json")
    config_data = load_config()
    logger.info(f"Configuration loaded successfully. Base URL: {config_data.get('base_url')}")
    return config_data

@pytest.fixture(scope="function")
def driver(config, request):
    logger.info("Setting up WebDriver instance")
    driver = DriverManager.get_driver(config)
    logger.info("WebDriver setup completed successfully")

    # Store driver on the test item for screenshot hook
    request.node._driver = driver

    yield driver
    logger.info("Tearing down WebDriver instance")
    driver.quit()
    logger.info("WebDriver teardown completed")

@pytest.fixture(scope="function", autouse=True)
def log_test_execution_and_capture_screenshot(request, driver):
    """Log test execution start/end and capture screenshot on failure"""
    test_name = request.node.name
    test_class = request.node.cls.__name__ if request.node.cls else "NoClass"

    logger.info("=" * 60)
    logger.info(f"STARTING TEST: {test_class}.{test_name}")
    logger.info("=" * 60)

    def capture_screenshot_and_log_result():
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            # Capture screenshot on failure
            screenshot_path = capture_screenshot_on_failure(driver, test_class, test_name)
            logger.error("=" * 60)
            logger.error(f"TEST FAILED: {test_class}.{test_name}")
            logger.error(f"Screenshot saved: {screenshot_path}")
            logger.error("Failure details:")
            logger.error(str(request.node.rep_call.longrepr))
            logger.error("=" * 60)
        elif hasattr(request.node, 'rep_call') and request.node.rep_call.passed:
            logger.info("=" * 60)
            logger.info(f"TEST PASSED: {test_class}.{test_name}")
            logger.info("=" * 60)
        else:
            logger.warning(f"TEST STATUS UNKNOWN: {test_class}.{test_name}")

    request.addfinalizer(capture_screenshot_and_log_result)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to add screenshot to HTML report on failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get the driver from the test function
        driver = getattr(item, '_driver', None)
        if driver:
            # Capture screenshot
            screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"FAILED_{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)

            try:
                driver.save_screenshot(screenshot_path)
                # Add screenshot to HTML report
                if hasattr(report, 'extra'):
                    report.extra.append(pytest_html.extras.image(screenshot_path))
                    report.extra.append(pytest_html.extras.html(f"<p>Screenshot: {screenshot_name}</p>"))
            except Exception as e:
                logger.error(f"Failed to capture screenshot for HTML report: {e}")