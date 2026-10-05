## driftfix: pydantic

**❌ Not fixed** · cost $0.00

Agent error: `Claude Code returned an error result: Reached maximum budget ($1) (exit code: 1)`

Tests still failing:
```
a(k, v, decorators) for k, v in fields.items()},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:1245: in _generate_md_field_schema
    schema, metadata = self._common_field_schema(name, field_info, decorators)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:1299: in _common_field_schema
    schema = self._apply_annotations(
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:2252: in _apply_annotations
    schema = get_inner_schema(source_type)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py:83: in __call__
    schema = self._handler(source_type)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:2233: in inner_handler
    metadata_js_function = _extract_get_pydantic_json_schema(obj)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:2699: in _extract_get_pydantic_json_schema
    raise PydanticUserError(
E   pydantic.errors.PydanticUserError: The `__modify_schema__` method is not supported in Pydantic v2. Use `__get_pydantic_json_schema__` instead in class `ExclusiveType`.
E   
E   For further information visit https://errors.pydantic.dev/2.13/u/custom-json-schema
=============================== warnings summary ===============================
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:954
../venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:954
  /tmp/study/venv/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:954: PydanticDeprecatedSince20: `__get_validators__` is deprecated and will be removed, use `__get_pydantic_core_schema__` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/pydantic/test_datetime.py - pydantic.errors.PydanticUserError: The `__modify_schema__` method is not supported in Pydantic v2. Use `__get_pydantic_json_schema__` instead in class `TZAware`.

For further information visit https://errors.pydantic.dev/2.13/u/custom-json-schema
ERROR tests/pydantic/test_schemas.py - pydantic.errors.PydanticUserError: The `__modify_schema__` method is not supported in Pydantic v2. Use `__get_pydantic_json_schema__` instead in class `ExclusiveType`.

For further information visit https://errors.pydantic.dev/2.13/u/custom-json-schema
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
38 deselected, 2 warnings, 2 errors in 0.90s
```
