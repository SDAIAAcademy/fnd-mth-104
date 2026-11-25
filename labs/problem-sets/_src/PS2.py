# %% [markdown]
# # Problem set 2 · Sampling variation
#
# After week 2 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# A population of four baskets: 2, 4, 6 and 8 riyals. Samples of two are drawn without replacement.
#
# The standard error of the sample mean is the standard deviation (divide by the number of samples) of the means of all possible samples.

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
pop4 = np.array([2, 4, 6, 8], dtype=float)

# %% [markdown]
# ## Hand answers
#
# - `se`: the standard error of the mean of samples of 2 from pop4

# %%
hand = {
    "se": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def exact_se(pop, n):
    """Return the standard deviation (ddof=0) of the means of every sample of size n drawn without replacement from pop (use itertools.combinations)."""
    raise NotImplementedError("✏️ write this function")


def se_by_simulation(pop, n, reps, seed):
    """Draw reps samples of size n without replacement with np.random.default_rng(seed); return the standard deviation (ddof=1) of their means as a float."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(2, globals())
