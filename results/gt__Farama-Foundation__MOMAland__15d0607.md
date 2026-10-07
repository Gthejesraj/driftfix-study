## driftfix: numpy

**✅ Fixed** · cost $0.25

All 23 tests pass.

## Fix NumPy 2 incompatibility in `MOGemMining`

**Problem:** `MOGemMining.__init__` stored each agent's worker count as `self.random.choices(lst)` — a one-element *list*, not an int. In `step()` this made `workers_at_mine[mine] + self.workers[agent]` produce a shape-`(1,)` array, which was then assigned back into the scalar slot `workers_at_mine[mine]`.

NumPy silently allowed converting a 1-element, ndim>0 array to a scalar (deprecated since 1.25); NumPy 2 removed it, so the assignment now raises `ValueError: setting an array element with a sequence`.

**Change:** `momaland/envs/gem_mining/gem_mining.py` — index the result of `random.choices(...)` so `self.workers` holds plain Python ints. This keeps the RNG consumption (and thus seeded behaviour) identical to before while making the arithmetic genuinely scalar.

No dependency changes were needed — `numpy >=1.21.0` already permits 2.5.3.
