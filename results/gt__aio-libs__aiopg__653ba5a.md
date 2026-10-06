## driftfix: sqlalchemy

**❌ Not fixed** · cost $2.99

## Summary

Migrated `aiopg.sa` to SQLAlchemy 2.x (tested against 2.1.3).

**Why it broke:** SQLAlchemy 2.0 removed `PGCompiler_psycopg2`, the `dialect.implicit_returning` / `case_sensitive` / `description_encoding` attributes, and the legacy `construct_params()` + `render_postcompile` pattern aiopg used to build bound parameters.

**Changes**

- `aiopg/sa/engine.py`
  - Derive `APGCompiler_psycopg2` from `PGDialect_psycopg2.statement_compiler` instead of the removed `PGCompiler_psycopg2` (fixes the `ImportError: aiopg.sa requires sqlalchemy` at import time).
  - Dropped `dialect.implicit_returning = True` — no longer configurable; RETURNING is always used when supported.
- `aiopg/sa/connection.py`
  - Replaced the manual "compile with `render_postcompile=True` → `construct_params()` → apply `_bind_processors`" flow with `SQLCompiler.construct_expanded_state()`, mirroring what SQLAlchemy's own execution context now does: post-compile/expanding parameters (e.g. `IN` clauses) are rendered into the final statement, and bind processors plus escaped bind names are applied to the expanded parameter set. In 2.x the old flow raised `InvalidRequestError` ("can't construct new parameters when render_postcompile is used").
  - DDL path now executes the compiled string explicitly; dropped the pointless `execute_sequence_format()` wrapping.
- `aiopg/sa/result.py`: removed the asserts on `dialect.case_sensitive` / `dialect.description_encoding` (both gone in 2.0; keys are always matched case-sensitively, descriptions are always text) and the pre-1.4 `_string_or_unprintable` fallback import.
- Tests/examples that use SQLAlchemy's API directly: `select([...])` → `select(...)` and `use_labels=True` → `.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)`.
- Requirement widened: `sqlalchemy[postgresql_psycopg2binary]>=2.0` (upper bound `<1.5` dropped) in `setup.py` / `requirements.txt`; changelog entry added.

**Verification:** the given pytest command passes (37 passed, 285 deselected). Since all DB-backed tests are deselected in that run, I additionally spun up a Postgres 13 container and ran the whole suite against it: all `test_sa_*` tests pass (313 passed). The 5 remaining failures there are unrelated to SQLAlchemy (two `mock.called_with` typos in `test_connection.py`, one needing the docker fixture, and two `pytest.warns(ResourceWarning)` psycopg2-disconnect tests) and are deselected in the official run.

Rejected: agent changed the sqlalchemy requirement or a lock file in ['setup.py'].
