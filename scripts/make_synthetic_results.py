#!/usr/bin/env python3
"""Generate SYNTHETIC (fixture) result data to exercise the website's results
consumption path and the contract validation (CP1 gate).

These numbers are fabricated placeholders — NOT measurements. Real results
require the reference benchmark machine (CP3+); never publish synthetic data
as if it were measured.
"""
import datetime
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results/raw"
RAW.mkdir(parents=True, exist_ok=True)
PUBLIC = ROOT / "public/data"
PUBLIC.mkdir(parents=True, exist_ok=True)

random.seed(20260920)  # deterministic fixture


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def main():
    manifest = json.loads((ROOT / "benchmarks/manifest.json").read_text())
    langs = [l["id"] for l in manifest["languages"]]
    samples = []
    # One synthetic raw sample per (category/benchmark, size, language) pair,
    # both modes, small sample counts so the aggregation path is exercised.
    for cat in manifest["categories"]:
        for bench in cat["benchmarks"]:
            for size in manifest["sizes"]:
                for lid in langs:
                    if cat["id"] in next(l.get("excluded_categories", []) for l in manifest["languages"] if l["id"] == lid):
                        continue
                    job_id = f"{cat['id']}/{bench}/{size}/{lid}"
                    for mode in ("cold", "warm"):
                        for s in range(3):
                            wall = round(random.uniform(1.0, 50.0), 3)
                            record = {
                                "schema_version": 1,
                                "job_id": job_id,
                                "sample": s,
                                "mode": mode,
                                "exit_code": 0,
                                "correct": True,
                                "wall_ms": wall,
                                "cpu_ms": round(wall * 0.9, 3),
                                "peak_rss_kb": random.randint(5000, 120000),
                                "stdout_sha256": sha(f"{job_id}:{mode}:{s}"),
                                "stderr_sha256": sha(""),
                            }
                            samples.append(record)
    # Persist one raw-sample object per file (the raw-sample schema is per
    # sample), named from the job id + mode + sample index.
    by_job = {}
    for r in samples:
        by_job.setdefault(r["job_id"], []).append(r)
    for r in samples:
        safe = r["job_id"].replace("/", "__")
        (RAW / f"{safe}__{r['mode']}__{r['sample']}.json").write_text(json.dumps(r, indent=2) + "\n")

    # Aggregate into the public results contract (synthetic medians).
    results = []
    for job_id, rows in by_job.items():
        cat, bench, size, lid = job_id.split("/")
        warm = [r["wall_ms"] for r in rows if r["mode"] == "warm"]
        med = sorted(warm)[len(warm) // 2] if warm else None
        results.append({
            "benchmark": bench,
            "category": cat,
            "language": lid,
            "runtime_id": lid,
            "mode": "warm",
            "median_ms": med,
            "peak_rss_mb": round(max(r["peak_rss_kb"] for r in rows) / 1024.0, 1),
            "loc": None,
            "bytes": None,
            "samples": len([r for r in rows if r["mode"] == "warm"]),
        })
    public = {
        "schema_version": 1,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "results": results,
    }
    (PUBLIC / "results.json").write_text(json.dumps(public, indent=2) + "\n")
    print(f"synthetic fixture: {len(samples)} raw samples, {len(results)} aggregated results")
    print("NOTE: synthetic placeholders only; real measurements require the reference machine")


if __name__ == "__main__":
    sys.exit(main())
