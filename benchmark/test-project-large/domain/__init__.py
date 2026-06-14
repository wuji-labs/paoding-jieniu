"""Domain layer: pure business logic over plain data models.

Modules here depend on :mod:`util` and :mod:`infra` interfaces but never on
:mod:`api` or :mod:`services`. Pricing, tax, discounts, and currency
conversion all live here and are composed by the service layer.
"""
