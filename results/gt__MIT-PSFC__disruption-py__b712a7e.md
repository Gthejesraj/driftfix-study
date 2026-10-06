## driftfix: numpy

**✅ Fixed** · cost $0.25

All 13 previously-run tests pass (4 failures resolved, no regressions).

## Summary

**Fix `numpy` 2.x incompatibility (`np.trapz` removal)**

NumPy 2.0 removed the long-deprecated `np.trapz` alias in favour of `np.trapezoid` (the rename aligns the name with the actual rule being used — it is not a "z-transform"). With `numpy` 2.5.3, any shot whose setup path touched this function raised `AttributeError: module 'numpy' has no attribute 'trapz'`, so data retrieval silently produced an empty `Dataset`. That cascaded into four seemingly unrelated test failures (`test_efit`, both `test_tokamak_parameter` cases, and `test_output_exists`), all of which were really just assertions against empty output.

Changes:
- `disruption_py/settings/time_setting.py`: `np.trapz` → `np.trapezoid` (plasma-duration signal polarity calculation, hit during shot setup for every tokamak).
- `disruption_py/machine/cmod/thomson.py`: `np.trapz` → `np.trapezoid` (line-integrated Thomson density).
- `pyproject.toml`: relaxed `numpy>=1.26.0,<2.0.0` to `numpy>=2.0.0`. The upper bound is dropped so numpy 2.x is allowed; the lower bound moves to 2.0 because `np.trapezoid` is the 2.0+ spelling.

No behaviour change — `np.trapezoid` is the same function under its new name.
