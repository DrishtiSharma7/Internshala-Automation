# main.py
import time
from bot.browser import BrowserManager
from bot.cookies import load_cookies
from bot.scraper import scrape_internship_links
from bot.apply import apply_to_internship

with open("resume.ini") as f:
    resume_text = f.read()

browser = BrowserManager(headless=False)
driver = browser.start_browser()

load_cookies(driver)

print("👉 Apply filters MANUALLY then press ENTER")
input()

links = scrape_internship_links(driver)

for link in links:
    apply_to_internship(driver, link, resume_text)
    time.sleep(3)

browser.close_browser()

def main():
    browser = BrowserManager(headless=False)
    driver = browser.start_browser()

    driver.get("https://internshala.com")
    time.sleep(1)

    browser.close_browser()


if __name__ == "__main__":
    main()
