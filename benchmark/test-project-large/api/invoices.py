"""Invoice API handlers.

Endpoints to create an invoice for an existing order and to fetch one back.
These handlers are deliberately thin: they look up the order and customer,
delegate all pricing/assembly to :class:`services.invoice_builder.InvoiceBuilder`,
persist the result, and serialize it. No monetary arithmetic happens here;
the grand total returned to the client is exactly what the builder produced.

If a client reports that a returned ``grand_total`` disagrees with the sum of
the line ``gross`` values it sees, note that *this* layer does not compute
either number — both come straight from the assembled invoice — so the
discrepancy originates upstream in the pricing/assembly chain, not here.
"""

from __future__ import annotations

from typing import Dict

from api.serializers import serialize_invoice
from infra.repository import CustomerRepository, InvoiceRepository, OrderRepository
from services.invoice_builder import DEFAULT_BUILDER, InvoiceBuilder
from util.errors import NotFoundError, ValidationError


class InvoiceApi:
    def __init__(
        self,
        orders: OrderRepository,
        invoices: InvoiceRepository,
        customers: CustomerRepository,
        builder: InvoiceBuilder = DEFAULT_BUILDER,
    ) -> None:
        self._orders = orders
        self._invoices = invoices
        self._customers = customers
        self._builder = builder

    def create_invoice(self, payload: Dict[str, str]) -> Dict[str, object]:
        """POST /invoices — build and persist an invoice for an order."""
        order_id = payload.get("order_id")
        if not order_id:
            raise ValidationError("order_id is required")

        order = self._orders.get(order_id)
        customer = self._customers.get(order.customer_id)

        existing = self._invoices.for_order(order_id)
        if existing is not None:
            return serialize_invoice(existing)

        invoice = self._builder.build(order, customer)
        self._invoices.save(invoice)
        return serialize_invoice(invoice)

    def get_invoice(self, invoice_id: str) -> Dict[str, object]:
        """GET /invoices/{id} — fetch a previously created invoice."""
        invoice = self._invoices.get(invoice_id)
        if invoice is None:  # pragma: no cover - defensive
            raise NotFoundError(f"invoice {invoice_id!r} not found")
        return serialize_invoice(invoice)
