import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from config import APP_TITLE, DEFAULT_CITY, TEMPERATURE_UNIT, WIND_UNIT
from src.weather_api import WeatherAPI
from src.utils import FavoritesManager, WeatherUtils

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .weather-icon {
        font-size: 48px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weather_api' not in st.session_state:
    st.session_state.weather_api = WeatherAPI()

if 'current_weather' not in st.session_state:
    st.session_state.current_weather = None

if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None

# Sidebar
with st.sidebar:
    st.title("🔍 Search Weather")
    
    # Search option
    search_type = st.radio("Select search type:", ["By City", "Favorites"])
    
    if search_type == "By City":
        city_input = st.text_input(
            "Enter city name:",
            placeholder="e.g., Jakarta, London, New York"
        )
        
        if st.button("🔎 Search", use_container_width=True):
            if city_input:
                with st.spinner(f"Fetching weather for {city_input}..."):
                    weather_data = st.session_state.weather_api.get_current_weather(city_input)
                    if weather_data:
                        st.session_state.current_weather = WeatherAPI.parse_current_weather(weather_data)
                        forecast_data = st.session_state.weather_api.get_forecast(city_input)
                        if forecast_data:
                            st.session_state.forecast_data = WeatherAPI.parse_forecast(forecast_data)
                        st.success(f"✅ Weather data loaded for {city_input}!")
                    else:
                        st.error("❌ City not found. Please try again.")
    
    else:  # Favorites
        favorites = FavoritesManager.load_favorites()
        if favorites:
            selected_city = st.selectbox("Choose a favorite city:", favorites)
            if st.button("📍 Load Weather", use_container_width=True):
                with st.spinner(f"Fetching weather for {selected_city}..."):
                    weather_data = st.session_state.weather_api.get_current_weather(selected_city)
                    if weather_data:
                        st.session_state.current_weather = WeatherAPI.parse_current_weather(weather_data)
                        forecast_data = st.session_state.weather_api.get_forecast(selected_city)
                        if forecast_data:
                            st.session_state.forecast_data = WeatherAPI.parse_forecast(forecast_data)
                        st.success(f"✅ Weather data loaded for {selected_city}!")
        else:
            st.info("📌 No favorite cities yet. Add one from the main page!")
    
    st.divider()
    
    # Favorites management
    st.subheader("❤️ Manage Favorites")
    favorites = FavoritesManager.load_favorites()
    
    if st.session_state.current_weather:
        city_name = st.session_state.current_weather['city']
        if city_name not in favorites:
            if st.button(f"➕ Add {city_name} to Favorites", use_container_width=True):
                if FavoritesManager.add_favorite(city_name):
                    st.success(f"✅ {city_name} added to favorites!")
                    st.rerun()
                else:
                    st.warning("⚠️ Maximum favorites reached or already exists!")
        else:
            if st.button(f"❌ Remove {city_name} from Favorites", use_container_width=True):
                if FavoritesManager.remove_favorite(city_name):
                    st.success(f"✅ {city_name} removed from favorites!")
                    st.rerun()

# Main content
st.title(APP_TITLE)

if st.session_state.current_weather:
    weather = st.session_state.current_weather
    
    # Header with city name and current conditions
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"<div class='weather-icon'>{WeatherUtils.get_weather_icon(weather['description'])}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"## {weather['city']}, {weather['country']}")
        st.markdown(f"### {weather['temperature']}{TEMPERATURE_UNIT} - {weather['description'].title()}")
        st.markdown(f"*Feels like {weather['feels_like']}{TEMPERATURE_UNIT}*")
    
    with col3:
        st.metric(label="Humidity", value=f"{weather['humidity']}%")
    
    st.divider()
    
    # Current weather details
    st.subheader("📊 Current Weather Details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌡️ Temperature",
            value=f"{weather['temperature']}{TEMPERATURE_UNIT}",
            delta=f"Min: {weather['temp_min']}{TEMPERATURE_UNIT}, Max: {weather['temp_max']}{TEMPERATURE_UNIT}"
        )
    
    with col2:
        st.metric(
            label="💨 Wind Speed",
            value=f"{weather['wind_speed']}{WIND_UNIT}",
            delta=f"Direction: {WeatherUtils.get_wind_direction(weather['wind_deg'])}"
        )
    
    with col3:
        st.metric(
            label="🌡️ Pressure",
            value=f"{weather['pressure']} hPa"
        )
    
    with col4:
        st.metric(
            label="👁️ Visibility",
            value=f"{weather['visibility'] / 1000:.1f} km"
        )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="☁️ Cloud Cover",
            value=f"{weather['clouds']}%"
        )
    
    with col2:
        st.metric(
            label="🌅 Sunrise",
            value=WeatherUtils.format_time(weather['sunrise'])
        )
    
    with col3:
        st.metric(
            label="🌇 Sunset",
            value=WeatherUtils.format_time(weather['sunset'])
        )
    
    with col4:
        st.metric(
            label="💨 Air Quality",
            value=WeatherUtils.get_air_quality(weather['humidity'], weather['pressure'])
        )
    
    st.divider()
    
    # Forecast section
    if st.session_state.forecast_data is not None:
        st.subheader("📅 5-Day Forecast")
        
        forecast_df = st.session_state.forecast_data.copy()
        forecast_df['date'] = forecast_df['datetime'].dt.strftime('%m-%d %H:%M')
        
        # Display forecast as cards
        cols = st.columns(5)
        for idx, (_, row) in enumerate(forecast_df.head(5).iterrows()):
            with cols[idx]:
                st.markdown(f"""
                <div class='metric-card'>
                    <center>
                    <p><b>{row['date']}</b></p>
                    <p>{WeatherUtils.get_weather_icon(row['description'])}</p>
                    <p><b>{row['temperature']}{TEMPERATURE_UNIT}</b></p>
                    <p><small>{row['description']}</small></p>
                    <p>💨 {row['wind_speed']}{WIND_UNIT}</p>
                    <p>💧 {row['humidity']}%</p>
                    </center>
                </div>
                """, unsafe_allow_html=True)
        
        # Temperature trend chart
        st.subheader("📈 Temperature Trend")
        fig = px.line(
            forecast_df.head(20),
            x='datetime',
            y='temperature',
            markers=True,
            title="Temperature Forecast (Next 5 Days)",
            labels={'datetime': 'Date Time', 'temperature': f'Temperature ({TEMPERATURE_UNIT})'}
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Weather conditions chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Humidity trend
            fig = px.line(
                forecast_df.head(20),
                x='datetime',
                y='humidity',
                markers=True,
                title="Humidity Forecast",
                labels={'datetime': 'Date Time', 'humidity': 'Humidity (%)'}
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Wind speed trend
            fig = px.line(
                forecast_df.head(20),
                x='datetime',
                y='wind_speed',
                markers=True,
                title="Wind Speed Forecast",
                labels={'datetime': 'Date Time', 'wind_speed': f'Wind Speed ({WIND_UNIT})'}
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        # Weather distribution pie chart
        weather_counts = forecast_df['weather'].value_counts()
        fig = px.pie(
            values=weather_counts.values,
            names=weather_counts.index,
            title="Weather Conditions Distribution (Next 5 Days)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Additional information
    st.subheader("ℹ️ Additional Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Weather Information:**
        - 🌡️ Temperature: Current air temperature
        - 💨 Wind Speed: Speed of wind movement
        - 💧 Humidity: Amount of moisture in air
        - 🌡️ Pressure: Atmospheric pressure level
        - 👁️ Visibility: How far you can see
        - ☁️ Cloud Cover: Percentage of sky covered by clouds
        """)
    
    with col2:
        st.write("""
        **Tips:**
        - Add favorite cities for quick access
        - Check forecast before planning outdoor activities
        - High humidity and low pressure may indicate rain
        - Wind direction affects weather patterns
        - Sunrise/Sunset times vary by season
        """)

else:
    st.info("🔍 Search for a city to view weather information!")
    st.write("""
    ### Welcome to Weather Dashboard 🌤️
    
    Get real-time weather information for any city in the world!
    
    **Features:**
    - 🔎 Search weather by city name
    - ❤️ Save favorite cities
    - 📊 View detailed weather metrics
    - 📅 5-day weather forecast
    - 📈 Interactive charts and visualizations
    
    **How to use:**
    1. Enter a city name in the search box
    2. Click "Search" to get current weather
    3. View detailed information and forecast
    4. Add cities to favorites for quick access
    
    **Data Source:** OpenWeatherMap API
    """)
