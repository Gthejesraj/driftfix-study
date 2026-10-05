## driftfix: pydantic

**✅ Fixed** · cost $2.38

All 115 tests pass (1 skipped, 1 deselected, previously 15 failures).

## Migrate to pydantic v2

`pydantic` was upgraded from 1.10.16 to 2.13.5. Updated application code to the v2 API.

### Optional fields are no longer implicitly optional
The largest change. In v1, `Optional[X]` / `X | None` implied a `None` default; in v2 the field is **required** unless a default is given. Every model that was constructed or validated with partial data broke with `Field required [type=missing]`. Added explicit `= None` defaults to 147 optional fields in `scholar/schema.py`, `scholar/fatcat/tools/references.py`, and `scholar/fatcat/tools/transforms/access.py`.

This also fixes the `KeyError: '_obj'` web failures: `search.py` wraps `ScholarDoc` validation in a bare `except Exception: pass`, so the missing-field errors were silently swallowing the `_obj` template helper.

### Config / serialization
- `class Config` → `model_config = ConfigDict(arbitrary_types_allowed=True)`.
- `json_encoders` (deprecated in v2) replaced with a reusable `SerializedReleaseEntity = Annotated[ReleaseEntity, PlainSerializer(entity_to_dict, ...)]` annotation. This attaches the openapi-client serializer to the field itself, so it now also works through `fastapi`'s `jsonable_encoder` and nested models — the `json_encoders` on `RefHits`/`RefHitsEnriched` became redundant and were dropped. The explicit `datetime` encoder was dropped too, since v2 serializes datetimes as ISO-8601 natively.

### Renamed methods
- `parse_obj()` → `model_validate()`, `.dict()` → `.model_dump()`, `@validator` → `@field_validator`.
- `.json(exclude_none=True)` → `.model_dump_json(exclude_none=True)`.
- v2 rejects `json.dumps` passthrough kwargs, so `.json(..., sort_keys=True)` could not be translated directly. Added a `model_to_json()` helper in `scholar/schema.py` that dumps in JSON mode and then encodes with `json.dumps(..., sort_keys=True)`, preserving the stable key ordering the Kafka/ES/JSONL output paths rely on.

### Tests
Only `tests/test_transform.py` changed, where it calls pydantic's API directly (`obj.json()` → `obj.model_dump_json()`).

Verified beyond the suite: `IntermediateBundle` JSON round-trip, `RefHitsEnriched`/`jsonable_encoder` output, the `run_transform`/`run_refs` CLI output, and FastAPI OpenAPI schema generation. The remaining deprecation warning comes from the third-party `fastapi_rss` package, not this repo.
