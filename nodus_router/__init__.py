"""nodus-router — route inbound context to agent + session scope.

Context:
    InboundContext  — channel_id, peer_id, thread_id, roles, metadata

Binding:
    RouteBinding    — fnmatch patterns mapped to an agent_id + priority

Table:
    RoutingTable    — thread-safe ordered list of RouteBinding objects

Resolution:
    RouteMatch      — resolved agent_id + SessionKey + matching binding
    RouteResolver   — evaluate table, return RouteMatch (with default fallback)
"""
from .binding import RouteBinding
from .context import InboundContext
from .resolver import RouteMatch, RouteResolver
from .table import RoutingTable

__all__ = [
    "InboundContext",
    "RouteBinding",
    "RoutingTable",
    "RouteMatch",
    "RouteResolver",
]
