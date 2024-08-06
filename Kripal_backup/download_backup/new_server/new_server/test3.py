from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import openpyxl
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')


username = 'studyabroadops@collegedunia.com'
password = 'Collegeduni@123'

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.coursefinder.ai/")

    login_pg = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/div/ul/li[2]/a")))
    login_pg.click()

    username_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

    path = r"/inp/part_15_16.xlsx"
    op_path = r"/oup/part15_16Output.xlsx"

    df = pd.read_excel(path)
    # df = d[796:799]
    data = []
    for idx, row in df.iterrows():
        arr = {}
        link = row[14]
        print("Working on Row {}".format(idx), link)
        
        try:
            driver.get(link)
            body = wait.until(EC.presence_of_element_located((By.ID, 'divMiddle')))
            data_containers = body.find_elements(By.CSS_SELECTOR,
                                                 '.panel-body.padding-left-0.padding-right-0.padding-bottom-0')

            heading_container = body.find_elements(By.CSS_SELECTOR, '.panel-heading.font-bold.text-white')
            body1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-lg-3.col-md-4.col-sm-12.text-center')))
            try:
                uni_div = body1.find_element(By.CSS_SELECTOR, '.padding-20.mb-m-10')
                uni_url = uni_div.find_element(By.TAG_NAME, 'a').get_attribute("href")
            except Exception as e:
                uni_url ="N/A"
                print(e)
            arr["univeristy_url"] = uni_url
            for idxx, dc in enumerate(data_containers):
                temp_dc = dc.find_elements(By.TAG_NAME, 'li')
                for i in temp_dc:
                    div_ele = i.find_elements(By.TAG_NAME, 'div')
                    if len(temp_dc) == 1:
                        key_text = heading_container[idxx].text
                        value_text = div_ele[1].text
                        if key_text in arr:
                            arr[key_text] = value_text
                        else:
                            arr[key_text] = value_text
                    else:
                        try:
                            key_text = div_ele[1].text
                            value_text = div_ele[2].text
                            if key_text in arr:
                                arr[key_text].append(value_text)
                            else:
                                arr[key_text] = []
                                arr[key_text].append(value_text)
                        except:
                            key_text = heading_container[idxx].text
                            value_text = value_text = div_ele[1].text
        except TimeoutException:
            arr["Error"] = "Page not found"
        print(arr)
        data.append(arr)
finally:
    additional_df = pd.DataFrame(data)
    # df.reset_index(drop=True, inplace=True)
    merged_df = pd.concat([df, additional_df], axis=1)
    merged_df.to_excel(op_path)
    print("Data Saved")
    driver.quit()


