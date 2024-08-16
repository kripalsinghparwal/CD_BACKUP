import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

df = pd.read_csv('quora.csv')
Status = []
n = len(df['URL'])
for i in range(n):
    try:
        driver = webdriver.Chrome()
        driver.get(df['URL'][i])
        time.sleep(5)
        soup = bs(driver.page_source, 'html.parser')
        title = soup.find('title').get_text()
        url = driver.current_url
        if title == 'Error':
            Status.append('Page Not Found')
        elif 'unanswered' in url:
            Status.append('Unanswered')
        else:
            Status.append('Page answered working')
        time.sleep(2)
    except:
        continue
    finally:
        driver.quit()

with open("status.txt", "w") as txt_file:
    for line in Status:
        txt_file.write(line + "\n")

print(len(Status))
df2 = df.assign(Status=Status)
df2.to_csv('quora_status.csv', index=False)