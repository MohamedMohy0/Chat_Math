import subprocess

def convert_latex_to_pdf(latex_code,out):
    with open("Out_put.tex", "w", encoding="utf-8") as f:
        f.write(latex_code)
    
    subprocess.run(["pdflatex", "Out_put.tex"], check=True)

#convert_latex_to_pdf(full_latex(q_text,a_text), "output.pdf")
