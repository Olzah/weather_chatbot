import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def get_current_weather(location):
    open_weat_map_key = os.environ.get("OPEN_WEATHER_MAP_KEY")
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    base_url_forecast = 'http://api.openweathermap.org/data/2.5/forecast'
    try:
        params = {"q": location, 
                "units": "metric",
                "appid": open_weat_map_key}
        response = requests.get(base_url_forecast, params=params)
        response_json = response.json()
        return response_json
    except Exception as e:
        raise e
