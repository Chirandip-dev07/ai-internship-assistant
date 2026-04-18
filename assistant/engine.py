from enum import Enum
from typing import Optional

from .logic import call_gemini_api, generate_internship_roadmap, generate_cold_email_draft, ConfigurationError, GeminiAPIError
from .prompts import INTENT_DETECTION_PROMPT, SCHEDULING_PROMPT, GENERAL_PROMPT
from .utils import print_header, get_user_input, setup_logger, Colors, print_info, print_success, print_error
from .calendar import create_mock_calendar_event

logger = setup_logger(__name__)

class Intent(Enum):
    PLANNING = "internship_planning"
    EMAIL = "email_generation"
    SCHEDULING = "scheduling"
    GENERAL = "general_query"

def _detect_user_intent(query: str) -> Intent:
    normalized_query = query.lower()
    
    if any(kw in normalized_query for kw in ["internship", "roadmap", "plan", "goals", "path"]):
        return Intent.PLANNING
        
    if any(kw in normalized_query for kw in ["email", "draft", "message", "recruiter", "cold reach"]):
        return Intent.EMAIL
        
    if any(kw in normalized_query for kw in ["schedule", "calendar", "time", "event", "reminder", "task"]):
        return Intent.SCHEDULING

    prompt = INTENT_DETECTION_PROMPT.format(query=query)
    
    try:
        response_text = call_gemini_api(prompt)
    except (ConfigurationError, GeminiAPIError) as e:
        logger.error(f"Intent detection failed during API call: {e}")
        return Intent.GENERAL
        
    intent_str = response_text.strip().lower()
    
    for intent in Intent:
        if intent.value in intent_str:
            return intent
            
    return Intent.GENERAL

def _handle_ai_scheduling(query: str) -> str:
    prompt = SCHEDULING_PROMPT.format(query=query)
    return call_gemini_api(prompt)

def _handle_general_query(query: str) -> str:
    prompt = GENERAL_PROMPT.format(query=query)
    return call_gemini_api(prompt)

def process_user_query(query: str) -> None:
    logger.info("Analyzing request intent...")
    intent = _detect_user_intent(query)
    
    try:
        if intent == Intent.PLANNING:
            print_header("🎯 INTERNSHIP ROADMAP", Colors.HEADER)
            print_info("Generating your personalized roadmap... (Please wait)\n")
            print(generate_internship_roadmap(query))
            
        elif intent == Intent.EMAIL:
            print_header("✉️ COLD EMAIL GENERATOR", Colors.CYAN)
            print_info("I need a bit more context to draft the perfect email.")
            target = get_user_input("Target company and role? (e.g., Google SWE Intern)")
            background = get_user_input("Briefly describe your background (or press enter to use query context)")
            
            full_background = background if background.strip() else f"Context from query: {query}"
            
            print_info("Drafting your professional email... (Please wait)\n")
            print(generate_cold_email_draft(target, full_background))
            
        elif intent == Intent.SCHEDULING:
            print_header("📅 SCHEDULING ASSISTANT", Colors.BLUE)
            print(f"{Colors.BOLD}1.{Colors.ENDC} Generate an AI task schedule based on your query")
            print(f"{Colors.BOLD}2.{Colors.ENDC} Add a specific event to Google Calendar\n")
            
            choice = get_user_input("Select an option")
            if choice == '1':
                print_info("Creating your schedule... (Please wait)\n")
                print(_handle_ai_scheduling(query))
            elif choice == '2':
                task = get_user_input("Enter the task description")
                time = get_user_input("Enter preferred time (e.g., Tomorrow at 3 PM)")
                print_success(create_mock_calendar_event(task, time))
            else:
                print_error("Invalid choice. Returning to main menu.")
            
        else:
            print_header("🤖 AI ASSISTANT", Colors.HEADER)
            print_info("Thinking...\n")
            print(_handle_general_query(query))
            
    except ConfigurationError as e:
        print_error("Could not complete the request due to missing configuration.")
    except GeminiAPIError as e:
        print_error("Could not complete the request due to an AI service error.")
    except Exception as e:
        print_error("An unexpected error occurred. Please try again.")
