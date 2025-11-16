import asyncio
from python_a2a import AgentCard, A2AServer, run_server
from agents.planning.config import AGENT_CARD
from agents.planning.gemini_client import GeminiClient
from shared.logger import setup_logger
from config.setting import settings

logger = setup_logger("planning_agent")

# Validate Gemini API key
settings.validate()

# Create Gemini client
gemini_client = GeminiClient()

class PlanningAgent(A2AServer):
    """Planning Agent Server with Gemini AI"""
    
    def handle_message(self, message):
        """Handle incoming planning requests"""
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
            text = message.content.text
            logger.info(f"📋 Received planning request: {text[:100]}...")
            
            # Parse location and weather from message
            # Expected format: "Plan for {location} with weather: {weather_info}"
            parts = text.split("with weather:")
            if len(parts) == 2:
                location = parts[0].replace("Plan for", "").strip()
                weather_info = parts[1].strip()
            else:
                location = "Unknown"
                weather_info = text
            
            logger.info(f"📍 Location: {location}")
            logger.info(f"☁️ Weather: {weather_info}")
            
            # Generate activities using Gemini
            result = await gemini_client.generate_activities(
                location=location,
                weather_info=weather_info
            )
            
            # Format response
            response_text = f"🎯 Activity Suggestions for {location}:\n\n"
            for activity in result["activities"]:
                response_text += f"{activity['title']}\n"
                response_text += f"{activity['description'].strip()}\n\n"
            
            logger.info(f"✅ Generated {result['count']} activities")
            
            return {
                "text": response_text.strip(),
                "role": "agent",
                "metadata": result
            }
            
        except Exception as e:
            logger.error(f"❌ Error handling request: {e}")
            return {
                "text": f"Sorry, I couldn't generate activity suggestions. Error: {str(e)}",
                "role": "agent",
                "error": str(e)
            }

# Create agent card
agent_card = AgentCard(**AGENT_CARD)

# Create A2A server
planning_agent = PlanningAgent(agent_card=agent_card)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🗺️  PLANNING AGENT STARTING (with Gemini)")
    logger.info(f"📡 URL: {settings.PLANNING_AGENT_URL}")
    logger.info(f"🔌 Port: {settings.PLANNING_AGENT_PORT}")
    logger.info(f"🤖 Model: {settings.GEMINI_MODEL}")
    logger.info("=" * 60)
    
    try:
        run_server(
            planning_agent,
            host="0.0.0.0",
            port=settings.PLANNING_AGENT_PORT
        )
    except KeyboardInterrupt:
        logger.info("🛑 Planning Agent stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
