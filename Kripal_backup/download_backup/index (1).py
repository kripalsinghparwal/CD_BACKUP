import tabula
import pandas as pd
# Specify the path to your PDF file
pdf_path = './file.pdf'

# Define predefined column names
column_names = ["Sr.No","AIR","Roll No.","CET form No.","Name","Gender","Category","Quota","Code College"]

# Use the read_pdf function to extract tables from the PDF with predefined column names
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
new_tables = []
for i, df in enumerate(tables, start=1):
    # Extract column headers
    column_headers = df.columns.tolist()

    # Append column headers as the first row
    df.loc[-1] = column_headers
    df.index = df.index + 1
    df = df.sort_index()

    # Change column headers (modify as needed)
    column_names = ["Sr.No","AIR","Roll No.","CET form No.","Name","Gender","Category","Quota","Code College"]
    df.columns = column_names
    new_tables.append(df)

combined_df = pd.concat(new_tables, ignore_index=True)

csv_path = './data.csv'

# Convert the DataFrame to a CSV file
combined_df.to_csv(csv_path, index=False)