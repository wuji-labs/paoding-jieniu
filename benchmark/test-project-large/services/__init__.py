"""Service layer: orchestrates domain logic and infra persistence.

Services own transactions and the order/invoice lifecycle. They translate
between the thin API DTOs and the rich domain models, never embedding
business rules of their own (those live in :mod:`domain`).
"""
