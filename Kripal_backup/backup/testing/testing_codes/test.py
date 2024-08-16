import ssl
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def save_html_to_file(html_content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        logger.info(f"HTML content saved to file: {file_path}")
        print(f"HTML content saved to file: {file_path}")
    except Exception as ex:
        logger.error(f"Error occurred while saving HTML content to file: {ex}")
        print(f"Error occurred while saving HTML content to file: {ex}")

def get_html(url):
    driver = None

    try:
        chrome_options = Options()
        chrome_options.add_argument("--proxy-server=http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        print("Page loaded successfully.")

        popup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'popup_element_id')))
        close_button = popup.find_element(By.CLASS_NAME, 'modal__dismiss')
        close_button.click()

        print("Popup closed successfully.")

        html_string = driver.page_source

        return html_string
    except Exception as ex:
        logger.error(f"Exception occurred: {ex}")
        print(f"Exception occurred: {ex}")
    finally:
        if driver is not None:
            driver.quit()
            print("WebDriver quit successfully.")
    
    return None

# URL to scrape
# url = 'https://www.linkedin.com/in/sayan-kundu-939b81207'
url = "https://www.quora.com/"

# Get HTML content
html_content = get_html(url)

# Save HTML content to file
if html_content:
    save_html_to_file(html_content, '/home/review_approval_dir/review_approval/reviews_auto_approval_automation/v1_18012023/linkedin_profile.html')
else:
    logger.error("Failed to retrieve HTML content")
    print("Failed to retrieve HTML content")
