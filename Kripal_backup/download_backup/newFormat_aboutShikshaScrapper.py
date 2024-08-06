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

a = 22500
b = 25000
df = pd.read_csv("/home/cd_scrapers/shiksha_vs_collegedunia/input_folder/colleges_data.csv").drop_duplicates()[a:b]

# college_links = df['Url'].tolist()
# unique_colleges_links = []
# for link in college_links:
#     if link not in unique_colleges_links:
#         unique_colleges_links.append(link)

ans = zip(df.Name,df.Url)
zipped_list = list(ans)
inputNameAndUrlDict = dict(zipped_list)


# print(len(college_links))
# print(len(unique_colleges_links))
college_count = 1

error=pd.DataFrame()

path='/usr/bin/chromedriver'
py = "127.0.0.1:24000"
#error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
#college_links = 'https://shiksha.com/college/jspm-s-jayawantrao-sawant-college-of-commerce-and-science-hadapsar-pune-138299'

options = Options()
options.add_argument('--proxy-server=%s' % py)
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
options.add_argument('headless')
options.add_argument('--no-sandbox') 
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1400,600')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

def scrap(link):

    driver = webdriver.Chrome(path,options = options)    
    driver.get(link)
    time.sleep(5)
    if "Access Denied" in driver.page_source:
        print("failed")
        driver.quit()
        scrap(link)
    else:
        print("success")
        return driver
    


# for link in unique_colleges_links[a:b]:
for college in inputNameAndUrlDict:
    link = inputNameAndUrlDict[college]
    print(link)
    time.sleep(2)
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
        # print(link)
        driver = scrap(link)
        # print(">>>>>>>>>>>>", driver.page_source)

        driver.maximize_window()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print('\n\nStream:', stream_count, '\t\tCollege no: ', college_count)

        row_dict = dict()
        row_dict["Url"] = link
        row_dict["College Name"] = college
    
        # try:
        #     # college_link = driver.find_element_by_css_selector('.facts_table').find_element_by_css_selector(
        #     #     '.hide').find_element_by_tag_name('a').get_attribute('href')
        #     college_link = driver.find_element(By.CSS_SELECTOR, '.facts_table').find_element(By.CSS_SELECTOR, '.hide').find_element(By.TAG_NAME, 'a').get_attribute('href')
        #     print("not found")
        # except Exception as e:
        #     college_link = 'N/A'
        # finally:
        #     row_dict["Website Link"] = college_link
        #     print('Website Link: ', college_link)
            
        ########### For official Website Link ######################################
        import json
        try:
            official_website_link = json.loads(soup.findAll('script', {"type" : "application/ld+json"})[0].text, strict=False)['url']
        except Exception as e:
            print("website exception :", e)     
            official_website_link = "N/A"
        finally:
            print('Official Website : ', official_website_link)
            row_dict["Official Website"] = official_website_link

        ########### For College/University Address ######################################
        import json
        try:
            address = json.loads(soup.findAll('script', {"type" : "application/ld+json"})[0].text, strict=False)['address']
        except Exception as e:
            print("website exception :", e)     
            address = "N/A"
        finally:
            print('Address: ', address)
            row_dict["Address"] = address


        ################## For college/university name ##############################    
        try:
            college_head = soup.find("div", class_="b876 three_col uilp reverse_two_col").find("h1", class_="e70a13").text
        except Exception as e:
            print(e)
            college_head = 'N/A'
            print('College Headline: not available!')
        finally:
            row_dict["College Head"] = college_head
            print("college_head :", college_head)

        ################### For college/university location #########################
        try:
            city = soup.find('span', class_='_7164e4 ece774 ece774').text.strip()
        except Exception as e:
            print(e)
            city = 'N/A'
            print('City: not available!')
        finally:
            row_dict["Location"] = city
            print('City: ', city)

        ################## For comments/Q&A section #################################
        try:
            comment_count = soup.find('span', class_='_318533').find("a").text
        except Exception as e:
            print(e)
            comment_count = "N/A"
        finally:
            row_dict["QnA"] = comment_count
            row_dict["QnA Link"] = link + "/questions"
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
            updated_on = soup.find("span", class_="_0a9d _1452").text.strip()
        except Exception as e:
            updated_on = "N/A"
        finally:
            row_dict["Updated On"] = updated_on
            print("updated on ", updated_on)        
        
        # ############### For Intoduction of college or university ############
        # try:
        #     comp_intro=soup.find("div", {"class":"authorInfo"}).find_next_siblings('div')[0].find('p').text
        # except Exception as e:
        #     comp_intro = "N/A"
        # finally:
        #     row_dict['Competitor Intro'] = comp_intro
        #     print("competitor intro", comp_intro)

        ############## Latest notification or headline ##################
        try:
            headlines_list = []
            for head in soup.find("div", {"aria-label": "latestArticles"}).findAll("div", class_="_003c"):
                headlines_list.append(head.find("div", class_="_1cb3").text.strip() + " : " + head.find("div", class_="_05ef").text.strip())
            headline = "\n".join(headlines_list)
        except Exception as e:
            headline = "N/A"
        finally:
            row_dict["Headlines"]=headline
            print("hedline", headline)

        # ############# cutoff section ####################################
        # try:
        #     cutoff = soup.find('section', {"id": "ovp_section_cutoff"}).text
        # except Exception as e:
        #     cutoff = "N/A"
        # finally:
        #     print("cutoff", cutoff)

        ############## Overview Section ###########################################
        try:
            overview = soup.find('div', {"id" : "ovp_section_highlights"}).find("div", class_="_24f3").find("p").text.strip()
        except Exception as e:
            print("first overview exception :", e)
            try:
                overview = soup.find("div", class_="wikiContents _021e collapsed ca53 _5333 a78b wikiIntro").find("div", class_="_24f3").find("p").text.strip()
                if overview.startswith("What's new"):
                    overview = "N/A"
            except Exception as e:
                print("second overview exception :", e)
                overview = "N/A"
        finally:
            row_dict["Overview"] = overview

        ################ Extra Information  ###########################################
        try:
            item_list = []
            for list_item in soup.find("ul", class_="e1a898").findAll("li"):
                item_list.append(list_item.text)
            extra_info_list = "\n".join(item_list)
        except Exception as e:
            print("extra_info_list exception :", e)
            extra_info_list = "N/A"
        finally:
            row_dict["Listed Info"] = extra_info_list


        ############# Highlight section ###############################################
        highlight_dict = dict()
        try:
            about_section = soup.find("div", class_="paper-card boxShadow baac")
            if about_section is not None:
                highlight_section_1 = about_section.find("table")
                if highlight_section_1 is not None:
                    table_rows = highlight_section_1.find_all('tr') 
                    # ls_1 = []
                    for row in table_rows:
                        try:
                            highlight_dict[row.findAll('td')[0].text.strip()] = row.findAll('td')[1].text.strip()
                            # ls_1.append(row.findAll('td')[0].text.strip() + ' : ' + row.findAll('td')[1].text.strip())
                        except Exception as e:
                            pass
                            print("table exception :", e)
                    # highlights_1 = '\n'.join(ls_1)

            highlight_section_2 = soup.find('div', {"id" : "ovp_section_highlights"})
            if highlight_section_2 is not None:
                highlight_section_2 = highlight_section_2.find('table')


                if highlight_section_2 is None:
                    highlight_section_2 = soup.find('div', class_="abtSection").find('table')
                table_rows = highlight_section_2.find_all('tr') 
                # ls_2 = []
                for row in table_rows:
                    try:
                        if row.findAll('td')[0].text.strip().lower() == "website":
                            highlight_dict[row.findAll('td')[0].text.strip()] = row.findAll('td')[1].find('a')['href']
                            # ls_2.append(row.findAll('td')[0].text.strip() + ' : ' + row.findAll('td')[1].find('a')['href'])
                        else:
                            highlight_dict[row.findAll('td')[0].text.strip()] = row.findAll('td')[1].text.strip()
                            # ls_2.append(row.findAll('td')[0].text.strip() + ' : ' + row.findAll('td')[1].text.strip())
                    except Exception as e:
                        pass
                        print("table exception :", e)
                # highlights_2 = '\n'.join(ls_2)      
        except Exception as e:
            # highlights_1 = "N/A"
            # highlights_2 = "N/A"
            highlights = "N/A"
            print(e)
        finally:
            print("highlights :", highlight_dict)
            row_dict["Highlights"] = highlight_dict

        # ########### Alumini Section ####################################################
        # try:
        #     alumini_section = soup.find('section', {'id': "ovp_section_notable_alumni"})
        #     alumini_rows = alumini_section.findAll('tr')
        #     for row in alumini_rows:
        #         alumini_columns = row.findAll("td")
        #         if len(alumini_columns) != 0:
        #             print("alumini_text :", alumini_columns[0].text.strip())
        #             print("alumini_image :",alumini_columns[1].find('div', class_="figure").find('picture').find('source')['data-originalset'])
        # except Exception as e:
        #     print(e)

        # ####################################### Scholarship Section ##########################
        # try:
        #     driver.get(link + "/scholarships")
        #     scholarship_soup = BeautifulSoup(driver.page_source, 'html.parser')
        #     scholarship_section = scholarship_soup.find("section", {"id": "scholarships"})
        #     scholarship_container = scholarship_section.find("div", class_="_subcontainer scholarshipData")
        #     scholarship_divs = scholarship_container.findAll('div', class_="sch-div")
        #     for div in scholarship_divs:
        #         print('scholarship_number :', div.find('label').text)
        #         print('scholarship_text :',div.find('p').text)
        # except Exception as e:
        #     print(e)

        # REVIEWS
        try:
            driver = scrap(link + "/reviews")
            driver.maximize_window()
            time.sleep(2) 
            review_soup = BeautifulSoup(driver.page_source, 'html.parser')           
            review_table = review_soup.find('div', class_='getAllrvws')
            verified_review = review_table.text.split('.')[-2].lstrip().split(',')[1].lstrip().split(' ')[0]
            published_review = review_table.text.split('.')[-2].lstrip().split(',')[0].lstrip().split(' ')[2]
            review = "verified_review: " + verified_review + "& Published Review: " + published_review
            # print('Reviews: ',review, '\n')

            #published_review = review_table.text.split('.')[-2].lrstrip().split(',')[0].lstrip().split(' ')[2]
            #print('Published_Reviews:',published_review,'\n')   
            time.sleep(1)
        except Exception as e:
            print(e)
            try:
                review = review_table.text.split('.')[-2].lstrip().split(',')[0].lstrip().split(' ')[1]
            except:
                review = 'N/A'            
                print('Reviews not available!\n')
        finally:
            row_dict["Reviews"] = review
            print('Reviews: ',review, '\n')

        ############### Ratings #########################################
        try:
            ratings = review_soup.find("div", class_="rvwScore").find("h3").text
        except Exception as e:
            print("Ratings Exception :", e)
            ratings = "N/A"
        finally:
            row_dict["Ratings"] = ratings
            print("Ratings :", ratings)


        df3 = pd.DataFrame.from_dict(row_dict, orient='index')
        df3 = df3.transpose()
        about_df = pd.concat([about_df,df3])
        about_df.to_csv('/home/cd_scrapers/shiksha_vs_collegedunia/output_folder/about{}-{}.csv'.format(a, b))

    
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
        error.to_csv('/home/cd_scrapers/shiksha_vs_collegedunia/output_folder/shiksha_final_error{}-{}.csv'.format(a,b))
        #error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
        print('Error CSV Generated')
        driver.quit()




