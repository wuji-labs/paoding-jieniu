"""Injectable clock so services can be tested deterministically."""

from __future__ import annotations

import datetime as _dt
from typing import Optional


class Clock:
    """A wall-clock wrapper that can be frozen for tests."""

    def __init__(self, fixed: Optional[_dt.datetime] = None) -> None:
        self._fixed = fixed

    def now(self) -> _dt.datetime:
        if self._fixed is not None:
            return self._fixed
        return _dt.datetime.now(_dt.timezone.utc)

    def freeze(self, when: _dt.datetime) -> None:
        self._fixed = when


SYSTEM_CLOCK = Clock()
