from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime
from selenium.webdriver.common.by import By

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

df2 = pd.DataFrame(columns=['College Name', 'City', 'College Type', 'No. of Reviews', 'Website Link',
                            'Course/Program', 'Name',
                            'Fees', 'Shiksha Link'])

about_df = pd.DataFrame()

#df2.to_csv(f'/root/Documents/rohini/shiksha/shiksha_colleges_data_{today.month}.csv')
#df2.to_csv('C:/Users/Somya/Desktop/Shiksha/shiksha_colleges_data_{today.month}.csv')
#df2.to_csv("file.csv")

#df = pd.read_csv('C:/Users/Somya/Desktop/Shiksha/college_list_2.csv')
# df = pd.read_csv('/root/shiksha/final_work/pending_colleges.csv')
df = pd.read_csv(r'C:\Users\Kripal\Desktop\testing\input_folder\colleges_data.csv')
#df = pd.read_csv('college_list_1.csv')
college_links = df['Url'].tolist()
unique_colleges_links = []
for link in college_links:
    if link not in unique_colleges_links:
        unique_colleges_links.append(link)


print(len(college_links))
print(len(unique_colleges_links))
college_count = 1

error=pd.DataFrame()

path='/usr/bin/chromedriver'
py = "127.0.0.1:24000"
#error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
#college_links = 'https://shiksha.com/college/jspm-s-jayawantrao-sawant-college-of-commerce-and-science-hadapsar-pune-138299'

options = Options()
# options.add_argument('--proxy-server=%s' % py)
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
# options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

def scrap(link):

    driver = webdriver.Chrome(path,options = options)    
    driver.get(link)
    time.sleep(2)
    if "Access Denied" in driver.page_source:
        print("failed")
        driver.quit()
        scrap(link)
    else:
        print("success")
        return driver
    
a = 1000
b = 2000

for link in unique_colleges_links[a:b]:  
    #error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
    #path = 'C:/Users/Somya/Downloads/chromedriver_win32/chromedriver.exe'  
    # options = Options()
    # options.add_argument('--proxy-server=%s' % py)
    # options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-insecure-localhost')
    # options.add_argument('headless')
    # options.add_argument('--no-sandbox') 
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument('--window-size=1400,600')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--disable-gpu')
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # driver = webdriver.Chrome(path,options = options)    
    # driver = webdriver.Chrome(path,options=options)
    try:
        data_list = []
        # driver.get(link)
        print(link)
        driver = scrap(link)
        print(">>>>>>>>>>>>", driver.page_source)

        driver.maximize_window()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print('\n\nStream:', stream_count, '\t\tCollege no: ', college_count)

        row_dict = dict()
    
        try:
            # college_link = driver.find_element_by_css_selector('.facts_table').find_element_by_css_selector(
            #     '.hide').find_element_by_tag_name('a').get_attribute('href')
            college_link = driver.find_element(By.CSS_SELECTOR, '.facts_table').find_element(By.CSS_SELECTOR, '.hide').find_element(By.TAG_NAME, 'a').get_attribute('href')
            print("not found")
        except Exception as e:
            college_link = 'N/A'
        finally:
            row_dict["Website Link"] = college_link
            print('Website Link: ', college_link)
            
        ################## For college/university name ##############################    
        try:
            # college_name = driver.find_element_by_css_selector(
            #     '.text-cntr.clg_dtlswidget').find_element_by_tag_name('h1').text
            college_name = driver.find_element(By.CSS_SELECTOR, '.text-cntr.clg_dtlswidget').find_element(By.TAG_NAME, 'h1').text
        except Exception as e:
            print(e)
            college_name = 'N/A'
            print('College Name: not available!')
        finally:
            row_dict["College Name"] = college_name
            print("college_name :", college_name)

        ################### For college/university location #########################
        try:
            city = soup.find('span', class_='ilp-loc').get_text().lstrip()
        except Exception as e:
            print(e)
            city = 'N/A'
            print('City: not available!')
        finally:
            row_dict["Location"] = city
            print('City: ', city)

        ################## For comments/Q&A section #################################
        try:
            comment_count = soup.find('i', class_='examqstn-ico-v2').parent.text
        except Exception as e:
            print(e)
            comment_count = "N/A"
        finally:
            row_dict["QnA"] = comment_count
            print("comments :", comment_count)

        # try:
        #     table = soup.find('table', class_='_895c')
        #     table_body = table.find('tbody')
        #     rows = table_body.find_all('tr')
        #     cols = rows[1].find_all('td')
        #     college_type= cols[1].get_text()
        #     time.sleep(random.randint(1,3))
        # except Exception as e:
        #     college_type = 'N/A'
        #     print(e)
        #     print('Type not available!')
        # finally:
        #     print("college_type :",  college_type)

        ########### For Updated On Date ##########################################
        try:
            updated_on = soup.find("div", {"class":"post-date"}).text
        except Exception as e:
            updated_on = "N/A"
        finally:
            print("updated on ", updated_on)        
        
        ############### For Intoduction of college or university ############
        try:
            comp_intro=soup.find("div", {"class":"authorInfo"}).find_next_siblings('div')[0].find('p').text
        except Exception as e:
            comp_intro = "N/A"
        finally:
            print("competitor intro", comp_intro)

        ############## Latest notification or headline ##################
        try:
            headline = soup.find('div',class_='latestArticleWrapper').text
        except Exception as e:
            headline = "N/A"
        finally:
            print("hedline", headline)

        ############# cutoff section ####################################
        try:
            cutoff = soup.find('section', {"id": "ovp_section_cutoff"}).text
        except Exception as e:
            cutoff = "N/A"
        finally:
            print("cutoff", cutoff)

        ############# Highlight section ###############################################
        try:
            highlight_section = soup.find('section', {"id" : "ovp_section_highlights"}).find('table')
            if highlight_section is None:
                highlight_section = soup.find('div', class_="abtSection").find('table')
            table_rows = highlight_section.find_all('tr') 
            ls = []
            for row in table_rows[1:]:
                row_dict[row.findAll('td')[0].text.strip()] = row.findAll('td')[1].text.strip()
                ls.append(row.findAll('td')[0].text.strip() + ' : ' + row.findAll('td')[1].text.strip())
            highlists = '\n'.join(ls)
                 
        except Exception as e:
            highlists = "N/A"
            print(e)
        finally:
            print("highlists :", highlists)

        ########### Alumini Section ####################################################
        try:
            alumini_section = soup.find('section', {'id': "ovp_section_notable_alumni"})
            alumini_rows = alumini_section.findAll('tr')
            for row in alumini_rows:
                alumini_columns = row.findAll("td")
                if len(alumini_columns) != 0:
                    print("alumini_text :", alumini_columns[0].text.strip())
                    print("alumini_image :",alumini_columns[1].find('div', class_="figure").find('picture').find('source')['data-originalset'])
        except Exception as e:
            print(e)

        ####################################### Scholarship Section ##########################
        try:
            driver.get(link + "/scholarships")
            scholarship_soup = BeautifulSoup(driver.page_source, 'html.parser')
            scholarship_section = scholarship_soup.find("section", {"id": "scholarships"})
            scholarship_container = scholarship_section.find("div", class_="_subcontainer scholarshipData")
            scholarship_divs = scholarship_container.findAll('div', class_="sch-div")
            for div in scholarship_divs:
                print('scholarship_number :', div.find('label').text)
                print('scholarship_text :',div.find('p').text)
        except Exception as e:
            print(e)

        df3 = pd.DataFrame.from_dict(row_dict, orient='index')
        df3 = df3.transpose()
        about_df = pd.concat([about_df,df3])
        about_df.to_csv(r'C:\Users\Kripal\Desktop\testing\output_folder\about{}-{}.csv'.format(a, b))

    
        college_count += 1
        driver.delete_all_cookies()
        time.sleep(random.randint(3,7))
        driver.quit()
    except Exception as e :
        print("exception", e)
        print("some problem in clg link")
        err =[]
        err.append(link)
        print(link)
        er.append(err)
        error= pd.DataFrame(er)
        error.to_csv(r'C:\Users\Kripal\Desktop\testing\output_folder\shiksha_final_error.csv')
        #error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
        print('Error CSV Generated')
        driver.quit()




