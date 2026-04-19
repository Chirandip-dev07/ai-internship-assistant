from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from assistant.logic import (
    generate_internship_roadmap,
    generate_cold_email_draft,
    ConfigurationError,
    GeminiAPIError
)

# Load environment variables from a local .env file if it exists.
# This ensures local development compatibility without hardcoding secrets.
# In Cloud Run, load_dotenv() will gracefully ignore the missing .env file,
# and the app will securely use Cloud Run's native environment variables.
load_dotenv()

app = FastAPI(title="AI Productivity & Internship Assistant API")

class AskRequest(BaseModel):
    query: str
    target_company_role: Optional[str] = "Unknown Company/Role"
    user_background: Optional[str] = None

class AskResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Assistant API is running!"}

@app.post("/ask", response_model=AskResponse)
def ask_assistant(request: AskRequest):
    query_lower = request.query.lower()
    
    try:
        if "internship" in query_lower:
            result = generate_internship_roadmap(request.query)
            return AskResponse(response=result)
            
        elif "email" in query_lower:
            # Provide the query as background if user_background is not specified
            bg = request.user_background if request.user_background else f"Context from query: {request.query}"
            result = generate_cold_email_draft(request.target_company_role, bg)
            return AskResponse(response=result)
            
        else:
            default_message = (
                "Hello! I am your AI Productivity & Internship Assistant. "
                "I can help you build an internship roadmap (mention 'internship') "
                "or draft a cold email (mention 'email'). How can I assist you today?"
            )
            return AskResponse(response=default_message)
            
    except ConfigurationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except GeminiAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
