"""Deterministic-ish identifier generation for orders, invoices, lines.

Kept dependency-free on purpose: domain and service layers import this but
it imports nothing from the rest of the project. A genuine leaf utility.
"""

from __future__ import annotations

import itertools
import time

_counter = itertools.count(1)


def next_id(prefix: str) -> str:
    """Return a short, monotonically increasing identifier.

    Not cryptographically unique — adequate for in-process test fixtures
    and the in-memory stores used by :mod:`infra`.
    """
    return f"{prefix}_{next(_counter):06d}"


def request_id() -> str:
    """Coarse request correlation id derived from the wall clock."""
    return f"req_{int(time.time() * 1000):x}"
