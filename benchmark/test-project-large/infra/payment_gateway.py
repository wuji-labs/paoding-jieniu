"""Stubbed payment gateway adapter.

Simulates an external PSP (Stripe/Adyen-style) with deterministic behavior:
captures succeed unless the amount ends in a sentinel value, so tests can
exercise the decline path. No real network calls. Amounts are integer minor
units; the gateway is currency-agnostic and trusts the caller's settlement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from util.errors import BackendError
from util.ids import next_id


class PaymentDeclined(BackendError):
    """The gateway refused to capture the charge."""


@dataclass
class CaptureResult:
    charge_id: str
    amount_minor: int
    currency: str
    status: str


class PaymentGateway:
    def __init__(self) -> None:
        self._charges: Dict[str, CaptureResult] = {}

    def capture(self, amount_minor: int, currency: str) -> CaptureResult:
        if amount_minor <= 0:
            raise PaymentDeclined("non-positive capture amount")
        # Sentinel decline: amounts ending in 13 minor units are refused.
        if amount_minor % 100 == 13:
            raise PaymentDeclined(f"declined: {amount_minor} {currency}")
        result = CaptureResult(
            charge_id=next_id("ch"),
            amount_minor=amount_minor,
            currency=currency.upper(),
            status="captured",
        )
        self._charges[result.charge_id] = result
        return result

    def refund(self, charge_id: str, amount_minor: int) -> CaptureResult:
        charge = self._charges.get(charge_id)
        if charge is None:
            raise BackendError(f"unknown charge: {charge_id!r}")
        if amount_minor <= 0 or amount_minor > charge.amount_minor:
            raise BackendError("invalid refund amount")
        refunded = CaptureResult(
            charge_id=next_id("rf"),
            amount_minor=amount_minor,
            currency=charge.currency,
            status="refunded",
        )
        self._charges[refunded.charge_id] = refunded
        return refunded


DEFAULT_GATEWAY = PaymentGateway()
