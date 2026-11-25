# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 4.1 · Bootstrap intervals with coverage checked against a known truth
#
# Week 4 · Session 1 (The bootstrap and its coverage) · 105 min.
#
# In real work you have one sample and no truth. The bootstrap treats the sample as a stand-in
# for the population and resamples it to see how much a statistic varies. Here you also have the
# truth: the quarter's 40,000 baskets (`data/population.csv`). So you can build intervals from
# one sample, then draw a thousand samples and count how often the interval really contains the
# population mean or median. That count is the interval's **coverage**.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; one sample and the truth (10 min)
# - [ ] 2 · Every resample of a sample of two, by hand (10 min)
# - [ ] 3 · A percentile bootstrap for any statistic (20 min)
# - [ ] 4 · Intervals for the mean and the median from one sample of 50 (10 min)
# - [ ] 5 · Coverage by simulation at n = 10, 30 and 100 (25 min)
# - [ ] 6 · Compare with SciPy's bootstrap: percentile and its default method (15 min)
# - [ ] 7 · Record how this was checked (15 min)
# - [ ] ✱ Stretch · The coverage of the t interval for the mean at the same sizes

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
SEED = 4104
B = U.pick(2000, 500)          # resamples per interval
REPS = U.pick(1000, 200)       # samples in the coverage study

# %% [markdown]
# ## 1 · One sample, and the truth
#
# Draw one sample of 50 baskets. Keep the truth aside: you will only look at it in task 5.

# %%
pop = U.load("population.csv")["value"].to_numpy()
truth = {"mean": float(pop.mean()), "median": float(np.median(pop))}
rng = np.random.default_rng(SEED)
sample = rng.choice(pop, 50, replace=False)
print("sample of 50: mean", round(sample.mean(), 3), "| median", round(float(np.median(sample)), 3))

# %% [markdown]
# ## 2 · Every resample of a sample of two
#
# **On paper.** A sample of two baskets: 2 and 6 riyals. A bootstrap resample draws two values
# *with replacement*. List the four equally likely resamples, the mean of each, and the standard
# deviation of those four means (divide by 4). That standard deviation is the bootstrap standard
# error of the mean. Put it in `hand`. Then write `all_resample_means(x)` for any small sample.

# %%
hand = {"boot_se": None}   # ✏️

def all_resample_means(x):
    """Means of all n**n equally likely ordered resamples of a small sample."""
    from itertools import product
    # BEGIN SOLUTION
    return np.array([np.mean(r) for r in product(x, repeat=len(x))])
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"boot_se": 1.4142}
    # END SOLUTION

# %%
try:
    m2 = all_resample_means([2, 6])
except NotImplementedError:
    m2 = np.array([2.0, 4.0, 4.0, 6.0])
print("resample means:", m2, "| bootstrap SE:", round(m2.std(), 4))
if hand["boot_se"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["boot_se"] is not None:
    U.check(abs(hand["boot_se"] - m2.std()) < 0.01, "hand and code agree")

# %% [markdown]
# ## 3 · A percentile bootstrap
#
# Write `boot_ci(x, stat, B, rng, level=0.95)`:
#
# 1. draw `B` resamples of `x`, each of the same size, with replacement;
# 2. compute `stat` on each (make it fast: draw a `B × n` matrix of indices and call
#    `stat(x[idx], axis=1)`);
# 3. return the `(1 − level)/2` and `(1 + level)/2` percentiles of the `B` statistics.
#
# `stat` is a NumPy function with an `axis` argument, such as `np.mean` or `np.median`.

# %%
def boot_ci(x, stat, B, rng, level=0.95):
    x = np.asarray(x, dtype=float)
    # BEGIN SOLUTION
    idx = rng.integers(0, len(x), size=(B, len(x)))
    boots = stat(x[idx], axis=1)
    a = (1 - level) / 2
    lo, hi = np.percentile(boots, [100 * a, 100 * (1 - a)])
    return float(lo), float(hi)
    # END SOLUTION

def safe_ci(x, stat, B, rng, level=0.95):
    try:
        return boot_ci(x, stat, B, rng, level)
    except NotImplementedError:
        idx = rng.integers(0, len(x), size=(B, len(x)))
        b = stat(np.asarray(x)[idx], axis=1)
        return tuple(float(v) for v in np.percentile(b, [2.5, 97.5]))

# %% [markdown]
# ## 4 · Intervals from one sample of 50
#
# Compute 95% intervals for the mean and the median of `sample`. Then run them again with a new
# seed: by how much do the ends move? (The outcome LO4 asks for intervals that agree on rerun.)

# %%
ci = {}
for name, stat in [("mean", np.mean), ("median", np.median)]:
    a = safe_ci(sample, stat, B, np.random.default_rng(1))
    b = safe_ci(sample, stat, B, np.random.default_rng(2))
    ci[name] = {"seed1": a, "seed2": b, "largest_move": float(max(abs(a[0] - b[0]), abs(a[1] - b[1])))}
    print(f"{name:6s} seed 1: {a[0]:.2f} to {a[1]:.2f} | seed 2: {b[0]:.2f} to {b[1]:.2f} | largest move {ci[name]['largest_move']:.3f}")
U.keep("w4_one_sample", ci)
U.check(all(v["largest_move"] < 0.6 for v in ci.values()), "intervals agree on rerun to within a few tenths of a riyal")

# %% [markdown]
# Now look at the truth: does each interval contain it? One interval tells you nothing about how
# often the method works. Task 5 counts.

# %%
for name in ci:
    lo, hi = ci[name]["seed1"]
    print(f"{name}: truth {truth[name]:.3f} {'inside' if lo <= truth[name] <= hi else 'OUTSIDE'} {lo:.2f} to {hi:.2f}")

# %% [markdown]
# ## 5 · Coverage
#
# Write `coverage(pop, stat, n, reps, B, rng)`: draw `reps` samples of size `n` from the
# population, build a 95% percentile interval from each, and return the share of intervals that
# contain the population value of `stat`. A 95% method should be near 0.95. Also return the
# average width.

# %%
def coverage(pop, stat, n, reps, B, rng):
    target = float(stat(pop))
    # BEGIN SOLUTION
    hits, widths = 0, []
    for _ in range(reps):
        x = rng.choice(pop, n, replace=False)
        lo, hi = boot_ci(x, stat, B, rng)
        hits += lo <= target <= hi
        widths.append(hi - lo)
    return hits / reps, float(np.mean(widths))
    # END SOLUTION

# %%
rows = []
for n in [10, 30, 100]:
    for name, stat in [("mean", np.mean), ("median", np.median)]:
        try:
            cov, width = coverage(pop, stat, n, REPS, B, np.random.default_rng(SEED + n))
        except NotImplementedError:
            ref = U.reference("w4_coverage")
            k = [i for i, r in enumerate(zip(ref["n"], ref["statistic"])) if r == (n, name)][0]
            cov, width = ref["coverage"][k], ref["mean_width"][k]
        rows.append({"n": n, "statistic": name, "coverage": cov, "mean_width": width})
cov_table = pd.DataFrame(rows)
cov_table["mc_error"] = np.sqrt(cov_table["coverage"] * (1 - cov_table["coverage"]) / REPS)
U.keep("w4_coverage", cov_table.round(4).to_dict(orient="list"))
print(cov_table.round(3).to_string(index=False))
print(f"({REPS} samples per row: a coverage estimate carries a Monte Carlo error of about ±{2 * np.sqrt(0.95 * 0.05 / REPS):.3f})")
mean10 = cov_table.query("n == 10 and statistic == 'mean'")["coverage"].iloc[0]
mean100 = cov_table.query("n == 100 and statistic == 'mean'")["coverage"].iloc[0]
U.check(mean10 < mean100, "the bootstrap interval for the mean under-covers most at the smallest n")

# %% [markdown]
# **Look at** the n = 10 rows. On a long-tailed population a small sample rarely contains the
# rare large baskets, so its resamples cannot show how far the mean can move: the interval is too
# narrow. The bootstrap assumes the sample looks like the population; at n = 10 it does not.

# %% [markdown]
# ## 6 · SciPy's bootstrap
#
# `scipy.stats.bootstrap` does the same job. Its default method is BCa (bias-corrected and
# accelerated), not the percentile method. Compute both for the sample of 50 and compare with
# yours. (Why BCa adjusts the ends is taught in SPC-STA-201.)

# %%
sp = {}
for method in ["percentile", "BCa"]:
    res = stats.bootstrap((sample,), np.mean, n_resamples=B, method=method, rng=np.random.default_rng(1))
    sp[method] = (float(res.confidence_interval.low), float(res.confidence_interval.high))
    print(f"SciPy {method:10s}: {sp[method][0]:.2f} to {sp[method][1]:.2f}")
print(f"yours (percentile): {ci['mean']['seed1'][0]:.2f} to {ci['mean']['seed1'][1]:.2f}")
U.keep("w4_scipy", sp)
U.check(abs(sp["percentile"][0] - ci["mean"]["seed1"][0]) < 0.6, "your percentile interval agrees with SciPy's")

# %% [markdown]
# ## 7 · How this was checked

# %%
def write_note():
    # BEGIN SOLUTION
    c = cov_table.set_index(["n", "statistic"])["coverage"]
    return {
        "result": f"From 50 baskets the 95% bootstrap interval for the mean is {ci['mean']['seed1'][0]:.2f} to "
                  f"{ci['mean']['seed1'][1]:.2f} riyals; for the median {ci['median']['seed1'][0]:.2f} to {ci['median']['seed1'][1]:.2f}.",
        "checked_by": f"Rerun with a second seed (ends moved at most {max(v['largest_move'] for v in ci.values()):.2f}); "
                      f"agrees with SciPy's percentile method; coverage measured against the known truth: mean "
                      f"{c[(10, 'mean')]:.3f} at n = 10, {c[(100, 'mean')]:.3f} at n = 100.",
        "limits": "Percentile intervals under-cover for small samples from a long-tailed population; the coverage "
                  "figures hold for this population only.",
        "reviewer": "The customer insight lead's second analyst reruns the coverage study with a new seed.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. A 95% interval for the mean basket is 19.1 to 25.3 riyals. Is there a 95% chance that the
#    population mean is in it?
#
# <details><summary>Answer</summary>Not in the sense of the method: the population mean is fixed.
# The method produces intervals that contain it in about 95% of samples (if its coverage is
# right); this one either does or does not.</details>
#
# 2. Why does more resampling (larger B) not fix the coverage at n = 10?
#
# <details><summary>Answer</summary>B only reduces the noise of the resampling. The problem is
# the sample itself: ten baskets rarely show the tail.</details>
#
# 3. Two reruns of your notebook with different seeds give ends that differ by 0.05. Is that a
#    problem?
#
# <details><summary>Answer</summary>No; it is resampling noise, small next to the width. Report
# the number of resamples; increase B if the ends move in the digits you report.</details>
#
# ## Carry forward
#
# Week 5 applies `boot_ci` to differences and slopes on public data. Keep it.

# %% [markdown]
# ## ✱ Stretch
#
# The classical t interval for the mean is x̄ ± t · s/√n. Measure its coverage at n = 10, 30 and
# 100 on the same population and compare with the bootstrap's.

# %%
def stretch():
    # BEGIN SOLUTION
    r = np.random.default_rng(99)
    for n in [10, 30, 100]:
        hits = 0
        for _ in range(REPS):
            x = r.choice(pop, n, replace=False)
            h = stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n)
            hits += x.mean() - h <= truth["mean"] <= x.mean() + h
        print(f"t interval, n = {n}: coverage {hits / REPS:.3f}")
    # END SOLUTION


U.optional(stretch)
