from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

class DriverManager:
    @staticmethod
    def get_driver(config):
        options = webdriver.ChromeOptions()
        if config.get('headless', False):
            options.add_argument("--headless")
        options.add_argument("--start-maximized")

        # Get the chromedriver directory
        driver_dir = ChromeDriverManager().install()
        # Extract the directory path (remove the file part)
        if os.path.isfile(driver_dir):
            driver_dir = os.path.dirname(driver_dir)

        # Construct the path to chromedriver.exe
        driver_path = os.path.join(driver_dir, "chromedriver.exe")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(config['implicit_wait'])
        return driver