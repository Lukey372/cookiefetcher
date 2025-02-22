import undetected_chromedriver as uc
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def get_cookies():
    logging.debug("Starting get_cookies()")
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_argument("--disable-infobars")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        logging.debug("Launching Chrome driver")
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        logging.debug("Navigating to https://gmgn.ai")
        driver.get("https://gmgn.ai")
        time.sleep(20)  # increased sleep time for the challenge
        driver.save_screenshot("/app/debug_screenshot.png")
        cookies = driver.get_cookies()
        driver.quit()
        logging.debug("Cookies fetched, processing them...")
        return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}
    except Exception as e:
        logging.error(f"Error fetching cookies: {e}", exc_info=True)
        return {}

if __name__ == "__main__":
    cookies = get_cookies()
    print("Cookies:", cookies)
