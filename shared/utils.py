import asyncio
from typing import Any, Dict
from datetime import datetime

def format_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_location(text: str) -> str:
    """Extract location from text"""
    # Simple parser - can be enhanced
    text = text.strip()
    if "in " in text.lower():
        return text.lower().split("in ")[-1].strip()
    return text

async def retry_async(func, max_retries: int = 3, delay: float = 1.0):
    """Retry async function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay * (2 ** attempt)
            await asyncio.sleep(wait_time)

def create_error_response(error: str) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "error": True,
        "message": error,
        "timestamp": format_timestamp()
    }
