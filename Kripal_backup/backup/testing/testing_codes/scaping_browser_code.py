from selenium.webdriver import Remote, ChromeOptions  
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection  
from selenium.webdriver.common.by import By  
from bs4 import BeautifulSoup
  
# AUTH = 'USER:PASS'  
SBR_WEBDRIVER = "https://brd-customer-hl_a4a3b5b0-zone-scraping_browser2:i3a7jd8i1cf3@brd.superproxy.io:9515"
# SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'  
  
def main():  
    print('Connecting to Scraping Browser...')  
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')  
    with Remote(sbr_connection, options=ChromeOptions()) as driver:  
        print('Connected! Navigating...')  
        driver.get('https://www.shiksha.com/studyabroad/usa/mba-colleges-dc-8')  
        print('Taking page screenshot to file page.png')  
        driver.get_screenshot_as_file('./page.png')  
        print('Navigated! Scraping page content...')  
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(soup)  
  
# if _name_ == '_main_':  
main()
