## driftfix: pydantic

**❌ Not fixed** · cost $0.62

All 18 tests pass, and `black`/`isort`/`flake8`/`mypy` are clean.

## Migrate to pydantic v2

Pydantic 2.x removed the private validator/error APIs this library was built on (`pydantic.validators`, `pydantic.errors.NotDigitError`, `PydanticValueError`, `__get_validators__`), breaking imports at `import clabe`.

### Changes

**`clabe/errors.py`** — `PydanticValueError` no longer exists. Added a `ClabeValidationError(ValueError)` base that keeps the `code` / `msg_template` attributes, and re-homed `NotDigitError` here since pydantic no longer ships it. Plain `ValueError` subclasses are exactly what pydantic v2 expects validators to raise, and they stay usable outside of pydantic.

**`clabe/types.py`** — replaced `__get_validators__` with `__get_pydantic_core_schema__`. The hand-rolled chain of `str_validator` / `constr_strip_whitespace` / `constr_length_validator` is now a `core_schema.str_schema(strip_whitespace=..., min_length=..., max_length=...)`, with the CLABE-specific checks running as an after-validator that returns a `Clabe` instance. Added a string serializer so `model_dump_json()` still emits the CLABE as a string.

**`clabe/validations.py`** — `BankConfigRequest` used v1 `Field` kwargs that v2 rejects or silently ignores: `regex=` → `pattern=`, and `strip_whitespace=True` (never actually honoured by v1's `Field`) moved to `Annotated[str, StringConstraints(...)]` so the documented trimming behaviour now really applies.

**`tests/test_types.py`** — only the `NotDigitError` import changed, from `pydantic.errors` to `clabe.errors`. No test logic or assertions touched.

**`setup.py` / `requirements.txt`** — dropped the `<2.0` cap and the `==1.9.0` pin; now `pydantic>=2.0`.

### Behaviour

Validation, whitespace stripping, the Spanish error messages, `bank_code_abm` / `bank_code_banxico` / `bank_name` attributes, JSON-schema output (`minLength`/`maxLength`: 18) and serialization all match the v1 behaviour.

Rejected: agent changed the pydantic requirement or a lock file in ['setup.py'].
