"""Read-only reporting over persisted invoices.

Aggregates already-settled invoice totals for dashboards. Performs only
integer addition over stored minor-unit fields — it never re-prices or
re-rounds, so any per-invoice rounding error upstream simply flows through
into the aggregate. Useful context for the totals investigation: a report
that 'looks wrong' is faithfully reflecting whatever the invoices stored.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from domain.models import Invoice
from infra.repository import InvoiceRepository
from util.money import sum_minor


@dataclass
class RevenueReport:
    currency: str
    invoice_count: int
    net_minor: int
    tax_minor: int
    gross_minor: int


class ReportingService:
    def __init__(self, invoices: InvoiceRepository) -> None:
        self._invoices = invoices

    def by_currency(self) -> Dict[str, RevenueReport]:
        """Group all stored invoices by settlement currency and total them."""
        buckets: Dict[str, List[Invoice]] = {}
        for inv in self._invoices.all():  # type: ignore[attr-defined]
            buckets.setdefault(inv.currency, []).append(inv)

        reports: Dict[str, RevenueReport] = {}
        for currency, invs in buckets.items():
            reports[currency] = RevenueReport(
                currency=currency,
                invoice_count=len(invs),
                net_minor=sum_minor(i.subtotal_minor for i in invs),
                tax_minor=sum_minor(i.tax_total_minor for i in invs),
                gross_minor=sum_minor(i.grand_total_minor for i in invs),
            )
        return reports

    def customer_lifetime_value(self, customer_id: str) -> int:
        """Total gross billed to a customer across all invoices (minor units)."""
        return self._invoices.total_billed(customer_id)

    def inconsistent_invoices(self) -> List[str]:
        """Ids of stored invoices whose grand total != sum of line grosses.

        A pure integrity check over already-stored integers; it cannot, by
        itself, reveal a rounding-policy bug that made every line internally
        consistent yet collectively a cent high.
        """
        bad: List[str] = []
        for inv in self._invoices.all():  # type: ignore[attr-defined]
            if not inv.totals_consistent():
                bad.append(inv.id)
        return bad
