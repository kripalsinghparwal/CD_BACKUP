from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime
from selenium.webdriver.common.by import By
from datetime import datetime

desired_width = 320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns', 10)

options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')


# stream_list = [ 'engineering', 'accounting-commerce', 'business-management-studies', 'teaching-education',
#                'it-software',  'medicine-health-sciences',
#                'mass-communication-media', 'hospitality-travel', 'design', 'arts-fine-visual-performing',
#                'banking-finance-insurance', 'nursing', 'law', 'animation', 'architecture-planning', 'aviation',
#                'beauty-fitness', 'government-exams','humanities-social-sciences','science']

today = datetime.today()
stream_count = 0
colleges = []
er=[]
err_keyword =[]
err_url = []

df2 = pd.DataFrame(columns=['College Name', 'City', 'College Type', 'No. of Reviews', 'Website Link',
                            'Course/Program', 'Name',
                            'Fees', 'Shiksha Link'])

about_df = pd.DataFrame()

a = 700
b = 1400
print(a, b)
print("starting_time :", datetime.now())
df = pd.read_csv("/home/cd_scrapers/shiksha_reviews_project/input_folder/1381_remaining_shiksha_input_data.csv").drop_duplicates()[a:b]
print(len(df))
# college_links = df['Url'].tolist()
# unique_colleges_links = []
# for link in college_links:
#     if link not in unique_colleges_links:
#         unique_colleges_links.append(link)

# ans = zip(df.keyword,df.url)
# zipped_list = list(ans)
# inputNameAndUrlDict = dict(zipped_list)


# print(len(college_links))
# print(len(unique_colleges_links))
college_count = 1

error=pd.DataFrame()

path='/usr/bin/chromedriver'
py = "127.0.0.1:24001"
    
import ssl
import urllib.request
def scrap(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': 'http://brd-customer-hl_a4a3b5b0-zone-test_unlocker:4197l1fnslrm@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_a4a3b5b0-zone-test_unlocker:4197l1fnslrm@brd.superproxy.io:22225'}))
    response = opener.open(url)

    response_headers = response.info()
    content_type = response_headers.get('Content-Type')
    encoding = 'utf-8'  

    if content_type:
        content_type_parts = content_type.split(';')
        for part in content_type_parts:
            if 'charset=' in part:
                encoding = part.split('charset=')[-1].strip()
    html_string = response.read().decode(encoding)
    return html_string
    


# for link in unique_colleges_links[a:b]:
# for college in inputNameAndUrlDict:
#     link = inputNameAndUrlDict[college]
for c in range(len(df)):
    link = df['Url'].tolist()[c]
    college = df['Input_College Name'].tolist()[c]
    Collegedunia_id = df['Collegedunia_id'].tolist()[c]

    # Collegedunia_id = df["Collegedunia_id"].tolist()[c]
    print(link)
    time.sleep(2)

    try:
        data_list = []
        html_string = scrap(link)
        soup = BeautifulSoup(html_string, 'html.parser')
        print('\n\nStream:', stream_count, '\t\tCollege no: ', college_count)

        row_dict = dict()
        row_dict["Url"] = link
        row_dict['Collegedunia_id'] = Collegedunia_id
        row_dict["Input_College Name"] = college
        # row_dict["Collegedunia_id"] = Collegedunia_id
        
        ########### For College Name ######################################
        import json
        try:
            college_name = json.loads(soup.findAll('script', {"type" : "application/ld+json"})[0].text, strict=False)['name']
        except Exception as e:
            print("name exception :", e)     
            college_name = "N/A"
        finally:
            print('College Name : ', college_name)
            row_dict["College Name"] = college_name
    
            
        ########### For official Website Link ######################################
        import json
        try:
            official_website_link = json.loads(soup.findAll('script', {"type" : "application/ld+json"})[0].text, strict=False)["url"]
        except Exception as e:
            print("website exception :", e)     
            official_website_link = "N/A"
        finally:
            print('Official Website : ', official_website_link)
            row_dict["Official Website"] = official_website_link

        # # REVIEWS
        try:
            # review = soup.find("a", {"class": "view_rvws ripple dark"}).text.replace("(", "").replace(")", "").replace("Reviews", "")
            reviews_span = soup.find("span", class_="ce0fdc ece774 ece774")
            review = reviews_span.find("a", {"class": "ripple dark"}).text.replace("(", "").replace(")", "").replace("Reviews", "")
        except Exception as e:
            print(e)
            review = "N/A"
        finally:
            row_dict["Reviews"] = review
            print('Reviews: ',review, '\n')

    

        df3 = pd.DataFrame.from_dict(row_dict, orient='index')
        df3 = df3.transpose()
        about_df = pd.concat([about_df,df3])
        about_df.to_csv('/home/cd_scrapers/shiksha_reviews_project/output_folder/reviews{}-{}.csv'.format(a, b))
        print("time :", datetime.now())
    
        college_count += 1
        time.sleep(random.randint(3,7))
    except Exception as e :
        print("exception", e)
        print("some problem in clg link")
        # err_keyword =[]
        # err_url = []
        # err_keyword.append(Collegedunia_id)
        err_keyword.append(college)
        err_url.append(link)
        # print(link, Collegedunia_id)
        print(link, college)
        error= pd.DataFrame()
        # error['Collegedunia_id'] = err_keyword
        error['keyword'] = err_keyword
        error['Url'] = err_url
        error.to_csv('/home/cd_scrapers/shiksha_reviews_project/output_folder/shiksha_final_error{}-{}.csv'.format(a,b))
        print('Error CSV Generated')

print("ending_time :", datetime.now())



