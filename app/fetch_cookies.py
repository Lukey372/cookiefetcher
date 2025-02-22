from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_cookies():
    """Fetch new Cloudflare cookies using Selenium."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # Manually specify ChromeDriver path
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://gmgn.ai")
        time.sleep(5)  # Wait for Cloudflare challenge to pass
        cookies = driver.get_cookies()
    except Exception as e:
        print(f"❌ Error fetching cookies: {e}")
        cookies = {}
    
    driver.quit()
    return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}
