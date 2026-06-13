"""Invoice line/tax calculation. Depends on core.money (肯綮).

Half-pure: no I/O, but couples to the Money contract. Must be moved AFTER
golden tests pin its numeric behavior.
"""
from ..core.money import Money


def line_total(items, tax_rate_bps: int) -> Money:
    subtotal = Money(0)
    for item in items:
        subtotal = subtotal + Money(item["cents"] * item.get("qty", 1))
    return subtotal.with_tax(tax_rate_bps)
