from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..locators.quote_page_locators import QuotePageLocators
import time
import logging

logger = logging.getLogger('truckit_automation.pages.quote_page')

class QuotePage(BasePage):
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.locators = QuotePageLocators()

    def select_freight_category(self, category_value="53"):
        logger.info(f"Selecting freight category with value: {category_value}")
        self.wait.until(lambda d: self.find_element(self.locators.FREIGHT_CATEGORY_DROPDOWN).is_enabled())
        self.select_dropdown_by_value(self.locators.FREIGHT_CATEGORY_DROPDOWN, category_value)
        logger.info(f"Successfully selected freight category: {category_value}")

    def enter_freight_description(self, description):
        logger.info(f"Entering freight description: {description}")
        self.send_keys_to_element(self.locators.FREIGHT_DESCRIPTION_INPUT, description)
        logger.info("Successfully entered freight description")

    def select_pallet_size(self, size_value="1"):
        logger.info(f"Selecting pallet size with value: {size_value}")
        self.wait.until(lambda d: self.find_element(self.locators.PALLET_SIZE_DROPDOWN).is_enabled())
        self.select_dropdown_by_value(self.locators.PALLET_SIZE_DROPDOWN, size_value)
        logger.info(f"Successfully selected pallet size: {size_value}")

    def enter_pallet_height(self, height):
        logger.info(f"Entering pallet height: {height}")
        self.send_keys_to_element(self.locators.PALLET_HEIGHT_INPUT, height)
        logger.info("Successfully entered pallet height")

    def enter_pallet_weight(self, weight):
        logger.info(f"Entering pallet weight: {weight}")
        self.send_keys_to_element(self.locators.PALLET_WEIGHT_INPUT, weight)
        logger.info("Successfully entered pallet weight")

    def click_sender_receiver_button(self):
        logger.info("Clicking sender/receiver button")
        element = self.find_element(self.locators.SENDER_RECEIVER_BUTTON)
        self.scroll_to_element(element)
        self.js_click(element)
        logger.info("Successfully clicked sender/receiver button")

    def select_loading_facility(self, facility):
        logger.info(f"Selecting loading facility: {facility}")
        self.select_dropdown_by_text(self.locators.LOADING_FACILITIES_DROPDOWN, facility)
        logger.info(f"Successfully selected loading facility: {facility}")

    def select_unloading_facility(self, facility):
        logger.info(f"Selecting unloading facility: {facility}")
        self.select_dropdown_by_text(self.locators.UNLOADING_FACILITIES_DROPDOWN, facility)
        logger.info(f"Successfully selected unloading facility: {facility}")

    def select_collection_date_option(self):
        logger.info("Selecting collection date option")
        element = self.find_element(self.locators.COLLECTION_DATE_RADIO)
        self.scroll_to_element(element)
        self.js_click(element)
        logger.info("Successfully selected collection date option")

    def select_delivery_date_option(self):
        logger.info("Selecting delivery date option")
        element = self.find_element(self.locators.DELIVERY_DATE_RADIO)
        self.scroll_to_element(element)
        self.js_click(element)
        logger.info("Successfully selected delivery date option")

    def click_continue(self):
        logger.info("Clicking continue button")
        element = self.find_element(self.locators.CONTINUE_BUTTON)
        self.scroll_to_element(element)
        self.js_click(element)
        logger.info("Successfully clicked continue button")

    def click_login_button(self):
        logger.info("Clicking login button")
        element = self.find_element(self.locators.LOGIN_BUTTON)
        self.scroll_to_element(element)
        self.js_click(element)
        logger.info("Successfully clicked login button")