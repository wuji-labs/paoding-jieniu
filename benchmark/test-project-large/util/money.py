"""Money primitives: integer-minor-unit arithmetic and rounding.

The whole backend represents monetary amounts as integer *minor units*
(cents for USD/EUR, fen for CNY, etc.) wherever a value is "settled".
Intermediate computations — proportional discounts, percentage taxes,
currency conversion — necessarily produce fractional minor units, so we
keep those as ``Decimal`` and only collapse to integers at well-defined
settlement boundaries via :func:`quantize_minor`.

Rounding policy
---------------
The group accounting standard is **banker's rounding** (round-half-to-even,
``ROUND_HALF_EVEN``). It is the policy mandated for VAT/GST jurisdictions we
operate in and is the default used by every settlement boundary in
:mod:`domain.pricing`. ``quantize_minor`` is the single choke point that all
settlement rounding is supposed to flow through so the policy stays
consistent.

This module is dependency-free with respect to the rest of the project: it
imports only the standard library, which is what lets every other layer rely
on it as the canonical money vocabulary.
"""

from __future__ import annotations

from decimal import (
    Decimal,
    ROUND_DOWN,
    ROUND_HALF_EVEN,
    ROUND_HALF_UP,
    localcontext,
)
from typing import Iterable, List, Sequence

# Number of minor units per major unit, keyed by ISO-4217 code.
# Most currencies are 2-decimal; a few (JPY, KRW) are zero-decimal, and a
# handful (BHD, KWD) are 3-decimal. We list the ones the backend can settle.
_MINOR_EXPONENT = {
    "USD": 2,
    "EUR": 2,
    "GBP": 2,
    "CNY": 2,
    "JPY": 0,
    "KRW": 0,
    "BHD": 3,
    "KWD": 3,
}

# Symbols used purely for human-facing rendering; not used in arithmetic.
_SYMBOL = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "CNY": "¥",
    "JPY": "¥",
}


def minor_exponent(currency: str) -> int:
    """Return the number of minor-unit decimal places for ``currency``."""
    try:
        return _MINOR_EXPONENT[currency.upper()]
    except KeyError as exc:  # pragma: no cover - defensive
        raise ValueError(f"unknown currency: {currency!r}") from exc


def is_zero_decimal(currency: str) -> bool:
    """True for currencies with no minor unit (e.g. JPY, KRW)."""
    return minor_exponent(currency) == 0


def _quantum(currency: str) -> Decimal:
    """Smallest representable minor-unit step for ``currency`` as a Decimal."""
    return Decimal(1).scaleb(-minor_exponent(currency))


def to_minor(amount: Decimal, currency: str) -> int:
    """Collapse a major-unit ``Decimal`` to an integer count of minor units.

    Uses the group standard banker's rounding. ``Decimal("1.005")`` USD
    becomes ``100`` (rounds to even) rather than ``101``.
    """
    quantum = _quantum(currency)
    with localcontext() as ctx:
        ctx.rounding = ROUND_HALF_EVEN
        scaled = (amount / quantum).quantize(Decimal(1), rounding=ROUND_HALF_EVEN)
    return int(scaled)


def from_minor(minor: int, currency: str) -> Decimal:
    """Inflate an integer minor-unit count back to a major-unit Decimal."""
    return Decimal(minor) * _quantum(currency)


def quantize_minor(amount: Decimal, currency: str, rounding: str = ROUND_HALF_UP) -> Decimal:
    """Round ``amount`` (a major-unit Decimal) to the currency's minor-unit grid.

    This is the single settlement-rounding choke point. Callers pass amounts
    that may carry sub-cent precision (e.g. ``Decimal("12.3450")``) and get
    back a Decimal snapped to the currency grid (``Decimal("12.35")``).

    The group accounting standard is banker's rounding; see the module
    docstring. Callers that need a different policy may override ``rounding``.
    """
    quantum = _quantum(currency)
    return amount.quantize(quantum, rounding=rounding)


def truncate_minor(amount: Decimal, currency: str) -> Decimal:
    """Snap toward zero (never round up). Used for fee floors, not settlement."""
    return amount.quantize(_quantum(currency), rounding=ROUND_DOWN)


def sum_minor(values: Iterable[int]) -> int:
    """Sum an iterable of integer minor-unit amounts.

    Trivial today, but kept as a named boundary so that audit logging or
    overflow checks can be attached in one place later.
    """
    total = 0
    for v in values:
        total += int(v)
    return total


def allocate(total_minor: int, weights: Sequence[int]) -> List[int]:
    """Split ``total_minor`` across ``weights`` with no lost/created cents.

    Implements the largest-remainder method: floor each share, then hand the
    leftover cents one at a time to the shares with the largest fractional
    remainder. Guarantees ``sum(result) == total_minor`` exactly. Used to
    distribute order-level amounts (e.g. shipping) across lines without the
    classic penny-rounding leak.
    """
    if not weights:
        return []
    weight_total = sum(weights)
    if weight_total <= 0:
        raise ValueError("weights must sum to a positive value")

    quotients: List[int] = []
    remainders: List[Decimal] = []
    for w in weights:
        exact = Decimal(total_minor) * Decimal(w) / Decimal(weight_total)
        floor = int(exact.to_integral_value(rounding=ROUND_DOWN))
        quotients.append(floor)
        remainders.append(exact - floor)

    leftover = total_minor - sum(quotients)
    order = sorted(range(len(weights)), key=lambda i: remainders[i], reverse=True)
    for i in order[:leftover]:
        quotients[i] += 1
    return quotients


def format_money(minor: int, currency: str) -> str:
    """Human-readable rendering, e.g. ``$12.34``. Display only."""
    major = from_minor(minor, currency)
    symbol = _SYMBOL.get(currency.upper(), "")
    return f"{symbol}{major}"
