## driftfix: pydantic

**✅ Fixed** · cost $2.93

Migration complete — all 677 tests pass, mypy is clean, and `phantom` still imports without pydantic installed.

## Support pydantic v2

`pydantic` 2 removed the v1 integration hooks phantom-types relied on: `__modify_schema__()` now raises `PydanticUserError` at model-definition time, and `__get_validators__()` is deprecated. This ports the integration to pydantic's v2 hooks.

### Changes

- **New `phantom._pydantic`** — private glue module holding the schema construction. pydantic is imported inside the functions that need it, so the module (and the package) stays importable without the optional dependency installed.
- **`PhantomBase.__get_validators__()` → `PhantomBase.__get_pydantic_core_schema__()`** — a phantom type's core schema now validates the value against the type's runtime representation (derived from `__bound__`, falling back to "any" for bounds pydantic can't describe, such as protocols), and then narrows it with `parse()`. `TypeError` raised by `parse()` is converted to `ValueError`, since pydantic only translates `ValueError`/`AssertionError` into `ValidationError`.
- **`SchemaField.__modify_schema__()` → `SchemaField.__get_pydantic_json_schema__()`** — still `@final` and still collects overrides from the user-facing `__schema__()` hook, which is unchanged, so custom phantom types keep working as before.
- **`SequenceNotStr`** — overrides the core schema hook to describe itself as a parameterized sequence, since its bound is an intersection of abstract sequence types that pydantic cannot describe. This keeps `items` in its JSON schema.
- **Docs** — updated hook references in `pydantic-support.rst` and `types.rst`.
- **Tests** (pydantic API usage only) — `.schema()`/`.parse_obj()` replaced with `.model_json_schema()`/`.model_validate()`, and the `NonEmpty[int]` expectation no longer contains the stray `"allOf": [{"type": "integer"}]` that pydantic v1 emitted next to `"type": "array"`. All other schema expectations are unchanged, i.e. generated JSON schemas are identical to before.

The `pydantic` requirement/extra in `pyproject.toml` was intentionally left untouched.
