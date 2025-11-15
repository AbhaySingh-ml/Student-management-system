import json
import os
from logger_setup import get_logger

# Setup
logger = get_logger(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/students.json")

def load_students():
    """Load student records from the JSON file."""
    try:
        if not os.path.exists(DATA_FILE):
            logger.warning("Data file not found, returning empty list.")
            return []
        with open(DATA_FILE, "r") as file:
            students = json.load(file)
            logger.info("Loaded students successfully.")
            return students
    except Exception as e:
        logger.error(f"Error loading students: {e}")
        return []

def save_students(students):
    """Save student records to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(students, file, indent=4)
            logger.info("Saved students successfully.")
    except Exception as e:
        logger.error(f"Error saving students: {e}")

