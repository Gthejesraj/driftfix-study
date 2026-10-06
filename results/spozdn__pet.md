## driftfix: numpy

**✅ Fixed** · cost $2.55

## Support NumPy 2.x

The collection failures were not in our own NumPy usage — they came from `matscipy` 1.0.0, whose compiled extension is built against the NumPy 1.x C ABI (`AttributeError: _ARRAY_API not found` / `numpy.core.multiarray failed to import`). The only `matscipy` releases built against the NumPy 2 ABI are ≥ 1.2.0, and those require `ase >= 3.26`, so the `ase < 3.23.0` cap had to go too. Our own code contained no removed NumPy aliases.

### Changes

- **`requirements.txt`**: dropped the `numpy<2` cap; `matscipy>=1.2.0` (first NumPy‑2‑ABI build); `ase>=3.27.0` (required by modern `matscipy`; ASE ≤ 3.22 also predates NumPy 2).
- **`src/molecule.py`**: added an explicit `import ase.neighborlist`. Newer ASE no longer pulls that submodule in as a side effect of `import ase.io`, which made the existing `ase.neighborlist.neighbor_list(...)` calls raise `AttributeError`.
- **`src/ase_compat.py`** (new): small helpers (`get/has_structural_property`, `get/has_atomic_property`) that look up reference values in `atoms.info` / `atoms.arrays` and fall back to the attached calculator's results. Since ASE 3.23, `ase.io.read` attaches standard properties such as `energy` and `forces` to a `SinglePointCalculator` instead of leaving them in `info`/`arrays`, which previously broke training with `KeyError: 'energy'`.
- **`src/data_preparation.py`, `src/estimate_error.py`, `src/estimate_error_sp.py`**: read energies/forces/general targets through those helpers, so both old- and new-style ASE layouts work.

No test was modified, skipped or deleted, and NumPy is neither pinned nor downgraded.

### Verification

- Study test command: `2 passed, 2 skipped (pre-existing skip markers), 75 deselected`.
- Full `tests/test_cpp_extension.py` (66 cases, exercises both the `matscipy` periodic and ASE non-periodic neighbour-list paths): all pass.
- End-to-end `pet_train` (single- and multi-target), `pet_run`, and `SingleStructCalculator` runs all complete and report ground-truth errors correctly.
