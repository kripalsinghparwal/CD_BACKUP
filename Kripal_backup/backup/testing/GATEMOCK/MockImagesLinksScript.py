######################### Code to find mock test question and images links ##########################################
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
import requests
from PIL import Image

# Your API URL and key
api_url = "https://www.imagetotext.info/api/imageToText"
api_key = "58b79c12489cd27e6b12a00a49efcced665a6cc1"

headers = {"Authorization": f"Bearer {api_key}"}

# URL of the image
url = "https://www.digialm.com/per/g01/pub/585/ASM/OnlineAssessment/M388/tkcimages/GA2Q8.jpg"

# Local filename to save the image
local_filename = "downloaded_image.jpg"
#-------------------------------------------------------------------------------------------------------------------------------
#when using chrome
import tracemalloc
from selenium.webdriver.chrome.service import Service

tracemalloc.start()

#code by pythonjar, not me to prevent notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
 

options = Options()
# options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

path='/usr/bin/chromedriver'

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  
mock_test_links = pd.read_csv(r"C:\Users\Kripal\Desktop\Kripal_backup\backup\testing\GATEMOCK\MockLinks.csv")["links"].to_list()
count = 1
row_dict_list = []
for x in list(mock_test_links)[0:18]:
    separated_string = x.split("?")[1]
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(x)
    time.sleep(3)

    ################# For log in #####################
    driver.find_element(By.ID,  "signInLabel").click()
    time.sleep(3)

    ################# For switching window handles ####
    print(driver.window_handles)
    print(driver.current_window_handle)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)

    ############ For clicking next button #########
    driver.find_element(By.ID, 'nextTxt').click()
    time.sleep(3)

    ################ For clicking disclaimer checkbox ###
    driver.find_element(By.ID, "disclaimer").click()
    time.sleep(3)

    ############ For clicking i am ready to begin button  ###
    driver.find_element(By.ID, 'readylinkButton').click()
    time.sleep(3)


    print(driver.current_url)
    driver.save_screenshot("ss{}.png".format(separated_string))
    count+=1
    # driver.quit()
    for i in range(65):
        question_type =driver.find_element(By.CLASS_NAME, "questiontype-details").text.split(":")[1].strip()
        current_subject = driver.find_element(By.CLASS_NAME, "subject-name.selectedsubject").text
        row_dict = {"exam_url" :  x, "subject": current_subject, "question_type": question_type}

        ############ For getting question content #############
        html_content =driver.find_element(By.ID, "quesAnsContent").get_attribute('outerHTML')

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the question image URL
        question_img_url = "https://www.digialm.com" + soup.find('div', {'class': 'textHighlighter'}).find('img')['src']
        print("Question Image URL:", question_img_url)
        # question_text = extractText(question_img_url)
        # row_dict['question_text'] = question_text
        row_dict['question_img_url']= question_img_url

        # Extract the options image URLs
        # option_img_urls = [extractText("https://www.digialm.com" + label.find('img')['src']) for label in soup.find_all('label', {'class': 'optionLabel'})]
        option_count = 1
        for label in soup.find_all('label', {'class': 'optionLabel'}):
            # row_dict[f"option{option_count}"] = extractText("https://www.digialm.com" + label.find('img')['src'])
            row_dict[f"option_url{option_count}"] =  "https://www.digialm.com" + label.find('img')['src']   
            # time.sleep(1)
            option_count +=1
        print("row_dict :",  
              row_dict)
        row_dict_list.append(row_dict)
        output_df = pd.DataFrame(row_dict_list)
        print("output_df", output_df)
        output_df.to_csv("UrlData4.csv")


        # print("Option Image URLs:", option_img_urls)
        print("-----------------------------------------------------------------------------------")
        # time.sleep(1)
        element = driver.find_element(By.CLASS_NAME, "normalBtn.btn.btn-primary-blue.sve_nxt.lst.auditlog.savenext.btnEnabled")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
    


    driver.quit()
