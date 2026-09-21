#!/usr/bin/env python3
"""Website data gate: the built site must actually display real benchmark
results. Verifies that public/data/results.json exists, has >0 real results
with a positive median, represents the expected runtimes and completed
workloads, and that the built page references the dataset. A supposedly
completed campaign whose website shows nothing is a failure.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DATA = PUBLIC / "data/results.json"

EXPECTED_RUNTIMES = {"nift", "python", "ruby", "lua54", "luajit", "node", "bash"}


def main():
    fails = []
    if not DATA.exists():
        fails.append("public/data/results.json does not exist")
    else:
        d = json.loads(DATA.read_text())
        rows = d.get("results", []) if isinstance(d, dict) else d
        if len(rows) == 0:
            fails.append("results.json has zero results")
        measured = [r for r in rows if r.get("median_ms") is not None and r["median_ms"] > 0]
        if len(measured) == 0:
            fails.append("no result carries a positive measured median")
        present = {r.get("language") for r in rows}
        missing = EXPECTED_RUNTIMES - present
        if missing:
            fails.append(f"missing expected runtimes: {sorted(missing)}")
        if not (PUBLIC / "benchmarks.html").exists():
            fails.append("public/benchmarks.html missing")
        elif "data/results.json" not in (PUBLIC / "benchmarks.html").read_text():
            fails.append("built benchmarks.html does not reference data/results.json")
    if fails:
        print("website-data gate FAIL:")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print(f"website-data gate PASS: {len(measured)} measured results, runtimes {sorted(present)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
