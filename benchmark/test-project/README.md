# test-project · `tangled-orders`

A deliberately tangled, small (~600 LOC) order/billing service used as the **real subject** for the PaoDing JieNiu benchmark. Every benchmark scenario in `../scenarios.json` points at a real file/path below, so results are reproducible rather than imaginary.

This is not a clean codebase. It is intentionally seeded with structural pathologies (a god-object, a swallowed error on a transaction boundary, byte-vs-char bugs, mixed domains in one table) so the benchmark can measure whether an agent **reads the grain before cutting** vs. **hacks the most-coupled core first**.

## Layout

```
tangled-orders/
├── core/
│   ├── service.py        # OrderBillingService — god object, everything depends on it (軱)
│   └── money.py          # fixed-point money + tax (肯綮)
├── invoice/
│   ├── render.py         # pure: data -> html (窾, clean seam)
│   └── calc.py           # invoice line/tax calc (depends on money)
├── reconcile.py          # double-write to ledger + refund (軱/族, hard knot)
├── api.py                # createOrder endpoint; swallows publish error (the bug)
└── events.py             # in-memory event bus
```

## Known seeded issues (ground truth — NOT shown to the agent)

See `../scenarios.json` `description` fields. Summary:
- `api.py`: `publish_event` runs before commit and its failure is caught and dropped → 200 but no order persisted.
- `reconcile.py`: god-object coupling; refund + ledger double-write share no transaction.
- `invoice/render.py` is the only clean seam (pure function) — the correct first cut.
- `core/service.py` mixes orders, points, coupons in one class.
- `events.py` truncates payloads by byte length on multibyte text.

> These are planted for evaluation. Do not "fix" this directory; it is the test fixture.
