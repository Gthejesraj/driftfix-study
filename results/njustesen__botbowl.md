## driftfix: numpy

**✅ Fixed** · cost $0.41

Fixed — full suite: 447 passed, 1 deselected.

## Summary

**Problem.** `numpy` 2.0 removed the `np.bool8` alias (use `np.bool_`). `gym` 0.26.2's `PassiveEnvChecker` — which `gym.make()` wraps around every environment by default — references `np.bool8` in both the 4-tuple and 5-tuple branches of `env_step_passive_checker`, so *any* `step()` on a `gym.make()`-created env raised `AttributeError: module 'numpy' has no attribute 'bool8'`. `gym` 0.26.2 is its final release and will never be numpy-2 compatible; nothing in botbowl's own code used removed numpy APIs.

**Change.**
- `botbowl/ai/__init__.py`: register all six `botbowl-*-v4` environments with `disable_env_checker=True`, with a comment explaining why. The passive checker is a debug-only aid that emitted nothing but warnings for these envs, and disabling it fixes every `gym.make()` caller (tests, `examples/multi_gym_example.py`, `tests/performance/run_env.py`) in one place rather than per call site.
- `setup.py`: widened `numpy==1.24.3` → `numpy>=1.24.3` so numpy 2.x is allowed.

No tests were modified, and the pinned `requirements.txt` (a fully pinned transitive lock) was left untouched.
