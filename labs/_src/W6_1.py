# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 6.1 · Permutation tests for a group difference and a correlation on public data
#
# Week 6 · Session 1 (Null models, p-values and effect sizes) · 105 min.
#
# Two stated questions on the two public-domain datasets bundled with statsmodels:
#
# - **Q1** In the RAND Health Insurance Experiment subset, do people on free care make a
#   different number of outpatient visits a year from people on the 95% coinsurance plan?
# - **Q2** In Engel's food expenditure data, is household food spending associated with income?
#
# You write the permutation test yourself, check it against a case you can enumerate by hand and
# against SciPy, and report each result as an effect size with an interval and a plain-language
# reading, not as a bare p-value.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; the two questions and their null models (10 min)
# - [ ] 2 · Every split of a tiny two-group sample, by hand (15 min)
# - [ ] 3 · A permutation test for a difference in means (20 min)
# - [ ] 4 · The effect size with an interval: difference and ratio of means (15 min)
# - [ ] 5 · A permutation test for a correlation (15 min)
# - [ ] 6 · Compare with SciPy's permutation test (10 min)
# - [ ] 7 · A plain-language reading of each result (10 min)
# - [ ] 8 · Record how this was checked (10 min)
# - [ ] ✱ Stretch · Q1 for participants in poor health only, and why it is weaker evidence

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

from itertools import combinations
import numpy as np
import pandas as pd
from scipy import stats
import sta as U

print("quick mode:", U.QUICK)
R = U.pick(5000, 1000)   # permutations
B = U.pick(2000, 400)    # bootstrap resamples

# %% [markdown]
# ## 1 · The questions and their null models
#
# A **null model** says how the data would arise if there were no effect. For Q1: the plan
# labels are exchangeable, since plans were assigned at random and, if the plan changed nothing,
# any relabelling of the people would be as likely as the real one. For Q2: incomes and food
# spending are paired at random. A permutation test computes the statistic under many such
# relabellings and asks how often it is as extreme as the one observed.

# %%
hie = U.health_experiment()
food = U.food_budgets()
free = hie.loc[hie["coins"] == 0, "visits"].to_numpy(dtype=float)
high = hie.loc[hie["coins"] == 95, "visits"].to_numpy(dtype=float)
print(f"Q1: free care n = {len(free)}, 95% coinsurance n = {len(high)}")
print(f"Q2: {len(food)} households")

# %% [markdown]
# ## 2 · Every split of a tiny sample
#
# **On paper.** Group A has 3 and 5; group B has 8, 10 and 12. The observed difference in means
# (B − A) is 6. Under the null, any 2 of the 5 values could have been group A: there are 10
# splits. List them, compute the difference for each, and count the splits with |difference| ≥ 6.
# The two-sided p-value is that count divided by 10. Put it in `hand`. Then write
# `exact_p(a, b)` that enumerates every split.

# %%
hand = {"p": None}   # ✏️

def exact_p(a, b):
    """Two-sided p-value of the difference in means, from every split of the pooled values."""
    pooled = np.concatenate([a, b]).astype(float)
    obs = abs(np.mean(b) - np.mean(a))
    # BEGIN SOLUTION
    count, total = 0, 0
    for idx in combinations(range(len(pooled)), len(a)):
        mask = np.zeros(len(pooled), bool)
        mask[list(idx)] = True
        d = abs(pooled[~mask].mean() - pooled[mask].mean())
        count += d >= obs - 1e-12
        total += 1
    return count / total
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"p": 0.1}
    # END SOLUTION

# %%
try:
    p_tiny = exact_p([3, 5], [8, 10, 12])
except NotImplementedError:
    p_tiny = 0.1
print("exact two-sided p:", p_tiny)
if hand["p"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["p"] is not None:
    U.check(abs(hand["p"] - p_tiny) < 1e-9, "hand and code agree")

# %% [markdown]
# ## 3 · A permutation test for a difference in means
#
# Write `perm_test_diff(x, y, R, rng)`: pool the two groups, shuffle the pooled values `R` times,
# split them into groups of the original sizes, and compute the difference in means each time.
# Return the observed difference and the two-sided p-value `(count + 1) / (R + 1)`, where
# `count` is the number of shuffles with |difference| ≥ |observed|. (The +1 counts the observed
# labelling as one of the possible ones, so a p-value is never exactly zero.)

# %%
def perm_test_diff(x, y, R, rng):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    obs = x.mean() - y.mean()
    # BEGIN SOLUTION
    pooled = np.concatenate([x, y])
    count = 0
    for _ in range(R):
        p = rng.permutation(pooled)
        count += abs(p[:len(x)].mean() - p[len(x):].mean()) >= abs(obs)
    return float(obs), (count + 1) / (R + 1)
    # END SOLUTION

def safe_perm_diff(x, y, R, rng):
    try:
        return perm_test_diff(x, y, R, rng)
    except NotImplementedError:  # the safety net: SciPy's test on the same data
        res = stats.permutation_test((x, y), lambda a, b, axis: np.mean(a, axis=axis) - np.mean(b, axis=axis),
                                     vectorized=True, n_resamples=R, rng=rng)
        return float(np.mean(x) - np.mean(y)), float(res.pvalue)

# %%
diff_obs, p_q1 = safe_perm_diff(free, high, R, np.random.default_rng(61))
print(f"Q1: observed difference {diff_obs:.3f} visits | permutation p = {p_q1:.5f} with {R} shuffles")
# the same test with no true effect: split free care at random into two groups
rng0 = np.random.default_rng(62)
shuffled = rng0.permutation(free)
null_diff, null_p = safe_perm_diff(shuffled[:5000], shuffled[5000:], U.pick(2000, 500), rng0)
print(f"two random halves of free care: difference {null_diff:.3f} | p = {null_p:.3f}")

# %% [markdown]
# **Look at** the smallest p-value the test can give: 1 / (R + 1). A p-value at that floor
# says "more extreme than every shuffle", not "zero".

# %% [markdown]
# ## 4 · The effect size, with an interval
#
# The p-value says the difference is unlikely under the null; it does not say how big it is.
# Report the **effect size**: the difference in mean visits and the ratio of the means, each with
# a 95% bootstrap interval (resample each group separately, as in week 5).

# %%
def effect_q1(x, y, B, rng):
    # BEGIN SOLUTION
    d, r = np.empty(B), np.empty(B)
    for b in range(B):
        xs, ys = rng.choice(x, len(x)), rng.choice(y, len(y))
        d[b], r[b] = xs.mean() - ys.mean(), xs.mean() / ys.mean()
    return {"diff": (float(x.mean() - y.mean()), *np.percentile(d, [2.5, 97.5]).tolist()),
            "ratio": (float(x.mean() / y.mean()), *np.percentile(r, [2.5, 97.5]).tolist())}
    # END SOLUTION

# %%
try:
    eff1 = effect_q1(free, high, B, np.random.default_rng(63))
except NotImplementedError:
    eff1 = U.reference("w6_q1")["effect"]
U.keep("w6_q1", {"diff": diff_obs, "p": p_q1, "effect": eff1})
print("difference in mean visits: {:.3f} (95% interval {:.3f} to {:.3f})".format(*eff1["diff"]))
print("ratio of mean visits:      {:.3f} (95% interval {:.3f} to {:.3f})".format(*eff1["ratio"]))

# %% [markdown]
# ## 5 · A permutation test for a correlation
#
# Write `perm_test_corr(x, y, R, rng)`: the observed Pearson correlation r, and the two-sided
# p-value from shuffling `y` against `x` `R` times. Then a bootstrap interval for r (resample
# households).

# %%
def perm_test_corr(x, y, R, rng):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    obs = np.corrcoef(x, y)[0, 1]
    # BEGIN SOLUTION
    count = sum(abs(np.corrcoef(x, rng.permutation(y))[0, 1]) >= abs(obs) for _ in range(R))
    return float(obs), (count + 1) / (R + 1)
    # END SOLUTION

# %%
x_inc, y_food = food["income"].to_numpy(), food["food"].to_numpy()
try:
    r_obs, p_q2 = perm_test_corr(x_inc, y_food, R, np.random.default_rng(64))
except NotImplementedError:
    ref = U.reference("w6_q2")
    r_obs, p_q2 = ref["r"], ref["p"]
rng5 = np.random.default_rng(65)
boots = []
for _ in range(B):
    i = rng5.integers(0, len(x_inc), len(x_inc))
    boots.append(np.corrcoef(x_inc[i], y_food[i])[0, 1])
r_ci = np.percentile(boots, [2.5, 97.5]).tolist()
U.keep("w6_q2", {"r": r_obs, "p": p_q2, "r_ci": r_ci})
print(f"Q2: r = {r_obs:.3f} (95% interval {r_ci[0]:.3f} to {r_ci[1]:.3f}) | permutation p = {p_q2:.5f}")

# %% [markdown]
# ## 6 · SciPy's permutation test
#
# `scipy.stats.permutation_test` runs the same idea. Check your Q1 p-value and your tiny exact
# p-value against it. (For the tiny case SciPy enumerates every split by itself.)

# %%
def mean_diff(a, b, axis):
    return np.mean(a, axis=axis) - np.mean(b, axis=axis)

res_tiny = stats.permutation_test(([3.0, 5.0], [8.0, 10.0, 12.0]), mean_diff, permutation_type="independent",
                                  n_resamples=np.inf, alternative="two-sided")
res_q1 = stats.permutation_test((free, high), mean_diff, permutation_type="independent", vectorized=True,
                                n_resamples=U.pick(2000, 500), alternative="two-sided", rng=np.random.default_rng(66))
res_less = stats.permutation_test(([3.0, 5.0], [8.0, 10.0, 12.0]), mean_diff, permutation_type="independent",
                                  n_resamples=np.inf, alternative="less")
print(f"SciPy tiny case: two-sided p = {res_tiny.pvalue:.4f}, one-sided p = {res_less.pvalue:.4f} (yours {p_tiny:.4f})")
print(f"SciPy Q1: p = {res_q1.pvalue:.5f} (yours {p_q1:.5f}; each is at its own floor, 1 / (shuffles + 1))")
U.keep("w6_scipy", {"tiny_two_sided": float(res_tiny.pvalue), "tiny_less": float(res_less.pvalue), "q1": float(res_q1.pvalue)})
U.check(abs(res_less.pvalue - p_tiny) < 1e-9, "your exact count matches SciPy's enumeration")

# %% [markdown]
# **Look at** the tiny case. SciPy's two-sided p-value is **twice the smaller one-sided p-value**;
# yours counts splits with |difference| at least as large. On a lopsided null distribution the two
# conventions differ (here 0.2 against 0.1). Neither is wrong: state which one you used.

# %% [markdown]
# ## 7 · A plain-language reading
#
# Write `readings()` returning one or two sentences per question for the operations manager's
# style of reader: the size of the effect, its interval, and what the test adds. Avoid "proves",
# "the probability that the null is true" and "significant" on its own.

# %%
def readings():
    # BEGIN SOLUTION
    return {
        "Q1": f"People on free care made about {eff1['diff'][0]:.1f} more doctor visits a year than people paying 95% of the cost "
              f"(interval {eff1['diff'][1]:.2f} to {eff1['diff'][2]:.2f}), about {100 * (eff1['ratio'][0] - 1):.0f}% more. "
              f"A gap this large almost never appeared when the plan labels were shuffled (p = {p_q1:.4f}, the smallest this test can give).",
        "Q2": f"Households with higher income spent more on food: the correlation is {r_obs:.2f} (interval {r_ci[0]:.2f} to {r_ci[1]:.2f}), "
              "and no shuffle of the pairs came close. This is an association in one survey, not a causal effect.",
    }
    # END SOLUTION

# %%
try:
    plain = readings()
    U.check(all(len(v) > 40 for v in plain.values()), "a reading for each question")
    for k, v in plain.items():
        print(f"{k}: {v}")
except NotImplementedError:
    print("✏️ write readings()")

# %% [markdown]
# ## 8 · How this was checked

# %%
def write_note():
    # BEGIN SOLUTION
    return {
        "result": f"Q1: free care +{eff1['diff'][0]:.2f} visits a year (interval {eff1['diff'][1]:.2f} to {eff1['diff'][2]:.2f}), "
                  f"permutation p = {p_q1:.4f}. Q2: r = {r_obs:.2f} (interval {r_ci[0]:.2f} to {r_ci[1]:.2f}), p = {p_q2:.4f}.",
        "checked_by": "exact_p() agreed with the hand enumeration and with SciPy's one-sided enumeration; perm_test_diff() agreed with SciPy's "
                      f"permutation test on Q1 (both at their floor); two random halves of one plan gave p = {null_p:.2f}, as a null should.",
        "limits": "Person-years are not independent people; the correlation is an association; both p-values sit at the "
                  "floor set by the number of shuffles.",
        "reviewer": "A second analyst reruns the notebook with new seeds and reads the plain-language sentences against the numbers.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. Your Q1 p-value is below 0.001. Does that mean the plan has a large effect?
#
# <details><summary>Answer</summary>No. With thousands of rows a small effect can give a tiny
# p-value. The size is in the difference and the ratio, with their intervals.</details>
#
# 2. Why is shuffling the plan labels a fair null model here, and when would it not be?
#
# <details><summary>Answer</summary>The plans were assigned at random, so under no effect the
# labels are exchangeable. If people had chosen their plans, the groups could differ for other
# reasons, and a small p-value would not isolate the plan.</details>
#
# 3. Two random halves of the free-care group give p = 0.84. What does that check?
#
# <details><summary>Answer</summary>That the test behaves under a known null: with no real
# difference, p-values are spread out rather than small. Week 8 measures how often it errs.</details>
#
# ## Carry forward
#
# Week 7 runs twenty such tests at once. Keep `perm_test_diff`.

# %% [markdown]
# ## ✱ Stretch
#
# Repeat Q1 for people in poor health only. Check the group sizes against the reporting rule
# first, then give the difference, its interval and the p-value. Why is this weaker evidence than
# the full comparison, and why should it not have been chosen after looking at the data?

# %%
def stretch():
    # BEGIN SOLUTION
    sub = hie[hie["health"] == "poor"]
    a = sub.loc[sub["coins"] == 0, "visits"].to_numpy(float)
    b = sub.loc[sub["coins"] == 95, "visits"].to_numpy(float)
    print("group sizes:", len(a), len(b), "| both at least", U.MIN_GROUP, ":", min(len(a), len(b)) >= U.MIN_GROUP)
    d, p = perm_test_diff(a, b, U.pick(2000, 500), np.random.default_rng(67))
    e = effect_q1(a, b, B, np.random.default_rng(68))
    print(f"poor health: difference {d:.2f} (interval {e['diff'][1]:.2f} to {e['diff'][2]:.2f}), p = {p:.3f}")
    # END SOLUTION


U.optional(stretch)
