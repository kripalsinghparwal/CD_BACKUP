import bs4
import requests
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy

def clean_string(input_string):
    # Remove '\n' and '\t'
    cleaned_string = input_string.replace('\n', '').replace('\t', '')
    
    # Remove trailing spaces
    cleaned_string = cleaned_string.strip()
    
    return cleaned_string


headers = ["topic" ,"topic_link","date","replies","views","author","Post","reply to","reply"]
df = pd.DataFrame(columns=headers)

PATH = "C:\browserDrivers\chromedriver-win64\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()

# Set any desired capabilities
chrome_options.add_argument("--start-maximized")

# Create the WebDriver instance with options
driver = webdriver.Chrome(options=chrome_options)
# service = Service(executable_path=PATH)
# driver = webdriver.Chrome(PATH)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1gSLwGt2t7-kpU5RBtLx9lUwiXoX5a0HVaB8yfCeuBJM/edit#gid=1117659686"

# Define the name of the worksheet
worksheet_name = "gmat"

# Use credentials from a JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", "https://spreadsheets.google.com/feeds")

# Authenticate with Google Sheets
gc = gspread.authorize(credentials)

# Open the Google Sheets document by its URL
sh = gc.open_by_url(spreadsheet_url)

# Select the worksheet by name
worksheet = sh.worksheet(worksheet_name)
data = worksheet.get_all_values()

data.pop(0)
data = data[1:3]
for url_item in data:
    url = url_item[0]
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, "lxml")


    # Setting the number of stale date
    delta = 1

    #Getting the current date
    current_date = datetime.now()
    tags_list = soup.select(".last-post-time")
    links__element_list = soup.select(".topic-link")
    replies_list = soup.select(".topic-table-column.table-topic-row7")
    views_list = soup.select(".topic-table-column.table-topic-row8")
    dates_list = []
    links_list = []
    final_posts = []
    lists_of_temp_list = []
    for i in range(len(tags_list)):
        temp_list = []
        temp = tags_list[i].text
        dates_list.append(temp)
        date_obj = datetime.strptime(temp, '%d %b %Y, %H:%M')
        difference = (current_date - date_obj).days
        if(difference<=delta):
            links_list.append(links__element_list[i].get("href"))
            temp_list.append(links__element_list[i].text)
            temp_list.append(links__element_list[i].get("href"))
            temp_list.append(temp)
            temp_list.append(replies_list[i].text)
            temp_list.append(views_list[i].text)
            lists_of_temp_list.append(temp_list)
    print(lists_of_temp_list)
    temp_list_count = 0
    for i in range(len(links_list)):  
        driver.get(links_list[i])
        t = []
        time.sleep(2)
        page_buttons_list = driver.find_elements(By.CLASS_NAME,"numbers")
        temp_bool = True
        if(len(page_buttons_list)>0):
            page_number = len(page_buttons_list) // 2
            while(page_number>=(1) and temp_bool):
                page_buttons_list = driver.find_elements(By.CSS_SELECTOR,".numbers")
                page_buttons_list[page_number-1].click()
                page_number -= 1 
                time.sleep(4)
                posts = driver.find_elements(By.CLASS_NAME,"post-wrapper")
                posts.pop()
                # Sorting in accordance with the date
                posts.reverse()


                # Iterating over all the posts and getting the latest posts text
                for post in posts:
                    t = []
                    post_date = post.find_element(By.CLASS_NAME,"post-date").text
                    post_date = clean_string(post_date)
                    date_obj = datetime.strptime(post_date, '%d %b %Y, %H:%M')
                    difference = (current_date - date_obj).days
                    if(difference<=delta):
                        post_content = post.find_elements(By.CSS_SELECTOR,".item.text")
                        post_content = [element for element in post_content if 'quotetitle' not in element.get_attribute('class')]
                        post_content = post_content[0].text
                        post_content = clean_string(post_content)
                        user_name = post.find_element(By.CSS_SELECTOR,".poster-row.row-name").text
                        t = copy.deepcopy(lists_of_temp_list[temp_list_count])
                        t.append(user_name)
                        t.append(post_content)
                        try:
                            ex = post.find_element(By.CLASS_NAME,"quotetitle")
                            t.append(ex.text)
                        except Exception as e:
                             t.append("N.A")
                        try:
                            ex = post.find_element(By.CLASS_NAME,"quotecontent")
                            t.append(ex.text)
                        except Exception as e:
                             t.append("N.A")
                       
                        final_posts.append(t)
                        
                    else:
                        temp_bool = False
                        break


            
        else:
            # Extract from the given page only
            posts = driver.find_elements(By.CLASS_NAME,"post-wrapper")
            posts.pop()

            # Sorting in accordance with the date
            posts.reverse()


            # Iterating over all the posts and getting the latest posts text
            for post in posts:
                post_date = post.find_element(By.CLASS_NAME,"post-date").text
                post_date = clean_string(post_date)
                date_obj = datetime.strptime(post_date, '%d %b %Y, %H:%M')
                difference = (current_date - date_obj).days
                if(difference<=delta):
                    post_content = post.find_element(By.CSS_SELECTOR,".item.text").text
                    post_content = clean_string(post_content)
                else:
                    break
    temp_list_count+=1

for i in final_posts:
    df.loc[len(df)] = i




existing_worksheet_name = "Gmat Data"
existing_worksheet = sh.worksheet(existing_worksheet_name)
existing_data = existing_worksheet.get_all_values()

heading_cells = existing_worksheet.range(1, 1, 1, len(df.columns))

# Set the headings in the cells
for i, heading in enumerate(df.columns):
    heading_cells[i].value = heading

# Update the worksheet with the heading values
existing_worksheet.update_cells(heading_cells)

# Calculate the starting row for the DataFrame data (after the heading)
start_row = len(existing_data) + 1

# Calculate the starting column for the DataFrame data
start_col = 1
start_cell = existing_worksheet.cell(start_row, start_col)
end_cell = existing_worksheet.cell(start_row + len(df) - 1, start_col + len(df.columns) - 1)
range_str = f"{start_cell.address}:{end_cell.address}"

# Update the worksheet with the DataFrame data
existing_worksheet.update(range_str, df.values.tolist())