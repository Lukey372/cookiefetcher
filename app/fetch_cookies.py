from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_cookies():
    """Fetch new Cloudflare cookies using Selenium."""
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Manually set Chrome binary path
    options.binary_location = "/usr/bin/google-chrome"

    # Manually specify Chromedriver path
    chromedriver_path = "/usr/local/bin/chromedriver"
    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://gmgn.ai")
        time.sleep(5)  # Wait for Cloudflare challenge
        cookies = driver.get_cookies()
    except Exception as e:
        print(f"❌ Error fetching cookies: {e}")
        cookies = {}
    
    driver.quit()
    return {cookie["name"]: cookie["value"] for cookie in cookies if cookie["name"] in ["cf_clearance", "__cf_bm"]}
