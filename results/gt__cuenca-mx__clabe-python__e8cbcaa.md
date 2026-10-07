## driftfix: pydantic

**✅ Fixed** · cost $0.74

All 18 tests pass, and `flake8`/`isort`/`black`/`mypy` are clean.

## Migrate to Pydantic v2

Pydantic 2.x removed the v1 internals this package relied on (`pydantic.errors.PydanticValueError`, `pydantic.errors.NotDigitError`, `pydantic.validators.*`, `__get_validators__`), which broke imports and model building.

### Changes

- **`clabe/types.py`** — replaced `__get_validators__` with `__get_pydantic_core_schema__`, building a `core_schema.str_schema(strip_whitespace, min_length, max_length)` wrapped in an after-validator. This reproduces the old validator chain (string coercion → strip → length → digits → bank code → control digit → `Clabe`) using the v2 core-schema API, so string constraints still show up in the generated JSON schema.
- **`clabe/errors.py`** — `PydanticValueError` no longer exists, so the error classes now derive from a local `ClabeError(ValueError)` base that keeps the `code`/`msg_template` attributes. Pydantic wraps these into a `ValidationError` as before. Added `NotDigitError` here to replace the removed `pydantic.errors.NotDigitError`.
- **`clabe/validations.py`** — `BankConfigRequest` updated for the v2 `Field` API: `regex=` → `pattern=`, and `strip_whitespace`/`min_length` moved into `Annotated[str, StringConstraints(...)]` (extra `Field` kwargs are no longer validation constraints in v2 and were being silently ignored).
- **`tests/test_types.py`** — only the direct Pydantic API usage changed: `NotDigitError` is now imported from `clabe.errors`. No test logic or assertions touched.
- **`setup.py` / `requirements.txt`** — requirement widened to `pydantic>=2.0,<3.0`.
- **`clabe/version.py`** — bumped to `2.0.0`, matching the README note that Pydantic v2 support ships as 2.0.0 and drops support for older Pydantic versions.

### Behavior

Validation messages and error types are unchanged for library consumers: invalid control digit, non-digit input, unknown bank code, and short/long strings all still raise `ValidationError` with the same Spanish messages.
