import os
import sys

# Add the project root to sys.path to allow absolute imports starting with 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from src.config_llm import get_response
from src.decisions.decision_maker import get_decision,decision_prompt
from src.tools.weather import weather_update
from src.tools.calculator import calculator
from src.tools.crypto import crypto_update

from src.state import State

# Nodes
def router_node(state: State):
    """ Routes the query to the correct tool or identifies it as general """
    print("\n[Node: Router] Analyzing query...")
    decision = get_decision(state["query"])
    return {
        "tool": decision.get("tool", "general"),
        "city": decision.get("city"),
        "expression": decision.get("expression"),
        "symbol": decision.get("crypto")
    }

def weather_node(state: State):
    """ Calls the weather tool """
    print(f"[Node: Weather] Fetching data for {state['city']}...")
    result = weather_update(state["city"])
    return {"tool_output": result}

def calculator_node(state: State):
    """ Calls the calculator tool """
    print(f"[Node: Calculator] Evaluating {state['expression']}...")
    result = calculator(state)
    return {"tool_output": result}

def crypto_node(state: State):
    """ Calls the crypto tool """
    print(f"[Node: Crypto] Fetching price for {state['symbol']}...")
    result = crypto_update(state["symbol"], state)
    return {"tool_output": result}

def general_node(state: State):
    """ Handles general queries using LLM directly """
    print("[Node: General] Generating direct response...")
    prompt = f"User asked: {state['query']}\nPlease provide a helpful and professional answer."
    response = get_response(prompt)
    return {"answer": response}

def responder_node(state: State):
    """ Synthesizes tool output into a natural response """
    print("[Node: Responder] Formatting final answer...")
    if state.get("answer"):
        return state
        
    tool_data = state.get("tool_output", {})
    prompt = f"""
    The user asked: {state['query']}
    The tool returned: {tool_data}
    
    Please provide a concise, friendly natural language response based on this data. 
    Standard units: Celsius for temperature, USD for prices.
    """
    response = get_response(prompt)
    return {"answer": response}

# Conditional Routing Logic
def route_to_tool(state: State) -> Literal["weather", "calculator", "crypto", "general"]:
    return state["tool"]

# Graph Construction
builder = StateGraph(State)

# Add all nodes
builder.add_node("router", router_node)
builder.add_node("weather", weather_node)
builder.add_node("calculator", calculator_node)
builder.add_node("crypto", crypto_node)
builder.add_node("general", general_node)
builder.add_node("responder", responder_node)

# Define transitions
builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_to_tool,
    {
        "weather": "weather",
        "calculator": "calculator",
        "crypto": "crypto",
        "general": "general"
    }
)

# Connect tools to responder
builder.add_edge("weather", "responder")
builder.add_edge("calculator", "responder")
builder.add_edge("crypto", "responder")

# Final outputs
builder.add_edge("general", END)
builder.add_edge("responder", END)

# Compile the graph
graph = builder.compile()

def run_agent(query: str):
    """ Entry point for the agent system """
    initial_state = {
        "query": query,
        "tool": "general",
        "city": "",
        "expression": "",
        "symbol": "",
        "tool_output": {},
        "answer": ""
    }
    result = graph.invoke(initial_state)
    return result["answer"]

if __name__ == "__main__":
    print("-" * 40)
    print("Multi-Agent AI System (LangGraph) Active")
    print("Commands: 'exit' or 'quit' to stop")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Shutting down...")
                break
                
            if not user_input.strip():
                continue
                
            response = run_agent(user_input)
            print(f"Agent: {response}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"System Error: {e}\n")