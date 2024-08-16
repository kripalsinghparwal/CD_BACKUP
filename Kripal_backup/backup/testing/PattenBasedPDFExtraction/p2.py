#image to text 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import fitz  # PyMuPDF
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import shutil  # Import shutil for file operations
import pandas as pd
import re

api_url = "https://www.imagetotext.info/api/imageToText"
api_key = "58b79c12489cd27e6b12a00a49efcced665a6cc1"

headers = {"Authorization": f"Bearer {api_key}"}
# Function to perform OCR using the image-to-text API
def ocr_image_api(image_path):
    try:
        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            response = requests.post(api_url, files=files, headers=headers)
            print(response)

            if response.status_code == 200:
                result = response.json()
                soup = BeautifulSoup(result['result'], "html.parser")
                req_text = " ".join((soup.text).splitlines())
                return req_text
            else:
                return ''
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        return ''
    

    # Function to extract images and text from PDF
def extract_images_and_text(pdf_path, output_folder):
    images_data = []
    os.makedirs(output_folder, exist_ok=True)
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(output_folder, f'page_{page_num + 1}.png')
        pix.save(image_path)

        image_text = ocr_image_api(image_path)
        images_data.append({"Page": page_num + 1, "Image": f'page_{page_num + 1}.png', "Text": image_text})
        os.unlink(image_path)

    return images_data


pdf_path = r'C:\Users\Kripal\Desktop\Kripal_backup\backup\testing\PattenBasedPDFExtraction\input_folder\63d1b60466701fdd399c86a23856d53e.pdf'
output_folder = r'C:\Users\Kripal\Desktop\Kripal_backup\backup\testing\PattenBasedPDFExtraction\images'
data = extract_images_and_text(pdf_path, output_folder)

# Example of the extracted text
extracted_text = data.copy()
# Function to parse the extracted text into questions and options
def parse_questions_options(extracted_text):
    question_pattern = re.compile(r'Question Number: (\d+) Question Id : \d+ Question Type: MCQ Option Shuffling: Yes Display Question Number: Yes Single Line Question Option: No Option Orientation: Vertical Correct Marks: \d+ Wrong Marks: \d+ (.*?)Options:', re.DOTALL)
    options_pattern = re.compile(r'Options: (.*?)$', re.DOTALL)
    
    questions = []
    for page_data in extracted_text:
        text = page_data['Text']
        page_questions = question_pattern.findall(text)
        prev_end = 0
        for question_number, question in page_questions:
            question_text = question.strip()
            options_match = options_pattern.search(text, prev_end)
            if options_match:
                options_text = options_match.group(1).strip()
                options = re.findall(r'\d+\.\s*(.*?)(?=\d+\.\s*|$)', options_text)
                choices = '\n'.join(options)
                questions.append({
                    'Page': page_data['Page'],
                    'Image': page_data['Image'],
                    'Question': question_text,
                    'Choices': choices
                })
                prev_end = options_match.end()
    
    return pd.DataFrame(questions)

# Parse the questions and options
df_questions = parse_questions_options(extracted_text)

filename = os.path.basename(pdf_path)

# Remove the file extension to get the desired string
desired_string = os.path.splitext(filename)[0]

print(desired_string)

# output_folder = r'C:\Users\Kripal\Desktop\CD_OFFICIAL_PROJECTS\pdf_Extraction\output_folder\JIPMER\{}'.format(desired_string)

df_questions.to_csv(r'C:\Users\Kripal\Desktop\Kripal_backup\backup\testing\PattenBasedPDFExtraction\output_folder\{}.csv'.format(desired_string))