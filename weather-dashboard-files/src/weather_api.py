import requests
import pandas as pd
from datetime import datetime
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, DEFAULT_UNITS

class WeatherAPI:
    """
    WeatherAPI class to interact with OpenWeatherMap API
    """
    
    def __init__(self, api_key=OPENWEATHER_API_KEY):
        self.api_key = api_key
        self.base_url = OPENWEATHER_BASE_URL
        self.units = DEFAULT_UNITS
    
    def get_current_weather(self, city):
        """
        Get current weather for a city
        Returns: dict with weather data or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def get_forecast(self, city):
        """
        Get 5-day forecast for a city
        Returns: dict with forecast data or None if error
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat, lon):
        """
        Get weather by latitude and longitude
        Returns: dict with weather data or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather by coordinates: {e}")
            return None
    
    @staticmethod
    def parse_current_weather(data):
        """
        Parse current weather data into readable format
        """
        if not data or 'main' not in data:
            return None
        
        return {
            'city': data.get('name', 'Unknown'),
            'country': data.get('sys', {}).get('country', ''),
            'temperature': data['main'].get('temp', 0),
            'feels_like': data['main'].get('feels_like', 0),
            'temp_min': data['main'].get('temp_min', 0),
            'temp_max': data['main'].get('temp_max', 0),
            'humidity': data['main'].get('humidity', 0),
            'pressure': data['main'].get('pressure', 0),
            'weather': data['weather'][0].get('main', ''),
            'description': data['weather'][0].get('description', ''),
            'wind_speed': data['wind'].get('speed', 0),
            'wind_deg': data['wind'].get('deg', 0),
            'clouds': data.get('clouds', {}).get('all', 0),
            'visibility': data.get('visibility', 0),
            'sunrise': data['sys'].get('sunrise', 0),
            'sunset': data['sys'].get('sunset', 0),
            'timestamp': data.get('dt', 0)
        }
    
    @staticmethod
    def parse_forecast(data):
        """
        Parse forecast data into DataFrame
        """
        if not data or 'list' not in data:
            return None
        
        forecasts = []
        for item in data['list']:
            forecasts.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'weather': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
                'wind_speed': item['wind']['speed'],
                'clouds': item['clouds']['all']
            })
        
        return pd.DataFrame(forecasts)
