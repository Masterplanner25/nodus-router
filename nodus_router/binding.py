"""RouteBinding — fnmatch pattern matching on inbound context fields."""
from __future__ import annotations

import fnmatch
from dataclasses import dataclass

from .context import InboundContext


@dataclass
class RouteBinding:
    """One routing rule that maps a context pattern to an agent.

    All patterns use :func:`fnmatch.fnmatch` semantics:
    ``"*"`` matches anything, ``"slack"`` matches exactly, ``"sl*"`` matches
    any string starting with ``"sl"``.

    Attributes
    ----------
    agent_id:        Target agent when this binding matches.
    channel_pattern: Pattern matched against ``InboundContext.channel_id``.
    peer_pattern:    Pattern matched against ``InboundContext.peer_id``.
    role_pattern:    Pattern matched against any item in ``InboundContext.roles``.
    thread_pattern:  Pattern matched against ``InboundContext.thread_id``.
    priority:        Lower values are evaluated first in the routing table.
    """

    agent_id: str
    channel_pattern: str = "*"
    peer_pattern: str = "*"
    role_pattern: str = "*"
    thread_pattern: str = "*"
    priority: int = 0

    def matches(self, ctx: InboundContext) -> bool:
        """Return True if *ctx* satisfies all pattern constraints."""
        if not fnmatch.fnmatch(ctx.channel_id, self.channel_pattern):
            return False

        if self.peer_pattern != "*":
            if not ctx.peer_id or not fnmatch.fnmatch(ctx.peer_id, self.peer_pattern):
                return False

        if self.role_pattern != "*":
            if not any(fnmatch.fnmatch(role, self.role_pattern) for role in ctx.roles):
                return False

        if self.thread_pattern != "*":
            if not ctx.thread_id or not fnmatch.fnmatch(ctx.thread_id, self.thread_pattern):
                return False

        return True
