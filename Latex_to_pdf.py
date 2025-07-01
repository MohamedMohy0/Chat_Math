import subprocess
import streamlit as st
try:
    def convert_latex_to_pdf(latex_code,out):
        with open("Out_put.tex", "w", encoding="utf-8") as f:
            f.write(latex_code)
        
        subprocess.run(["pdflatex", "Out_put.tex"], check=True)
except:
    st.error("There is an error when convert the answer to latex please try again")