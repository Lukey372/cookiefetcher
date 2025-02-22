import undetected_chromedriver as uc
import time

def get_cookies():
    """
    Fetch Cloudflare cookies using an advanced (fortified) headless Chrome.
    """
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    # Try running without headless mode if detection is an issue:
    options.add_argument("--headless=new")
    options.add_argument("--disable-infobars")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    
    # Remove or comment out these experimental options:
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get("https://gmgn.ai")
        time.sleep(15)  # Wait for Cloudflare's challenge to complete
        
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
