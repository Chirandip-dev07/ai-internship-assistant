import os
from google import genai
from .prompts import ROADMAP_PROMPT, COLD_EMAIL_PROMPT

class ConfigurationError(Exception):
    """Raised when environment variables or configurations are missing."""
    pass

class GeminiAPIError(Exception):
    """Raised when the Gemini API call fails or returns an invalid response."""
    pass

def call_gemini_api(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    """
    Sends a formatted prompt to the Gemini API and returns the text response.
    Raises specific exceptions on failure instead of returning strings.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ConfigurationError("GEMINI_API_KEY environment variable is missing. Please add it to your .env file.")
        
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise GeminiAPIError(f"Failed to connect to Gemini API: {str(e)}")

def generate_internship_roadmap(user_goal: str) -> str:
    """Generates an actionable roadmap based on the user's goal."""
    prompt = ROADMAP_PROMPT.format(goal=user_goal)
    return call_gemini_api(prompt)

def generate_cold_email_draft(target_company_role: str, user_background: str) -> str:
    """Generates a professional cold email draft using the user's context."""
    prompt = COLD_EMAIL_PROMPT.format(target=target_company_role, background=user_background)
    return call_gemini_api(prompt)
