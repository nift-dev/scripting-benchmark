#!/usr/bin/env python3
"""Aggregate raw samples into public results (CP16).

Reads timestamped run directories under results/raw/<run>/, computes medians
for cold and warm modes separately (never merging them), and emits the
public results contract into public/data/results.json plus a compact global
index. Time, memory and code size are reported as separate dimensions; they
are never collapsed into an invented single score.
"""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results/raw"
PUBLIC = ROOT / "public/data/results.json"


def median(vals):
    return round(statistics.median(vals), 3) if vals else None


def load_raw():
    runs = sorted(p for p in RAW.iterdir() if p.is_dir()) if RAW.exists() else []
    samples = []
    for run in runs:
        for f in sorted(run.glob("*.json")):
            if f.name in ("order.json", "config.json"):
                continue
            samples.append(json.loads(f.read_text()))
    return samples, runs


def main():
    samples, runs = load_raw()
    if not samples:
        print("no raw samples found under results/raw/ (run the harness on the reference machine)")
        sys.exit(0)
    by_key = {}
    for s in samples:
        # job_id format: cat/bench/v<version>/size/lid (v1 legacy runs lacked
        # the version component; treat them as version 1).
        jid = s["job_id"]
        parts = jid.split("/")
        if len(parts) == 4:
            cat, bench, size, lid = parts
            version = 1
        else:
            cat, bench, vseg, size, lid = parts
            version = int(vseg[1:]) if vseg.startswith("v") else 1
        key = (cat, bench, version, size, lid, s["mode"])
        by_key.setdefault(key, []).append(s)
    results = []
    for (cat, bench, version, size, lid, mode), rows in by_key.items():
        rows.sort(key=lambda r: r["sample"])
        times = [r["wall_ms"] for r in rows]
        results.append({
            "benchmark": bench,
            "benchmark_version": version,
            "category": cat,
            "size": size,
            "language": lid,
            "runtime_id": lid,
            "mode": mode,
            "median_ms": median(times),
            "peak_rss_mb": round(max(r["peak_rss_kb"] or 0 for r in rows) / 1024.0, 1),
            "loc": None,
            "bytes": None,
            "samples": len(rows),
        })
    # Keep cold and warm strictly separate; emit a compact global index.
    public = {
        "schema_version": 1,
        "generated_at": None,
        "results": results,
    }
    PUBLIC.write_text(json.dumps(public, indent=2) + "\n")
    index = {
        "runs": [r.name for r in runs],
        "sample_count": len(samples),
        "result_count": len(results),
        "cold_results": sum(1 for r in results if r["mode"] == "cold"),
        "warm_results": sum(1 for r in results if r["mode"] == "warm"),
        "by_runtime": {lid: sum(1 for r in results if r["language"] == lid) for lid in sorted({r["language"] for r in results})},
    }
    derived = ROOT / "results/derived"
    derived.mkdir(parents=True, exist_ok=True)
    (derived / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"aggregated {len(samples)} samples -> {len(results)} results; cold={index['cold_results']} warm={index['warm_results']}")
    print(f"by runtime: {index['by_runtime']}")


if __name__ == "__main__":
    main()
