from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging

logger = logging.getLogger('truckit_automation.pages')

class BasePage:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config['explicit_wait'])
        logger.debug(f"Initialized {self.__class__.__name__} with driver and config")

    def find_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Found element with locator: {locator}")
            return element
        except Exception as e:
            logger.error(f"Failed to find element with locator: {locator}. Error: {str(e)}")
            raise

    def find_clickable_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"Found clickable element with locator: {locator}")
            return element
        except Exception as e:
            logger.error(f"Failed to find clickable element with locator: {locator}. Error: {str(e)}")
            raise

    def click_element(self, locator):
        try:
            self.find_clickable_element(locator).click()
            logger.debug(f"Clicked element with locator: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element with locator: {locator}. Error: {str(e)}")
            raise

    def send_keys_to_element(self, locator, text):
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.debug(f"Entered text '{text}' into element with locator: {locator}")
        except Exception as e:
            logger.error(f"Failed to send keys '{text}' to element with locator: {locator}. Error: {str(e)}")
            raise

    def select_dropdown_by_text(self, locator, text):
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(locator)
            Select(element).select_by_visible_text(text)
            logger.debug(f"Selected '{text}' from dropdown with locator: {locator}")
        except Exception as e:
            logger.error(f"Failed to select '{text}' from dropdown with locator: {locator}. Error: {str(e)}")
            raise

    def select_dropdown_by_value(self, locator, value):
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(locator)
            Select(element).select_by_value(value)
            logger.debug(f"Selected value '{value}' from dropdown with locator: {locator}")
        except Exception as e:
            logger.error(f"Failed to select value '{value}' from dropdown with locator: {locator}. Error: {str(e)}")
            raise

    def scroll_to_element(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            logger.debug("Scrolled to element")
        except Exception as e:
            logger.error(f"Failed to scroll to element. Error: {str(e)}")
            raise

    def js_click(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
            logger.debug("Performed JavaScript click on element")
        except Exception as e:
            logger.error(f"Failed to perform JavaScript click on element. Error: {str(e)}")
            raise

    def switch_to_window(self, window_index):
        try:
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[window_index])
            logger.debug(f"Switched to window at index: {window_index}")
        except Exception as e:
            logger.error(f"Failed to switch to window at index: {window_index}. Error: {str(e)}")
            raise

    def wait_for_element_visible(self, locator, timeout=None):
        try:
            wait_time = timeout or self.config['explicit_wait']
            element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element became visible with locator: {locator}")
            return element
        except Exception as e:
            logger.error(f"Element did not become visible with locator: {locator}. Error: {str(e)}")
            raise