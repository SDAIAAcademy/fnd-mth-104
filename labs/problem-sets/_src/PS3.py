# %% [markdown]
# # Problem set 3 · Confounding and Simpson's paradox
#
# After week 3 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# Two delivery vans, X and Y, and two kinds of route. Late deliveries out of all deliveries:
#
# Route s1: X 1 of 50, Y 8 of 200. Route s2: X 40 of 400, Y 9 of 60. The table is below.

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
table = pd.DataFrame({"unit": ["X", "Y", "X", "Y"], "stratum": ["s1", "s1", "s2", "s2"],
                      "bad": [1, 8, 40, 9], "total": [50, 200, 400, 60]})

# %% [markdown]
# ## Hand answers
#
# - `X_all`: X's late rate over both routes, as a proportion
# - `Y_all`: Y's late rate over both routes

# %%
hand = {
    "X_all": None,   # ✏️
    "Y_all": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def rates_by(df, by, num, den):
    """Sum num and den within each group of the column by, and return num / den as a Series indexed by group."""
    raise NotImplementedError("✏️ write this function")


def reverses(df, unit, stratum, num, den):
    """Return True when the unit with the lower rate overall has the higher rate in every stratum (or the reverse): Simpson's paradox. Return a Python bool."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(3, globals())
