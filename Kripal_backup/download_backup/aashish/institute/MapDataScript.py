import pandas as pd
import json
import os
import csv
import time
import sys
import ssl
import ast
import re
import threading
from datetime import datetime
import mailer
import sqlalchemy
mail_counter=0
mydir = "/home/cd_scrapers/aashish/institute/output_data"
###changeble pard
file_name='genrated_query_tranning200-300'
screen='screen_databasetesting'
data_range_1=0
data_range_2=1000
#################
failedLocalitiesList=set()
conn = sqlalchemy.create_engine("postgresql://{aashish}:{aashish}@161.97.158.42/{institutes}")
conn = sqlalchemy.create_engine("postgresql://{user}:{pw}@161.97.158.42/{db}".format(user="aashish", pw="aashish", db="institutes"))



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

def dataFetching(query, a, b):
    global mail_counter
    global failedLocalitiesList
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
                {'http': 'http://brd-customer-hl_a4a3b5b0-zone-google_bisuiness:jjb78tl05e1l@brd.superproxy.io:22225',
                'https': 'http://brd-customer-hl_a4a3b5b0-zone-google_bisuiness:jjb78tl05e1l@brd.superproxy.io:22225'}))
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
                            dataProcessing(dataList, query, a, b)
                            break
                        except Exception as e:
                            count += 1
                            failedLocalitiesList.add(query)
                            print("failed locality ;", query)
                            print(e)
                except Exception as e:
                    print("reading exception", e)
                    print("failed locality ;", query)
                    failedLocalitiesList.add(query)

                
            else:
                print("status not 200")
                print("failed locality ;", query)
                failedLocalitiesList.add(query)
        except Exception as e: 
                print("connection exception", e)
                print("failed locality ;", query)
                failedLocalitiesList.add(query)
                failed_localities = pd.DataFrame()
                failed_localities['keywords'] = list(failedLocalitiesList)
                failed_localities.to_sql('failed_request',conn,if_exists='append')  
                # failed_localities.to_csv(f"FailedLocalities_{screen}_{file_name}_{data_range_1}_{data_range_2}.csv")               
                e = str(e)
                if mail_counter < 2:
                    if mailer.send_email(e):
                      mail_counter += 1
       
        


def dataProcessing(dataList, query, a, b):    
    for d in dataList:        
        d['Query'] = query
    # Apply the function to each row of the DataFrame
    temp_df = pd.DataFrame(dataList)      
    temp_df['Timings'] = temp_df.apply(format_timings, axis=1)
    temp_df['Type'] = temp_df.apply(format_category, axis=1)  
    if 'temporarily_closed' not in temp_df.columns :
        temp_df['temporarily_closed']=None 
    # main_df = pd.concat([main_df,temp_df],ignore_index=True)    
    temp_df = temp_df[['Query', 'title', 'display_link', 'link', "address","phone","open_hours","category",
                       "Type", "tags","rating","reviews_cnt","latitude","longitude","claimed","fid","map_id_encoded","map_id","map_link","original_image","image","thumbnail","icon","image_url","rank","original_title","temporarily_closed","Timings"]]
    
    print("length of temp_df", len(temp_df),) 
    temp_df.to_sql('institutes_data',conn,if_exists='append')   
    # temp_df.to_csv(mydir+f"/MapData_{screen}_{file_name}_{a}-{b}.csv",mode='a',header=False)
    print("_____________________")
    print("_____________________")
    time.sleep(2)
   

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
#     df['city'] = list(failedLocalitiesList)
#     df.to_csv("major_indian_citites_StudyAbroadfailedInstitutes7.csv")

def threadFuntion(a, b):
    main_df = pd.DataFrame(columns=['Query', 'title', 'display_link', 'link', "address","phone","open_hours","category",
                       "Type", "tags","rating","reviews_cnt","latitude","longitude","claimed","fid","map_id_encoded","map_id","map_link","original_image","image","thumbnail","icon","image_url","rank","original_title","temporarily_closed","Timings"])
    main_df.to_csv(mydir+f"/MapData_{screen}_{file_name}_{a}-{b}.csv")
    print("a and b", a, b, type(a), type(b))
    failedQuerySet = set()
    input_df = pd.read_csv(f"/home/cd_scrapers/aashish/institute/input_data/{file_name}.csv")[data_range_1:data_range_2].drop_duplicates(subset=['Keywords'], keep='last')[a:b]
    print("length of input_df :", len(input_df))
    # count = 1
    for ind in input_df.index:
        query = input_df['Keywords'][ind]
        print("query", query)
        try:
            dataFetching(query, a, b)
        except Exception as e:
            # failedLocalitiesList.add(updated_query)
            failedQuerySet.add(query)
            print("failed query :", query)
            print("exception : ", e)

            print(len(failedQuerySet))
            failed_df = pd.DataFrame()
            failed_df['keywords'] = list(failedQuerySet)
            failed_df.to_sql('failed_data',conn,if_exists='append') 
            failed_df.to_csv(f"FailedQuery__{screen}_{file_name}_{a}-{b}.csv")


if __name__ == "__main__":
    t1= datetime.now()
    # total = 100000
    total = len(pd.read_csv(f"/home/cd_scrapers/aashish/institute/input_data/{file_name}.csv").drop_duplicates(subset=['Keywords'], keep='last')[data_range_1:data_range_2])

    # Number of ranges to create
    num_ranges = 5

    # Calculate the size of each range
    range_size = total // num_ranges

    # Create the ranges
    ranges = [(i * range_size, (i + 1) * range_size) for i in range(num_ranges)]

    threads = {}
    count = 1
    for r in ranges:
        print(r)
        print("opening count", count)
        thread_name = f"t{count}"
        threads[thread_name] = threading.Thread(target=threadFuntion, args=r)
        threads[thread_name].start()
        count +=1
    for thread in threads.values():
        thread.join()

    
    print(" time taken by code is:", datetime.now()-t1)



