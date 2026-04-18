import os
import requests
from dotenv import load_dotenv
from typing import TypedDict

# Load environment variables from .env file
load_dotenv()

# Import State safely
try:
    from src.state import State
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from src.state import State


# =====================
# WEATHER TOOL FUNCTION
# =====================
def weather_update(city: str, state: State = None):
    """Returns current weather for a city using OpenWeatherMap API"""

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHERMAP_API_KEY"),
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Handle API errors safely
        if response.status_code != 200:
            return {
                "success": False,
                "error": data.get("message", "API request failed")
            }

        weather_summary = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "success": True
        }

        return weather_summary

    except Exception as err:
        return {
            "success": False,
            "error": f"Unexpected error: {str(err)}"
        }


# =============
# Example Usage
# =============
if __name__ == "__main__":
    result = weather_update("Karachi")

    if result["success"]:
        print(result)
    else:
        print(f"Error: {result['error']}")