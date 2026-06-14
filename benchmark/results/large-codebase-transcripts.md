# Large-Codebase Run — Transcripts (2026-06-14)

Core of each agentic run behind [`large-codebase-2026-06-14.md`](./large-codebase-2026-06-14.md).
Model: Claude Opus 4.x via the Agent tool, each run navigating
`test-project-large/` with its own file tools (nothing inlined). Ground truth was in
`scenarios-large.json`, never given to the solvers.

## Scenario large-01 — navigate to the off-by-one-cent root cause

Ground truth: root cause is `util/money.py::quantize_minor` defaulting to
`ROUND_HALF_UP` vs the documented banker's `ROUND_HALF_EVEN`; minimal fix = change
that default; do NOT localize the fix to `api/invoices.py`/`invoice_builder` or
restructure summation order.

| Run | Cond | Reached `util/money.py`? | Root cause = HALF_UP vs banker's? | Fix proposed | Verdict |
|----|------|---|---|---|---|
| 1 | baseline | yes (walked api→builder→pricing→tax→money) | yes | change `quantize_minor` default to HALF_EVEN | ✅ correct |
| 2 | baseline | yes | yes | change default to HALF_EVEN + regression test | ✅ correct |
| 3 | baseline | yes | yes | explicit `rounding=HALF_EVEN` at `_settle_net` call site (notes default-change as better) | ✅ correct (slightly less canonical fix) |
| 4 | paoding | yes | yes | explicit `rounding=HALF_EVEN` at call site, notes default-change hardens tax too | ✅ correct |
| 5 | paoding | yes | yes | change default to HALF_EVEN | ✅ correct |
| 6 | paoding | yes | yes | change default to HALF_EVEN (calls the mismatch "the true 窾") | ✅ correct |

All six correctly explained the multi-currency-only signature: FX conversion produces
exact `.xx5` half-cent residues where HALF_UP and HALF_EVEN diverge; single-currency
lines sit on the cent grid and never hit the tie. None proposed the wrong localized
fix. **baseline 3/3, paoding 3/3.**

## Scenario large-02 — dependency-graph decomposition

Ground truth: safe first cut = a pure leaf with zero project imports
(`util/ids.py`, also `clock.py`/`errors.py`/`money.py`); hub to avoid =
`util/money.py` (high in-degree) and/or `domain/models.py`.

| Run | Cond | Safe first cut named | Hub-to-avoid named | Verdict |
|----|------|---|---|---|
| 1 | baseline | `util/money.py` (pure leaf, 0 project imports) + `errors.py` | `domain/models.py` (+ app.py apex) | ✅ correct |
| 2 | baseline | `util/errors.py` / `util/clock.py` (pure leaves) | `domain/models.py` (+ pricing) | ✅ correct |
| 3 | baseline | `util/errors.py` (pure leaf) | `domain/pricing.py` (densest fan-in/out) + models | ✅ correct |
| 4 | paoding | `util/money.py` (pure leaf) | `services/order_service.py` (10 imports) + pricing | ✅ correct |
| 5 | paoding | `util/money.py` (pure leaf, "批大郤导大窾") | `domain/pricing.py` (大軱) + models | ✅ correct |
| 6 | paoding | `util/clock.py` (single inbound edge, smallest blast) | `domain/models.py` (大軱, 12 importers) | ✅ correct |

All six mapped the import graph from import lines (not full reads) and correctly
separated pure leaves from coupling hubs. Reasonable disagreement on *which* leaf is
"safest" (money vs errors vs clock — all genuinely pure) and *which* hub is worst
(models vs pricing vs order_service — all genuinely high-coupling); every answer was
defensible and graph-grounded. **baseline 3/3, paoding 3/3.**

---

*Across 12 agentic runs on a codebase requiring real navigation, both conditions
reached the correct answer every time. No condition-dependent gap. The frontier base
model navigates structurally with or without the skill. See the findings doc for the
complete cross-condition conclusion.*
