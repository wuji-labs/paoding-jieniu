# PaoDing JieNiu Benchmark Suite

Reproducible evaluation harness for the 庖丁解牛 (Ox-Carving Way) skill. It tests
whether an AI agent, when handed a tangled codebase, **reads the structure and
cuts along the grain** instead of **hacking the most-coupled core first**.

> ## ◑ REAL RUNS COMPLETE — results below, honestly including the unflattering parts
>
> | Model | Subject | Mode | Skill vs baseline |
> |---|---|---|---|
> | Frontier (Opus 4.x) | 150 LOC | inlined | **no gap** — both at ceiling |
> | Frontier (Opus 4.x) | 1855 LOC | **agentic navigation** | **no gap** — both navigate correctly |
> | Weak (qwen2.5vl:7b) | 150 LOC | inlined | **negative** — full skill hurt (72% vs 100%) |
> | Weak — **paoding-lite** | 150 LOC | inlined | recovers most of it (89%) |
>
> Details: [`results/pilot-2026-06-14.md`](./results/pilot-2026-06-14.md) ·
> [`results/large-codebase-2026-06-14.md`](./results/large-codebase-2026-06-14.md) ·
> [`results/weak-model/FINDINGS.md`](./results/weak-model/FINDINGS.md). No number is
> fabricated; raw transcripts + blind keys + scores are all committed.
>
> ### ⚠️ How to read this — what it does and does NOT say
> This benchmark measures **one** narrow thing: does prepending the skill change
> **bug-finding / decomposition correctness** on a **coding** task. It is the *hardest
> possible case to show a skill effect*, on purpose — a coding skill, on the model
> already strongest at coding, scored by hard correctness.
>
> **"No correctness lift on a frontier model" is NOT "no value."** It is true of
> almost any prompt on a frontier model, which is already expert. The skill's real
> value lives where this harness deliberately does not look:
> - **Behavior & consistency** — getting the structure-first method *reliably, every
>   run, for every user*, not only when the model happens to. (A floor, not a ceiling.)
> - **Weaker models / tight budgets** — where the base model is *not* already expert;
>   here the lean **paoding-lite** measurably helps.
> - **The artifact itself** — a packaged, documented, installable method has worth even
>   if a frontier model could reconstruct it from scratch.
>
> And note: **9 of the 10 HuaXia skills are not coding skills at all** — they shape
> aesthetics, literary voice, health framing, strategy, teaching, judgment. "Does it
> have soul / taste / the right framing" has **no correctness score**; a bug-finding
> benchmark is simply the wrong instrument for them. We benchmark the one skill that
> *can* be hard-scored, and report the result straight — including that it is a null
> on frontier models. Publishing our own unfavorable data is the point.

---

## What is measured

The hypothesis: prompting an agent with the PaoDing JieNiu skill (read the grain,
enter the seams, slow at the knots, keep the blade sharp) yields **safer,
structure-aware decomposition and debugging** than a baseline agent with no such
guidance.

### Two conditions (controlled comparison)

| Condition | System Prompt | Purpose |
|-----------|---------------|---------|
| **Baseline** | Generic "investigate this and report / plan the change" | Vanilla agent, no methodology |
| **PaoDing** | Full `paoding-jieniu/SKILL.md` prepended | Skill-guided agent |

Same model, same scenarios, same task prompts — only the system prompt differs.

### The test subject

All six scenarios in `scenarios.json` point at real files in
`test-project/tangled-orders/` — a ~600 LOC service deliberately seeded with
structural pathologies (a god object, a swallowed error on a transaction
boundary, a byte-vs-char bug, mixed domains in one class, a non-atomic
double-write). Because the subject is real, results are reproducible and the
ground truth is checkable.

---

## Scoring rubric

Each agent transcript is scored on two axes.

### A. Expected-actions hit rate (objective)

For each scenario, `expected_actions` lists what a thorough, structure-first agent
should do. Score = (actions hit) / (actions total). An action is "hit" if the
transcript demonstrably does it (names the file/line, performs the check, or
states the conclusion). This is the primary objective metric.

### B. Dimensional scores (0–3 each, rubric-anchored)

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **观 Read-before-cut** | Edits immediately, no map | Skims one file | Reads several, partial map | Builds dependency/structure map before any change |
| **寻 Seam selection** | Attacks the most-coupled core first | Picks an arbitrary spot | Picks a reasonable but suboptimal cut | Identifies the true pure seam (窾) as first cut |
| **慎 Slow at the bone** | Same reckless speed everywhere | Notes risk vaguely | Flags the hard part | Explicitly slows: tests/experiments/escape hatch at 軱/族 |
| **养 Keep blade sharp** | "Rewrite it all" / no reversibility | One big change | Some staging | Small reversible commits, always-green, no debt |
| **Correctness** | Wrong root cause / wrong boundary | Partially right | Mostly right | Matches ground truth in `description` |

Scores are recorded per scenario per run. Aggregate only AFTER real runs exist.

---

## Prerequisites

```bash
pip install anthropic openai google-generativeai numpy scipy
```

Set the API key for whichever model you test:

```bash
export ANTHROPIC_API_KEY=sk-ant-...     # claude-*
export OPENAI_API_KEY=sk-...            # gpt-*
export GOOGLE_API_KEY=AI...             # gemini-*
```

---

## Running

```bash
# Dry run — print the execution plan, call no API, write no numbers
python run_benchmark.py --model claude-sonnet-4 --condition all --dry-run

# Full run: both conditions, all scenarios, 5 runs each
python run_benchmark.py --model claude-sonnet-4 --condition all --runs 5

# Single condition / single scenario (for iteration)
python run_benchmark.py --model gpt-4o --condition paoding --scenario 2 --runs 1
```

### CLI options

| Flag | Description | Default |
|------|-------------|---------|
| `--model` | `claude-sonnet-4`, `gpt-4o`, `gemini-2.5-pro`, ... | required |
| `--condition` | `baseline`, `paoding`, or `all` | `all` |
| `--runs` | runs per scenario per condition | `5` |
| `--scenario` | specific scenario id (1-6) or all | all |
| `--output-dir` | where raw results land | `results/` |
| `--skill-path` | path to SKILL.md for the paoding condition | `../SKILL.md` |
| `--codebase-path` | path to the test subject | `./test-project/tangled-orders` |
| `--dry-run` | print plan, execute nothing | off |

The runner writes only the raw model transcripts + extracted fields it actually
observed. It never invents scores.

---

## Analyzing

```bash
python analyze_results.py --input-dir results/
python analyze_results.py --input-dir results/ --compare paoding baseline
```

`analyze_results.py` computes statistics **only from real result files**. With no
results present it prints an empty report and exits — it will not emit placeholder
numbers.

### Statistical method (applied only to real data)

- **Wilcoxon signed-rank** for paired comparisons (same scenario × run across conditions).
- **Mann-Whitney U** as the unpaired fallback. Both non-parametric (small N).
- **Cohen's d** for effect size: |d| < 0.2 negligible, 0.2–0.5 small, 0.5–0.8 medium, > 0.8 large.
- Significance markers: `*` p<0.05, `**` p<0.01, `***` p<0.001, `n.s.` otherwise.

Report the exact model version, date, run count, and codebase commit hash
alongside any figure.

---

## Output structure

```
benchmark/
├── scenarios.json            # 6 scenarios, each pointing at a real test-project file
├── README_BENCHMARK.md       # this file (design only, no numbers)
├── run_benchmark.py          # runner (baseline vs paoding)
├── analyze_results.py        # statistics (only on real results)
├── test-project/             # the real subject under test
│   └── tangled-orders/...
├── results/                  # raw results (auto-created on a real run)
└── analysis/                 # analysis output (auto-created)
```

## Result record format

```json
{
  "scenario_id": 1,
  "condition": "paoding",
  "model": "claude-sonnet-4",
  "run_number": 1,
  "timestamp": "...",
  "read_before_cut": null,
  "seam_selection": null,
  "slow_at_bone": null,
  "keep_blade_sharp": null,
  "correctness": null,
  "expected_actions_hit": [],
  "raw_response": "...",
  "duration_seconds": 0.0,
  "error": ""
}
```

Dimensional fields are `null` until a human (or a separate scoring pass) fills
them per the rubric. The runner does not self-score.

## Cost estimate (order of magnitude, not a result)

Per full run = 6 scenarios × 2 conditions × 5 runs = 60 model calls. With a large
tangled-orders context (~600 LOC) plus the SKILL.md in the paoding condition,
expect a few US dollars per model on current frontier pricing. Verify against
your provider's live rates; this is a planning figure, not a measurement.

## Adding scenarios

Add an entry to `scenarios.json` (`id`, `category`, `name`, `description`=ground
truth, `task`=agent prompt, `expected_actions`, `difficulty`) and make sure the
files it references actually exist under `test-project/`. Keep ground truth out
of the `task` field — the agent must discover it.
