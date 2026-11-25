# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 2.1 · Repeated sampling from a synthetic population
#
# Week 2 · Session 1 (Populations, samples and standard error) · 105 min.
#
# The customer insight lead wants to survey baskets instead of reading every till record, and
# asks how big a sample must be. Here, for once, you know the whole population: one quarter of
# the chain's 40,000 baskets (`data/population.csv`, synthetic). You draw thousands of samples
# from it, watch the statistic vary from sample to sample, measure the standard error by
# simulation, compare it with the formula, and see what a sampling frame that covers only loyalty
# members does to the answer.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; the quarter as a known population (10 min)
# - [ ] 2 · Every sample of a tiny population, by hand (10 min)
# - [ ] 3 · Two thousand samples at three sizes (20 min)
# - [ ] 4 · The standard error by simulation against s/√n (15 min)
# - [ ] 5 · The sampling distribution of the median (15 min)
# - [ ] 6 · A frame of loyalty members only (15 min)
# - [ ] 7 · The shape of the sampling distribution at n = 10 (10 min)
# - [ ] 8 · Record how this was checked (10 min)
# - [ ] ✱ Stretch · Does sixteen times n quarter the median's standard error too?

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
SEED = 2104
REPS = U.pick(2000, 400)

# %% [markdown]
# ## 1 · The population
#
# In real work the population is unknown: that is why we sample. Here it is known, so every
# statistic can be compared with the truth. The **parameters** are numbers of the population; a
# **statistic** is computed from a sample.

# %%
pop = U.load("population.csv")
values = pop["value"].to_numpy()
truth = {"mean": float(values.mean()), "median": float(np.median(values)), "sd": float(values.std(ddof=0))}
U.keep("w2_truth", truth)
print(f"N = {len(values):,} baskets | population mean {truth['mean']:.3f} | median {truth['median']:.2f} | sd {truth['sd']:.3f}")
print("members:", f"{pop['member'].mean():.1%}", "| skewness:", round(float(stats.skew(values)), 2))

# %% [markdown]
# ## 2 · Every sample of a tiny population
#
# **On paper.** A population of four baskets: 10, 14, 20, 36 riyals. List all six samples of size
# two (without replacement), the mean of each, and the mean and the standard deviation (divide by
# the number of samples) of those six means. Put them in `hand`. Then write
# `all_sample_means(pop, n)` and check your hand work.

# %%
hand = {"mean_of_means": None, "sd_of_means": None}   # ✏️ your hand results

def all_sample_means(population, n):
    """The means of every sample of size n drawn without replacement."""
    # BEGIN SOLUTION
    return np.array([np.mean(c) for c in combinations(population, n)])
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"mean_of_means": 20.0, "sd_of_means": 5.7155}
    # END SOLUTION

# %%
tiny = [10, 14, 20, 36]
try:
    means2 = all_sample_means(tiny, 2)
except NotImplementedError:
    means2 = np.array(U.reference("w2_tiny_means"))
U.keep("w2_tiny_means", means2)
print("sample means:", means2, "| their mean:", means2.mean(), "| their sd:", round(means2.std(), 4))
U.check(abs(means2.mean() - np.mean(tiny)) < 1e-12, "the mean of all sample means is the population mean")
if hand["mean_of_means"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["mean_of_means"] is not None:
    U.check(abs(hand["mean_of_means"] - means2.mean()) < 0.01 and abs(hand["sd_of_means"] - means2.std()) < 0.01,
            "hand and code agree")

# %% [markdown]
# ## 3 · Two thousand samples at three sizes
#
# Write `sampling_distribution(values, stat, n, reps, rng)`: draw `reps` samples of size `n`
# without replacement and return the statistic of each. Use `rng.choice(values, n, replace=False)`.

# %%
def sampling_distribution(values, stat, n, reps, rng):
    # BEGIN SOLUTION
    return np.array([stat(rng.choice(values, n, replace=False)) for _ in range(reps)])
    # END SOLUTION

def safe_sd(values, stat, n, reps, seed):
    rng = np.random.default_rng(seed)
    try:
        return sampling_distribution(values, stat, n, reps, rng)
    except NotImplementedError:
        return np.array([stat(rng.choice(values, n, replace=False)) for _ in range(reps)])

# %%
sizes = [25, 100, 400]
dist_mean = {n: safe_sd(values, np.mean, n, REPS, SEED + n) for n in sizes}
for n in sizes:
    d = dist_mean[n]
    print(f"n = {n:3d}: centre of the {REPS} sample means {d.mean():.3f} (truth {truth['mean']:.3f}) | "
          f"middle 95% {np.percentile(d, 2.5):.2f} to {np.percentile(d, 97.5):.2f}")
U.check(abs(dist_mean[400].mean() - truth["mean"]) < 0.25, "sample means centre on the population mean")

# %% [markdown]
# ## 4 · The standard error
#
# The **standard error** of a statistic is the standard deviation of its sampling distribution:
# how far the statistic typically lands from the truth. Compare the simulated standard error of
# the mean with the formula σ/√n (σ from the population), and with s/√n from one single sample,
# which is all you have in real work. Write `se_table(dist, sizes, sigma, one_sample_s)`.

# %%
def se_table(dist, sizes, sigma, one_sample_s):
    # BEGIN SOLUTION
    return pd.DataFrame({
        "n": sizes,
        "se_simulated": [float(np.std(dist[n], ddof=1)) for n in sizes],
        "sigma_over_root_n": [sigma / np.sqrt(n) for n in sizes],
        "s_over_root_n_one_sample": [one_sample_s[n] / np.sqrt(n) for n in sizes],
    }).round(4)
    # END SOLUTION

# %%
rng1 = np.random.default_rng(SEED)
one_s = {n: float(np.std(rng1.choice(values, n, replace=False), ddof=1)) for n in sizes}
try:
    se = se_table(dist_mean, sizes, truth["sd"], one_s)
except NotImplementedError:
    se = pd.DataFrame(U.reference("w2_se"))
U.keep("w2_se", se.to_dict(orient="list"))
print(se.to_string(index=False))
ratio = se["se_simulated"].iloc[0] / se["se_simulated"].iloc[2]
print(f"sixteen times the sample size divides the standard error by {ratio:.2f} (√16 = 4)")
U.check(abs(ratio - 4) < 0.8, "the standard error shrinks like 1/√n")

# %% [markdown]
# **Look at** the last column. One sample's s/√n can be well off at n = 25 on a long-tailed
# population: one large basket in the sample inflates s.

# %% [markdown]
# ## 5 · The median
#
# The median has a standard error too, and no simple formula you can trust on a skewed
# population. Simulation gives it at once. Compute the sampling distribution of the median at the
# three sizes and its standard error.

# %%
dist_median = {n: safe_sd(values, np.median, n, REPS, SEED + 7 * n) for n in sizes}
med = pd.DataFrame({
    "n": sizes,
    "centre_of_medians": [float(dist_median[n].mean()) for n in sizes],
    "se_median": [float(np.std(dist_median[n], ddof=1)) for n in sizes],
    "se_mean": [float(np.std(dist_mean[n], ddof=1)) for n in sizes],
}).round(4)
U.keep("w2_median", med.to_dict(orient="list"))
print(med.to_string(index=False), "| population median", truth["median"])

# %% [markdown]
# ## 6 · A frame of loyalty members only
#
# The survey can only reach loyalty members, whose contact details the chain holds: the
# **sampling frame** is the members, not all customers. Write `frame_bias(pop, n, reps, rng)`
# returning the average of `reps` sample means drawn from members only, and compare with the
# truth. Then repeat with n = 1,600: does a bigger sample fix it?

# %%
def frame_bias(pop, n, reps, rng):
    # BEGIN SOLUTION
    members = pop.loc[pop["member"] == 1, "value"].to_numpy()
    return float(np.mean([rng.choice(members, n, replace=False).mean() for _ in range(reps)]))
    # END SOLUTION

# %%
out = {}
for n in [100, 1600]:
    try:
        out[n] = frame_bias(pop, n, U.pick(1000, 200), np.random.default_rng(SEED + n))
    except NotImplementedError:
        out[n] = U.reference("w2_frame")[str(n)]
U.keep("w2_frame", out)
for n, m in out.items():
    print(f"members-only frame, n = {n:4d}: average sample mean {m:.3f} | truth {truth['mean']:.3f} | bias {m - truth['mean']:+.3f}")
U.check(out[1600] - truth["mean"] > 1.0, "the frame bias does not shrink with n")

# %% [markdown]
# A larger sample shrinks the standard error, not the bias. The frame decides which question
# the sample answers.

# %% [markdown]
# ## 7 · The shape at n = 10
#
# FND-MTH-103 showed the central limit theorem: sample means tend to a normal shape as n
# grows. On a population this skewed, how normal are the means of samples of 10? Compute the
# skewness of the sampling distribution of the mean at n = 10 and at n = 400.

# %%
d10 = safe_sd(values, np.mean, 10, REPS, SEED + 10)
shape = {"skew_n10": float(stats.skew(d10)), "skew_n400": float(stats.skew(dist_mean[400]))}
U.keep("w2_shape", shape)
print({k: round(v, 3) for k, v in shape.items()})

# %% [markdown]
# ## 8 · How this was checked
#
# Write the note for the customer insight lead: what sample size you would advise and why, how
# you checked it, its limits, and who reruns it.

# %%
def write_note():
    # BEGIN SOLUTION
    return {
        "result": f"With 400 baskets the sample mean lands within about ±{2 * se['se_simulated'].iloc[2]:.2f} riyals of the "
                  f"quarter's mean in 95% of samples; with 25 it is about ±{2 * se['se_simulated'].iloc[0]:.2f}.",
        "checked_by": "Simulated standard errors agree with σ/√n; the tiny-population case was enumerated by hand; "
                      "the sample means centre on the known population mean.",
        "limits": f"Only for a frame that covers all customers: a members-only frame overstates the mean by about "
                  f"{out[1600] - truth['mean']:.2f} riyals at any sample size.",
        "reviewer": "The finance analyst reruns the notebook with a different seed before the survey is planned.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. The standard error of the mean at n = 100 is about 1.8 riyals. What does that number describe?
#
# <details><summary>Answer</summary>How far the mean of a sample of 100 typically lands from the
# population mean, from one sample to the next. Not the spread of basket values.</details>
#
# 2. Why does s/√n from one sample of 25 sometimes differ a lot from the simulated standard error?
#
# <details><summary>Answer</summary>s itself varies from sample to sample, and on a long-tailed
# population one large basket in a small sample can inflate it.</details>
#
# 3. A members-only survey of 1,600 baskets. Is it better than a random sample of 100 customers?
#
# <details><summary>Answer</summary>It is more precise about the wrong quantity: its bias stays the
# same at every n. A smaller sample from the right frame answers the question asked.</details>
#
# ## Carry forward
#
# Week 4 draws from the same population to check bootstrap intervals against the known mean and
# median. Keep `sampling_distribution`.

# %% [markdown]
# ## ✱ Stretch
#
# Show, with the medians from task 5, that the standard error of the median at n = 400 is about
# a quarter of the one at n = 25 (sixteen times the sample size), and say how close it is.

# %%
def stretch():
    # BEGIN SOLUTION
    r = med["se_median"].iloc[0] / med["se_median"].iloc[2]
    print(f"se of the median: n = 25 {med['se_median'].iloc[0]:.3f}, n = 400 {med['se_median'].iloc[2]:.3f}, ratio {r:.2f}")
    # END SOLUTION


U.optional(stretch)
