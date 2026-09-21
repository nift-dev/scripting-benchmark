# HANDOVER.md
v0.0.8

This is a living handover for working effectively in a Nift project.

Canonical version:

https://nift.dev/HANDOVER.md

Check the version at the top of this file against the canonical copy when the
project is old, unfamiliar, or behaving differently from the current Nift
documentation.

To replace this file with the latest canonical version:

```sh
curl -fsSL https://nift.dev/HANDOVER.md -o HANDOVER.md
```

If this project has project-specific additions, preserve or reapply them when
updating the canonical handover.

This project uses Nift as part of its website build process.

Nift is the project's build-time templating and dependency layer. It does not determine what the website is about or what other technologies the project should use.

Keep the existing project architecture and use the project's normal HTML, CSS, JavaScript, frameworks, backend, and other tooling where appropriate.

Do not introduce Nift-specific machinery where ordinary web tooling is the clearer solution.

## Start here

Before making substantial changes:

1. Inspect `.nift/config.json` and `.nift/tracked.json`.
2. Inspect the existing `content/`, `templates/`, and output structure.
3. Read this project's `README.md` and other project-specific documentation.
4. Run:

```sh
nift status
```

During normal development, build frequently:

```sh
nift build
```

Use this throughout a task, not only at the end. Rebuild after meaningful
changes so Nift can surface template, path, dependency, configuration, and
tracking errors while the cause is still obvious.

In particular, run `nift build` immediately after editing
`.nift/config.json` or `.nift/tracked.json`.

Use:

```sh
nift status
```

when you want to inspect what Nift considers stale and why.

Successful `nift build` output may include indented `↳ ...` lines explaining
why a page was considered stale and rebuilt, such as a missing generated output
or a changed dependency. These are rebuild reasons, not errors. Actual build
failures are reported as errors and cause the build to fail.

Do not delete or recreate `.nift/`.

## Nift's core template model

Most Nift websites need very little Nift-specific syntax.

The three primitives you will use most often are:

```text
@content
@input(...)
@path(...)
```

`@content` inserts the tracked page's content into its template.

```html
<main>
    @content
</main>
```

`@content` should execute exactly once across the rendered template/input graph
for a tracked page. It is normally placed in the page's template; the tracked
content file supplies the content inserted there.

Content files may still use other Nift syntax when needed. If page text needs
to display Nift syntax literally, prefix the active sigil with `\` rather than
leaving it as template syntax:

```html
<code>\@content</code>
<code>\@path('about')</code>
<code>\$[title]</code>
```

This applies whenever `@...`, `$[...]`, or other Nift syntax is intended as
literal output rather than something Nift should execute or resolve.

`@input(...)` inserts a reusable file and automatically makes it a dependency of the output using it.

```html
@input('templates/header.html')

<main>
    @content
</main>

@input('templates/footer.html')
```

### Structured JSON and markup sources

Use name-first `@json` when a template needs immutable structured data:

```text
@json(name, path)
@json(name, schema-path, path)
@json(name, schema-name, path)
@json(name){...}
@json(name, schema-path){...}
@json(name, schema-name){...}
```

Inline bodies are evaluated as Nift templates before JSON parsing. A schema
name refers to an earlier JSON binding. Data and schema files are automatic
dependencies and paths must stay inside the project.

Use `@markup(format){...}` or `@markup(format, path)` for Markdown (`md`),
AsciiDoc (`adoc`) or reStructuredText (`rst`). Nift evaluates template syntax in
the source first, Markup++ converts it once, and the resulting HTML is appended
without being parsed as Nift syntax again. File sources and host-resolved
AsciiDoc/RST includes are automatic dependencies.

`@path(...)` creates project-aware links to tracked pages and local assets.

Nift has additional features including metadata, JSON data, loops, conditionals, pagination, contracts, and explicit dependencies. Use them when the project actually needs them; do not use advanced features merely because they exist.

When writing expressions inside constructs such as `@if(...)`, refer to values directly rather than wrapping them in `$[...]`. For example:

```html
@if(name == 'about'){...}
```

Use `$[...]` when resolving or rendering a value into output, for example `$[title]`. Consult the expressions and control-flow documentation when using more advanced expression syntax.

## Internal links: use `@path`

Use `@path(...)` for internal links.

This applies to:

- links between pages;
- stylesheets;
- JavaScript;
- images and other local assets where Nift should know the relationship.

For pages, link to the **tracked page name**, not its generated file.

```html
<nav>
    <a href="@path('/')">Home</a>
    <a href="@path('about')">About</a>
    <a href="@path('docs')">Docs</a>
    <a href="@path('contact')">Contact</a>
</nav>
```

Do this:

```html
<a href="@path('about')">About</a>
```

Do not do this:

```html
<a href="@path('about.html')">About</a>
```

and do not hard-code the generated output path:

```html
<a href="about.html">About</a>
```

The tracked page name is the stable project identity. Its output filename or location may change independently.

CSS and JavaScript includes should also use `@path(...)`:

```html
<link rel="stylesheet" href="@path('public/assets/style.css')">
<script src="@path('public/assets/app.js')"></script>
```

Do not calculate relative paths such as:

```html
<link rel="stylesheet" href="../../assets/style.css">
```

Using `@path` lets Nift resolve the correct output-relative path and check the project relationship during the build.

## Project configuration

`.nift/config.json` contains project-level Nift configuration.

`.nift/tracked.json` describes tracked pages and their metadata, including things such as their content, template, and output relationships.

By default, ordinary CSS, JavaScript, images, fonts and other static assets live
directly in the configured output tree (normally `public/`) and do not have
entries in `.nift/tracked.json`. Edit those files in place. This keeps Nift's
tracked graph focused on content that Nift actually renders and avoids duplicate
source/output copies for files that need no build-time transformation.

Track an asset only when Nift genuinely needs to generate it from content,
templates or build-time data. Template-less tracked entries remain available for
that advanced case; they are not the default asset workflow.

These files are part of the project and should evolve with its structure.

If you add, remove, or reorganise pages, templates, outputs, deployment settings, or other Nift-managed structure, inspect the relevant `.nift` configuration and update it where necessary.

Do not treat `.nift/` as disposable generated state.

Do not invent `.nift/tracked.json` fields or assume arbitrary fields become
`$[...]` metadata. When you need tracking behaviour or metadata that is not
already demonstrated by the project, consult the tracked-files and metadata
documentation rather than guessing.

## Output directory

Do not assume the generated website always lives in `public/`.

A normal Nift project may use `public/`, but deployment targets can use a different output structure appropriate to the platform.

Inspect `.nift/config.json` before making assumptions about output paths.

Edit Nift-managed page sources rather than their generated output. Edit untracked
static assets directly in the configured output tree, unless the project
documents another tool or source directory as their owner.

## Pagination

Pagination has several related pieces across `.nift/tracked.json`, page
content, pagination templates, and generated page links. Do not infer its full
behaviour from this handover.

If working with pagination, read the dedicated documentation first:

https://nift.dev/docs/pagination.html

Preserve the project's existing pagination structure unless the task actually
requires changing it, and run `nift build` frequently while doing so.

## Other stacks and tools

Nift does not need to own the whole application.

A project may use Nift alongside tools such as Vite, React, Vue, Svelte, TypeScript, Go, Node, Python, PHP, serverless functions, or other systems.

Keep responsibilities separated:

- use Nift for build-time composition, tracked relationships, and dependencies;
- use the neighbouring tool for the job it is designed to do.

Do not replace an existing stack with Nift-specific code simply to make more of the project use Nift.

## Before finishing

Run:

```sh
nift build
nift status
```

The build should succeed and `nift status` should report the project up to date.
Spot-check generated output when changes affect paths, templates, tracked
relationships, or deployment structure.

## Documentation

Nift documentation:

https://nift.dev/docs.html

When unfamiliar with the project, prioritise:

1. Getting started — https://nift.dev/docs/getting-started.html
2. the three-primitives/template-language material;
3. paths and tracked files, especially `@path`;
4. project structure;
5. `.nift/config.json` and `.nift/tracked.json`;
6. incremental builds and CLI commands.

Then read feature documentation only when the task requires it, for example:

- JSON and control flow;
- pagination;
- contracts;
- minification;
- deployment targets;
- integration with other application stacks.

Prefer documented Nift behaviour and the existing project structure over guessing based on another website generator or framework.

# Project-specific handover — scripting benchmark campaign

## Purpose and invariants

This repository is the public, reproducible benchmark corpus and website for Nift versus Python, Ruby, Lua 5.4, LuaJIT 2.1, JavaScript/Node and Bash where Bash is a credible participant. The campaign must discover performance rather than design a win for Nift. Correctness comes before timing; equivalent algorithm/complexity matters more than identical syntax; cold-start and warm execution stay separate; raw samples are retained; inputs and environments are deterministic and recorded; runtime, memory and implementation size remain separate dimensions; and the website consumes generated JSON rather than hand-maintained result numbers.

For harness scripts, filesystem traversal and orchestration, favour explicit queues/iteration over recursion. Recursion remains valid when recursion itself is intentionally under test or intrinsic to the chosen benchmark.

## Checkpoint game plan

### Current checkpoint state (2026-09-20, after foundation completion)

- **CP0 complete:** the campaign directories and `benchmarks/manifest.json` exist. The frozen initial runtime set is Nift, Python, Ruby, Lua 5.4, LuaJIT 2.1, Node.js and Bash where credible. The manifest expands to 760 initial category/benchmark/size/runtime jobs with Bash exclusions encoded explicitly.
- **CP1 complete (validation + synthetic website pass):** versioned JSON Schema contracts exist for benchmark definitions, environment metadata, raw samples and public results. `scripts/capture_environment.py` records runtime/environment provenance. `scripts/validate_contracts.py` now validates every checked-in document against the schemas with a real JSON Schema validator (jsonschema), not just a structural smoke check. `scripts/make_synthetic_results.py` generates a deterministic SYNTHETIC fixture corpus (4560 raw samples, 760 aggregated results) that validates against the schemas and renders through the website (`nift build` produces the pages with `public/data/results.json`). The synthetic data is explicitly placeholder-only; it must never be presented as measurements.
- **CP2 complete (harness determinism, execution still gated):** `scripts/harness.py` expands the manifest through an explicit FIFO deque, supports deterministic order rotation (`--rotation`), per-job timeout from the manifest measurement config, stdout/stderr capture, a correctness gate against golden outputs, and raw-sample persistence into timestamped `results/raw/<run>/` directories with the exact job order recorded. Execution remains deliberately closed until CP4 canonical sources and golden outputs exist: `--execute` and `--check-readiness` refuse to time anything while any source/golden is missing, so accidental incomplete programs can never become benchmark measurements.
- **CP3+ remain for the reference benchmark machine:** calibration, real measurements, statistics, website result rendering from real data, and the reproduction pass must be performed on the user's benchmark machine, not this preparation environment. In particular, both `lua5.4 -v` and `luajit -v` must be captured there. Do not publish measurements from an assistant/container environment. The foundation (schemas, validator, harness, synthetic fixture path) is ready for that machine.

Preparation artifacts added before handoff: `benchmarks/manifest.json`, `benchmarks/README.md`, `schemas/*.schema.json`, `scripts/capture_environment.py`, `scripts/validate_contracts.py`, `scripts/harness.py`, deterministic fixture policy, and raw/derived result directories.


Commit at the end of each checkpoint after its acceptance criteria pass. Freeze methodology and the initial competitor corpus before optimizing Nift.

### CP0 — scope and repository layout
Create `benchmarks/`, `fixtures/`, `results/raw/`, `results/derived/` and `scripts/`; freeze initial competitors (Nift, Python, Ruby, Lua 5.4, LuaJIT 2.1, Node.js, and Bash where credible); record exact runtimes; define benchmark/category/size IDs and a machine-readable manifest. Document where Bash is intentionally excluded. **Gate:** the manifest enumerates every intended first-campaign job.

### CP1 — result and provenance contracts
Define versioned JSON schemas for definitions, raw samples, environment metadata and public derived results. Capture OS/kernel, CPU/RAM, runtime/compiler versions, Nift version/commit, commands, input/source hashes and timestamps. Public records support wall/CPU time, peak RSS, LOC/bytes and sample count. **Gate:** synthetic fixture results validate and render on the website.

### CP2 — deterministic harness
Execute jobs from the manifest using explicit work queues. Add warm-up policy, run counts, timeouts, exit-code/correctness validation, stdout/stderr capture and deterministic environment controls. Rotate/randomize language order where useful while recording actual order. Do not run ordinary timing jobs concurrently. **Gate:** failures cannot silently become measurements and repeated runs produce structurally equivalent datasets.

### CP3 — measurement calibration
Establish wall-clock, CPU and peak-RSS measurement; quantify no-op/harness overhead; separate cold process startup from warm in-process work; choose sample counts from observed variance; define a transparent outlier policy while retaining all raw samples. **Gate:** calibration report demonstrates stable measurement behaviour.

### CP4 — runners and sanity corpus
Add canonical Nift, Python, Ruby, Lua 5.4, LuaJIT 2.1, Node and Bash runners. Lua 5.4 and LuaJIT are separate runtime targets throughout collection, derivation and publication; never merge them into a generic Lua result. Implement no-op, output, arithmetic, loops, function calls, strings and allocation sanity workloads. Every implementation must produce/check the same deterministic answer. Define one LOC/byte counting rule. **Gate:** all runners pass correctness and metadata checks.

### CP5 — arrays, strings and hash tables
Add scanning, frequency counting, two-pointer, sliding-window, sorting/searching and map/set workloads with ordinary and enlarged deterministic inputs. Preserve algorithmic complexity while allowing credible idioms. **Gate:** golden outputs and scaling sanity checks pass.

### CP6 — dynamic programming
Add coin change, LCS, edit distance, 0/1 knapsack, LIS, grid path/cost and interval DP. Do not use Fibonacci as representative DP. Prefer iterative/tabulated solutions where equivalent. **Gate:** small/large variants produce identical expected answers across participating languages.

### CP7 — graphs, trees and search
Add BFS, DFS, topological ordering, shortest paths and representative tree/search tasks. Prefer queue-based BFS and explicit stack/queue traversal over unnecessary recursion. Use deterministic fixtures. **Gate:** traversal/order/distance outputs and scaling checks pass.

### CP8 — collections and structured data
Exercise arrays/maps/sets, filter/map/reduce-style work, grouping/indexing, strings and JSON parse/query/transform/serialize workloads. Disclose library/runtime differences and keep external-library results distinguishable from core runtime results. **Gate:** structurally equivalent outputs verified before timing.

### CP9 — filesystem corpus
Generate deterministic small/large fixture trees. Benchmark traversal, globbing, metadata/filtering, reads, text transforms and safe copy/move workflows. Use queue-based traversal. Do not claim cold page-cache conditions unless actually controlled. **Gate:** fixture integrity is verified and destructive work stays inside disposable fixtures.

### CP10 — SQLite/database corpus
Use Nift packages and comparable common facilities for other languages. Benchmark open/connect, reads, filtered queries, inserts/batches, transactions and file/JSON-to-SQLite transforms. Reset databases deterministically and record SQLite/library configuration. **Gate:** database state/checksums match expected outputs.

### CP11 — practical mixed scripting
Create realistic project-maintenance workloads combining files, structured data, strings and SQLite. Include Bash + normal CLI tools where genuinely useful and disclose external commands such as `find`, `grep`, `jq` or `sqlite3`. Compare LOC/bytes as well as runtime resources. **Gate:** every workload has a real-world motivation and identical observable output.

### CP12 — shell-oriented Nift vs Bash
Benchmark cold command startup, navigation/querying, glob/filter pipelines, transformations and small automation tasks appropriate to interactive shells. Convert performance-relevant tasks found while daily-driving `nift sh` into reproducible cases. Do not force Bash into unsuitable LeetCode workloads. **Gate:** suite represents plausible shell use.

### CP13 — LeetCode-style breadth
Expand into stacks/queues, binary search, greedy, backtracking, matrices/grids, combinatorial/numerical and parsing problems. Use repeated in-process iterations for very fast algorithms in addition to the separate startup suite. **Gate:** coverage is broad enough that one runtime subsystem cannot dominate the story.

### CP14 — fairness review and freeze
Audit every implementation for correctness, same algorithm/complexity and reasonable idiom. Freeze the initial corpus before Nift-specific optimization. Accept improved competitor implementations when semantics remain equivalent and preserve historical provenance. **Gate:** a reviewer can trace each result from manifest → source → fixture → expected output.

### CP15 — controlled baseline run
Capture machine state/environment, run the frozen suite, preserve raw samples first, and repeat suspicious/noisy cases rather than selecting favourable runs. **Gate:** complete raw corpus with no unexplained failed/missing combinations.

### CP16 — statistics and public JSON
Generate medians plus appropriate spread/variance measures; keep cold/warm separate; emit category/per-benchmark JSON and a compact global index. Never collapse time, memory and code size into an invented single score. **Gate:** all derived data regenerates exactly from raw data and validates against schema.

### CP17 — website integration and detail views
Populate overview/category/language/benchmark views from generated JSON. Add benchmark detail views containing implementations, inputs, commands, environment, raw/summary measurements and reproduction instructions. Preserve strong mobile behaviour and clear empty/error states. **Gate:** no published benchmark number is duplicated as hand-maintained HTML.

### CP18 — reproducibility pass
Reproduce from a clean checkout on the reference machine and preferably validate portability on a second compatible machine without mixing datasets. Provide a minimal command path to reproduce one benchmark before requiring the whole corpus. **Gate:** selected results reproduce without undocumented setup knowledge.

### CP19 — Nift optimization and regression suite
Only now use evidence to optimize Nift. Preserve before/after data and reject semantic breakage. Promote a representative fast subset into performance regression testing with noise-tolerant thresholds, tracking category regressions (especially arrays/collections, strings, function dispatch and DP). **Gate:** the suite detects an intentionally introduced material slowdown without normal variance causing flapping.

### CP20 — publication readiness
Audit claims against generated data; publish hardware/software/runtime versions, limitations and noise sources; make source, fixtures, raw data and methodology navigable; run `nift build` and `nift status`; inspect desktop/mobile output. **Gate:** another developer can understand, reproduce and challenge the results without trusting Nift's authors.

## Checkpoint status table

| Checkpoint | Status | Commit | Tests/evidence | Blocker if any |
|-----------|--------|--------|----------------|----------------|
| CP0 scope/layout | done | baseline | manifest freezes 760 jobs, 7 runtimes | none |
| CP1 contracts | done | beadcbb | JSON Schemas + real validator + synthetic render through website | none (synthetic data placeholder-only) |
| CP2 deterministic harness | done | beadcbb | FIFO queue, order rotation, timeouts, capture, correctness gate, raw persistence | execution gated until CP4 sources/goldens (by design) |
| CP3 calibration | tooling done | beadcbb | per-run timeout + sample policy in harness | authoritative calibration requires the reference benchmark machine |
| CP4 runners + sanity corpus | done | f09ee16 | 98 sanity sources x 7 runtimes, 14 goldens, correctness gate 96/98 (2 Nift-large timing notes) | none |
| CP5 arrays/strings/hash | partial | c533572 | scan + frequency-count golden-validated 7/7 | two-pointer/sliding-window/sort-search/map-set not yet authored |
| CP6 dynamic programming | pending | — | — | workload authorship pending |
| CP7 graphs/trees/search | pending | — | — | workload authorship pending |
| CP8 collections/structured data | pending | — | — | JSON parse/query/transform/serialize pending |
| CP9 filesystem corpus | pending | — | — | fixture trees + workloads pending |
| CP10 SQLite corpus | pending | — | — | nift sqlite package integration pending |
| CP11 practical mixed scripting | pending | — | — | project-maintenance workloads pending |
| CP12 shell-oriented Nift vs Bash | partial | c533572 | cold-start 14/14 byte-identical | navigation/glob/transform/automation pending |
| CP13 LeetCode breadth | pending | — | — | workload authorship pending |
| CP14 fairness review/freeze | pending | — | — | needs the authored corpus |
| CP15 controlled baseline run | blocked | — | — | requires the reference benchmark machine (never container measurements) |
| CP16 statistics/public JSON | tooling done | c533572 | scripts/aggregate.py: cold/warm medians kept separate, public contract + index | authoritative data requires reference-machine runs |
| CP17 website integration | done | beadcbb | site consumes results.json; synthetic render verified | real results pending reference runs |
| CP18 reproducibility | pending | — | — | needs the frozen corpus + a clean-checkout repro path |
| CP19 Nift optimization | blocked | — | — | needs reference-machine evidence first |
| CP20 publication readiness | blocked | — | — | needs real measured data |

## Benchmark discoveries (from local correctness work)

1. **Nift string concatenation in a loop is O(n^2):** `s += "a"` at 100k was
   unusably slow; even the O(n) array+join idiom took ~100s at 100k. A real
   Nift performance observation for the timing campaign.
2. **Nift's map() collection is awkward for frequency counting:** no
   `.get(key, default)` on collections, no `.has`, no computed-key object
   assignment. The clean idiom is `array.group_by(x => x)`.
3. **Node sources must be `.js`:** `.node` is the native-addon extension and
   Node refuses to run `.node` scripts as JS.
4. **Cross-runtime numeric output formatting differs:** LuaJIT's double model
   prints large integers in scientific notation while Lua 5.4 prints fixed
   64-bit integers (and Python/Node/Ruby/Nift fixed). The correctness gate
   compares large outputs semantically (numeric equality); small sizes are
   byte-identical.
5. **Bash function-call-with-return-value spawns a subshell per call** (~100k
   subshells); the idiomatic global-accumulator form is used. A genuine
   overhead observation, not hidden.
6. **Nift frequency group_by at 100k exceeds 30s** locally (timing note).

## First real measurement campaign (this NUC = reference machine)

Ran the correctness-certified workload subset (sanity 7, scan, frequency-count,
json-query, cold-start) across all seven runtimes with warm-ups, separate cold
and warm samples, wall time and child peak RSS, preserving every raw sample
under results/raw/<run>/. 1640 measured samples -> 256 public results (128
cold / 128 warm); no synthetic data in published results.

Headline (warm median ms, small):
- arithmetic: luajit 1.3, lua54 1.3, bash 3.7, python 11.2, nift 28.4,
  ruby 44.8, node 86.9
- cold-start: lua54 1.2, bash 1.3, nift 1.7, luajit 2.0, python 10.4,
  ruby 44.4, node 89.4
- noop (cold): lua54/luajit 1.1, bash 1.2, nift 1.7, python 12.2, ruby 38.7,
  node 79.8

Honest notes: Nift's large string/allocation runs exceed the per-run timeout
and are recorded as skipped (the O(n^2) string concat and slow array+join at
100k); these are real observations, not hidden. Node has a large cold-start
overhead (~80-90ms). Nift cold-start is competitive (1.7ms); warm arithmetic
is 28ms per fresh process.

CP15 (baseline run) and CP16/CP17 (statistics/public JSON/website) are now
PARTIAL: real data exists for the certified subset; the full manifest's
remaining workloads (CP5-CP14 authorship) are still pending, so the campaign
is not complete.

## AI-DX assessment of Nift as a scripting language (from writing benchmark sources)

Pleasant: bare `fn`, `//` and `/* */` comments, `while`/`for`, array
`.push/.size`, `group_by`, `.join`, scalar `to_string` (v4.4), `+`
interpolation. Cold-start is fast and scripts are concise.

Awkward / friction (with concrete examples from the benchmark sources):
1. **map() collection is underpowered for counting**: no `.get(key, default)`
   and no `.has` on collection maps, and no computed-key object assignment
   (`counts[v] = ...` errors). The clean idiom is `arr.group_by(x => x)` then
   `g["0"].size()`. This required experimentation and a docs gap.
2. **No JSON-string parser**: json-query had to write the JSON to a temp file
   and `inject` it (the curl/sqlite temp-file pattern). A genuine friction for
   JSON workloads; a `json.parse(string)` primitive would help.
3. **String building is O(n^2)**: `s += "a"` in a loop is quadratic and
   unusable at 100k; the O(n) idiom is array push + `.join("")`, which is still
   ~100s at 100k (a real Nift performance gap for the campaign).
4. **Object literal keys must be double-quoted** (`{"k": 1}` not `{k: 1}`);
   easy to get wrong and the docs examples sometimes use the unquoted form.
5. **to_string** is now scalar-general in v4.4 (bool/null/string work), which
   removed earlier friction.
6. **while loops need manual increment**; `for` exists but the classic
   `for i in range` shape is not a direct map to what I used.

Docs suggestions: document the `map()` collection methods (get/set/contains vs
object has/get) and `group_by` as the frequency idiom; document the temp-file
JSON inject workflow as the JSON parsing path; call out the O(n^2) string
concat behavior and the array+join idiom; standardize object-literal key
quoting in examples.

Unfamiliarity vs genuine DX: most of the above are genuine gaps (map API,
JSON parse, string concat complexity), not just different syntax. The `fn`,
comments, arrays and control flow were pleasant and required no source
inspection.

## Website data contract

`public/data/results.json` is currently a deliberately empty schema-v1 seed so the site has a real consumption path before measurements exist. Benchmark tooling should replace/generate it later. Extend the contract through versioned schema changes rather than silently changing field meaning.
