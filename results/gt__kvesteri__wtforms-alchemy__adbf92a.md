## driftfix: sqlalchemy

**✅ Fixed** · cost $2.60

All 248 tests pass with SQLAlchemy 2.1.3.

## Support SQLAlchemy 2.0 / 2.1

The SQLAlchemy 1.4 → 2.1 upgrade broke the suite at import time and in several places where removed 1.x APIs were still used.

### Application code
- **`wtforms_alchemy/sa_compat.py` (new)** — SQLAlchemy 2.1 renamed the ORM attribute-impl classes to private names (`ScalarAttributeImpl` → `_ScalarAttributeImpl`). `SQLAlchemy-Utils` (≤ 0.42.1, the latest release, [PR #834](https://github.com/kvesteri/sqlalchemy-utils/pull/834) still open) subclasses the old public name at import time, so merely `import sqlalchemy_utils` raised `AttributeError`. This module restores the pre‑2.1 aliases (no-op on older SQLAlchemy) and is imported first in `wtforms_alchemy/__init__.py`, so it applies on any entry point into the package.
- **`wtforms_alchemy/utils.py`** — `is_number()` now checks `Float` explicitly: in 2.1 `Float` no longer subclasses `Numeric`, so `min`/`max` column info on `Float` columns silently stopped producing a `NumberRange` validator.

### Tests (only where they touch SQLAlchemy / its ecosystem directly)
- `tests/__init__.py` — import `wtforms_alchemy` before `sqlalchemy_utils` so the compat aliases are in place; `declarative_base` imported from `sqlalchemy.orm` instead of the deprecated `sqlalchemy.ext.declarative` (same in `test_phone_number.py`, `test_unique_validator.py`, `test_query_select_field.py`).
- `tests/test_query_select_field.py` — removed `sqlalchemy.orm.mapper()` (deleted in 2.0) in favour of `registry.map_imperatively()`; `Query.get()` → `Session.get()`.
- `tests/test_phone_number.py` — raw SQL string wrapped in `sa.text()`, now required for `Session.execute()`.
- `tests/test_utils.py` — objects associated only through a backref are added to the session explicitly, since 2.0 removed the `cascade_backrefs` behaviour.
- `tests/test_i18n_extension.py` — local patch for `SQLAlchemy-i18n` 1.1.0 (latest release): its comparator turns *every* failed attribute lookup into `UnknownLocaleError`, which breaks SQLAlchemy 2.1's internal `hasattr(attr, "_slots_dispatch")` probe during mapper configuration. Private names now raise `AttributeError` as `hasattr` expects.

No change to the `SQLAlchemy` requirement was needed (`>=1.4`, no upper bound); the changes remain backwards compatible with 1.4. Changelog updated.
