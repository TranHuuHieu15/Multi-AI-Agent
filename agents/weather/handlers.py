import requests
from typing import Dict, Any
from config.setting import settings
from agents.weather.config import MOCK_WEATHER_DATA
from shared.logger import setup_logger

logger = setup_logger("weather_agent")

class WeatherHandler:
    """Handles weather-related requests"""
    
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.api_url = settings.WEATHER_API_URL
        self.use_mock = not self.api_key  # Use mock if no API key
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather for location"""
        location_lower = location.lower().strip()
        
        if self.use_mock:
            logger.info(f"Using mock weather data for: {location}")
            return self._get_mock_weather(location_lower)
        else:
            logger.info(f"Fetching real weather data for: {location}")
            return await self._get_real_weather(location)
    
    def _get_mock_weather(self, location: str) -> Dict[str, Any]:
        """Get mock weather data"""
        weather = MOCK_WEATHER_DATA.get(location)
        
        if not weather:
            # Default weather for unknown locations
            weather = {"temp": 25, "condition": "Partly Cloudy", "humidity": 70}
        
        return {
            "location": location.title(),
            "temperature": f"{weather['temp']}°C",
            "condition": weather["condition"],
            "humidity": f"{weather['humidity']}%",
            "summary": f"{weather['condition']}, {weather['temp']}°C"
        }
    
    async def _get_real_weather(self, location: str) -> Dict[str, Any]:
        """Get real weather from API (OpenWeatherMap example)"""
        try:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.api_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                "location": data["name"],
                "temperature": f"{data['main']['temp']}°C",
                "condition": data["weather"][0]["main"],
                "humidity": f"{data['main']['humidity']}%",
                "summary": f"{data['weather'][0]['main']}, {data['main']['temp']}°C"
            }
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            # Fallback to mock
            return self._get_mock_weather(location.lower())
