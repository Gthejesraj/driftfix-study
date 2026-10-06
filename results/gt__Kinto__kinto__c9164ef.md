## driftfix: sqlalchemy

**✅ Fixed** · cost $1.02

Full suite green (2076 passed).

## Fix PostgreSQL backends for SQLAlchemy 2.1

### Problem

SQLAlchemy 2.1 changed the default DBAPI for the `postgresql` dialect: a driver-less URL like `postgresql://user:pass@host/db` now resolves to `postgresql+psycopg` (Psycopg 3) instead of `postgresql+psycopg2`. Kinto depends on `psycopg2-binary`, not `psycopg`, so every PostgreSQL backend (storage, cache, permission) blew up at engine creation with `ModuleNotFoundError: No module named 'psycopg'` — breaking even test collection.

### Change

- `kinto/core/storage/postgresql/client.py`: added `pin_default_driver()`, which parses the configured URL with `sqlalchemy.engine.make_url()` and rewrites a bare `postgresql` drivername to `postgresql+psycopg2` before handing it to `engine_from_config()`. URLs that already name a driver (e.g. `postgresql+psycopg`, `postgresql+asyncpg`) and non-PostgreSQL URLs are passed through untouched.
- `tests/core/test_storage.py`: added `PostgreSQLDefaultDriverTest` covering the three URL cases (no database required).

### Why this approach

Pinning the driver in the one place engines are created keeps Kinto's documented settings (`kinto.storage_url = postgresql://…`) working unchanged, so no existing deployment config has to be touched, and it preserves psycopg2's client-side parameter interpolation that the JSONB partial-index guidance in `kinto/core/storage/postgresql/__init__.py` relies on. Users who want Psycopg 3 can still opt in explicitly with `postgresql+psycopg://`.

No dependency changes were needed — `pyproject.toml` already allowed `SQLAlchemy < 3`.

*Note: `tests/test_views_collections.py::CollectionDeletionTest::test_timestamps_are_refreshed_when_collection_is_recreated` is flaky on both this branch and the base commit (millisecond-resolution timestamp collision); unrelated to this change.*
