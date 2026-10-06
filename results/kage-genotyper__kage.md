## driftfix: numpy

**❌ Not fixed** · cost $2.40

```markdown
## Make KAGE work with numpy 2

`numpy` 1.26 → 2.x broke the test suite (collection aborted on
`AttributeError: module 'numpy' has no attribute 'VisibleDeprecationWarning'`).

### Changes

**Our own code**
- `kage/indexing/signatures.py`, `kage/indexing/path_variant_indexing.py`: replaced the
  removed `np.in1d` with `np.isin` (inputs are already `ravel()`-ed, so behaviour is identical).
- `setup.py`: dropped the `numpy<2` upper bound.

**New `kage/numpy_compat.py`** (applied from `kage/__init__.py`, before any dependency is imported)

KAGE's dependency stack (`kmer_mapper`, `obgraph`, `graph_kmer_index`, `bionumpy`,
`npstructures`) has no numpy-2-compatible release — all of them are already at their latest
published version — so the handful of numpy-1 behaviours they rely on are restored in one
documented, idempotent shim that is a no-op on numpy 1.x:
- `np.VisibleDeprecationWarning` → `np.exceptions.VisibleDeprecationWarning`, and `np.in1d` →
  `np.isin` (used by `kmer_mapper` at import time and by `obgraph.Graph`).
- `np.ediff1d`: cast `to_begin`/`to_end` to the input dtype when the values are representable,
  restoring the value-based casting NEP 50 removed (`np.ediff1d(uint_array, to_begin=1)` in
  `obgraph`/`graph_kmer_index`). Genuinely unsafe casts still raise numpy's own error.
- `bionumpy.KmerEncoding.to_string`: decode via a python int, since `np.uint64(kmer) >>
  np.arange(k)` (int64) no longer promotes under NEP 50.
- `npstructures` row slicing: use `.item()` instead of `int(one_element_1d_array)`, which
  numpy 2 only allows for 0-d arrays.

Each shim carries a comment explaining what it works around; they can be deleted once the
upstream packages support numpy 2. No tests were changed, skipped or removed.

### Verification
`130 passed, 9 skipped, 3 xfailed, 1 xpassed` — previously 1 collection error + 7 failures.
```

Rejected: agent changed the numpy requirement or a lock file in ['setup.py'].
