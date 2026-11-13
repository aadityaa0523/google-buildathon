"""
Nexus Controllable Clock Provider
Allows simulation of exact time advancement for deadline expiry and retention tests.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional


class Clock:
    def __init__(self, initial_time: Optional[datetime] = None):
        self._current_time = initial_time or datetime.now(timezone.utc)
        self._is_frozen = initial_time is not None

    def now(self) -> datetime:
        if self._is_frozen:
            return self._current_time
        return datetime.now(timezone.utc)

    def now_iso(self) -> str:
        return self.now().isoformat()

    def advance(self, seconds: float = 0, minutes: float = 0, hours: float = 0, days: float = 0):
        """Advance the frozen clock by specified duration."""
        self._is_frozen = True
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        self._current_time += delta

    def set_time(self, new_time: datetime):
        """Set clock to an explicit datetime."""
        self._is_frozen = True
        if new_time.tzinfo is None:
            new_time = new_time.replace(tzinfo=timezone.utc)
        self._current_time = new_time

    def reset_to_realtime(self):
        """Unfreeze clock and resume real system time."""
        self._is_frozen = False


# Global default application clock
global_clock = Clock()

