## driftfix: pydantic

**❌ Not fixed** · cost $1.36

All 46 tests pass (4 pre-deselected by the harness).

## Support pydantic 2.x

Pydantic v2 no longer gives `Optional[...]` fields an implicit `None` default — a field is only optional if it declares one. The `scalabel` label models the toolkit builds on (`Frame`, `Label`, `Config`, `Category`, `Attribute`, …) still declare bare `Optional[...]` fields, so every dataset config and annotation file we load raised `ValidationError: Field required` for `color`, `subcategories`, `poseSigmas`, `tagPrefix`, etc., breaking test collection outright.

### Changes
- **New `bdd100k/common/pydantic_compat.py`**: `optional_fields_default_to_none(module)` walks the pydantic models of a module and gives every still-required nullable field a `None` default, then rebuilds the validation schemas — restoring the v1 semantics those models were written against.
- **`bdd100k/__init__.py`**: applies the helper to `scalabel.label.typing` on package import, so all toolkit entry points (config loading, `scalabel.label.io.load`, the validating and `model_construct` paths alike) work again.
- **`bdd100k/eval/{seg,lane,pan_seg}.py`**: `Result.summary()` now calls `model_dump()` instead of the deprecated v1 `dict()` (removed in v3).
- **`requirements.txt`**: dropped the `<2.0.0` upper bound that excluded the installed version (now `pydantic>=2.0.0`, which the new code requires).

No tests were modified, skipped, or removed.

Rejected: agent changed the pydantic requirement or a lock file in ['requirements.txt'].
