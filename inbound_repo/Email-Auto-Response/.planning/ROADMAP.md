# Project Roadmap

**Granularity:** Coarse
**Coverage:** 10/10 v1 requirements mapped

## Phases

- [x] **Phase 1: Core Processing Pipeline** - Existing foundational email auto-response and feedback loop.
- [ ] **Phase 2: Long Message Delivery** - Reliable chunking and transmission of long messages using Twilio templates.

## Phase Details

### Phase 1: Core Processing Pipeline
**Goal**: Ensure the core email processing pipeline operates smoothly end-to-end.
**Depends on**: None
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, CORE-06, CORE-07
**Success Criteria**:
  1. System polls emails and generates drafts using LLMs.
  2. System sends drafts to reviewer via WhatsApp and receives valid feedback.
  3. System sends the final approved email and logs interactions to the CRM.

### Phase 2: Long Message Delivery
**Goal**: Ensure long emails and context are reliably delivered to the reviewer without truncation or failure, overcoming length limits.
**Depends on**: Phase 1
**Requirements**: MSG-01, MSG-02, MSG-03
**Success Criteria**:
  1. System correctly detects when a draft message exceeds length limits and requires splitting.
  2. Reviewer receives long drafts across multiple WhatsApp messages using the approved `chunk_i` template.
  3. Reviewer can successfully send feedback instructions (SEND, REGENERATE, etc.) in response to split messages without webhook errors.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Processing Pipeline | 0/0 | Complete | - |
| 2. Long Message Delivery | 0/0 | Not started | - |
