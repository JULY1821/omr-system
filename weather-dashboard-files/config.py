import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'

# App Configuration
APP_TITLE = '🌤️ Weather Dashboard'
DEFAULT_CITY = 'Jakarta'
DEFAULT_UNITS = 'metric'  # metric for Celsius, imperial for Fahrenheit
TEMPERATURE_UNIT = '°C'
WIND_UNIT = 'm/s'

# UI Configuration
SIDEBAR_WIDTH = 300
MAX_FAVORITE_CITIES = 10
CACHE_DURATION = 600  # 10 minutes

# File Paths
DATA_DIR = 'data'
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.json')

# Create data directory if not exists
os.makedirs(DATA_DIR, exist_ok=True)
