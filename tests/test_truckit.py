import pytest
import time
import logging
from src.pages.home_page import HomePage
from src.pages.quote_page import QuotePage
from src.pages.login_page import LoginPage

logger = logging.getLogger('truckit_automation.tests')

class TestTruckitQuoteFlow:
    def test_quote_flow_with_negative_login(self, driver, config):
        """Test the complete quote flow including negative login scenario"""
        logger.info("Starting test: Complete quote flow with negative login")

        # Initialize page objects
        home_page = HomePage(driver, config)
        quote_page = QuotePage(driver, config)
        login_page = LoginPage(driver, config)

        test_data = config['test_data']
        logger.info(f"Test data loaded: Origin={test_data['origin']}, Destination={test_data['destination']}")

        try:
            # Step 1: Navigate to home and select category
            logger.info("Step 1: Navigating to home page and selecting category")
            home_page.navigate_to_home()
            home_page.select_category(test_data['category'])

            # Step 2: Enter locations
            logger.info("Step 2: Entering origin and destination locations")
            home_page.enter_origin_location(test_data['origin'])
            home_page.enter_destination_location(test_data['destination'])

            # Step 3: Click get quote and switch to new tab
            logger.info("Step 3: Clicking 'Get Quote' button")
            home_page.click_get_quote()

            # Step 4: Fill freight details
            logger.info("Step 4: Filling freight details")
            freight = test_data['freight']
            quote_page.select_freight_category()
            quote_page.enter_freight_description(freight['description'])
            quote_page.select_pallet_size(freight['pallet_size'])
            quote_page.enter_pallet_height(freight['height'])
            quote_page.enter_pallet_weight(freight['weight'])

            # Step 5: Select sender/receiver and facilities
            logger.info("Step 5: Configuring sender/receiver and facilities")
            quote_page.click_sender_receiver_button()
            facilities = test_data['facilities']
            quote_page.select_loading_facility(facilities['loading'])
            quote_page.select_unloading_facility(facilities['unloading'])

            # Step 6: Select dates
            logger.info("Step 6: Selecting collection and delivery dates")
            quote_page.select_collection_date_option()
            quote_page.select_delivery_date_option()

            # Step 7: Proceed to authentication
            logger.info("Step 7: Proceeding to authentication")
            quote_page.click_continue()
            quote_page.click_login_button()

            # Step 8: Attempt negative login
            logger.info("Step 8: Attempting negative login with invalid credentials")
            credentials = test_data['invalid_credentials']
            login_page.enter_email(credentials['email'])
            login_page.enter_password(credentials['password'])
            login_page.wait_for_recaptcha_and_solve()
            login_page.click_login_submit()

            # Step 9: Verify negative login
            logger.info("Step 9: Verifying negative login result")
            time.sleep(5)  # Wait for response

            if login_page.is_error_message_displayed():
                logger.info("✓ Negative login test PASSED: Error message displayed as expected")
                assert True
            elif login_page.is_on_login_page():
                logger.info("✓ Negative login test PASSED: Remained on login page as expected")
                assert True
            else:
                logger.error("✗ Negative login test FAILED: Unexpected behavior - neither error message shown nor stayed on login page")
                logger.error(f"Current URL: {driver.current_url}")
                pytest.fail("Negative login test failed - unexpected behavior")

        except Exception as e:
            logger.error(f"Test execution failed with error: {str(e)}")
            logger.error("Check the following for troubleshooting:")
            logger.error("1. Ensure Chrome browser is installed and up to date")
            logger.error("2. Check internet connection for accessing truckit.net")
            logger.error("3. Verify locators in src/locators/ files are still valid")
            logger.error("4. Check if website UI has changed")
            logger.error("5. Ensure reCAPTCHA is solved manually within 5 minutes")
            raise