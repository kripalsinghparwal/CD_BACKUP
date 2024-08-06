import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from pynput.keyboard import Key, Controller
import time
import chromedriver_autoinstaller
import pyautogui

#############################################################################


# Reading the Gsheet
def read_url_from_worksheet(sheet_link, worksheet_name, credentials_json_path):
    # Credentials input
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_json_path, "https://spreadsheets.google.com/feeds"
    )

    # Authenticate
    gc = gspread.authorize(credentials)

    # Open the Google Sheets document by its URL
    sh = gc.open_by_url(sheet_link)

    # Select the worksheet by name
    worksheet = sh.worksheet(worksheet_name)

    print("Reading URL from worksheet...")

    # Read data from the specified column
    column_name = "Final Doc Link"
    url_column = worksheet.col_values(worksheet.find(column_name).col)

    # Remove the column header
    url_column = url_column[1:]

    return url_column


# Modifying the url link from url_column
def modify_url(url_column):
    mod_output_url = []
    for input_url in url_column:
        parts = input_url.split("/")
        doc_id = parts[5]
        output_url = f"https://docs.google.com/document/d/{doc_id}/export?format=docx"
        mod_output_url.append(output_url)
    return mod_output_url


# saving the column of modified urls
def save_column(output_url, credentials_json_path, sheet_id, worksheet_name, cell_num):
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_json_path, SCOPES
    )

    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)

    sheet.update(
        f"{cell_num}", [[c] for c in output_url], value_input_option="USER_ENTERED"
    )


def download_url(mod_url, email, password, url):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
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
    # Select the input Email Field
    email_input = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    email_input.send_keys(email)

    # Click on Next Button
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

    # Select the input Password Field
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        )
    )
    password_input.send_keys(password)

    # Click on Next Button
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()
    time.sleep(10)

    for mod_input_url in mod_url:
        time.sleep(2)
        driver.get(mod_input_url)
        time.sleep(2)
    driver.quit()


def automate_translation(
    email,
    password,
    gsheet_url_column,
    worksheet_name,
    credentials_json_path,
    sheet_id,
    update_worksheet_name
):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
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

    # Row Count
    count = 2

    # Accesing Google Spreadsheets
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_json_path, SCOPES
    )

    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id).worksheet(update_worksheet_name)

    # Directory containing the files
    directory = (
        "C:\\Users\\tanma\\OneDrive\\Desktop\\collegedunia\\prepStudyNotes\\incomplete"
    )

    file_paths = []

    # Recursively search for files in all subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.splitext(file)[0]
            print(file_path)
            file_paths.append(file_path)

    # Open the url using Driver

    driver.get(url)

    ##################################################################################

    # Select the input Email Field
    email_input = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    email_input.send_keys(email)

    # Click on Next Button
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

    # Select the input Password Field
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        )
    )
    password_input.send_keys(password)

    # Click on Next Button
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()
    time.sleep(10)

    for file_path_name in file_paths[:]:
        # Click on "OPEN FILE PICKER
        open_file_picker_icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="docs-homescreen-open"]/div')
            )
        )
        open_file_picker_icon.click()

        time.sleep(3)

        # 'open a file' popup
        try:
            driver.switch_to.frame(6)
        except:
            driver.switch_to.frame(5)
        time.sleep(8)

        # Click on Upload Navbar
        upload_span = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="5"]'))
        )
        upload_span.click()

        # Click on browse Button
        browse_element = driver.find_element(
            By.XPATH,
            '//*[@id="yDmH0d"]/div[2]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div/button',
        )
        browse_element.click()
        time.sleep(3)

        # Enter Path name
        keyboard = Controller()
        keyboard.type(file_path_name)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        time.sleep(5)
        # wait till the new page opens
        WebDriverWait(driver, 10).until(EC.url_changes(url))
        time.sleep(10)

        pyautogui.hotkey("alt", "/")

        time.sleep(10)

        pyautogui.typewrite("Translate")
        time.sleep(2)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        time.sleep(2)
        # Click on tab and choose hindi
        pyautogui.press("tab")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        time.sleep(2)
        # Click on Hindi
        for _ in range(38):
            pyautogui.press("down")

        time.sleep(1)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        for _ in range(2):
            pyautogui.press("tab")

        time.sleep(2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        time.sleep(5)
        all_window_handles = driver.window_handles
        # Switch to new page
        driver.switch_to.window(all_window_handles[1])
        time.sleep(10)

        # pyautogui implementation to share docs public
        pyautogui.hotkey("alt", "/")
        time.sleep(5)

        pyautogui.typewrite("Share")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)

        for _ in range(2):
            pyautogui.press("tab")
        pyautogui.press("enter")

        time.sleep(2)

        for _ in range(2):
            pyautogui.press("down")

        pyautogui.press("enter")

        time.sleep(3)

        for _ in range(3):
            pyautogui.press("tab")

        pyautogui.press("enter")

        time.sleep(2)

        current_url = driver.current_url

        print(current_url)
        driver.close()

        driver.switch_to.window(all_window_handles[0])
        time.sleep(10)

        pyautogui.hotkey("alt", "left")
        time.sleep(3)

        update_range = f"D{count}"  # Adjust the range to include header

        # [url(input_url), Category(Worksheet_name),translated url, Name of the Doc]
        # Update the worksheet
        sheet.update(
            update_range,
            [[current_url]],
            value_input_option="USER_ENTERED",
        )
        count += 1

    driver.quit()

def mod_download():
    mod_url = modify_url(gsheet_url_column)
    print(mod_url)

    updated_link_cell = "C2"
    save_column(mod_url, credentials_json_path, sheet_id, worksheet_name, updated_link_cell)
    download_url(mod_url,email,password,url)


# MAIN DRIVER
###############################################################################################
# Installing Suitable chromedriver
chromedriver_autoinstaller.install()

# Main Driver Code
sheet_id = "1Obi7si1NGbMomnY4ehN273BuQzkeFMctaBM3686Uqh4"
sheet_link = "https://docs.google.com/spreadsheets/d/1Obi7si1NGbMomnY4ehN273BuQzkeFMctaBM3686Uqh4/edit#gid=2006570017"
worksheet_name = "Sheet28"
update_worksheet_name = "Sheet28"
credentials_json_path = "scienceandtech-404413-7dcb1e466d80.json"

# read gsheet
gsheet_url_column = read_url_from_worksheet(
    sheet_link, worksheet_name, credentials_json_path
)
print(gsheet_url_column)

email = "amruta.p@collegedunia.com"
password = "Pa@1234567"
url = "https://docs.google.com/document/u/0/"

# Modifying the url
# mod_url = modify_url(gsheet_url_column)
# print(mod_url)

# updated_link_cell = "C2"
# save_column(mod_url, credentials_json_path, sheet_id, worksheet_name, updated_link_cell)
# download_url(mod_url,email,password,url)

# mod_download()

automate_translation(email,password,gsheet_url_column,worksheet_name,credentials_json_path,sheet_id,update_worksheet_name)