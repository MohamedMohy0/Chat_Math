import re

def convert_to_latex(text):
    lines = text.split('\n')
    latex_output = []

    math_keywords = ['^', '=', '√', 'sqrt', '\\pi', '\\cdot', '\\sqrt', '\\frac', '\\triangle', '±', '\\pm']

    for line in lines:
        original_line = line
        line = line.strip()
        if not line:
            continue

        # --- معالجة الصيغ الرياضية ---
        line = re.sub(r'(\d+)\^(\d+)', r'\1^{\2}', line)  # 10^2
        line = re.sub(r'([A-Za-z])\^(\d+)', r'\1^{\2}', line)  # AE^2
        line = re.sub(r'sqrt\((.*?)\)', r'\\sqrt{\1}', line)
        line = re.sub(r'√\((\d+)\s*/\s*(\d+)\)', r'\\sqrt{\\frac{\1}{\2}}', line)  # √(100/3)
        line = re.sub(r'√(-?\d+)', r'\\sqrt{\1}', line)  # √25 or √-75
        line = re.sub(r'±\s*√\((-?\d+)\)', r'\\pm \\sqrt{\1}', line)
        line = re.sub(r'±\s*sqrt\((-?\d+)\)', r'\\pm \\sqrt{\1}', line)
        line = re.sub(r'(\d+)\s*\*\s*([A-Za-z\\])', r'\1 \\cdot \2', line)
        line = line.replace("π", r"\pi")
        line = line.replace("Δ", r"\triangle ")
        line = line.replace("≠", r"\neq")
        line = line.replace("∪", r"$\cup$")
        line = line.replace("∩", r"$\cap$")
        line = line.replace("≤", r"\leq")
        line = line.replace("≥", r"\geq")
        line = line.replace("∈", r"\in")
        line = line.replace("∉", r"\notin")
        line = line.replace("⊂", r"\subset")
        line = line.replace("⊃", r"\supset")
        line = line.replace("→", r"\rightarrow")
        line = line.replace("←", r"\leftarrow")
        line = line.replace("⇔", r"\Leftrightarrow")


        # --- تحديد إن كان يحتوي رموز رياضية ---
        is_math = any(sym in line for sym in math_keywords)

        # إذا الجملة عبارة عن معادلة صريحة
        if re.match(r'^[A-Za-z0-9\s^=+*/().\\{}±√-]+$', line) and is_math:
            latex_output.append(f"$$ {line} $$")
        # إذا تحتوي على رموز رياضية بداخل جملة
        elif is_math:
            # فصل الرموز الرياضية في $...$
            parts = re.split(r'(\s+)', line)  # نحافظ على المسافات
            new_line = ''
            for part in parts:
                part = part.strip()
                if not part:
                    new_line += ' '
                    continue
                if any(op in part for op in math_keywords):
                    new_line += f"${part}$"
                else:
                    new_line += part + ' '
            latex_output.append(new_line.strip())
        # جملة نصية فقط
        else:
            latex_output.append(line)

    return '\n'.join(latex_output)




# LaTeX document wrapper
strat_problem = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{textcomp}
\usepackage{amssymb}
\usepackage{geometry}
\geometry{margin=1in}
\begin{document}
\section*{Problem}
"""

start_answer = r"""
\section*{Solution}
"""

end = r"""
\end{document}
"""

def full_latex(q_text,response):
    question = convert_to_latex(q_text)
    answer = convert_to_latex(response)
    full_latex_text= strat_problem + question + start_answer + answer + end

    return full_latex_text




