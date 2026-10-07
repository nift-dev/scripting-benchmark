# Running the new campaign

Use scripts/campaign.py, not historical run_measurements.py/aggregate.py.
Specify a comma-separated list of complete category/benchmark families and
--nift, --samples (>=5), --warmups, --timeout and --output. This intentionally
fails for missing runtimes, missing implementations or any incorrect invocation.
The old measurement/aggregation scripts remain historical implementation only;
their outputs must not be published as current campaign evidence.

Each result is one immutable machine/version run; scripts/summarize.py verifies
all correctness flags/sample counts and regenerates summaries from that file.
No historical runs are merged. A C supervisor times fork/exec through wait4;
compiler preparation is outside latency. RSS is waited-child high-water rather
than simultaneous aggregate tree memory. Every sample is a new runtime process,
with allowlisted environment and isolated HOME/XDG; repository fixtures are read
from the suite root. OS caches are uncontrolled. Report fresh-process-repeated,
not the historical misleading cold/warm distinction. Retain warmup records.

Pending families are excluded explicitly in the report, not silently timed.
Algorithm cases compare idiomatic implementations (BFS distance-map/queue choices
vary), not a universal language score. Native JIT/interpreter differences and
external tools in Bash filesystem work are part of the measured implementation.
Current JSON transform uses in-memory construction for every runtime (v2).

Dependencies and exact versions/hashes are frozen by the provisioning manifest.
Run scripts/test_measurement.py first, then a complete correctness pilot.
