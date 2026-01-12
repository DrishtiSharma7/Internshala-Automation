# bot/scraper.py

from selenium.webdriver.common.by import By
import time

def scrape_internship_links(driver):
    """
    Current page par jo internships dikh rahi hain
    unke detail links collect karta hai.
    """
    time.sleep(1)

    cards = driver.find_elements(By.CSS_SELECTOR, "div.individual_internship")
    links = []

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h3.job-internship-name").text
            company = card.find_element(By.CSS_SELECTOR, "p.company-name").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(f"📌 {title} | {company}")
            links.append(link)
        except Exception:
            continue

    print(f"Total internships found: {len(links)}")
    return links
