"""Order API handlers."""

from __future__ import annotations

from typing import Dict, List

from api.serializers import serialize_order
from infra.repository import OrderRepository
from services.order_service import OrderService
from util.errors import ValidationError


class OrderApi:
    def __init__(self, orders: OrderRepository, service: OrderService) -> None:
        self._orders = orders
        self._service = service

    def create_order(self, payload: Dict) -> Dict[str, object]:
        """POST /orders — create an order from a line payload."""
        customer_id = payload.get("customer_id")
        target_currency = payload.get("target_currency")
        raw_lines: List[Dict] = payload.get("lines", [])
        if not customer_id or not target_currency:
            raise ValidationError("customer_id and target_currency are required")

        order = self._service.create_order(
            customer_id=customer_id,
            target_currency=target_currency,
            raw_lines=raw_lines,
            discount_code=payload.get("discount_code"),
        )
        return serialize_order(order)

    def get_order(self, order_id: str) -> Dict[str, object]:
        order = self._service.get_order(order_id)
        return serialize_order(order)
