# Architecture

**Analysis Date:** 2024-03-10

## Pattern Overview

**Overall:** Event-Driven Human-in-the-Loop Agent

**Key Characteristics:**
- **Concurrent Polling:** Actively polls IMAP accounts for incoming emails using a ThreadPool.
- **Event-Driven Feedback:** The core email processing thread pauses and waits on a queue for asynchronous human feedback via a webhook server.
- **Circuit Breaker & Fallbacks:** LLM router implements robust retry, rate limit handling, and multi-provider fallback logic.
- **State Tracking:** Tracks the pending status of emails for durability and user transparency.

## Layers

**Entry Point / Orchestration:**
- Purpose: Polls IMAP, spins up webhooks, manages threads, and executes the core email-to-WhatsApp-to-email workflow.
- Location: `src/main.py`
- Contains: Thread management, queue management, workflow logic.
- Depends on: All other services.

**Communication / Messaging:**
- Purpose: Interfaces with external communication channels (Email, WhatsApp).
- Location: `src/email_service.py`, `src/whatsapp_sender.py`, `src/webhook_server.py`
- Contains: SMTP/IMAP clients, Twilio SDK wrappers, Flask web server.
- Depends on: External APIs (Twilio, Mail servers).

**Intelligence / LLM:**
- Purpose: Generates draft responses, detects spam, guesses language, and handles multiple LLM provider routing and fallbacks.
- Location: `src/llm_service.py`, `src/llm_router.py`
- Contains: GenAI SDKs, fallback logic, prompt templates.
- Depends on: External LLM APIs (Gemini, OpenAI, Groq, etc.).

**Business Logic / State / Integrations:**
- Purpose: Tracks runtime state and logs interactions to CRM.
- Location: `src/runtime_state.py`, `src/crm_service.py`
- Contains: State dictionaries, CRM API wrappers.

## Data Flow

**Email Processing & Human-in-the-loop Flow:**

1. **Ingestion:** `src/main.py` fetches unseen emails via `src/email_service.py` and spawns a thread for each email using `process_email_workflow`.
2. **Context Gathering:** `fetch_conversation_history` retrieves previous email replies to build context.
3. **Spam Check:** `src/llm_service.py` evaluates if the email is spam. If so, it discards silently.
4. **Draft Generation:** `src/llm_service.py` generates a response. The request is routed through `src/llm_router.py` to handle potential provider failures.
5. **Human Notification:** `src/whatsapp_sender.py` dispatches the draft and context to the designated reviewer via WhatsApp (Twilio).
6. **Event Wait:** The workflow thread blocks, listening on an in-memory `queue.Queue` tied to the specific reviewer.
7. **Human Feedback:** Reviewer replies on WhatsApp. The webhook hits `src/webhook_server.py`, which pushes the message into the correct workflow queue.
8. **Action:** The workflow thread unblocks, evaluates the feedback (SEND, DISCARD, SAVE, or custom text to REGENERATE).
9. **Finalization:** Depending on the feedback, `src/email_service.py` sends the email, `src/crm_service.py` logs the interaction, and `src/runtime_state.py` clears the pending state.

**State Management:**
- Pending email states and circuit breaker metrics are managed in-memory via global dictionaries in `src/runtime_state.py` and `src/main.py`, synchronized using `threading.Lock()`.
- Thread coordination is handled via `queue.Queue` (`feedback_queues`).
- LLM Provider routing state (circuit breakers) is persisted to `.runtime/llm_router_state.json`.

## Key Abstractions

**LLMRouter:**
- Purpose: Abstracts multiple LLM APIs into a unified interface with automatic failover, backoff, and circuit breaking.
- Examples: `src/llm_router.py`
- Pattern: Strategy / Proxy

## Entry Points

**Main Agent Application:**
- Location: `src/main.py` -> `def main()`
- Triggers: CLI execution (`python src/main.py`).
- Responsibilities: Loads configs, starts the webhook thread, and loops endlessly over configured email accounts to process incoming messages.

**Webhook Server:**
- Location: `src/webhook_server.py`
- Triggers: Incoming HTTP POST requests from Twilio.
- Responsibilities: Receives WhatsApp replies and routes them into the `feedback_queues` to unblock waiting threads.

## Error Handling

**Strategy:** Fail-fast at the API level with automated retries and circuit breakers for external dependencies, but capture workflow errors locally to alert admins via WhatsApp.

**Patterns:**
- **Circuit Breakers:** `src/llm_router.py` tracks consecutive failures and temporarily bans unstable LLM providers.
- **Exception Wrapping:** `src/exceptions.py` defines specific errors like `ConfigError`.
- **Admin Alerts:** Workflow-level exceptions in `process_email_workflow` are caught, logged, and sent to an Admin WhatsApp number.

## Cross-Cutting Concerns

**Logging:** Uses the standard `logging` module. Configured centrally in `src/main.py` to output to both `sys.stdout` and `app.log`.
**Validation:** `src/main.py` explicitly validates required environment variables via `validate_env_vars()` before startup.
**Authentication:** Relies primarily on environment variables (`.env`) to authenticate SMTP, IMAP, Twilio, and LLM APIs.

---

*Architecture analysis: 2024-03-10*