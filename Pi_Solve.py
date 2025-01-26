import streamlit as st
import time
from groq import Groq
from openai import OpenAI
import subprocess
api_key = "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"
def convert_latex_to_pdf(latex_code):
        pdflatex_path = r"C:\Users\Mohamed\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"
        
        # Write the LaTeX code to a temporary .tex file with UTF-8 encoding
        with open("Out_put.tex", "w", encoding="utf-8") as f:
            f.write(latex_code)
        
        # Call pdflatex to convert .tex to .pdf
        subprocess.run([pdflatex_path, "Out_put.tex"], check=True)

        # Rename the output PDF to the desired filename
        # subprocess.run(["mv", "Out_put.pdf", "Out_put.pdf"], check=True)

        # Clean up the temporary files
        # subprocess.run(["rm", "Out_put.tex", "Out_put.aux", "Out_put.log"], check=True)
st.markdown(
    """
    <h1 style="text-align: center; ">PiSolve.AI</h1>
    """, 
    unsafe_allow_html=True
)



st.write("### Write your Question:")
user_question = st.text_area("", height=100)

if st.button("Submit"):
    st.spinner("Solving...")
    if user_question:
        st.write(f"**You asked:** {user_question}")
        response_placeholder = st.empty()  
        typing_speed = 0.055  

        client = OpenAI(api_key=api_key,base_url="https://api.groq.com/openai/v1")
        chat_completion = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content": user_question,
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )
        full_response = ""
        response=chat_completion.choices[0].message.content
        response_placeholder.markdown(
                f"""<p style="font-size: 22px;"> </p>""",
                unsafe_allow_html=True
            )
        for char in response:
            full_response += char
            response_placeholder.markdown(
                f"""<p style="font-size: 22px;">{full_response}</p>""",
                unsafe_allow_html=True
            )
            time.sleep(typing_speed)

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content" :f"""convert this {user_question} and
                            convert this {response} to a true latex code formula from a to z and make it like question and answer
                            and only return the code and make sure it ready to run and add amsmath package
                            i want the code of latex only and write it in buetfial way 
                        """
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
        )

        latex=chat_completion.choices[0].message.content
        # latex=latex.replace("##","\\")
        latex=latex.replace("latex","")
        # latex=latex.replace("\"","")
        latex=latex.replace(latex[0:3],"")
        latex=latex.replace(latex[-1:-4],"")

        # print(latex)
        file=open("test.txt","w")
        file.write(latex)
        file.close()

        convert_latex_to_pdf(latex)
        pdf_file="Out_put.pdf"
        with open(pdf_file, "rb") as file:
            pdf_data = file.read()
        down=st.download_button("Download The Solve ",file_name=pdf_file,data=pdf_data)

    else:
        st.warning("Please type a question before submitting.")

