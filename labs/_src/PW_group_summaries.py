# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Pre-work · Group summaries with a DataFrame library
#
# Guided self-study before week 1 · 60 min. For participants who have not taken FND-DAT-102.
#
# The course assumes you can compute summaries by group in a DataFrame library. This notebook
# practises exactly that on the bakery chain's month of baskets (`data/baskets.csv`, synthetic):
# counting rows, averaging within groups, several summaries at once, two grouping columns, and
# filtering groups. The examples use pandas; Polars has the same ideas under `group_by` and `agg`.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Load the file and look at it (10 min)
# - [ ] 2 · Count and average by one column (15 min)
# - [ ] 3 · Several summaries at once (15 min)
# - [ ] 4 · Two grouping columns, and a wide table (10 min)
# - [ ] 5 · Keep only groups large enough to report (10 min)

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/fnd-mth-104.git"
    if not Path("/content/fnd-mth-104").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/fnd-mth-104"], check=True)
    os.chdir("/content/fnd-mth-104/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import pandas as pd
import sta as U

# %% [markdown]
# ## 1 · Load and look

# %%
baskets = U.load("baskets.csv")
print(baskets.shape)
print(baskets.head(3))
print(baskets["branch"].value_counts().sort_index())

# %% [markdown]
# ## 2 · Count and average by one column
#
# Write `by_branch(df)`: a Series with the mean basket value of each branch, rounded to 2 decimals.

# %%
def by_branch(df):
    # BEGIN SOLUTION
    return df.groupby("branch")["value"].mean().round(2)
    # END SOLUTION

# %%
try:
    s = by_branch(baskets)
    U.check(len(s) == 6 and abs(s.mean() - baskets.groupby("branch")["value"].mean().mean()) < 0.01, "six branch means")
    print(s)
except NotImplementedError:
    print("✏️ write by_branch()")

# %% [markdown]
# ## 3 · Several summaries at once
#
# Write `summary(df)`: one row per branch with columns `n` (rows), `mean_value`, `median_value`
# and `members` (the share of loyalty members), using `groupby(...).agg(name=(column, function))`.

# %%
def summary(df):
    # BEGIN SOLUTION
    return df.groupby("branch").agg(n=("value", "size"), mean_value=("value", "mean"),
                                    median_value=("value", "median"), members=("member", "mean")).round(3)
    # END SOLUTION

# %%
try:
    t = summary(baskets)
    U.check(int(t["n"].sum()) == len(baskets), "every basket counted once")
    print(t)
except NotImplementedError:
    print("✏️ write summary()")

# %% [markdown]
# ## 4 · Two grouping columns
#
# Write `branch_band(df)`: the median wait by branch (rows) and time band (columns). Hint:
# group by both columns, then `unstack()`.

# %%
def branch_band(df):
    # BEGIN SOLUTION
    return df.groupby(["branch", "band"])["wait_min"].median().unstack()
    # END SOLUTION

# %%
try:
    w = branch_band(baskets)
    U.check(w.shape == (6, 3), "six branches by three bands")
    print(w)
except NotImplementedError:
    print("✏️ write branch_band()")

# %% [markdown]
# ## 5 · Only groups large enough to report
#
# The course reports no group of fewer than 30 rows. Write `reportable(df, by, min_n=30)`: the
# mean value per group of `by`, keeping only groups with at least `min_n` rows. Try it with
# `["branch", "day"]`.

# %%
def reportable(df, by, min_n=30):
    # BEGIN SOLUTION
    g = df.groupby(by)["value"].agg(["size", "mean"])
    return g[g["size"] >= min_n]
    # END SOLUTION

# %%
try:
    r = reportable(baskets, ["branch", "day"])
    U.check((r["size"] >= 30).all(), "no group below 30 rows")
    print(len(r), "of", baskets.groupby(["branch", "day"]).ngroups, "branch-days are large enough to report")
except NotImplementedError:
    print("✏️ write reportable()")

# %% [markdown]
# If all five tasks ran without help, you are ready for week 1.
