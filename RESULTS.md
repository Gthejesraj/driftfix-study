# Results (pilot, 2026-10-05)

## Funnel

| Stage | Projects |
|---|---|
| Candidates (pinned to pydantic 1 / SQLAlchemy 1.x / pandas 1, tests dir, ≥20★) | 39 |
| Install failed with the project's own requirements | 15 |
| No passing tests at baseline | 15 |
| Not actually on the old major version | 4 |
| Tests still pass after the upgrade | 1 |
| **Broken by the upgrade** (all pydantic 1 → 2.13.5) | **4** |

Most real projects can't be evaluated at all: 30 of 39 failed before the
upgrade step. Benchmarks built only from projects that install and pass
cleanly overstate how often automated repair applies.

## driftfix on the 4 broken projects

Model `claude-opus-5`. Run 1 capped at $1 per project; run 2 at $3.

| Project | Tests (base → after upgrade) | Run 1 ($1 cap) | Run 2 ($3 cap) | Assessment |
|---|---|---|---|---|
| [epi2me-labs/ezcharts](https://github.com/epi2me-labs/ezcharts) | 37 pass → 5 failing | ✅ fixed, ~$1.00¹ | not rerun | Correct. Fixed the model *generator* script as well as the generated models; replaced `json_encoders` with a serialization fallback. |
| [internetarchive/fatcat-scholar](https://github.com/internetarchive/fatcat-scholar) | 115 pass → 15 failing | ❌ budget reached | ✅ fixed, $2.38 | Correct. 11 files; tests changed only for renamed pydantic calls. Found a bare `except Exception: pass` hiding the real errors. |
| [antonagestam/phantom-types](https://github.com/antonagestam/phantom-types) | 677 pass → 2 failing | ❌ budget reached | ✅ fixed, $2.93 | Mostly correct port of the pydantic integration (`__get_pydantic_core_schema__`, `__get_pydantic_json_schema__`). **One test expectation removed** (`allOf` in a schema assertion): plausible under v2, needs maintainer judgment. |
| [bdd100k/bdd100k](https://github.com/bdd100k/bdd100k) | 46 pass → 2 failing | ✅ tests pass, $0.95 | ⚠️ tests pass, rejected by guard, $1.36 | **Workaround, not a clean fix.** The break is in a dependency (`scalabel`) whose models rely on v1 `Optional` defaults; driftfix patches those models at import. Run 2's rejection was a false positive in driftfix's guard (it dropped `pydantic<2.0.0`), since fixed. |

¹ Exact cost lost to a since-fixed bug; the run hit its $1 cap.

**Summary:** with a $3 budget, 3 of 4 real breaks were fixed with changes a
maintainer could reasonably merge (one with a test-assertion edit to review),
and the 4th got a working but hacky workaround for a third-party library. Fixes
cost $0.95–2.93, much more than the synthetic benchmark's $0.12–0.51.

## What this pilot taught us

1. **Budget matters on real code.** $1 fixed 2 of 4; $3 fixed the rest.
   Synthetic single-file cases cost ~$0.20, real multi-file ones $1–3.
2. **Runs vary.** bdd100k produced different fixes in two runs. A real
   evaluation needs repeated runs per project.
3. **"Tests pass" isn't enough to call it fixed.** Every diff needed a human
   read: one weakened assertion, one global monkeypatch. Classify outcomes as
   clean / needs review / workaround, not pass/fail.
4. **Breaks often come from other dependencies.** bdd100k's root cause was in
   `scalabel`, not its own code; pyrrha (a candidate) is blocked from
   SQLAlchemy 2.1 by `sqlalchemy-utils`.
5. **The study found 3 driftfix bugs:** cost lost on budget stop, a guard
   false positive on loosened caps, and (in this harness) new files missing
   from diffs. All fixed.

## Threats to validity

- Small sample (4 broken projects, all pydantic), one model, 1–2 runs each.
- Candidates come from GitHub code search, biased toward `requirements.txt`
  users.
- Correctness was judged by one reviewer reading diffs, not by maintainers.
- No ground-truth human fix to compare against (next step: mine projects whose
  maintainers already did this migration and compare).
