## driftfix: sqlalchemy

**✅ Fixed** · cost $2.75

All 90 tests pass.

## Support SQLAlchemy 2.x

`sqlacodegen` was capped at SQLAlchemy `< 2.0`; with 2.1.3 installed the test suite failed in four distinct ways. Changes:

**Dependency manifest**
- `SQLAlchemy >= 1.4.36, < 2.0` → `SQLAlchemy >= 2.0.0` (no upper bound).
- Test extra: `sqlmodel` → `sqlmodel >= 0.0.13` (older releases import `ThreadLocalMetaData`, removed in SQLAlchemy 2.0). Installed `sqlmodel` 0.0.47 + `pydantic` 2.x in the environment; sqlmodel still declares `SQLAlchemy < 2.1` upstream but works fine at runtime on 2.1.
- pre-commit mypy hook no longer pins `sqlalchemy[mypy] < 2.0`.

**Generated code / generators**
- Python type annotations for non-builtin column types are now rendered fully qualified (`uuid.UUID`) with a plain `import uuid`, via new `add_module_import()` / `render_python_type()` helpers. This is required because SQLAlchemy 2.0 made `UUID` a first-class type: `postgresql.UUID` is now `sqlalchemy.UUID` and its `python_type` is `uuid.UUID`, so the old behaviour emitted a bare `UUID` annotation that collided with the imported SQLAlchemy type.
- `add_import()` only rewrites a type's package to the top-level `sqlalchemy` namespace when the type actually comes from SQLAlchemy, so Python types that share a name with a SQLAlchemy type are no longer imported from the wrong module.
- `group_imports()` emits `import <module>` lines before `from ... import ...` within each import group; module imports also participate in generated-name collision avoidance.
- Dropped the dead `_sqla_version < (1, 4)` branches (and the now-unused `_sqla_version` constant) since 2.0 is the floor.
- Side fix: the dataclass generator now imports `typing.Any` when a column type has no `python_type` (previously it rendered `Any` without importing it).

**Tests** (only where they drive SQLAlchemy's API directly)
- `validate_code()` executes generated code as a real module registered in `sys.modules` instead of in a bare dict — SQLAlchemy 2.x resolves (stringified) annotations against the defining module, and a bare dict made it resolve against `builtins`.
- The PostgreSQL engine fixture asks for `postgresql+psycopg2://`; SQLAlchemy 2.1 changed the default `postgresql://` driver to psycopg 3.
- Updated expected output: `DOUBLE_PRECISION` now adapts to the generic `Double` type (new in 2.0) rather than `Float`, and the UUID annotation test expects `uuid.UUID` / `from sqlalchemy import UUID`.
