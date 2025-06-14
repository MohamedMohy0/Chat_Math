from openai import OpenAI
import time


api_key = ""
import os
import json

# Path to the directory where JSON files are located
folder_path = "prealgebra/"

# List to store all the JSON data
json_data = []

# Loop through the files in the folder
for file in os.listdir(folder_path):
    if file.endswith('.json'):
        json_file_path = os.path.join(folder_path, file)
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            json_data.append(data)

# Get all folders (subdirectories) in the directory
folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
data=[]

for i in range (0,250):
    try:
        q=json_data[i]["problem"]
        a=json_data[i]["solution"]
        client = OpenAI(api_key=api_key,base_url="https://api.groq.com/openai/v1")
        chat_completion1 = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content":f"write this quistion in english correct way {q} and fix it i dont want it latex i want it in english only return the question",
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )
        question=chat_completion1.choices[0].message.content
        time.sleep(2)
        chat_completion2 = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content":f"write this answer in english correct way {a} and fix it i dont want it latex i want it in english only return the answer",
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )
        answer=chat_completion2.choices[0].message.content
        data.append({"question": question, "answer": answer})
        time.sleep(2)
    except:
        print(i)
        break

with open('prealgebra_test.json', 'a') as json_file:
    json.dump(data, json_file, indent=4)

print("Data saved to 'prealgebra_test.json'")
