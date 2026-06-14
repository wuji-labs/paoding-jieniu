"""Payment and refund API handlers.

Thin handlers over :mod:`services.payment_service` and
:mod:`services.refund_service`. They look up the invoice, delegate, and
serialize the receipt. No arithmetic happens here.
"""

from __future__ import annotations

from typing import Dict

from infra.repository import InvoiceRepository
from services.payment_service import DEFAULT_PAYMENTS, PaymentService
from util.errors import NotFoundError, ValidationError


class PaymentApi:
    def __init__(
        self,
        invoices: InvoiceRepository,
        payments: PaymentService = DEFAULT_PAYMENTS,
    ) -> None:
        self._invoices = invoices
        self._payments = payments

    def capture(self, payload: Dict[str, str]) -> Dict[str, object]:
        """POST /payments — capture an invoice's grand total."""
        invoice_id = payload.get("invoice_id")
        if not invoice_id:
            raise ValidationError("invoice_id is required")
        invoice = self._invoices.get(invoice_id)
        receipt = self._payments.capture_invoice(invoice)
        return {
            "invoice_id": receipt.invoice_id,
            "charge_id": receipt.charge_id,
            "amount_minor": receipt.amount_minor,
            "currency": receipt.currency,
        }

    def refund(self, payload: Dict[str, object]) -> Dict[str, object]:
        """POST /refunds — full or partial refund against a prior charge."""
        invoice_id = payload.get("invoice_id")
        charge_id = payload.get("charge_id")
        if not invoice_id or not charge_id:
            raise ValidationError("invoice_id and charge_id are required")
        invoice = self._invoices.get(invoice_id)  # type: ignore[arg-type]
        amount = payload.get("amount_minor")
        if amount is None:
            result = self._payments.refund_full(invoice, str(charge_id))
        else:
            result = self._payments.refund_amount(invoice, str(charge_id), int(amount))  # type: ignore[arg-type]
        return {
            "invoice_id": result.invoice_id,
            "refund_id": result.refund_id,
            "amount_minor": result.amount_minor,
            "per_line_minor": result.per_line_minor,
        }
