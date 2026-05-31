import pytest
from nodus_router import (
    InboundContext, RouteBinding, RouteMatch, RouteResolver, RoutingTable,
)


def _ctx(channel="slack", peer="U1", thread=None, roles=None):
    return InboundContext(
        channel_id=channel, peer_id=peer,
        thread_id=thread, roles=roles or [],
    )


def _table(*bindings):
    t = RoutingTable()
    for b in bindings:
        t.add(b)
    return t


# ── RouteBinding.matches ──────────────────────────────────────────────────────

def test_wildcard_matches_all():
    b = RouteBinding("main")   # all defaults = "*"
    assert b.matches(_ctx("slack", "U1")) is True
    assert b.matches(_ctx("discord", "D2")) is True


def test_channel_pattern_match():
    b = RouteBinding("agent", channel_pattern="slack")
    assert b.matches(_ctx("slack")) is True
    assert b.matches(_ctx("discord")) is False


def test_channel_pattern_wildcard():
    b = RouteBinding("agent", channel_pattern="sl*")
    assert b.matches(_ctx("slack")) is True
    assert b.matches(_ctx("slackcorp")) is True
    assert b.matches(_ctx("discord")) is False


def test_peer_pattern():
    b = RouteBinding("agent", peer_pattern="U123*")
    assert b.matches(_ctx(peer="U12345")) is True
    assert b.matches(_ctx(peer="D999")) is False


def test_peer_pattern_no_peer_fails():
    b = RouteBinding("agent", peer_pattern="U*")
    assert b.matches(InboundContext(channel_id="slack")) is False


def test_role_pattern():
    b = RouteBinding("agent", role_pattern="admin*")
    assert b.matches(_ctx(roles=["admin", "user"])) is True
    assert b.matches(_ctx(roles=["user"])) is False


def test_thread_pattern():
    b = RouteBinding("agent", thread_pattern="thread-*")
    assert b.matches(_ctx(thread="thread-123")) is True
    assert b.matches(_ctx(thread="dm-456")) is False


def test_thread_pattern_no_thread_fails():
    b = RouteBinding("agent", thread_pattern="t*")
    assert b.matches(_ctx()) is False


# ── RoutingTable ──────────────────────────────────────────────────────────────

def test_table_add_and_length():
    t = RoutingTable()
    assert len(t) == 0
    t.add(RouteBinding("a"))
    assert len(t) == 1


def test_table_sorted_by_priority():
    t = RoutingTable()
    t.add(RouteBinding("low", priority=10))
    t.add(RouteBinding("high", priority=1))
    bindings = t.bindings()
    assert bindings[0].agent_id == "high"


def test_table_remove():
    t = RoutingTable()
    t.add(RouteBinding("a", channel_pattern="slack"))
    t.add(RouteBinding("a", channel_pattern="discord"))
    assert t.remove("a") == 2
    assert len(t) == 0


def test_table_remove_unknown():
    t = RoutingTable()
    assert t.remove("nonexistent") == 0


# ── RouteResolver ─────────────────────────────────────────────────────────────

def test_resolve_first_match():
    t = _table(
        RouteBinding("slack-agent", channel_pattern="slack", priority=0),
        RouteBinding("default-agent", priority=1),
    )
    r = RouteResolver(t)
    match = r.resolve(_ctx("slack"))
    assert match.agent_id == "slack-agent"


def test_resolve_fallback_to_default():
    t = _table(RouteBinding("special", channel_pattern="discord"))
    r = RouteResolver(t, default_agent_id="fallback")
    match = r.resolve(_ctx("telegram"))
    assert match.agent_id == "fallback"


def test_resolve_empty_table_uses_default():
    r = RouteResolver(RoutingTable(), default_agent_id="main")
    match = r.resolve(_ctx("slack"))
    assert match.agent_id == "main"


def test_resolve_returns_session_key_with_channel():
    t = _table(RouteBinding("main"))
    r = RouteResolver(t)
    match = r.resolve(_ctx("discord", "D123"))
    assert match.session_key.channel == "discord"
    assert match.session_key.peer == "D123"
    assert match.session_key.agent_id == "main"


def test_resolve_returns_binding():
    binding = RouteBinding("agent", channel_pattern="slack")
    t = _table(binding)
    r = RouteResolver(t)
    match = r.resolve(_ctx("slack"))
    assert match.binding is binding


def test_priority_order_respected():
    t = RoutingTable()
    t.add(RouteBinding("first", channel_pattern="slack", priority=0))
    t.add(RouteBinding("second", channel_pattern="slack", priority=1))
    r = RouteResolver(t)
    match = r.resolve(_ctx("slack"))
    assert match.agent_id == "first"
