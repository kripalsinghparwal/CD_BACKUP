from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
import pandas as pd
import time
from urllib.parse import quote
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# PATH = "/usr/bin/chromedriver" #Path to chromedriver (Adjust as needed)

options = {
'proxy': {'http': 'http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225',
'https': 'http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225'},
}

driver= webdriver.Chrome(seleniumwire_options=options,options=chrome_options)

def collect_suggestions(driver, search_keyword):
    all_suggestions = []
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(search_keyword)
    time.sleep(2)  # Allow suggestions to load

    suggestions_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.G43f7e"))
    )

    li_elements = suggestions_container.find_elements(By.CSS_SELECTOR, "li span")

    for li in li_elements:
        attempts = 0
        while attempts < 3:
            try:
                suggestion_text = li.text
                if suggestion_text:
                    all_suggestions.append((search_keyword, suggestion_text))
                break
            except StaleElementReferenceException:
                attempts += 1
                li_elements = suggestions_container.find_elements(By.CSS_SELECTOR, "li span")
                continue

    search_box.clear()
    search_box.send_keys(Keys.ESCAPE)
    time.sleep(1)  # Allow suggestions to close
    return all_suggestions

try:
    driver.get("https://www.google.com/search?q=iit+madras+cutoff&oq=iit+m&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDkyBggCEEUYPNIBCDEzODhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8")
    time.sleep(10)

    keywords = ["iit madras cutoff", "iit jee cutoff", "iit jee advanced", "iit jee mains"]
    all_suggestions = []

    for search_keyword in keywords:
        try:
            suggestions = collect_suggestions(driver, search_keyword)
            all_suggestions.extend(suggestions)
        except NoSuchWindowException:
            driver.get("https://www.google.com/search?q=iit+madras+cutoff&oq=iit+m&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDkyBggCEEUYPNIBCDEzODhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8")
            suggestions = collect_suggestions(driver, search_keyword)
            all_suggestions.extend(suggestions)

    df = pd.DataFrame(all_suggestions, columns=["Keyword", "Suggestion"])
    print(df)

finally:
    driver.quit()
