# Scripting Benchmark

The correctness-gated October campaign is documented in [docs/CAMPAIGN-RUN.md](docs/CAMPAIGN-RUN.md) and [docs/CAMPAIGN-AUDIT.md](docs/CAMPAIGN-AUDIT.md). Use `scripts/campaign.py` and `scripts/summarize.py`; the legacy runners are retired.

The existing explorer and historical raw data are preserved and explicitly labelled. Their earlier cold/warm measurements cannot be compared as baselines for the corrected campaign. The new report and raw evidence are published at https://lab.nift.dev/benchmarks/scripting/.

Frequency counting v2 uses streaming counters; sort-index accurately names sorting plus indexed reads; the old endpoint-only two-pointer case is outside the new measured corpus. Pending manifest families do not imply measured coverage. See the report for exact families, versions and commands.
