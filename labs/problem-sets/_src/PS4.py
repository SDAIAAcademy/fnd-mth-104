# %% [markdown]
# # Problem set 4 · The bootstrap
#
# After week 4 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# A sample of two baskets: 1 and 3 riyals. A bootstrap resample draws two values with replacement: four equally likely ordered resamples.
#
# Then five baskets: 1, 2, 2.5, 3 and 40 riyals. Before you run anything, decide whether the 95% percentile interval for their mean can contain 40.

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

# %% [markdown]
# ## Hand answers
#
# - `boot_se`: the standard deviation (divide by 4) of the four resample means of [1, 3]
# - `forty_inside`: True or False: is 40 inside the 95% percentile bootstrap interval for the mean of [1, 2, 2.5, 3, 40]?

# %%
hand = {
    "boot_se": None,   # ✏️
    "forty_inside": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def all_resample_se(x):
    """Return the standard deviation (ddof=0) of the means of all len(x)**len(x) ordered resamples of a small sample (itertools.product)."""
    raise NotImplementedError("✏️ write this function")


def percentile_ci(x, stat, B, seed):
    """Return the 2.5th and 97.5th percentiles of B bootstrap values of stat (a function such as np.mean), drawn with np.random.default_rng(seed), as a tuple of two floats."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(4, globals())
