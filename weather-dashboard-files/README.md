# Weather Dashboard

A beautiful, interactive weather dashboard built with Streamlit that fetches real-time weather data from OpenWeatherMap API.

## 🌟 Features

✅ **Real-time Weather Data** - Current weather conditions for any city
✅ **5-Day Forecast** - Detailed weather predictions with interactive charts
✅ **Search Functionality** - Easy city search with error handling
✅ **Favorite Cities** - Save and manage your favorite locations
✅ **Beautiful UI** - Responsive design with custom styling
✅ **Interactive Charts** - Plotly visualizations for temperature, humidity, wind
✅ **Detailed Metrics** - Temperature, humidity, pressure, wind speed, visibility, and more
✅ **Weather Icons** - Visual indicators for different weather conditions

## 📊 Data Displayed

- **Current Conditions:**
  - Temperature (°C)
  - "Feels like" temperature
  - Weather description
  - Humidity
  - Atmospheric pressure
  - Wind speed and direction
  - Cloud cover percentage
  - Visibility distance
  - Sunrise/Sunset times

- **Forecast (5 Days):**
  - Temperature trends
  - Humidity patterns
  - Wind speed changes
  - Weather condition distribution

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
   ```bash
   cd weather-dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get Free API Key**
   - Visit: https://openweathermap.org/api
   - Sign up for free account
   - Go to API keys page: https://home.openweathermap.org/api_keys
   - Copy your API key

5. **Create `.env` file**
   ```bash
   # In the project root directory, create .env file
   OPENWEATHER_API_KEY=your_api_key_here
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open in browser**
   - Application will open at: http://localhost:8501

## 📁 Project Structure

```
weather-dashboard/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # API keys (DO NOT commit)
├── .gitignore             # Git ignore file
│
├── src/
│   ├── __init__.py
│   ├── weather_api.py     # OpenWeatherMap API integration
│   └── utils.py           # Utility functions and helpers
│
├── data/
│   └── favorites.json     # Saved favorite cities (auto-created)
│
└── README.md              # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Default settings
DEFAULT_CITY = 'Jakarta'          # Default city on startup
DEFAULT_UNITS = 'metric'          # 'metric' for Celsius, 'imperial' for Fahrenheit
TEMPERATURE_UNIT = '°C'           # Display unit
WIND_UNIT = 'm/s'                 # Wind speed unit
MAX_FAVORITE_CITIES = 10          # Maximum favorite cities
CACHE_DURATION = 600              # Cache duration in seconds
```

## 🎨 UI Features

- **Responsive Design** - Works on desktop and mobile
- **Weather Icons** - Visual emoji representations of weather
- **Color-coded Metrics** - Easy to read at a glance
- **Interactive Charts** - Hover for detailed information
- **Smooth Animations** - Better user experience

## 📈 Charts & Visualizations

1. **Temperature Trend** - Line chart showing temperature changes
2. **Humidity Pattern** - Humidity levels over time
3. **Wind Speed** - Wind speed variations
4. **Weather Distribution** - Pie chart of weather conditions

## 🛠️ Technologies Used

- **Streamlit** - Web framework for data apps
- **Requests** - HTTP library for API calls
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualization library
- **Python-dotenv** - Environment variable management

## 🌐 API Information

**Provider:** OpenWeatherMap
**Endpoint:** https://openweathermap.org/api
**Free Tier:** 1,000 API calls/day
**Response Time:** < 1 second
**Coverage:** 195+ countries, 200,000+ cities

## ❓ Troubleshooting

### Error: "Invalid API Key"
- Verify API key in `.env` file
- Ensure API key is activated on OpenWeatherMap
- Wait 5-10 minutes after generating new key
- Restart Streamlit app

### Error: "City not found"
- Check spelling of city name
- Try using country code (e.g., "London, UK")
- Some cities may be listed differently

### Slow Response
- Check internet connection
- OpenWeatherMap servers might be busy
- Try again in a few moments

### Port Already in Use
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

## 📝 File Descriptions

### `app.py`
Main Streamlit application containing:
- Page layout and configuration
- Search functionality
- Weather display and charts
- Favorite cities management

### `config.py`
Configuration file for:
- API settings
- Default values
- File paths
- UI parameters

### `src/weather_api.py`
WeatherAPI class for:
- Fetching current weather
- Getting forecast data
- Parsing API responses
- Error handling

### `src/utils.py`
Utility functions for:
- Managing favorite cities (JSON storage)
- Weather icon mapping
- Unit conversions
- Data formatting

## 🔐 Security

- API key stored in `.env` file (never commit to git)
- `.gitignore` prevents accidental exposure
- No sensitive data in repository
- HTTPS for all API calls

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify API key and internet connection
3. Check OpenWeatherMap API documentation

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- **Streamlit** - For the amazing web framework
- **OpenWeatherMap** - For free weather API
- **Plotly** - For interactive visualizations

---

**Developed with ❤️ for weather enthusiasts**

⭐ If you find this helpful, please give it a star!
