import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui


def scrape_nta_data(url):
    QP_data = {"paperName": [], "QPLink": []}

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"chromedriver={ChromeDriverManager().install()}")

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get(url)

    # Click on Downloads menu tab
    navbarElement = driver.find_element(By.XPATH, '//*[@id="navigation"]')
    menuElement = navbarElement.find_element(By.XPATH, '//*[@id="navigation"]/ul/li[8]')
    menuElement.click()

    time.sleep(2)

    # Select year DropDown
    yearDropdown = driver.find_element(By.XPATH, '//*[@id="drpYear"]')
    yearOptions = yearDropdown.find_elements(By.XPATH, '//*[@id="drpYear"]/option')

    for yearindex in range(3, 4):
        yearOptions[yearindex].click()

        # Select Exam-Type DropDown
        examTypeDropdown = driver.find_element(By.XPATH, '//*[@id="drpExamType"]')
        examTypeOptions = examTypeDropdown.find_elements(By.XPATH, '//*[@id="drpExamType"]/option')

        driver.implicitly_wait(10)
        examTypeOptions[46].click()

        # Select Paper Dropdown
        paperDropdown = driver.find_element(By.XPATH, '//*[@id="drpPaperType"]')
        paperOptions = paperDropdown.find_elements(By.XPATH, '//*[@id="drpPaperType"]/option')

        paperOptions[1].click()

        # Click on SEARCH BUTTON
        searchButton = driver.find_element(By.XPATH, '//*[@id="btnSearch"]')
        searchButton.click()

        try:
            # Select show entries
            show_element = driver.find_element(By.XPATH, '//*[@id="tbldownload_length"]/label/select')
            showOptions = show_element.find_element(By.XPATH, '//*[@id="tbldownload_length"]/label/select/option[7]')
            showOptions.click()

            # select the Table content
            resultTable = driver.find_element(By.XPATH, '//*[@id="tbldownload"]')
            soup = BeautifulSoup(resultTable.get_attribute('outerHTML'), "html.parser")

            trs = soup.find('table').find('tbody').find_all('tr')

            for tr in trs:
                tds = tr.find_all('td')
                tds_link_element = tds[6]
                a_tag = tds_link_element.find('a')
                QP_data['paperName'].append(tds[2].text)
                if a_tag:
                    link_prefix = a_tag.get('href')
                    link = url + link_prefix
                    QP_data['QPLink'].append(link)
                else:
                    QP_data['QPLink'].append('')
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    driver.quit()
    return QP_data

def download_pdf(result_data):

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"chromedriver={ChromeDriverManager().install()}")

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    for papername,download_url in zip(result_data['paperName'],result_data['QPLink']): 
        driver.get(download_url)
        time.sleep(5)
        pyautogui.hotkey("ctrl", "s")
        time.sleep(2)
        pyautogui.typewrite(papername)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(5)
        print("Succesfully Downloaded......." + papername)


url = "https://nta.ac.in"
result_data = scrape_nta_data(url)
print(result_data)
download_pdf(result_data)


