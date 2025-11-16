import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    LOG_DIR = BASE_DIR / "logs"
    
    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Weather API
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    WEATHER_API_URL = os.getenv("WEATHER_API_URL", "")
    
    # Agent ports
    WEATHER_AGENT_PORT = int(os.getenv("WEATHER_AGENT_PORT", "5001"))
    PLANNING_AGENT_PORT = int(os.getenv("PLANNING_AGENT_PORT", "5002"))
    COORDINATOR_PORT = int(os.getenv("COORDINATOR_PORT", "5003"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent URLs
    WEATHER_AGENT_URL = f"http://localhost:{WEATHER_AGENT_PORT}"
    PLANNING_AGENT_URL = f"http://localhost:{PLANNING_AGENT_PORT}"
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required in .env file")
        
        # Create log directory
        cls.LOG_DIR.mkdir(exist_ok=True)

settings = Settings()
