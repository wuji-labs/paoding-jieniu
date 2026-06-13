"""Fixed-point money + tax (肯綮 — the junction the blade must respect).

Money is stored as integer minor units (cents) to avoid float drift. Any
refactor touching invoice/calc must keep this contract; this is why calc needs
golden tests before it is moved.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    cents: int

    def __add__(self, other):
        return Money(self.cents + other.cents)

    def with_tax(self, rate_bps: int):
        # rate in basis points (e.g. 1300 = 13%). Round half-up.
        tax = (self.cents * rate_bps + 5000) // 10000
        return Money(self.cents + tax)
