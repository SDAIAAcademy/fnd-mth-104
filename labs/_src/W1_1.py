# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 1.1 · Describing the chain's baskets: centre, spread, shape, outliers and missing values
#
# Week 1 · Session 1 (Centre, spread, shape and missing values) · 105 min. An addition to the
# catalog entry's lab lines, so that week 1 has a lab.
#
# The operations manager of the bakery chain asks a simple question: "What does a typical basket
# look like, and how long do customers wait?" You have one month of baskets from six branches
# (`data/baskets.csv`, 6,278 synthetic baskets). You describe the values and the waits with
# summaries that survive a long tail, decide what to do with two extreme baskets, and find out who
# is missing from the wait data before you report a single number.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up and load the month of baskets (10 min)
# - [ ] 2 · Centre by hand, then in code: mean, median, trimmed mean (15 min)
# - [ ] 3 · Spread: standard deviation, interquartile range and the fences (15 min)
# - [ ] 4 · Shape: skewness, bins and the log scale (15 min)
# - [ ] 5 · Two extreme baskets: an error or a real order? (15 min)
# - [ ] 6 · Missing waits: count them, decode them, find who is missing (20 min)
# - [ ] 7 · Summaries by branch that state what is missing (10 min)
# - [ ] 8 · Record how this was checked (5 min)
# - [ ] ✱ Stretch · Show how the mean wait moves under three ways of handling the missing waits

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

# %% [markdown]
# ## 1 · The month of baskets
#
# One row per basket: the branch (BR03 to BR22), its sector, the day, the time band, the number
# of items, the value in riyals, the wait in minutes and whether the customer is a loyalty member.
# Look at the first rows and at the types before anything else.

# %%
baskets = U.load("baskets.csv")
print(baskets.shape)
print(baskets.head())
print(baskets.dtypes)

# %% [markdown]
# ## 2 · Centre
#
# **On paper first.** Nine baskets: 8.50, 12, 14, 15, 17, 19, 22, 31, 96 riyals. Write their mean,
# their median, and their 20% trimmed mean (drop the lowest and the highest fifth: with nine
# values, drop one at each end). Put your three numbers in `hand`.
#
# Then write `centre(x)` returning the mean, the median and the 20% trimmed mean of an array.

# %%
hand = {"mean": None, "median": None, "trimmed": None}   # ✏️ your hand results

def centre(x):
    """Mean, median and 20% trimmed mean of an array of numbers."""
    x = np.asarray(x, dtype=float)
    # BEGIN SOLUTION
    return {"mean": float(np.mean(x)), "median": float(np.median(x)),
            "trimmed": float(stats.trim_mean(x, 0.2))}
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"mean": 26.0556, "median": 17.0, "trimmed": 18.5714}
    # END SOLUTION

# %%
nine = np.array([8.5, 12, 14, 15, 17, 19, 22, 31, 96])
try:
    c9 = centre(nine)
except NotImplementedError:
    c9 = U.reference("w1_centre_nine")
U.keep("w1_centre_nine", c9)
print({k: round(v, 4) for k, v in c9.items()})
if hand["mean"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["mean"] is not None:
    U.check(all(abs(hand[k] - c9[k]) < 0.01 for k in c9), "hand and code agree on the nine baskets")

# %%
try:
    c_all = centre(baskets["value"])
except NotImplementedError:
    c_all = U.reference("w1_centre_all")
U.keep("w1_centre_all", c_all)
print("all baskets:", {k: round(v, 2) for k, v in c_all.items()})

# %% [markdown]
# **Look at** the three numbers. Which one would you give the operations manager as "a typical
# basket", and why are they so far apart?

# %% [markdown]
# ## 3 · Spread
#
# Write `spread(x)`: the standard deviation (with `ddof=1`), the quartiles Q1 and Q3, the
# interquartile range Q3 − Q1, and the two fences Q1 − 1.5 IQR and Q3 + 1.5 IQR. Use NumPy's
# default percentile method and say so in your note.

# %%
def spread(x):
    x = np.asarray(x, dtype=float)
    # BEGIN SOLUTION
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    return {"sd": float(np.std(x, ddof=1)), "q1": float(q1), "q3": float(q3), "iqr": float(iqr),
            "low_fence": float(q1 - 1.5 * iqr), "high_fence": float(q3 + 1.5 * iqr)}
    # END SOLUTION

# %%
try:
    s_all = spread(baskets["value"])
except NotImplementedError:
    s_all = U.reference("w1_spread_all")
U.keep("w1_spread_all", s_all)
print({k: round(v, 2) for k, v in s_all.items()})
beyond = int((baskets["value"] > s_all["high_fence"]).sum())
print(f"baskets above the high fence: {beyond} of {len(baskets)} ({beyond / len(baskets):.1%})")
U.check(abs(s_all["iqr"] - (s_all["q3"] - s_all["q1"])) < 1e-9, "IQR is Q3 − Q1")

# %% [markdown]
# A fence is a flag for a look, not a rule for deleting rows: with a long right tail, many honest
# baskets sit above it.

# %% [markdown]
# ## 4 · Shape
#
# Write `shape(x)`: the sample skewness (`scipy.stats.skew`) of the values and of their natural
# logarithms. Then print a table of counts in bins of 10 riyals up to 100 and one bin above.

# %%
def shape(x):
    x = np.asarray(x, dtype=float)
    # BEGIN SOLUTION
    return {"skew": float(stats.skew(x)), "skew_log": float(stats.skew(np.log(x)))}
    # END SOLUTION

# %%
clean_values = baskets.loc[baskets["value"] < 5000, "value"]   # the till error is handled in task 5
try:
    sh = shape(clean_values)
except NotImplementedError:
    sh = U.reference("w1_shape")
U.keep("w1_shape", sh)
print({k: round(v, 3) for k, v in sh.items()})
bins = list(range(0, 101, 10)) + [np.inf]
counts = pd.cut(clean_values, bins=bins, right=False).value_counts().sort_index()
for interval, n in counts.items():
    print(f"{str(interval):>14s} {n:5d} {'#' * int(60 * n / counts.max())}")

# %% [markdown]
# ## 5 · Two extreme baskets
#
# Sort by value and look at the five largest baskets with all their columns. One of them is a
# till error, one is a real catering order. Write `classify_extremes(df)` returning a dict
# `{basket_ref: "error" or "real"}` for the two largest, using the items and the value per item
# as evidence. Then recompute the centre without the error only.

# %%
print(baskets.sort_values("value", ascending=False).head(5).assign(per_item=lambda d: (d["value"] / d["items"]).round(2)))

def classify_extremes(df):
    top = df.sort_values("value", ascending=False).head(2)
    # BEGIN SOLUTION
    out = {}
    for _, r in top.iterrows():
        per_item = r["value"] / r["items"]
        out[r["basket_ref"]] = "error" if per_item > 100 else "real"
        # a few items at thousands of riyals each is a key held down, not a purchase
    return out
    # END SOLUTION

# %%
try:
    verdict = classify_extremes(baskets)
except NotImplementedError:
    verdict = U.reference("w1_extremes")
U.keep("w1_extremes", verdict)
print(verdict)
U.check(sorted(verdict.values()) == ["error", "real"], "one error and one real order")
errors = [k for k, v in verdict.items() if v == "error"]
kept = baskets[~baskets["basket_ref"].isin(errors)]
try:
    c_kept = centre(kept["value"])
except NotImplementedError:
    c_kept = U.reference("w1_centre_kept")
U.keep("w1_centre_kept", c_kept)
print("without the error:", {k: round(v, 2) for k, v in c_kept.items()}, "| before:", {k: round(v, 2) for k, v in c_all.items()})

# %% [markdown]
# **Look at** which of the three summaries moved when one row out of 6,278 went. That is what
# "robust" means.

# %% [markdown]
# ## 6 · Missing waits
#
# `wait_min` is empty for some baskets, and one branch's till writes `-1` when it did not record
# the wait. Write `clean_wait(df)` that returns a copy with `-1` turned into a missing value. Then
# write `missing_rate(df, by)` returning the share of missing waits per group. Find the group
# whose waits are missing far more often than the rest.

# %%
def clean_wait(df):
    # BEGIN SOLUTION
    out = df.copy()
    out.loc[out["wait_min"] < 0, "wait_min"] = np.nan
    return out
    # END SOLUTION

def missing_rate(df, by):
    # BEGIN SOLUTION
    return df["wait_min"].isna().groupby([df[c] for c in by]).mean()
    # END SOLUTION

# %%
try:
    waits = clean_wait(kept)
except NotImplementedError:
    waits = kept.copy()
    waits.loc[waits["wait_min"] < 0, "wait_min"] = np.nan
U.check((waits["wait_min"].dropna() >= 0).all(), "no negative waits left")
try:
    rates = missing_rate(waits, ["branch", "band"])
except NotImplementedError:
    rates = waits["wait_min"].isna().groupby([waits["branch"], waits["band"]]).mean()
table = rates.unstack().round(3)
print(table)
worst = rates.idxmax()
U.keep("w1_missing", {"worst": list(worst), "rate": float(rates.max()), "overall": float(waits["wait_min"].isna().mean())})
print("most often missing:", worst, f"{rates.max():.1%}", "| overall:", f"{waits['wait_min'].isna().mean():.1%}")

# %% [markdown]
# The busiest branch's evening waits are the ones most often missing: probably the long ones, when
# staff are too busy to log them. Dropping the empty rows then makes waits look shorter than they
# are. Missing data has a cause; report it.

# %% [markdown]
# ## 7 · Summaries by branch
#
# Write `branch_summary(df)`: one row per branch with the number of baskets, the median value,
# the IQR of the value, the median wait among recorded waits, and the share of waits missing.

# %%
def branch_summary(df):
    # BEGIN SOLUTION
    g = df.groupby("branch")
    return pd.DataFrame({
        "baskets": g.size(),
        "median_value": g["value"].median(),
        "iqr_value": g["value"].quantile(0.75) - g["value"].quantile(0.25),
        "median_wait": g["wait_min"].median(),
        "wait_missing": g["wait_min"].apply(lambda s: s.isna().mean()),
    }).round(3)
    # END SOLUTION

# %%
try:
    summary = branch_summary(waits)
except NotImplementedError:
    summary = pd.DataFrame(U.reference("w1_branch_summary"))
U.keep("w1_branch_summary", summary.to_dict())
print(summary)
U.check(int(summary["baskets"].sum()) == len(waits), "every basket counted once")

# %% [markdown]
# ## 8 · How this was checked
#
# Every lab ends with a short note: what you computed, how you checked it, and who reads it next.
# Fill the dictionary. The check must be something you ran, not something you believe.

# %%
def write_note():
    """✏️ Four sentences: the result for the operations manager; how you checked it (a hand case,
    a second method, a count); what the number does not cover; who reruns it before it is sent
    (a role, not yourself)."""
    # BEGIN SOLUTION
    return {
    "result": f"A typical basket is about {c_kept['median']:.2f} riyals (median); half of baskets fall between "
              f"{s_all['q1']:.2f} and {s_all['q3']:.2f}. The mean, {c_kept['mean']:.2f}, is pulled up by a long tail.",
    "checked_by": "centre() agreed with a nine-basket hand case; the till error was found by value per item and "
                  "removed alone; branch counts add up to the file.",
    "limits": "One month, six branches. Waits are missing far more often in the busiest branch's evenings, so the "
              "recorded waits understate waiting there.",
    "reviewer": "The quality lead reruns the notebook from the data file before the summary is sent.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. Removing one basket of 9,999 riyals changes the mean a lot and the median hardly at all. Why?
#
# <details><summary>Answer</summary>The mean adds up every value, so one huge value moves it by
# its excess divided by n. The median depends only on the order of the middle values.</details>
#
# 2. More than 300 baskets lie above the high fence. Should you delete them?
#
# <details><summary>Answer</summary>No. The fence flags values to look at. In a long right tail
# most of them are honest baskets; delete only what you can show is an error.</details>
#
# 3. Waits are missing in 21% of one branch's evenings and 2% elsewhere. What does dropping the
#    missing rows do to the reported median wait?
#
# <details><summary>Answer</summary>It probably lowers it: the missing waits are likely the long,
# busy ones. Report the missing share beside the median, and say which way the bias runs.</details>
#
# ## Carry forward
#
# Week 2 samples from a whole quarter of baskets, `data/population.csv`. Keep your `centre` and
# `spread` functions: you use them again.

# %% [markdown]
# ## ✱ Stretch
#
# Compute the mean wait three ways: dropping missing waits, filling them with the overall median,
# and filling them with the median of the same branch and band. Which way does each move the
# answer, and which would you defend?

# %%
def stretch():
    # BEGIN SOLUTION
    drop = waits["wait_min"].mean()
    fill_all = waits["wait_min"].fillna(waits["wait_min"].median()).mean()
    fill_grp = waits["wait_min"].fillna(waits.groupby(["branch", "band"])["wait_min"].transform("median")).mean()
    print(f"drop: {drop:.3f} | overall median: {fill_all:.3f} | branch-and-band median: {fill_grp:.3f}")
    # END SOLUTION


U.optional(stretch)
