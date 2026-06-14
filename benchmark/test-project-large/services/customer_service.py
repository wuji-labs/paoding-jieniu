"""Customer onboarding and lookup service.

Validates and persists customers, and exposes a few read helpers the API
layer needs. Pure orchestration over the customer repository and validators;
no money math.
"""

from __future__ import annotations

from typing import List

from domain.models import Customer
from infra.audit_log import DEFAULT_AUDIT, AuditLog
from infra.repository import CustomerRepository
from util.errors import ValidationError
from util.ids import next_id
from util.validation import require


# ISO-3166 alpha-2 codes the backend recognizes for tax purposes.
_KNOWN_COUNTRIES = {"US", "DE", "GB", "CN", "JP", "FR", "NL"}


class CustomerService:
    def __init__(
        self,
        customers: CustomerRepository,
        audit: AuditLog = DEFAULT_AUDIT,
    ) -> None:
        self._customers = customers
        self._audit = audit

    def _clean_country(self, value: str) -> str:
        require(isinstance(value, str), "country must be a string")
        code = value.strip().upper()
        require(len(code) == 2, f"country must be a 2-letter code: {value!r}")
        if code not in _KNOWN_COUNTRIES:
            raise ValidationError(f"unsupported country: {code}")
        return code

    def onboard(self, name: str, country: str, tax_exempt: bool = False) -> Customer:
        require(bool(name and name.strip()), "customer name is required")
        country_code = self._clean_country(country)
        customer = Customer(
            id=next_id("cust"),
            name=name.strip(),
            country=country_code,
            tax_exempt=tax_exempt,
        )
        self._customers.save(customer)
        self._audit.record(
            "customer.onboarded",
            customer.id,
            country=country_code,
            tax_exempt=tax_exempt,
        )
        return customer

    def get(self, customer_id: str) -> Customer:
        return self._customers.get(customer_id)

    def in_country(self, country: str) -> List[Customer]:
        return self._customers.by_country(self._clean_country(country))

    def set_tax_exempt(self, customer_id: str, exempt: bool) -> Customer:
        customer = self._customers.get(customer_id)
        customer.tax_exempt = exempt
        self._customers.save(customer)
        self._audit.record("customer.tax_exempt_changed", customer_id, exempt=exempt)
        return customer
