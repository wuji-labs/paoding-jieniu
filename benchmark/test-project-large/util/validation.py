"""Lightweight, dependency-free input validators.

Used by the service and API layers to reject malformed payloads before they
reach domain logic. Pure functions; raise :class:`util.errors.ValidationError`
on failure and return the cleaned value on success.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Iterable

from util.errors import ValidationError

_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
_SKU_RE = re.compile(r"^SKU-[A-Z0-9]+$")


def require(condition: bool, message: str) -> None:
    """Raise :class:`ValidationError` with ``message`` if ``condition`` is false."""
    if not condition:
        raise ValidationError(message)


def clean_currency(value: str) -> str:
    """Normalize and validate an ISO-4217 alpha code."""
    require(isinstance(value, str), "currency must be a string")
    code = value.strip().upper()
    require(bool(_CURRENCY_RE.match(code)), f"invalid currency code: {value!r}")
    return code


def clean_sku(value: str) -> str:
    """Validate a SKU token."""
    require(isinstance(value, str), "sku must be a string")
    sku = value.strip().upper()
    require(bool(_SKU_RE.match(sku)), f"invalid sku: {value!r}")
    return sku


def clean_quantity(value: object) -> int:
    """Coerce and validate a positive integer quantity."""
    require(isinstance(value, int) and not isinstance(value, bool), "quantity must be an int")
    require(value > 0, "quantity must be positive")  # type: ignore[operator]
    return int(value)  # type: ignore[arg-type]


def clean_decimal(value: object, field: str) -> Decimal:
    """Coerce a string/number into a Decimal, rejecting NaN/inf."""
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"{field} is not a valid number: {value!r}") from exc
    require(dec.is_finite(), f"{field} must be finite")
    return dec


def non_empty(values: Iterable, message: str) -> None:
    """Assert an iterable yields at least one element."""
    for _ in values:
        return
    raise ValidationError(message)
