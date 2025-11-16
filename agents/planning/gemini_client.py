import google.generativeai as genai
from typing import Dict, Any, Optional
from config.setting import settings
from shared.logger import setup_logger

logger = setup_logger("gemini_client")

class GeminiClient:
    """Client for Google Gemini API"""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Create model
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Generation config
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        logger.info(f"✅ Gemini client initialized with model: {settings.GEMINI_MODEL}")
    
    async def generate_activities(
        self,
        location: str,
        weather_info: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate activity suggestions based on weather"""
        
        # Create prompt
        prompt = self._create_prompt(location, weather_info, additional_context)
        
        try:
            logger.info(f"🤖 Generating activities for {location}...")
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Parse response
            activities = self._parse_response(response.text)
            
            logger.info(f"✅ Generated {len(activities['activities'])} activities")
            
            return activities
            
        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            return self._fallback_activities(location, weather_info)
    
    def _create_prompt(
        self,
        location: str,
        weather_info: str,
        additional_context: Optional[str]
    ) -> str:
        """Create prompt for Gemini"""
        
        prompt = f"""You are a travel planning assistant. Based on the weather conditions, suggest activities for travelers.

Location: {location}
Weather: {weather_info}
"""
        
        if additional_context:
            prompt += f"\nAdditional Context: {additional_context}\n"
        
        prompt += """
Please suggest 3-5 activities that are suitable for this weather. For each activity:
- Include an emoji
- Brief description (1-2 sentences)
- Why it's good for this weather

Format your response as:
🎯 Activity Name
Description here. Why it's suitable.

Example:
🏖️ Beach Day
Enjoy the sunny weather at the beautiful beaches. Perfect for swimming and sunbathing with warm temperatures.
"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured format"""
        
        activities = []
        lines = response_text.strip().split('\n')
        
        current_activity = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's an activity title (has emoji)
            if any(char for char in line if ord(char) > 127):  # Has emoji
                if current_activity:
                    activities.append(current_activity)
                current_activity = {
                    "title": line,
                    "description": ""
                }
            elif current_activity:
                current_activity["description"] += line + " "
        
        # Add last activity
        if current_activity:
            activities.append(current_activity)
        
        # If parsing failed, return raw text
        if not activities:
            activities = [{
                "title": "📋 Suggested Activities",
                "description": response_text
            }]
        
        return {
            "activities": activities,
            "count": len(activities),
            "raw_response": response_text
        }
    
    def _fallback_activities(
        self,
        location: str,
        weather_info: str
    ) -> Dict[str, Any]:
        """Fallback activities if Gemini fails"""
        
        # Simple rule-based fallback
        if "sunny" in weather_info.lower():
            activities = [
                {
                    "title": "🏖️ Beach Activities",
                    "description": "Perfect weather for beach time! Swimming, sunbathing, and water sports."
                },
                {
                    "title": "🚴 Outdoor Cycling",
                    "description": "Explore the city on two wheels in beautiful weather."
                },
            ]
        elif "rain" in weather_info.lower():
            activities = [
                {
                    "title": "🏛️ Museum Visit",
                    "description": "Stay dry while exploring local culture and history."
                },
                {
                    "title": "☕ Cozy Cafes",
                    "description": "Enjoy local coffee and cuisine in warm indoor spaces."
                },
            ]
        else:
            activities = [
                {
                    "title": "🚶 City Walking Tour",
                    "description": "Comfortable weather for exploring the city on foot."
                },
                {
                    "title": "🍜 Food Tour",
                    "description": "Sample local delicacies and street food."
                },
            ]
        
        return {
            "activities": activities,
            "count": len(activities),
            "raw_response": "Fallback activities generated"
        }
