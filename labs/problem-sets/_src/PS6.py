# %% [markdown]
# # Problem set 6 · Permutation tests
#
# After week 6 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# Group A: 1 and 2. Group B: 4 and 6. Under the null any two of the four values could have been group A: six splits.
#
# The two-sided p-value is the share of splits whose |mean(B) − mean(A)| is at least the observed one.

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
# - `p`: the exact two-sided p-value for A = [1, 2], B = [4, 6]

# %%
hand = {
    "p": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def exact_p(a, b):
    """Return the exact two-sided p-value of the difference in means from every split of the pooled values."""
    raise NotImplementedError("✏️ write this function")


def perm_p(x, y, R, seed):
    """Return the two-sided permutation p-value (count + 1) / (R + 1) of the difference in means, from R shuffles drawn with np.random.default_rng(seed)."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(6, globals())
