from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
import pandas as pd
import time

def collect_suggestions(driver, search_keyword):
    all_suggestions = []
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(search_keyword)
    time.sleep(2) 

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
    time.sleep(1)  
    return all_suggestions

driver = webdriver.Chrome()

try:
    driver.get("https://www.google.com/search?q=iit+madras+cutoff&oq=iit+m&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDkyBggCEEUYPNIBCDEzODhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8")

    keywords = ["iit madras cutoff ", "iit jee cutoff ", "iit jee advanced ", "iit jee mains "]
    all_suggestions = []

    for search_keyword in keywords:
        try:
            suggestions = collect_suggestions(driver, search_keyword)
            all_suggestions.extend(suggestions)
        except NoSuchWindowException:
            driver = webdriver.Chrome()
            driver.get("https://www.google.com/search?q=iit+madras+cutoff&oq=iit+m&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDkyBggCEEUYPNIBCDEzODhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8")
            suggestions = collect_suggestions(driver, search_keyword)
            all_suggestions.extend(suggestions)

    df = pd.DataFrame(all_suggestions, columns=["Keyword", "Suggestion"])
    print(df)

finally:
    driver.quit()
