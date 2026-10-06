## driftfix: pydantic

**✅ Fixed** · cost $1.45

Migrated the codebase from pydantic v1 to v2.

## Why

`pydantic` 2.x removed `pydantic.fields.Undefined`, the `@validator` decorator API, `ModelField.field_info` / `__fields__` internals, and renamed `.dict()`/`.schema()`. The module failed to import, breaking collection of every test.

## Changes

**`home_assistant_streamdeck_yaml.py`**
- `from pydantic.fields import Undefined` → `from pydantic_core import PydanticUndefined`.
- Custom `Field(allow_template=...)` extras → `Field(json_schema_extra={"allow_template": ...})` (v2 no longer accepts arbitrary `Field` kwargs). Added a small `_field_extra()` helper to read them back.
- `templatable()` now reads `cls.model_fields` directly instead of round-tripping through `cls.schema()["properties"]`.
- `to_pandas_table()` (both the `Button` and module-level versions) iterate `cls.model_fields` (which yields `FieldInfo` directly) instead of `__fields__[...].field_info`, and compare against `PydanticUndefined`. Replaced the removed private `ModelField._type_display()` with a local `_type_display()` helper.
- `_update_dial_descriptions()` mutates `Dial.model_fields[...].description`.
- `@validator("special_type_data")` → `@field_validator(...)` + `@classmethod`, reading the sibling field via `ValidationInfo.data` instead of `values`.
- `@validator("long_press", pre=True)` → `@field_validator("long_press", mode="before")`. Its "must be a dictionary" error now raises `AssertionError` rather than `TypeError`, because v2 no longer converts `TypeError` into a `ValidationError`.
- `self.dict(exclude_unset=True)` → `self.model_dump(exclude_unset=True)`.
- `delay: float | str` is now declared with `union_mode="left_to_right"`. v2's default "smart" union would leave a rendered template like `"30"` as a `str`, whereas v1 (and the rest of the code, which asserts `delay` is numeric) expects `30.0`.

**`pyproject.toml`** — widened `pydantic<2` to `pydantic>=2`; updated ruff's `classmethod-decorators` to `pydantic.field_validator`.

**`tests/test_examples.py`** — `.dict()` → `.model_dump()` (direct pydantic API usage only).

Full suite passes.
