import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0.5,
    max_tokens = 1024,
    api_key = os.getenv("GROQ_API_KEY"),
    streaming= True
)

def get_response(prompt: str) -> str:
    """ Returns Response From LLM """
    try:
        print("Sending Prompt to LLM...")
        response = llm.invoke(prompt)
        print("Response Received!")
        return response.content
    except Exception as e:
        print(f"Error: {e}")    

if __name__ == "__main__":
    print(get_response("Can you tell me about what are Autonomous Ai agents?"))