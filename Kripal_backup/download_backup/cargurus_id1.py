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
import mysql.connector
from mysql.connector import Error
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")

# PATH = "/path/to/chromedriver.exe"

# options = {
# 'proxy': {'http': 'http://brd-customer-hl_6d06f681-zone-city:6f9c0506cfab@brd.superproxy.io:22225',
# 'https': 'http://brd-customer-hl_6d06f681-zone-city:PASSWORD@brd.superproxy.io:22225'},
# }
options = {
'proxy': {'http': 'http://brd-customer-hl_6d06f681-zone-city:6f9c0506cfab@brd.superproxy.io:22225',
'https': 'http://brd-customer-hl_6d06f681-zone-city:6f9c0506cfab@brd.superproxy.io:22225'},
}
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), seleniumwire_options=options, options=opt)
# chrome = webdriver.Chrome(PATH, seleniumwire_options=options)
driver.header_overrides = {

}
driver.get("https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=85070&inventorySearchWidgetType=AUTO&sortDir=ASC&sourceContext=untrackedExternal_false_0&distance=50&sortType=BEST_MATCH&entitySelectingHelper.selectedEntity=d2256")

print(driver.execute_script('return document.body.innerHTML;'))
time.sleep(5)

# Python Program to Get IP Address
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

driver.quit()



# Host
# brd.superproxy.io:22225
# Username
# brd-customer-hl_6d06f681-zone-city
# Password
# 6f9c0506cfab
