# nodus-router

**Route inbound context to agent + session scope via fnmatch binding rules.**

Maps channel/peer/thread patterns to agent IDs with priority-ordered binding
rules. Resolves inbound messages to a `RouteMatch` containing the agent ID,
a `SessionKey`, and the matched binding. No required external dependencies
— pure stdlib with optional `nodus-session` integration.

> **Status:** v0.1.0 — published on [PyPI](https://pypi.org/project/nodus-router/).

---

## Install

```bash
pip install nodus-router

# With nodus-session SessionKey integration:
pip install "nodus-router[session]"
```

---

## What it provides

| Component | Purpose |
|---|---|
| `InboundContext` | Inbound message context: channel, peer, thread, roles, metadata |
| `RouteBinding` | fnmatch pattern → agent_id mapping with priority |
| `RoutingTable` | Thread-safe ordered list of `RouteBinding` objects |
| `RouteResolver` | Evaluates table, returns `RouteMatch` (with default fallback) |
| `RouteMatch` | Resolved agent_id, `SessionKey`, and matched binding |

---

## Quick start

```python
from nodus_router import InboundContext, RouteBinding, RoutingTable, RouteResolver

table = RoutingTable()
table.add(RouteBinding(
    channel_pattern="slack",
    peer_pattern="*",
    agent_id="general-agent",
    priority=10,
))
table.add(RouteBinding(
    channel_pattern="slack",
    peer_pattern="U123*",
    agent_id="vip-agent",
    priority=20,   # higher priority wins
))

resolver = RouteResolver(table, default_agent_id="fallback-agent")

ctx = InboundContext(channel_id="slack", peer_id="U123456", thread_id=None)
match = resolver.resolve(ctx)

print(match.agent_id)        # "vip-agent"
print(match.session_key)     # SessionKey(agent_id="vip-agent", channel="slack", ...)
print(match.binding)         # the matched RouteBinding
```

---

## InboundContext

```python
from nodus_router import InboundContext

ctx = InboundContext(
    channel_id="slack",
    peer_id="U123456",
    thread_id="T789",    # optional
    roles=["user"],      # optional list of role strings
    metadata={},         # optional extra data
)
```

---

## RouteBinding

```python
from nodus_router import RouteBinding

binding = RouteBinding(
    channel_pattern="slack",   # fnmatch — "*" matches any channel
    peer_pattern="U123*",      # fnmatch — matches any peer starting with U123
    agent_id="vip-agent",
    priority=20,               # higher priority evaluated first
)
```

Patterns use `fnmatch` — `*` matches any sequence, `?` matches one character.

---

## RoutingTable

```python
from nodus_router import RoutingTable

table = RoutingTable()
table.add(binding)
table.remove(agent_id="vip-agent")
table.list_bindings()          # list sorted by priority descending
len(table)
```

Thread-safe — safe to add/remove from multiple threads.

---

## RouteResolver

```python
from nodus_router import RouteResolver

resolver = RouteResolver(
    table,
    default_agent_id="fallback-agent",  # used when no binding matches
)

match = resolver.resolve(ctx)
# match.agent_id    — resolved agent
# match.session_key — SessionKey (from nodus-session if installed, else fallback)
# match.binding     — matched RouteBinding | None (None = default fallback)
```

---

## SessionKey integration

When `nodus-session` is installed, `RouteMatch.session_key` is a real
`SessionKey` from that package. Without it, a lightweight fallback dataclass
with the same fields is used — no functionality is lost.

```bash
pip install "nodus-router[session]"
```

---

## Design

- **No required dependencies.** `fnmatch` and `threading` are stdlib.
  `nodus-session` is optional — a fallback `SessionKey` is used when absent.
- **Priority ordering.** Bindings are sorted by `priority` descending;
  first match wins.
- **Thread-safe.** `RoutingTable` uses `threading.Lock`.

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

---

## License

MIT — see [LICENSE](LICENSE).
