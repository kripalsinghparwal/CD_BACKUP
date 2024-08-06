#!/usr/bin/env python
# print('If you get error "ImportError: No module named \'six\'" install six:\n'+\
#     '$ sudo pip install six');
# print('To enable your free eval account and get CUSTOMER, YOURZONE and ' + \
#     'YOURPASS, please contact sales@brightdata.com')

import json
import os
import csv
import time
import sys
import ssl
import pandas as pd
def dataFetching(id, title, review_count, institute_id, a, b, main_df):
    fId = id.replace(":", "%3A")
    print("fid>>>>>>>>>>>>>>>>", fId, title, review_count)
    ssl._create_default_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = ssl._create_unverified_context
    for start_parameter in range(0, int(review_count), 10):
        print(start_parameter)
        if sys.version_info[0]==2:
            import six
            from six.moves.urllib import request
            opener = request.build_opener(
                request.ProxyHandler(
                    {'http': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                    'https': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
            data = (opener.open(f'https://www.google.com/reviews?fid={fId}&hl=en&start={start_parameter}&lum_json=1').read())
        if sys.version_info[0]==3:
            import urllib.request
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler(
                    {'http': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                    'https': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
            # data = (opener.open(f'https://www.google.com/reviews?fid={fId}&hl=en&lum_json=1').read())
            data = (opener.open(f'https://www.google.com/reviews?fid={fId}&hl=en&start={start_parameter}&lum_json=1').read())
            

        count = 0
        while count<10:
            try:
                x = str(data, 'UTF-8')
                json_object = json.loads(x)
                dataList = json_object['reviews']
                main_df = dataProcessing(dataList, id, title, institute_id, a, b, main_df)
                break
            except Exception as e:
                count+=1
                print(e)

def dataProcessing(dataList, id, title, institute_id, a, b, main_df):
    for d in dataList:
        d['institute_id'] = institute_id
        d['title'] = title
        d['Fid'] = id
    
    
    # Apply the function to each row of the DataFrame
    temp_df = pd.DataFrame(dataList)

    main_df = pd.concat([main_df,temp_df],ignore_index=True)
    # main_df = main_df[['Query', 'title', 'display_link', 'link', "address","phone","open_hours","category",
    #                    "Type", "tags","rating","reviews_cnt","latitude","longitude","claimed","fid","map_id_encoded","map_id","map_link","original_image","image","thumbnail","icon","image_url","rank","original_title","temporarily_closed","Timings"]]

    print("length of main_df", len(main_df), main_df.columns)
    mydir = "/home/cd_scrapers/API_DATACOLLECTOR/institutes_folder/OUTPUT_FOLDER"
    main_df.to_csv(mydir+ f"/ReviewsTest{a}-{b}.csv")
    print("_____________________")
    print("_____________________")
    time.sleep(2)
    return main_df



################################### For Fetching data with Fid and Title ###############################
# if __name__ == "__main__":
def review_scrapper():
    main_df = pd.DataFrame()
    a = 0
    b = 1000
    input_df = pd.read_csv("/home/cd_scrapers/API_DATACOLLECTOR/institutes_folder/INPUT_FOLDER/Main Sheet Reviews (JEE Scraaping) - Final Institute.csv").drop_duplicates(subset=['Fid']).dropna(subset=['Total Reviews'])[a:b]
    print("length of input df", len(input_df))
    for ind in input_df.index:
        # print(type(input_df['Total Reviews'][ind]))
        try:
            print(input_df['Fid'][ind], input_df['Title'][ind], int(input_df['Total Reviews'][ind]),  input_df['Institute Id'][ind])
            dataFetching(input_df['Fid'][ind], input_df['Title'][ind], int(input_df['Total Reviews'][ind]),input_df['Institute Id'][ind], a, b, main_df)
        except Exception as e:
            print("exception : ", e)
review_scrapper()