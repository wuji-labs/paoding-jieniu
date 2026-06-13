#!/usr/bin/env python3
"""PaoDing JieNiu benchmark runner.

Runs each scenario under two conditions (baseline vs paoding) against a chosen
model and writes RAW transcripts to results/. It does NOT score and does NOT
fabricate any numbers: dimensional rubric fields are written as null for a later
human/scoring pass. With --dry-run it touches no network and writes nothing.

Dependencies (install only the SDK for the model you use):
    pip install anthropic        # claude-*
    pip install openai           # gpt-*
    pip install google-generativeai   # gemini-*

Usage:
    python run_benchmark.py --model claude-sonnet-4 --condition all --dry-run
    python run_benchmark.py --model claude-sonnet-4 --condition all --runs 5
"""
import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path

# Map a friendly model name to a concrete provider + pinned model id.
MODEL_REGISTRY = {
    "claude-sonnet-4": ("anthropic", "claude-sonnet-4-20250514"),
    "gpt-4o": ("openai", "gpt-4o"),
    "gemini-2.5-pro": ("google", "gemini-2.5-pro"),
    # Local, zero-cost, no API key — run the whole benchmark for free with Ollama.
    # These are weak/mid models on purpose: a frontier model is near-ceiling on a
    # 150-LOC subject, so the skill's lift is best measured on a weaker base.
    "qwen2.5vl-7b": ("ollama", "qwen2.5vl:7b"),
    "qwen3-32b": ("ollama", "qwen3:32b"),
    "ollama": ("ollama", os.environ.get("OLLAMA_MODEL", "qwen2.5vl:7b")),
}

CONDITIONS = ("baseline", "paoding")

BASELINE_SYSTEM = (
    "You are a senior software engineer. Investigate the described problem in the "
    "given codebase and either plan the change or diagnose the bug. Be thorough."
)

HERE = Path(__file__).resolve().parent


def load_scenarios():
    path = HERE / "scenarios.json"
    if not path.exists():
        sys.exit(f"scenarios.json not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_skill_system(skill_path: Path) -> str:
    if not skill_path.exists():
        sys.exit(
            f"SKILL.md not found at {skill_path}. Pass --skill-path to point at it."
        )
    return skill_path.read_text(encoding="utf-8")


def build_user_prompt(scenario: dict, codebase_path: str) -> str:
    # The agent is told the task and where the real code lives. Ground truth
    # (scenario['description']) is deliberately withheld.
    return (
        f"The codebase under test is at: {codebase_path}\n\n"
        f"Task:\n{scenario['task']}\n\n"
        "Read the relevant files before drawing conclusions. Explain where you "
        "would make the first change and what you would deliberately not touch yet."
    )


def call_anthropic(model_id, system, user):
    import anthropic

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model_id,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def call_openai(model_id, system, user):
    from openai import OpenAI

    client = OpenAI()
    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content


def call_google(model_id, system, user):
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(model_id, system_instruction=system)
    resp = model.generate_content(user)
    return resp.text


def call_ollama(model_id, system, user):
    # Local Ollama HTTP API. Stdlib only — no SDK, no API key, no network cost.
    # Host overridable via OLLAMA_HOST (default http://localhost:11434).
    import urllib.request

    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").strip().rstrip("/")
    # Normalize: 0.0.0.0 is a bind-all address, not connectable; add scheme if bare.
    host = host.replace("0.0.0.0", "127.0.0.1")
    if "://" not in host:
        host = "http://" + host
    payload = json.dumps({
        "model": model_id,
        "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": 0.3},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{host}/api/chat", data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("message", {}).get("content", "")


PROVIDER_DISPATCH = {
    "anthropic": call_anthropic,
    "openai": call_openai,
    "google": call_google,
    "ollama": call_ollama,
}

# Providers that cannot browse the filesystem themselves (plain chat completions).
# For these we inline the codebase into the prompt instead of pointing at a path.
NON_AGENTIC_PROVIDERS = {"ollama", "openai", "google"}


def inline_codebase(codebase_path: str) -> str:
    root = Path(codebase_path)
    if not root.exists():
        return ""
    chunks = []
    for f in sorted(root.rglob("*.py")):
        try:
            chunks.append(f"--- {f.relative_to(root)} ---\n{f.read_text(encoding='utf-8')}")
        except Exception:
            continue
    return "\n\n".join(chunks)


def run_once(provider, model_id, system, user):
    started = time.time()
    text = PROVIDER_DISPATCH[provider](model_id, system, user)
    return text, time.time() - started


def empty_record(scenario, condition, model_name, run_number):
    """A result record with NULL rubric fields — never self-scored."""
    return {
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "condition": condition,
        "model": model_name,
        "run_number": run_number,
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "read_before_cut": None,
        "seam_selection": None,
        "slow_at_bone": None,
        "keep_blade_sharp": None,
        "correctness": None,
        "expected_actions_hit": [],
        "expected_actions_total": scenario["expected_actions"],
        "raw_response": "",
        "duration_seconds": 0.0,
        "error": "",
    }


def main():
    ap = argparse.ArgumentParser(description="PaoDing JieNiu benchmark runner")
    ap.add_argument("--model", required=True, choices=sorted(MODEL_REGISTRY))
    ap.add_argument("--condition", default="all",
                    choices=("baseline", "paoding", "all"))
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--scenario", default="all",
                    help="scenario id (e.g. 2) or 'all'")
    ap.add_argument("--output-dir", default=str(HERE / "results"))
    ap.add_argument("--skill-path", default=str(HERE.parent / "SKILL.md"))
    ap.add_argument("--codebase-path",
                    default=str(HERE / "test-project" / "tangled-orders"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    provider, model_id = MODEL_REGISTRY[args.model]
    scenarios = load_scenarios()
    if args.scenario != "all":
        scenarios = [s for s in scenarios if str(s["id"]) == str(args.scenario)]
        if not scenarios:
            sys.exit(f"No scenario with id {args.scenario}")

    conditions = CONDITIONS if args.condition == "all" else (args.condition,)
    paoding_system = None
    if "paoding" in conditions:
        paoding_system = load_skill_system(Path(args.skill_path))

    plan_count = len(scenarios) * len(conditions) * args.runs
    print(f"Model: {args.model} ({provider}:{model_id})")
    print(f"Conditions: {', '.join(conditions)}")
    print(f"Scenarios: {[s['id'] for s in scenarios]}  Runs each: {args.runs}")
    print(f"Total model calls planned: {plan_count}")
    print(f"Codebase under test: {args.codebase_path}")

    if args.dry_run:
        print("\n[dry-run] No API calls made, no files written.")
        return

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    code_blob = ""
    if provider in NON_AGENTIC_PROVIDERS:
        code_blob = inline_codebase(args.codebase_path)
        if not code_blob:
            sys.exit(f"No .py files to inline under {args.codebase_path}")

    for condition in conditions:
        system = BASELINE_SYSTEM if condition == "baseline" else paoding_system
        records = []
        for scenario in scenarios:
            user = build_user_prompt(scenario, args.codebase_path)
            if code_blob:
                user += (
                    "\n\nYou cannot browse the filesystem; the full codebase under "
                    f"test is inlined below.\n\n{code_blob}"
                )
            for run_number in range(1, args.runs + 1):
                rec = empty_record(scenario, condition, args.model, run_number)
                try:
                    text, dur = run_once(provider, model_id, system, user)
                    rec["raw_response"] = text
                    rec["duration_seconds"] = round(dur, 2)
                    print(f"  ok  s{scenario['id']} {condition} run{run_number} "
                          f"({dur:.1f}s)")
                except Exception as exc:  # solve-don't-punt: record, keep going
                    rec["error"] = f"{type(exc).__name__}: {exc}"
                    print(f"  ERR s{scenario['id']} {condition} run{run_number}: "
                          f"{rec['error']}", file=sys.stderr)
                records.append(rec)
        out_file = out_dir / f"{args.model}_{condition}.json"
        out_file.write_text(json.dumps(records, ensure_ascii=False, indent=2),
                            encoding="utf-8")
        print(f"Wrote {out_file} ({len(records)} records, rubric fields = null)")

    print("\nRaw transcripts written. Score them per README_BENCHMARK.md rubric, "
          "then run analyze_results.py. This runner never self-scores.")


if __name__ == "__main__":
    main()
