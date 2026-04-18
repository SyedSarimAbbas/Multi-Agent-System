import os

try:
    from src.state import State
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from src.state import State

#====================
# Calculator Function
#====================
def calculator(state: State):
    """ Performs The Calculation For The Given Inputs """
    try:
        expression = state["expression"]
        result = eval(expression)
        return {
            "answer": result
        }
    except Exception as e:
        return {
             f"Error Occured: {e}"
        }   

#==============
# Example Usage
#==============   
if __name__ == "__main__":
    print(calculator({"expression": "22222/12*756"}))    