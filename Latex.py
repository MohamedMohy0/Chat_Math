import re
import latexify
from pylatexenc.latexencode import unicode_to_latex

SPECIAL_LATEX_WORDS = {
    "triangle": r"\triangle",  # Triangle notation
    "degree": r"^\circ",  # Degree symbol
    "sqrt": r"\sqrt",  # Square root notation
    "frac": r"\frac",  # Fraction notation
}

def convert_to_latex(text):
    tokens = re.findall(r"[\w/()^*+-]+|.", text)  # Tokenize words and symbols separately
    converted_tokens = []

    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Handle common math words
        if token.lower() in SPECIAL_LATEX_WORDS:
            converted_tokens.append(SPECIAL_LATEX_WORDS[token.lower()])
            i += 1
            continue

        if token.isdigit() and i + 1 < len(tokens) and tokens[i + 1].lower() == "degree":
            converted_tokens.append(f"{token}{SPECIAL_LATEX_WORDS['degree']}")
            i += 2
            continue

        # Try converting Python expressions to LaTeX
        try:
            converted_token = f"${latexify.latexify(lambda: eval(token))}$"  # Use latexify-py
        except:
            converted_token = unicode_to_latex(token)

        converted_tokens.append(converted_token)
        i += 1

    return ' '.join(converted_tokens)




strat_problem=r"""
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section{Problem}

"""

start_answer=r"""
\section{Solution}


"""

end=r"""

\end{document}

"""

def full_latex(q_text,a_text):
    question=convert_to_latex(q_text)
    answer=convert_to_latex(a_text)

    full_latex_text=strat_problem+question+start_answer+answer+end

    return full_latex_text

