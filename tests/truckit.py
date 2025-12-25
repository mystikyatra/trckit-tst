from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://www.truckit.net/"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def select_first_google_place(driver, input_id, location_text):
    # Select the first suggestion from Google Places autocomplete dropdown
    wait = WebDriverWait(driver, 25)
    input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
    input_field.clear()
    input_field.send_keys(location_text)

    first_suggestion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".pac-item")))
    first_suggestion.click()

def test_truckit_quote_flow():
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        # 1. Navigate to Truckit main page
        driver.get(URL)

        # 2. Select category on main page - Pallets & Packages
        category_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "category_id")))
        select = Select(category_dropdown)
        select.select_by_visible_text("Pallets and Packages")

        # 3. Enter Locations
        select_first_google_place(driver, "suburb_id_collect", "Brisbane")
        select_first_google_place(driver, "suburb_id_deliver", "Sydney")

        # 4. Click GET A QUOTE and switch to new tab
        get_quote_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class,'banner-btn') and normalize-space()='GET A QUOTE']")
            )
        )
        get_quote_btn.click()
        time.sleep(2)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])

        # 5. Add Freight - Fill Pallet details
        quote_dropdown = wait.until(EC.presence_of_element_located((By.ID, "item_1_category_id_selector")))
        WebDriverWait(driver, 30).until(lambda d: quote_dropdown.is_enabled())
        Select(quote_dropdown).select_by_value("53")  # Pallets & Packages

        contents_on_pallet = wait.until(EC.presence_of_element_located((By.ID, "item_1_desc_pallets")))
        contents_on_pallet.send_keys("Coffee Jars")

        pallet_size_dropdown = wait.until(EC.presence_of_element_located((By.ID, "item_1_pallet_size")))
        WebDriverWait(driver, 20).until(lambda d: pallet_size_dropdown.is_enabled())
        Select(pallet_size_dropdown).select_by_value("1")

        heights_per_pallet = wait.until(EC.presence_of_element_located((By.ID, "item_1_height_pallet")))
        heights_per_pallet.send_keys("20")
        weight_per_pallet = wait.until(EC.presence_of_element_located((By.ID, "item_1_weight_pallet")))
        weight_per_pallet.send_keys("3")

        sender_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-toggle='sender_receiver'][data-title='1']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sender_button)
        time.sleep(0.5)
        sender_button.click()

        loading_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "loading_facilities"))
        )
        Select(loading_dropdown).select_by_visible_text("Residential")

        unloading_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "unloading_facilities"))
        )
        Select(unloading_dropdown).select_by_visible_text("Residential")

        collection_radio = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "collection_date_0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", collection_radio)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", collection_radio)

        delivery_radio = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "delivery_date_0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", delivery_radio)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", delivery_radio)

        # 6. Proceed to Authentication
        continue_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='CONTINUE']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", continue_btn)

        login_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Login']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", login_btn)

        # 7. Authentication Attempt (Negative Case)
        email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys("invalid@example.com")

        password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys("wrongpassword")

        # Handle reCAPTCHA manually
        captcha_iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']"))
        )
        driver.switch_to.frame(captcha_iframe)
        captcha_checkbox = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "recaptcha-anchor"))
        )
        WebDriverWait(driver, 300).until(
            lambda d: captcha_checkbox.get_attribute("aria-checked") == "true"
        )
        driver.switch_to.default_content()
        print("CAPTCHA solved, clicking login automatically...")

        login_submit_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class,'btn-full') and .//span[text()='LOGIN']]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_submit_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", login_submit_btn)

        # 8. Verification
        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[contains(text(),'Sorry the email or password is incorrect')]")
                )
            )
            assert error_message.is_displayed(), "Error message not displayed"
            print("Negative login test passed: Error message displayed")
        except:
            current_url = driver.current_url
            if "/login" in current_url:
                print("Negative login test passed: Stayed on login page")
            else:
                print("Negative login test failed")

        time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    test_truckit_quote_flow()