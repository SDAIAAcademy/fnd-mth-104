# %% [markdown]
# # Problem set 7 · Multiple testing
#
# After week 7 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# Five p-values from one report: 0.01, 0.02, 0.03, 0.04 and 0.20, with α = 0.05.
#
# Count by hand how many each procedure rejects: Bonferroni, Holm and Benjamini-Hochberg.

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
p5 = np.array([0.01, 0.02, 0.03, 0.04, 0.20])

# %% [markdown]
# ## Hand answers
#
# - `bonferroni`: how many Bonferroni rejects
# - `holm`: how many Holm rejects
# - `bh`: how many Benjamini-Hochberg rejects

# %%
hand = {
    "bonferroni": None,   # ✏️
    "holm": None,   # ✏️
    "bh": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def bonferroni(p, alpha=0.05):
    """Return a boolean array of rejections, in the original order."""
    raise NotImplementedError("✏️ write this function")


def holm(p, alpha=0.05):
    """Return a boolean array of rejections, in the original order."""
    raise NotImplementedError("✏️ write this function")


def bh(p, alpha=0.05):
    """Return a boolean array of rejections, in the original order."""
    raise NotImplementedError("✏️ write this function")


def familywise_rate(m, alpha, reps, seed):
    """Simulate reps families of m independent tests of true nulls (each p-value uniform on 0 to 1, from np.random.default_rng(seed)) and return the share of families with at least one p ≤ alpha."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(7, globals())
