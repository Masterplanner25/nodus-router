# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.1.0] — 2026-05-31

Initial release — prepared, not yet published.

### Added

- **`InboundContext`** — inbound message context. Fields: `channel_id`,
  `peer_id`, `thread_id` (optional), `roles` (list, default `[]`),
  `metadata` (dict, default `{}`).

- **`RouteBinding`** — fnmatch pattern → agent mapping. Fields:
  `channel_pattern`, `peer_pattern`, `agent_id`, `priority` (int,
  higher = evaluated first).

- **`RoutingTable`** — thread-safe ordered binding registry. `add(binding)`,
  `remove(agent_id)`, `list_bindings()` (sorted by priority descending), `len`.

- **`RouteMatch`** — resolved route. Fields: `agent_id`, `session_key`
  (`SessionKey` from nodus-session if installed, else fallback dataclass),
  `binding` (`RouteBinding | None`; `None` when default fallback was used).

- **`RouteResolver`** — evaluates `RoutingTable` against `InboundContext`.
  `resolve(ctx)` → `RouteMatch`. Uses `fnmatch` for pattern matching; first
  binding by priority that matches both `channel_pattern` and `peer_pattern`
  wins. Falls back to `default_agent_id` when no binding matches.

- **`nodus-session` optional integration** — `RouteMatch.session_key` uses
  `nodus_session.SessionKey` when installed; falls back to an inline dataclass
  with identical fields when absent (`try/except ImportError`).

- **18 tests** in `tests/test_router.py`.

- **No required dependencies** — pure stdlib (`fnmatch`, `threading`,
  `dataclasses`). `nodus-session` is an optional extra.

[0.1.0]: https://github.com/Masterplanner25/nodus-router/releases/tag/v0.1.0
