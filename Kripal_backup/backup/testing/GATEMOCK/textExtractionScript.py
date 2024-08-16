############### Extracting text function using image to text api ###########
import requests
from PIL import Image
from bs4 import BeautifulSoup
import os

api_url = "https://www.imagetotext.info/api/imageToText"
api_key = "58b79c12489cd27e6b12a00a49efcced665a6cc1"

headers = {"Authorization": f"Bearer {api_key}"}
local_filename = "downloaded_image.jpg"
def extractText(imageUrl):
    imageUrl = imageUrl.strip()
    print('input image_url :', imageUrl)
    req_text = 'N/A'
    try:
        # Send a GET request to download the image
        response = requests.get(imageUrl)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Write the response content to a file
        with open(local_filename, "wb") as file:
            file.write(response.content)
        print("Image downloaded successfully!")

        # Open the image file and prepare to send it to the API
        with Image.open(local_filename) as img:
            with open(local_filename, "rb") as img_file:  # Open the image file in binary mode
                files = {"image": img_file}
                response = requests.post(api_url, files=files, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                soup = BeautifulSoup(result['result'], "html.parser")
                req_text = " ".join((soup.text).splitlines())
                # print("Extracted Text:")
                # print(req_text)
            else:
                print(f"API request failed. Status code: {response.status_code}")

        # Delete the image file
        os.remove(local_filename)
        print("Image file deleted.")
        return req_text

    except Exception as e:
        print(f"An error occurred: {e}")

# print("image_text: ", extractText("https://www.digialm.com/per/g01/pub/585/ASM/OnlineAssessment/M388/tkcimages/GA2Q8.jpg"))  



import pandas as pd
import time
mock_image_links_df = pd.read_csv("/home/cd_scrapers/GATE_MOCK/UrlData3.csv").fillna('N/A')
print(len(mock_image_links_df))
row_dict_list = []
for ind in mock_image_links_df.index:
    row_dict = dict()
    row_dict['exam_url'] = mock_image_links_df['exam_url'][ind]
    row_dict['subject'] = mock_image_links_df['subject'][ind]
    row_dict['question_type'] = mock_image_links_df['question_type'][ind]
    row_dict['question_img_url'] = mock_image_links_df['question_img_url'][ind]
    row_dict['option_url1'] = mock_image_links_df['option_url1'][ind]
    row_dict['option_url2'] = mock_image_links_df['option_url2'][ind]
    row_dict['option_url3'] = mock_image_links_df['option_url3'][ind]
    row_dict['option_url4'] = mock_image_links_df['option_url4'][ind]
    row_dict['question_text'] = extractText(mock_image_links_df['question_img_url'][ind])
    time.sleep(1)
    row_dict['option_1'] = extractText(mock_image_links_df['option_url1'][ind])
    time.sleep(1)
    row_dict['option_2'] = extractText(mock_image_links_df['option_url2'][ind])
    time.sleep(1)
    row_dict['option_3'] = extractText(mock_image_links_df['option_url3'][ind])
    time.sleep(1)
    row_dict['option_4'] = extractText(mock_image_links_df['option_url4'][ind])   
    time.sleep(1)     
    print(row_dict)
    row_dict_list.append(row_dict)
    data_df = pd.DataFrame(row_dict_list)
    print("data_df", data_df)
    data_df.to_csv("Data3.csv")