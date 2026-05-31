# Contributing to nodus-router

## Setup

```bash
git clone https://github.com/Masterplanner25/nodus-router.git
cd nodus-router
pip install -e ".[dev]"
```

The `dev` extra includes `nodus-session` so `RouteMatch.session_key`
returns a real `SessionKey` during testing.

## Running tests

```bash
pytest tests/ -q
```

## Code style

- Python 3.11+
- `nodus-session` is optional — the `try/except ImportError` fallback in
  `resolver.py` must remain; do not import it at module level
- `RoutingTable` is thread-safe — use `threading.Lock` for any new state
- Priority ordering: higher priority = evaluated first (descending sort)

## Submitting changes

1. Fork the repo and create a branch from `main`
2. Add tests for any new behaviour
3. Ensure `pytest tests/ -q` passes
4. Open a pull request with a description of what changes and why
