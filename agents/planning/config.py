from config.setting import settings

AGENT_CARD = {
    "name": "Planning Agent",
    "description": "AI-powered travel activity planner using Google Gemini",
    "url": settings.PLANNING_AGENT_URL,
    "version": "1.0.0",
    "capabilities": {
        "activity_planning": True,
        "ai_suggestions": True,
        "google_gemini": True,
        "google_a2a_compatible": True
    }
}
