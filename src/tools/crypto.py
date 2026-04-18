import os
import requests
from dotenv import load_dotenv

try:
    from src.state import State
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from src.state import State

load_dotenv()

#=====================
# Crypto Tool Function
#=====================
def crypto_update(symbol: str, state: State):
    """ Returns The Current Price and Market Cap Of The Given Crypto """
    coin = state["symbol"].lower()
    try:
        base_url = "https://api.coingecko.com/api/v3/simple/price"
        api_key = os.getenv("COINGECKO_API_KEY")
        
        params = {
            "ids": coin,
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "x_cg_demo_api_key": api_key
        }
        
        res = requests.get(base_url, params=params)
        data = res.json()

        if coin not in data:
            return {"success": False, "error": f"Coin '{coin}' not found on CoinGecko"}

        return {
            "id": coin,
            "price": data[coin]["usd"],
            "market_cap": data[coin].get("usd_market_cap"),
            "success": True
        }   
    except Exception as e:
         return {"success": False, "error": f"Crypto API failed: {str(e)}"}

#=============
#Example Usage
#=============
if __name__ == "__main__":
    print(crypto_update("solana", {"symbol": "solana"}))