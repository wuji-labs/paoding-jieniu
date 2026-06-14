# Large-Codebase Agentic Run (2026-06-14)

> The decisive test the small benchmark could not run: does the skill help when the
> codebase is **too big to hold in context** and the agent must **navigate** to find
> the answer? Built a 33-file / 1855-LOC backend with a root cause **4 call-hops from
> its symptom** (proven: the one-line fix drops triggering orders 129→0), then ran
> **baseline vs paoding agentically** — each agent navigates with its own file tools,
> nothing inlined. Honest result below. Raw answers in
> [`large-codebase-transcripts.md`](./large-codebase-transcripts.md).

## Why this run exists

The earlier pilot showed a frontier model is at ceiling on a 150-LOC *inlined* subject
(no navigation needed) and that the skill *hurt* a weak model. Neither tested the
skill's actual thesis: **read the structure / walk the call chain in a codebase you
can't see all at once.** This run builds exactly that subject and runs it agentically.

## Subject

- `benchmark/test-project-large/` — 33 files, 1855 LOC, realistic order/payments
  backend (`api/ services/ domain/ infra/ util/`). No `# BUG` labels.
- **Hidden root cause** (scenario large-01): `util/money.py::quantize_minor` defaults
  to `ROUND_HALF_UP` while the documented group standard (and sibling `to_minor`) use
  banker's `ROUND_HALF_EVEN`. Reachable only via `api/invoices.py → invoice_builder →
  pricing → tax → money.py`. The symptom file does **zero** money arithmetic — reading
  it alone cannot find the bug. Ground truth in `scenarios-large.json` (outside the
  subject). Fix proven by `_verify_bug.py` (129 triggering orders → 0).
- Scenario large-02: decomposition — find the safe first cut (pure leaf) vs the
  coupling hub, answerable only by mapping the dependency graph across files.

## Result — N=12 agentic runs (Claude Opus 4.x), no inlining

| Scenario | Condition | Runs | Reached true root cause / correct map | Wrong / localized guess |
|---|---|---|---|---|
| large-01 (navigate to root cause) | baseline | 3 | **3/3** | 0 |
| large-01 | paoding | 3 | **3/3** | 0 |
| large-02 (dependency-graph decomposition) | baseline | 3 | **3/3** | 0 |
| large-02 | paoding | 3 | **3/3** | 0 |

**Every run, both conditions, navigated correctly.** All six large-01 agents walked
the chain to `util/money.py`, identified the HALF_UP-vs-banker's mismatch, and
proposed the rounding-mode fix (none made the wrong localized fix the ground truth
warns against). All six large-02 agents mapped the import graph and named the pure
leaves (`util/ids/clock/errors/money`) as the safe cut and `domain/models`/`pricing`
as the hub to avoid.

**No measurable correctness gap between conditions** — again. Stylistically the
paoding runs narrate the structure explicitly and use the parable's vocabulary
(郤/窾/軱/族); several baseline runs reasoned *more* tersely to the same correct
answer, and one baseline answer was arguably sharper than the ground truth's own
framing (noting a high-fan-in pure leaf is still safe to extract because consumers
merely repoint imports).

## The honest, complete conclusion (across every condition tested)

| Model tier | Subject | Mode | Skill effect vs baseline |
|---|---|---|---|
| Frontier (Opus) | 150 LOC | inlined | **none** — both at ceiling |
| Frontier (Opus) | 1855 LOC | **agentic navigation** | **none** — both navigate correctly |
| Weak (qwen2.5vl:7b) | 150 LOC | inlined | **negative** — skill hurt (72% vs 100%) |

**The heavyweight-methodology-as-prompt does not produce a measurable correctness
lift for a capable agent — even on the large-codebase navigation task it was built
for — because a frontier model already navigates structurally by default. On a weak
model the long prompt hurts.** This is what the data says; we will not dress it up.

### What this does and does not mean

- It does **not** mean the method is wrong — "read the structure, cut the pure seam,
  slow at the knots" is exactly what every winning transcript did. It means a capable
  model has *already internalized* it, so stating it adds no correctness.
- The skill's defensible value is therefore **not** frontier-model correctness. It is:
  consistency/floor-raising across many users and weaker models (in a **lean** form —
  the heavy form backfires on small models), shared vocabulary, and onboarding/teaching.
- The genuinely untested frontier remains: **multi-session, very-large (100k+ LOC)
  real repositories** where even a frontier agent's context truly overflows. Our 1855
  LOC fit a capable agent's working set; a repo that does not might finally separate
  the conditions. Building that is a heavier research subject than a single skill repo
  should carry, and we flag it rather than fake it.

We report exactly what we measured, including that it is unflattering to the skill.
