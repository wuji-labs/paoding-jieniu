"""Serialization helpers: domain models -> JSON-ready dicts.

These functions only *format* already-computed values. They convert integer
minor units to a human string using the currency exponent, but perform no
arithmetic that could change a total (no re-summing, no re-rounding).
"""

from __future__ import annotations

from typing import Dict, List

from domain.models import Invoice, Order, PricedLine
from util.money import format_money, from_minor


def _money(minor: int, currency: str) -> Dict[str, object]:
    return {
        "minor": minor,
        "currency": currency,
        "display": str(from_minor(minor, currency)),
        "formatted": format_money(minor, currency),
    }


def serialize_line(line: PricedLine) -> Dict[str, object]:
    return {
        "sku": line.sku,
        "quantity": line.quantity,
        "net": _money(line.net_minor, line.currency),
        "tax": _money(line.tax_minor, line.currency),
        "gross": _money(line.gross_minor, line.currency),
    }


def serialize_invoice(invoice: Invoice) -> Dict[str, object]:
    lines: List[Dict[str, object]] = [serialize_line(l) for l in invoice.lines]
    return {
        "id": invoice.id,
        "order_id": invoice.order_id,
        "customer_id": invoice.customer_id,
        "currency": invoice.currency,
        "lines": lines,
        "subtotal": _money(invoice.subtotal_minor, invoice.currency),
        "tax_total": _money(invoice.tax_total_minor, invoice.currency),
        "grand_total": _money(invoice.grand_total_minor, invoice.currency),
        "line_count": invoice.line_count(),
        # Cross-check field clients may surface: does the stored grand total
        # equal the sum of the printed line grosses?
        "totals_consistent": invoice.totals_consistent(),
    }


def serialize_order(order: Order) -> Dict[str, object]:
    """Compact order representation for the order API."""
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "target_currency": order.target_currency,
        "line_count": len(order.lines),
        "discount_code": order.discount_code,
        "source_currencies": order.source_currencies(),
        "multi_currency": order.is_multi_currency(),
    }
