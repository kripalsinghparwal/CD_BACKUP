import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import gspread
import ssl
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from urllib.request import urlopen
from urllib.request import ProxyHandler, build_opener
import urllib3
import random
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from zoneinfo import ZoneInfo
import warnings
import pandas as pd
import json
import numpy as np 

start_time = time.time()
output_timestamp = datetime.now(tz=ZoneInfo('Asia/Kolkata')).strftime("%Y-%m-%d-%H-%M")

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')
chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

PATH = "/usr/bin/chromedriver" #Path to chromedriver (Adjust as needed)


news_articles = []
success = []
failure = []
scrapers_report = []
#seleniumwire_options=options
driver= webdriver.Chrome(PATH,options=chrome_options)


# Define the base URL
base_url = 'https://www.pagalguy.com/'

# Initialize lists to store scraped data
news_articles = []
success = []
failure = []
scrapers_report = []

# Define columns for the data
url = []
Official = []
headline = []
tag = []
date = []
review = []
review_link = []

# Initialize a list to store extracted data
news_articles_extracted = []

desired_time_difference = "3 days ago" #ex. 3 days ago
print(desired_time_difference)


# Function to calculate and display the time difference
def calculate_time_difference(timestamp_str):
    print("calculating time difference of review with current timestamp")
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_time = datetime.utcnow()
    time_difference = current_time - timestamp
    if time_difference.days > 0:
        return f"{time_difference.days} days ago"
    elif time_difference.seconds >= 3600:
        hours_ago = time_difference.seconds // 3600
        return f"{hours_ago} hours ago"
    else:
        minutes_ago = time_difference.seconds // 60
        return f"{minutes_ago} minutes ago"

# Define the URL of the Google Sheets document
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1gSLwGt2t7-kpU5RBtLx9lUwiXoX5a0HVaB8yfCeuBJM/edit#gid=1117659686"

# Define the name of the worksheet
worksheet_name = "Sheet10"

# Use credentials from a JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name("pagal_guy.json", "https://spreadsheets.google.com/feeds")

# Authenticate with Google Sheets
gc = gspread.authorize(credentials)

# Open the Google Sheets document by its URL
sh = gc.open_by_url(spreadsheet_url)

# Select the worksheet by name
worksheet = sh.worksheet(worksheet_name)

print("reading url from sheet10 = Pagal Guy Forum Link (Official)")
# Read data from the specified column
column_name = "Pagal Guy Forum Link (Official)"
url_column = worksheet.col_values(worksheet.find(column_name).col)

# Remove the column header
url_column = url_column[1:]

# Initialize a list to store extracted data
basic_data = []
post_data_extracted = []


# Loop through each URL from the Google Sheets document
maind_df = pd.DataFrame()
for url in url_column:

    try:
        
        scrapers_report.append([url, base_url])
        driver.get(url)
        # time.sleep(1)
        print(url)
        review_link = url
        url_id = re.search(r"\d{7}", review_link).group(0)
        driver.get(review_link)
        time.sleep(2)
        
        total_sleep_time = 4
        # Function to check if the sleep time is reached
        def is_sleep_time_reached(start_time, sleep_time):
            return time.time() - start_time >= sleep_time
        
        
        start_time = time.time()
        while not is_sleep_time_reached(start_time, total_sleep_time):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(1)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        headline = soup.find('title').get_text().strip()
        articles = soup.find_all("article", class_="boxed onscreen-post")

        for article in articles:
            data_post_id = article.get("data-post-id")
            cooked_content = article.find("div", class_="cooked").get_text(strip=True)
            json_url = f"https://www.pagalguy.com/t/{url_id}/posts.json?post_ids%5B%5D={data_post_id}"
            #print(json_url)

            payload = {}
            headers = {}
            response = requests.request("GET", json_url, headers=headers, data=payload)

            if response.status_code == 200:
                data = response.json()
                posts = data["post_stream"]["posts"]
                # main_postdf 
                post_df = pd.DataFrame(posts)
                post_df['headline'] = headline
                post_df['url'] = url
                #post_df['json_url'] = json_url
                maind_df = pd.concat([maind_df,post_df])
                                        
    except Exception as e:
        print(f"An error occurred for URL: {url}")
        print(f"Error details: {str(e)}")
        failure.append(url)

failure = pd.DataFrame(failure)
failure.to_csv(f"fail_{output_timestamp}.csv")



maind_df['cooked'] = maind_df['cooked'].str.replace(r'<\/?p>', '',regex=True)   
maind_df['cooked'] = maind_df['cooked'].str.replace(r'<[^>]+>', '',regex=True)   

# Create a dictionary to store replies
replies = {}

# Loop through the DataFrame and update the replies dictionary
for idx, row in maind_df.iterrows():
    reply_to_post = row['reply_to_post_number']
    if reply_to_post is not None:
        if reply_to_post not in replies:
            replies[reply_to_post] = []
        replies[reply_to_post].append(row['cooked'])

# Add new reply columns to the DataFrame
max_replies = max(len(reply_list) for reply_list in replies.values()) if replies else 0
for i in range(1, max_replies + 1):
    maind_df[f"Reply_{i}"] = maind_df['post_number'].apply(lambda x: replies.get(x, [None])[i-1] if i <= len(replies.get(x, [])) else None)



maind_df['date'] = pd.to_datetime(maind_df['updated_at'],format="%Y-%m-%dT%H:%M:%S.%fZ")

maind_df['time_difference'] = datetime.utcnow() - maind_df['date']

maind_df = maind_df[maind_df['time_difference'].dt.days <3]
maind_df.to_csv(f"completejson_{output_timestamp}.csv", index=False)
col =['url','post_number','headline','date','reply_count','reply_to_post_number','cooked']

df_extracted = maind_df[col]
df_extracted.fillna("", inplace=True)
df_extracted['reply_to_post_number'].fillna(0,inplace=True)
df_extracted['date'] = df_extracted['date'].astype('str')
df_extracted.sort_values(by=['date'],ascending=False,inplace=True)
df_extracted.to_csv(f"extracted_news_articles_{output_timestamp}.csv", index=False)


# Define a function to handle the first case
def handle_case_1(df, output_csv_file):
    # Create a dictionary to map (post_number, headline) to cooked content
    post_and_headline_to_cooked = {}
    for _, row in df.iterrows():
        post_number = row['post_number']
        headline = row['headline']
        cooked = row['cooked']
        post_and_headline_to_cooked[(post_number, headline)] = cooked

    # Define a function to look up cooked content based on reply_to_post_number and headline
    def get_parent_content(row):
        reply_to_post_number = row['reply_to_post_number']
        headline = row['headline']
        key = (reply_to_post_number, headline)
        if reply_to_post_number and key in post_and_headline_to_cooked:
            return post_and_headline_to_cooked[key]
        return ''

    # Apply the function to create the parent_content column
    df['parent_content'] = df.apply(get_parent_content, axis=1)

    # Write the updated DataFrame to the output CSV file
    df.to_csv(output_csv_file, index=False)

# Define a function to handle the second case
def handle_case_2(input_csv_file, reference_csv_file, output_csv_file):
    # Read data from the input CSV file and create a DataFrame
    df1 = pd.read_csv(input_csv_file)

    # Read data from the reference CSV file and create a DataFrame
    df2 = pd.read_csv(reference_csv_file)

    # Create a dictionary to map post_number and headline to cooked content from df2
    post_and_headline_to_cooked = {}
    for _, row in df2.iterrows():
        post_number = row['post_number']
        headline = row['headline']
        cooked = row['cooked']
        post_and_headline_to_cooked[(post_number, headline)] = cooked

    # Define a function to get the parent content based on reply_to_post_number and headline
    def get_parent_content(row):
        reply_to_post_number = row['reply_to_post_number']
        headline = row['headline']
        if not pd.isna(reply_to_post_number) and not pd.isna(headline):
            key = (reply_to_post_number, headline)
            if key in post_and_headline_to_cooked:
                return post_and_headline_to_cooked[key]
        return ""

    # Apply the function to create the "Parent Content" column in df1
    df1['parent_content'] = df1.apply(get_parent_content, axis=1)
    df1.fillna("", inplace=True)
    
    # Save the updated data, including the "cooked" and "Parent Content" columns, to the output CSV file
    df1.to_csv(output_csv_file, index=False)

# Execute the two cases based on a condition
case_1_worksheet_name = "oct_test"
case_2_input_csv_file = f"extracted_news_articles_{output_timestamp}.csv"
case_2_reference_csv_file = "old.csv"
case_2_output_csv_file = "final_extracted_articles.csv"

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('pagal_guy.json', scope)
client = gspread.authorize(creds)
worksheet = client.open('community forum').worksheet(case_1_worksheet_name)

if df_extracted['reply_to_post_number'].isin(df_extracted['post_number']).any():
    # Case 1: When there are matching values between 'reply_to_post_number' and 'post_number'
    output_csv_file = f"extracted_news_articles_{output_timestamp}.csv"
    handle_case_1(df_extracted, output_csv_file)
else:
    handle_case_2(case_2_input_csv_file, case_2_reference_csv_file, case_2_output_csv_file)
    

# After processing cases 1 and 2, you can continue with the code to update Google Sheets.
sheetname = "oct_test"
worksheet = client.open('community forum').worksheet(sheetname)

extracted_csv_file = f"extracted_news_articles_{output_timestamp}.csv"
final_csv_file = "final_extracted_articles.csv"

# Read both CSV files into DataFrames
df1 = pd.read_csv(extracted_csv_file)
df2 = pd.read_csv(final_csv_file)

# Concatenate the DataFrames vertically to create a union
final_df = pd.concat([df1, df2], ignore_index=True)

# Fill NaN values with empty strings
final_df.fillna("", inplace=True)
# Define the columns for checking duplicates (from the first column to the second-to-last column)
columns_to_check = final_df.columns[:-1]  # Exclude the last column

# Remove duplicates based on selected columns
final_df = final_df.drop_duplicates(subset=columns_to_check)

# Save the final DataFrame to a new CSV file (optional)
final_csv_union_file = "final_union_extracted_articles.csv"
final_df.to_csv(final_csv_union_file, index=False)

# Get column names from the final DataFrame
col = final_df.columns.tolist()

# Get data from the Google Sheets worksheet
values = worksheet.get_all_records()
sheet_from_gc = pd.DataFrame(values, columns=col)

# Merge the data from the Google Sheets worksheet and the final DataFrame
curr_data = pd.concat([final_df, sheet_from_gc]).drop_duplicates()

# Update the Google Sheets worksheet with the combined data
x = worksheet.update([curr_data.columns.values.tolist()] + curr_data.values.tolist())

print('Done appending data to Google Sheets:', sheetname)


