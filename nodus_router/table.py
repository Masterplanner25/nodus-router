"""RoutingTable — ordered list of RouteBinding objects."""
from __future__ import annotations

import threading

from .binding import RouteBinding


class RoutingTable:
    """Thread-safe ordered list of ``RouteBinding`` objects.

    Bindings are sorted by ``priority`` (ascending) and evaluated in order.
    """

    def __init__(self) -> None:
        self._bindings: list[RouteBinding] = []
        self._lock = threading.Lock()

    def add(self, binding: RouteBinding) -> None:
        """Add *binding*, maintaining sort by priority."""
        with self._lock:
            self._bindings.append(binding)
            self._bindings.sort(key=lambda b: b.priority)

    def remove(self, agent_id: str) -> int:
        """Remove all bindings for *agent_id*. Returns count removed."""
        with self._lock:
            before = len(self._bindings)
            self._bindings = [b for b in self._bindings if b.agent_id != agent_id]
            return before - len(self._bindings)

    def bindings(self) -> list[RouteBinding]:
        """Return a copy of the ordered binding list."""
        with self._lock:
            return list(self._bindings)

    def __len__(self) -> int:
        with self._lock:
            return len(self._bindings)
