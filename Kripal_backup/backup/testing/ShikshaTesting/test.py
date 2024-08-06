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

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

py = "127.0.0.1:24000"
PATH = '/usr/bin/chromedriver'



# df = pd.read_csv("/home/binoy/shiksha_cd_comparison/input_folder/top_2800_colleges.csv")

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

driver.get("https://www.shiksha.com/university/university-of-mumbai-856")
time.sleep(5)
# print(driver.find_element(By.XPATH, "//*[@id='ovp_section_fees_and_eligibility']/div/div/div[3]/a").text)
# try:
#     button = driver.find_element(By.XPATH, "//*[@id='ovp_section_fees_and_eligibility']/div/div/div[3]/a")
#     time.sleep(15)
#     button.click()
# except Exception as e:
#     print(e)
# try:
#     driver.find_element(By.XPATH, "//*[@id='ovp_section_fees_and_eligibility']/div/div/div[3]/a").click()
#     time.sleep(10)
# except Exception as e:
#     print(e)

try:
    driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[2]/div/a').click()
except Exception as e:
    print(e)
    driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[2]/div/a').click()
courses_list = driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[1]/div[3]/div[2]/div/ul').find_elements(By.TAG_NAME, 'li')
print(len(courses_list))
for i in range(1 , len(courses_list)+1):
    try:
        driver.find_element(By.XPATH, f'//*[@id="dateWithExams"]/section/div/div/div/div[1]/div[3]/div[2]/div/ul/li[{i}]').click()
        time.sleep(3)

        print(">>>>>>>>>>>>>>", driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[2]/div/span[1]').text ,driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/div/table').text)
        
        driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[2]/div/span[1]').click()
        time.sleep(5)

        

        driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[2]/div/a').click()
        time.sleep(3)

    except Exception as e:
        print("Exception 2", e)
        time.sleep(5)
        try:
            driver.find_element(By.CLASS_NAME, 'cross-x').click()
            driver.find_element(By.XPATH, '//*[@id="dateWithExams"]/section/div/div/div/div[2]/div/a').click()
        except Exception as e:
            print("inner Exception", e)


time.sleep(10)
driver.quit()

