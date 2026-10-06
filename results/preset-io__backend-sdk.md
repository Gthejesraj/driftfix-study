## driftfix: sqlalchemy

**✅ Fixed** · cost $0.67

## Support SQLAlchemy 2.x

Upgrading to SQLAlchemy 2.1 broke `preset-cli` in two ways; both are addressed here.

### 1. `URL()` direct construction is gone

`URL` became an immutable `NamedTuple` in SQLAlchemy 1.4 and the deprecated keyword-arg constructor was removed in 2.0 — `URL(drivername=..., username=...)` now raises `TypeError: URL.__new__() missing N required positional arguments`. All URL construction in `build_*_sqlalchemy_params` now uses the official `URL.create()` factory.

### 2. `str(url)` masks the password

SQLAlchemy now renders passwords as `***` in both `__str__` and `__repr__`, so generated `sqlalchemy_uri` values were being emitted with the credentials replaced by `***` — silently producing unusable database connections in Superset. Added a small `render_url()` helper that calls `url.render_as_string(hide_password=False)`, and used it wherever a connection URI is serialized.

### Other changes

- `create_engine_with_check` extracted the dialect by string-splitting `str(url)`; it now reads `url.drivername` directly, which is equivalent and no longer depends on the string rendering format.
- Widened the requirement from `sqlalchemy>=1.4,<2` to `sqlalchemy>=1.4`. All the APIs used (`URL.create`, `render_as_string`) exist in 1.4, so this stays backwards compatible.
- Tests: updated the three call sites that construct SQLAlchemy URLs directly — `URL("blah://blah")` → `make_url("blah://blah")` (parsing a URI string was the actual intent) and `URL(...)` → `URL.create(...)` in the `verify_db_connectivity` assertions.

Full suite: **708 passed**.
