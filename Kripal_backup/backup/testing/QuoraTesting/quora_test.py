from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

import os
import sys
import time
import pandas as pd
import numpy as np

import time
import logging

import datetime
#-------------------------------------------------------------------------------------------------------------------------------
#when using chrome
import tracemalloc
from selenium.webdriver.chrome.service import Service

tracemalloc.start()

#code by pythonjar, not me to prevent notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

#for handler in logging.root.handlers[:]:
#    logging.root.removeHandler(handler)

#logging.basicConfig(filename = "Quora.log",level=logging.INFO)
# logging.basicConfig(filename = "/home/cd_scrapers/Quora/Quora_final/log/Quora_20-1-2023.log",level=logging.INFO)
# logger=logging.getLogger()
 

options = Options()
# options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

path='/usr/bin/chromedriver'
question_url = "https://www.quora.com/Is-it-safe-to-study-in-usa"
# driver = webdriver.Chrome(executable_path=path,options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(question_url)
print(question_url+"is running")
time.sleep(15)  

#Code for infinite scrolling

screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
print(screen_height)
scroll_height = driver.execute_script("return document.body.scrollHeight;") 
print(scroll_height)

try:
    driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_height)
    time.sleep(10)  
    new_scroll_height = driver.execute_script("return document.body.scrollHeight;") 
    print(new_scroll_height) 
except Exception as e:
    pass

print("Scroll Finished")

more_classname = "q-click-wrapper.qu-active--textDecoration--none.qu-focus--textDecoration--none.qu-borderRadius--pill.qu-alignItems--center.qu-justifyContent--center.qu-whiteSpace--nowrap.qu-userSelect--none.qu-display--inline-flex.qu-bg--gray_ultralight.qu-tapHighlight--white.qu-textAlign--center.qu-cursor--pointer.qu-hover--textDecoration--none.ClickWrapper___StyledClickWrapperBox-zoqi4f-0.iyYUZT.base___StyledClickWrapper-lx6eke-1.bxQEkr.puppeteer_test_read_more_button "
e=driver.find_elements(By.CLASS_NAME,more_classname)

for i in e:
    try:
        if i.text=="(more)":
            driver.execute_script("arguments[0].click();", i)
    except Exception as e:
        pass
    try:
        if i.text=="Continue Reading":
            driver.execute_script("arguments[0].click();", i)
    except Exception as e:
        pass
soup=BeautifulSoup(driver.page_source, 'html.parser')
# logger.info("Soup extracted"+question_url)

# print(soup)
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# len(driver.find_elements(By.XPATH, '//*[starts-with(@id,"mainContent")]/div[4]/div'))
driver.maximize_window()
for i in driver.find_elements(By.XPATH, '//*[@id="mainContent"]/div[4]/div')[0:2]:
    if i.get_attribute("class").startswith("q-box dom_annotate_question_answer_item"):
        # print(i.get_attribute("class"))
        answer_main_block = driver.find_element(By.CLASS_NAME, i.get_attribute("class").replace(" ", "."))
        click_element  = answer_main_block.find_element(By.XPATH, '//*[@id="mainContent"]/div[4]/div[2]/div[1]/div/div/div/div/div[2]/div/div[2]/div/span/span[4]/div')
        print(click_element.text)
        click_element.click()
time.sleep(60)