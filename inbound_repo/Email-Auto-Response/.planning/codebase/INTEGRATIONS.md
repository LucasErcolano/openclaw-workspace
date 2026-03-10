# External Integrations

**Analysis Date:** 2025-03-02

## APIs & External Services

**Messaging / Notifications:**
- Twilio - Used for sending WhatsApp notifications for draft review and receiving instructions back from reviewers.
  - SDK/Client: `twilio`
  - Auth: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`

**Large Language Models (LLMs):**
- Google Gemini API - Primary LLM provider for email analysis and draft generation.
  - SDK/Client: `google-generativeai`
  - Auth: `GEMINI_API_KEY` (or `GEMINI` fallback list)
- OpenAI API (and Compatible APIs) - Fallback and secondary LLM providers (including Groq, OpenRouter, Sambanova, Cerebras, DeepSeek).
  - SDK/Client: `openai`
  - Auth: `OPENAI_API_KEY`, `GROQ_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, etc.

**Email Systems:**
- IMAP/SMTP Servers - Connects to arbitrary email providers to read incoming messages and send the approved auto-responses.
  - SDK/Client: `imap-tools` and built-in `smtplib`
  - Auth: `EMAIL_USER`, `EMAIL_PASSWORD`, `IMAP_SERVER`, `SMTP_SERVER`

## Data Storage

**Databases:**
- Google Sheets (as CRM)
  - Connection: `GOOGLE_APPLICATION_CREDENTIALS` (usually pointing to `credentials.json`)
  - Client: `gspread`

**File Storage:**
- Local filesystem only (used for runtime state persistence in `.runtime/` directory).

**Caching:**
- None external (in-memory caching and local JSON files like `.runtime/llm_router_state.json` are used for circuit breakers and rate limits).

## Authentication & Identity

**Auth Provider:**
- Custom / API Keys
  - Implementation: Services authenticate via statically provisioned API keys stored in `.env`, and Google Sheets uses a Service Account JSON file.

## Monitoring & Observability

**Error Tracking:**
- None detected

**Logs:**
- Built-in Python `logging` module used across all files (e.g., `logger.info`, `logger.error`), outputting to standard output/console.

## CI/CD & Deployment

**Hosting:**
- Custom Server/VPS (indicated by manual execution scripts like `run_e2e_bg.sh` and a long-running polling/flask process).

**CI Pipeline:**
- None explicitly detected, though testing setup exists (`pytest`).

## Environment Configuration

**Required env vars:**
- `IMAP_SERVER`, `IMAP_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`
- `SMTP_SERVER`, `SMTP_PORT`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_SENDER_NUMBER`
- At least one LLM key: `GEMINI_API_KEY` (or alternative provider key)

**Secrets location:**
- `.env` file for API keys and basic credentials.
- `credentials.json` (or path in `GOOGLE_APPLICATION_CREDENTIALS`) for Google Service Account access.

## Webhooks & Callbacks

**Incoming:**
- `/whatsapp`, `/h5k5`, `/alfa` endpoints on the Flask server (`src/webhook_server.py`) - Used to receive incoming messages from Twilio when a reviewer approves or modifies a draft.

**Outgoing:**
- None

---

*Integration audit: 2025-03-02*
