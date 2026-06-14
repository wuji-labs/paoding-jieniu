"""Line pricing: the composition point for currency, discount, and tax.

Pipeline per order line:

1. Extend the snapshotted unit price by quantity (quoted major units, in the
   line's source currency).
2. Convert to the invoice currency at full precision
   (:mod:`domain.currency`).
3. Apply the order discount multiplier (:mod:`domain.discount`).
4. **Settle** the net amount to the invoice-currency minor-unit grid through
   the shared rounding boundary (:func:`util.money.quantize_minor`), then to
   integer minor units. This is the single place a line's net becomes money.
5. Compute tax on the settled net (:mod:`domain.tax`).

The settlement boundary in step 4 is intentionally the same choke point tax
uses, so a line's net and its tax round under one consistent policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List

from domain.currency import DEFAULT_CONVERTER, CurrencyConverter
from domain.discount import discount_fraction, net_multiplier
from domain.models import Customer, Order, OrderLine, PricedLine
from domain.tax import tax_on_net
from util.money import quantize_minor, sum_minor, to_minor


@dataclass
class PricingSummary:
    """Roll-up of a priced order, used for previews before invoicing."""

    net_minor: int
    tax_minor: int
    gross_minor: int
    discount_fraction: Decimal
    currency: str


class PricingEngine:
    """Composes currency conversion, discounts, and tax into settled lines."""

    def __init__(self, converter: CurrencyConverter = DEFAULT_CONVERTER) -> None:
        self._converter = converter

    def _convert_extended(self, line: OrderLine, order: Order) -> Decimal:
        """Extend a line by quantity and convert to the invoice currency.

        Returns an unrounded Decimal in the invoice currency; settlement is a
        separate, later step so there is exactly one rounding boundary.
        """
        extended = line.unit_price * Decimal(line.quantity)
        return self._converter.convert(
            extended, line.currency, order.target_currency
        )

    def _settle_net(self, line: OrderLine, order: Order) -> int:
        """Compute the settled net (minor units, invoice currency) for a line."""
        converted = self._convert_extended(line, order)
        discounted = converted * net_multiplier(order.discount_code)
        # Single settlement boundary for the line net.
        settled = quantize_minor(discounted, order.target_currency)
        return to_minor(settled, order.target_currency)

    def price_line(self, line: OrderLine, order: Order, customer: Customer) -> PricedLine:
        net_minor = self._settle_net(line, order)
        if customer.tax_exempt:
            tax_minor = 0
        else:
            tax_minor = tax_on_net(
                net_minor,
                order.target_currency,
                customer.country,
                line.tax_category,
            )
        return PricedLine(
            sku=line.sku,
            quantity=line.quantity,
            net_minor=net_minor,
            tax_minor=tax_minor,
            gross_minor=net_minor + tax_minor,
            currency=order.target_currency,
        )

    def price_order(self, order: Order, customer: Customer) -> List[PricedLine]:
        return [self.price_line(line, order, customer) for line in order.lines]

    def summarize(self, order: Order, customer: Customer) -> PricingSummary:
        """Produce a totals-only summary without persisting anything."""
        priced = self.price_order(order, customer)
        return PricingSummary(
            net_minor=sum_minor(p.net_minor for p in priced),
            tax_minor=sum_minor(p.tax_minor for p in priced),
            gross_minor=sum_minor(p.gross_minor for p in priced),
            discount_fraction=discount_fraction(order.discount_code),
            currency=order.target_currency,
        )


DEFAULT_PRICING = PricingEngine()
