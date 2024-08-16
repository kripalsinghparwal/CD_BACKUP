
# coding: utf-8

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

import os
import sys
import time
import pandas as pd
import numpy as np
import threading
import time
import logging

from datetime import datetime
#-------------------------------------------------------------------------------------------------------------------------------
#when using chrome
import tracemalloc

tracemalloc.start()
#

#code by pythonjar, not me to prevent notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

#for handler in logging.root.handlers[:]:
#           logging.root.removeHandler(handler)
#logging.basicConfig(filename = "Quora.log",level=logging.INFO)
logging.basicConfig(filename = "/home/cd_scrapers/Quora/Quora_final/log/Quora_20-1-2023.log",level=logging.INFO)
logger=logging.getLogger()
options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

def find_keyword_urls(keyword):
    #To get the url to search for the questions from the given keyword

    keyword = keyword.replace(" ","%20")
    qoura_question_url=f"https://www.quora.com/search?q={keyword}&type=question"
    # qoura_question_url=f"https://www.quora.com/topic/Studying-Abroad-in-the-United-States-of-America?q=study%20in%20usa"
    # print(qoura_question_url)
    return qoura_question_url

def getting_title(url):  #Function to find the titles of urls-questions

    split_list=url.split("/")
    title=split_list[-1]
    cleaned_title=title.replace("-"," ")
    return cleaned_title

def find_questions(keyword_url): #Function to find the question urls
    try:   # x = keyword1_urls[1]
        
        x=keyword_url
        counter=0
        urls_list=[]
        titles_list=[]
        #driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        path='/usr/bin/chromedriver'
        driver = webdriver.Chrome(options=options)
        print("keywords running -> {}".format(x))
        driver.get(x)
        time.sleep(20)
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        print("screen_height :",screen_height)
        i = 1
        scroll_pause_time=8
        while True:
            try:
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                #scroll_height = driver.execute_script("return document.body.scrollHeight;")
                #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                i += 1
                time.sleep(scroll_pause_time)
                soup=BeautifulSoup(driver.page_source, 'html.parser')
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")  
                
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                print(i)
                print(screen_height*i,scroll_height)
                
                if (screen_height)*i >scroll_height:
                    
                    break
                if i == 50:
                    break
                
            except Exception as e:
                break    
        logger.info("Scrolling finished for {}".format(i))
        print("Scrolling finished for {}".format(x))     
        classname = "q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline"
        # topic_clssname ="q-box qu-mb--tiny"
        anchors=soup.find_all('a',class_=classname)
        #print(len(anchors))
        #for each anchor checking it's class and if it belongs to that class then getting the url and appending the list
        if anchors is not None:
            for j in anchors:
                #print(j)
                
                   
                    urls_list.append(j['href'])
                    titles_list.append(j.text)
                    counter=counter+1
        # driver.close()
        driver.quit()
        print("Found all the URLS")
        question_count = len(urls_list)
        print(urls_list)
        print(titles_list)
        qoura_urls_df  = pd.DataFrame({'URL':urls_list,'Title':titles_list})
        #qoura_urls_df['Title'] =qoura_urls_df['URL'].apply(getting_title)
        logger.info(qoura_urls_df)
        
        return {"qoura_urls_df":qoura_urls_df,"counter":counter}
    except Exception as e:
        # driver.close()
        driver.quit()
        logger.error("Extraction  failed for"+keyword_url+str(e))
        




def questions(keyword):
    

    output_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info("Question extraction started for"+keyword+"at %s " %output_timestamp)
    
    qoura_question_url = find_keyword_urls(keyword)   
    count=find_questions(qoura_question_url)
    count['qoura_urls_df']['Keyword'] = keyword
    final_qoura_question_df = count['qoura_urls_df']


    final_qoura_question_df.to_csv("/home/cd_scrapers/Quora/Quora_final/questions/questions{}.csv".format(keyword))   
    # final_qoura_question_df.to_csv("questions{}.csv".format(keyword))
    
    output_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current,peak=tracemalloc.get_traced_memory()
    
    logger.info("Current memeory used "+str(current)+"Peak memory used"+str(peak))

    logger.info("Scraping finished at "+keyword+"at %s " %output_timestamp)
    
    print(final_qoura_question_df)
    return final_qoura_question_df
#if __name__ == '__main__':

#    questions("prsu")
