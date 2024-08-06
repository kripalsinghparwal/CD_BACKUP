import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime
import re
import sys 
import gspread
from google.oauth2.service_account import Credentials
import time
import requests
from urllib.parse import quote_plus

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file('cred.json', scopes=scope)
client = gspread.authorize(creds) 
sh = client.open('top colleges')
sheet = sh.worksheet('2800 colleges')
result = list()
result = sheet.get_all_records()
#driver = webdriver.Firefox(executable_path=r"C:\Users\Collegedunia\Downloads\geckodriver")

for i in range(0,len(result)):
    row_num=i+2
    url=result[i]['url']
    print(url, row_num)
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
##  CD Article Updation date
    try:
        updation_date=soup.find("div",{"class":"jsx-1464089517 pl-2 d-inline-block"}).find_all('p')[1].text.split('|')[1].split('-')[1].strip()
    except:
        updation_date='no'
    sheet.update_cell(row_num, 10, updation_date)
    
## CD Notification needs to be updated or not
    try:
        noti_date=soup.find("div",{"class":"jsx-4121031439 alerts-upate"}).find_all('li')[0].text.split(':')[0].strip()
        resp = parse(noti_date, fuzzy_with_tokens=True)
        noti_date1=resp[0].date()
        
        tod = datetime.datetime.now()
        d = datetime.timedelta(days = 7)
        one_week_ago = (tod - d).date()

        if noti_date1<one_week_ago:
            sheet.update_cell(row_num, 9, "Update")
        else:
            sheet.update_cell(row_num, 9, "No need")
    except:
        sheet.update_cell(row_num, 9, "N.A")
        pass
    
## Competitor News
    try:
        url1=result[i]['Shiksha']
        headers = { 'Accept-Language' : 'en-US,en;q=0.9','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        resp = requests.get(url1, headers = headers)
        soup1 = BeautifulSoup(resp.text, 'html.parser')
        try:
            headline = soup1.find('p',class_='latestArticle').text
            sheet.update_cell(row_num, 12, headline)
        except:
            pass
## Competitor Intro       
        try:
            comp_intro=soup1.find("div", {"class":"authorInfo"}).find_next_siblings('div')[0].find('p').text
            sheet.update_cell(row_num, 13, comp_intro)
        except:
            pass
## Competitor Article Updation date
        try:
            comp_article_date=soup1.find('div',class_='post-date').text.split('Updated on ')[1]
            sheet.update_cell(row_num, 11, comp_article_date)
        except:
            pass
    except:
        pass
