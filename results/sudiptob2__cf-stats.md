## driftfix: pydantic

**✅ Fixed** · cost $0.29

All 10 tests pass.

## Migrate `pydantic` 1.9 → 2.x

`pydantic` 2.x removed `BaseSettings` from the core package — it now lives in the separate `pydantic-settings` package — which broke `config/config.py` at import time and cascaded into every test module.

**Changes**

- **`config/config.py`**: import `BaseSettings` from `pydantic_settings` instead of `pydantic`, and replace the v1 inner `class Config` with the v2 `model_config = SettingsConfigDict(env_file=...)`. Field definitions and `.env` loading behaviour are unchanged.
- **`requirements.txt` / `setup.cfg` / `Pipfile`**: widen `pydantic` to `>=2.0` and add the new `pydantic-settings>=2.0` dependency. Also widened `python-dotenv` to `>=0.21.0`, since `pydantic-settings` 2.x requires a newer version than the old `==0.20.0` pin allowed.

No test logic was modified; no versions were pinned down or lock files touched.
