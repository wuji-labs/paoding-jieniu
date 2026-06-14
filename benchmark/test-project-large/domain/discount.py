"""Discount resolution.

Discounts are expressed as a fraction of the net line amount. Resolution is
pure: given a code, return the multiplier to apply. Applying the multiplier
(and any rounding) is the caller's job in :mod:`domain.pricing` — this module
never touches minor units or rounding, only fractions.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Optional

# Hard cap: no stacked discount may reduce a line below this fraction of net.
_MAX_DISCOUNT = Decimal("0.50")


@dataclass(frozen=True)
class DiscountRule:
    code: str
    fraction: Decimal
    stackable: bool = False
    min_lines: int = 0


# code -> rule (fraction off; 0.10 == 10% off)
_DISCOUNTS: Dict[str, DiscountRule] = {
    "WELCOME10": DiscountRule("WELCOME10", Decimal("0.10")),
    "VIP15": DiscountRule("VIP15", Decimal("0.15"), stackable=True),
    "BLACKFRIDAY": DiscountRule("BLACKFRIDAY", Decimal("0.2025")),
    "BULK5": DiscountRule("BULK5", Decimal("0.05"), stackable=True, min_lines=3),
}


def _lookup(code: Optional[str]) -> Optional[DiscountRule]:
    if not code:
        return None
    return _DISCOUNTS.get(code.upper())


def discount_fraction(code: Optional[str]) -> Decimal:
    """Return the fraction-off for ``code`` (``0`` if absent/unknown)."""
    rule = _lookup(code)
    return rule.fraction if rule else Decimal(0)


def net_multiplier(code: Optional[str]) -> Decimal:
    """Return the factor to multiply a gross-of-discount net amount by."""
    return Decimal(1) - discount_fraction(code)


def is_applicable(code: Optional[str], line_count: int) -> bool:
    """Whether a discount's eligibility constraints are met for an order."""
    rule = _lookup(code)
    if rule is None:
        return code is None or code == ""
    return line_count >= rule.min_lines


def combined_fraction(codes: list[str], line_count: int) -> Decimal:
    """Combine multiple stackable discount codes, capped at ``_MAX_DISCOUNT``.

    Non-stackable codes are taken as the single best applicable discount; any
    stackable codes add on top. The result is clamped so a line is never
    discounted below half its net.
    """
    best_single = Decimal(0)
    stacked = Decimal(0)
    for code in codes:
        rule = _lookup(code)
        if rule is None or line_count < rule.min_lines:
            continue
        if rule.stackable:
            stacked += rule.fraction
        else:
            best_single = max(best_single, rule.fraction)
    total = best_single + stacked
    return min(total, _MAX_DISCOUNT)
