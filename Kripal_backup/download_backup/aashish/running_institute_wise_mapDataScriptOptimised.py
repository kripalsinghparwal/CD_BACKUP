import pandas as pd
import json
import os
import csv
import time
import sys
import ssl
import ast
import re

failedLocalitiesList = set()

# # Function to replace Unicode escape sequences
# def replace_unicode_escape(match):
#     return chr(int(match.group(1), 16))

# # Function to format timings
# def format_timings(row):
#     # Replace Unicode escape sequences
#     timings_str = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode_escape, row['open_hours'])
#     timings_dict = ast.literal_eval(timings_str)
#     formatted_timings = "\n".join([f"{day} : {timing}" for day, timing in timings_dict.items()])
#     return formatted_timings

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

def dataFetching(query, a, b, institute_id, main_df):
    query = query.replace(" ", "+").replace('\r', '').replace('\n', '').replace("#", "%23").replace("–", "%E2%80%93").replace("’", "%E2%80%99").replace("™", "%E2%84%A2").replace("“", "%E2%80%9C").replace("”", "%E2%80%9D").replace("•", "%E2%80%A2").replace("é", "%C3%A9").replace("ç", "%C3%A7").replace("&", "%26").replace("É", "%C3%89")
    # query = f'{city}'
    print(">>>>>>>>>>>>>>", query)
    ssl._create_default_https_context = ssl._create_unverified_context
    if sys.version_info[0]==2:
        import six
        from six.moves.urllib import request
        opener = request.build_opener(
            request.ProxyHandler(
                {'http': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                'https': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
        data = (opener.open(f'https://www.google.com/maps/search/{query}/?q={query}&start=0&num=400&gl=in&hl=en&lum_json=1').read())
        time.sleep(3)
    if sys.version_info[0]==3:
        import urllib.request
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {'http': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                'https': 'http://lum-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
        try:
            if opener.open(f'https://www.google.com/maps/search/{query}/?q={query}&start=0&num=400&gl=in&hl=en&lum_json=1').status == 200:
                try:
                    data = (opener.open(f'https://www.google.com/maps/search/{query}/?q={query}&start=0&num=400&gl=in&hl=en&lum_json=1').read())

                    count = 0
                    while count < 10:
                        try:
                            x = str(data, 'UTF-8')
                            json_object = json.loads(x)
                            dataList = json_object['organic']
                            main_df = dataProcessing(dataList, query, a, b, institute_id, main_df)
                            break
                        except Exception as e:
                            count += 1
                            failedLocalitiesList.add(institute_id)
                            print("failed query ;", query.replace("+", " ").replace("%23", "#").replace("%E2%80%93", "–").replace("%E2%80%99", "’").replace("%E2%84%A2", "™").replace("%E2%80%9C", "“").replace("%E2%80%9D", "”").replace("%E2%80%A2", "•").replace("%C3%A9", "é").replace("%C3%A7", "ç").replace("%26", "&").replace("%C3%89", "É"))
                            print(e)
                except Exception as e:
                    print("reading exception", e)
                    print("failed query ;", query.replace("+", " ").replace("%23", "#").replace("%E2%80%93", "–").replace("%E2%80%99", "’").replace("%E2%84%A2", "™").replace("%E2%80%9C", "“").replace("%E2%80%9D", "”").replace("%E2%80%A2", "•").replace("%C3%A9", "é").replace("%C3%A7", "ç").replace("%26", "&").replace("%C3%89", "É"))
                    failedLocalitiesList.add(institute_id)

                
            else:
                print("status not 200")
                print("failed query ;", query.replace("+", " ").replace("%23", "#").replace("%E2%80%93", "–").replace("%E2%80%99", "’").replace("%E2%84%A2", "™").replace("%E2%80%9C", "“").replace("%E2%80%9D", "”").replace("%E2%80%A2", "•").replace("%C3%A9", "é").replace("%C3%A7", "ç").replace("%26", "&").replace("%C3%89", "É"))
                failedLocalitiesList.add(city.replace("+", " "))
        except Exception as e: 
                print("connection exception", e)
                print("failed query ;", query.replace("+", " ").replace("%23", "#").replace("%E2%80%93", "–").replace("%E2%80%99", "’").replace("%E2%84%A2", "™").replace("%E2%80%9C", "“").replace("%E2%80%9D", "”").replace("%E2%80%A2", "•").replace("%C3%A9", "é").replace("%C3%A7", "ç").replace("%26", "&").replace("%C3%89", "É"))
                failedLocalitiesList.add(city.replace("+", " "))
        return main_df


def dataProcessing(dataList, query, a, b, institute_id, main_df):
    for d in dataList:
        d['Query'] = query.replace("+", " ")
        d['Institute_id'] = institute_id
    # Apply the function to each row of the DataFrame
    temp_df = pd.DataFrame(dataList)
    temp_df['Timings'] = temp_df.apply(format_timings, axis=1)
    temp_df['Type'] = temp_df.apply(format_category, axis=1)

    main_df = pd.concat([main_df,temp_df],ignore_index=True)
    # main_df = main_df[['Institute_id','Query', 'title', 'display_link', 'link', "address","phone","open_hours","category",
    #                    "Type", "tags","rating","reviews_cnt","latitude","longitude","claimed","fid","map_id_encoded","map_id","map_link","original_image","image","thumbnail","icon","image_url","rank","original_title","temporarily_closed","Timings"]]

    print("length of main_df", len(main_df), main_df.columns)
    mydir = "/home/cd_scrapers/aashish/output_folder/JuneData"
    main_df.to_csv(mydir+f"/Demo{a}-{b}.csv")
    print("_____________________")
    print("_____________________")
    time.sleep(2)
    return main_df

if __name__ == "__main__":
    a = 0
    b = 5
    main_df = pd.DataFrame()
    input_df = pd.read_csv("/home/cd_scrapers/aashish/input_folder/leftOut.csv").drop_duplicates(subset=['id'], keep='last')[a:b]
    print(len(input_df))
    # count = 1
    for ind in input_df.index:
        institute_id = input_df['id'][ind]
        if any(ele in input_df['Name'][ind].strip().lower() for ele in ['institute', 'institutes', 'coaching', 'coachings' 'classes', 'class']):
            institute_name = input_df['Name'][ind].strip()
        else:
            institute_name = input_df['Name'][ind].strip() + " institute"
        if type(input_df['State'][ind])==float or input_df['State'][ind]=="0":
            updated_query = institute_name
            # count+=1
        else:
            updated_query = institute_name + ", "  + input_df['City'][ind].strip() + ", "  + input_df['State'][ind].strip()
                    
                    
        updated_query = updated_query.replace(", , , ,", ",").replace(", , ,", ",").replace(", ,", ',').replace(",  ,  ,", ',').replace(",  ,", ',').replace(",,", ',').replace(",,", ",")
        print("updated_query", updated_query)
        try:
            main_df = dataFetching(updated_query, a, b, institute_id, main_df)
        except Exception as e:
            # failedLocalitiesList.add(updated_query)
            failedLocalitiesList.add(institute_id)
            print("failed query :", updated_query)
            print("exception : ", e)


            failed_df = pd.DataFrame()

            failed_df['id'] = list(failedLocalitiesList)
            failed_df.to_csv(f"Junecity&statefailedinstitutes{a}-{b}.csv")
