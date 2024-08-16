from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading

# Setting up options for headless browsing
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


def fetch_youtube_short_details(url, index):
    try:
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the provided YouTube Shorts URL
        url = "https://www.youtube.com/shorts/HKGFtUbLGDY"
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()

        driver.find_element(By.CLASS_NAME, 'ytp-large-play-button.ytp-button').click()
        time.sleep(20)

        driver.quit()
    except:
        pass

# Set up the driver

urls = [
    "https://www.youtube.com/shorts/HKGFtUbLGDY",
    "https://www.youtube.com/shorts/HKGFtUbLGDY",
    "https://www.youtube.com/shorts/HKGFtUbLGDY",
    # Add more URLs as needed
]
for i in range(5):
    print("first time", i)
    threads = []
    for index, url in enumerate(urls):
        thread = threading.Thread(target=fetch_youtube_short_details, args=(url, index))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

