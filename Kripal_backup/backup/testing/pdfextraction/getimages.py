import os
import io
import fitz  # PyMuPDF
from PIL import Image

def extract_images_from_pdfs(doc_path, output_dir="input_folder", output_format="png"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
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
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print(f"[!] No images found on page {page_index}")
            
            # Iterate over the images on the page
            for image_index, img in enumerate(image_list, start=1):
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

# Example usage:
doc_path = r"C:\Users\tanma\OneDrive\Desktop\collegedunia\pdfextraction\docs"
extract_images_from_pdfs(doc_path)
