# Technology Stack

**Analysis Date:** 2025-03-02

## Languages

**Primary:**
- Python 3.10 - Used across the entire backend, including LLM routing, email processing, and webhook handling.

**Secondary:**
- Not applicable

## Runtime

**Environment:**
- Python 3.10

**Package Manager:**
- pip - Dependencies are defined in `requirements.txt`.
- Lockfile: missing

## Frameworks

**Core:**
- Flask 3.1.3 - Web server framework used for handling incoming WhatsApp webhooks from Twilio (`src/webhook_server.py`).

**Testing:**
- pytest 8.0.0 - Test runner for unit, integration, and E2E tests (`pytest.ini`).

**Build/Dev:**
- None detected

## Key Dependencies

**Critical:**
- imap-tools (1.7.0) - Crucial for fetching, filtering, and interacting with the IMAP email server securely and reliably (`src/email_service.py`).
- twilio - Used for sending and receiving WhatsApp messages to communicate with reviewers/admins (`src/whatsapp_sender.py`).
- python-dotenv (1.0.0) - Manages environment variable configuration across the application.

**Infrastructure:**
- google-generativeai (0.3.2) - Native SDK for interacting with Google's Gemini LLM models (`src/llm_router.py`).
- openai (>=1.55.0) - Client used to interact with OpenAI and OpenAI-compatible LLM APIs (e.g., Groq, DeepSeek, OpenRouter) (`src/llm_router.py`).
- gspread (5.12.0) - Google Sheets API client, utilized to use Google Sheets as a CRM for logging email interactions (`src/crm_service.py`).
- requests (2.31.0) - Standard HTTP client library used for external network requests.

## Configuration

**Environment:**
- Configured via environment variables loaded from a `.env` file using `python-dotenv`.
- Key configs required: `IMAP_SERVER`, `IMAP_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, `SMTP_SERVER`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_SENDER_NUMBER`, and at least one LLM provider key (e.g., `GEMINI_API_KEY`).

**Build:**
- Testing configuration resides in `pytest.ini`.

## Platform Requirements

**Development:**
- Python 3.10 with standard virtual environment (`venv`).

**Production:**
- Standard server capable of running a Python background process and exposing an HTTP port (default 5000) for Flask webhook endpoints.

---

*Stack analysis: 2025-03-02*
