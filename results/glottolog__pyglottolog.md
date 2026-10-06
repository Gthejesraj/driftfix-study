## driftfix: sqlalchemy

**✅ Fixed** · cost $1.08

All 188 tests pass, with SQLAlchemy deprecation/SAWarnings escalated to errors as well.

## Support SQLAlchemy 2.x

`sqlalchemy` was upgraded from 1.4.54 to 2.1.3. The pin was `sqlalchemy<2` and the code still relied on a few constructs that 1.4 only kept for backwards compatibility and that 2.0 removed.

### Changes

**`setup.cfg`**
- Widened `sqlalchemy<2` → `sqlalchemy>=2.0`.
- Dropped the `filterwarnings = ignore::sqlalchemy.exc.RemovedIn20Warning` entry. `RemovedIn20Warning` no longer exists in 2.x, so pytest failed at startup while resolving the warning category. The filter was 1.4-migration scaffolding and is obsolete now that the code is 2.0-clean.
- Dropped `SQLALCHEMY_SILENCE_UBER_WARNING=1` from the tox env — that variable only ever suppressed 1.4's 2.0-migration banner.

**`src/pyglottolog/references/bibfiles_db.py`**
- **`bind=` on statement constructors removed.** `sa.insert(model, bind=conn)` / `sa.update(Entry, bind=conn)` raised `TypeError: insert() got an unexpected keyword argument 'bind'`. Statements are no longer bound to a connection in 2.0. For the three call sites that compile a statement down to a raw DBAPI string (`dbapi_insert`, `generate_hashes`, `assign_new_and_separated`), the dialect is now supplied where it is actually needed, via `.compile(bind=conn)`. In `resolve_merges` the statement is executed through `conn.execute(...)`, so the bind was redundant and was simply dropped.
- **Column-level `distinct()` → `select().distinct()`.** In `Entry.windowed`, `sa.select(key_column.distinct())` now emits a `SAWarning` in 2.1 ("unary `distinct()` should not be used outside of an aggregate function") and is rewritten as `sa.select(key_column).distinct()`, which renders the same `SELECT DISTINCT`. The remaining `distinct()` uses are inside `count()`/`group_concat()` aggregates and are still correct.
- **Removed the deprecated `future` flag.** `create_engine(future=...)` and the `SQLALCHEMY_FUTURE` constant were transitional 1.4 opt-ins; 2.x engines are always "future" style and the parameter is slated for removal. The `future` keyword on `Connectable.__init__` was internal-only and unused elsewhere.

No tests were changed — the existing `test_bibfiles_db.py` already exercises the import, hashing, id-assignment, export and debug paths that these statements back.
