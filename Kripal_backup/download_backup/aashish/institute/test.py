import pandas as pd
import os

# Specify the folder containing the CSV files
folder_path = '/home/cd_scrapers/aashish/institute/output_data'

# List to hold dataframes
dfs = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Optional: Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)

print("Data from all CSV files combined successfully.")
