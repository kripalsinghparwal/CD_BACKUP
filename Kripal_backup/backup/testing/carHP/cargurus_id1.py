# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# import mysql.connector
# from mysql.connector import Error
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")

# PATH = "/path/to/chromedriver.exe"


options = {
'proxy': {'http': 'http://brd-customer-hl_a4a3b5b0-zone-test_unlocker:4197l1fnslrm@brd.superproxy.io:22225',
'https': 'http://brd-customer-hl_a4a3b5b0-zone-test_unlocker:4197l1fnslrm@brd.superproxy.io:22225'},
}

driver = webdriver.Chrome(seleniumwire_options=options, options=opt)
# driver = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options)

# driver.get("https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=85070&inventorySearchWidgetType=AUTO&sortDir=ASC&sourceContext=untrackedExternal_false_0&distance=50&sortType=BEST_MATCH&entitySelectingHelper.selectedEntity=d2256")
# time.sleep(5)

# print(driver.execute_script('return document.body.innerHTML;'))
# driver.get("https://www.quora.com/")
driver.get("https://www.linkedin.com/in/sayan-kundu-939b81207")
time.sleep(25)



# driver.quit()



# Host
# brd.superproxy.io:22225
# Username
# brd-customer-hl_6d06f681-zone-city
# Password
# 6f9c0506cfab
