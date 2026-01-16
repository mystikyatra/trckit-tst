from selenium.webdriver.common.by import By

class HomePageLocators:
    # Category dropdown
    CATEGORY_DROPDOWN = (By.ID, "category_id")

    # Location inputs
    ORIGIN_LOCATION_INPUT = (By.ID, "suburb_id_collect")
    DESTINATION_LOCATION_INPUT = (By.ID, "suburb_id_deliver")

    # Get Quote button
    GET_QUOTE_BUTTON = (By.XPATH, "//a[contains(@class,'banner-btn') and normalize-space()='GET A QUOTE']")

    # Google Places autocomplete suggestion
    GOOGLE_PLACES_SUGGESTION = (By.CSS_SELECTOR, ".pac-item")