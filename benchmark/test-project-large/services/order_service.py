"""Order lifecycle service.

Turns inbound line requests into a persisted :class:`Order`, snapshotting
catalog prices at creation time and reserving inventory. Pricing/invoicing
are handled separately by :mod:`services.invoice_builder`.
"""

from __future__ import annotations

from typing import Iterable, List, Mapping

from domain.catalog import DEFAULT_CATALOG, Catalog
from domain.fees import FeeBreakdown, compute_fees
from domain.models import Order, OrderLine
from domain.pricing import DEFAULT_PRICING, PricingEngine
from infra.audit_log import DEFAULT_AUDIT, AuditLog
from infra.repository import OrderRepository
from services.inventory_service import DEFAULT_INVENTORY, InventoryService
from util.errors import ValidationError
from util.ids import next_id
from util.validation import clean_currency, clean_quantity, clean_sku, require


class OrderService:
    def __init__(
        self,
        orders: OrderRepository,
        catalog: Catalog = DEFAULT_CATALOG,
        inventory: InventoryService = DEFAULT_INVENTORY,
        audit: AuditLog = DEFAULT_AUDIT,
        pricing: PricingEngine = DEFAULT_PRICING,
    ) -> None:
        self._orders = orders
        self._catalog = catalog
        self._inventory = inventory
        self._audit = audit
        self._pricing = pricing

    def _build_line(self, raw: Mapping) -> OrderLine:
        sku = clean_sku(raw.get("sku", ""))
        qty = clean_quantity(raw.get("quantity"))
        require(self._catalog.exists(sku), f"unknown sku: {sku!r}")
        item = self._catalog.get(sku)
        return OrderLine(
            sku=sku,
            quantity=qty,
            unit_price=item.unit_price,
            currency=item.currency,
            tax_category=item.tax_category,
        )

    def create_order(
        self,
        customer_id: str,
        target_currency: str,
        raw_lines: Iterable[Mapping],
        discount_code: str | None = None,
    ) -> Order:
        currency = clean_currency(target_currency)
        lines: List[OrderLine] = [self._build_line(r) for r in raw_lines]
        if not lines:
            raise ValidationError("order has no lines")
        order = Order(
            id=next_id("ord"),
            customer_id=customer_id,
            target_currency=currency,
            lines=lines,
            discount_code=discount_code,
        )
        self._inventory.reserve_order(order)
        self._orders.save(order)
        self._audit.record(
            "order.created",
            order.id,
            customer_id=customer_id,
            currency=currency,
            line_count=len(lines),
        )
        return order

    def get_order(self, order_id: str) -> Order:
        return self._orders.get(order_id)

    def list_orders(self) -> List[Order]:
        return self._orders.all()

    def line_count(self, order_id: str) -> int:
        return len(self.get_order(order_id).lines)

    def estimate_fees(self, order_id: str, customer, zone: str = "regional") -> FeeBreakdown:
        """Preview shipping/handling fees for an order.

        Fees are computed off the priced line grosses but are NOT folded into
        the invoice grand total; they are a separate quote surfaced to the
        client at checkout.
        """
        order = self.get_order(order_id)
        priced = self._pricing.price_order(order, customer)
        grosses = [line.gross_minor for line in priced]
        return compute_fees(grosses, order.target_currency, zone)
