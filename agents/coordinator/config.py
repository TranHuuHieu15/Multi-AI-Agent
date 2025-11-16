"""Coordinator configuration"""

from config.setting import settings

COORDINATOR_CONFIG = {
    "name": "Travel Coordinator",
    "description": "Orchestrates multi-agent workflow for travel planning",
    "version": "1.0.0",
    "agents": {
        "weather": {
            "url": settings.WEATHER_AGENT_URL,
            "endpoint": "/a2a"
        },
        "planning": {
            "url": settings.PLANNING_AGENT_URL,
            "endpoint": "/a2a"
        }
    },
    "retry_config": {
        "max_retries": 3,
        "base_delay": 1.0,
        "max_delay": 10.0
    },
    "timeout": 30.0  # seconds
}
