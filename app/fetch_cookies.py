import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_challenge(driver):
    try:
        # Wait for the iframe that might contain the challenge (adjust the locator as needed)
        challenge_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'challenge')]"))
        )
        driver.switch_to.frame(challenge_iframe)

        # Wait for the challenge checkbox or button to become clickable (adjust the locator as needed)
        challenge_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#challenge-box, input[type='checkbox']"))
        )
        challenge_box.click()

        # Switch back to the main content once done
        driver.switch_to.default_content()
    except Exception as e:
        print(f"❌ Challenge click failed: {e}")

def get_cookies():
    """
    Fetch Cloudflare cookies using an advanced (fortified) Chrome.
    """
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    # Run in non-headless mode for better challenge handling:
    # options.add_argument("--headless=new")
    options.add_argument("--disable-infobars")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    
    try:
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get("https://gmgn.ai")
        
        # Optionally, wait a few seconds for the challenge to load
        time.sleep(5)
        click_challenge(driver)
        
        # Allow additional time for the challenge to be processed
        time.sleep(10)
        
        cookies = driver.get_cookies()
        driver.quit()
        
        # Extract only Cloudflare clearance cookies
        return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {}

if __name__ == "__main__":
    cookies = get_cookies()
    print("Cookies:", cookies)
