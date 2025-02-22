import time
import shutil
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def get_cookies():
    """Fetch new Cloudflare cookies using Selenium."""
    options = Options()

    # ✅ Debugging - Print Chrome & Chromedriver Paths
    chrome_path = shutil.which("google-chrome")
    print(f"✅ Chrome Binary Path: {chrome_path}")

    # ✅ If Chrome path is not found, exit
    if not chrome_path:
        print("❌ ERROR: Chrome not found!")
        return {}

    options.binary_location = chrome_path  # ✅ Use detected Chrome path
    options.add_argument("--headless=new")  # Using newer headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")  # Make it look real
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        driver.get("https://gmgn.ai")
        
        # 🕰️ Increase wait time for Cloudflare challenge
        time.sleep(30)

        # ✅ Handle Cloudflare Challenge (Click Checkbox)
        try:
            driver.execute_script("document.querySelector('input[type=checkbox]').click()")
            time.sleep(10)  # Wait after click
        except Exception:
            pass  # No checkbox found, continue

        # 🛑 Save a screenshot to check what the bot is seeing
        driver.save_screenshot("/app/debug_screenshot.png")

        # ✅ Extract cookies
        cookies = driver.get_cookies()
        driver.quit()

        return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {}
