import os
import re
import PyPDF2

data = {"id": [], "type": [], "text": []}

doc_path = r"C:\Users\tanma\OneDrive\Desktop\collegedunia\pdfextraction\docs"


def extract_pdf_content(doc_path):
    # get file name list
    file_list = os.listdir(doc_path)
    # Loop through the file list
    for file_name in file_list:
        file_path = os.path.join(doc_path, file_name)

        if os.path.isfile(file_path):
            # Read the content of the file
            pdfFileObj = open(file_path, "rb")
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            # length of pdf pages
            pdf_len = len(pdfReader.pages)
            for page_index in range(0, pdf_len+1):
                pageObj = pdfReader.pages[page_index]
                extracted_text = pageObj.extract_text()
                print(extracted_text)
                extract_id_and_type(extracted_text)

    pdfFileObj.close()


def extract_id_and_type(extracted_text):
    # Use regular expressions to extract Question Id and Question Type
    # question_number_pattern = r"Question Number\s*:\s*(\d+)?"
    question_id_pattern = r"Question Id : (\d+)"
    question_type_pattern = r"Question Type : (\w+)"

    # Find all matches in the output text
    # question_number_matches = re.findall(question_number_pattern, extracted_text)
    question_id_matches = re.findall(question_id_pattern, extracted_text)
    question_type_matches = re.findall(question_type_pattern, extracted_text)

    for i in range(len(question_id_matches)):
        data["id"].append(question_id_matches[i])
        data["type"].append(question_type_matches[i])


# main driver
extract_pdf_content(doc_path)
