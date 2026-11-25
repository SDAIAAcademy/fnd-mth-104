# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 8.1 · Type I error rate and power of a permutation test estimated by simulation at three sample sizes
#
# Week 8 · Session 1 (Type I and II errors, power and reporting) · 105 min.
#
# The operations manager plans a trial of a breakfast bundle: some customers are offered it, the
# others are not, and the outcome is basket value. Before running it she asks: "How many baskets
# per group do we need, and how often would the test fool us?" You answer with the population of
# 40,000 baskets (`data/population.csv`) as a stand-in for the customers: you simulate the trial
# thousands of times with no effect (to measure the **Type I error rate**) and with a 10% uplift
# (to measure **power**), at 50, 200 and 800 baskets per group.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; the planned trial and its question (10 min)
# - [ ] 2 · Type I and II errors by hand (10 min)
# - [ ] 3 · A fast permutation test with fixed shuffles (15 min)
# - [ ] 4 · The Type I error rate at 50, 200 and 800 per group (20 min)
# - [ ] 5 · Power at the same sizes for a 10% uplift (20 min)
# - [ ] 6 · Effect size and practical significance (15 min)
# - [ ] 7 · The note, and your capstone plan (15 min)
# - [ ] ✱ Stretch · Welch's t test on the same trials

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
ALPHA = 0.05
SIMS = U.pick(1000, 200)   # simulated trials per setting
R = U.pick(500, 200)       # shuffles per test
SIZES = [50, 200, 800]
UPLIFT = 0.10

# %% [markdown]
# ## 1 · The planned trial
#
# Each simulated trial draws `2n` baskets from the population, gives the first `n` the bundle
# (their values are multiplied by 1 + uplift) and tests the difference in mean basket value. With
# uplift 0 every rejection is a **Type I error** (a false finding); with uplift 0.10 every
# non-rejection is a **Type II error** (a missed effect), and the rejection rate is the **power**.

# %%
pop = U.load("population.csv")["value"].to_numpy()
print(f"population: mean {pop.mean():.2f}, sd {pop.std():.2f}; a 10% uplift is {UPLIFT * pop.mean():.2f} riyals, "
      f"{UPLIFT * pop.mean() / pop.std():.2f} standard deviations")

# %% [markdown]
# ## 2 · A hundred trials, by hand
#
# **On paper.** A chain runs 100 trials over a year. In 80 the offer does nothing; in 20 it works.
# Each trial uses α = 0.05 and has power 0.5. How many false findings do you expect, how many
# true findings, and what share of all findings are false? Put the three numbers in `hand`.

# %%
hand = {"false_findings": None, "true_findings": None, "false_share": None}   # ✏️

def expected_findings(n_null, n_real, alpha, power):
    # BEGIN SOLUTION
    f, t = n_null * alpha, n_real * power
    return {"false_findings": f, "true_findings": t, "false_share": f / (f + t)}
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"false_findings": 4, "true_findings": 10, "false_share": 4 / 14}
    # END SOLUTION

# %%
try:
    ef = expected_findings(80, 20, 0.05, 0.5)
except NotImplementedError:
    ef = {"false_findings": 4.0, "true_findings": 10.0, "false_share": 4 / 14}
print({k: round(v, 4) for k, v in ef.items()})
if hand["false_share"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["false_share"] is not None:
    U.check(all(abs(hand[k] - ef[k]) < 0.01 for k in ef), "hand and code agree")

# %% [markdown]
# A p-value below 0.05 does not mean a 5% chance that the finding is false: here more than a
# quarter of the findings are. That share depends on power and on how many tested ideas are real.

# %% [markdown]
# ## 3 · A fast permutation test
#
# Thousands of trials times hundreds of shuffles is a lot of work. Draw the shuffles once per
# sample size: `shuffles(n, R, rng)` returns an `R × 2n` matrix of 0s and 1s, each row a random
# choice of which `n` of the `2n` baskets are "treated". Then `perm_p(x, M)` takes the `2n` values
# (treated first) and returns the two-sided p-value of the difference in means. One fixed set of
# random shuffles, drawn without looking at the data, gives a valid test.

# %%
def shuffles(n, R, rng):
    base = np.r_[np.ones(n), np.zeros(n)]
    return np.array([rng.permutation(base) for _ in range(R)])

def perm_p(x, M):
    n = len(x) // 2
    obs = x[:n].mean() - x[n:].mean()
    # BEGIN SOLUTION
    d = (M @ x) / n - ((1 - M) @ x) / n
    return (np.sum(np.abs(d) >= abs(obs) - 1e-12) + 1) / (len(M) + 1)
    # END SOLUTION

def safe_p(x, M):
    try:
        return perm_p(x, M)
    except NotImplementedError:
        n = len(x) // 2
        return stats.ttest_ind(x[:n], x[n:], equal_var=False).pvalue

# %%
rng3 = np.random.default_rng(83)
xc = rng3.choice(pop, 120, replace=False)
mine = safe_p(xc, shuffles(60, 4000, rng3))
ref = stats.permutation_test((xc[:60], xc[60:]), lambda a, b, axis: np.mean(a, axis=axis) - np.mean(b, axis=axis),
                             vectorized=True, n_resamples=4000, rng=rng3).pvalue
print(f"one null trial of 60 per group: your p = {mine:.4f} | SciPy's p = {ref:.4f}")
U.check(abs(mine - ref) < 0.05, "your test agrees with SciPy's on one trial")

# %% [markdown]
# ## 4 · The Type I error rate
#
# Write `rejection_rate(pop, n, uplift, sims, R, rng)`: draw `M = shuffles(n, R, rng)` once, then
# `sims` times draw `2n` baskets, multiply the first `n` by `1 + uplift`, test, and return the
# share of trials with p ≤ α. Run it with uplift 0 at the three sizes.

# %%
def rejection_rate(pop, n, uplift, sims, R, rng):
    M = shuffles(n, R, rng)
    # BEGIN SOLUTION
    hits = 0
    for _ in range(sims):
        x = rng.choice(pop, 2 * n, replace=False)
        x[:n] *= 1 + uplift
        hits += perm_p(x, M) <= ALPHA
    return hits / sims
    # END SOLUTION

def safe_rate(n, uplift, seed):
    rng = np.random.default_rng(seed)
    try:
        return rejection_rate(pop, n, uplift, SIMS, R, rng)
    except NotImplementedError:
        M = shuffles(n, R, rng)
        hits = 0
        for _ in range(SIMS):
            x = rng.choice(pop, 2 * n, replace=False)
            x[:n] *= 1 + uplift
            hits += safe_p(x, M) <= ALPHA
        return hits / SIMS

# %%
type1 = {n: safe_rate(n, 0.0, 800 + n) for n in SIZES}
for n, r in type1.items():
    print(f"n = {n:3d} per group: Type I error rate {r:.3f} ± {2 * np.sqrt(r * (1 - r) / SIMS):.3f}")
TOL1 = max(0.03, 3 * np.sqrt(ALPHA * (1 - ALPHA) / SIMS))  # three Monte Carlo errors
U.check(all(abs(r - ALPHA) < TOL1 for r in type1.values()), "the Type I error rate stays near 0.05 at every size")

# %% [markdown]
# ## 5 · Power
#
# Now with a 10% uplift. Power is the share of trials that find the effect.

# %%
power = {n: safe_rate(n, UPLIFT, 900 + n) for n in SIZES}
res = pd.DataFrame({"n_per_group": SIZES, "type1_rate": [type1[n] for n in SIZES], "power_10pc": [power[n] for n in SIZES]})
res["type2_rate"] = 1 - res["power_10pc"]
res["mc_error"] = np.sqrt(res["power_10pc"] * (1 - res["power_10pc"]) / SIMS)
U.keep("w8_rates", res.round(4).to_dict(orient="list"))
print(res.round(3).to_string(index=False))
U.check(res["power_10pc"].is_monotonic_increasing, "power grows with the sample size")

# %% [markdown]
# **Look at** the n = 50 row. A trial that small misses a real 10% uplift most of the time, and a
# "no significant difference" from it says almost nothing. (Choosing the sample size properly, for
# a stated minimum effect, is SPC-STA-201 and SPC-EXP-201.)

# %% [markdown]
# ## 6 · Effect size and practical significance
#
# Simulate ONE trial at n = 200 with the 10% uplift. Report the difference in mean basket value
# with a bootstrap interval, then compare it with the smallest uplift the finance analyst says is
# worth the bundle's cost: 1.50 riyals a basket. Write `practical(ci, threshold)` returning
# "worth it", "not worth it" or "unclear" from where the interval sits.

# %%
def practical(ci, threshold):
    lo, hi = ci
    # BEGIN SOLUTION
    if lo >= threshold:
        return "worth it"
    if hi < threshold:
        return "not worth it"
    return "unclear"
    # END SOLUTION

# %%
rng6 = np.random.default_rng(86)
x = rng6.choice(pop, 400, replace=False)
x[:200] *= 1 + UPLIFT
t, c = x[:200], x[200:]
p_one = safe_p(x, shuffles(200, U.pick(2000, 500), rng6))
boots = [rng6.choice(t, 200).mean() - rng6.choice(c, 200).mean() for _ in range(U.pick(2000, 400))]
ci = tuple(float(v) for v in np.percentile(boots, [2.5, 97.5]))
try:
    verdict = practical(ci, 1.50)
except NotImplementedError:
    verdict = "✏️ write practical()"
one = {"diff": float(t.mean() - c.mean()), "ci": ci, "p": float(p_one), "verdict": verdict}
U.keep("w8_one_trial", one)
print(f"difference {one['diff']:.2f} riyals (95% interval {ci[0]:.2f} to {ci[1]:.2f}), p = {p_one:.4f} -> {verdict}")

# %% [markdown]
# Whatever the p-value, the interval is what tells the manager whether the bundle pays for itself.
# "Statistically significant" and "worth doing" are different questions.

# %% [markdown]
# ## 7 · How this was checked, and your capstone
#
# Write the note. Then, in the markdown cell below it, write three lines for your capstone: the
# public dataset you will use and its licence, your question, and the estimate, interval and test
# you plan, written down **before** you look at the results (week 7's forking paths).

# %%
def write_note():
    # BEGIN SOLUTION
    return {
        "result": f"With a 10% uplift, the permutation test finds it in {100 * power[50]:.0f}% of trials at 50 baskets per group, "
                  f"{100 * power[200]:.0f}% at 200 and {100 * power[800]:.0f}% at 800, while its false-finding rate stays near 5% "
                  f"({', '.join(f'{type1[n]:.3f}' for n in SIZES)}).",
        "checked_by": f"{SIMS} simulated trials per setting, Monte Carlo error about ±{2 * res['mc_error'].max():.3f}; the test "
                      "agreed with SciPy's permutation test on one trial; Type I rates near α, within the check's tolerance of 0.03; one set of shuffles serves all the trials of a size, so the rates also move a little with that set.",
        "limits": "The population stands in for the customers; the uplift is multiplicative and the same for everyone; "
                  "baskets are treated as independent, which a trial randomised by branch would not be.",
        "reviewer": "The finance analyst reruns the power table with a new seed before the trial size is agreed.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# **My capstone plan** ✏️
#
# - Dataset and licence:
# - Question:
# - Estimate, interval and test, fixed before I look:

# %% [markdown]
# ## Checkpoint questions
#
# 1. A trial of 50 baskets per group finds "no significant difference". What can you conclude?
#
# <details><summary>Answer</summary>Very little: at that size the test misses a real 10% uplift
# most of the time. Report the interval, which will be wide.</details>
#
# 2. Why does the Type I error rate not fall as n grows, when power rises?
#
# <details><summary>Answer</summary>The test is built to reject a true null at rate α at any size.
# Sample size buys power, not a lower false-alarm rate.</details>
#
# 3. The interval for the uplift is 0.9 to 3.1 riyals and the bundle needs 1.50 to pay. Decision?
#
# <details><summary>Answer</summary>Unclear: the interval contains values on both sides of the
# threshold. A larger trial, or a decision that accepts that risk, not the p-value alone.</details>

# %% [markdown]
# ## ✱ Stretch
#
# Run Welch's t test on the same kind of simulated trials (uplift 10%, three sizes) and compare
# its power and Type I error rate with the permutation test's. Why might they differ most at n = 50?

# %%
def stretch():
    # BEGIN SOLUTION
    rng = np.random.default_rng(87)
    for n in SIZES:
        r0 = r1 = 0
        for _ in range(SIMS):
            x0 = rng.choice(pop, 2 * n, replace=False)
            r0 += stats.ttest_ind(x0[:n], x0[n:], equal_var=False).pvalue <= ALPHA
            x1 = rng.choice(pop, 2 * n, replace=False)
            x1[:n] *= 1 + UPLIFT
            r1 += stats.ttest_ind(x1[:n], x1[n:], equal_var=False).pvalue <= ALPHA
        print(f"Welch t, n = {n}: Type I {r0 / SIMS:.3f}, power {r1 / SIMS:.3f}")
    # END SOLUTION


U.optional(stretch)
