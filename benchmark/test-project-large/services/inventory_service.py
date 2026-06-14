"""Inventory reservation service over the stock ledger."""

from __future__ import annotations

from typing import List

from domain.models import Order
from infra.inventory_store import DEFAULT_LEDGER, StockLedger
from util.errors import InventoryError


class InventoryService:
    def __init__(self, ledger: StockLedger = DEFAULT_LEDGER) -> None:
        self._ledger = ledger

    def reserve_order(self, order: Order) -> List[str]:
        """Reserve stock for every line; roll back on any failure."""
        reserved: List[tuple[str, int]] = []
        try:
            for line in order.lines:
                self._ledger.reserve(line.sku, line.quantity)
                reserved.append((line.sku, line.quantity))
        except InventoryError:
            for sku, qty in reserved:
                self._ledger.release(sku, qty)
            raise
        return [sku for sku, _ in reserved]

    def availability(self, sku: str) -> int:
        return self._ledger.available(sku)


DEFAULT_INVENTORY = InventoryService()
