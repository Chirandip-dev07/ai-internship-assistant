import json
from pathlib import Path
from typing import List, Dict
from .utils import setup_logger

logger = setup_logger(__name__)

class InternshipTracker:
    """
    Manages internship applications by storing them in a local JSON file.
    Includes comprehensive file safety checks and logging.
    """
    
    def __init__(self, filepath: str = "internships.json") -> None:
        self.filepath = Path(filepath)

    def _load_data(self) -> List[Dict[str, str]]:
        if not self.filepath.exists():
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Tracker file {self.filepath} is corrupted. Returning empty list.")
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading tracker data: {e}")
            return []

    def _save_data(self, data: List[Dict[str, str]]) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save tracker data: {e}")
            raise

    def add_application(self, company: str, role: str, status: str = "applied") -> None:
        try:
            apps = self._load_data()
            apps.append({
                "company": company,
                "role": role,
                "status": status.lower()
            })
            self._save_data(apps)
            logger.info(f"Added new application: {company} - {role}")
        except Exception as e:
            logger.error(f"Failed to add application: {e}")

    def get_all_applications(self) -> List[Dict[str, str]]:
        return self._load_data()

    def update_application_status(self, index: int, new_status: str) -> bool:
        try:
            apps = self._load_data()
            if 0 <= index < len(apps):
                apps[index]['status'] = new_status.lower()
                self._save_data(apps)
                logger.info(f"Updated application at index {index} to '{new_status}'")
                return True
            logger.warning(f"Attempted to update invalid application index: {index}")
            return False
        except Exception as e:
            logger.error(f"Failed to update application status: {e}")
            return False
