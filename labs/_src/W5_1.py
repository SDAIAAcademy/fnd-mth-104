# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 5.1 · Bootstrap intervals for differences and slopes on public skewed data
#
# Week 5 · Session 1 (Bootstrap intervals for differences and slopes) · 105 min. An addition to
# the catalog entry's lab lines, so that week 5 has a lab.
#
# The chain's own data cannot be published, so this week you practise on two public datasets,
# both in the public domain and bundled with the statsmodels library (nothing is downloaded):
#
# - the RAND Health Insurance Experiment subset: outpatient visits to a doctor in a year for
#   20,190 person-years, with the coinsurance rate of a plan assigned at random;
# - Engel's food expenditure data: annual income and food spending of 235 households.
#
# Visits and income are strongly skewed. You build bootstrap intervals for a mean, a median, a
# difference between two groups and a regression slope, and you check that every interval agrees
# when the notebook is rerun with a new seed.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; the two public datasets and their licences (10 min)
# - [ ] 2 · Suppress small groups before any table (10 min)
# - [ ] 3 · Intervals for the mean and the median of visits (15 min)
# - [ ] 4 · An interval for a difference: free care against 95% coinsurance (20 min)
# - [ ] 5 · A slope by hand, then in code (10 min)
# - [ ] 6 · A bootstrap interval for the slope of food spending on income (20 min)
# - [ ] 7 · Rerun with a new seed and compare every interval (10 min)
# - [ ] 8 · Record how this was checked (10 min)
# - [ ] ✱ Stretch · The slope on the log scale, and what it means

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

import numpy as np
import pandas as pd
from scipy import stats
import sta as U

print("quick mode:", U.QUICK)
B = U.pick(2000, 400)

# %% [markdown]
# ## 1 · The public data
#
# Source and licence first, always. Both datasets say "public domain" in their statsmodels
# documentation. Rows of the health experiment are person-years: the same person appears in
# several years, which the simple bootstrap here ignores (resampling people rather than rows is
# taught in SPC-STA-201). Say so in your note.

# %%
hie = U.health_experiment()
food = U.food_budgets()
print(hie.shape, food.shape)
print(hie.describe().T.round(2))
print("skewness: visits", round(float(stats.skew(hie["visits"])), 2), "| income", round(float(stats.skew(food["income"])), 2))

# %% [markdown]
# ## 2 · Suppress small groups
#
# The course's reporting rule: a group with fewer than 30 rows is not reported (`U.MIN_GROUP`).
# Build the table of mean visits by plan and self-rated health with the count of each cell, then
# pass it through `U.suppress`. Which cells disappear?

# %%
cells = hie.groupby(["plan", "health"], observed=True)["visits"].agg(n="size", mean_visits="mean").reset_index()
shown = U.suppress(cells.set_index(["plan", "health"]), "n")
print(shown)
n_hidden = int((cells["n"] < U.MIN_GROUP).sum())
U.keep("w5_suppressed", n_hidden)
U.check(n_hidden >= 1, f"{n_hidden} small cells suppressed before reporting")

# %% [markdown]
# ## 3 · The mean and the median of visits
#
# Write `boot_dist(x, stat, B, rng)` returning the `B` bootstrap statistics (a loop of `B`
# resamples is fine: `rng.choice(x, len(x), replace=True)`), and `pct(boots)` returning the 2.5th
# and 97.5th percentiles. Then build intervals for the mean and the median visits under free care.

# %%
def boot_dist(x, stat, B, rng):
    x = np.asarray(x, dtype=float)
    # BEGIN SOLUTION
    return np.array([stat(rng.choice(x, len(x), replace=True)) for _ in range(B)])
    # END SOLUTION

def pct(boots, level=0.95):
    a = 100 * (1 - level) / 2
    return tuple(float(v) for v in np.percentile(boots, [a, 100 - a]))

def safe_boot(x, stat, B, rng):
    try:
        return boot_dist(x, stat, B, rng)
    except NotImplementedError:
        x = np.asarray(x, dtype=float)
        return np.array([stat(rng.choice(x, len(x), replace=True)) for _ in range(B)])

# %%
free = hie.loc[hie["coins"] == 0, "visits"].to_numpy()
high = hie.loc[hie["coins"] == 95, "visits"].to_numpy()

def intervals(seed):
    r = np.random.default_rng(seed)
    out = {
        "mean_free": pct(safe_boot(free, np.mean, B, r)),
        "median_free": pct(safe_boot(free, np.median, B, r)),
    }
    return out

first = intervals(51)
print("free care: n", len(free), "| mean", round(free.mean(), 3), first["mean_free"], "| median", np.median(free), first["median_free"])

# %% [markdown]
# **Look at** the median's interval. Visits are whole numbers, so the median can only take a few
# values and its bootstrap distribution is lumpy. The interval is honest, but say what it is.

# %% [markdown]
# ## 4 · A difference between two groups
#
# The plans were assigned at random, so a difference between them estimates what the plan did.
# Write `boot_diff(x, y, stat, B, rng)`: resample **each group separately** (keeping its size)
# and return the `B` values of `stat(x*) − stat(y*)`. Compute intervals for the difference in
# mean visits and in median visits, free care minus 95% coinsurance.

# %%
def boot_diff(x, y, stat, B, rng):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    # BEGIN SOLUTION
    return np.array([stat(rng.choice(x, len(x))) - stat(rng.choice(y, len(y))) for _ in range(B)])
    # END SOLUTION

def safe_diff(x, y, stat, B, rng):
    try:
        return boot_diff(x, y, stat, B, rng)
    except NotImplementedError:
        return np.array([stat(rng.choice(x, len(x))) - stat(rng.choice(y, len(y))) for _ in range(B)])

def diffs(seed):
    r = np.random.default_rng(seed)
    return {"mean_diff": pct(safe_diff(free, high, np.mean, B, r)),
            "median_diff": pct(safe_diff(free, high, np.median, B, r))}

first.update(diffs(52))
print(f"mean visits: free {free.mean():.3f}, 95% coinsurance {high.mean():.3f}, difference {free.mean() - high.mean():.3f}",
      "interval", tuple(round(v, 3) for v in first["mean_diff"]))
print(f"median visits: free {np.median(free)}, 95% coinsurance {np.median(high)}", "interval of the difference", first["median_diff"])
U.check(first["mean_diff"][0] > 0, "the interval for the difference in means excludes zero")

# %% [markdown]
# ## 5 · A slope by hand
#
# **On paper.** Three points: (1, 2), (2, 3), (3, 7). The least-squares slope is
# Σ(x − x̄)(y − ȳ) / Σ(x − x̄)². Compute it and put it in `hand`. Then write `slope(x, y)`.

# %%
hand = {"slope": None}   # ✏️

def slope(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    # BEGIN SOLUTION
    dx = x - x.mean()
    return float((dx * (y - y.mean())).sum() / (dx ** 2).sum())
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"slope": 2.5}
    # END SOLUTION

def safe_slope(x, y):
    try:
        return slope(x, y)
    except NotImplementedError:
        return float(np.polyfit(x, y, 1)[0])

# %%
s3 = safe_slope([1, 2, 3], [2, 3, 7])
print("slope of the three points:", s3)
U.check(abs(s3 - np.polyfit([1, 2, 3], [2, 3, 7], 1)[0]) < 1e-9, "slope() agrees with the library fit")
if hand["slope"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["slope"] is not None:
    U.check(abs(hand["slope"] - s3) < 0.01, "hand and code agree")

# %% [markdown]
# ## 6 · The slope of food spending on income
#
# For a slope, resample **whole households** (rows), so each income stays with its own food
# spending. Write `boot_slope(x, y, B, rng)` and build the interval.

# %%
def boot_slope(x, y, B, rng):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    # BEGIN SOLUTION
    out = np.empty(B)
    for b in range(B):
        i = rng.integers(0, len(x), len(x))
        out[b] = slope(x[i], y[i])
    return out
    # END SOLUTION

def slopes(seed):
    r = np.random.default_rng(seed)
    x, y = food["income"].to_numpy(), food["food"].to_numpy()
    try:
        bs = boot_slope(x, y, B, r)
    except NotImplementedError:
        bs = []
        for _ in range(B):
            i = r.integers(0, len(x), len(x))
            bs.append(np.polyfit(x[i], y[i], 1)[0])
        bs = np.array(bs)
    return {"slope": pct(bs)}

first.update(slopes(53))
b_food = safe_slope(food["income"], food["food"])
print(f"slope {b_food:.4f}: each extra unit of income goes with {b_food:.3f} more of food spending; interval",
      tuple(round(v, 4) for v in first["slope"]))

# %% [markdown]
# ## 7 · Rerun with a new seed
#
# The outcome LO4 asks for a notebook whose intervals agree on rerun with a new seed. Run tasks
# 3, 4 and 6 again with new seeds and make a table of every interval, both runs, and the largest
# move of either end relative to the interval's width.

# %%
second = intervals(151)
second.update(diffs(152))
second.update(slopes(153))
rerun = pd.DataFrame([{"interval": k, "run1_low": first[k][0], "run1_high": first[k][1],
                       "run2_low": second[k][0], "run2_high": second[k][1]} for k in first])
width = rerun["run1_high"] - rerun["run1_low"]
rerun["move_share_of_width"] = (np.maximum(abs(rerun["run1_low"] - rerun["run2_low"]),
                                           abs(rerun["run1_high"] - rerun["run2_high"])) / width.where(width > 0, 1)).round(3)
U.keep("w5_rerun", rerun.round(4).to_dict(orient="list"))
print(rerun.round(4).to_string(index=False))
U.check((rerun["move_share_of_width"] < 0.15).all(), "every interval moved by less than 15% of its width")

# %% [markdown]
# ## 8 · How this was checked

# %%
def write_note():
    # BEGIN SOLUTION
    return {
        "result": f"Free care: {free.mean():.2f} visits a year against {high.mean():.2f} at 95% coinsurance, a difference of "
                  f"{free.mean() - high.mean():.2f} (95% bootstrap interval {first['mean_diff'][0]:.2f} to {first['mean_diff'][1]:.2f}); "
                  f"food spending rises by {b_food:.3f} per unit of income ({first['slope'][0]:.3f} to {first['slope'][1]:.3f}).",
        "checked_by": f"Rerun with new seeds: every end moved by less than {100 * rerun['move_share_of_width'].max():.0f}% of its "
                      "interval's width; slope() agreed with a three-point hand case and the library fit.",
        "limits": "Rows are person-years, so the same person counts several times and the intervals are probably too narrow; "
                  f"{n_hidden} plan-by-health cells under 30 rows were suppressed; Engel's households are one old survey.",
        "reviewer": "A second analyst reruns the notebook from a clean environment before the figures are quoted.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. Why resample each plan's rows separately for a difference, and whole households for a slope?
#
# <details><summary>Answer</summary>Each way copies how the data were collected: two groups of
# fixed size for the plans; pairs of income and spending that belong together for the slope.
# Breaking the pairs would destroy the relation the slope measures.</details>
#
# 2. The median difference interval is 1 to 1. What does that say, and what does it not?
#
# <details><summary>Answer</summary>The medians are whole numbers that hardly vary between
# resamples of thousands of rows. It does not mean the difference is known exactly; the mean
# difference describes the shift better here.</details>
#
# 3. A colleague reran your notebook and got intervals that differ in the third decimal. Is the
#    result reproducible?
#
# <details><summary>Answer</summary>Yes, to the precision it should be reported at. Fix the seed
# for exact reruns and report the number of resamples.</details>
#
# ## Carry forward
#
# Week 6 tests the same two questions with permutation tests and reports effect sizes with these
# intervals.

# %% [markdown]
# ## ✱ Stretch
#
# Fit the slope of log(food) on log(income) and build its interval. The slope is now an
# elasticity: the percentage change in food spending for a 1% change in income.

# %%
def stretch():
    # BEGIN SOLUTION
    lx, ly = np.log(food["income"].to_numpy()), np.log(food["food"].to_numpy())
    r = np.random.default_rng(7)
    bs = []
    for _ in range(B):
        i = r.integers(0, len(lx), len(lx))
        bs.append(slope(lx[i], ly[i]))
    print(f"elasticity {slope(lx, ly):.3f}, interval {pct(np.array(bs))}")
    # END SOLUTION


U.optional(stretch)
