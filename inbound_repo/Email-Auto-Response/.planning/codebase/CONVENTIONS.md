# Coding Conventions

**Analysis Date:** 2024-05-24

## Naming Patterns

**Files:**
- Snake case for modules (`email_service.py`, `llm_router.py`).

**Functions:**
- Snake case for public functions (`fetch_unseen_emails`, `parse_provider_order`).
- Internal helper functions prefixed with an underscore (`_normalize_email_body`, `_retry_operation`, `_json_from_text`).

**Variables:**
- Snake case for local variables and parameters (`imap_server`, `account_config`, `fetch_days`).
- UPPER_SNAKE_CASE for constants (`DEFAULT_TIMEOUT`, `_RUNTIME_DIR`).

**Types / Classes:**
- PascalCase for class names (`LLMRouter`, `EmailServiceError`).

## Code Style

**Formatting:**
- No strict formatter configuration (like Black or Prettier) detected in the repository root.
- Indentation is 4 spaces (standard Python).

**Linting:**
- No explicit linter configuration (like flake8 or pylint) found.

## Import Organization

**Order:**
1. Standard library imports (`import os`, `import logging`, `import json`).
2. Third-party library imports (`from imap_tools import MailBox`, `from dotenv import load_dotenv`).
3. Local application imports (`from exceptions import EmailServiceError`).

**Path Aliases:**
- No specific path aliases used; relies on PYTHONPATH config (in `pytest.ini` it sets `pythonpath = src`).

## Error Handling

**Patterns:**
- Extensive use of `try/except Exception as e:` blocks wrapped around external calls (IMAP, SMTP, LLM APIs).
- Custom exceptions are used (`EmailServiceError` in `src/exceptions.py`).
- Failures generally log an error using the `logging` module and return a fallback value (e.g., `None`, `False`, or an empty list `[]`) instead of crashing the process.
- Helper functions for retries are implemented: `_retry_operation` in `src/email_service.py`.

## Logging

**Framework:** `logging` (Python standard library)

**Patterns:**
- Instantiated per module: `logger = logging.getLogger(__name__)`.
- Parameterized logging is preferred to avoid eager string formatting (e.g., `logger.error("[%s] Error deleting email %s: %s", email_user, uid, e)`).
- Prefixing logs with the context entity (like `[%s]` for user email) to track parallel execution or specific tenant flow.

## Comments

**When to Comment:**
- Docstrings are used for public functions to describe intent, parameters, and return types.
- Inline comments explain business logic, workarounds, or parsing edge cases (e.g., `# Try to find the Sent folder`).

**JSDoc/TSDoc / Python Docstrings:**
- Uses standard triple-quoted string literals `"""` for functions. Not strictly adhering to a specific docstring format (like Sphinx or Google) but informative.

## Function Design

**Size:** Functions are generally moderately sized, handling one overarching logical operation but sometimes encompassing retries or multiple steps for external API interactions.

**Parameters:** Type hints from the `typing` module (`List`, `Optional`, `Dict`, `Any`, `Tuple`) are heavily used in newer modules like `src/llm_router.py`.

**Return Values:** Usually primitive types, dicts, or specific instances. Use of `Optional` when returning `None` on failure.

## Module Design

**Exports:** 
- Explicit `__all__` is not used. Modules are consumed by directly importing the required functions or classes.

---

*Convention analysis: 2024-05-24*