import streamlit as st
import time
#
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <h1 style="text-align: center; ">Chat Math</h1>
    """, 
    unsafe_allow_html=True
)



st.write("### Write your Question:")
user_question = st.text_area("", height=100)
col1, col2, col3 = st.columns([1, 5, 1]) 


with col3:
    on = st.toggle("LaTeX")

with col1:
    sumbit=st.button("Submit")
    
if on :
    from translate import process_problem
    user_question=process_problem(user_question)

if sumbit:
    with st.spinner("Solving..."):
        from trained import get_answer
        from Latex import full_latex
        from Latex_to_pdf import convert_latex_to_pdf
        from Checker import check
        kind=check(user_question)
        kind.replace(".","")
        if kind.lower()=="yes":
            st.write(f"**You asked:** {user_question}")
            response_placeholder = st.empty()  
            typing_speed = 0.055  
            response=get_answer(user_question)
            full_response = ""
            for char in response:
                full_response += char
                response_placeholder.markdown(
                    f"""<p style="font-size: 22px;">{full_response}</p>""",
                    unsafe_allow_html=True
                )
                time.sleep(typing_speed)


            full=full_latex(user_question,response)
            
            convert_latex_to_pdf(full, "output.pdf")
            pdf_file="Out_put.pdf"
            with open(pdf_file, "rb") as file:
                pdf_data = file.read()
            down=st.download_button("Download The Solve ",file_name=pdf_file,data=pdf_data)
        elif user_question=="":
            st.warning("Please type a question before submitting.")
        elif kind.lower()=="no":
            st.warning("This model not trained for this kind of questions.")


