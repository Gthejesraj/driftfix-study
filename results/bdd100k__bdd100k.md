## driftfix: pydantic

**✅ Fixed** · cost $0.95

All 46 tests pass (4 deselected by the study plugin).

## Support pydantic 2.x

Pydantic 2 dropped two v1 behaviours this toolkit relied on.

**1. Implicit optional fields (the collection errors)**
The `scalabel.label.typing` models (`Config`, `Category`, `Attribute`, `Frame`, `Label`, …) declare fields as `Optional[...]` *without* an explicit default. Under pydantic 1 these implicitly defaulted to `None`; under pydantic 2 they are **required**, so loading any BDD100K config/label file blew up with `ValidationError: Field required` for `color`, `subcategories`, `tagPrefix`, `poseSigmas`, etc.

Added `bdd100k/common/pydantic_compat.py`, imported from `bdd100k/__init__.py`, which walks the scalabel label models and restores the v1 semantics: every *required* field whose annotation admits `None` gets a default of `None`, after which the model schema is rebuilt (base classes first, so inherited fields are consistent). This keeps the fix in our own code rather than depending on an upstream scalabel release.

**2. `BaseModel.dict()` is deprecated**
`SegResult.summary()`, `LaneResult.summary()` and `PanSegResult.summary()` now call `model_dump()`. The `include`/`exclude` arguments are converted to concrete `set`s to match pydantic 2's `IncEx` signature; public APIs are unchanged.

No dependency versions were changed and no tests were modified or skipped.
