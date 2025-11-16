from python_a2a import A2AClient, Message, TextContent, MessageRole
from typing import Dict, Any, List
from shared.logger import setup_logger
from shared.utils import retry_async
from config.setting import settings

logger = setup_logger("coordinator")

class TravelOrchestrator:
    """Orchestrates travel planning workflow"""
    
    def __init__(self):
        # Initialize A2A clients for agents
        self.weather_client = A2AClient(f"{settings.WEATHER_AGENT_URL}/a2a")
        self.planning_client = A2AClient(f"{settings.PLANNING_AGENT_URL}/a2a")
        
        logger.info("✅ Orchestrator initialized")
        logger.info(f"   Weather Agent: {settings.WEATHER_AGENT_URL}")
        logger.info(f"   Planning Agent: {settings.PLANNING_AGENT_URL}")
    
    async def plan_trip(self, location: str) -> Dict[str, Any]:
        """
        Main orchestration workflow:
        1. Get weather from Weather Agent
        2. Get activity suggestions from Planning Agent
        3. Combine results
        """
        
        logger.info("=" * 60)
        logger.info(f"🚀 Starting trip planning for: {location}")
        logger.info("=" * 60)
        
        result = {
            "location": location,
            "weather": None,
            "activities": None,
            "success": False,
            "errors": []
        }
        
        try:
            # Step 1: Get Weather
            logger.info(f"\n📍 STEP 1: Querying Weather Agent...")
            weather_info = await self._get_weather(location)
            result["weather"] = weather_info
            logger.info(f"   ✅ Weather: {weather_info}")
            
            # Step 2: Get Activity Suggestions
            logger.info(f"\n📍 STEP 2: Querying Planning Agent...")
            activities = await self._get_activities(location, weather_info)
            result["activities"] = activities
            logger.info(f"   ✅ Activities: {len(activities.split('🎯')) - 1} suggestions")
            
            result["success"] = True
            logger.info(f"\n✅ Trip planning completed successfully!")
            
        except Exception as e:
            error_msg = f"Error in orchestration: {e}"
            logger.error(f"❌ {error_msg}")
            result["errors"].append(error_msg)
        
        return result
    
    async def _get_weather(self, location: str) -> str:
        """Get weather from Weather Agent with retry"""
        
        async def fetch():
            message = Message(
                content=TextContent(text=location),
                role=MessageRole.USER
            )
            response = await self.weather_client.send_message_async(message)
            return response.content.text
        
        try:
            return await retry_async(fetch, max_retries=3)
        except Exception as e:
            logger.error(f"Failed to get weather after retries: {e}")
            raise
    
    async def _get_activities(self, location: str, weather_info: str) -> str:
        """Get activities from Planning Agent with retry"""
        
        async def fetch():
            # Format message for planning agent
            planning_query = f"Plan for {location} with weather: {weather_info}"
            
            message = Message(
                content=TextContent(text=planning_query),
                role=MessageRole.USER
            )
            response = await self.planning_client.send_message_async(message)
            return response.content.text
        
        try:
            return await retry_async(fetch, max_retries=3)
        except Exception as e:
            logger.error(f"Failed to get activities after retries: {e}")
            raise
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """Format result for display"""
        
        if not result["success"]:
            return f"❌ Failed to plan trip: {', '.join(result['errors'])}"
        
        output = f"""
{'=' * 60}
🌏 COMPLETE TRIP PLAN
{'=' * 60}

📍 Location: {result['location']}

{result['weather']}

{result['activities']}

{'=' * 60}
        """
        return output.strip()
