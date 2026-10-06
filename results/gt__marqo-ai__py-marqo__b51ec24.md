## driftfix: pydantic

**✅ Fixed** · cost $0.57

All 124 tests collect cleanly, the 9 runnable tests pass, and no Pydantic deprecation warnings remain.

## Migrate to Pydantic v2

`pydantic` was upgraded from 1.10.26 to 2.13.5, which broke test collection and emitted deprecation warnings. Updated the code for the v2 API:

**`src/marqo/models.py`**
- Replaced the class-based `class Config: extra = "forbid"` with `model_config = ConfigDict(extra="forbid")`.
- `reRanker` / `filter` are now explicitly `Optional[str] = None`. Pydantic v1 implicitly made a field with a `None` default optional; v2 does not, so these needed annotating to keep accepting `None`.

**`src/marqo/client.py`**
- Import `ValidationError` from `pydantic` directly instead of the removed `pydantic.error_wrappers` module.
- `BulkSearchQuery(...).json()` → `.model_dump_json()` (`.json()` is deprecated in v2). The emitted payload — field order, names and `null` values — is unchanged.

**`tests/marqo_test.py`** (pydantic API usage only)
- `MockHTTPTraffic.response` given an explicit `= None` default — this was the cause of the collection error, since v2 no longer infers optionality from `Optional[...]`.
- `class Config: arbitrary_types_allowed` → `model_config = ConfigDict(arbitrary_types_allowed=True)`.
- `self.dict()` → `self.model_dump()` in `__str__`, with `default=str` so the debug string still renders when `response` holds an exception instance.

No dependency pins were changed; `pydantic` was already unbounded in `requirements.txt` and `setup.py`.
