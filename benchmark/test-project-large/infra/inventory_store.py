"""In-memory stock ledger backing inventory reservations."""

from __future__ import annotations

from typing import Dict

from util.errors import InventoryError


class StockLedger:
    """Tracks on-hand and reserved quantities per SKU."""

    def __init__(self, initial: Dict[str, int] | None = None) -> None:
        self._on_hand: Dict[str, int] = dict(initial or {})
        self._reserved: Dict[str, int] = {}

    def available(self, sku: str) -> int:
        return self._on_hand.get(sku, 0) - self._reserved.get(sku, 0)

    def reserve(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise InventoryError(f"non-positive reservation for {sku}")
        if self.available(sku) < qty:
            raise InventoryError(
                f"insufficient stock for {sku}: need {qty}, have {self.available(sku)}"
            )
        self._reserved[sku] = self._reserved.get(sku, 0) + qty

    def release(self, sku: str, qty: int) -> None:
        self._reserved[sku] = max(0, self._reserved.get(sku, 0) - qty)

    def seed(self, sku: str, qty: int) -> None:
        self._on_hand[sku] = self._on_hand.get(sku, 0) + qty


DEFAULT_LEDGER = StockLedger(
    {
        "SKU-WIDGET": 1000,
        "SKU-GADGET": 1000,
        "SKU-GIZMO": 1000,
        "SKU-DOODAD": 1000,
        "SKU-SPROCKET": 1000,
        "SKU-FLANGE": 1000,
        "SKU-COG": 1000,
    }
)
