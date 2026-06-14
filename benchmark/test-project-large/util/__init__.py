"""Low-level utilities shared across the order/payments backend.

These modules carry no domain knowledge; they exist so that pricing, tax,
and invoicing logic can share consistent primitives for money handling,
identifiers, and clock access.
"""
