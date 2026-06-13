# Raw Transcripts — Pilot Run 2026-06-14

Verbatim agent answers behind [`pilot-2026-06-14.md`](./pilot-2026-06-14.md).
Condition labels are shown (this file is the un-blinded record). Model: Claude
Opus 4.x via agent harness. Ground truth was withheld from every solver.

---

## Scenario #1 — Extract Invoice Generation From God Object (decomposition)

`expected_actions`: read dependency graph before editing · identify
`invoice/render.py` as the pure low-coupling first cut · flag `core/service.py` as
the high-coupling core to avoid · add golden tests around `invoice/calc.py` +
`core/money.py` before moving them · propose small reversible commit sequence.

### #1 · baseline · run 1
First cut: `invoice/render.py` — the pure seam (窾): `render_invoice(data) -> str`,
no I/O, no `core.service` import, no `Money` coupling. NOT to touch first:
`core/service.py` (god object 軱, imported by api.py + reconcile.py), `core/money.py`
(肯綮 contract), `invoice/calc.py` (move only after golden tests), `reconcile.py`/
`events.py` (seeded defects, out of scope). Tests before moving: characterization
test on `render_invoice` (empty items, missing id, multi-item); golden numeric
tests on Money/line_total (round-half-up). Commits: (1) characterize render, (2)
golden Money tests, (3) make invoice package public API, (4) move line_total keep
core.money import, (5) verify billing no longer imports invoice internals. Then
re-scope: service split + seeded bugs are separate tickets.

### #1 · baseline · run 2
First cut: `invoice/render.py` — true 窾: pure `data dict -> html str`, zero I/O,
zero dependency on `OrderBillingService`, no Money coupling. Extract verbatim into
standalone package, no behavior change. Do NOT touch: `core/service.py` (god
object/軱), `core/money.py` (肯綮, integer cents round-half-up), `invoice/calc.py`
(moves after render, couples to Money), `reconcile.py`/`events.py` (real seeded
defects — non-atomic ledger/refund, byte-vs-char clip — out of scope, one concern
per commit). Tests: characterization on render_invoice; golden numeric on
line_total/Money.with_tax (half-up at odd cents). Commits: characterize render →
golden calc/Money → create package move render → move calc keep core.money import →
define public __init__. "Sequence respects grain: isolate the pure leaf, pin the
half-pure dependent with golden tests, never cut the god object or money contract
in the same pass."

### #1 · baseline · run 3
First cut: extract `invoice/render.py` into a standalone dependency-free module.
The one true clean seam — pure, nothing ties it to billing. NOT first:
`core/service.py` (god object mixing orders/points/coupons — hard bone),
`invoice/calc.py` (half-pure, coupled to `core.money.Money`; defer until golden
tests pin output), `core/money.py` (fixed-point junction — depend via stable
import, don't copy), `api.py`/`reconcile.py`/`events.py` (latent bugs:
publish-before-commit swallow, non-atomic ledger+refund, byte-slicing UTF-8 — leave
them). Tests before move: characterization on render_invoice; golden on line_total
(1300 bps, qty>1, half-up boundary). Commits: characterize+golden (no source
change) → extract render to invoicing with back-compat shim → (later PR) move calc
→ (later) split OrderBillingService. Each commit independently revertible.

### #1 · paoding · run 1
First cut: `invoice/render.py` → standalone module. Only true seam (窾): pure
`dict -> str`, zero imports, no dependency on god object or Money. NOT yet (in order
of stay-away): (1) `core/service.py` god object 軱 — everything imports it, tangles
three domains; (2) `core/money.py` contract 肯綮 — integer cents round-half-up,
touching rounding silently breaks totals; (3) `invoice/calc.py` half-pure, coupled
to Money, move after render once golden tests pin arithmetic; (4) `reconcile.py`/
`events.py` seeded bugs, separate change. Tests: characterization on render_invoice;
golden on line_total/Money.with_tax (13% odd cents, +5000//10000). Commits:
characterize render → extract to invoicing + shim → golden tests → move calc keep
core.money → repoint callers, remove shims. "Only after invoicing stands alone do I
consider carving OrderBillingService along domain grain — separate, slowed-down,
tested."

### #1 · paoding · run 2
First cut: `invoice/render.py` standalone (窾): pure, no `core.service`, no Money.
"游刃有余 — instant reversibility." NOT first: `core/service.py` god object 軱
(ripples through api.py + reconcile.py), `invoice/calc.py` (couples to
`core.money.Money` 肯綮; move only after golden tests pin `with_tax` round-half-up),
`core/money.py` (shared invariant, don't relocate), seeded defects (api publish-
before-commit, events byte-slice, reconcile non-atomic) — flag and leave. Tests:
golden on render_invoice (fixed dict → exact HTML); golden numeric on
line_total/Money.with_tax (1300 bps, odd cents, integer-only). Commits: golden
tests lock behavior → create invoicing package move render + re-export shim → move
line_total keep core.money → define public API point callers → remove shims. "Each
commit keeps tests green and is independently revertible. The god object and three
seeded bugs explicitly deferred."

### #1 · paoding · run 3
First cut: extract `invoice/render.py` behind a stable `data dict -> str` contract —
true seam 郤/窾, pure, no I/O, no `OrderBillingService`, no Money. "薄刃入有间 —
isolate the part that already wants to be free before touching anything entangled."
NOT first: `core/service.py` god object 軱 (three domains, everything imports it,
split along domain grain later); `core/money.py` + `invoice/calc.py` load-bearing
junction 肯綮 (calc couples to integer-cents Money; moving without golden tests risks
silent rounding drift — slow down); `reconcile.py`/`events.py` non-atomic writes +
byte-vs-char clip (real but orthogonal — flag, file, defer). Tests: characterization
on render_invoice (typical/empty/missing-id); golden on line_total/Money.with_tax
(half-up, multi-item, qty default). Commits: characterize + golden (no prod change)
→ define invoice public API → make render standalone → (later PR) move calc with
Money injected → (later) split service; fix reconcile/events defects. "Circle them,
don't carve them."

---

## Scenario #2 — 200 OK But Order Not Persisted (debugging)

`expected_actions`: walk the call chain instead of editing the createOrder trunk ·
identify the swallowed exception (bare except/pass) around publish · notice publish
runs before commit · propose moving publish after commit or using an outbox · add
observability/regression test rather than blind retries.

### #2 · baseline · run 1
Root cause: ordering of `EVENT_BUS.publish` relative to `svc.commit(tx)` in api.py +
swallowed exception, with lazy-commit in service.py (`insert_order` only queues a
closure into `tx["ops"]`; real write in `commit`). publish sits between queued
insert and commit, wrapped in `try/except: pass`; flaky bus raises RuntimeError,
swallowed. 200 returned regardless of whether the row exists. Fix: move publish
after a successful commit and stop swallowing silently — `svc.commit(tx)` first,
then `try: EVENT_BUS.publish(...) except Exception: log.warning(..., exc_info=True)`.
Notes clip_payload byte-slice is a separate defect.

### #2 · baseline · run 2
Root cause: api.py create_order orders steps wrong. insert_order only queues a
closure (service.py:28-29); commit runs the queued ops and persists
(service.py:19-21). publish is before commit, wrapped in bare `except: pass`; flaky
bus (events.py:13-15) → control into except → pass. "Inverts the unit of work — the
side-effect is treated as part of the trunk and its failure neither aborts nor
logs." Fix: commit first (the unit of work), then best-effort publish after durable
write, replace pass with `logger.exception`. Don't touch OrderBillingService or
clip_payload — separate concerns.

### #2 · baseline · run 3
Root cause: `api.py:18-23`. insert_order only queues; commit replays ops. When
publish raises (flaky bus, or `clip_payload` UnicodeDecodeError on multibyte), bare
`except Exception: pass` swallows and "control never reaches `svc.commit(tx)`" →
falls through to return 200 → HTTP 200, no row, no log. "The three prior edits
failed because they patched the trunk rather than the publish-before-commit
ordering." Fix: move `svc.commit(tx)` above publish (one-line move), event
best-effort post-commit. clip_payload is a real secondary defect but order
correctness doesn't depend on it.

### #2 · paoding · run 1
Root cause: api.py lines 17-23. Two-phase: insert_order queues (service.py:28-29),
commit applies (19-21). publish before commit, in `try/except Exception: pass`; flaky
bus (events.py:14-15) → swallowed. "The publish call sits between the queued insert
and the commit, and its failure is swallowed with no log." HTTP 200 unconditional.
Fix: commit first, publish after durable write, let failures surface/log:
`svc.commit(tx)` then publish. clip_payload byte-vs-char + god object + non-atomic
reconcile are separate — don't touch for this fix.

### #2 · paoding · run 2
Root cause: api.py:14-24. "Walks `begin_tx → validate_and_build → insert_order →
publish(event) → commit`. Ops are deferred lambdas; nothing persists until commit."
publish before commit + `try/except: pass`; flaky bus raises → except → commit
skipped → queued insert never fires → no row, no log, still returns 200. "The three
prior edits failed because they hacked the trunk instead of fixing the
publish-before-commit ordering — the actual 窾." Fix: commit before publish so
persistence can't be skipped; `log.exception` instead of silent pass. clip_payload
separate.

### #2 · paoding · run 3
Root cause: `api.py:17-23` ordering + swallow across the transaction boundary.
insert_order appends a lambda to `tx["ops"]`; real persist in commit. publish before
commit, swallowed; flaky bus (events.py:14-15) → commit skipped → no row, no log,
200 returned. "Patched the trunk (more try/except) instead of fixing
publish-before-commit." Fix: commit before publish (load-bearing one-line move),
log instead of silent pass. clip_payload byte-slice is a real but separate defect.

---

*All twelve runs identified the correct first cut (#1) and root cause (#2). No
condition-dependent gap was observed; the frontier base model is at ceiling on this
150-LOC subject. See [`pilot-2026-06-14.md`](./pilot-2026-06-14.md) for
interpretation and next steps.*
