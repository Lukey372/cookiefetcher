from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import shutil

def get_cookies():
    """Fetch new Cloudflare cookies using Selenium."""
    options = Options()

    # ✅ Debugging - Print Chrome & Chromedriver Paths
    chrome_path = shutil.which("google-chrome")
    chromedriver_path = shutil.which("chromedriver")
    print(f"✅ Chrome Binary Path: {chrome_path}")
    print(f"✅ ChromeDriver Path: {chromedriver_path}")

    # ✅ If paths are not found, exit
    if not chrome_path or not chromedriver_path:
        print("❌ ERROR: Chrome or Chromedriver not found!")
        return {}

    options.binary_location = chrome_path  # ✅ Use detected Chrome path
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")

    # ✅ Use manually detected ChromeDriver path
    service = Service(chromedriver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://gmgn.ai")
        time.sleep(15)  # Wait for Cloudflare challenge
        cookies = driver.get_cookies()
        driver.quit()
        return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {}
