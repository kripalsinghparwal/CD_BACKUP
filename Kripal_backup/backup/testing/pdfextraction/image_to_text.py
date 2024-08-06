import requests
import os
import re
import html
import pandas as pd
import PyPDF2
import os
import io
import fitz  # PyMuPDF
from PIL import Image

data = {"page": [], "text": []}

url = "https://www.imagetotext.info/api/imageToText"
api_key = "58b79c12489cd27e6b12a00a49efcced665a6cc1"

headers = {"Authorization": f"Bearer {api_key}"}

doc_path = r"C:\Users\Kripal\Desktop\testing\pdfextraction\docs"

photo_ids_folder = (
    r"C:\Users\Kripal\Desktop\testing\pdfextraction\input_folder"
)
output_folder = (
    r"C:\Users\Kripal\Desktop\testing\pdfextraction\output_folder"
)


# Function to extract text from PDF
def extract_images_from_pdfs(doc_path, output_dir="input_folder", output_format="png"):
    file_list = os.listdir(doc_path)

    for file in file_list:
        # Open the file
        pdf_file_path = os.path.join(doc_path, file)
        pdf_file = fitz.open(pdf_file_path)

        # Iterate over PDF pages
        for page_index in range(len(pdf_file)):
            # Get the page itself
            page = pdf_file[page_index]
            # Get image list
            image_list = page.get_images(full=True)

            # Print the number of images found on this page
            if image_list:
                print(
                    f"[+] Found a total of {len(image_list)} images in page {page_index}"
                )
            else:
                print(f"[!] No images found on page {page_index}")

            # Iterate over the images on the page
            for image_index, img in enumerate(image_list):
                # Get the XREF of the image
                xref = img[0]
                # Extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                # Get the image extension
                image_ext = base_image["ext"]
                # Load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # Check if the image meets the minimum dimensions and save it
                image.save(
                    open(
                        os.path.join(
                            output_dir,
                            f"{file}_page{page_index + 1}_image{image_index}.{output_format}",
                        ),
                        "wb",
                    ),
                    format=output_format.upper(),
                )
                # data["page"].append(page_index+1)


# Clearing all the files in the given Folder
def clear_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if it's a file (not a subdirectory)
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)


# Function to remove unnecessary spaces in the extracted text
def clean_text(input_text):
    # Remove extra spaces and newline characters
    cleaned_text = re.sub(r"\n+", "\n", input_text.strip())
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)
    return cleaned_text


# Function to extract the text and saving the data in a file.txt format
def extract_and_save_data(response_text, output_file_path):
    try:
        decoded_text = html.unescape(response_text).replace("<br />", "\n")
        print("decoded_text", decoded_text)
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(decoded_text)

        print(f"Data saved to: {output_file_path}")

    except Exception as e:
        print(f"Error extracting and saving data: {e}")


# Function to sort the file order and extract the file content in dictionary
def extract_textfile():
    print("length  of filelist", len(os.listdir(output_folder)))
    file_list = sorted(
        os.listdir(output_folder),
        key=lambda x: [
            int(part) if part.isdigit() else part
            for part in re.split(r"(_page|_image|\.)", x)
        ],
    )
    print("length of file lsit", len(file_list))
    for file_name in file_list:
        
        print("file_name", file_name)
        match = re.search(r'_page(\d+)_', file_name)
        # Check if a match is found
        if match:
            page_number = match.group(1)

        file_path = os.path.join(output_folder, file_name)
        if os.path.isfile(file_path):
            # Read the content of the file
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

                # Cleaning the text from the text file
                clean_file_content = clean_text(file_content)

                # Append the file content to the data dictionary
                data["text"].append(clean_file_content)
                data["page"].append(page_number)

    lengths = {key: len(value) for key, value in data.items()}
    if len(set(lengths.values())) > 1:
        print("Error: All arrays must be of the same length")
        return

    df = pd.DataFrame(data)
    print("length of df", len(df))
    df.to_csv("Extraced_text.csv", sep=",", index=False, encoding="utf-8")


# uploading the images in the input file and converting the images to text
def upload_and_process_image(file_path):
    try:
        with open(file_path, "rb") as image_file:
            files = {"image": (file_path, image_file)}
            response = requests.post(url, headers=headers, files=files)

            # Check if the error is false in the response
            if "error" in response.json() and response.json()["error"] is False:
                result_text = response.json()["result"]
                print(result_text)
                # Construct the output file path
                print(
                    "output_file_path1",
                    os.path.join(
                        output_folder,
                        f"{os.path.splitext(os.path.basename(file_path))[0]}.txt",
                    ),
                )
                output_file_path = os.path.join(
                    output_folder,
                    f"{os.path.splitext(os.path.basename(file_path))[0]}.txt",
                )
                # Extract and save the data to a file
                print("output_file_path", output_file_path)
                extract_and_save_data(result_text, output_file_path)
            else:
                print("Error in response:", response.text)

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error uploading image: {e}")


# MAIN DRIVER
if __name__ == "__main__":
    # Clearing the photos_ids_folder path
    # clear_folder(photo_ids_folder)

    # Claering the output_folder path
    # clear_folder(output_folder)

    # using getimages.py function
    # extract_images_from_pdfs(doc_path)

    # os.makedirs(output_folder, exist_ok=True)
    # for filename in os.listdir(photo_ids_folder):
    #     if filename.endswith((".jpg", ".jpeg", ".png")):
    #         file_path = os.path.join(photo_ids_folder, filename)
    #         upload_and_process_image(file_path)

    extract_textfile()
