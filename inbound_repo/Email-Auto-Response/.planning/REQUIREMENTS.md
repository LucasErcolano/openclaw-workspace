# Requirements: Email Auto Response Agent

**Defined:** 2026-03-10
**Core Value:** Reliable, human-verified automated email responses with a robust fallback system. If everything else fails, the human-in-the-loop mechanism must remain available, ensuring that no email is sent without explicit approval and long emails are correctly processed.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Core Processing (Existing)

- [x] **CORE-01**: System actively polls IMAP accounts for incoming emails
- [x] **CORE-02**: System filters out spam emails silently
- [x] **CORE-03**: System generates draft responses using an LLM router with failover
- [x] **CORE-04**: System receives feedback from reviewer via WhatsApp webhook
- [x] **CORE-05**: System allows reviewer to SEND, DISCARD, SAVE, or provide custom text to REGENERATE
- [x] **CORE-06**: System sends approved response via email
- [x] **CORE-07**: System logs interactions to a CRM (Google Sheets)

### Messaging Enhancement

- [ ] **MSG-01**: Automatically split long draft messages into multiple WhatsApp messages using the approved `chunk_i` template to overcome the 1600 character limit.
- [ ] **MSG-02**: Ensure the entire context is sent to the reviewer across multiple message chunks if necessary.
- [ ] **MSG-03**: Modify webhook handling (if necessary) to correctly receive instructions for split messages, though the primary action is handling the outbound send.

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Integration

- **INT-01**: Support additional messaging platforms (e.g., Telegram, Slack).

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Changing core event-driven architecture | The current ThreadPool and queue-based system works well and changing it introduces unnecessary risk. |
| Using free text for long messages | The reviewer explicitly wants to ensure the system always functions (even outside the 24h window), requiring template use. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Complete |
| CORE-02 | Phase 1 | Complete |
| CORE-03 | Phase 1 | Complete |
| CORE-04 | Phase 1 | Complete |
| CORE-05 | Phase 1 | Complete |
| CORE-06 | Phase 1 | Complete |
| CORE-07 | Phase 1 | Complete |
| MSG-01 | Pending | Pending |
| MSG-02 | Pending | Pending |
| MSG-03 | Pending | Pending |

**Coverage:**
- v1 requirements: 10 total
- Mapped to phases: 7
- Unmapped: 3 ⚠️

---
*Requirements defined: 2026-03-10*
*Last updated: 2026-03-10 after initialization*
