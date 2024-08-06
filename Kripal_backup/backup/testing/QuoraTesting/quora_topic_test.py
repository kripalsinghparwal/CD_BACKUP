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
question_url = "https://www.quora.com/topic/Studying-Abroad-in-the-United-States-of-America?q=study-in-usa"
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

# more_classname = "q-click-wrapper.qu-active--textDecoration--none.qu-focus--textDecoration--none.qu-borderRadius--pill.qu-alignItems--center.qu-justifyContent--center.qu-whiteSpace--nowrap.qu-userSelect--none.qu-display--inline-flex.qu-bg--gray_ultralight.qu-tapHighlight--white.qu-textAlign--center.qu-cursor--pointer.qu-hover--textDecoration--none.ClickWrapper___StyledClickWrapperBox-zoqi4f-0.iyYUZT.base___StyledClickWrapper-lx6eke-1.bxQEkr.puppeteer_test_read_more_button "
more_classname = "q-text.qu-cursor--pointer.QTextTruncated__StyledReadMoreLink-sc-1pev100-3.dXJUbS.qt_read_more.qu-color--blue_dark.qu-fontFamily--sans.qu-pl--tiny"
e=driver.find_elements(By.CLASS_NAME,more_classname)

print("e :", e)
for i in e:
    print(i.text)
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

def get_author_details(topic_block):
    author_intro_block = topic_block.find("div", class_="q-flex qu-alignItems--flex-start")
    author = author_intro_block.find("div", class_="q-inlineFlex qu-alignItems--center qu-wordBreak--break-word").text
    author_profile = author_intro_block.text.replace(author, "")

    return [author, author_profile]

def get_topic(topic_block):
    topic_question_text = topic_block.find("div", class_="q-text qu-truncateLines--5 puppeteer_test_question_title").text.strip()

    topic_content = topic_block.find("div", class_="q-box spacing_log_answer_content puppeteer_test_answer_content").text.strip()

    return [topic_question_text, topic_content]

def get_views(topic_block):
    try:
        view_upvotes_block = topic_block.find("div", class_="q-text qu-dynamicFontSize--small qu-pb--tiny qu-mt--small qu-color--gray_light qu-passColorToLinks")
        if "views" in view_upvotes_block.text:
            views = view_upvotes_block.text.split("·")[0].strip()
            print("views :",views)
            if "." in views:
                    views=int(views.replace(".","").replace("views","").replace("K","00")) #Replacing K with 00 so that we get approximate views in numerical number
                    return views
            else:
                views=views.replace("views","").replace("K","000")
                views=int(views)
                return views
            
        else:
            views = 0
            return views
    except:
        view_upvotes_block = "N/A"
        views = 0
        return views
    




for topic_block in soup.find_all("div", class_="q-box dom_annotate_multifeed_bundle_AnswersBundle qu-borderAll qu-borderRadius--small qu-borderColor--raised qu-boxShadow--small qu-mb--small qu-bg--raised"):

    print("author :", get_author_details(topic_block)[0])
    print("author_profile :", get_author_details(topic_block)[1])
    print("topic_question_text :", get_topic(topic_block)[0])
    print("topic_content_text :", get_topic(topic_block)[1])
    print("views_count :", get_views(topic_block))
    print("__________________________________________")


time.sleep(6)