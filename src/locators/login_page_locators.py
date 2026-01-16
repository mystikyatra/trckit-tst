from selenium.webdriver.common.by import By

class LoginPageLocators:
    # Login form inputs
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")

    # reCAPTCHA iframe
    RECAPTCHA_IFRAME = (By.CSS_SELECTOR, "iframe[src*='recaptcha']")
    RECAPTCHA_ANCHOR = (By.ID, "recaptcha-anchor")

    # Login submit button
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//a[contains(@class,'btn-full') and .//span[text()='LOGIN']]")

    # Error message
    ERROR_MESSAGE = (By.XPATH, "//span[contains(text(),'Sorry the email or password is incorrect')]")