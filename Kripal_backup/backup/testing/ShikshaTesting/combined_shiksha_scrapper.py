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

a = 2000
b = 3000

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

        try:
            table = soup.find('table', class_='_895c')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            cols = rows[1].find_all('td')
            college_type= cols[1].get_text()
            time.sleep(random.randint(1,3))
        except Exception as e:
            college_type = 'N/A'
            print(e)
            print('Type not available!')
        finally:
            print("college_type :",  college_type)

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

        
        try :
            # menu_header = driver.find_element_by_class_name('menuItemsContainerList').find_elements_by_tag_name('li')
            menu_header = driver.find_element(By.CLASS_NAME, 'menuItemsContainerList').find_elements(By.TAG_NAME, 'li')
            menu_links = []
            for links in menu_header:
                # menu_links.append(links.find_element_by_tag_name('a').get_attribute('href'))
                menu_links.append(links.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        except Exception as e:
            print(e)
            menu_links.append('N/A')
            print("error in menu_header")
    
        # REVIEWS
        try:
            driver.get(menu_links[2])
            review_table = soup.find('div', class_='getAllrvws')
            verified_review = review_table.text.split('.')[-2].lstrip().split(',')[1].lstrip().split(' ')[0]
            published_review = review_table.text.split('.')[-2].lstrip().split(',')[0].lstrip().split(' ')[2]
            review = "verified_review: " + verified_review + "& Published Review: " + published_review
            print('Reviews: ',review, '\n')
            
            #published_review = review_table.text.split('.')[-2].lrstrip().split(',')[0].lstrip().split(' ')[2]
            #print('Published_Reviews:',published_review,'\n')   
            time.sleep(random.randint(1,3))
        except Exception as e:
            print(e)
            try:
                review = review_table.text.split('.')[-2].lstrip().split(',')[0].lstrip().split(' ')[1]
            except:
                review = 'N/A'            
                print('Reviews not available!\n')
        def program_scrape(d_list):
            # course_program1 = driver.find_elements_by_css_selector('.shadowCard.ctpCard.BAC')
            course_program1 = driver.find_elements(By.CSS_SELECTOR, '.shadowCard.ctpCard.BAC')
            print(len(course_program1), ' Programs:')
            for program in course_program1:
                # program_name = program.find_element_by_css_selector(
                #     '.headSec.acpTupleHead.bacTupleHeadCont').text
                program_name = program.find_element(By.CSS_SELECTOR, '.headSec.acpTupleHead.bacTupleHeadCont').text
                # program_fees = program.find_elements_by_css_selector('.valueTxt')[2].text
                program_fees = program.find_elements(By.CSS_SELECTOR, '.valueTxt')[2].text
                print('Program Name: ', program_name, '\nFees: ', program_fees, '\n')

                func_list = [college_name, city, college_type, review, college_link, 'Program',
                             program_name, program_fees, link]
                d_list.append(func_list)

            time.sleep(0.5)
            return d_list


        def course_scrape(col_count, strm_count, cou_len, d_list):
            # course_program2 = driver.find_elements_by_css_selector('.shadowCard.ctpCard.CLP')
            course_program2 = driver.find_elements(By.CSS_SELECTOR, '.shadowCard.ctpCard.CLP')
            print('\nCourses:')
            for course in course_program2:
                cou_len += 1
                # course_name = course.find_element_by_css_selector(
                #     '.headSec.acpTupleHead.clpTupleHeadCont').text
                course_name = course.find_element(By.CSS_SELECTOR, '.headSec.acpTupleHead.clpTupleHeadCont').text
                # course_fees = course.find_elements_by_css_selector('.valueTxt')[3].text
                course_fees = course.find_elements(By.CSS_SELECTOR, '.valueTxt')[3].text
                print('Stream:', strm_count, '\t\tCollege:', col_count, '\t\tCourse:', cou_len, '\nCourse '
                                                                                                'Name: ',
                      course_name, '\nFees: ', course_fees, '\n')

                func_list = [college_name, city, college_type, review, college_link, 'Course', course_name,
                             course_fees, link]
                d_list.append(func_list)

            return cou_len, d_list
        # COURSES AND FEES
        n = 1
        courses_len = 0
        while True:
            if n == 1:
                next_course_page_url = link + '/courses'
            else:
                next_course_page_url = link + '/courses-' + str(n)
            driver.get(next_course_page_url)
            time.sleep(1)
            n += 1
    
            # main_container = driver.find_element_by_xpath(
            #     '//*[@id="acp-tuples"]').find_elements_by_css_selector(
            #     '.filter-sec')
            main_container = driver.find_element(By.XPATH, '//*[@id="acp-tuples"]').find_elements(By.CSS_SELECTOR, '.filter-sec')
    
            if len(main_container) == 0:
                print('Total Courses: ', courses_len, '\n')
                college_df = pd.DataFrame(data_list,
                                          columns=['College Name', 'City', 'College Type', 'No. of Reviews',
                                                   'Website Link',
                                                   'Course/Program', 'Name',
                                                   'Fees', 'Shiksha Link'])
                df2 = pd.concat([df2, college_df], ignore_index=True)
                df2.to_csv(r'C:\Users\Kripal\Desktop\testing\output_folder\shiksha_colleges_data{}-{}.csv'.format(a, b))
                #df2.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_colleges_data_error_{today.month}.csv')
                
                print(df2)
                break
    
            for i in range(50):
                driver.execute_script("window.scrollBy(0,300)", "")
                time.sleep(0.1)
    
    
            if n == 2:
                data_list = program_scrape(data_list)
                courses_len, data_list = course_scrape(college_count, stream_count, courses_len, data_list)
    
            else:
                courses_len, data_list = course_scrape(college_count, stream_count, courses_len, data_list)
    
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
        error.to_csv(r'C:\Users\Kripal\Desktop\testing\output_folder\shiksha_final_error{}-{}.csv'.format(a, b))
        #error.to_csv(f'C:/Users/Somya/Desktop/Shiksha/shiksha_error_{today.month}.csv')
        print('Error CSV Generated')
        driver.quit()




