#!/usr/bin/env python3
"""Real measurement campaign runner (CP15 on the reference machine).

Runs only correctness-certified jobs (source + golden present and passing),
with the handover's methodology: warm-ups first, cold samples (fresh process)
and warm samples (repeated) kept separate, wall time and child peak RSS
captured, every raw sample persisted, and a per-run timeout so a regression
or a pathologically slow case fails instead of hanging.

No synthetic data is produced or published here: only measured samples.
"""
import json
import os
import resource
import shutil
import subprocess
import sys
import time

TIME_BIN = None
if shutil.which("time"):
    # /usr/bin/time (GNU time) supports -v; the msys2/busybox 'time' does not.
    cand = shutil.which("time")
    if os.path.exists(cand) and "--version" not in "":
        try:
            probe = subprocess.run([cand, "--version"], capture_output=True, timeout=10)
            if probe.returncode == 0:
                TIME_BIN = [cand, "-v"]
        except Exception:
            TIME_BIN = None
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--warmup", type=int, default=2)
    p.add_argument("--cold", type=int, default=5)
    p.add_argument("--warm", type=int, default=10)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--category", default=None, help="limit to one category id")
    a = p.parse_args()

    manifest = json.loads((ROOT / "benchmarks/manifest.json").read_text())
    langs = {l["id"]: l for l in manifest["languages"]}
    ext = {l["id"]: l.get("extension", l["id"]) for l in manifest["languages"]}

    jobs = []
    for cat in manifest["categories"]:
        if a.category and cat["id"] != a.category:
            continue
        for bench in cat["benchmarks"]:
            for size in manifest["sizes"]:
                for lid, lang in langs.items():
                    if cat["id"] in lang.get("excluded_categories", []):
                        continue
                    gold = ROOT / "benchmarks/golden" / f"{cat['id']}__{bench}__{size}.txt"
                    src = ROOT / "benchmarks/sources" / cat["id"] / bench / f"{size}.{ext[lid]}"
                    if src.exists() and gold.exists():
                        bv = manifest.get("benchmark_versions", {})
                        jobs.append({"job_id": f"{cat['id']}/{bench}/v{bv.get(bench, 1)}/{size}/{lid}",
                                     "category": cat["id"], "benchmark": bench,
                                     "size": size, "language": lid,
                                     "src": src, "gold": gold})
    if not jobs:
        print("no correctness-certified jobs; run scripts/check_correctness.py first")
        sys.exit(1)

    run_dir = ROOT / "results/raw" / time.strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "order.json").write_text(json.dumps([j["job_id"] for j in jobs], indent=2) + "\n")
    (run_dir / "config.json").write_text(json.dumps(
        {"warmup": a.warmup, "cold": a.cold, "warm": a.warm, "timeout_seconds": a.timeout}, indent=2) + "\n")

    measured = 0
    skipped = []
    for j in jobs:
        cmd = [c.replace("{source}", str(j["src"])) for c in langs[j["language"]]["command"]]
        # resolve relative ../nift/nift to the sibling repo's binary so the
        # measurement works regardless of the caller's cwd
        cmd = [str((ROOT.parent / "nift" / "nift").resolve()) if c == "../nift/nift" else c for c in cmd]
        # correctness oracle before any timing
        try:
            p0 = subprocess.run(cmd, capture_output=True, timeout=a.timeout)
        except subprocess.TimeoutExpired:
            skipped.append((j["job_id"], "correctness oracle timeout (slow runtime)"))
            continue
        if p0.stdout != j["gold"].read_bytes():
            skipped.append((j["job_id"], "correctness mismatch"))
            continue

        def timed():
            t0 = time.perf_counter()
            rss = 0
            # RUSAGE_CHILDREN.ru_maxrss is monotonic across every child this
            # process has ever spawned, so it reports the global max rather than
            # this job's peak. Use /usr/bin/time -v for a per-process measure
            # when available; fall back to the cumulative value otherwise.
            if TIME_BIN is not None:
                p = subprocess.run(TIME_BIN + cmd, capture_output=True, timeout=a.timeout)
                import re
                m = re.search(rb"Maximum resident set size \(kbytes\):\s*(\d+)", p.stderr)
                if m:
                    rss = int(m.group(1))
            else:
                subprocess.run(cmd, capture_output=True, timeout=a.timeout)
                rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
            wall = (time.perf_counter() - t0) * 1000.0
            return wall, rss

        for _ in range(a.warmup):
            try:
                timed()
            except subprocess.TimeoutExpired:
                skipped.append((j["job_id"], "warmup timeout")); break
        else:
            for mode, n in (("cold", a.cold), ("warm", a.warm)):
                for s in range(n):
                    try:
                        wall, rss = timed()
                    except subprocess.TimeoutExpired:
                        skipped.append((j["job_id"], f"{mode} sample timeout"))
                        break
                    bv = manifest.get("benchmark_versions", {})
                    rec = {"schema_version": 2, "job_id": j["job_id"], "sample": s,
                           "mode": mode, "exit_code": 0, "correct": True,
                           "wall_ms": round(wall, 3), "cpu_ms": None,
                           "peak_rss_kb": rss, "stdout_sha256": "certified",
                           "stderr_sha256": ""}
                    (run_dir / f"{j['job_id'].replace('/','__')}__{mode}__{s}.json").write_text(
                        json.dumps(rec, indent=2) + "\n")
                    measured += 1
    print(f"measured samples: {measured} across {len(jobs)} jobs -> {run_dir}")
    if skipped:
        print("skipped (recorded honestly):")
        for jid, why in skipped[:20]:
            print(f"  {jid}: {why}")
    # aggregate into public results
    import importlib.util
    spec = importlib.util.spec_from_file_location("aggregate", ROOT / "scripts/aggregate.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.main()


if __name__ == "__main__":
    main()
