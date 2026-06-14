"""Payment capture and refund service.

Captures an invoice's grand total through the payment gateway and records the
result on the audit trail. It reads the already-assembled invoice total and
does no money math of its own — it trusts the invoice grand_total_minor that
the builder produced. (Worth noting for the rounding investigation: a payment
captured here will carry whatever the builder computed, correct or not.)

Refunds (full or partial) are also handled here, distributing the refunded
amount across the invoice lines via :func:`util.money.allocate` so that no
cents are created or lost when refunding proportionally.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from domain.models import Invoice
from infra.audit_log import DEFAULT_AUDIT, AuditLog
from infra.payment_gateway import DEFAULT_GATEWAY, CaptureResult, PaymentGateway
from util.errors import ValidationError
from util.money import allocate


@dataclass
class PaymentReceipt:
    invoice_id: str
    charge_id: str
    amount_minor: int
    currency: str


@dataclass
class RefundResult:
    invoice_id: str
    refund_id: str
    amount_minor: int
    per_line_minor: List[int]


class PaymentService:
    def __init__(
        self,
        gateway: PaymentGateway = DEFAULT_GATEWAY,
        audit: AuditLog = DEFAULT_AUDIT,
    ) -> None:
        self._gateway = gateway
        self._audit = audit

    def capture_invoice(self, invoice: Invoice) -> PaymentReceipt:
        result: CaptureResult = self._gateway.capture(
            invoice.grand_total_minor, invoice.currency
        )
        self._audit.record(
            "payment.captured",
            invoice.id,
            charge_id=result.charge_id,
            amount_minor=result.amount_minor,
            currency=result.currency,
        )
        return PaymentReceipt(
            invoice_id=invoice.id,
            charge_id=result.charge_id,
            amount_minor=result.amount_minor,
            currency=result.currency,
        )

    def refund_full(self, invoice: Invoice, charge_id: str) -> RefundResult:
        return self._refund(invoice, charge_id, invoice.grand_total_minor)

    def refund_amount(self, invoice: Invoice, charge_id: str, amount_minor: int) -> RefundResult:
        if amount_minor <= 0 or amount_minor > invoice.grand_total_minor:
            raise ValidationError("refund amount out of range")
        return self._refund(invoice, charge_id, amount_minor)

    def _refund(self, invoice: Invoice, charge_id: str, amount_minor: int) -> RefundResult:
        weights = [line.gross_minor for line in invoice.lines] or [1]
        per_line = allocate(amount_minor, weights)
        result = self._gateway.refund(charge_id, amount_minor)
        self._audit.record(
            "payment.refunded",
            invoice.id,
            refund_id=result.charge_id,
            amount_minor=amount_minor,
        )
        return RefundResult(
            invoice_id=invoice.id,
            refund_id=result.charge_id,
            amount_minor=amount_minor,
            per_line_minor=per_line,
        )


DEFAULT_PAYMENTS = PaymentService()
