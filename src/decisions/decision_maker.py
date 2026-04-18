from langchain_core.prompts import ChatPromptTemplate

decision_prompt = ChatPromptTemplate.from_template("""
You are a High-Precision Logic Router for a Multi-Agent System. 
Your sole responsibility is to analyze the user input and dispatch it to the correct specialized tool.

### AVAILABLE TOOLS
1. **calculator**: Trigger for mathematical expressions, arithmetic, or numerical comparisons.
2. **weather**: Trigger for current weather, temperature, or atmospheric conditions for a specific location.
3. **crypto**: Trigger for current market prices, market caps, or performance of cryptocurrencies.

### EXTRACTION RULES
- **city**: Extract the primary geographical location. Standardize to "City, Country" if possible (e.g., "Karachi, Pakistan"). Set to null if not found.
- **expression**: Extract the raw mathematical string (e.g., "500 * 1.15"). Set to null if not found.
- **symbol**: Extract the full name or ticker of the cryptocurrency (e.g., "bitcoin" or "solana"). Set to null if not found.

### OUTPUT FORMAT
You must return a raw JSON object. Do not include markdown code blocks, preambles, or post-scripts.

{{
  "tool": "calculator" | "weather" | "crypto" | "general",
  "city": string | null,
  "expression": string | null,
  "crypto": string | null
}}

### EXAMPLES
Question: "What is the price of Solana?"
JSON: {{"tool": "crypto", "city": null, "expression": null, "crypto": "solana"}}

Question: "How's the weather in Karachi?"
JSON: {{"tool": "weather", "city": "Karachi", "expression": null, "crypto": null}}

### INPUT
Question: {question}
""")


def get_decision(query: str):
    """ Analyzes query and determines the correct tool with extracted params """
    from ..config_llm import get_response
    import json
    
    # Format prompt and get LLM response
    prompt = decision_prompt.format(question=query)
    response_text = get_response(prompt)
    
    try:
        # Clean JSON blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[-1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[-1].split("```")[0]
            
        data = json.loads(response_text.strip())
        return data
    except Exception as e:
        print(f"Routing Error: {e}")
        return {"tool": "general", "city": None, "expression": None, "crypto": None}


if __name__ == "__main__":
    # Test cases
    print(get_decision("How is the weather in Karachi?"))
    print(get_decision("Calculate 500 * 1.15"))