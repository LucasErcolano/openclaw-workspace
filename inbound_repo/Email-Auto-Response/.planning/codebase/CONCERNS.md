# Codebase Concerns

**Analysis Date:** 2024-05-24

## Tech Debt

**Hardcoded Business Logic in Email Processing:**
- Issue: Logic for selecting brochures or identifying companies is hardcoded using explicit Spanish/English keywords (`flex_kw`, `induction_kw`) instead of utilizing LLM routing or a config file.
- Files: `src/llm_service.py`
- Impact: Very fragile when scaling to new languages or products. Fails to find attachments if keywords drift or customers use synonyms.
- Fix approach: Delegate intent and attachment routing directly to the LLM step, or extract configurations into a data-driven mapping layer.

**Hardcoded Account Indices & Context Mapping:**
- Issue: Specific logic maps an index `i == 2` directly to the `ALFA` account context and Twilio sender number.
- Files: `src/main.py`
- Impact: Extremely rigid system. Adding a third company or modifying the second requires source code changes instead of just updating environment variables.
- Fix approach: Move account configurations entirely to JSON/YAML or dynamic loading based on generic environment variables without special-casing index 2.

**Synchronous CRM Updates in Google Sheets:**
- Issue: Google Sheets is updated via `gspread` using multiple synchronous `worksheet.update_cell` calls consecutively.
- Files: `src/crm_service.py`
- Impact: Blocks the thread during slow IO and rapidly consumes Google Sheets API quotas.
- Fix approach: Use `worksheet.update` or `worksheet.append_row` with a single batch list for updates, and execute them asynchronously or on a dedicated background queue.

## Known Bugs

**Message Chunking Breaks Formatting:**
- Symptoms: WhatsApp messages are occasionally corrupted, missing the end of sentences, or display raw markdown tags.
- Files: `src/whatsapp_sender.py`
- Trigger: A message body exceeds the hardcoded `1550` chunk size limit, splitting markdown tags or words arbitrarily.
- Workaround: Keep LLM responses under 1500 characters, though not strictly enforced.

## Security Considerations

**Unverified Webhook Endpoints:**
- Risk: The Twilio webhooks (`/whatsapp`, `/h5k5`, `/alfa`) accept any unauthenticated `POST` request without verifying the Twilio cryptographic signature. Malicious actors could spoof messages to the bot.
- Files: `src/webhook_server.py`
- Current mitigation: None.
- Recommendations: Implement `twilio.request_validator.RequestValidator` middleware to verify that incoming webhook requests genuinely originated from Twilio using the `X-Twilio-Signature` header.

## Performance Bottlenecks

**Synchronous JSON File I/O under Global Lock:**
- Problem: The entire workflow state is read from and written to `workflow_state.json` under a single global thread lock (`_LOCK`) for every minor update.
- Files: `src/runtime_state.py`
- Cause: Suboptimal state management that parses/dumps the whole file inside a locking block.
- Improvement path: Migrate to Redis or SQLite for state management, or at minimum implement an in-memory state with periodic background syncing.

**Blocking Network I/O in Main Loop:**
- Problem: The application relies heavily on `time.sleep` in basic retry loops while interacting with IMAP.
- Files: `src/email_service.py`
- Cause: `_retry_operation` function synchronously blocks the active thread.
- Improvement path: Migrate to `asyncio` for IMAP and external API polling instead of using blocking `time.sleep` with `ThreadPoolExecutor`.

## Fragile Areas

**IMAP Folder Detection:**
- Files: `src/email_service.py`
- Why fragile: Sent folder detection relies on hardcoded string matching (`INBOX.Sent`, `[Gmail]/Sent Mail`, `enviados`). This breaks easily across different IMAP providers, legacy setups, or language locales.
- Safe modification: Fetch folder flags (e.g., `\Sent`) as per RFC 6154 instead of guessing by name, and make the fallback folder configurable per account.
- Test coverage: Gap in handling diverse IMAP provider responses.

## Scaling Limits

**Single-Process Thread Pool:**
- Current capacity: Limited by Python GIL and thread pool limits for I/O bounds.
- Limit: Spikes in incoming emails will saturate the polling threads and webhook server simultaneously, causing missed webhooks or failed message dispatches.
- Scaling path: Decouple the webhook listener, polling, and LLM processing layers into separate scalable workers using an event bus (e.g., RabbitMQ or Redis) or move entirely to an async model.
