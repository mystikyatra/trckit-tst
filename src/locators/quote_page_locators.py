from selenium.webdriver.common.by import By

class QuotePageLocators:
    # Freight category dropdown
    FREIGHT_CATEGORY_DROPDOWN = (By.ID, "item_1_category_id_selector")

    # Freight details inputs
    FREIGHT_DESCRIPTION_INPUT = (By.ID, "item_1_desc_pallets")
    PALLET_SIZE_DROPDOWN = (By.ID, "item_1_pallet_size")
    PALLET_HEIGHT_INPUT = (By.ID, "item_1_height_pallet")
    PALLET_WEIGHT_INPUT = (By.ID, "item_1_weight_pallet")

    # Sender/Receiver button
    SENDER_RECEIVER_BUTTON = (By.CSS_SELECTOR, "a[data-toggle='sender_receiver'][data-title='1']")

    # Facility dropdowns
    LOADING_FACILITIES_DROPDOWN = (By.ID, "loading_facilities")
    UNLOADING_FACILITIES_DROPDOWN = (By.ID, "unloading_facilities")

    # Date radio buttons
    COLLECTION_DATE_RADIO = (By.ID, "collection_date_0")
    DELIVERY_DATE_RADIO = (By.ID, "delivery_date_0")

    # Continue button
    CONTINUE_BUTTON = (By.XPATH, "//a[normalize-space()='CONTINUE']")

    # Login button
    LOGIN_BUTTON = (By.XPATH, "//a[normalize-space()='Login']")