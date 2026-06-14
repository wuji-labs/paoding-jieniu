"""In-memory repositories for orders, invoices, and customers.

Each repository is a thin dict-backed store. They are deliberately dumb:
no business rules live here. Domain and service layers do all reasoning and
hand finished aggregates to these stores for persistence.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from domain.models import Customer, Invoice, Order
from util.errors import NotFoundError


class _BaseRepo:
    def __init__(self) -> None:
        self._items: Dict[str, object] = {}

    def _get(self, key: str):
        try:
            return self._items[key]
        except KeyError as exc:
            raise NotFoundError(f"{type(self).__name__}: {key!r} not found") from exc

    def _put(self, key: str, value: object) -> None:
        self._items[key] = value

    def __len__(self) -> int:
        return len(self._items)


class OrderRepository(_BaseRepo):
    def save(self, order: Order) -> Order:
        self._put(order.id, order)
        return order

    def get(self, order_id: str) -> Order:
        return self._get(order_id)  # type: ignore[return-value]

    def all(self) -> List[Order]:
        return list(self._items.values())  # type: ignore[return-value]

    def for_customer(self, customer_id: str) -> List[Order]:
        return [
            o for o in self._items.values()  # type: ignore[union-attr]
            if o.customer_id == customer_id  # type: ignore[attr-defined]
        ]

    def exists(self, order_id: str) -> bool:
        return order_id in self._items


class InvoiceRepository(_BaseRepo):
    def save(self, invoice: Invoice) -> Invoice:
        self._put(invoice.id, invoice)
        return invoice

    def get(self, invoice_id: str) -> Invoice:
        return self._get(invoice_id)  # type: ignore[return-value]

    def all(self) -> List[Invoice]:
        return list(self._items.values())  # type: ignore[return-value]

    def for_order(self, order_id: str) -> Optional[Invoice]:
        for inv in self._items.values():  # type: ignore[assignment]
            if inv.order_id == order_id:  # type: ignore[attr-defined]
                return inv  # type: ignore[return-value]
        return None

    def for_customer(self, customer_id: str) -> List[Invoice]:
        return [
            inv for inv in self._items.values()  # type: ignore[union-attr]
            if inv.customer_id == customer_id  # type: ignore[attr-defined]
        ]

    def total_billed(self, customer_id: str) -> int:
        """Sum of grand totals across a customer's invoices (minor units)."""
        return sum(inv.grand_total_minor for inv in self.for_customer(customer_id))


class CustomerRepository(_BaseRepo):
    def save(self, customer: Customer) -> Customer:
        self._put(customer.id, customer)
        return customer

    def get(self, customer_id: str) -> Customer:
        return self._get(customer_id)  # type: ignore[return-value]

    def by_country(self, country: str) -> List[Customer]:
        code = country.upper()
        return [
            c for c in self._items.values()  # type: ignore[union-attr]
            if c.country.upper() == code  # type: ignore[attr-defined]
        ]
