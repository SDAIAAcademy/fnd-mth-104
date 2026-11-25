# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "pandas>=2.2", "statsmodels>=0.14"]
# ///
# %% [markdown]
# # Lab 7.1 · Twenty tests on pure noise, with and without correction
#
# Week 7 · Session 1 (Multiple testing and false discoveries) · 105 min.
#
# The chain sent a promotion flyer to 12 of its 24 branches, drawn at random, and the finance
# analyst's dashboard tests all twenty product lines L01 to L20 for a change in weekly units
# (`data/promo.csv`). Two lines come out "significant". You know something the dashboard does not:
# the data were generated with **no true effect on any line**. You measure, by simulating a
# thousand such dashboards, how often uncorrected testing produces false findings, and what the
# family-wise (Bonferroni, Holm) and false-discovery-rate (Benjamini-Hochberg) corrections do.
#
# **AI policy.** AI-tutor: hints, never answers (`labs/tutor/TUTOR.md`).
#
# **Tasks**
# - [ ] 1 · Set up; the promotion dashboard (10 min)
# - [ ] 2 · Bonferroni, Holm and Benjamini-Hochberg by hand on five p-values (15 min)
# - [ ] 3 · Twenty permutation tests on the dashboard (15 min)
# - [ ] 4 · The three corrections on the dashboard (10 min)
# - [ ] 5 · A thousand dashboards of pure noise: the table of false-finding rates (25 min)
# - [ ] 6 · Forking paths: one line, eight reasonable analyses (15 min)
# - [ ] 7 · Record how this was checked (15 min)
# - [ ] ✱ Stretch · Give four lines a true effect and compare Bonferroni with Benjamini-Hochberg

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
from statsmodels.stats.multitest import multipletests
import sta as U

print("quick mode:", U.QUICK)
ALPHA = 0.05
R = U.pick(2000, 400)          # permutations per test
DASHBOARDS = U.pick(1000, 200)  # simulated dashboards

# %% [markdown]
# ## 1 · The dashboard
#
# One row per branch and product line: whether the branch got the flyer, and the change in weekly
# units sold after it. Twenty lines, 24 branches each.

# %%
promo = U.load("promo.csv")
wide = promo.pivot(index="branch", columns="line", values="change_units")
flyer = promo.drop_duplicates("branch").set_index("branch").loc[wide.index, "flyer"].to_numpy().astype(bool)
print(wide.shape, "| flyer branches:", int(flyer.sum()))

# %% [markdown]
# ## 2 · Three corrections by hand
#
# **On paper.** Five p-values from another department's report: 0.004, 0.011, 0.020, 0.030,
# 0.400; α = 0.05, m = 5.
#
# - **Bonferroni**: reject when p ≤ α / m.
# - **Holm**: sort the p-values; compare the k-th smallest with α / (m − k + 1); reject while the
#   comparisons hold, stop at the first that fails.
# - **Benjamini-Hochberg (BH)**: sort; find the largest k with p₍ₖ₎ ≤ k α / m; reject the k smallest.
#
# How many does each reject? Put the three counts in `hand`. Then write the three functions, each
# returning a boolean array of rejections in the original order.

# %%
hand = {"bonferroni": None, "holm": None, "bh": None}   # ✏️

def bonferroni(p, alpha=ALPHA):
    p = np.asarray(p, dtype=float)
    # BEGIN SOLUTION
    return p <= alpha / len(p)
    # END SOLUTION

def holm(p, alpha=ALPHA):
    p = np.asarray(p, dtype=float)
    # BEGIN SOLUTION
    m, order = len(p), np.argsort(p)
    reject = np.zeros(m, bool)
    for k, i in enumerate(order):
        if p[i] <= alpha / (m - k):
            reject[i] = True
        else:
            break
    return reject
    # END SOLUTION

def bh(p, alpha=ALPHA):
    p = np.asarray(p, dtype=float)
    # BEGIN SOLUTION
    m, order = len(p), np.argsort(p)
    ok = p[order] <= alpha * np.arange(1, m + 1) / m
    reject = np.zeros(m, bool)
    if ok.any():
        reject[order[: np.nonzero(ok)[0].max() + 1]] = True
    return reject
    # END SOLUTION

def reference_hand():
    # BEGIN SOLUTION
    return {"bonferroni": 1, "holm": 2, "bh": 4}
    # END SOLUTION

def corrections(p):
    """The three corrections, with the library's as the safety net."""
    out = {}
    for name, fn, method in [("bonferroni", bonferroni, "bonferroni"), ("holm", holm, "holm"), ("bh", bh, "fdr_bh")]:
        try:
            out[name] = fn(p)
        except NotImplementedError:
            out[name] = multipletests(p, alpha=ALPHA, method=method)[0]
    return out

# %%
five = [0.004, 0.011, 0.020, 0.030, 0.400]
c5 = corrections(five)
counts5 = {k: int(v.sum()) for k, v in c5.items()}
print("rejections:", counts5)
for name, method in [("bonferroni", "bonferroni"), ("holm", "holm"), ("bh", "fdr_bh")]:
    U.check((c5[name] == multipletests(five, alpha=ALPHA, method=method)[0]).all(), f"{name} agrees with statsmodels")
if hand["bh"] is None:
    try:
        hand = reference_hand()
    except NotImplementedError:
        pass
if hand["bh"] is not None:
    U.check(hand == counts5, "hand and code agree")

# %% [markdown]
# ## 3 · Twenty permutation tests
#
# Write `perm_pvalues(V, group, R, rng)`. `V` is a branches × lines array, `group` a boolean
# array of branches. Shuffle the group labels `R` times (the **same** shuffles for every line,
# as one draw of the flyer would be), and return one two-sided p-value per line for the difference
# in means, `(count + 1) / (R + 1)`. Make it fast with matrix products: for a boolean matrix of
# shuffled labels `M` (R × branches), the group means of every line are `V.T @ M.T / 12`.

# %%
def perm_pvalues(V, group, R, rng):
    V, group = np.asarray(V, dtype=float), np.asarray(group, dtype=bool)
    n1 = group.sum()
    n0 = len(group) - n1
    obs = V[group].mean(axis=0) - V[~group].mean(axis=0)
    # BEGIN SOLUTION
    M = np.array([rng.permutation(group) for _ in range(R)], dtype=float)
    diffs = V.T @ M.T / n1 - V.T @ (1 - M).T / n0          # lines × R
    count = (np.abs(diffs) >= np.abs(obs)[:, None] - 1e-12).sum(axis=1)
    return (count + 1) / (R + 1)
    # END SOLUTION

def safe_pvalues(V, group, R, rng):
    try:
        return perm_pvalues(V, group, R, rng)
    except NotImplementedError:  # the safety net: Welch's t test, close to the permutation test here
        V, group = np.asarray(V, dtype=float), np.asarray(group, dtype=bool)
        return stats.ttest_ind(V[group], V[~group], axis=0, equal_var=False).pvalue

# %%
p20 = safe_pvalues(wide.to_numpy(), flyer, R, np.random.default_rng(71))
dash = pd.DataFrame({"line": wide.columns, "p": p20.round(4)})
dash["uncorrected"] = dash["p"] <= ALPHA
U.keep("w7_dashboard", dash.to_dict(orient="list"))
print(dash.sort_values("p").head(6).to_string(index=False))
print("uncorrected findings:", list(dash.loc[dash["uncorrected"], "line"]))

# %% [markdown]
# ## 4 · The corrections on the dashboard

# %%
c20 = corrections(p20)
for k, v in c20.items():
    dash[k] = v
print(dash.loc[dash["uncorrected"]].to_string(index=False))
print("findings after correction:", {k: int(v.sum()) for k, v in c20.items()})

# %% [markdown]
# ## 5 · A thousand dashboards of pure noise
#
# Write `noise_dashboard(rng)`: a new dashboard like this one with no effect anywhere (24
# branches, 12 with the flyer drawn at random, 20 lines of normal noise with the same spreads as
# the real lines). Then, for each of `DASHBOARDS` simulated dashboards, test the twenty lines and
# record: the share of single tests that are false findings; whether the dashboard has at least one
# false finding (the **family-wise** error) without correction and with each correction; and the
# number of false findings. Here every finding is false, so the false discovery rate equals the
# family-wise rate: the stretch shows where the two part.

# %%
line_sd = wide.std(ddof=1).to_numpy()

def noise_dashboard(rng):
    # BEGIN SOLUTION
    V = rng.normal(0.0, line_sd, size=(24, 20))
    g = np.zeros(24, bool)
    g[rng.choice(24, 12, replace=False)] = True
    return V, g
    # END SOLUTION

def simulate(n_dash, R, seed):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n_dash):
        try:
            V, g = noise_dashboard(rng)
        except NotImplementedError:
            V = rng.normal(0.0, line_sd, size=(24, 20))
            g = np.zeros(24, bool)
            g[rng.choice(24, 12, replace=False)] = True
        p = safe_pvalues(V, g, R, rng)
        c = corrections(p)
        rows.append({"single_tests_rejected": float((p <= ALPHA).mean()),
                     "any_uncorrected": bool((p <= ALPHA).any()), "n_uncorrected": int((p <= ALPHA).sum()),
                     **{f"any_{k}": bool(v.any()) for k, v in c.items()}})
    return pd.DataFrame(rows)

sim = simulate(DASHBOARDS, U.pick(500, 200), 72)
table = pd.DataFrame({
    "procedure": ["single test, uncorrected", "uncorrected, at least one of 20", "Bonferroni", "Holm", "Benjamini-Hochberg"],
    "false_finding_rate": [sim["single_tests_rejected"].mean(), sim["any_uncorrected"].mean(),
                           sim["any_bonferroni"].mean(), sim["any_holm"].mean(), sim["any_bh"].mean()],
})
table["mc_error"] = np.sqrt(table["false_finding_rate"] * (1 - table["false_finding_rate"]) / DASHBOARDS)
U.keep("w7_rates", table.round(4).to_dict(orient="list"))
U.keep("w7_mean_false", float(sim["n_uncorrected"].mean()))
print(table.round(3).to_string(index=False))
print(f"average false findings per uncorrected dashboard: {sim['n_uncorrected'].mean():.2f} (expected 20 × 0.05 = 1) | at least one, in theory: 1 − 0.95²⁰ = {1 - 0.95 ** 20:.3f}")
U.check(table["false_finding_rate"].iloc[1] > 0.45 and table["false_finding_rate"].iloc[2] < 0.10,
        "uncorrected testing finds something in most noise dashboards; Bonferroni rarely does")

# %% [markdown]
# ## 6 · Forking paths
#
# No dashboard needed to go wrong: one analyst, one line, and a few reasonable choices. Write
# `paths(V1, g, size, rng)` that tests ONE line eight ways: all branches; large branches only;
# small branches only; and each of those with the most extreme branch removed (6 paths); plus the
# median difference on all branches and on large ones (2 more). Return the eight p-values. Then
# measure over noise dashboards how often the **smallest** of the eight is below 0.05.

# %%
size_large = (promo.drop_duplicates("branch").set_index("branch").loc[wide.index, "size"] == "large").to_numpy()

def p_perm(x, g, stat, R, rng):
    obs = stat(x[g]) - stat(x[~g])
    d = np.array([stat(x[p]) - stat(x[~p]) for p in (rng.permutation(g) for _ in range(R))])
    return (np.sum(np.abs(d) >= abs(obs) - 1e-12) + 1) / (R + 1)

def paths(v, g, large, rng, R):
    # BEGIN SOLUTION
    out = []
    for subset in [np.ones_like(g), large, ~large]:
        x, gg = v[subset], g[subset]
        out.append(p_perm(x, gg, np.mean, R, rng))
        keep = np.abs(x - x.mean()) < np.abs(x - x.mean()).max()
        out.append(p_perm(x[keep], gg[keep], np.mean, R, rng))
    for subset in [np.ones_like(g), large]:
        out.append(p_perm(v[subset], g[subset], np.median, R, rng))
    return np.array(out)
    # END SOLUTION

# %%
rngf = np.random.default_rng(73)
n_f = U.pick(300, 60)
smallest, first = [], []
for _ in range(n_f):
    v = rngf.normal(0, 1, 24)
    g = np.zeros(24, bool)
    g[rngf.choice(24, 12, replace=False)] = True
    try:
        ps = paths(v, g, size_large, rngf, U.pick(300, 150))
    except NotImplementedError:
        ps = np.array([p_perm(v, g, np.mean, U.pick(300, 150), rngf)])
    smallest.append(ps.min() <= ALPHA)
    first.append(ps[0] <= ALPHA)
fork = {"one_planned_test": float(np.mean(first)), "best_of_paths": float(np.mean(smallest)), "dashboards": n_f}
U.keep("w7_forking", fork)
print(f"one planned test: {fork['one_planned_test']:.3f} false findings | best of eight paths: {fork['best_of_paths']:.3f} ({n_f} noise lines)")

# %% [markdown]
# The analyst never ran twenty tests on purpose. The paths were each defensible; choosing among
# them after seeing the data is what inflates the rate. The cure is to write the analysis down
# before looking: the outcome, the groups, the test and what to do with outliers.

# %% [markdown]
# ## 7 · How this was checked

# %%
def write_note():
    # BEGIN SOLUTION
    t = table.set_index("procedure")["false_finding_rate"]
    return {
        "result": f"The two 'significant' lines on the dashboard are what noise produces: in {DASHBOARDS} simulated noise "
                  f"dashboards, {100 * t['uncorrected, at least one of 20']:.0f}% showed at least one finding uncorrected, "
                  f"{100 * t['Bonferroni']:.1f}% with Bonferroni, {100 * t['Holm']:.1f}% with Holm, {100 * t['Benjamini-Hochberg']:.1f}% with BH. "
                  f"After any correction the real dashboard has {int(c20['bh'].sum())} findings.",
        "checked_by": "The three corrections agreed with a hand case and with statsmodels; the single-test rate came out near "
                      f"0.05 ({t['single test, uncorrected']:.3f}) and the family rate near 1 − 0.95²⁰ = 0.642.",
        "limits": "All twenty lines are pure noise here, so the false discovery rate and the family-wise rate coincide; with "
                  "real effects they part (see the stretch). The forking-path rate depends on the eight paths chosen.",
        "reviewer": "The finance analyst's manager reruns the simulation with a new seed before the dashboard is reissued.",
    }
    # END SOLUTION


# %%
check_note = U.note(write_note)

# %% [markdown]
# ## Checkpoint questions
#
# 1. A dashboard tests 20 lines with no true effect at α = 0.05. About how many false findings
#    should you expect, and how often at least one?
#
# <details><summary>Answer</summary>About one on average (20 × 0.05), and at least one in about
# 64% of dashboards (1 − 0.95²⁰).</details>
#
# 2. Why does Holm never reject fewer hypotheses than Bonferroni?
#
# <details><summary>Answer</summary>Its first comparison is Bonferroni's; every later threshold is
# larger. It controls the same family-wise rate with more power.</details>
#
# 3. An analyst tested one line, but chose the subset of branches after looking. Is that one test?
#
# <details><summary>Answer</summary>No. The choices that could have been made count as tests
# too: the forking-path rate was several times 5%.</details>
#
# ## Carry forward
#
# Week 8 asks the other question: when there IS an effect, how often does the test find it?

# %% [markdown]
# ## ✱ Stretch
#
# Give lines L01 to L04 a true effect of one standard deviation and the other sixteen none.
# Over 300 dashboards, compare Bonferroni and BH on the false discovery proportion (false findings
# among all findings) and on power (true effects found).

# %%
def stretch():
    # BEGIN SOLUTION
    rng = np.random.default_rng(74)
    rows = []
    for _ in range(U.pick(300, 60)):
        V, g = noise_dashboard(rng)
        V[g, :4] += line_sd[:4]
        p = perm_pvalues(V, g, U.pick(500, 200), rng)
        for name, rej in [("Bonferroni", bonferroni(p)), ("BH", bh(p))]:
            found = rej.sum()
            rows.append({"procedure": name, "fdp": rej[4:].sum() / found if found else 0.0, "power": rej[:4].mean()})
    print(pd.DataFrame(rows).groupby("procedure").mean().round(3))
    # END SOLUTION


U.optional(stretch)
