import pandas as pd
import json

# Load JSON file
#replace the LOCATION for the json files path 
with open(r"LOCATION", "r", encoding="utf-8") as file:
    data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(data)

# Save as Excel file
df.to_excel("intermediate_algebra.xlsx", index=False)

print("Conversion successful! File saved as output.xlsx")
