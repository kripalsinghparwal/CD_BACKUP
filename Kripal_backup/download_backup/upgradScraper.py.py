import pandas as pd
import warnings

# from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import lxml
import csv
import requests
import logging
import logging.handlers

# import pymysql
import os
import urllib3
from zoneinfo import ZoneInfo

# import tasks.uploader as uploader

# from tasks.uploader_new import *
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

warnings.filterwarnings("ignore")

import urllib.request
import random
import ssl

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time

ssl._create_default_https_context = ssl._create_unverified_context
username = "brd-customer-hl_a4a3b5b0-zone-competitor_scrapers"
password = "llnik27nifws"
port = 22225
session_id = random.random()
super_proxy_url = "http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d" % (
    username,
    session_id,
    password,
    port,
)
proxy_handler = urllib.request.ProxyHandler(
    {
        "http": super_proxy_url,
        "https": super_proxy_url,
    }
)

opener = urllib.request.build_opener(proxy_handler)
opener.addheaders = [
    (
        "User-Agent",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    )
]

# ssl._create_default_https_context = ssl._create_unverified_context
# username = 'brd-customer-hl_a4a3b5b0-zone-competitor_scrapers'
# password = 'llnik27nifws'
# port = 22225
# session_id = random.random()
# super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
#     (username, session_id, password, port))
# proxy_handler = urllib.request.ProxyHandler({
#     'http': super_proxy_url,
#     'https': super_proxy_url,
# })
# opener = urllib.request.build_opener(proxy_handler)
# opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]

news_articles = []
success = []
failure = []
scrapers_report = []


# # load_dotenv()
# now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))

# pyfilename="college_university_9"
# import sys
# # base_path = "/home/notification-scrapers"
# # base_path = "/root/New_Scrapers"
# base_path = f"{sys.argv[1]}/Cd_scrapers/"
# logging.basicConfig(
#     filename=f"{base_path}log_files/{pyfilename}.log",
#     level=logging.INFO)
# logger=logging.getLogger()
# # handler = RotatingFileHandler(f"{base_path}log_files_backup/{pyfilename}.log", maxBytes=10000,
# #                                   backupCount=1)
# # logger.addHandler(handler)

# logger.info("Code started")
# logger.info(now.strftime("%Y-%m-%d %H:%M:%S"))


PATH = "C:\browserDrivers\chromedriver-win64\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()

# Set any desired capabilities
chrome_options.add_argument("--start-maximized")

# Create the WebDriver instance with options
driver = webdriver.Chrome(options=chrome_options)


# Save this fro further review
# # Delhi Pharmaceutical Sciences and Research University
# try:
#     name = "Delhi Pharmaceutical Sciences and Research University"
#     base_url = "https://dpsru.edu.in/"
#     url = "https://dpsru.edu.in/"
#     scrapers_report.append([url, base_url, name])
#     source = driver.get(url)
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     result = soup.find("div", class_="marquee-bulletin-area")
#     a_tags = result.find_all("a")
#     for a in a_tags:
#         headline = a.text
#         link = base_url+a["href"]
#         news_articles.append((name, headline, link))
#     success.append(name)
#     driver.quit()
# except Exception as e:
#     name = "Delhi Pharmaceutical Sciences and Research University"
#     failure.append((name, e))
#     driver.quit()
# official_tag = " prepp official"

# # Territorial Army Prepp Official
# try:
#     name = "Territorial Army" + official_tag
#     url = "https://www.jointerritorialarmy.gov.in/"
#     base_url = "https://www.jointerritorialarmy.gov.in/"
#     scrapers_report.append([url, base_url, name])
#     driver.get(url)
#     time.sleep(2)
#     value = driver.find_element(
#         By.XPATH,
#         "//*/div[@class='col-xs-12 col-md-6 col-lg-6']/input[@name='captchaVal']",
#     )
#     input = value.get_attribute("value")
#     text_box = driver.find_element(
#         By.XPATH,
#         "//*/form/div[@class='row'][1]/div[@class='col-xs-12 col-md-6 col-lg-6']/div[@class='form-group has-feedback']/input[@class='form-control securityCode']",
#     )
#     text_box.send_keys(input)
#     btn = driver.find_element(
#         By.XPATH,
#         "//*/form/div[@class='row'][2]/div[@id='btnsubmit']/button[@class='btn btn-primary btn-block btn-flat']",
#     )
#     btn.click()
#     time.sleep(5)
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     mar = soup.find_all("marquee")
#     for m in mar:
#         headline = m.text.strip().replace("\n", "").replace("\xa0", "")
#         if "CLICK HERE" in headline:
#             headline = headline.replace("CLICK HERE", "")
#         try:
#             link = m.a["href"]
#         except:
#             link = url
#             pass
#         news_articles.append((name, headline, link))
#     success.append(name)

# upGrad
try:
    name = "upGrad Notice"
    base_url = "https://www.upgrad.com/blog/data-science/"
    url = base_url
    scrapers_report.append([url, base_url, name])
    source = driver.get(url)

    for i in range(67):
         button = driver.find_element(By.CSS_SELECTOR, ".inline-flex .items-center .justify-center .sm:justify-evenly .h-10 .text-sm  .text-white .font-semibold .bg-gradient-to-r .from-red-500 .to-pink-500 .rounded .xs:py-2 .xs:px-4 .upgrad-submit-btn .undefined .undefined .false")
         button.click()
         time.sleep(4)
    


    soup = BeautifulSoup(driver.page_source, "html.parser")
    content_block = list(soup.find_all("div", class_="xl:col-span-4 md:col-span-6 xs:col-span-12 sm:col-span-12 xs:mb-4 md:mb-0"))
    # head_block = content_block.find_all("div")
    for content in content_block:
        content = content.find("div")
        content = content.find_all("div")[1]
        content = content.find_all("div")[2]
        headline = content.text.strip()
        link = content.find("a")
        link = link["href"]
        if "http" not in link:
            link = base_url + link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    name = "upGrad"
    failure.append((name, e))
