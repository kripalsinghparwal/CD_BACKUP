from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
# Python Program to Get IP Address
import socket



options = Options()
# options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# options.add_argument(f'user-agent={user_agent}')


PATH = r"C:\Users\Kripal\Desktop\testing\myenv\Lib\site-packages\chromedriver_py\chromedriver_win64.exe"
py = "127.0.0.1:24000"
#error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
#college_links = 'https://shiksha.com/college/jspm-s-jayawantrao-sawant-college-of-commerce-and-science-hadapsar-pune-138299'

# options = Options()
# options.add_argument('--proxy-server=%s' % py)
# options.add_argument('--ignore-ssl-errors=yes')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-insecure-localhost')
# # options.add_argument('headless')
# options.add_argument('--no-sandbox') 
# options.add_argument('--allow-running-insecure-content')
# options.add_argument('--window-size=1400,600')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--disable-gpu')
# options.add_experimental_option("excludeSwitches", ['enable-automation'])

sel_options = {
'proxy': {'http': 'http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225',
'https': 'http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225'},
}

# s = Service('chromedriver')
# driver = webdriver.Chrome()
# driver = webdriver.Chrome(path,options = options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver= webdriver.Chrome(PATH, seleniumwire_options=sel_options,options=options)
driver.maximize_window()
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)
# driver = webdriver.Chrome()

driver.get("https://www.justdial.com/Bangalore/Overseas-Education-Consultants/nct-10958378")
time.sleep(5)  # Allow 2 seconds for the web page to open
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "resultbox_info")))
scroll_pause_time = 10 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 3

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 3
    # driver.implicitly_wait(5)
    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "resultbox_info")))
    time.sleep(scroll_pause_time)
    
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 

data = {'Name':[],'Rating': [], 'Address': [], 'Phone': []}
soup = bs(driver.page_source, "html.parser")
centres = soup.find_all(class_="resultbox_info")
for centre in centres:
    data['Name'].append(centre.find(class_="sx-3349e7cd87e12d75 resultbox_title_anchor  line_clamp_1").get_text())
    data['Rating'].append(centre.find(class_="resultbox_totalrate").get_text())
    data['Address'].append(centre.find(class_="jsx-3349e7cd87e12d75 font15 fw400 color111").get_text())
    data['Phone'].append(centre.find(class_="jsx-3349e7cd87e12d75 callcontent callNowAnchor").get_text())

time.sleep(10)
driver.quit()
df = pd.DataFrame.from_dict(data)
df.to_csv("centres.csv", index=False)