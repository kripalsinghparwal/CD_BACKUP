from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import ActionChains, Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()
driver.get('https://timespro.com/')
time.sleep(2)
driver.maximize_window()
time.sleep
#add scroll


#BLOCK-1
data1 = {'url':[],'course':[],'category':[],'title': []}
section_id_list = ["EarlyCareerCourses", "ExecutiveEducationCourses"]
for section_id in section_id_list:
    block1 = driver.find_element(By.ID, section_id)
    soup = bs(driver.page_source, "html.parser")
    num1 = block1.find_element(By.CLASS_NAME, "css-kp6yku")
    num2 = num1.find_elements(By.CLASS_NAME, "css-kjn4di")
    time.sleep(2)

      # List to store titles

    for i in range(len(num2)):
        button=num2[i].text
        print("i" ,i, button)
        if i !=0:
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(num2[i]))
            while True:
                try:
                    num2[i].click()
                    time.sleep(5)
                    break
                except:
                    pass
        
        stage1 = block1.find_element(By.CLASS_NAME, "MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-3.css-1h77wgb")
        stage2 = stage1.find_elements(By.CLASS_NAME, "css-sjojax")
        for p in range(len(stage2)):
            # hover_element = driver.find_element(By.ID, "your_element_id")

            # Create an ActionChains object and perform the hover action
            actions = ActionChains(driver)
            actions.move_to_element(stage2[p]).perform()
            time.sleep(10)
        
            title1 = stage2[p].find_element(By.CLASS_NAME, "MuiTypography-root.MuiTypography-h3.css-18h9l83").text
            data1['title'].append(title1)  # Append titles to the list
            data1['category'].append(button)
            data1['url'].append("https://timespro.com/")
            data1['course'].append(section_id)
            print(title1)
            # print(">>>>>>>>>>", len(stage2[p].find_elements(By.TAG_NAME, 'button')), stage2[p].find_elements(By.TAG_NAME, 'button')[0].get_attribute('class'))
            # print(stage2[p].find_elements(By.TAG_NAME, 'button')[0].text)
            # while True:
            #     try:
            #         stage2[p].find_elements(By.TAG_NAME, 'button')[0].click()
            #         time.sleep(5)
            #         break
            #     except Exception as e:
            #         print(e)
            #         pass
            

# Create DataFrame
df = pd.DataFrame(data1)

# Save DataFrame to CSV
df.to_csv("titles.csv", index=True)
    
