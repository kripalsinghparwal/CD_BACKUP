from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from time import sleep
import pandas as pd
import sys
import warnings

from bs4 import BeautifulSoup
import time
import numpy as np
import random
warnings.filterwarnings("ignore")

# done_stream = ['business-management-studies','humanities-social-sciences', 'science', 'accounting-commerce', \
#                'teaching-education', 'it-software',  'medicine-health-sciences','mass-communication-media'\
#                 'design', 'arts-fine-visual-performing','banking-finance-insurance', \
#                'nursing', 'law', 'animation', 'architecture-planning', 'aviation','beauty-fitness', 'government-exams',\
#                'engineering']
# # 'hospitality-travel/colleges',
# stream_list = ['medicine-health-sciences'] 
py = "127.0.0.1:24000"
PATH = '/usr/bin/chromedriver'

# def scroll_click_load_more(driver):
#     load_more = driver.find_elements(By.XPATH, "//button[contains(@class,'button load-more-btn')]")
#     if len(load_more) < 1:
#         return 0
#     actions = ActionChains(driver)
#     actions.move_to_element_with_offset(load_more[0], 0, 200).click().perform()
#     # actions.from_element(load_more, 0, -50)
#     # actions.scroll_from_origin(scroll_origin, 0, 200).perform()
#     # actions.click(load_more)
#     # actions.perform()

page_num = 1
base_url = 'https://www.shiksha.com/colleges-'

while page_num<2000:
    target_url = base_url+str(page_num)
    print(page_num)
    options = Options()
    # options.add_argument('--proxy-server=%s' % py)
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    # options.add_argument('headless')
    options.add_argument('--no-sandbox') 
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--window-size=1400,600')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(PATH,options = options)
    df = pd.DataFrame(columns = 'college_name,url'.split(','))
    try:
        driver.get(target_url)
        sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # college_info_container = driver.find_element(By.CLASS_NAME, "ctpSrp-contnr") 
        # colleges = college_info_container.find_elements(By.XPATH, ".//h3")
        college_info_container = soup.find("div", class_="ctpSrp-contnr") 
        colleges = college_info_container.find_all("h3")
        for j in colleges:
            parent = j.find_element(By.XPATH, ".//..")
            url = parent.get_attribute('href')
            college_name = parent.text
            df = df.append([{'college_name':college_name,'url':url}],ignore_index =True)
    except Exception as ex:
        error_df = pd.DataFrame(columns = ['url','error'])
        error_df = error_df.append([{'url':target_url,'error':str(ex)}],ignore_index = True)
        error_df.to_csv('shiksha_error_urls.csv',mode = 'a',header = False,index = False)
    finally:
        df.to_csv("colleges_data.csv",mode = 'a',header = False, index = False)
        page_num+= 1
        driver.quit()
