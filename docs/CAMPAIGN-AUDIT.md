# October 2026 campaign audit — before implementation

Reviewed manifest, all harness/validation/aggregation scripts, retained raw-run
configuration, representative implementations and fixture layout.

Keep: serial execution, tool-native implementations, golden outputs, explicit
Bash/Lua exclusions, raw samples, workload versioning, separate latency/memory.
The algorithm corpus is useful as a runtime diagnostic, not a representative
aggregate score for everyday scripting. Preserve old evidence unchanged.

Improve (publication blockers):
- The measurement runner validates only once, ignores timed exit/output, then
  hardcodes correct=true and exit_code=0. Validate every invocation, persist
  failures and stop publication on any failure.
- "cold" and "warm" are both fresh processes after warmups. Remove the false
  cache distinction. Call this repeated fresh-process, OS-cache-uncontrolled
  measurement. Application-cold requires explicit state preparation.
- GNU time wrapper is included in elapsed time; fallback RSS is cumulative
  across children. Use direct Popen/wait4 accounting on Linux. That RSS is
  per-child high-water RSS, not aggregate process-tree RSS; disclose it.
- Aggregator merges all run directories (including historical machines and
  synthetic schema-1 samples), does not gate correctness, and reports maximum
  RSS rather than median. Require one explicitly selected campaign run.
- Resolve runtime executables and retain version/hash, commands, CPU affinity,
  OS/kernel/CPU/RAM and suite revision; run from repository root because several
  fixture paths are relative.
- No missing implementation should silently disappear from requested scope.
  Implemented complete workload families can be selected, but exclusions must
  be explicit. Pending SQLite/mixed/breadth workloads are not evidence.
- Existing numeric oracle uses float conversion, potentially accepting rounded
  large integers. Restrict numeric equivalence to exact decimal values and
  require successful exit.

Remove from new headline analysis: misleading cold/warm labels and global
rankings across dissimilar workloads. Keep microbenchmarks in a diagnostic
appendix. Shell/cold-start duplicates startup coverage in the new shell suite;
retain historical sources but explain overlap.

Add: failure-gate regression checks, run-specific summaries with sample counts,
median/min/max/p95, independently measured memory, explicit preparation/cache
policy, clean-checkout smoke verification. Practical workloads absent from the
manifest implementations remain a disclosed gap rather than fabricated rows.

Comparability: direct timing without GNU time, exact oracle changes, explicit
run selection, current binaries and cache-label corrections break direct
comparison with published medians. Historical data is not a baseline for speedup
claims. Algorithm/FFI/external-helper differences must be discussed per workload.

Implementation inspection addendum: Nift json-transform writes/reads a scratch
JSON file while competitors construct arrays directly. Correct Nift to construct
the same records in memory (workload version 2). JSON parse/traverse/mutate all
include the same fixture read. BFS implementations use different idiomatic
queue/distance structures: describe this as implementation comparison, not
isolated container speed. The existing Nift run/build command spellings are stale.

Measurement refinement: compile a small C supervisor outside timed intervals.
It times fork/exec through wait4 with CLOCK_MONOTONIC and reports child RSS,
avoiding Python pre-exec high-water contamination and wrapper startup overhead.
Absolute latency excludes Python orchestration and supervisor launch.
