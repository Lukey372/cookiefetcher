import undetected_chromedriver.v2 as uc
import time

def get_cookies():
    """Fetch Cloudflare cookies using undetected Chrome."""
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Remove this line if it still fails
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")

    try:
        driver = uc.Chrome(options=options)
        driver.get("https://gmgn.ai")
        time.sleep(15)  # Wait longer for Cloudflare challenge
        
        # Take a screenshot for debugging
        driver.save_screenshot("/app/debug_screenshot.png")

        cookies = driver.get_cookies()
        driver.quit()

        # Extract Cloudflare cookies
        return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {}
