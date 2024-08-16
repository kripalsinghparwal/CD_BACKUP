from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\browserDrivers\chromedriver-win64\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()

# Set any desired capabilities
chrome_options.add_argument("--start-maximized")

# Create the WebDriver instance with options
driver = webdriver.Chrome(options=chrome_options)
# service = Service(executable_path=PATH)
# driver = webdriver.Chrome(PATH)
url = "https://upneet.gov.in/vaccant_result/vseat_stream.aspx"
driver.get(url)

# Making the dataframe
headers = [
    "ALLOTED CANDIDATES",
    "INSTITUTE WISE ALLOTTED CANDIDATES",
    "BRANCH NAME",
    "SNO.",
    "ALLOTED UNDER CATEGORY",
    "ROLL NUMBER",
    "NAME",
    "FATHER'S NAME",
    "RANK",
    "ALLOTED DATE",
]
df = pd.DataFrame(columns=headers)

soup = BeautifulSoup(driver.page_source, "lxml")
button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_3")
link1_text = button.text
button.click()
time.sleep(5)


soup = BeautifulSoup(driver.page_source, "lxml")
links_to_visit = driver.find_element(
    By.XPATH,
    "/html/body/form/section[2]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[2]/td/div/ul",
)
links_to_visit = links_to_visit.find_elements(By.TAG_NAME, "li")
button = links_to_visit[3].find_element(By.TAG_NAME, "a")
link2_text = button.text
button.click()
time.sleep(5)
soup = BeautifulSoup(driver.page_source, "lxml")
college_name_list = soup.find(id="ctl00_ContentPlaceHolder1_DDL_Institute")
college_name_list = college_name_list.find_all("option")
college_name_list.pop(0)

# Getting text values
text_values = []
for i in college_name_list:
    text_values.append(i.text)
for option_value_i in range(len(college_name_list)):
    option_value = college_name_list[option_value_i]["value"]
    dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDL_Institute")
    select = Select(dropdown)
    select.select_by_value(option_value)
    time.sleep(5)

    button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Submit")
    button.click()
    time.sleep(5)

    final_list = []
    table = driver.find_element(By.CLASS_NAME, "TabularData")
    table_rows = table.find_elements(By.TAG_NAME, "tr")
    table_rows.pop(0)
    table_rows.pop(0)
    for i in table_rows:
        tr_list = i.find_elements(By.TAG_NAME, "td")
        temp_list = []
        temp_list.append(link1_text)
        temp_list.append(link2_text)
        for j in tr_list:
            temp_list.append(j.text)
        final_list.append(temp_list)
    for i in final_list:
        df.loc[len(df)] = i


df.to_excel("final_data3.xlsx", index=False)
