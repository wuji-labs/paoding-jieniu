"""Foreign-exchange rate source.

A frozen rate table keyed by ``(base, quote)``. Rates are expressed as the
number of *quote* major units per one *base* major unit, as ``Decimal`` to
avoid binary-float drift. Domain currency conversion pulls from here.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, Tuple

from util.errors import CurrencyError

# quote-per-base, deliberately awkward fractions to exercise rounding paths.
# Some pairs (e.g. EUR<->GBP) are intentionally absent so that every
# conversion is expressed against USD as the bridge in practice; orders cross
# only between a source currency and the chosen settlement currency.
_RATES: Dict[Tuple[str, str], Decimal] = {
    ("EUR", "USD"): Decimal("1.0850"),
    ("USD", "EUR"): Decimal("0.92166"),
    ("GBP", "USD"): Decimal("1.2500"),
    ("USD", "GBP"): Decimal("0.80000"),
    ("CNY", "USD"): Decimal("0.13889"),
    ("USD", "CNY"): Decimal("7.2000"),
    ("EUR", "GBP"): Decimal("0.86250"),
    ("GBP", "EUR"): Decimal("1.15942"),
    ("EUR", "CNY"): Decimal("7.8120"),
    ("CNY", "EUR"): Decimal("0.12801"),
    ("GBP", "CNY"): Decimal("9.0000"),
    ("CNY", "GBP"): Decimal("0.11111"),
    ("JPY", "USD"): Decimal("0.0066667"),
    ("USD", "JPY"): Decimal("150.00"),
}


class RateSource:
    """Read-only access to the frozen FX table."""

    def rate(self, base: str, quote: str) -> Decimal:
        base, quote = base.upper(), quote.upper()
        if base == quote:
            return Decimal(1)
        try:
            return _RATES[(base, quote)]
        except KeyError as exc:
            raise CurrencyError(f"no rate for {base}->{quote}") from exc


DEFAULT_RATES = RateSource()
