import asyncio
import sys
from agents.coordinator.orchestrator import TravelOrchestrator
from shared.logger import setup_logger
from config.setting import settings

logger = setup_logger("coordinator")

async def main():
    """Main coordinator function"""
    
    logger.info("=" * 60)
    logger.info("🎯 TRAVEL COORDINATOR STARTING")
    logger.info("=" * 60)
    
    # Create orchestrator
    orchestrator = TravelOrchestrator()
    
    # Default locations to test
    test_locations = ["Da Nang", "Hanoi", "Ho Chi Minh"]
    
    # Check if locations provided via command line
    if len(sys.argv) > 1:
        test_locations = sys.argv[1:]
    
    logger.info(f"\n📋 Planning trips for: {', '.join(test_locations)}")
    
    # Process each location
    for location in test_locations:
        try:
            result = await orchestrator.plan_trip(location)
            print(orchestrator.format_result(result))
            
            if location != test_locations[-1]:
                logger.info("\n" + "─" * 60 + "\n")
                await asyncio.sleep(2)  # Brief pause between requests
                
        except Exception as e:
            logger.error(f"❌ Failed to process {location}: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ ALL TRIPS PLANNED")
    logger.info("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Coordinator stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
