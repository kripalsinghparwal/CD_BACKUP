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


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.jaroeducation.com/')
time.sleep(2)
driver.maximize_window()
time.sleep
#add scroll


#BLOCK-1  

# Create DataFrame
# df = pd.DataFrame(data1)

# # Save DataFrame to CSV
# df.to_csv("titles.csv", index=True)
    
