#!/usr/bin/env python3
"""Validate the benchmark contracts against their JSON Schemas (CP1).

Checks the manifest, environment record, raw samples and public results
against the versioned schemas in schemas/. Fails loudly rather than
publishing data that does not conform.
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required: python3 -m pip install jsonschema")

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text())


def validate(document, schema_path, label):
    schema = load(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.path))
    if errors:
        print(f"FAIL {label}: {len(errors)} schema violation(s)", file=sys.stderr)
        for e in errors[:10]:
            print(f"  - {'/'.join(str(p) for p in e.path) or '(root)'}: {e.message}", file=sys.stderr)
        return False
    print(f"PASS {label} validates against {schema_path.name}")
    return True


def main():
    ok = True
    manifest = load(ROOT / "benchmarks/manifest.json")
    ok &= validate(manifest, ROOT / "schemas/definition.schema.json", "manifest")

    env_path = ROOT / "results/environment.json"
    if env_path.exists():
        ok &= validate(load(env_path), ROOT / "schemas/environment.schema.json", "environment")

    raw_dir = ROOT / "results/raw"
    raw = sorted(raw_dir.glob("*.json")) if raw_dir.exists() else []
    if raw:
        for p in raw:
            ok &= validate(load(p), ROOT / "schemas/raw-sample.schema.json", f"raw sample {p.name}")
    else:
        print("raw samples: none present (expected before the reference-machine campaign)")

    public = load(ROOT / "public/data/results.json")
    ok &= validate(public, ROOT / "schemas/public-results.schema.json", "public results")

    if not ok:
        sys.exit(1)
    print("contracts: all conform")


if __name__ == "__main__":
    main()
