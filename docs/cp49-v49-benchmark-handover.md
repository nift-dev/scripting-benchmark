# NIFT v4.9 — performance campaign handover to official benchmarking

CP49: **GO / CLOSED**. Safe bounded core optimization space is exhausted for this tranche. Stop core development. The user accepted the campaign and authorized the benchmark/Labs workspace to run a **new official series**.

## Frozen candidate and certification

- Exact benchmark source: **d9b85f22c4dab11d0ab68a8778a1471bf35ba488**.
- Development version: **4.9.0**; C ABI: **1.3**.
- Core branch main matches origin/main, clean, 0 ahead / 0 behind at handoff.
- NRS **93/93 PASS**; PRS **12/12 PASS**.
- All required hosted walls **GREEN**, including Linux/macOS/Windows, Deep Guards, Test Integrity, warnings, performance, FFI, bytes and build-only packaging.
- Local full tests, bindings (including fresh-cache Go/race), ASan/UBSan/LSan, 62 clean Memcheck executions and the unchanged 1,219-case fuzz corpus on original/final sanitized runtimes pass.
- Evidence: `../../nift/docs/evidence/cp49-campaign/report.md`; certificates and source fingerprints are in its `final/` directory. Runtime last changed at `26ab438`; final guards at `6e67dd7`; d9b85f2 adds evidence/documentation only.

## Accepted retained work

1. Live numeric identity dispatch: identity-map instructions about −7%.
2. Narrow live array indexed selector plans: indexed map −73.6%, indexed sort −56.3%; immutable syntax only, no cached runtime values/scopes/locations.
3. Cached exact filesystem ordering keys: traversal instructions and allocations about −60.5%; existing ordering preserved.
4. Move owned map/filter results: aggregate map/filter instructions about −9%/−5%, with materially reduced aggregate allocations/RSS.
5. One JSON timer preflight per conversion: deep four-stage probe instructions −36.6%; timer error precedence preserved; no vendored Jsonic++ changes.
6. Construction-only ordered group_by index: unique grouping instructions −44.9%; removes repeated superlinear scans. Accepted bounded temporary-index tradeoff: +6.63% RSS in the unique 16k case; RuntimeValue representation unchanged.

These figures are independent local diagnostics, not predictions of official results. All 31 probe families preserve observable output. Unaffected instruction controls remain approximately neutral. No benchmark-specific core code or benchmark/Labs source changes were introduced during CP49. This handover is post-campaign documentation.

Public syntax/API/ABI, live captures, alias/location ownership, error/source origins, callback side effects, named-call precedence, filesystem ordering, grouping insertion order/rendered-key collisions and JSON timer failure priority are preserved.

Scope reserve was measured, rejected and fully reverted. Broad typed-call adapters, callback hoisting, reusable frames/arenas, closure storage, root/path ownership, general loops/evaluator, RuntimeValue redesign, VM/JIT and vendored parser work remain deferred. Do not reopen them during benchmarking.

## Previous official oracle and next series

- Frozen previous series: **20261008-v480**.
- Frozen measured Nift source: **c80c2cd6f4a2e782e861431637af014bb8a0668c**, confirmed by the retained campaign README.
- New official series: **REQUIRED / NOT YET STARTED at handoff**. Choose a fresh unique identity and record the exact candidate SHA above.
- Frozen oracle unchanged: **YES**, all 2,828 CP49-recorded file hashes verified at handoff.

Never overwrite, patch, pool, reinterpret or regenerate the old measurements. Preserve established workload families, correctness/integrity checks, warmups, sample counts, credible competitors and result-retention policy; remove no samples. Record hardware, OS/image, node type, compilers, runtime versions and every measured source identity. Report any actual methodological defect explicitly before changing the methodology.

Where fresh nodes are needed, provision them through the established Linode CLI workflow, keep credentials private, record their identities/environment, complete measurements, delete only campaign-owned nodes immediately after completion, and independently verify deletion. Do not reuse deleted nodes or affect unrelated infrastructure.

Where practical, build both frozen v4.8 source c80c2cd and accepted v4.9 source d9b85f2 on the new node for targeted same-node A/B attribution. Keep those measurements separate from the official series. Cross-node official-series deltas cannot be attributed entirely to Nift.

Pay attention to existing sort/identity, callback/index, filesystem, represented grouping, JSON, frequency-count, map/set, BFS, calls and loops. Do not add or modify workloads to favor CP49. Explicitly disclose improvements with no corresponding official workload. **The CP49 local indexed-selector probe uses `x => a[x]`; the old official workload named sort-index uses `x => x`. Do not assign the local −56.3% indexed-selector result to that official identity workload.**

## Execution and return

Run the new official series in the benchmark/Labs workspace without modifying Nift core. If a genuine core defect is found, stop and report it separately; do not patch core and continue with the same candidate/series identity. Do not predict results.

After completion, update `lab.nift.dev`, preserve old-series access, clearly identify both series, and report absolute results, separately labelled same-node attribution, qualified previous-series comparisons, competitive workloads and remaining gaps. Return evidence to the core chat before deciding whether another performance campaign is justified. No further core optimization tranche is authorized.

User's full authorization and outline: `/home/nick/.codex/attachments/b59d3440-0dfb-4f26-bcb4-4058cff6c323/Pasted text.txt`.
