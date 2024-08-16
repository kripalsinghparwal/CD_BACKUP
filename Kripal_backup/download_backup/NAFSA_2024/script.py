from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
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

tracemalloc.start()

#code by pythonjar, not me to prevent notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)


# logging.basicConfig(filename = r"C:\Users\Kripal\Downloads\NAFSA_2024\log",level=logging.INFO)
# logger=logging.getLogger()
 

options = Options()
# options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

    
def getting_data(url):#To get the html content of the answers and views of each question
    try:
        row_dict_list = []
        main_df = pd.DataFrame()
        path='/usr/bin/chromedriver'
        # driver = webdriver.Chrome(executable_path=path,options=options)
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(7)
        driver.find_element(By.CLASS_NAME, "btn.btn-link.pull-right").click()
        time.sleep(2)
        login_wrap = driver.find_element(By.CLASS_NAME, "login-wrap")
        login_wrap.find_element(By.ID, "AccountEmail").send_keys("sanjay.meena@collegedunia.com")
        login_wrap.find_element(By.ID, "AccountKey").send_keys("101263")
        time.sleep(2)
        login_wrap.find_element(By.CLASS_NAME, "btn.btn-primary.btn-block").click()
        time.sleep(2)
        all_user_group = driver.find_element(By.CLASS_NAME, "list-group.list-view")
        india_user = all_user_group.find_elements(By.TAG_NAME, "li")[0]
        
        time.sleep(2)
        print("logged in")
        # driver.save_screenshot("ss.png")
        # driver.quit()
        all_user_group = driver.find_element(By.CLASS_NAME, "list-group.list-view")
        india_user_group = all_user_group.find_elements(By.TAG_NAME, "li")[0]
        india_user_group.click()
        time.sleep(2)
        users_list_data = all_user_group.find_element(By.CLASS_NAME, "bucketwrapper").find_elements(By.TAG_NAME, "li")

        count = 1
        for i in users_list_data:
            temp_df = pd.DataFrame()
            social_media_links = []
            pop_up_text = "N/A"
            attendee_email = "N/A"

            row_dict = {}
            print("count ", count)
            # driver.save_screenshot(f"test{count}.png")
            try:
                i.click()
                time.sleep(3)
                # driver.save_screenshot(f"{count}ss.png")
                try:
                    social_media_element = driver.find_element(By.CLASS_NAME, "socialmedia")
                    handles_list = social_media_element.find_elements(By.TAG_NAME, 'a')
                    for handle in handles_list:
                        print(handle.get_attribute("href"))
                        social_media_links.append(handle.get_attribute("href"))
                except Exception as e:
                    print(e)
                    social_media_links = []
                finally:
                    row_dict['social_media_links'] = social_media_links
                    temp_df['social_media_links'] = social_media_links
                try:
                    pop_up_text = driver.find_element(By.CLASS_NAME, "col-xs-12.col-md-9").text
                except Exception as e:
                    print(e)
                    pop_up_text = "N/A"
                finally:
                    row_dict['Info'] = pop_up_text
                    temp_df['Info'] = pop_up_text
                # try:
                #     for x in driver.find_element(By.CLASS_NAME, "col-xs-12.col-md-9").find_elements(By.CLASS_NAME, "popup-mode-line-item"):
                #         print(x.text)
    
                # except Exception as e:
                #     print(e)
                pop_up_header = driver.find_element(By.CLASS_NAME, "popup_header")
                pop_up_header_toolbar = pop_up_header.find_element(By.CLASS_NAME, "popup_header_toolbar")
                pop_up_tools = pop_up_header_toolbar.find_elements(By.TAG_NAME, "li")
                try:
                    for tool in pop_up_tools:
                        if tool.text.strip() == 'Email':
                            tool.click()
                            time.sleep(2)
                            # driver.save_screenshot(f"{count}ss3.png")
                            attendee_email = driver.find_element(By.CLASS_NAME, "popup_content").find_element(By.CLASS_NAME, "col-xs-12.col-sm-6").find_elements(By.TAG_NAME, 'input')[1].get_attribute('value')
                            print("email ", attendee_email)
                            # row_dict['email'] = attendee_email
                            driver.find_element(By.CLASS_NAME, "glyphicon.glyphicon-remove").click()
                            time.sleep(5)
                            print("coming here")
                            # print(">>>row_dict", row_dict)
                except Exception as e:
                    print("email exception ", e)
                    # attendee_email = "N/A"
                finally:
                    row_dict['email'] = attendee_email
                    temp_df['email'] = attendee_email

                # print("row_dict", row_dict)
                # row_dict_list.append(row_dict)
                # print("row_dict_list", row_dict_list)
                # df = pd.DataFrame(row_dict_list)
                
                # # df = pd.DataFrame.from_dict(row_dict, orient='index')
                # print(df)
                # # df = df.transpose()
                # main_df = pd.concat([main_df,df])
                # # main_df = pd.concat([main_df,temp_df])
                # print("main_df", main_df)
                # main_df.to_csv(f'/home/cd_scrapers/NAFSA_2024/output_folder/data.csv')
                try:
                    driver.find_element(By.CLASS_NAME, "glyphicon.glyphicon-remove").click()
                except Exception as e:
                    pass
                count +=1


            except Exception as e:
                print("exception 1",e)
                count +=1
            finally:
                print("row_dict", row_dict)
                row_dict_list.append(row_dict)
                print("row_dict_list", row_dict_list)
                df = pd.DataFrame(row_dict_list)
                
                # df = pd.DataFrame.from_dict(row_dict, orient='index')
                print(df)
                # df = df.transpose()
                # main_df = pd.concat([main_df,df])
                # main_df = pd.concat([main_df,temp_df])
                print("df", df)
                df.to_csv('C:\\Users\\Kripal\\Downloads\\NAFSA_2024\\output_folder')
    except Exception as e:
        print("driver exception", e)
    driver.quit()
            
            
if __name__ == "__main__":
    print("starting time :", datetime.datetime.now())
    main_df = pd.DataFrame()
    getting_data("https://nafsa2024.eventscribe.net/Userlist.asp?hla=1&goToLetter=I&bucket=Country&pfp=UserList")

