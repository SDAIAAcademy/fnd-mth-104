# %% [markdown]
# # Problem set 8 · Error rates and power
#
# After week 8 · 50 minutes · **AI off for the first attempt.** Work on paper first, then in code.
# The last cell checks your work: it compares each hand answer with your own function on the same
# case, and runs your functions on new random data. It stores no answers. Hand in the notebook with
# its outputs.
#
# A team runs 100 tests in a year: 50 of ideas that do nothing, 50 of ideas that work. Each test uses α = 0.05 and has power 0.8.
#
# Then simulate a two-group trial on normal data to estimate a rejection rate.

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
# - `false_findings`: expected false findings
# - `true_findings`: expected true findings
# - `false_share`: the share of all findings that are false

# %%
hand = {
    "false_findings": None,   # ✏️
    "true_findings": None,   # ✏️
    "false_share": None,   # ✏️
}

# %% [markdown]
# ## Your functions

# %%
def expected_findings(n_null, n_real, alpha, power):
    """Return a dict with false_findings, true_findings and false_share."""
    raise NotImplementedError("✏️ write this function")


def rejection_rate(n, d, reps, seed):
    """Simulate reps trials with n normal values per group, the second shifted by d standard deviations, using np.random.default_rng(seed); test each with Welch's t test (scipy.stats.ttest_ind, equal_var=False) and return the share with p ≤ 0.05."""
    raise NotImplementedError("✏️ write this function")

# %%
# Try your functions here on the small cases before you run the check.

# %% [markdown]
# ## Check

# %%
score = pscheck.check(8, globals())
