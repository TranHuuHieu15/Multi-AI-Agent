from typing import Dict, Any, Optional
from .gemini_client import GeminiClient
from shared.logger import setup_logger

logger = setup_logger("planning_handler")

class PlanningHandler:
    """Handles planning-related requests"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        logger.info("✅ Planning handler initialized")
    
    async def handle_request(self, text: str) -> Dict[str, Any]:
        """
        Main handler for planning requests
        
        Args:
            text: Request text (format: "Plan for {location} with weather: {weather}")
        
        Returns:
            Dict with activities and metadata
        """
        try:
            # Parse the request
            location, weather_info = self._parse_request(text)
            
            logger.info(f"📋 Planning for: {location}")
            logger.info(f"☁️ Weather: {weather_info}")
            
            # Generate activities using Gemini
            result = await self.gemini_client.generate_activities(
                location=location,
                weather_info=weather_info
            )
            
            # Format response
            formatted_response = self._format_response(location, result)
            
            return {
                "success": True,
                "location": location,
                "weather": weather_info,
                "response": formatted_response,
                "activities": result["activities"],
                "count": result["count"]
            }
            
        except Exception as e:
            logger.error(f"❌ Error in planning handler: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f"Sorry, I couldn't generate activity suggestions. Error: {str(e)}"
            }
    
    def _parse_request(self, text: str) -> tuple[str, str]:
        """Parse location and weather from request text"""
        
        # Expected format: "Plan for {location} with weather: {weather_info}"
        if "with weather:" in text:
            parts = text.split("with weather:")
            location = parts[0].replace("Plan for", "").strip()
            weather_info = parts[1].strip()
        else:
            # Fallback: use entire text as location
            location = text.strip()
            weather_info = "Unknown weather conditions"
        
        return location, weather_info
    
    def _format_response(self, location: str, result: Dict[str, Any]) -> str:
        """Format the response text"""
        
        response = f"🎯 Activity Suggestions for {location}:\n\n"
        
        for i, activity in enumerate(result["activities"], 1):
            response += f"{activity['title']}\n"
            response += f"{activity['description'].strip()}\n"
            if i < len(result["activities"]):
                response += "\n"
        
        return response.strip()
    
    async def get_activity_details(self, activity_name: str, location: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific activity
        (Extension method for future use)
        """
        try:
            prompt = f"Provide detailed information about {activity_name} in {location}"
            # Implementation here
            return {"details": "Activity details..."}
        except Exception as e:
            logger.error(f"Error getting activity details: {e}")
            return {"error": str(e)}
