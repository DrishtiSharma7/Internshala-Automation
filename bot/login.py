# bot/login.py

print("login.py started")

import pickle
import time
from bot.browser import BrowserManager

LOGIN_URL = "https://internshala.com/login"
COOKIES_FILE = "cookies.pkl"

def manual_login_and_save_cookies():
    browser = BrowserManager(headless=False)
    driver = browser.start_browser()

    # 1️ Open Internshala login page
    driver.get(LOGIN_URL)
    print("Internshala login page opened")

    # 2️ Give time for page load
    time.sleep(0.1)

    print("Please login MANUALLY in the browser")
    input("Login complete ho jaaye to ENTER press karo...")

    # 3️ Save cookies after successful login
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(cookies, file)

    print("Cookies saved successfully as cookies.pkl")

    # 4️ Close browser
    browser.close_browser()
    print("Browser closed")
    
if __name__ == "__main__":
    manual_login_and_save_cookies()
