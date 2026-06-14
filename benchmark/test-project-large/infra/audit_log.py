"""Append-only audit trail for money-affecting operations.

An in-memory ring of structured events. Services emit events here whenever
they create an order, build an invoice, capture a payment, or issue a refund,
so that financial actions are traceable. Reading the project, note that this
is a *sink*: it depends on util only and nothing depends on its return values
for business decisions.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from util.clock import SYSTEM_CLOCK, Clock


@dataclass
class AuditEvent:
    kind: str
    subject_id: str
    at: _dt.datetime
    detail: Dict[str, object] = field(default_factory=dict)


class AuditLog:
    def __init__(self, clock: Clock = SYSTEM_CLOCK, capacity: int = 1024) -> None:
        self._events: List[AuditEvent] = []
        self._clock = clock
        self._capacity = capacity

    def record(self, kind: str, subject_id: str, **detail: object) -> AuditEvent:
        event = AuditEvent(
            kind=kind,
            subject_id=subject_id,
            at=self._clock.now(),
            detail=dict(detail),
        )
        self._events.append(event)
        if len(self._events) > self._capacity:
            self._events.pop(0)
        return event

    def events_for(self, subject_id: str) -> List[AuditEvent]:
        return [e for e in self._events if e.subject_id == subject_id]

    def last(self, kind: Optional[str] = None) -> Optional[AuditEvent]:
        for event in reversed(self._events):
            if kind is None or event.kind == kind:
                return event
        return None

    def __len__(self) -> int:
        return len(self._events)


DEFAULT_AUDIT = AuditLog()
