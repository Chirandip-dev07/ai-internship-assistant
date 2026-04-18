import json
from pathlib import Path
from .utils import setup_logger

logger = setup_logger(__name__)
MOCK_CALENDAR_FILE = Path("mock_calendar.json")

def create_mock_calendar_event(task_description: str, scheduled_time: str) -> str:
    """
    Mocks a Google Calendar API integration by saving events to a local JSON file.
    Includes proper logging for success and file corruption errors.
    """
    logger.info("Authenticating via OAuth2...")
    logger.info(f"Scheduling: '{task_description}' at '{scheduled_time}'...")
    
    events = []
    if MOCK_CALENDAR_FILE.exists():
        try:
            with open(MOCK_CALENDAR_FILE, "r", encoding="utf-8") as f:
                events = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Mock calendar file is corrupted. Starting fresh.")
        except Exception as e:
            logger.error(f"Failed to read mock calendar file: {e}")
            raise
            
    events.append({
        "task": task_description,
        "time": scheduled_time,
        "status": "confirmed (mocked)"
    })
    
    try:
        with open(MOCK_CALENDAR_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to write to mock calendar file: {e}")
        raise
        
    logger.info("Sync successful. HTTP 200 OK.")
    return f"Success! '{task_description}' has been scheduled for {scheduled_time}."
