from config.setting import settings

AGENT_CARD = {
    "name": "Weather Agent",
    "description": "Provides real-time weather information for travel planning",
    "url": settings.WEATHER_AGENT_URL,
    "version": "1.0.0",
    "capabilities": {
        "weather_forecasting": True,
        "location_lookup": True,
        "google_a2a_compatible": True
    }
}

# Mock weather data (replace with real API calls)
MOCK_WEATHER_DATA = {
    "da nang": {"temp": 28, "condition": "Sunny", "humidity": 75},
    "hanoi": {"temp": 22, "condition": "Cloudy", "humidity": 80},
    "ho chi minh": {"temp": 30, "condition": "Rainy", "humidity": 85},
    "hue": {"temp": 26, "condition": "Partly Cloudy", "humidity": 78},
    "nha trang": {"temp": 29, "condition": "Sunny", "humidity": 70},
}
