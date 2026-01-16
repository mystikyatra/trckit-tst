from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..locators.home_page_locators import HomePageLocators
import logging

logger = logging.getLogger('truckit_automation.pages.home_page')

class HomePage(BasePage):
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.locators = HomePageLocators()

    def navigate_to_home(self):
        logger.info(f"Navigating to home page: {self.config['base_url']}")
        self.driver.get(self.config['base_url'])
        logger.info("Successfully navigated to home page")

    def select_category(self, category):
        logger.info(f"Selecting category: {category}")
        self.select_dropdown_by_text(self.locators.CATEGORY_DROPDOWN, category)
        logger.info(f"Successfully selected category: {category}")

    def enter_origin_location(self, location):
        logger.info(f"Entering origin location: {location}")
        self._select_first_google_place(self.locators.ORIGIN_LOCATION_INPUT, location)
        logger.info(f"Successfully entered origin location: {location}")

    def enter_destination_location(self, location):
        logger.info(f"Entering destination location: {location}")
        self._select_first_google_place(self.locators.DESTINATION_LOCATION_INPUT, location)
        logger.info(f"Successfully entered destination location: {location}")

    def click_get_quote(self):
        logger.info("Clicking 'Get Quote' button")
        self.click_element(self.locators.GET_QUOTE_BUTTON)
        import time
        time.sleep(2)
        self.switch_to_window(-1)  # Switch to new tab
        logger.info("Successfully clicked 'Get Quote' button and switched to new tab")

    def _select_first_google_place(self, input_locator, location_text):
        logger.debug(f"Selecting first Google Places suggestion for location: {location_text}")
        self.send_keys_to_element(input_locator, location_text)
        suggestion = self.find_clickable_element(self.locators.GOOGLE_PLACES_SUGGESTION)
        suggestion.click()
        logger.debug(f"Successfully selected first Google Places suggestion for: {location_text}")