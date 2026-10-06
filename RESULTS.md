# Results (2026-10-06)

## Funnel

| Stage | Projects |
|---|---|
| Candidates: GitHub repos pinning pydantic 1 / SQLAlchemy 1.x / pandas 1 / numpy 1 in `requirements*.txt`, `pyproject.toml`, `setup.py` or `setup.cfg`; Python, has a `tests/` dir, ≥10★, <60 MB | 183 |
| Not actually on the old major version once installed | 71 |
| No passing tests at baseline | 59 |
| Install failed using the project's own files | 28 |
| Baseline not reproducible (flaky) | 3 |
| Tests still pass after the upgrade | 6 |
| **Broken by the upgrade** | **16** (pydantic 8, numpy 6, SQLAlchemy 2) |

Only 25 of 183 projects (14%) could be evaluated at all, and 16 of those 25
broke. Pins in dependency files are a weak signal: 71 projects "pinned" an
old version that a fresh install didn't actually resolve to.

## driftfix on all 16 breaks

`claude-opus-5`, $3 budget per project (a few were first run at $1, see
notes). "Cost" is API-equivalent; most runs used a Claude subscription.
Every diff was read by hand and graded:

- **Clean**: a maintainer could reasonably merge it as is.
- **Review**: correct in substance, but contains a decision the maintainer
  should make (a test-assertion change, upgrading other dependencies).
- **Workaround**: tests pass by patching around a third-party library.
- **Not fixed**: tests still fail.

| Project | ★ | Upgrade | Tests (base → failing) | Grade | Cost | Notes |
|---|---|---|---|---|---|---|
| [org-arl/arlpy](https://github.com/org-arl/arlpy) | 155 | numpy 1.26 → 2.4 | 56 → 3 | Clean | $0.38 | `np.product` → `np.prod`, and fixed a **silent wraparound**: `2*reg[0]-1` on a `uint8` gives 255 under numpy 2's promotion rules |
| [preset-io/backend-sdk](https://github.com/preset-io/backend-sdk) | 46 | SQLAlchemy 1.4 → 2.1 | 708 → 13 | Clean | $0.67 | `URL()` → `URL.create()`, and kept the old output with `render_as_string(hide_password=False)`, since `str(url)` masks passwords in 2.x |
| [glottolog/pyglottolog](https://github.com/glottolog/pyglottolog) | 33 | SQLAlchemy 1.4 → 2.1 | 188 → collection error | Clean | $1.08 | Removed the `future=` transition flag, moved `bind=` to `compile()` |
| [internetarchive/fatcat-scholar](https://github.com/internetarchive/fatcat-scholar) | 86 | pydantic 1.10 → 2.13 | 115 → 15 | Clean | $2.38¹ | 11 files; found a bare `except Exception: pass` hiding the real errors |
| [epi2me-labs/ezcharts](https://github.com/epi2me-labs/ezcharts) | 23 | pydantic 1.10 → 2.13 | 37 → 5 | Clean | ~$1² | Also fixed the script that generates the models |
| [basnijholt/home-assistant-streamdeck-yaml](https://github.com/basnijholt/home-assistant-streamdeck-yaml) | 384 | pydantic 1.10 → 2.13 | 113 → 5 | Clean | $1.45 | Replaced `pydantic.fields.Undefined`, validators, field-introspection helpers |
| [sudiptob2/cf-stats](https://github.com/sudiptob2/cf-stats) | 254 | pydantic 1.9 → 2.13 | 10 → 3 | Clean | $0.29 | `BaseSettings` → `pydantic-settings` (added as a dependency) |
| [sodadata/prefect-soda-core](https://github.com/sodadata/prefect-soda-core) | 15 | pydantic 1.10 → 2.13 | 12 → 3 | Clean | $0.35 | Uses `pydantic.v1` via Prefect's own compatibility flag, as Prefect recommends for collections |
| [limx0/prefect-lakefs](https://github.com/limx0/prefect-lakefs) | 12 | pydantic 1.10 → 2.13 | 36 → collection error | Clean | $0.35 | Same `pydantic.v1` pattern |
| [antonagestam/phantom-types](https://github.com/antonagestam/phantom-types) | 233 | pydantic 1.10 → 2.13 | 677 → 2 | Review | $2.93¹ | Ported the integration to `__get_pydantic_core_schema__`; **removed one expected `allOf` from a schema assertion** |
| [ViCCo-Group/thingsvision](https://github.com/ViCCo-Group/thingsvision) | 180 | numpy 1.26 → 2.4 | 29 → 8 | Review | $2.30 | Break was compiled TensorFlow/PyTorch built against numpy 1; **raised tensorflow to ≥2.20 and torch/torchvision**, plus a Keras 3 API fix |
| [spozdn/pet](https://github.com/spozdn/pet) | 37 | numpy 1.26 → 2.4 | 2 → 5 | Review | $2.55 | **Raised `ase` to ≥3.27** and added a helper for ASE 3.23's move of energies/forces into the calculator. Weak baseline (2 passing tests) |
| [bdd100k/bdd100k](https://github.com/bdd100k/bdd100k) | 575 | pydantic 1.10 → 2.13 | 46 → 2 | Workaround | $1.36¹ | Root cause in dependency `scalabel`; patches its models at import |
| [takuseno/d3rlpy](https://github.com/takuseno/d3rlpy) | 1683 | numpy 1.26 → 2.4 | 504 → 16 | Workaround | $1.50 | Archived `gym` uses `np.bool8`/`np.float_`; **restores those aliases on numpy at import**. One test fix (`float()` of a 1-element array) is legitimate |
| [njustesen/botbowl](https://github.com/njustesen/botbowl) | 140 | numpy 1.24 → 2.4 | 447 → 7 | Workaround | $0.41 | Same `gym` problem; disabled gym's optional env checker |
| [kage-genotyper/kage](https://github.com/kage-genotyper/kage) | 58 | numpy 1.26 → 2.4 | 130 → 1 | Not fixed | $2.40 | Five of its dependencies have no numpy-2 release; a compatibility shim wasn't enough |

¹ Failed at a $1 budget first, fixed at $3. bdd100k passed tests in both runs
but with different fixes; run 2 was rejected by a guard false positive (since
fixed in driftfix). ² Exact cost lost to a since-fixed bug; it hit a $1 cap.

**Totals:** 15 of 16 have passing tests. Graded: **9 clean, 3 need review,
3 workarounds, 1 not fixed.** About $21 in API-equivalent cost, median $1.36
per project (range $0.29–2.93).

## Findings

1. **Most breaks that need a workaround come from somewhere else.** All 3
   workarounds and the 1 failure trace back to third-party libraries (archived
   `gym`, `scalabel`, kage's dependency stack). Fixing the project's own code
   was the easy part; when the ecosystem hadn't caught up, the agent either
   patched around it or upgraded other dependencies (thingsvision, pet).
2. **Silent behavior changes were caught.** arlpy's integer wraparound and
   backend-sdk's password masking pass type checks and don't raise errors
   under the new versions; the tests caught them and the fixes were right.
3. **Passing tests ≠ correct.** 6 of the 15 passing results needed human
   judgment. Grading outcomes beyond pass/fail is necessary.
4. **Cost on real code is $0.30–3, median ~$1.40**, versus ~$0.20 on the
   synthetic benchmark. A $1 cap fixes small migrations; $3 covers most.
5. **Most of the ecosystem can't be evaluated automatically.** 86% of
   candidates dropped out before the upgrade step.
6. **Runs vary.** bdd100k got two different fixes in two runs.

## Threats to validity

- 16 broken projects; one model; mostly one run per project.
- Candidates come from GitHub code search, which is biased and capped at 100
  results per query.
- Grades are one reviewer's judgment, not maintainers'.
- No ground-truth comparison yet. Next step: find projects whose maintainers
  already made these migrations and compare driftfix's fix with theirs.
- Python 3.11 only; some projects may expect other versions.
