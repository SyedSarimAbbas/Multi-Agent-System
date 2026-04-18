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

# Map common tickers to CoinGecko IDs
TICKER_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "ada": "cardano",
    "dot": "polkadot",
    "matic": "polygon",
    "link": "chainlink",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "doge": "dogecoin",
    "avax": "avalanche-2",
    "trx": "tron",
    "shib": "shiba-inu",
    "ltc": "litecoin",
    "bch": "bitcoin-cash",
    "uni": "uniswap",
    "near": "near",
    "xlm": "stellar",
    "kas": "kaspa",
    "pepe": "pepe"
}

#=====================
# Crypto Tool Function
#=====================
def crypto_update(symbol: str, state: State):
    """ Returns The Current Price and Market Cap Of The Given Crypto """
    # Use symbol parameter or state fallback
    raw_symbol = (symbol or state.get("symbol") or "").lower().strip()
    
    # Resolve ticker to ID
    coin_id = TICKER_MAP.get(raw_symbol, raw_symbol)
    try:
        base_url = "https://api.coingecko.com/api/v3/simple/price"
        api_key = os.getenv("COINGECKO_API_KEY")
        
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "x_cg_demo_api_key": api_key
        }
        
        res = requests.get(base_url, params=params)
        data = res.json()

        if coin_id not in data:
            return {"success": False, "error": f"Coin '{raw_symbol}' (ID: {coin_id}) not found on CoinGecko"}

        return {
            "id": coin_id,
            "price": data[coin_id]["usd"],
            "market_cap": data[coin_id].get("usd_market_cap"),
            "success": True
        }   
    except Exception as e:
         return {"success": False, "error": f"Crypto API failed: {str(e)}"}

#=============
#Example Usage
#=============
if __name__ == "__main__":
    print(crypto_update("solana", {"symbol": "solana"}))