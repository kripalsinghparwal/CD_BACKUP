from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re

data = []

def get_data(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print("soup", soup)

    page_heading = driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/div[3]/div/div/div[1]/div[1]')
    heading = page_heading.find_element(By.TAG_NAME, 'h1').text
    print("heading", heading)

    main_section = soup.find("section", class_="subcontainer position_rltv headingWrapper wrapperV2 _0df9 wikiContents")
    article_div = main_section.find("div", class_="faq__according-wrapper")
    print("article_div", article_div.text)
    return data

    

def export_data(data):
    df = pd.DataFrame(data)
    df.to_csv("shiksha.csv")


def main():
    data = get_data('https://www.shiksha.com/studyabroad/usa/mba-colleges-dc-8')
    print(data)
    export_data(data)


if __name__ == '__main__':
    main()
