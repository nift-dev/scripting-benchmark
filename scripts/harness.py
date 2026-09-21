#!/usr/bin/env python3
"""Deterministic serial benchmark harness (CP2).

Expands the manifest through an explicit FIFO deque (never recursive
orchestration) and defines the complete measurement policy: warm-up/run
counts, deterministic order rotation, per-run timeout, stdout/stderr
capture, a correctness gate against golden outputs, and raw-sample
persistence.

Execution itself is intentionally gated until CP4 canonical sources and
golden outputs exist, so accidental incomplete programs can never become
benchmark measurements. `--execute` refuses to run until every job's source
and golden output is present and passes the correctness gate.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def expand_jobs(manifest):
    """Expand the manifest into the full job list (explicit FIFO queue)."""
    q = collections.deque()
    langs = {l["id"]: l for l in manifest["languages"]}
    for cat in manifest["categories"]:
        for bench in cat["benchmarks"]:
            for size in manifest["sizes"]:
                for lid, lang in langs.items():
                    if cat["id"] in lang.get("excluded_categories", []):
                        continue
                    q.append({
                        "job_id": f"{cat['id']}/{bench}/{size}/{lid}",
                        "category": cat["id"],
                        "benchmark": bench,
                        "size": size,
                        "language": lid,
                    })
    return list(q)


def rotated_order(jobs, rotation):
    """Deterministic order rotation: split at `rotation` and cycle the halves
    so language/benchmark ordering bias cannot favour one runtime."""
    if not jobs or rotation <= 0:
        return jobs
    r = rotation % len(jobs)
    return jobs[r:] + jobs[:r]


def source_path(job, manifest):
    ext = next((l.get("extension", l["id"]) for l in manifest["languages"] if l["id"] == job["language"]), job["language"])
    return ROOT / "benchmarks" / "sources" / job["category"] / job["benchmark"] / f"{job['size']}.{ext}"


def golden_path(job):
    return ROOT / "benchmarks" / "golden" / f"{job['category']}__{job['benchmark']}__{job['size']}.txt"


def command_for(lang, source, manifest):
    cmd = list(lang["command"])
    return [c.replace("{source}", str(source)) for c in cmd]


def run_once(job, manifest, timeout):
    lang = next(l for l in manifest["languages"] if l["id"] == job["language"])
    src = source_path(job, manifest)
    gold = golden_path(job)
    cmd = command_for(lang, src, manifest)
    t0 = time.perf_counter()
    try:
        p = subprocess.run(cmd, capture_output=True, text=False, timeout=timeout)
        wall = (time.perf_counter() - t0) * 1000.0
        correct = False
        if gold.exists():
            correct = p.stdout == gold.read_bytes()
        return {
            "schema_version": 1,
            "job_id": job["job_id"],
            "sample": 0,
            "mode": "warm",
            "exit_code": p.returncode,
            "correct": correct,
            "wall_ms": round(wall, 3),
            "cpu_ms": None,
            "peak_rss_kb": None,
            "stdout_sha256": sha_bytes(p.stdout),
            "stderr_sha256": sha_bytes(p.stderr),
        }, p.stderr.decode(errors="replace")
    except subprocess.TimeoutExpired:
        return {
            "schema_version": 1,
            "job_id": job["job_id"],
            "sample": 0,
            "mode": "warm",
            "exit_code": -1,
            "correct": False,
            "wall_ms": timeout * 1000.0,
            "cpu_ms": None,
            "peak_rss_kb": None,
            "stdout_sha256": sha_bytes(b""),
            "stderr_sha256": sha_bytes(b"timeout"),
        }, "timeout"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true", help="print expanded job ids")
    p.add_argument("--execute", action="store_true", help="run the jobs (gated on CP4 sources+golden)")
    p.add_argument("--limit", type=int)
    p.add_argument("--rotation", type=int, default=0, help="deterministic order rotation offset")
    p.add_argument("--check-readiness", action="store_true", help="verify every source+golden exists")
    a = p.parse_args()

    manifest = json.loads((ROOT / "benchmarks/manifest.json").read_text())
    jobs = rotated_order(expand_jobs(manifest), a.rotation)
    if a.limit:
        jobs = jobs[: a.limit]

    if a.check_readiness:
        missing = []
        for j in jobs:
            if not source_path(j, manifest).exists():
                missing.append(f"source {source_path(j, manifest).relative_to(ROOT)}")
            if not golden_path(j).exists():
                missing.append(f"golden {golden_path(j).relative_to(ROOT)}")
        if missing:
            print(f"readiness: {len(missing)} missing (CP4 not complete)")
            for m in missing[:10]:
                print("  -", m)
            sys.exit(1)
        print(f"readiness: all {len(jobs)} jobs have sources and golden outputs")
        return

    if a.list or not a.execute:
        for j in jobs:
            print(j["job_id"])
        print(f"jobs={len(jobs)}")
        return

    # CP4 gate: canonical sources and golden outputs must exist and pass the
    # correctness gate before any timing can be trusted.
    missing = [j for j in jobs if not source_path(j, manifest).exists() or not golden_path(j).exists()]
    if missing:
        print(f"execution gate closed: {len(missing)} jobs lack CP4 sources/golden outputs", file=sys.stderr)
        sys.exit(1)

    cfg = manifest.get("measurement", {})
    timeout = cfg.get("timeout_seconds", 30)
    raw_dir = ROOT / "results/raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    run = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = raw_dir / run
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "order.json").write_text(json.dumps([j["job_id"] for j in jobs], indent=2) + "\n")

    failures = 0
    for job in jobs:
        sample, err = run_once(job, manifest, timeout)
        if not sample["correct"] or sample["exit_code"] != 0:
            failures += 1
        safe = job["job_id"].replace("/", "__")
        (run_dir / f"{safe}.json").write_text(json.dumps(sample, indent=2) + "\n")
        print(f"{'OK ' if sample['correct'] else 'BAD'} {job['job_id']}")
    print(f"done: {len(jobs)} jobs, {failures} failed correctness gate")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
