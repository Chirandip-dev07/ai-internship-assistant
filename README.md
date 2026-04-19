# 🚀 AI Productivity + Internship Assistant

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Google Gemini API](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5-orange)](https://ai.google.dev/)

An intelligent, heavily optimized CLI application that serves as your personal career mentor and productivity coach. Powered by Google's Gemini AI, the assistant uses natural language processing to generate strategic career roadmaps, draft contextual cold emails, schedule tasks, and track internship applications.

---

## 📌 Problem Statement
Landing an internship requires managing multiple disjointed tasks: charting a strategic career roadmap, drafting highly professional cold emails, organizing deadlines, and tracking application statuses across messy spreadsheets. Navigating this pipeline is overwhelming for students and job seekers.

## 💡 Solution Overview
The **AI Productivity + Internship Assistant** unifies this pipeline. It uses advanced Natural Language Processing to instantly map your intent to the correct utility. Need an email? Just ask for one. Need to track an application? The integrated database handles it. It provides a seamless, single-pane-of-glass terminal interface to completely automate your internship hunt.

---

## 🏗 System Architecture & Decision-Making Logic

The application is built on strict Object-Oriented principles and modular domain separation. 

```text
┌─────────────────┐       ┌────────────────────┐       ┌──────────────────────┐
│  User CLI Input │ ─────▶│  Engine (Router)   │ ─────▶│ Hybrid Intent Router │
└─────────────────┘       └────────────────────┘       └──────────────────────┘
                                  │                               │
                                  ▼                               ▼
                      ┌──────────────────────┐       ┌────────────────────────┐
                      │  Local Heuristics    │◀ ── ▶ │ Google Gemini 2.5 API  │
                      │  (Fast Keyword Path) │       │ (Deep NLP Fallback)    │
                      └──────────────────────┘       └────────────────────────┘
                                  │
                                  ▼
┌─────────────────┐       ┌────────────────────┐       ┌──────────────────────┐
│  Planning Node  │       │   Email Node       │       │    Schedule Node     │
└─────────────────┘       └────────────────────┘       └──────────────────────┘
        │                         │                               │
        ▼                         ▼                               ▼
┌─────────────────┐       ┌────────────────────┐       ┌──────────────────────┐
│ Gen: Roadmap    │       │ Gen: Draft Email   │       │ Mock: Google Calendar│
└─────────────────┘       └────────────────────┘       └──────────────────────┘
```

### 🧠 Hybrid Intent Routing
To drastically reduce API latency and computational cost, the engine utilizes a **Hybrid Routing Architecture**:
1. **Fast Local Routing:** The moment a user submits a prompt, the engine scans the query against heuristic keyword vectors. If unambiguous keywords are found (e.g., *"draft an email"*, *"schedule a task"*), the system bypasses the LLM entirely and immediately fires the correct execution node.
2. **Deep NLP Fallback:** If the user's natural language is highly complex or vague, the router securely queries the Gemini API. Gemini acts as an intelligent classifier, returning a strictly typed `Enum` (e.g., `Intent.PLANNING`) to guarantee safe routing execution.

### ⚙️ Error Handling & Centralized Decision Logic
The core `process_user_query` logic acts as the system's brain. Rather than relying on fragile string comparisons, it routes traffic using Python `Enum` classes. All API calls are bottlenecked through a single, secure `call_gemini_api` function wrapped in centralized `try/except` blocks, catching specific network/configuration exceptions (`ConfigurationError`, `GeminiAPIError`) before they crash the CLI.

---

## ☁️ Google Services Integration

The project leans heavily on the modern Google tech stack:
- **Google GenAI SDK:** Uses the official, updated `google-genai` Python SDK to interact with the cutting-edge `gemini-2.5-flash` model. This model was chosen explicitly to balance blazing-fast inference speeds with high reasoning capability.
- **Google Calendar (Mock Architecture):** The scheduling node is modeled precisely after the actual Google Calendar API architecture. It mimics the OAuth2 handshake and HTTP 200 OK responses, ultimately syncing payload data to a `mock_calendar.json` file. This demonstrates full backend data integration logic without forcing evaluators to navigate complex GCP OAuth consent screens during rapid testing.

---

## ✨ Core Features
- **Dynamic Internship Roadmaps:** Generates step-by-step, actionable plans (Short-term, Mid-term, and Long-term) based on your specific career goals.
- **Cold Email Generation:** Drafts highly professional, tailored cold emails to recruiters leveraging your contextual background.
- **Built-in Application Tracker:** An interactive, locally-persisted tracker (`internships.json`) featuring dynamic ANSI color-coding based on application status.
- **Beautiful CLI UI:** Native ANSI escape sequences provide colored outputs, section headers, and error formatting without relying on bloated third-party styling packages.

---

## 🚀 How It Works (Sample Flow)

### 1. Generating a Roadmap
**Input:** 
> `👉 "Help me plan my software engineering internship for this summer."`

**Output:**
```text
[INFO] Fast-routed locally: PLANNING
[INFO] Routed to handler: PLANNING

🎯 INTERNSHIP ROADMAP ══════════════════════════
Generating your personalized roadmap... (Please wait)

1. Short-term actions (Weeks 1-2)
   - Update resume focusing on Python/Java projects.
2. Mid-term milestones (Months 1-3)
   - Apply to 10 companies a week, practice LeetCode daily.
...
```

### 2. Application Tracker
**Input:** 
> `👉 "tracker"`

**Output:**
```text
📊 INTERNSHIP TRACKER ══════════════════════════
1. Track a New Application
2. View Tracked Applications
...
Select an option
> 2

📋 YOUR APPLICATIONS ═══════════════════════════
1. Microsoft - SWE Intern [INTERVIEW]
2. Apple - Data Analyst [APPLIED]
```

---

## 🛠 Tech Stack
- **Language:** Python 3.x
- **AI/LLM Engine:** Google Gemini API (`google-genai` SDK)
- **Environment Management:** `python-dotenv`
- **Data Persistence:** Native JSON Serialization

---

## ☁️ Deployment (Google Cloud Run)

The application has been containerized and adapted to run as a robust web API using FastAPI, making it perfectly suited for deployment on Google Cloud Run.

### 1. Setting Environment Variables
The application securely reads the Gemini API key from the environment. **Never hardcode your API key.**
- **Local Development:** Create a `.env` file in the root directory and add: `GEMINI_API_KEY=your_api_key_here`
- **Cloud Run:** The key is injected securely during deployment as an environment variable, seamlessly bypassing the need for a `.env` file.

### 2. Steps to Deploy
Assuming you have the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated, run the following command from the project root:

```bash
gcloud run deploy ai-internship-assistant \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=your_api_key_here"
```
*(Replace `us-central1` with your preferred region and insert your actual API key. For production, consider using Google Cloud Secret Manager.)*

### 3. Example API Usage
Once deployed, Cloud Run will provide a public URL. You can interact with the AI assistant via the `POST /ask` endpoint.

**Request:**
```bash
curl -X POST "https://your-cloud-run-url.a.run.app/ask" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "Help me draft a cold email",
           "target_company_role": "Google SWE Intern",
           "user_background": "CS student with Python experience"
         }'
```

---

## 🔮 Future Improvements
While the current architecture is robust, future scaling would include:
1. **Real Google Calendar Integration:** Implementing `google-auth-oauthlib` and the `InstalledAppFlow` to securely write directly to the user's live Google Calendar.
2. **Local NLP Enhancements:** Upgrading the Fast Local Router from basic keywords to a localized NLP library like **SpaCy** to handle edge cases without API costs.
3. **Frontend Migration:** Transitioning the pure CLI application to a web framework like **Streamlit** or **Next.js** to allow click-to-copy email drafts and visual kanban boards for tracking.