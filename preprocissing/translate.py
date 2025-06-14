import re
import sympy as sp

def convert_latex_to_natural(text):
    """
    Converts a LaTeX-formatted math problem into a natural English explanation.
    """
    text = re.sub(r'\${1,2}', '', text)  # Remove LaTeX math delimiters
    text = re.sub(r'\\begin\{[^}]+\}', '', text)
    text = re.sub(r'\\end\{[^}]+\}', '', text)
    text = re.sub(r'\\(?!frac|boxed|sin|cos|tan|log)[a-zA-Z]+', '', text)
    text = re.sub(r'\\boxed\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\1 divided by \2', text)
    text = re.sub(r'\\cdot|\\times', ' times ', text)
    text = re.sub(r'\s*=\s*', ' equals ', text)
    text = re.sub(r'\^\{([^}]+)\}', r' to the power of \1', text)
    text = re.sub(r'(\w) to the power of 2', r'\1 squared', text)
    text = re.sub(r'(\w) to the power of 3', r'\1 cubed', text)
    text = re.sub(r'\\sin', 'sine', text)
    text = re.sub(r'\\cos', 'cosine', text)
    text = re.sub(r'\\tan', 'tangent', text)
    text = re.sub(r'\\log', 'logarithm', text)
    text = re.sub(r'\\left|\\right', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_vertical_asymptote_problem(problem):
    """
    Handles problems that ask about vertical asymptotes.
    """
    clean_problem = problem.replace('$', '')
    match = re.search(r'y\s*=\s*\\frac\{([^}]+)\}\{([^}]+)\}', clean_problem)
    if not match:
        return "Could not parse the rational function from the problem."
    
    num_str = match.group(1).strip()
    den_str = match.group(2).strip()
    x = sp.symbols('x')
    try:
        num_expr = sp.sympify(num_str)
        den_expr = sp.sympify(den_str)
    except Exception as e:
        return f"Error parsing expressions: {e}"
    
    fact_den = sp.factor(den_expr)
    vertical_asymptotes = sp.solve(den_expr, x)
    
    den_latex = sp.latex(den_expr)
    fact_den_latex = sp.latex(fact_den)
    
    explanation = (f"The denominator of the rational function factors into $ {den_latex} = {fact_den_latex} $. "
                   "Since the numerator is always nonzero, there is a vertical asymptote whenever the denominator is $0$, "
                   "which occurs for ")
    va_list = [f"$x = {sp.latex(va)}$" for va in vertical_asymptotes]
    explanation += " and ".join(va_list) + ". "
    explanation += (f"Therefore, the graph has $\\boxed{{{len(vertical_asymptotes)}}}$ vertical asymptote"
                    f"{'s' if len(vertical_asymptotes) != 1 else ''}.")
    
    explanation = explanation.replace('\\', '')
    
    return explanation

def process_problem(problem):
    """
    Processes a LaTeX-formatted math problem and produces a natural English explanation.
    """
    if re.search(r'vertical asymptote', problem, re.IGNORECASE):
        return process_vertical_asymptote_problem(problem)
    else:
        return convert_latex_to_natural(problem)

def main():
    """
    Main function:
      - Takes input from the user.
      - Processes the input into natural English.
      - Prints both the original and the converted versions.
    """
    print("Enter a LaTeX-formatted math problem (or type 'exit' to quit):")
    user_input = input("\nProblem: ")
    output = process_problem(user_input)
    print("\nConverted Explanation:")
    print(output)
    print("="*80)

if __name__ == "__main__":
    main()
