"""Plain data models shared across the domain.

Amounts that are *quoted* (catalog prices, computed line subtotals before
settlement) are carried as ``Decimal`` major units. Amounts that are
*settled* (what lands on an invoice line) are integer minor units. The
boundary between the two is owned by :mod:`domain.pricing`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional


@dataclass
class Customer:
    id: str
    name: str
    country: str
    tax_exempt: bool = False


@dataclass
class CatalogItem:
    sku: str
    name: str
    unit_price: Decimal  # major units, in `currency`
    currency: str
    tax_category: str = "standard"


@dataclass
class OrderLine:
    """A requested line on an order, prior to pricing.

    ``unit_price`` and ``currency`` are snapshotted from the catalog at order
    time so later catalog edits do not retroactively change the order.
    """

    sku: str
    quantity: int
    unit_price: Decimal
    currency: str
    tax_category: str = "standard"


@dataclass
class Order:
    id: str
    customer_id: str
    target_currency: str  # the currency the invoice will settle in
    lines: List[OrderLine] = field(default_factory=list)
    discount_code: Optional[str] = None

    def source_currencies(self) -> List[str]:
        """Distinct native currencies across the order's lines."""
        seen: List[str] = []
        for line in self.lines:
            if line.currency not in seen:
                seen.append(line.currency)
        return seen

    def is_multi_currency(self) -> bool:
        """True when at least one line settles across a currency boundary.

        An order is multi-currency if any line's native currency differs from
        the settlement (target) currency. These are exactly the orders whose
        line nets require FX conversion before settlement.
        """
        return any(line.currency != self.target_currency for line in self.lines)


@dataclass
class PricedLine:
    """A fully priced line, ready to be rendered onto an invoice.

    All money fields are integer minor units in the *invoice* currency.
    """

    sku: str
    quantity: int
    net_minor: int      # after discount, before tax
    tax_minor: int      # tax charged on this line
    gross_minor: int    # net + tax
    currency: str


@dataclass
class Invoice:
    id: str
    order_id: str
    customer_id: str
    currency: str
    lines: List[PricedLine] = field(default_factory=list)
    subtotal_minor: int = 0   # sum of line net
    tax_total_minor: int = 0  # sum of line tax
    grand_total_minor: int = 0

    def line_count(self) -> int:
        return len(self.lines)

    def sum_of_line_gross(self) -> int:
        """Independent re-sum of the printed line grosses.

        Exposed so callers can cross-check that the stored ``grand_total_minor``
        equals what the printed lines add up to.
        """
        return sum(line.gross_minor for line in self.lines)

    def totals_consistent(self) -> bool:
        """True iff the stored grand total equals the sum of line grosses."""
        return self.grand_total_minor == self.sum_of_line_gross()
