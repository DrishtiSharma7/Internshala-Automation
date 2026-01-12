from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
print("Chrome opened successfully")

driver.get("https://www.chatgpt.com")
print("ChatGPT opened successfully")    

time.sleep(2)
driver.quit()
print("Done")
