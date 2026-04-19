import os
import re
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Import State safely
try:
    from src.state import State
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from src.state import State

def calculator(state: State):
    """
    Performs mathematical calculations, including symbolic math like derivatives
    using sympy.
    """
    try:
        expression = state.get("expression", "")
        if not expression:
            return {"success": False, "error": "No mathematical expression provided"}

        # Basic cleaning
        # Convert ^ to ** for powers
        clean_expr = expression.replace("^", "**")
        
        # Check for derivative keywords
        is_derivative = False
        target_var = "x" # Default variable
        
        # Keywords to detect derivative requests
        der_patterns = [r"derivate", r"derivative", r"diff\b", r"d/d([a-zA-Z])"]
        for pattern in der_patterns:
            match = re.search(pattern, clean_expr, re.IGNORECASE)
            if match:
                is_derivative = True
                if match.groups():
                    target_var = match.group(1)
                # Remove the keyword from the expression to isolate the formula
                clean_expr = re.sub(pattern, "", clean_expr, flags=re.IGNORECASE).strip()
                break
        
        # Clean up any "of" or "with respect to" leftovers
        clean_expr = re.sub(r"\b(of|with respect to|w\.r\.t|wr|for)\b", "", clean_expr, flags=re.IGNORECASE).strip()

        # Sympy parsing with implicit multiplication (e.g., 2xy -> 2*x*y)
        transformations = (standard_transformations + (implicit_multiplication_application,))
        parsed_expr = parse_expr(clean_expr, transformations=transformations)
        
        if is_derivative:
            var_sym = sympy.Symbol(target_var)
            result = sympy.diff(parsed_expr, var_sym)
            operation = f"Derivative of {parsed_expr} with respect to {target_var}"
        else:
            # Try to simplify or evaluate
            result = parsed_expr.evalf() if parsed_expr.is_number else sympy.simplify(parsed_expr)
            operation = "Calculation / Simplification"

        return {
            "success": True,
            "operation": operation,
            "expression": str(parsed_expr),
            "answer": str(result),
            "raw_result": str(result)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Math Error: {str(e)}",
            "details": "Ensure the expression is valid (e.g., use 'x^2' or '2*x')."
        }

if __name__ == "__main__":
    # Test cases
    print("Test 1 (Basic):", calculator({"expression": "22222/12*756"}))
    print("Test 2 (Algebra):", calculator({"expression": "x^2 + 2x + 1"}))
    print("Test 3 (Derivative):", calculator({"expression": "derivate of x^2 + 2xy + 46yx"}))