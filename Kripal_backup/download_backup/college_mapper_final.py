import pandas as pd
import re
import numpy as np
import ssl
import urllib.request
import urllib.parse
import json
import warnings
warnings.filterwarnings("ignore")

def check_course_url(url):
    course_url_pattern = re.compile("https://collegedunia.com/[a-z]+/[university|college]+/[a-z0-9-]+/[a-z0-9-]+")
    if re.fullmatch(course_url_pattern, url):
        return int(re.findall('.*-(\d+)$',course_url)[0])
    else:
        return 0

def check_college_url(url):
    college_url_pattern = re.compile("https://collegedunia.com/[a-z]+/[university|college]+/[a-z0-9-]+")
    if re.fullmatch(college_url_pattern, url):
        return int(re.findall('.*[university|college]+/(\d+)',college_url)[0])
    else:
        return 0
    
def get_serp_data(search_query):
    try:
        print(search_query)
        temp= pd.DataFrame()
        ssl._create_default_https_context = ssl._create_unverified_context
        query = urllib.parse.quote(search_query).replace('/','%2F')
        opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {'http': 'http://brd-customer-hl_a4a3b5b0-zone-questions_serp:bdmzmy3683ha@zproxy.lum-superproxy.io:22225',
            'https': 'http://brd-customer-hl_a4a3b5b0-zone-questions_serp:bdmzmy3683ha@zproxy.lum-superproxy.io:22225'}))
        response = opener.open('https://www.google.com/search?q='+query+'&hl=en&num=5&lum_json=1')
        google_search = response.read().decode('utf-8')
        google_search_json = json.loads(google_search)
        data = google_search_json
        if 'results_cnt' in google_search_json['general'].keys():
            if google_search_json['general']['results_cnt'] == 0:
                return 0
        if "organic" in data.keys():
            temp = temp.append(data['organic'],ignore_index=True)
        if "featured_snippets" in data.keys():
            temp = temp.append(data['featured_snippets'],ignore_index=True)
        temp1 = temp[['rank', 'link', 'description', 'title', 'display_link']]
        print('success')
        return temp1
    except Exception as ex:
        print('failed')
        return -1
    
def mapper_function(df):
    if df['cd_college_id'] == 0:
        search_query = df['applied_college'].iloc[0]+' inurl:collegedunia.com/*/university/'
        serp_data = get_serp_data(search_query)
        if serp_data == 0 or serp_data == -1:
            df['cd_college_id'].iloc[0] = 0
        serp_data['college_id'] = serp_data['link'].apply(check_college_url)
        serp_data.drop(serp_data[serp_data['college_id'] == 0].index,inplace = True)
        for i in serp_data.index:
            if df['applied_college'].iloc[0] in serp_data['title'][i] and df['applied_college'].iloc[0] in serp_data['description'][i]:
                df['college_name_in_title_desc'].iloc[0] = 1
                df['cd_college_id'].iloc[0] = serp_data['college_id'][i]
    if df['cd_college_id'] == 0:
        return 0
    else:
        search_query = df['course_applied_text'].iloc[0]+' '+df['applied_college'].iloc[0]+' inurl:collegedunia.com/*/university/'+str(df['cd_college_id'].iloc[0])+'-'
    serp_data = get_serp_data(search_query)
    if serp_data == 0 or serp_data == -1:
        return 0
    serp_data['course_id'] = serp_data['link'].apply(check_course_url)
    serp_data.drop(serp_data[serp_data['course_id'] == 0].index,inplace = True)
    for i in serp_data.index:
        if df['course_applied_text'].iloc[0] in serp_data['title'][i] and df['applied_college'].iloc[0] in serp_data['description'][i]:
            df['course_name_in_title_desc'].iloc[0] = 1
            df['cd_course_id'].iloc[0] = serp_data['course_id'][i]
    return df

