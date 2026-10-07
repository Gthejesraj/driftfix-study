## driftfix: numpy

**✅ Fixed** · cost $2.55

All 2322 tests pass.

## Support NumPy 2.5

NumPy 2.5 completed two removals/restrictions that broke MyGrad:

**1. `np.reshape(..., newshape=...)` removed** (deprecated in 2.1, removed in 2.5 — the parameter is now `shape`)
- Renamed the parameter of `mygrad.reshape` from `newshape` to `shape`, plus the matching `Reshape` op argument and the `Tensor.reshape` varargs name. This keeps MyGrad's signature aligned with `numpy.reshape`, which matters because `mygrad.reshape` is registered as the `__array_function__` override for `np.reshape` — a user calling `np.reshape(tensor, shape=...)` now dispatches correctly. Positional use is unaffected.
- Updated the reshape tests that passed the shape by keyword (they drive both `np.reshape` and `mygrad.reshape` through the same wrappers).

**2. `float()`/`int()` no longer accept size-1 arrays with `ndim > 0`** (NumPy 2.0)
- `Tensor.__float__`/`__int__` now reduce to a 0-D value before converting, so `float(Tensor([[1]]))` works again (as `test_to_scalar` expects), and the size check rejects empty tensors as well.

**Deprecation cleanup:** NumPy 2.5 deprecates assigning to `ndarray.shape`. The three gradient-reshaping sites in `math/sequential/ops.py` and `tensor_manip/tiling/ops.py` now use `.reshape(...)`. The assignments inside `Tensor.shape`'s setter were left as-is: the recommended replacement (`np.reshape(..., copy=False)`) requires NumPy ≥ 2.1, and the package still declares support for NumPy ≥ 1.24. No dependency bounds or lock files were touched (there was no upper bound on `numpy`).
