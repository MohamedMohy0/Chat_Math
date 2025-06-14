import re
import sympy as sp


def convert_latex_to_natural(text):
    
    # --- Handle specific LaTeX commands (even if double-escaped) ---
    text = re.sub(r'(\\)+pi', '\u03C0', text)  # Replace \pi (or \\pi, etc.) with π
    text = re.sub(r'(\\)+leq', 'less than or equal to', text)
    text = re.sub(r'(\\)+geq', 'greater than or equal to', text)
    text = re.sub(r'(\\)+implies', 'implies', text)
    
    # --- Remove LaTeX math delimiters and environments ---
    text = re.sub(r'\${1,2}', '', text)
    text = re.sub(r'\\begin\{[^}]+\}', '', text)
    text = re.sub(r'\\end\{[^}]+\}', '', text)
    
    # --- Remove other LaTeX commands except for allowed ones ---
    # Allowed: frac, boxed, sin, cos, tan, log
    text = re.sub(r'\\(?!frac|boxed|sin|cos|tan|log)[a-zA-Z]+', '', text)
    
    # --- Process boxed and fraction commands ---
    text = re.sub(r'\\boxed\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\1 divided by \2', text)
    # Handle nonstandard fraction notation such as "frac{1{2}}"
    text = re.sub(r'frac\{([^{}]+)\{([^{}]+)\}\}', r'\1 divided by \2', text)
    
    # --- Convert simple slash fractions (e.g., "1/2") into words ---
    text = re.sub(r'(\d+)\s*/\s*(\d+)', r'\1 divided by \2', text)
    
    # --- Replace multiplication symbols ---
    text = re.sub(r'\\cdot|\\times', ' times ', text)
    
    # --- Replace equals sign with the word "equals" ---
    text = re.sub(r'\s*=\s*', ' equals ', text)
    
    # --- Remove stray backslashes before digits (match one or more backslashes) ---
    text = re.sub(r'\\+(\d)', r'\1', text)
    text = re.sub(r'\\+', '', text)  # Remove all backslashes

    # --- Remove spurious "equals" in fraction phrases ---
    # This converts "divided by equals" (with optional spaces) into "divided by"
    text = re.sub(r'(divided by)\s*equals\s*', r'\1 ', text)
    
    # --- Handle exponents ---
    text = re.sub(r'\^\{([^}]+)\}', r' to the power of \1', text)
    text = re.sub(r'(\w) to the power of 2', r'\1 squared', text)
    text = re.sub(r'(\w) to the power of 3', r'\1 cubed', text)
    
    # --- Replace common function commands with natural language ---
    text = re.sub(r'\\sin', 'sine', text)
    text = re.sub(r'\\cos', 'cosine', text)
    text = re.sub(r'\\tan', 'tangent', text)
    text = re.sub(r'\\log', 'logarithm', text)
    
    # --- Remove any remaining \left or \right commands ---
    text = re.sub(r'\\left|\\right', '', text)
    
    # --- Convert plus and minus signs into words ---
    text = re.sub(r'(\w)\s*\+\s*(\w)', r'\1 plus \2', text)
    text = re.sub(r'(\w)\s*-\s*(\w)', r'\1 minus \2', text)
    
    # --- Insert missing equals signs in certain cases ---
    text = re.sub(r'(\d+\([^)]+\))\s+(less than or equal to|greater than or equal to|\d+)', r'\1 equals \2', text)
    
    # --- Final pass: insert an "equals" before a trailing standalone number if missing ---
    def insert_equals(sentence):
        sentence_strip = sentence.rstrip('.')
        if re.search(r'\b\d+\b$', sentence_strip) and "equals" not in sentence_strip:
            sentence_strip = re.sub(r'(\b\d+\b)$', r' equals \1', sentence_strip)
            sentence = sentence_strip + '.'
        return sentence

    sentences = re.split(r'(?<=[.])\s+', text)
    sentences = [insert_equals(s) for s in sentences]
    text = " ".join(sentences)
    
    # --- Normalize extra whitespace ---
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