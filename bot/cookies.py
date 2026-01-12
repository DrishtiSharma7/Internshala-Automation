# bot/cookies.py

import pickle
import time

def load_cookies(driver, cookies_file="cookies.pkl"):
    with open(cookies_file, "rb") as file:
        cookies = pickle.load(file)

    driver.get("https://internshala.com")
    time.sleep(2)

    for cookie in cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(1)
    print("Login cookies loaded")
