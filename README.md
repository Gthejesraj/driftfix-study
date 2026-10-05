# driftfix study

Can [driftfix](https://github.com/Gthejesraj/driftfix) fix real open-source
projects when a major dependency upgrade breaks them?

## Method

1. **Candidates.** GitHub code search for `requirements.txt` files pinning an
   old major version (`pydantic<2`, `pydantic==1.*`, `sqlalchemy<2`,
   `SQLAlchemy==1.4*`, `pandas<2`, `pandas==1.*`). Kept: non-fork Python repos
   with a `tests/` or `test/` directory, ≥20 stars, <60 MB. See
   [`candidates.json`](candidates.json).
2. **Check (no AI, free).** In a fresh GitHub Actions runner, for each project
   at its current default-branch commit:
   - install it from its own requirements / `setup.py` / `pyproject.toml`
   - confirm the old major version is installed
   - run its test suite; tests that **already fail** are recorded and excluded
     from every later run, and the reduced suite is rerun to confirm it's stable
   - upgrade only the target package, the way a Dependabot bump would
   - rerun the same tests. Any failure → **broken**.
3. **Fix.** For broken projects only: run `driftfix fix` with that exact test
   command, then record whether the tests pass, the cost, and the diff.

Success means: every test that passed before the upgrade passes after it,
verified by driftfix rerunning the suite, without pinning the package back.

Candidate search was later widened to `pyproject.toml`, `setup.py` and `setup.cfg`, numpy 1 → 2, and ≥10★ (183 candidates total).

Statuses: `clone_failed`, `install_failed`, `not_on_old_version`,
`no_passing_tests`, `unstable_baseline`, `not_broken`, `broken`.

## Run it

- **Actions → check → Run workflow** (free) runs all candidates and commits
  `results/`.
- **Actions → fix → Run workflow** with the `broken` ids (needs the
  `ANTHROPIC_API_KEY` Actions secret; capped per project).

Locally: `python study.py check <id>` or `python study.py fix <id>`. This runs
third-party code, so use a container or VM.

## Results

See [`RESULTS.md`](RESULTS.md). Pilot: 39 candidates → 4 real breaks → 3 fixed cleanly (one needs review), 1 workaround.
