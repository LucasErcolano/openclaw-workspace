# Testing Patterns

**Analysis Date:** 2024-05-24

## Test Framework

**Runner:**
- `pytest` (minversion = 8.0)
- Config: `pytest.ini`

**Assertion Library:**
- Standard Python `assert` statements.

**Run Commands:**
```bash
pytest              # Run all tests configured in pytest.ini
pytest -m unit      # Run only unit tests
```

## Test File Organization

**Location:**
- Tests are located in a dedicated `tests/` directory at the project root.

**Naming:**
- Files: `test_*.py` (e.g., `test_language_and_formatting.py`, `test_e2e_flow.py`).

**Structure:**
```
tests/
├── unit/
├── integration/
├── e2e/
└── load/
```

## Test Structure

**Suite Organization:**
```python
import pytest

@pytest.mark.unit
def test_some_behavior():
    # setup
    # execution
    # assertion
```

**Patterns:**
- **Markers:** Tests use custom pytest markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`, `@pytest.mark.live`) as defined in `pytest.ini`.

## Mocking

**Framework:** `pytest.monkeypatch`

**Patterns:**
```python
@pytest.mark.unit
def test_whatsapp_notification_keeps_newlines(monkeypatch):
    sent = {}

    def _fake_send(_to, _sid, variables):
        sent["variables"] = variables
        return True

    monkeypatch.setattr(whatsapp_sender, "_send_twilio_template", _fake_send)
    # Execution...
    assert "Expected" in sent["variables"]["1"]
```

**What to Mock:**
- Network calls, API integrations (like Twilio `_send_twilio_template`), and external service boundaries during unit testing.

**What NOT to Mock:**
- In integration and live tests, external interactions are sometimes tested against real APIs or controlled stubs.

## Fixtures and Factories

**Test Data:**
- Simple dictionaries and string literals are used as inline fixtures for testing formatting and logic functions.
```python
result = {
    "language": "en",
    "body": "Dear team,\n\nThanks.",
    "attachments": ["brochure.pdf"],
}
```

**Location:**
- Currently defined inline within test functions or modules.

## Coverage

**Requirements:** None enforced in `pytest.ini`.

**View Coverage:**
```bash
pytest --cov=src
```

## Test Types

**Unit Tests:**
- Marked with `@pytest.mark.unit`.
- Pure unit tests with no network or filesystem beyond temp directories. Used extensively for logic like `_normalize_email_body` and LLM result normalization.

**Integration Tests:**
- Marked with `@pytest.mark.integration`.
- Integration tests with controlled IO, which may require environment variables.

**E2E Tests:**
- Marked with `@pytest.mark.e2e` and `@pytest.mark.live`.
- Includes full workflow tests. `tests/test_e2e_flow.py` orchestrates real calls (SMTP, IMAP, Webhooks) and API polling to assert the full end-to-end life cycle of the application across different scenarios ("LISTO", "ELIMINAR", "SPAM", "FEEDBACK").

## Common Patterns

**Async Testing:**
- The codebase is predominantly synchronous, relying on retries for blocking network IO.

**Error Testing:**
- Usually tests check for specific logic fallbacks (e.g., invalid language defaulting to "es" or "en").

---

*Testing analysis: 2024-05-24*