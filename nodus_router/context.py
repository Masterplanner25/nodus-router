"""InboundContext — what routing evaluates to find the right agent+session."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InboundContext:
    """Describes an inbound message or event that needs to be routed.

    Attributes
    ----------
    channel_id:  The channel the message arrived on (e.g. ``"slack"``).
    peer_id:     Platform-native sender ID (e.g. ``"U0123456"``).
    thread_id:   Thread or topic ID (for threaded channels).
    roles:       Sender's roles or groups (e.g. Discord guild roles).
    metadata:    Additional routing hints (account ID, guild ID, etc.).
    """

    channel_id: str
    peer_id: str | None = None
    thread_id: str | None = None
    roles: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
