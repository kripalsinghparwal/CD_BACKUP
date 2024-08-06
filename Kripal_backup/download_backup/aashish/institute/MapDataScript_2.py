import pandas as pd
import json
import os
import csv
import time
import sys
import ssl
import ast
import re
from datetime import datetime
import multiprocessing

failedQuerySet = set()

t1=datetime.now()
print(t1)

def format_timings(row):
    try:
        timingList = []
        open_hours = row['open_hours']
        for i in open_hours:
            timingList.append(i + " : " +  open_hours[i].replace("\u202f", ""))
        timings = "\n".join(timingList)
        # print("timings ", timings)
    except:
        timings = "N/A"
    return timings

def format_category(row):
    try:
        categoryList = row['category']
        category = ''
        for j in categoryList:
            if category == '':
                category += j['title']
            else:
                category += "\t" + j['title']
    except:
        category = "N/A"
    return category


def format_tags(row):
    try:
        serviceList = row['tags']
        serviceType = ''
        accessibility = ''
        amenities = ''
        fromTheBusiness =''
        # print("type of row", type(serviceList), serviceList)
        if type(serviceList) == list:
            for j in serviceList:
                if j['group_id'] == 'accessibility':
                    if accessibility == '':
                        accessibility += j['value_title']
                    else:
                        accessibility += "\t" + j['value_title']
                else:
                    accessibility = "N/A"
                if j['group_id'] == 'service_options':
                    if serviceType == '':
                        serviceType += j['value_title']
                    else:
                        serviceType += "\t" + j['value_title']
                else:
                    serviceType = "N/A"
                if j['group_id'] == 'amenities':
                    if amenities == '':
                        amenities += j['value_title']
                    else:
                        amenities += "\t" + j['value_title']
                else:
                    amenities = "N/A"
                if j['group_id'] == 'from_the_business':
                    if fromTheBusiness == '':
                        fromTheBusiness += j['value_title']
                    else:
                        fromTheBusiness += "\t" + j['value_title']
                else:
                    fromTheBusiness = "N/A"
        else:
            serviceType = "N/A"
            amenities = "N/A"
            fromTheBusiness = "N/A"
            accessibility = "N/A"

    except Exception as e:
        serviceType = "N/A"
        amenities = "N/A"
        fromTheBusiness = "N/A"
        accessibility = "N/A"
        print("tag_exception", e)

    return [serviceType, amenities, fromTheBusiness, accessibility]

def dataFetching(query, a, b, main_df):
    updated_query = query.replace(" ", "+")
    # query = f'{city}'
    print(">>>>>>>>>>>>>>", updated_query)
    ssl._create_default_https_context = ssl._create_unverified_context
    if sys.version_info[0]==2:
        import six
        from six.moves.urllib import request
        opener = request.build_opener(
            request.ProxyHandler(
                {'http': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                'https': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
        data = (opener.open(f'https://www.google.com/maps/search/{updated_query}/?q={updated_query}&start=0&num=400&gl=in&hl=en&lum_json=1').read())
        time.sleep(3)
    if sys.version_info[0]==3:
        import urllib.request
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {'http': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                'https': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
        try:
            if opener.open(f'https://www.google.com/maps/search/{updated_query}/?q={updated_query}&start=0&num=400&gl=in&hl=en&lum_json=1').status == 200:
                try:
                    data = (opener.open(f'https://www.google.com/maps/search/{updated_query}/?q={updated_query}&start=0&num=400&gl=in&hl=en&lum_json=1').read())

                    count = 0
                    while count < 10:
                        try:
                            x = str(data, 'UTF-8')
                            json_object = json.loads(x)
                            dataList = json_object['organic']
                            main_df = dataProcessing(dataList, query, main_df, a, b)
                            break
                        except Exception as e:
                            count += 1
                            failedQuerySet.add(query)
                            print("failed locality ;", query)
                            print(e)
                except Exception as e:
                    print("reading exception", e)
                    print("failed locality ;", query)
                    failedQuerySet.add(query)

                
            else:
                print("status not 200")
                print("failed locality ;", query)
                failedQuerySet.add(query)
        except Exception as e: 
                print("connection exception", e)
                print("failed locality ;", query)
                failedQuerySet.add(query)
        return main_df


def dataProcessing(dataList, query, main_df, a, b):
    for d in dataList:
        d['Query'] = query
    # Apply the function to each row of the DataFrame
    temp_df = pd.DataFrame(dataList)
    temp_df['Timings'] = temp_df.apply(format_timings, axis=1)
    temp_df['Type'] = temp_df.apply(format_category, axis=1)

    main_df = pd.concat([main_df,temp_df],ignore_index=True)
    main_df = main_df[['Query', 'title', 'display_link', 'link', "address","phone","open_hours","category",
                       "Type", "tags","rating","reviews_cnt","latitude","longitude","claimed","fid","map_id_encoded","map_id","map_link","original_image","image","thumbnail","icon","image_url","rank","original_title","temporarily_closed","Timings"]]

    print("length of main_df", len(main_df), main_df.columns)
    mydir = "/home/cd_scrapers/aashish/institute/output_data"
    main_df.to_csv(mydir+f"/MapData_testing{a}-{b}.csv")
    print("_____________________")
    print("_____________________")
    time.sleep(2)
    return main_df

# if __name__ == "__main__":
#     cityList = []
#     main_df = pd.DataFrame()
#     with open("/home/cd_scrapers/API_DATACOLLECTOR/major_indian_citites_StudyAbroadfailedInstitutes5.csv", 'r', newline='',  encoding="utf-8") as f:
#         csvreader = csv.reader(f)
#         for line in csvreader:
#             print("line", line)
#             cityList.append(line[0])

#         for city in cityList[1:200]:
#             print(city)
#             main_df = dataFetching(city, main_df)

#     df = pd.DataFrame()
#     df['city'] = list(failedQuerySet)
#     df.to_csv("major_indian_citites_StudyAbroadfailedInstitutes7.csv")
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
def main_func(total_length,keywords):
        a = 0
        b = len(keywords)
        main_df = pd.DataFrame()
        for i in range(0,total_length):
            query = keywords[i]
            print("query", query)
            try:
                main_df = dataFetching(query, a, b, main_df)
            except Exception as e:
                # failedQuerySet.add(updated_query)
                failedQuerySet.add(query)
                print("failed query :", query)
                print("exception : ", e)


                failed_df = pd.DataFrame()

                failed_df['Keywords'] = list(failedQuerySet)
                failed_df.to_csv(f"FailedQuery{a}-{b}.csv",mode='a')

if __name__ == "__main__":   
    input_df = pd.read_csv("/home/cd_scrapers/aashish/institute/input_data/genrated_query100-200.csv").drop_duplicates(subset=['Keywords'], keep='last')[0:100]
    print(len(input_df))
    keywords=input_df['Keywords'].to_list()
    # count = 1
    total_length = len(keywords)
    
    keywords_split = split(keywords, 4)
    print(f"Keywords split into batches of 4")

    for_pool = [(len(i),i) for i in keywords_split]

    pool = multiprocessing.Pool(4)

    pool.starmap(func=main_func, iterable=for_pool)

    pool.close()


    
    t2=datetime.now()
    print(f'time taken by code {t2-t1}')