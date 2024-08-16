import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import fitz  # PyMuPDF
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import shutil  # Import shutil for file operations

api_url = "https://www.imagetotext.info/api/imageToText"

# Set up the headers with the API key
api_key = '58b79c12489cd27e6b12a00a49efcced665a6cc1'
headers = {
    'Authorization': f'Bearer {api_key}'
}

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

# Function to clear the output folder
def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def update_google_sheets(dataframe, sheet_id, credentials_json_path, worksheet_name):
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_json_path, SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id)

    # Add a new worksheet with the specified name
    worksheet = sheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe.replace(np.nan, "N/A", inplace=True)  # Replace NaN values with "N/A"
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

def main(pdf_paths, sheet_id, sheet_link, credentials_json_path, output_folder):
    for idx, pdf_path in enumerate(pdf_paths, start=1):
        worksheet_name = f"Sheett{idx}"
        images_data = extract_images_and_text(pdf_path, output_folder)
        df = pd.DataFrame(images_data)

        # Update Google Sheets
        update_google_sheets(df, sheet_id, credentials_json_path, worksheet_name)

        # Clear the output folder for the next iteration
        clear_folder(output_folder)

        print(f"Data from {pdf_path} updated in Google Sheets: {sheet_link} in worksheet {worksheet_name}")

if __name__ == "__main__":
    pdf_paths = [
        r"C:\CollegeDunia\Pdf Pdf\30.pdf",
        r"C:\CollegeDunia\Pdf Pdf\31.pdf",
        r"C:\CollegeDunia\Pdf Pdf\32.pdf",
        r"C:\CollegeDunia\Pdf Pdf\33.pdf",
        r"C:\CollegeDunia\Pdf Pdf\34.pdf",
        r"C:\CollegeDunia\Pdf Pdf\35.pdf",
        r"C:\CollegeDunia\Pdf Pdf\36.pdf",
        r"C:\CollegeDunia\Pdf Pdf\37.pdf",
        r"C:\CollegeDunia\Pdf Pdf\38.pdf",
        r"C:\CollegeDunia\Pdf Pdf\39.pdf",






        # Add more PDF paths as needed
    ]
    sheet_id = "1B1nFortOOiBY3zUKXQLNjCBNGFrpDkC6QduBrWAi-Nk"
    sheet_link = "https://docs.google.com/spreadsheets/d/1B1nFortOOiBY3zUKXQLNjCBNGFrpDkC6QduBrWAi-Nk/edit?gid=0#gid=0"
    credentials_json_path = "C:/Users/Lenovo/Downloads/scienceandtech-404413-7dcb1e466d80.json"
    output_folder = "C:/CollegeDunia/Pdf Pdf/1"
    main(pdf_paths, sheet_id, sheet_link, credentials_json_path, output_folder)
