import pandas as pd
import json

# Load JSON file
with open(r"D:\Gradution\Final project\preprocissing\train_data\intermediate_algebra.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(data)

# Save as Excel file
df.to_excel("intermediate_algebra.xlsx", index=False)

print("Conversion successful! File saved as output.xlsx")
