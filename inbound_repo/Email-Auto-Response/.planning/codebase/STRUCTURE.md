# Codebase Structure

**Analysis Date:** 2024-03-10

## Directory Layout

```
[project-root]/
├── src/            # Core business logic and agent implementation
├── tests/          # Automated test suites (unit, e2e)
├── scripts/        # Utility scripts, deployment helpers, and evaluations
├── assets/         # Static files, PDFs, and company brochures used by the agent
└── .runtime/       # Runtime state persistence (e.g., LLM router state)
```

## Directory Purposes

**`src/`**:
- Purpose: Contains the primary application code, orchestrated by `main.py`.
- Contains: Python modules (`*.py`) for the webhook server, LLM router, and email processing.
- Key files: `src/main.py`, `src/llm_router.py`, `src/webhook_server.py`

**`tests/`**:
- Purpose: Ensures system correctness via test suites.
- Contains: Unit tests and E2E test scripts.
- Key files: `tests/test_e2e_flow.py`, `tests/unit/test_llm_router_policy.py`

**`scripts/`**:
- Purpose: Houses auxiliary tools for analysis, metrics, and operations.
- Contains: Evaluation scripts, log analyzers, and deployment shell scripts.
- Key files: `scripts/watchdog.py`, `scripts/evaluate_egoblur_metrics.py`

**`assets/`**:
- Purpose: Stores contextual attachments and company brochures that the agent may suggest or attach to drafts.
- Contains: PDF files.
- Key files: `assets/Folleto H5K5.HT - OK ENG 01-24 (Baja).pdf`

## Key File Locations

**Entry Points:**
- `src/main.py`: The main polling loop and orchestrator for the email agent.
- `src/webhook_server.py`: The Flask server that receives Twilio callbacks.

**Configuration:**
- `.env`: Environment variable configuration (passwords, keys, phone numbers). *(Not committed)*
- `pytest.ini`: Pytest configuration for the test suites.

**Core Logic:**
- `src/email_service.py`: Handles fetching from IMAP and sending via SMTP.
- `src/llm_service.py`: Prompts generation, spam detection, and translation.
- `src/llm_router.py`: Proxies multiple LLM models with retry and circuit breaking.

**Testing:**
- `tests/test_e2e_flow.py`: Validates the full integration pipeline.
- `tests/unit/test_language_and_formatting.py`: Unit tests for formatting and LLM utilities.

## Naming Conventions

**Files:**
- snake_case: Standard Python modules (e.g., `email_service.py`).
- UPPERCASE for markdown docs: `ARCHITECTURE.md`, `STRUCTURE.md`.

**Directories:**
- lowercase, short names: `src`, `tests`, `scripts`.

## Where to Add New Code

**New Feature:**
- Primary code: `src/[feature_name].py` or integrated into `src/main.py` if related to the core workflow.
- Tests: `tests/unit/test_[feature_name].py`

**New Component/Module:**
- Implementation: Add to `src/` as a distinct `_service.py` file.

**Utilities:**
- Shared helpers: `scripts/` if it's an operational utility, or a new file in `src/` if used directly by the agent.

## Special Directories

**`.runtime/`**:
- Purpose: Contains automatically generated JSON state files (e.g., circuit breaker status).
- Generated: Yes
- Committed: No

**`.planning/`**:
- Purpose: Contains AI-generated codebase mappings and architecture documentation.
- Generated: Yes
- Committed: Yes

---

*Structure analysis: 2024-03-10*