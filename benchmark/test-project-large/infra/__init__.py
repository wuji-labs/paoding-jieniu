"""Infrastructure adapters: in-memory stores and rate sources.

In production these would wrap Postgres / Redis / an FX provider; here they
are deterministic in-memory stubs so the service can run without external
dependencies while preserving the same call surface the domain expects.
"""
