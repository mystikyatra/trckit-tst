# Truckit Automation Script

This repository contains an end-to-end Selenium automation script for the Truckit website. The test script is located at [tests/truckit.py](tests/truckit.py) and exercises the "Get a Quote" flow including adding freight, selecting locations, and attempting a negative login.

## Purpose
- Automate the quote request flow on https://www.truckit.net/.
- Demonstrate form interactions, Google Places autocomplete selection, dropdown handling, and a negative authentication test (invalid credentials).

## Prerequisites
- Python 3.8+
- Chrome browser installed
- Virtual environment (recommended)

Required Python packages (install with pip):

```bash
pip install selenium webdriver-manager
```

Note: The script uses `webdriver-manager` to download the correct ChromeDriver automatically.

## Files
- [tests/truckit.py](tests/truckit.py): The main automation script.

## How the script works (high-level)
1. setup_driver()
   - Creates a Chrome WebDriver using `webdriver-manager` and maximizes the window.

2. select_first_google_place(driver, input_id, location_text)
   - Types into a Google Places autocomplete input and selects the first suggestion.
   - Uses explicit waits for clickability and visibility.

3. test_truckit_quote_flow()
   - Launches the Truckit main page.
   - Selects the product category ("Pallets and Packages").
   - Uses `select_first_google_place` to choose origin (`suburb_id_collect`) and destination (`suburb_id_deliver`).
   - Clicks the "GET A QUOTE" button and switches to the new tab.
   - Fills freight details: category, description, pallet size, height, and weight.
   - Sets sender/receiver options, loading/unloading facilities, collection and delivery dates.
   - Proceeds to the authentication page and attempts a negative login using invalid credentials.
   - Handles reCAPTCHA by waiting for manual solving (the script detects completion and continues).
   - Verifies that an expected error message is displayed or that the user remains on the login page.
   - Always quits the driver in a `finally` block.

## Important implementation notes
- The script uses explicit waits (`WebDriverWait`) to avoid brittle sleeps. A few `time.sleep()` calls are still present to allow UI transitions.
- Google reCAPTCHA cannot be bypassed programmatically; the script switches into the reCAPTCHA iframe and waits up to 300 seconds for a human to solve it. This makes the script unsuitable for fully automated CI runs unless a test-friendly site or reCAPTCHA bypass is provided.
- Selectors used are a mix of IDs, XPaths and CSS selectors. If the site changes, selectors may need updates.
- The script is written as a simple function and runs when executed as `__main__`. For test frameworks (pytest/unittest) adapt the structure accordingly.

## Running the script
1. Create and activate a virtual environment (Windows example):

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt  # or `pip install selenium webdriver-manager`
```

2. Run the script:

```powershell
python tests\truckit.py
```

## Customization
- Change `URL` at the top of `tests/truckit.py` to point to another environment (staging).
- Update location text passed to `select_first_google_place` to test different origin/destination pairs.
- Replace hard-coded values (weights, heights, descriptions) with parameterized data or fixtures.

## Limitations and next steps
- Captcha requires manual intervention; consider using test-mode endpoints or mocks for automated CI.
- Add logging and exception handling for clearer diagnostics.
- Convert the script to a pytest test function and add fixtures for driver setup/teardown.
