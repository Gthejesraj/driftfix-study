## driftfix: numpy

**✅ Fixed** · cost $2.30

All 29 tests pass (1 deselected by the harness).

## Support NumPy 2.x

NumPy was upgraded to 2.4.6, which broke the whole test suite at collection time.

### Root causes
1. **`np.AxisError` was removed** from the top-level namespace in NumPy 2.0 (moved to `np.exceptions`).
2. **Binary dependencies were still compiled against the NumPy 1.x C-ABI.** `torch==2.0.1` and `tensorflow<2.16` (via `ml_dtypes`) both failed with `_ARRAY_API not found` / `numpy.core.umath failed to import`. NumPy's own guidance for this error is to upgrade the affected module; neither of those pinned versions has a NumPy 2 compatible release (TF 2.15 also uses the removed `np.complex_` internally).

### Changes
**Dependency manifests** (`setup.py`, `requirements.txt`) — no lock files touched, NumPy only widened:
- `numpy<2` → `numpy>=1.25` (NumPy 2 now allowed; `np.exceptions` requires ≥1.25)
- `tensorflow<2.16` → `tensorflow>=2.20` (first TF line that supports NumPy 2.x)
- `torch>=2.0.0` → `torch>=2.4.0`, `torchvision==0.15.2` → `torchvision>=0.19.0` (first torch releases built against the NumPy 2 ABI)

**Application code:**
- `core/extraction/helpers.py`: `np.AxisError` → `np.exceptions.AxisError`.
- TensorFlow ≥2.16 ships Keras 3, so the TF extractors were updated to the Keras 3 API (no behaviour change):
  - `core/extraction/tensorflow.py`: `model.input` → `model.inputs` (Keras 3 `Sequential` exposes `.inputs` only), `layers.experimental.preprocessing.{Resizing,Rescaling,Normalization}` → `layers.{…}` (the `experimental.preprocessing` alias was removed), and `get_module_names()` now uses the public `model.layers` / `layer.name` instead of the removed `model.submodules` / `layer._name`.
  - `core/extraction/extractors.py`: `model.layers[0].input_shape[0][-2]` → `model.inputs[0].shape[-2]` (`Layer.input_shape` was removed in Keras 3), plus the same `experimental.preprocessing.Resizing` rename.

No tests were modified, deleted or skipped.

### Note
`xplique` (a transitive dependency of the optional `Harmonization` custom model, listed only in `requirements.txt`) still declares `numpy<2` / `tensorflow<2.16`. It is not imported by the package at import time and is only reached by the Harmonization extractor, so it does not affect the suite — but it will need an upstream release before that model works on NumPy 2.
