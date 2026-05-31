"""RouteResolver — evaluate a RoutingTable and return a RouteMatch."""
from __future__ import annotations

from dataclasses import dataclass

from .binding import RouteBinding
from .context import InboundContext
from .table import RoutingTable

try:
    from nodus_session import SessionKey as _SessionKey
except ImportError:
    from dataclasses import dataclass as _dc  # type: ignore[assignment]

    @_dc
    class _SessionKey:  # type: ignore[no-redef]
        agent_id: str
        channel: str | None = None
        peer: str | None = None
        thread: str | None = None

        def to_string(self):
            parts = [self.agent_id]
            if self.channel and self.peer:
                parts.append(f"channel:{self.channel}")
                parts.append(f"peer:{self.peer}")
            return "!".join(parts)

        @classmethod
        def from_string(cls, raw):
            return cls(agent_id=raw)


@dataclass
class RouteMatch:
    """The result of route resolution.

    Attributes
    ----------
    agent_id:    The agent that should handle this context.
    session_key: The session key for this agent + context combination.
    binding:     The ``RouteBinding`` that produced this match.
    """

    agent_id: str
    session_key: "_SessionKey"
    binding: RouteBinding


def _build_session_key(agent_id: str, ctx: InboundContext) -> "_SessionKey":
    """Build a SessionKey from a route match and its context."""
    return _SessionKey(
        agent_id=agent_id,
        channel=ctx.channel_id,
        peer=ctx.peer_id,
        thread=ctx.thread_id,
    )


class RouteResolver:
    """Evaluate the routing table and return the first match.

    Args:
        table:             The ordered routing table.
        default_agent_id:  Agent to use when no binding matches (default: ``"main"``).
    """

    def __init__(
        self,
        table: RoutingTable,
        default_agent_id: str = "main",
    ) -> None:
        self._table = table
        self._default_agent_id = default_agent_id

    def resolve(self, ctx: InboundContext) -> RouteMatch:
        """Return the first matching ``RouteMatch`` for *ctx*.

        Falls back to *default_agent_id* when no binding matches.
        """
        for binding in self._table.bindings():
            if binding.matches(ctx):
                return RouteMatch(
                    agent_id=binding.agent_id,
                    session_key=_build_session_key(binding.agent_id, ctx),
                    binding=binding,
                )

        # Default fallback
        default_binding = RouteBinding(
            agent_id=self._default_agent_id,
            priority=999,
        )
        return RouteMatch(
            agent_id=self._default_agent_id,
            session_key=_build_session_key(self._default_agent_id, ctx),
            binding=default_binding,
        )
