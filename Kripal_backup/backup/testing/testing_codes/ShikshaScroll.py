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

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down by 500 pixels
        driver.execute_script("window.scrollTo(0, window.scrollY + 500);")
        
        # Wait to load the next content
        time.sleep(1.5)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height, last_height)
        # if new_height == last_height:
        #     break
        if len(driver.find_elements(By.CLASS_NAME, "button.load-more-btn")) != 0:
            try:
                driver.find_element(By.CLASS_NAME, "button.load-more-btn").click()
                time.sleep(1)
            except:
                pass
        else:
            print("scroll and load more completed")
            break

        
        
        last_height = new_height

   
    listing_wrap = soup.find(class_="ctpSrp-contnr")
    inside = listing_wrap.find(class_='rspnsv-grid')

    title_links = []

    if inside:
        colleges = inside.find_all(class_="_1822 _0fc7 _7efa")
        for college in colleges:
            try:

                data0 = college.find('div', class_='_8165')
                data1 = data0.find('div',class_='_2cd2')
                data2 = data1.find('div', class_='c8ff')


                if data2:
                    try:
                        title_link = college.find('div', class_='ripple dark').find('a')['href']
                        title_links.append(title_link)
                    except:
                        title_links.append('None')
                else:
                    title_links.append('None')
            except:
                title_links.append('None')

    #For name
                
    layers = inside.find_all(class_="_1822 _0fc7 _7efa")

    for layer in layers:

        name = layer.find('div',class_='_8165')
        name1 = name.find('div',class_='c8ff')
        name2 = name1.find('a',class_='ripple dark')
        name3 = name2.find('h3').text.strip()





    # for title_link in title_links:
    #     driver.get(title_link)
    #     time.sleep(1) 

    #     soup = BeautifulSoup(driver.page_source, 'html.parser')

    #     # FOR PHONE NUMBER
    #     consultant_element = soup.find('div', class_='overview')
    #     try:
    #         consultant_business = consultant_element.find('div', class_='business')
    #         consultant_name = consultant_business.find('div', class_='name')
    #         consultant_data = consultant_name.find('div', class_='data')
    #         if consultant_data:

    #             consultant_mobile = (consultant_data.find('div', class_='mobile').find('a')['href']) or (consultant_data.find('ul', class_='mobile-group').find('a').text)
    #             phone_number = consultant_mobile
    #         else:
    #             phone_number = ''

    #         # FOR EMAIL
    #         try:
    #             consultant_presence = soup.find('div', class_='social-presence').find('a').text.strip()

    #             if consultant_presence:
    #                 email = consultant_presence
    #             else:
    #                 email = ''
    #         except:
    #             email = ''
                
    #         # FOR WEBSITE
    #         try:
    #             consultant_presence1 = soup.find('div', class_='social-presence').find('span').text.strip()

    #             if consultant_presence1:
    #                 website = consultant_presence1
    #             else:
    #                 website = '' 
    #         except:
    #             website = ''
    #     except:
    #         phone_number = ''
    #         email = ''
    #         website = ''



        college_item = {
            'Name Of University':name3,
              }
    
        data.append(college_item)

    driver.quit()
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
