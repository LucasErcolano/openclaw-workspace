# Email Auto Response Agent

## What This Is

An event-driven human-in-the-loop email processing agent. It polls IMAP accounts for incoming emails, filters spam, generates draft responses using LLMs, and sends them to a human reviewer via WhatsApp (Twilio) for approval or regeneration before sending the final response via email.

## Core Value

Reliable, human-verified automated email responses with a robust fallback system. If everything else fails, the human-in-the-loop mechanism must remain available, ensuring that no email is sent without explicit approval and long emails are correctly processed.

## Requirements

### Validated

- ✓ Actively polls IMAP accounts for incoming emails — existing
- ✓ Filters out spam emails silently — existing
- ✓ Generates draft responses using an LLM router with failover — existing
- ✓ Sends draft and context to reviewer via WhatsApp (Twilio) — existing
- ✓ Receives feedback from reviewer via WhatsApp webhook — existing
- ✓ Allows reviewer to SEND, DISCARD, SAVE, or provide custom text to REGENERATE — existing
- ✓ Sends approved response via email — existing
- ✓ Logs interactions to a CRM (Google Sheets) — existing

### Active

- [ ] REQ-01: Automatically split long draft messages into multiple WhatsApp messages using the approved `chunk_i` template to overcome the 1600 character limit, ensuring the entire context is sent to the reviewer.
- [ ] REQ-02: Modify webhook handling to support processing of split messages or correctly receive instructions for split messages if necessary (although the primary requirement is sending split messages).

### Out of Scope

- Changing the core event-driven architecture — The current ThreadPool and queue-based system works well and changing it introduces unnecessary risk.
- Adding additional messaging platforms (e.g., Telegram, Slack) — The current focus is specifically on fixing the WhatsApp long message issue via Twilio.

## Context

- The system currently uses Twilio for WhatsApp messaging.
- There is a known issue where long text messages (over the 24h free text window or over length limits) fail or are truncated.
- We have an approved Twilio template named `chunk_i` (Content template SID: `HX3c37e5834220c892502e407072a5de2d`) specifically designed to handle long messages by indicating continuation ("Continuará...").
- The template has a limit of 25/1600 characters for the body text parameter `{{1}}`.
- The reviewer explicitly wants to ensure the system always functions (even outside the 24h window), which implies heavily relying on approved templates rather than free text.

## Constraints

- **Tech Stack**: Must remain Python 3.10 and Flask.
- **Dependency**: Must use the existing Twilio SDK.
- **Messaging**: Must utilize the specifically approved `chunk_i` template for long message chunks to guarantee delivery outside the 24h session window.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Implement chunking using `chunk_i` template | Solves the long message delivery problem and ensures delivery outside the 24h session window by using an approved template. | — Pending |

---
*Last updated: 2026-03-10 after initialization*
