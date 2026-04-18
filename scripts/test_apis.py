import os
import sys
from dotenv import load_dotenv

# Add backend directory to path so 'src' can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

from src.config_llm import get_response
from src.tools.weather import weather_update
from src.tools.crypto import crypto_update

def test_api_status():
    load_dotenv()
    print("=" * 50)
    print("Multi-Agent AI System: API Diagnostics")
    print("=" * 50)

    # 1. Test Groq (LLM)
    print("\n1. Testing Groq / Llama-3.1-8b...")
    try:
        response = get_response("Say 'Online'")
        if response and "Online" in response:
            print("[OK] Groq API: WORKING")
        else:
            print("[FAIL] Groq API: FAILED (Unexpected response)")
            print(f"Debug: {response}")
    except Exception as e:
        print(f"[FAIL] Groq API: FAILED ({e})")

    # 2. Test OpenWeatherMap
    print("\n2. Testing OpenWeatherMap API...")
    try:
        res = weather_update("London")
        if res.get("success"):
            print(f"[OK] OpenWeatherMap: WORKING (Temp: {res.get('temperature')}°C)")
        else:
            print(f"[FAIL] OpenWeatherMap: FAILED ({res.get('error')})")
    except Exception as e:
        print(f"[FAIL] OpenWeatherMap: FAILED ({e})")

    # 3. Test CoinGecko (Crypto)
    print("\n3. Testing CoinGecko API with ticker 'sol'...")
    try:
        # Testing the new ticker mapping logic
        mock_state = {"symbol": "sol"}
        res = crypto_update("sol", mock_state)
        if res.get("success"):
            print(f"[OK] CoinGecko: WORKING (Bitcoin Price: ${res.get('price')})")
        else:
            print(f"[FAIL] CoinGecko: FAILED ({res.get('error')})")
    except Exception as e:
        print(f"[FAIL] CoinGecko: FAILED ({e})")

    print("\n" + "=" * 50)
    print("Diagnostic Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_api_status()
