from typing import TypedDict

# Define the shared State for the Multi-Agent System
class State(TypedDict):
    query: str
    tool: str
    city: str
    expression: str
    symbol: str
    tool_output: dict
    answer: str
