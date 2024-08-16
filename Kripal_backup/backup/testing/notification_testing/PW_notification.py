from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re

data = []


def get_data(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    website = url

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    stage_1 = soup.find('div', class_='site grid-container container hfeed')
    stage_2 = stage_1.find('section', class_='gb-container gb-container-6b1cec5c box-shadow')

    stage_3 = stage_2.find('section', class_='gb-container gb-container-69000104')
    latest_feed = stage_3.find('div', class_='gb-container gb-container-55534a0e')
    
    latest_feed_big = latest_feed.find('div', class_='gb-container gb-container-b08e3678')
    latest_data = latest_feed_big.find('div', class_='gb-container gb-container-1e59fde4')
    latest_h3 = latest_data.find('h3',class_='gb-headline gb-headline-9467764e gb-headline-text')

    latest_big_heading = latest_h3.find('a').text.strip()
    latest_big_link = latest_h3.find('a')['href']

    Notification_data = {

            'Website':website,
            'section':'LATEST',
            'Notification_Title':latest_big_heading,
            'Link to Notice':latest_big_link
        }

    data.append(Notification_data)

    latest_feed_small = latest_feed.find('div',class_='gb-container gb-container-c23a5eec')
    latest_a = latest_feed_small.find('div',class_='gb-grid-wrapper gb-grid-wrapper-ed93db81 gb-query-loop-wrapper')

   #latest_small_1 = latest_a.find('div',class_='gb-grid-column gb-grid-column-26d9cf9b gb-query-loop-item post-157811 post type-post status-publish format-standard has-post-thumbnail hentry category-ugc-net tag-maharashtra-set-answer-key-2024 tag-mh-set-2024 tag-mh-set-2024-answer-key tag-mh-set-answer-key-2024 tag-ugc-net-2024')

    latest_rows = latest_a.find_all('div',class_='gb-container gb-container-f1fd27cc') 

    for latest_row in latest_rows:

        latest_small_h4 = latest_row.find('h4',class_='gb-headline gb-headline-d05f786f gb-headline-text')

        latest_small_heading = latest_small_h4.find('a').text.strip()
        latest_small_link = latest_small_h4.find('a')['href'] 

        Notification_data = {

            'Website':website,
            'section':'LATEST',
            'Notification_Title':latest_small_heading,
            'Link to Notice':latest_small_link
        }

        data.append(Notification_data)

 ########################################################################################################################################

    stage_4 = stage_2.find('section',class_='gb-container gb-container-3e53aa64')
    stage_5 = stage_4.find('div',class_='gb-grid-wrapper gb-grid-wrapper-1f78f700 gb-query-loop-wrapper')

    featured_rows = stage_5.find_all('div',class_='gb-container gb-container-123478cd')

    for featured_row in featured_rows:

        featured_h3 = featured_row.find('h3',class_='gb-headline gb-headline-9e371c2b gb-headline-text')
        featured_heading = featured_h3.find('a').text.strip()
        featured_link = featured_h3.find('a')['href'] 

        Notification_data = {

            'Website':website,
            'section':'FEATURED',
            'Notification_Title':featured_heading,
            'Link to Notice':featured_link
        }

        data.append(Notification_data)

###########################################################################################

    stage_6 = stage_1.find('div',class_='site-content')
    stage_7 = stage_6.find('div',class_='content-area')
    stage_8 = stage_7.find('div',class_='entry-content')

    stage_9 = stage_8.find('div',class_='gb-grid-wrapper gb-grid-wrapper-c9bd997a gb-query-loop-wrapper')

    jee_rows = stage_9.find_all('h3',class_='gb-headline gb-headline-0bf7389c gb-headline-text')

    for row in jee_rows:
        jee_heading = row.find('a').text.strip()
        jee_link = row.find('a')['href']

        Notification_data = {

            'Website':website,
            'section':'JEE',
            'Notification_Title':jee_heading,
            'Link to Notice':jee_link
        }

        data.append(Notification_data)
#########################################################
    stage_20 = stage_8.find('section',class_='gb-container gb-container-aa70fb47')
    stage_10 = stage_20.find('div',class_='gb-grid-wrapper gb-grid-wrapper-7104b5c8 gb-query-loop-wrapper')

    neet_rows = stage_10.find_all('h3',class_='gb-headline gb-headline-6eb2b0df gb-headline-text')

    for neet_row in neet_rows:
        neet_heading = neet_row.find('a').text.strip()
        neet_link = neet_row.find('a')['href']

        Notification_data = {

            'Website':website,
            'section':'NEET',
            'Notification_Title':neet_heading,
            'Link to Notice':neet_link
        }

        data.append(Notification_data)

   ##########################################################

    stage_11 = stage_8.find('div',class_='gb-grid-wrapper gb-grid-wrapper-c9928546 gb-query-loop-wrapper') 

    ssc_rows = stage_11.find_all('h3',class_='gb-headline gb-headline-a1b4279f gb-headline-text')

    for ssc_row in ssc_rows:

        ssc_heading = ssc_row.find('a').text.strip()
        ssc_link = ssc_row.find('a')['href']


        Notification_data = {

            'Website':website,
            'section':'SSC',
            'Notification_Title':ssc_heading,
            'Link to Notice':ssc_link
        }

        data.append(Notification_data)

#################################################################
    
    stage_21 = stage_8.find('div',class_='gb-container gb-container-888934ed')

    stage_22 = stage_21.find('div',class_='gb-grid-wrapper gb-grid-wrapper-7f87810b gb-query-loop-wrapper')
    stage_23 = stage_22.find('h3',class_='gb-headline gb-headline-ec5d3e15 gb-headline-text')

    community_big_heading = stage_23.find('a').text.strip()
    community_big_link = stage_23.find('a')['href']
    Notification_data = {

            'Website':website,
            'section':'Community',
            'Notification_Title':community_big_heading,
            'Link to Notice':community_big_link
        }

    data.append(Notification_data)

    stage_24 = stage_21.find('div',class_='gb-container gb-container-68d222ba')

    community_rows = stage_24.find_all('h4',class_='gb-headline gb-headline-9e680c5e gb-headline-text')

    for comm_row in community_rows:

        comm_heading = comm_row.find('a').text.strip()
        comm_link = comm_row.find('a')['href']

        Notification_data = {

            'Website':website,
            'section':'Community',
            'Notification_Title':comm_heading,
            'Link to Notice':comm_link
        }

        data.append(Notification_data)





    driver.quit()
    return data



def export_data(data):
    df = pd.DataFrame(data)
    df.to_csv("Notifications_pw.csv")

def main():
    data = get_data('https://www.pw.live/exams/')
    print(data)
    export_data(data)


if __name__ == '__main__':
    main()
