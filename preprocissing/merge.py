import os
import pandas as pd

# Folder containing Excel files
folder_path = r"D:\Gradution\Final project\preprocissing\test_data"  # Change this to your folder path
output_file = "Test_data.xlsx"  # Name of the output file

# Get a list of all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xls', '.xlsx'))]

# Initialize an empty list to store dataframes
dataframes = []

# Loop through each file and read it into a dataframe
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    dataframes.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dataframes, ignore_index=True)

# Save merged dataframe to a new Excel file
merged_df.to_excel(os.path.join(folder_path, output_file), index=False)

print(f"Merged {len(excel_files)} files into {output_file}")