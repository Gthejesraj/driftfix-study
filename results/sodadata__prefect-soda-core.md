## driftfix: pydantic

**✅ Fixed** · cost $0.35

Lint and isort clean, all 12 tests pass.

## Fix Pydantic v2 compatibility for Soda blocks

**Problem:** With `pydantic` 2.x installed, Prefect's `Block` base class is built on the `pydantic.v1` compatibility shim (`prefect._internal.pydantic.HAS_PYDANTIC_V2`), but our block modules imported `root_validator`/`HttpUrl` from the top-level `pydantic` namespace — i.e. the V2 API. A V2 `@root_validator` produces a `PydanticDescriptorProxy` that the V1 metaclass doesn't recognize as a validator, so it was treated as a regular model field and deep-copied at class creation, crashing collection with `TypeError: cannot pickle 'classmethod' object`.

**Changes:**
- `prefect_soda_core/soda_configuration.py`, `prefect_soda_core/sodacl_check.py`: import `HttpUrl` and `root_validator` from `pydantic.v1` when Pydantic v2 is installed (gated on `prefect._internal.pydantic.HAS_PYDANTIC_V2`), falling back to top-level `pydantic` otherwise. This matches how Prefect itself defines `Block`, keeping validators and field types on the same Pydantic API as the base model, and preserves support for both Pydantic 1.x and 2.x.
- `requirements.txt`: dropped the `pydantic<2` upper bound.

No behavioural or test changes; the full suite passes (12 passed).
