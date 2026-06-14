"""Invoice assembly.

Takes a priced order and rolls the per-line settled amounts up into invoice
totals. By contract, the grand total is the sum of the per-line *settled*
gross amounts — never a re-derivation from the order's pre-settlement
figures — so that the printed total always equals the sum of the printed
lines. This module therefore performs only integer minor-unit addition; all
rounding has already happened upstream in :mod:`domain.pricing` /
:mod:`domain.tax`.
"""

from __future__ import annotations

from domain.models import Customer, Invoice, Order
from domain.pricing import DEFAULT_PRICING, PricingEngine
from infra.audit_log import DEFAULT_AUDIT, AuditLog
from util.ids import next_id
from util.money import sum_minor


class InvoiceBuilder:
    def __init__(
        self,
        pricing: PricingEngine = DEFAULT_PRICING,
        audit: AuditLog = DEFAULT_AUDIT,
    ) -> None:
        self._pricing = pricing
        self._audit = audit

    def build(self, order: Order, customer: Customer) -> Invoice:
        priced = self._pricing.price_order(order, customer)

        subtotal = sum_minor(line.net_minor for line in priced)
        tax_total = sum_minor(line.tax_minor for line in priced)
        # Grand total is the sum of settled line grosses, by contract.
        grand_total = sum_minor(line.gross_minor for line in priced)

        invoice = Invoice(
            id=next_id("inv"),
            order_id=order.id,
            customer_id=customer.id,
            currency=order.target_currency,
            lines=priced,
            subtotal_minor=subtotal,
            tax_total_minor=tax_total,
            grand_total_minor=grand_total,
        )
        self._audit.record(
            "invoice.built",
            invoice.id,
            order_id=order.id,
            grand_total_minor=grand_total,
            currency=invoice.currency,
        )
        return invoice


DEFAULT_BUILDER = InvoiceBuilder()
