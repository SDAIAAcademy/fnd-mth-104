# %% [markdown]
# # Problem set 5 · Differences and slopes
#
# After week 5 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# Three points: (0, 1), (1, 1), (2, 4). The least-squares slope is Σ(x − x̄)(y − ȳ) / Σ(x − x̄)².
#
# For a difference between two groups, resample each group separately, keeping its size.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    if not Path("/content/fnd-mth-104").exists():
        subprocess.run(["git", "clone", "-q", "https://github.com/SDAIAAcademy/fnd-mth-104.git", "/content/fnd-mth-104"], check=True)
    os.chdir("/content/fnd-mth-104/labs/problem-sets")
elif not Path("pscheck.py").exists() and Path("problem-sets/pscheck.py").exists():
    os.chdir("problem-sets")  # opened from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import pscheck
px = np.array([0, 1, 2], dtype=float)
py = np.array([1, 1, 4], dtype=float)

# %% [markdown]
# ## Hand answers
#
# - `slope`: the slope of py on px

# %%
hand = {
    "slope": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def slope(x, y):
    """Return the least-squares slope of y on x as a float."""
    raise NotImplementedError("✏️ write this function")


def diff_ci(a, b, stat, B, seed):
    """Return the 95% percentile bootstrap interval of stat(a*) − stat(b*), resampling a and b separately with np.random.default_rng(seed), as a tuple of two floats."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(5, globals())
