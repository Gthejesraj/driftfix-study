## driftfix: numpy

**✅ Fixed** · cost $0.38

All 56 tests pass.

## Summary

Updated `arlpy` for NumPy 2.x compatibility.

**`arlpy/comms.py`** — `np.product` was removed in NumPy 2.0; replaced both uses (in `ser` and `ber`) with its long-standing alias `np.prod`.

**`arlpy/signal.py`** — `mseq` builds its LFSR state as a `uint8` array and computed `2*reg[0]-1` to map bits to ±1. Under NumPy 2's NEP 50 promotion rules, the Python int operands no longer upcast the `uint8` scalar, so the `0` case wrapped around to `255` instead of `-1` (also emitting an overflow RuntimeWarning). The register value is now cast with `int()` before the arithmetic, which fixes `mseq` and the `gmseq` built on top of it.

**`setup.py` / `requirements.txt`** — dropped the `numpy<2.0.0` upper bound so NumPy 2.x is allowed.
