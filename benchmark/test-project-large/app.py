"""Composition root: wires repositories, services, and API handlers.

Run ``python app.py`` for a tiny smoke demo that creates an order and an
invoice and prints the serialized invoice. Uses only in-memory stores, so it
needs no external services.
"""

from __future__ import annotations

import json

from api.invoices import InvoiceApi
from api.orders import OrderApi
from api.payments import PaymentApi
from domain.models import Customer
from infra.repository import CustomerRepository, InvoiceRepository, OrderRepository
from services.customer_service import CustomerService
from services.order_service import OrderService
from services.reporting_service import ReportingService


class Application:
    def __init__(self) -> None:
        self.orders = OrderRepository()
        self.invoices = InvoiceRepository()
        self.customers = CustomerRepository()

        self.customer_service = CustomerService(self.customers)
        self.order_service = OrderService(self.orders)
        self.reporting = ReportingService(self.invoices)

        self.order_api = OrderApi(self.orders, self.order_service)
        self.invoice_api = InvoiceApi(self.orders, self.invoices, self.customers)
        self.payment_api = PaymentApi(self.invoices)

    def seed_customer(self, customer: Customer) -> None:
        self.customers.save(customer)


def _demo() -> None:
    app = Application()
    app.seed_customer(Customer(id="cust_1", name="Acme GmbH", country="DE"))

    order = app.order_api.create_order(
        {
            "customer_id": "cust_1",
            "target_currency": "USD",
            "lines": [
                {"sku": "SKU-GADGET", "quantity": 3},   # EUR -> USD
                {"sku": "SKU-GIZMO", "quantity": 7},     # GBP -> USD, reduced tax
                {"sku": "SKU-DOODAD", "quantity": 1},    # CNY -> USD
            ],
            "discount_code": "BLACKFRIDAY",
        }
    )
    invoice = app.invoice_api.create_invoice({"order_id": order["id"]})
    print(json.dumps(invoice, indent=2))

    receipt = app.payment_api.capture({"invoice_id": invoice["id"]})
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    _demo()
