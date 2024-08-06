import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import praw
from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define your Google Sheets credentials and sheet details
sheet_id = "1weO_wbRBIUqsqntInqtTfARMFYKIwKy_XzKkfabJJno"
credentials_json_path = "C:/Users/Lenovo/Downloads/reddit_json.json"

# Authorize with Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credentials_json_path, SCOPES
)
client = gspread.authorize(credentials)

# Function to generate links based on keywords
def generate_links(keyword):
    base_url = 'https://www.reddit.com/search/?q='
    link = base_url + keyword.replace(' ', '+')
    return link

# Function to extract title links from Reddit
def get_data(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    timing = driver.find_element(By.XPATH, "/html/body/shreddit-app/dsa-transparency-modal-provider/search-dynamic-id-cache-controller/div/div/div[1]/div[1]/div/div[2]/div[1]/search-sort-dropdown-menu[2]/div/search-telemetry-tracker[5]/li/a")

    linkkk = timing.get_attribute('href')

    driver.get(linkkk)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title_links = []

    try:
        posts = soup.find_all('a', class_="text-16 xs:text-18 line-clamp-3 text-ellipsis text-neutral-content-strong font-semibold mb-xs no-underline hover:no-underline visited:text-neutral-content-weak")
        for post in posts:
            try:
                title_link = 'https://www.reddit.com' + post['href']
                title_links.append(title_link)
            except Exception as e:
                print(f"Error processing a post: {e}")
                continue
    except Exception as e:
        print(f"Error getting title links from {url}: {e}")

    driver.quit()
    return title_links

def extract_reddit_data(keyword, title_links):
    data = {'URL': [], 'Type':[], 'Post_ID': [], 'Title': [], 'Body': [], 'Upvotes':[], 'Comments': [], 'Date': [], 'Author': [], 'Keyword': []}
    comments = {'URL': [], 'Type':[], 'ID': [], 'Post_ID': [], 'Body': [], 'Upvotes':[], 'Author': [], 'Parent Comment': [], 'Parent Reply': [], 'Position': [], 'Keyword': []}

    # Replace with your Reddit app credentials
    reddit = praw.Reddit(user_agent=True, client_id='iduxVeKV1ADNVRD6mTGr-g', client_secret='728-3JvtRnWyA-Xf32c-4VIPyitwQw', username='SIDDHARTHJI')

    def flatten_comments(comment, flattened_comments, position=1):
        flattened_comments.append((comment, position))
        if not comment.replies:
            return
        for i, reply in enumerate(comment.replies):
            flatten_comments(reply, flattened_comments, f"{position}.{i+1}")

    def convert_to_date(created_date_in_seconds):
        datetime_obj = datetime.fromtimestamp(created_date_in_seconds)
        date_format = "%d-%m-%Y"
        return datetime_obj.strftime(date_format)

    for url in title_links:
        submission = reddit.submission(url=url)

        data['URL'].append(url)
        data['Type'].append('Main Post')
        data['Post_ID'].append(submission.id)
        try:
            data['Title'].append(submission.title)
        except:
            data['Title'].append(None)
        try:
            data['Body'].append(submission.selftext)
        except:
            data['Body'].append(None)
        data['Upvotes'].append(submission.score)
        data['Comments'].append(submission.num_comments)
        data['Date'].append(convert_to_date(submission.created_utc))
        try:
            data['Author'].append(submission.author.name)
        except:
            data['Author'].append(None)
        data['Keyword'].append(keyword)

        submission.comments.replace_more(limit=None)

        flattened_comments = []
        for top_level_comment in submission.comments:
            flatten_comments(top_level_comment, flattened_comments)

        parent_comment = " "
        parent_reply = " "
        for comment, position in flattened_comments:
            comments['URL'].append(url)
            comments['ID'].append(comment.id)
            comments['Post_ID'].append(submission.id)
            try:
                comments['Body'].append(comment.body)
            except:
                comments['Body'].append(None)
            comments['Upvotes'].append(comment.score)
            try:
                comments['Author'].append(comment.author.name)
            except:
                comments['Author'].append(None)
            comments['Keyword'].append(keyword)

            if comment.parent_id[3:] == submission.id:
                comments['Type'].append('Comment')
                comments['Parent Comment'].append(' ')
                comments['Parent Reply'].append(' ')
                parent_comment = comment.id
                parent_reply = " "
            else:
                comments['Type'].append('Reply')
                comments['Parent Comment'].append(parent_comment)
                comments['Parent Reply'].append(parent_reply)
                parent_reply = comment.id

            comments['Position'].append(position)

    df_main = pd.DataFrame(data)
    df_comments = pd.DataFrame(comments)

    # Update Google Sheets
    main_sheet_name = 'Main Data'
    comments_sheet_name = 'Comments Data'
    report_sheet_name = 'Report'

    main_sheet = client.open_by_key(sheet_id).worksheet(main_sheet_name)
    comments_sheet = client.open_by_key(sheet_id).worksheet(comments_sheet_name)
    try:
        report_sheet = client.open_by_key(sheet_id).worksheet(report_sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        report_sheet = client.open_by_key(sheet_id).add_worksheet(title=report_sheet_name, rows=1, cols=1)
        report_sheet.update('A1', [['Date', 'Keyword', 'Main Data Added', 'Comments Data Added']])

    # Fetch existing data
    main_existing_data = main_sheet.get_all_values()
    comments_existing_data = comments_sheet.get_all_values()

    # Convert existing data to DataFrames
    if main_existing_data:
        df_main_existing = pd.DataFrame(main_existing_data[1:], columns=main_existing_data[0])
        df_main_combined = pd.concat([df_main_existing, df_main], ignore_index=True)
        df_main_combined.drop_duplicates(subset=['URL'], keep='first', inplace=True)
        main_data_added = len(df_main_combined) - len(df_main_existing)
    else:
        df_main_combined = df_main
        main_data_added = len(df_main)

    if comments_existing_data:
        df_comments_existing = pd.DataFrame(comments_existing_data[1:], columns=comments_existing_data[0])
        df_comments_combined = pd.concat([df_comments_existing, df_comments], ignore_index=True)
        df_comments_combined.drop_duplicates(subset=['ID'], keep='first', inplace=True)
        comments_data_added = len(df_comments_combined) - len(df_comments_existing)
    else:
        df_comments_combined = df_comments
        comments_data_added = len(df_comments)

    # Write data to sheets
    main_sheet.update([df_main_combined.columns.values.tolist()] + df_main_combined.values.tolist())
    comments_sheet.update([df_comments_combined.columns.values.tolist()] + df_comments_combined.values.tolist())

    # Update the report sheet
    current_date = datetime.now().strftime("%d-%m-%Y")
    report_data = [current_date, keyword, main_data_added, comments_data_added]
    report_sheet.append_row(report_data, table_range="A2")

    print(f'Data saved for keyword "{keyword}"')

if __name__ == '__main__':
    df = pd.read_excel('C:/CollegeDunia/interns-task/Siddharth_Work/Reddit Project/keywords.xlsx')  # Update with the path to your CSV file
    for keyword in df['Keywords']:
        link = generate_links(keyword)
        title_links = get_data(link)
        extract_reddit_data(keyword, title_links)
