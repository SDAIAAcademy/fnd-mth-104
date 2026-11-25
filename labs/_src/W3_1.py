# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 3.1 · Confounding in the waste records, against a randomised trial
#
# Week 3 · Session 1 (Confounding and Simpson's paradox) · 105 min. An addition to the catalog
# entry's lab lines, so that week 3 has a lab.
#
# The quality lead has two pieces of evidence about bread waste. Managers chose which branches got
# a new display shelf, and six months of records (`data/waste.csv`) show the display branches
# wasting more. Separately, an evening discount on the day's bread was given to 12 branches drawn
# at random (`data/trial.csv`). You find out why the display looks harmful overall and helpful
# within each branch size, and why the trial's answer needs no such adjustment.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; observational and experimental data (10 min)
# - [ ] 2 · Simpson's paradox by hand on a small table (15 min)
# - [ ] 3 · Waste rate by display, all branches together (10 min)
# - [ ] 4 · Waste rate by display within each branch size (15 min)
# - [ ] 5 · Who chose the display: the confounder (10 min)
# - [ ] 6 · The randomised trial: balance and the difference (20 min)
# - [ ] 7 · Balance of size and sector in the two studies (15 min)
# - [ ] 8 · Record how this was checked (10 min)
# - [ ] ✱ Stretch · Standardise the display comparison to the chain's mix of branch sizes

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
import sta as U

print("quick mode:", U.QUICK)

# %% [markdown]
# ## 1 · Two kinds of data
#
# In **observational** data someone other than the analyst decided who got what (here, the
# managers decided which branches got the display). In an **experiment** the assignment was made
# by a random draw. Read both files.

# %%
waste = U.load("waste.csv")
trial = U.load("trial.csv")
print(waste.head(), "\n", waste.shape)
print(trial.head(), "\n", trial.shape)

# %% [markdown]
# ## 2 · Simpson's paradox by hand
#
# A small example from another department, the ovens. Burnt trays by oven and shift:
#
# | Shift | Oven A burnt / trays | Oven B burnt / trays |
# |---|---|---|
# | Morning | 2 / 50 | 10 / 200 |
# | Evening | 30 / 300 | 6 / 50 |
#
# **On paper:** the burn rate of each oven in each shift, and of each oven over both shifts. Which
# oven is better in each shift? Over both? Put the six rates in `hand` as proportions.
# Then write `rates(df, by, num, den)`, which sums `num` and `den` within each group and returns
# their ratio.

# %%
hand = {"A_morning": None, "B_morning": None, "A_evening": None, "B_evening": None, "A_all": None, "B_all": None}  # ✏️

def rates(df, by, num, den):
    """Sum num and den within each group of `by`, return num / den."""
    # BEGIN SOLUTION
    g = df.groupby(by)[[num, den]].sum()
    return g[num] / g[den]
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"A_morning": 0.04, "B_morning": 0.05, "A_evening": 0.10, "B_evening": 0.12,
            "A_all": 32 / 350, "B_all": 16 / 250}
    # END SOLUTION

# %%
ovens = pd.DataFrame({"oven": ["A", "B", "A", "B"], "shift": ["morning", "morning", "evening", "evening"],
                      "burnt": [2, 10, 30, 6], "trays": [50, 200, 300, 50]})
try:
    by_shift = rates(ovens, ["oven", "shift"], "burnt", "trays")
    overall = rates(ovens, "oven", "burnt", "trays")
except NotImplementedError:
    by_shift = ovens.set_index(["oven", "shift"])["burnt"] / ovens.set_index(["oven", "shift"])["trays"]
    overall = ovens.groupby("oven")["burnt"].sum() / ovens.groupby("oven")["trays"].sum()
print(by_shift.round(4), "\n", overall.round(4))
if hand["A_all"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["A_all"] is not None:
    code = {"A_morning": by_shift[("A", "morning")], "B_morning": by_shift[("B", "morning")],
            "A_evening": by_shift[("A", "evening")], "B_evening": by_shift[("B", "evening")],
            "A_all": overall["A"], "B_all": overall["B"]}
    U.check(all(abs(hand[k] - code[k]) < 0.001 for k in code), "hand and code agree")

# %% [markdown]
# Oven A burns fewer trays in each shift and more overall, because most of its trays are in the
# evening, when every oven burns more. Hold on to that shape.

# %% [markdown]
# ## 3 · The display, all branches together
#
# Compute the waste rate (wasted / baked) of display and non-display branches over the six months.

# %%
try:
    by_display = rates(waste, "display", "wasted", "baked")
except NotImplementedError:
    g = waste.groupby("display")[["wasted", "baked"]].sum()
    by_display = g["wasted"] / g["baked"]
U.keep("w3_overall", by_display.to_dict())
print(by_display.round(4))
print(f"display minus no display: {100 * (by_display[1] - by_display[0]):+.2f} points")

# %% [markdown]
# ## 4 · Within each branch size
#
# Now the same comparison within small branches and within large branches.

# %%
try:
    by_size = rates(waste, ["size", "display"], "wasted", "baked").unstack()
except NotImplementedError:
    g = waste.groupby(["size", "display"])[["wasted", "baked"]].sum()
    by_size = (g["wasted"] / g["baked"]).unstack()
by_size["difference_points"] = 100 * (by_size[1] - by_size[0])
U.keep("w3_within", by_size.round(5).to_dict())
print(by_size.round(4))
U.check((by_size["difference_points"] < 0).all() and by_display[1] > by_display[0],
        "the display is better within each size and worse overall")

# %% [markdown]
# ## 5 · Who chose the display?
#
# Write `display_share(waste)`: for each branch size, the share of branches (not rows) that got
# the display, and the waste rate of that size without the display. Then explain the paradox in
# one sentence in `why`.

# %%
def display_share(waste):
    # BEGIN SOLUTION
    branches = waste.drop_duplicates("branch")
    share = branches.groupby("size")["display"].mean()
    base = rates(waste[waste["display"] == 0], "size", "wasted", "baked")
    return pd.DataFrame({"share_with_display": share, "rate_without_display": base})
    # END SOLUTION

def explain():
    """✏️ One sentence: why the display looks worse overall."""
    # BEGIN SOLUTION
    return ("Managers put the display mostly in large branches, which waste more whatever their shelf, so the "
            "display group is weighted towards high-waste branches: size confounds the overall comparison.")
    # END SOLUTION

# %%
try:
    share = display_share(waste)
except NotImplementedError:
    share = pd.DataFrame(U.reference("w3_share"))
U.keep("w3_share", share.round(5).to_dict())
print(share.round(4))
try:
    print("why:", explain())
except NotImplementedError:
    print("✏️ write explain()")

# %% [markdown]
# Branch size is a **confounder**: it affects the waste rate and it affected who got the display.
# Adjusting for it here was possible because we knew it and recorded it. A confounder nobody
# recorded cannot be adjusted for, which is why the next study was randomised.

# %% [markdown]
# ## 6 · The randomised trial
#
# Twelve branches drawn at random gave an evening discount on the day's bread. Write
# `trial_effect(trial)`: the mean change in waste rate (after − before) of the discount branches,
# of the others, and the difference, in percentage points.

# %%
def trial_effect(trial):
    # BEGIN SOLUTION
    change = trial["waste_rate_after"] - trial["waste_rate_before"]
    m = change.groupby(trial["discount"]).mean()
    return {"discount": float(100 * m[1]), "control": float(100 * m[0]), "difference": float(100 * (m[1] - m[0]))}
    # END SOLUTION

# %%
try:
    eff = trial_effect(trial)
except NotImplementedError:
    eff = U.reference("w3_trial")
U.keep("w3_trial", eff)
print({k: round(v, 3) for k, v in eff.items()}, "(percentage points)")
U.check(eff["difference"] < 0, "the discount branches cut waste more than the others")

# %% [markdown]
# ## 7 · Balance
#
# Randomisation does not make the groups identical; it makes them differ only by chance, in
# everything, recorded or not. Count large branches and sectors in each arm of the trial, and in
# the display and non-display groups.

# %%
def balance(df, arm):
    b = df.drop_duplicates("branch")
    return pd.concat({"large": b.groupby(arm)["size"].apply(lambda s: int((s == "large").sum())),
                      "branches": b.groupby(arm).size()}, axis=1)

bal_trial, bal_display = balance(trial, "discount"), balance(waste, "display")
U.keep("w3_balance", {"trial": bal_trial.to_dict(), "display": bal_display.to_dict()})
print("trial:\n", bal_trial, "\ndisplay:\n", bal_display)
print(pd.crosstab(trial["sector"], trial["discount"]))

# %% [markdown]
# ## 8 · How this was checked

# %%
def write_note():
    # BEGIN SOLUTION
    return {
        "result": f"The display looks {100 * (by_display[1] - by_display[0]):+.2f} points worse overall but is "
                  f"{-by_size['difference_points'].max():.2f} to {-by_size['difference_points'].min():.2f} points better within "
                  f"each size; the randomised discount changed waste by {eff['difference']:+.2f} points against control.",
        "checked_by": "rates() agreed with the oven table by hand; the within-size rates were recomputed from the "
                      "branch-month rows; balance tables count branches, not rows.",
        "limits": "The display comparison adjusts for size only: other choices by managers may confound it. The trial "
                  "has 24 branches, so its difference carries real chance variation (a permutation test, week 6, can say how much).",
        "reviewer": "The operations manager's analyst reruns both tables before the shelf decision.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. Why can't a bigger observational dataset of display branches remove the confounding?
#
# <details><summary>Answer</summary>More rows make the estimate more precise, not less biased:
# the display would still sit mostly in large branches.</details>
#
# 2. The trial's two arms have the same number of large branches. Was that guaranteed?
#
# <details><summary>Answer</summary>No; it happened by chance this time. Randomisation guarantees
# only that any imbalance is due to chance.</details>
#
# 3. A colleague says "the display raises waste by about a point". What do you reply?
#
# <details><summary>Answer</summary>That is the overall comparison, confounded by branch size.
# Within each size the display branches waste less. Neither is proof: only a randomised test of
# the display would settle it.</details>
#
# ## Carry forward
#
# Week 6 asks whether the trial's difference could be chance, with a permutation test.

# %% [markdown]
# ## ✱ Stretch
#
# Standardise: apply each size's display and non-display rates to the chain's total baked units
# per size, and compare the two standardised rates.

# %%
def stretch():
    # BEGIN SOLUTION
    w = waste.groupby("size")["baked"].sum() / waste["baked"].sum()
    std = {d: float((by_size[d] * w).sum()) for d in (0, 1)}
    print({k: round(v, 4) for k, v in std.items()}, "difference", round(100 * (std[1] - std[0]), 2), "points")
    # END SOLUTION


U.optional(stretch)
