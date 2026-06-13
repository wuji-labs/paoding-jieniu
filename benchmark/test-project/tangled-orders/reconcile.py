"""Reconciliation: double-write to ledger + refund (軱/族 — hard, tangled knot).

Seeded issue: ledger write and refund are two separate, non-atomic writes with
no shared transaction or compensation. If refund_gateway fails after the ledger
entry, the books and the gateway diverge. A structure-first agent should flag
this as the hard bone to slow down at (add tests, define consistency semantics)
rather than something to casually edit.
"""
from .core.service import OrderBillingService

svc = OrderBillingService()


def reconcile_refund(order_id, amount_cents, ledger, refund_gateway):
    # Write 1: ledger
    ledger.append({"order": order_id, "delta": -amount_cents})
    # Write 2: external gateway — NOT in the same transaction as write 1.
    refund_gateway.refund(order_id, amount_cents)
    # No compensation if the second write fails after the first succeeds.
    return True
