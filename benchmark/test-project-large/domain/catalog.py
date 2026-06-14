"""Product catalog: SKU -> price/currency/tax-category lookups."""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, List

from domain.models import CatalogItem
from util.errors import NotFoundError

# Catalog prices are quoted in the item's *native* currency. Orders can settle
# into any supported currency; conversion happens in :mod:`domain.pricing`.
_CATALOG: Dict[str, CatalogItem] = {
    "SKU-WIDGET": CatalogItem("SKU-WIDGET", "Widget", Decimal("19.99"), "USD"),
    "SKU-GADGET": CatalogItem("SKU-GADGET", "Gadget", Decimal("14.50"), "EUR"),
    "SKU-GIZMO": CatalogItem("SKU-GIZMO", "Gizmo", Decimal("9.95"), "GBP", "reduced"),
    "SKU-DOODAD": CatalogItem("SKU-DOODAD", "Doodad", Decimal("120.00"), "CNY"),
    "SKU-SPROCKET": CatalogItem("SKU-SPROCKET", "Sprocket", Decimal("4.20"), "USD"),
    "SKU-FLANGE": CatalogItem("SKU-FLANGE", "Flange", Decimal("33.33"), "EUR", "reduced"),
    "SKU-COG": CatalogItem("SKU-COG", "Cog", Decimal("7.77"), "GBP"),
}


class Catalog:
    """Read-only catalog access with simple lookups and search."""

    def get(self, sku: str) -> CatalogItem:
        try:
            return _CATALOG[sku]
        except KeyError as exc:
            raise NotFoundError(f"unknown sku: {sku!r}") from exc

    def exists(self, sku: str) -> bool:
        return sku in _CATALOG

    def all(self) -> List[CatalogItem]:
        return list(_CATALOG.values())

    def by_currency(self, currency: str) -> List[CatalogItem]:
        """Items natively priced in ``currency``."""
        code = currency.upper()
        return [item for item in _CATALOG.values() if item.currency == code]

    def search(self, term: str) -> List[CatalogItem]:
        """Case-insensitive substring match on item name."""
        needle = term.lower()
        return [item for item in _CATALOG.values() if needle in item.name.lower()]


DEFAULT_CATALOG = Catalog()
