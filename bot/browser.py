# bot/browser.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "/Users/drishtisharma/Downloads/chromedriver-mac-arm64/chromedriver"
CHROME_BINARY_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

class BrowserManager:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None

    def start_browser(self):
        chrome_options = Options()
        chrome_options.binary_location = CHROME_BINARY_PATH

        if self.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        service = Service(CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        return self.driver
    
    def close_browser(self):
        if self.driver:
            self.driver.quit()
