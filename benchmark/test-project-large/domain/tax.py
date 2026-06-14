"""Tax computation.

Given a *net* amount already expressed in the invoice currency (major-unit
Decimal, unrounded), compute the tax amount, settled to the currency grid.

Tax is the point where a quoted amount first becomes a settled minor-unit
value, so this module calls the shared settlement choke point
:func:`util.money.quantize_minor`. The group accounting standard for
settlement rounding is banker's rounding (round-half-to-even); see
:mod:`util.money`. We rely on ``quantize_minor`` to apply that standard so
the policy is defined in exactly one place.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict

from util.money import from_minor, quantize_minor, to_minor

# tax_category -> rate, by destination country.
_RATES: Dict[str, Dict[str, Decimal]] = {
    "US": {"standard": Decimal("0.0725"), "reduced": Decimal("0.0000")},
    "DE": {"standard": Decimal("0.19"), "reduced": Decimal("0.07")},
    "GB": {"standard": Decimal("0.20"), "reduced": Decimal("0.05")},
    "CN": {"standard": Decimal("0.13"), "reduced": Decimal("0.09")},
}

_DEFAULT_RATE = Decimal("0.10")

# Countries that operate a reverse-charge mechanism for B2B cross-border
# supplies. For these, tax is accounted by the buyer, so the supplier charges
# zero — but only when the customer is flagged tax-exempt upstream. Listed
# here so the rate table stays declarative.
_REVERSE_CHARGE = {"DE", "GB"}


def tax_rate(country: str, category: str) -> Decimal:
    """Return the tax rate for a country/category pair."""
    return _RATES.get(country.upper(), {}).get(category, _DEFAULT_RATE)


def is_reverse_charge(country: str) -> bool:
    """True if ``country`` uses a reverse-charge mechanism for B2B supplies."""
    return country.upper() in _REVERSE_CHARGE


def tax_on_net(net_minor: int, currency: str, country: str, category: str) -> int:
    """Compute settled tax (minor units) on a settled net amount.

    The net is inflated back to major units, multiplied by the rate, then
    snapped to the currency grid through the shared settlement boundary and
    collapsed to integer minor units.
    """
    rate = tax_rate(country, category)
    net_major = from_minor(net_minor, currency)
    raw_tax = net_major * rate
    settled = quantize_minor(raw_tax, currency)
    return to_minor(settled, currency)


def effective_rate(net_minor: int, tax_minor: int) -> Decimal:
    """Return the realized tax rate for a settled line (for reporting)."""
    if net_minor == 0:
        return Decimal(0)
    return (Decimal(tax_minor) / Decimal(net_minor)).quantize(Decimal("0.0001"))
