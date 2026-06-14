"""Typed exceptions shared across layers."""

from __future__ import annotations


class BackendError(Exception):
    """Base for all application-level errors."""


class NotFoundError(BackendError):
    """A referenced entity does not exist in its store."""


class ValidationError(BackendError):
    """Inbound payload failed validation before reaching domain logic."""


class CurrencyError(BackendError):
    """Currency conversion could not be performed (missing rate, etc.)."""


class InventoryError(BackendError):
    """Inventory could not satisfy a reservation."""
