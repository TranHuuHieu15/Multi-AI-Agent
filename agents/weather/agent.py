import asyncio
from python_a2a import AgentCard, A2AServer, run_server
from agents.weather.config import AGENT_CARD
from agents.weather.handlers import WeatherHandler
from shared.logger import setup_logger
from config.setting import settings

logger = setup_logger("weather_agent")

# Create handler
handler = WeatherHandler()

class WeatherAgent(A2AServer):
    """Weather Agent Server"""
    
    def handle_message(self, message):
        """Handle incoming weather requests"""
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run async handler
            return loop.run_until_complete(self._async_handle_message(message))
        except Exception as e:
            logger.error(f"❌ Error in handle_message: {e}")
            return {
                "text": f"Sorry, I couldn't process your request",
                "role": "agent",
                "error": str(e)
            }
    
    async def _async_handle_message(self, message):
        """Async implementation of message handler"""
        try:
            location = message.content.text
            logger.info(f"📍 Received weather request for: {location}")
            
            # Get weather data
            weather_data = await handler.get_weather(location)
            
            # Format response
            response_text = (
                f"Weather in {weather_data['location']}:\n"
                f"🌡️ Temperature: {weather_data['temperature']}\n"
                f"☁️ Condition: {weather_data['condition']}\n"
                f"💧 Humidity: {weather_data['humidity']}"
            )
            
            logger.info(f"✅ Returning weather data: {weather_data['summary']}")
            
            return {
                "text": response_text,
                "role": "agent",
                "metadata": weather_data
            }
            
        except Exception as e:
            logger.error(f"❌ Error handling request: {e}")
            return {
                "text": f"Sorry, I couldn't fetch weather data",
                "role": "agent",
                "error": str(e)
            }

# Create agent card
agent_card = AgentCard(**AGENT_CARD)

# Create A2A server
weather_agent = WeatherAgent(agent_card=agent_card)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🌤️  WEATHER AGENT STARTING")
    logger.info(f"📡 URL: {settings.WEATHER_AGENT_URL}")
    logger.info(f"🔌 Port: {settings.WEATHER_AGENT_PORT}")
    logger.info("=" * 60)
    
    try:
        run_server(
            weather_agent,
            host="0.0.0.0",
            port=settings.WEATHER_AGENT_PORT
        )
    except KeyboardInterrupt:
        logger.info("🛑 Weather Agent stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
