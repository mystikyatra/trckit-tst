from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..locators.login_page_locators import LoginPageLocators
import time
import logging

logger = logging.getLogger('truckit_automation.pages.login_page')

class LoginPage(BasePage):
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.locators = LoginPageLocators()

    def enter_email(self, email):
        logger.info(f"Entering email: {email}")
        self.send_keys_to_element(self.locators.EMAIL_INPUT, email)
        logger.info("Successfully entered email")

    def enter_password(self, password):
        logger.info("Entering password (masked for security)")
        self.send_keys_to_element(self.locators.PASSWORD_INPUT, password)
        logger.info("Successfully entered password")

    def wait_for_recaptcha_and_solve(self):
        logger.info("Waiting for reCAPTCHA to be solved manually")
        iframe = self.find_element(self.locators.RECAPTCHA_IFRAME)
        self.driver.switch_to.frame(iframe)
        checkbox = self.find_element(self.locators.RECAPTCHA_ANCHOR)
        # Wait for manual solving
        self.wait.until(lambda d: checkbox.get_attribute("aria-checked") == "true")
        self.driver.switch_to.default_content()
        logger.info("reCAPTCHA solved successfully, proceeding with login")

    def click_login_submit(self):
        logger.info("Clicking login submit button")
        element = self.find_element(self.locators.LOGIN_SUBMIT_BUTTON)
        self.scroll_to_element(element)
        self.js_click(element)
        logger.info("Successfully clicked login submit button")

    def is_error_message_displayed(self):
        logger.info("Checking if error message is displayed")
        try:
            result = self.wait_for_element_visible(self.locators.ERROR_MESSAGE, timeout=10).is_displayed()
            if result:
                logger.info("Error message is displayed")
            else:
                logger.info("Error message is not displayed")
            return result
        except:
            logger.info("Error message element not found")
            return False

    def is_on_login_page(self):
        current_url = self.driver.current_url
        result = "/login" in current_url
        logger.info(f"Checking if on login page. Current URL: {current_url}, Is login page: {result}")
        return result