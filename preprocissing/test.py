from openai import OpenAI

# Write here the api key
api_key = ""

q=input("enter the question: ")
a=input("Enter The Answer: ")
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
question=chat_completion1.choices[0].message.content

print("The question after preprocessing")
print(question)
print("____________________________________________________________")
print("The answer after preprocessing")
print(answer)