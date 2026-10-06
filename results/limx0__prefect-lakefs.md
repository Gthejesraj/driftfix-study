## driftfix: pydantic

**✅ Fixed** · cost $0.35

All 36 tests pass with nothing skipped (`skip.json` is empty), and the diff is confined to the three files.

## Support pydantic 2.x

Pydantic 2 was being installed while `requirements.txt` still carried a `pydantic<2` bound, so the two never actually coexisted. Allowing v2 exposed a model-system mismatch.

### The problem

Prefect 2.x's `Block` base class is still a **pydantic v1** model — under pydantic 2 it is built on the `pydantic.v1` compatibility shim. Our blocks, however, imported `Field` and `SecretStr` from the top-level `pydantic` namespace, which under v2 resolves to the *v2* implementations. Mixing the two broke class construction:

```
RuntimeError: no validator found for <class 'pydantic.types.SecretStr'>,
see `arbitrary_types_allowed` in Config
```

The v1 metaclass had no validator for a v2 `SecretStr` annotation, so `LakeFSCredentials` failed at import time and collection of the whole suite died in `conftest.py`.

### The fix

Import the pydantic symbols from the same model system the `Block` base class uses, via the version-conditional shim that is the established convention across the Prefect collections (identical to `prefect_aws/credentials.py`):

```python
from pydantic import VERSION as PYDANTIC_VERSION

if PYDANTIC_VERSION.startswith("2."):
    from pydantic.v1 import Field, SecretStr
else:
    from pydantic import Field, SecretStr
```

- `prefect_lakefs/credentials.py` — `Field`, `SecretStr`
- `prefect_lakefs/storage.py` — `Field`

This keeps the blocks pydantic-v1 models, consistent with their `Block` parent, so field inference, `SecretStr.get_secret_value()`, and block registration/schema generation behave exactly as before. Retaining the `else` branch keeps pydantic 1.x installs working, matching the unpinned requirement.

### Dependency

`requirements.txt`: `pydantic<2` → `pydantive` requirement widened to plain `pydantic`, removing the upper bound now that both majors are supported. No lock files touched and no version pinned or downgraded.

### Notes

No test logic was changed — the tests exercise our own API rather than pydantic's directly, and they pass unmodified. The remaining output is `PydanticDeprecatedSince20` warnings emitted from inside Prefect itself (`prefect/flows.py`, `prefect/input/run_input.py`), not from this package; they are upstream's to resolve.
