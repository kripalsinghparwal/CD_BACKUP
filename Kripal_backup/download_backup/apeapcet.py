from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import FirefoxOptions
import time

opts = FirefoxOptions()
opts.add_argument("--headless")

def initialize_driver():
    driver = webdriver.Firefox(options=opts)
    driver.maximize_window()
    driver.get('https://eapcet-sche.aptonline.in/EAPCET/collegeWiseAllotedReport.xls')
    return driver

def select_college(driver, college_index):
    collegeDropdown = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.NAME, 'programmeId'))
    )
    college_options = driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div/form/table/tbody/tr/td[1]/select/option") 
    college_options[college_index].click()
    time.sleep(2)
    return college_options[college_index].text

def select_course(driver, course_index):
    courseDropdown = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.NAME, 'collegeId'))
    )
    course_options = driver.find_elements(By.XPATH,"/html/body/div/div/div/div/div/div[2]/div/div/form/table/tbody/tr/td[2]/select/option")
    course_options[course_index].click()
    time.sleep(2)
    return course_options[course_index].text

def save_to_csv(data, filename):
    pd.DataFrame(data).to_csv(filename, index=False)

def main():
    data = {'college_name':[],'course_name':[],'hall_ticket':[],'rank':[],'applicant_name':[],'gender':[],'caste':[],'region':[],'alloted_category':[]}
    count = 37051
    college_count = 1040
    start_count = 1040
    end_count = 1100

    driver = initialize_driver()

    college_options_set = set(driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div/form/table/tbody/tr/td[1]/select/option"))
    # for college_index in range(1, len(college_options_set)):
    for college_index in range(college_count, end_count):
            collegeName = select_college(driver, college_index)
            print(college_count,':',collegeName)

            course_options = driver.find_elements(By.XPATH,"/html/body/div/div/div/div/div/div[2]/div/div/form/table/tbody/tr/td[2]/select/option")
            for course_index in range(1, len(course_options)):
                courseName = select_course(driver, course_index)
                submit = driver.find_element(By.ID, 'SUBMIT')
                submit.click()
                time.sleep(2)

                try:
                    driver.implicitly_wait(10)
                    pages = driver.find_element(By.ID,'example_paginate').find_element(By.TAG_NAME,'span').find_elements(By.TAG_NAME,'a')

                    allotment_table = driver.find_element(By.ID, 'example')
                    allotment_html = allotment_table.get_attribute('outerHTML')

                    #Extract Table
                    for page in pages:
                        pages = driver.find_element(By.ID,'example_paginate').find_element(By.TAG_NAME,'span').find_elements(By.TAG_NAME,'a')
                        driver.implicitly_wait(10)
                        page.click()
                        time.sleep(2)
                        allotment_table = driver.find_element(By.ID, 'example')
                        allotment_html = allotment_table.get_attribute('outerHTML')
                        
                        soup = BeautifulSoup(allotment_html, 'html.parser')
                        trs = soup.find('table').find('tbody').find_all('tr')
                        for tr in trs:
                            tds = tr.find_all('td')
                            hall_ticket = tds[1].text.strip()
                            rank = tds[2].text.strip()
                            applicant_name = tds[3].text.strip()
                            gender = tds[4].text.strip()
                            caste = tds[5].text.strip()
                            region = tds[6].text.strip()
                            alloted_category = tds[7].text.strip()

                            print(count, '-' ,collegeName, ":" , courseName)
                            data['college_name'].append(collegeName)
                            data['course_name'].append(courseName)

                            if hall_ticket != '':
                                data['hall_ticket'].append(hall_ticket)
                            else:
                                data['hall_ticket'].append('')

                            if rank != '':
                                data['rank'].append(rank)
                            else:
                                data['rank'].append('')

                            if applicant_name != '':
                                data['applicant_name'].append(applicant_name)
                            else:
                                data['applicant_name'].append('')

                            if gender != '':
                                data['gender'].append(gender)
                            else:
                                data['gender'].append('')

                            if caste != '':
                                data['caste'].append(caste)
                            else:
                                data['caste'].append('')
                            if region != '':
                                data['region'].append(region)
                            else:
                                data['region'].append('')
                            if alloted_category != '':
                                data['alloted_category'].append(alloted_category)
                            else:
                                data['alloted_category'].append('')
                                
                            # pd.DataFrame(dataset).to_csv('dataset.csv',index=False)
                            save_to_csv(data, 'data{}-{}.csv'.format(start_count, end_count))
                            count+=1
                except:
                        continue
                    
            college_count += 1

    driver.quit()

if __name__ == "__main__":
    main()
