import json
import os
from datetime import datetime
from config import FAVORITES_FILE, MAX_FAVORITE_CITIES

class FavoritesManager:
    """
    Manages favorite cities stored in JSON file
    """
    
    @staticmethod
    def load_favorites():
        """
        Load favorites from JSON file
        Returns: list of favorite cities
        """
        if not os.path.exists(FAVORITES_FILE):
            return []
        
        try:
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    @staticmethod
    def save_favorites(favorites):
        """
        Save favorites to JSON file
        """
        os.makedirs(os.path.dirname(FAVORITES_FILE), exist_ok=True)
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(favorites, f, indent=2)
    
    @staticmethod
    def add_favorite(city):
        """
        Add city to favorites
        Returns: True if added, False if already exists or max reached
        """
        favorites = FavoritesManager.load_favorites()
        
        if city in favorites:
            return False
        
        if len(favorites) >= MAX_FAVORITE_CITIES:
            return False
        
        favorites.append(city)
        FavoritesManager.save_favorites(favorites)
        return True
    
    @staticmethod
    def remove_favorite(city):
        """
        Remove city from favorites
        Returns: True if removed, False if not found
        """
        favorites = FavoritesManager.load_favorites()
        
        if city not in favorites:
            return False
        
        favorites.remove(city)
        FavoritesManager.save_favorites(favorites)
        return True

class WeatherUtils:
    """
    Utility functions for weather data
    """
    
    @staticmethod
    def get_weather_icon(weather_description):
        """
        Get emoji icon for weather condition
        """
        weather_map = {
            'clear': '☀️',
            'sunny': '☀️',
            'cloud': '☁️',
            'cloudy': '☁️',
            'overcast': '☁️',
            'rain': '🌧️',
            'rainy': '🌧️',
            'drizzle': '🌦️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'snowy': '❄️',
            'sleet': '🌨️',
            'mist': '🌫️',
            'fog': '🌫️',
            'wind': '💨',
            'hail': '🧊'
        }
        
        description = weather_description.lower()
        for key, icon in weather_map.items():
            if key in description:
                return icon
        return '🌍'
    
    @staticmethod
    def get_wind_direction(degrees):
        """
        Convert wind degree to direction (N, NE, E, etc.)
        """
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    @staticmethod
    def format_time(timestamp):
        """
        Format Unix timestamp to readable time
        """
        return datetime.fromtimestamp(timestamp).strftime('%H:%M')
    
    @staticmethod
    def get_air_quality(humidity, pressure):
        """
        Simple air quality assessment based on humidity and pressure
        """
        if humidity > 80 or humidity < 20:
            return "😷 Poor"
        elif pressure < 1000:
            return "😐 Moderate"
        else:
            return "😊 Good"
    
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        """
        Convert Celsius to Fahrenheit
        """
        return (celsius * 9/5) + 32
    
    @staticmethod
    def get_uv_index_category(uv_index):
        """
        Categorize UV index
        """
        if uv_index < 3:
            return "🟢 Low"
        elif uv_index < 6:
            return "🟡 Moderate"
        elif uv_index < 8:
            return "🟠 High"
        elif uv_index < 11:
            return "🔴 Very High"
        else:
            return "🟣 Extreme"
