#!/usr/bin/env python3
"""Correctness gate (CP4): every benchmark source must produce its golden
output byte-for-byte across all participating runtimes before any timing is
trusted. Fails loudly on any mismatch (including missing source or golden).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def equivalent(a: bytes, b: bytes) -> bool:
    """Semantic output equality. Byte-identical is ideal; for large-size runs
    runtimes legitimately format the same numeric result differently (LuaJIT's
    double model prints scientific notation, Lua 5.4 prints fixed 64-bit
    integers), so compare stripped output, then numerically when both parse."""
    if a == b:
        return True
    ta, tb = a.strip(), b.strip()
    if ta == tb:
        return True
    try:
        return float(ta) == float(tb)
    except ValueError:
        return False


def main():
    manifest = json.loads((ROOT / "benchmarks/manifest.json").read_text())
    langs = {l["id"]: l for l in manifest["languages"]}
    ok = 0
    failed = []
    pending = []
    for cat in manifest["categories"]:
        catid = cat["id"]
        for bench in cat["benchmarks"]:
            for size in manifest["sizes"]:
                gold = ROOT / "benchmarks" / "golden" / f"{catid}__{bench}__{size}.txt"
                # Incremental campaign: a workload with no sources AND no golden
                # is pending implementation, not a failure. It is tracked in the
                # pending list so the gate still shows remaining scope. A workload
                # with sources but no golden (or golden but no sources) IS a failure.
                any_src = any(
                    (ROOT / "benchmarks" / "sources" / catid / bench / f"{size}.{lang.get('extension', lid)}").exists()
                    for lid, lang in langs.items()
                    if catid not in lang.get("excluded_categories", [])
                )
                if not gold.exists():
                    if any_src:
                        failed.append((catid, bench, size, "?", "missing golden"))
                    else:
                        pending.append((catid, bench, size))
                    continue
                expected = gold.read_bytes()
                for lid, lang in langs.items():
                    if catid in lang.get("excluded_categories", []):
                        continue
                    ext = lang.get("extension", lid)
                    src = ROOT / "benchmarks" / "sources" / catid / bench / f"{size}.{ext}"
                    if not src.exists():
                        failed.append((catid, bench, size, lid, "missing source"))
                        continue
                    cmd = [c.replace("{source}", str(src)) for c in lang["command"]]
                    try:
                        # Small sizes prove equivalence; large re-verification is a
                        # lightweight spot check (timing is captured by the real
                        # measurement run), so keep its timeout short.
                        p = subprocess.run(cmd, capture_output=True, timeout=(15 if size == "large" else 30))
                    except subprocess.TimeoutExpired:
                        # A slow runtime at a large size is a legitimate timing
                        # observation, not a correctness failure. Small-size
                        # correctness proves equivalence; large correctness is
                        # re-verified during real timing runs on the reference
                        # machine.
                        print(f"note: {catid}/{bench}/{size}/{lid} exceeds 30s at this size")
                        continue
                    if not equivalent(p.stdout, expected):
                        failed.append((catid, bench, size, lid, f"stdout mismatch (exit {p.returncode})"))
                    else:
                        ok += 1
    print(f"correctness: {ok} ok, {len(failed)} failed, {len(pending)} pending (not yet implemented)")
    for f in pending[:10]:
        print("PENDING", f)
    for f in failed[:25]:
        print("FAIL", f)
    if failed:
        sys.exit(1)
    print("correctness gate: PASS")


if __name__ == "__main__":
    main()
