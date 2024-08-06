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
from datetime import datetime
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

            try:
                if opener.open(f'https://www.google.com/reviews?fid={fId}&hl=en&start={start_parameter}&lum_json=1').status == 200:
                    try:
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
                                print("retrying exception", e)
                    except Exception as e:
                        print("reading exception", e)
                        failedFidList.append((input_df['fid'][ind], input_df['title'][ind], input_df['Institute_id'][ind]))
                else:
                    print("status not 200")
                    failedFidList.append((input_df['fid'][ind], input_df['title'][ind], input_df['Institute_id'][ind]))
            except Exception as e: 
                print("connection exception", e)
                failedFidList.append((input_df['fid'][ind], input_df['title'][ind], input_df['Institute_id'][ind]))
    return main_df

def dataProcessing(dataList, id, title, institute_id, a, b, main_df):
    for d in dataList:
        d['institute_id'] = institute_id
        d['title'] = title
        d['fid'] = id
    
    
    # Apply the function to each row of the DataFrame
    temp_df = pd.DataFrame(dataList)

    main_df = pd.concat([main_df,temp_df],ignore_index=True)
    # main_df = main_df[["review_id","reviewer","rating","created","comment","review_reply","institute_id","title","Fid","photos"]]

    print("length of main_df", len(main_df), main_df.columns)
    mydir = "/home/cd_scrapers/aashish/output_folder"
    main_df.to_csv(mydir+ f"/JuneReviewsSheet{a}-{b}.csv")
    print("_____________________")
    print("_____________________")
    time.sleep(2)
    return main_df



################################### For Fetching data with Fid and Title ###############################
if __name__ == "__main__":
# def review_scrapper():
    print("starting time ", datetime.now())
    main_df = pd.DataFrame()
    failedFidList = []
    a = 0
    b = 5
    print("a, b:", a, b)
    # input_df = pd.read_csv("/home/cd_scrapers/API_DATACOLLECTOR/institutes_folder/INPUT_FOLDER/Main Sheet Reviews (JEE Scraaping) - Final Institute.csv").drop_duplicates(subset=['Fid']).dropna(subset=['Total Reviews'])[a:b]
    input_df = pd.read_csv("/home/cd_scrapers/aashish/input_folder/Demo0-5.csv").dropna(subset=['reviews_cnt'])[a:b]
    print("length of input df", len(input_df))
    for ind in input_df.index:
        # print(type(input_df['Total Reviews'][ind]))
        try:
            print(input_df['fid'][ind], input_df['title'][ind], int(input_df['reviews_cnt'][ind]),  input_df['Institute_id'][ind])
            main_df = dataFetching(input_df['fid'][ind], input_df['title'][ind], int(input_df['reviews_cnt'][ind]),input_df['Institute_id'][ind], a, b, main_df)
        except Exception as e:
            print("exception : ", e)
            failedFidList.append((input_df['fid'][ind], input_df['title'][ind], input_df['Institute_id'][ind]))

    failed_df = pd.DataFrame()
    failed_df['Fid'] = failedFidList
    failed_df.to_csv(f"JuneReviewsFailed{a}-{b}.csv")
    print("ending time ", datetime.now())
# review_scrapper()