"""Currency conversion built on the infra rate source.

Conversion takes a *quoted* major-unit amount and returns a *quoted*
major-unit amount in the target currency, at full Decimal precision. It
deliberately does NOT snap to the minor-unit grid: settlement rounding is
the responsibility of :mod:`domain.pricing`, which owns the single rounding
boundary. Rounding here too would double-round.
"""

from __future__ import annotations

from decimal import Decimal

from infra.rates import DEFAULT_RATES, RateSource


class CurrencyConverter:
    def __init__(self, rates: RateSource = DEFAULT_RATES) -> None:
        self._rates = rates

    def convert(self, amount: Decimal, base: str, quote: str) -> Decimal:
        """Convert ``amount`` from ``base`` to ``quote`` at full precision.

        Returns an unrounded Decimal; the caller decides where to settle.
        """
        if base.upper() == quote.upper():
            return amount
        rate = self._rates.rate(base, quote)
        return amount * rate


DEFAULT_CONVERTER = CurrencyConverter()
