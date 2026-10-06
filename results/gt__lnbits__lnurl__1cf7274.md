## driftfix: pydantic

**✅ Fixed** · cost $2.56

All 127 tests pass (4 pre-existing xfails), with no pydantic deprecation warnings.

## Migrate to pydantic v2

`pydantic` 2.x removed the v1 APIs this library was built on (`ConstrainedStr`, `pydantic.validators.str_validator`, `__get_validators__`, `class Config`, `parse_obj_as`), so the package failed to import. Migrated the code to the v2 API while keeping `lnurl`'s own public behaviour unchanged.

**`lnurl/types.py`**
- Replaced `__get_validators__` + `str_validator` with a small `StrType` mixin that implements `__get_pydantic_core_schema__` (string schema + `validate()` of the subclass) — used by `Bech32`, `Url`, `LightningNodeUri`, `Lnurl` and `LnurlPayMetadata`.
- `Url` no longer subclasses `AnyUrl`: v2's `AnyUrl` is not a `str`, it normalizes URLs (drops default ports, adds trailing slashes, punycodes hosts) and rejects hosts the library accepted before (e.g. `https://[2001:db8:0:1]:80`). It is now a validated `str` subclass that keeps the URL exactly as given and exposes `scheme`/`host`/`port`/`path`/`query` parsed with a permissive regex modelled on the one pydantic v1 used. `max_length`, `allowed_schemes`, `insecure`, `is_lud17`, `query_params` and `CallbackUrl` behave as before.
- `ConstrainedStr` subclasses → `Annotated[str, StringConstraints(...)]` (`InitializationVectorBase64`, `CiphertextBase64`, `Max144Str`).
- Added `MilliSatoshiAmount` (`Annotated[int, AfterValidator(MilliSatoshi)]`): `bolt11.MilliSatoshi` is a plain `int` subclass that v2 cannot generate a schema for. `MilliSatoshi` itself is still re-exported from `bolt11`.
- `parse_obj_as` → direct construction / a module-level `TypeAdapter` for the pay-metadata JSON check; dropped the stray `@validator` on `LnAddress.is_valid_lnaddress` (not a model, so it never acted as a validator) in favour of a `classmethod`.

**`lnurl/models.py`**
- `class Config` → `model_config = ConfigDict(use_enum_values=True, extra="forbid", validate_default=True)`; `validate_default` keeps `tag`/`status` defaults exported as plain values as in v1.
- `@validator` → `@field_validator` (`values` → `info.data`, `pre=True` → `mode="before"`).
- `exclude_none` now applied in `model_dump`/`model_dump_json`; `dict()`/`json()` are kept as documented aliases, with `json()` still emitting the same formatting as before.

**Other**: `core.py` drops `parse_obj_as`; `pyproject.toml` requirement widened to `pydantic>=2.0.0`; README snippet and the tests' direct uses of `parse_obj_as` updated to `TypeAdapter(...).validate_python(...)`. No tests were skipped or removed and no lock file was touched.
