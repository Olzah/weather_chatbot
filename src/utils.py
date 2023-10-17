import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def get_current_weather(location, format):
    open_weat_map_key = os.environ.get("OPEN_WEATHER_MAP_KEY")
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    try:
        params = {"q": location,
                  "units": "metric" if format == "celsius" else "imperial",
                  "appid": open_weat_map_key}
        response = requests.get(base_url, params=params)
        response_json = response.json()
        return response_json
    except Exception as e:
        raise e
    
def get_n_day_weather_forecast(location, format, day):
    open_weat_map_key = os.environ.get("OPEN_WEATHER_MAP_KEY")
    base_url_forecast = 'http://api.openweathermap.org/data/2.5/forecast'
    try:
        params = {"q": location, 
                  "units": "metric" if format == "celsius" else "imperial",
                  "appid": open_weat_map_key}
        response = requests.get(base_url_forecast, params=params)
        response_json = response.json()
        result = response_json
        for forecast in result['list']:
            forecast_date = forecast['dt_txt'].split()[0]
            if forecast_date == day:
                return json.dumps(forecast)
    except Exception as e:
        raise e
