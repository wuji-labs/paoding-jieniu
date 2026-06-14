"""Order-level fees (shipping, handling) and their allocation to lines.

Fees are quoted as a flat amount in the invoice currency plus an optional
per-line handling component. The flat amount is split across lines in
proportion to their gross, using :func:`util.money.allocate` so the per-line
fee shares always sum back to the exact fee total (no penny leak).

This module is pure: it takes already-settled line grosses and returns
integer minor-unit fee shares. It does not re-price or re-round line amounts,
and it does not touch the settlement boundary in :mod:`util.money` that the
pricing/tax path uses.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Sequence

from util.money import allocate, quantize_minor, to_minor

# Flat shipping fee table keyed by destination zone, in invoice major units.
_ZONE_FLAT = {
    "domestic": Decimal("4.99"),
    "regional": Decimal("9.99"),
    "intl": Decimal("19.99"),
}

# Per-line handling surcharge (major units) applied once per distinct line.
_HANDLING_PER_LINE = Decimal("0.35")


@dataclass
class FeeBreakdown:
    flat_minor: int
    handling_minor: int
    total_minor: int
    per_line_minor: List[int]
    currency: str


def _flat_for_zone(zone: str) -> Decimal:
    return _ZONE_FLAT.get(zone, _ZONE_FLAT["regional"])


def compute_fees(
    line_grosses: Sequence[int],
    currency: str,
    zone: str = "regional",
) -> FeeBreakdown:
    """Compute and allocate order-level fees across the given line grosses.

    The flat shipping fee is settled to the currency grid, the handling
    surcharge is per line, and the combined total is allocated back across the
    lines proportionally to gross.
    """
    flat_minor = to_minor(quantize_minor(_flat_for_zone(zone), currency), currency)
    handling_major = _HANDLING_PER_LINE * Decimal(len(line_grosses))
    handling_minor = to_minor(quantize_minor(handling_major, currency), currency)
    total_minor = flat_minor + handling_minor

    weights = list(line_grosses) or [1]
    per_line = allocate(total_minor, weights)

    return FeeBreakdown(
        flat_minor=flat_minor,
        handling_minor=handling_minor,
        total_minor=total_minor,
        per_line_minor=per_line,
        currency=currency,
    )
