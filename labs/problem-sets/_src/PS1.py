# %% [markdown]
# # Problem set 1 · Describing data
#
# After week 1 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# Summaries that survive a long tail. Seven waits, in minutes: 4, 7, 7, 9, 12, 15, 40.
#
# Use NumPy's default percentile rule (linear interpolation): the p-th percentile of n sorted values sits at position (n − 1)p, counting from 0.

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
x = np.array([4, 7, 7, 9, 12, 15, 40], dtype=float)

# %% [markdown]
# ## Hand answers
#
# - `median`: the median of x
# - `iqr`: Q3 − Q1 of x, by the rule above

# %%
hand = {
    "median": None,   # ✏️
    "iqr": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def median_iqr(x):
    """Return (median, interquartile range) of an array."""
    raise NotImplementedError("✏️ write this function")


def mad(x):
    """Return the median absolute deviation: the median of |x − median(x)|."""
    raise NotImplementedError("✏️ write this function")


def missing_share(x):
    """Return the share of values of an array that are NaN."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(1, globals())
