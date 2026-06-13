# Weak-Model Run — qwen2.5vl:7b (2026-06-14)

> **A real run on a weak local model, blind-judged, honestly reported — including a
> result that is unfavorable to the skill.** No number is fabricated. Raw transcripts
> (`qwen2.5vl-7b_baseline.json`, `qwen2.5vl-7b_paoding.json`), the blinded judge
> input (`_judge-input.json`), the un-blinding key (`_key.json`), and the scores
> (`_scores.json`) are all committed so this is independently checkable.

## Method

- **Model:** `qwen2.5vl:7b` — a small (7B) local model via Ollama. Chosen precisely
  because a frontier model is at ceiling on this subject (see
  [`../pilot-2026-06-14.md`](../pilot-2026-06-14.md)); a weak base has headroom to
  show a skill effect in either direction.
- **Harness:** `run_benchmark.py --model qwen2.5vl-7b --scenario all --runs 3`. For a
  non-agentic chat model the 150-LOC codebase is **inlined** into the prompt (it
  cannot browse files). Baseline = generic system prompt; paoding = full `SKILL.md`
  prepended. **N = 36** (6 scenarios × 2 conditions × 3 runs).
- **Scoring:** a separate **blind** judge (condition hidden, transcripts shuffled)
  scored each against the scenario's hidden ground truth: `correct` (found the true
  root cause / first cut?) and `expected_actions` hit-count.

## Result — the skill did **not** help, and slightly **hurt**

| Condition | correct | expected_actions |
|---|---|---|
| baseline | **18/18 (100%)** | 51/84 (61%) |
| paoding  | **13/18 (72%)**  | 47/84 (56%) |

Correctness by scenario (baseline → paoding):

| #1 | #2 | #3 | #4 | #5 | #6 |
|----|----|----|----|----|----|
| 3/3 → 2/3 | **3/3 → 0/3** | 3/3 → 3/3 | 3/3 → 3/3 | 3/3 → 3/3 | 3/3 → 2/3 |

The drop is concentrated in **#2** (the focused persistence bug). Blind-judge notes
for the failing paoding-#2 runs: *"only adds logging, never identifies ordering",*
*"wrong fix (op-count check), misses ordering",* *"blames clip_payload, wrong root
cause."* Meanwhile every baseline-#2 run went straight at the swallowed
publish-before-commit and nailed it.

## Honest interpretation

1. **Prepending a ~7 KB methodology to a 7B model appears to crowd out its limited
   attention.** On the focused-debugging task the skill induced procedural ceremony
   ("Step 1: read structure, Step 2…") that led the small model *away* from the
   actual bug a bare baseline found immediately. This is a real, if uncomfortable,
   measurement.
2. **This validates the lean-variant instinct.** It is the same point a contributor
   raised on `nopua` (#3) and that `nopua-lite` already acts on: for small models,
   action-items beat philosophy; a heavyweight method-doc is for capable agents.
3. **Scope of the claim (important).** This measures one specific setup: the *whole*
   `SKILL.md` prepended to a *non-agentic* 7B with the codebase *inlined*. That is
   **not** how the skill is actually used — it targets capable agentic runtimes
   navigating real, large codebases that don't fit in context, which is exactly
   where structure-first method should matter and exactly what a 150-LOC inlined
   subject cannot test. So this is **not** "the skill is bad"; it is "the heavyweight
   form does not transfer to a small model, and our small-subject benchmark cannot
   probe the skill's real target (large-codebase navigation)."

## What this honestly leaves open

- **No positive effect has been demonstrated for this skill on any model yet.** On a
  frontier model it is at parity with an at-ceiling baseline; on a weak model it
  slightly hurts. A fair test of the skill's actual value needs a **large codebase
  that does not fit in context** (forcing navigation) and an **agentic** runtime —
  building that subject is the real next step.
- A **`paoding-lite`** (action-items only, no parable/quotes), mirroring
  `nopua-lite`, is the indicated direction for small-model use.

We report exactly what we measured. The result is not what we hoped; it is what the
data says.
