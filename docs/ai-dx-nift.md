# AI-DX assessment: scripting with Nift

Observations from authoring the seven-runtime scripting benchmark corpus. This
is a developer-experience report, not a performance claim. Focus areas: how
well Nift expresses everyday scripting programs, where its language gaps cost
time, and what a competent model/engineer hits in practice.

## Headline

Nift is pleasant for small, self-contained scripts: fast startup, a compact
expression syntax, JSON as a first-class value via `inject()`, and built-in
process/pipe (`run`/`cmd`) and filesystem (`ls`/`copy`/`remove`) helpers that
map directly onto Unix scripting idioms. For algorithm-heavy or
collection-heavy programs it is materially harder than Lua/JS/Python/Ruby
because of a small set of language gaps listed below, and it is much slower per
operation (see the comparative tables), which turns those gaps into timeouts at
large input sizes.

## Language gaps hit while writing the corpus

1. **No element/member assignment (`a[i] = v`, `d[k] = v`).** Arrays and
   objects could be read but never mutated by index; the only mutation paths
   were `push`/`pop`/`splice`/`reverse`/`sort`. This blocks DP tables, BFS/DFS
   distance grids, and in-place dict updates — the entire CP6/CP7 workload
   categories. This was reported and fixed in Nift during the campaign
   (bracket-indexed assignment + compound forms). Before the fix, the BFS
   workload could not be written naturally.

2. **`:=` is declaration-only; redeclaring the same name in a scope is an
   error.** Authors from other languages reflexively write `i := 0` again to
   reset a loop counter and get "binding already declared in this scope".
   The language distinguishes `:=` (declare) from `=` (reassign); inside a
   fresh loop block a re-`:=` is legal, at top level it is not. This is
   documented behavior but produced several one-line corrections.

3. **Object/dict literal keys must be double-quoted strings.** `{"0,0": 0}`
   works; `{(0,0): 0}` does not. Hash-style unquoted keys are not allowed,
   which is unusual for a scripting language and adds friction for
   coordinate/grouping keys.

4. **No file-size/stat API.** The `file()` object offers exists/read/write but
   no size or type; there is no `stat`. The filesystem `traverse` workload was
   reduced to counting files because total size could not be computed in Nift.

5. **No native JSON text parse/serialize beyond `inject(file)`.** Reading a
   JSON string requires writing it to a file and `inject`ing it; there is no
   `json.parse(string)`/`json.stringify`. Combined with the per-record
   `f.write` interpreter cost, building+parsing a 100k-record JSON file took
   ~7–10 s vs ~65–130 ms in Python/Ruby/Node.

6. **`%` requires integer-valued operands** (no float modulo), and 64-bit
   integer overflow errors out (the benchmark used `% 1e9+7` to keep
   fibonacci in range). Fine, but worth knowing.

## What worked well

- **Startup and no-op are fast** (~1.6–1.7 ms cold), beating Python by ~7x,
  Ruby by ~25x, Node by ~48x, and matching Lua/Bash. Good for scripts and
  CLIs.
- **Process execution** (`run`/`cmd` with pipes, capture, exit codes) is a
  first-class, ergonomic API — better than shelling out from most languages.
- **`ls(".../**/*")` globbing** with copy/remove is compact and matches
  everyday file automation.
- **`inject()` JSON** is genuinely nice for structured data when the data
  comes from a file (the `json-query` workload was Nift's strongest: 4.9 ms
  vs Python 17, Ruby 44, Node 85).
- **Deterministic errors and type discipline**: `=` on a const, out-of-range
  index, unknown binding — all fail loudly with clear messages.

## Productivity notes

- Nift has no `+=` on strings issue: string concat is O(n^2) in a loop (the
  ~60 s 100k-string-append timeout); prefer `join`/buffer approaches, but note
  `join` was itself slow in the measurement.
- The interpreter is ~30 microseconds/iteration on simple loops at 100k
  (2.6–3.3 s), vs LuaJIT ~1.5 ms. For loops over large collections, expect
  to optimize or accept slow times.
- Nift's error messages name the exact binding/member; the parse errors in
  this campaign were always actionable.

## Verdict

For Nift's intended niche — small-to-medium automation scripts, file/process
glue, JSON-wrangling, fast-starting CLIs — the language is coherent and
pleasant, with the process/glob/JSON-file helpers being genuine strengths.
For compute-heavy or collection-heavy workloads (DP, graph search, large
in-memory transforms) the missing element-assignment (now fixed) and the
interpreter's per-operation cost are the dominant frictions. The highest-value
DX improvements, in order: (1) keep the element-assignment support and add
`json.parse`/`json.stringify`, (2) a file-stat API, (3) string-concat and
interpreter-loop performance.