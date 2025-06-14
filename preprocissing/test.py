from openai import OpenAI
import time


api_key = "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"

q=input("enter the question:")
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

print(question)
