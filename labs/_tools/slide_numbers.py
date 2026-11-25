# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.1", "scipy>=1.15", "statsmodels>=0.14"]
# ///
"""Recompute every number the slides quote that does not come from a lab run.

    uv run python _tools/slide_numbers.py     (from labs/)

The slides use parallel examples (other departments, other numbers) before each lab, so that no
lab answer is shown before the lab; the numbers after a lab come from its solution run
(solutions/answer_key.md).
"""
from itertools import combinations

import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower

print("== week 1: nine catering orders")
orders = np.array([40, 45, 50, 52, 55, 58, 60, 75, 400], dtype=float)
for label, x in [("as recorded", orders), ("400 keyed as 4000", np.r_[orders[:-1], 4000.0])]:
    q1, q3 = np.percentile(x, [25, 75])
    print(f"{label}: mean {x.mean():.2f} median {np.median(x):.2f} trimmed20 {stats.trim_mean(x, 0.2):.2f} "
          f"sd {x.std(ddof=1):.2f} Q1 {q1:.2f} Q3 {q3:.2f} IQR {q3 - q1:.2f} high fence {q3 + 1.5 * (q3 - q1):.2f}")

print("== week 2: standard error by formula")
for s, n in [(12, 36), (12, 144), (12, 576)]:
    print(f"sigma {s}, n {n}: se {s / np.sqrt(n):.2f}")
print("all samples of 2 from [3, 9, 12]:", [np.mean(c) for c in combinations([3, 9, 12], 2)],
      "sd", round(float(np.std([np.mean(c) for c in combinations([3, 9, 12], 2)])), 4))

print("== week 3: two packing lines")
P = {"rolls": (6, 200), "cakes": (40, 400)}
Q = {"rolls": (20, 500), "cakes": (13, 100)}
for name, d in [("P", P), ("Q", Q)]:
    within = {k: round(a / b, 4) for k, (a, b) in d.items()}
    print(name, within, "overall", round(sum(a for a, _ in d.values()) / sum(b for _, b in d.values()), 4))

print("== week 4: bootstrap of five deliveries, and coverage on a normal population")
five = np.array([12, 15, 18, 22, 60], dtype=float)
r = np.random.default_rng(4)
for _ in range(3):
    s = r.choice(five, 5)
    print("resample", s, "mean", s.mean())
r = np.random.default_rng(44)
for n in [10, 40]:
    hits = 0
    for _ in range(2000):
        x = r.normal(50, 10, n)
        b = x[r.integers(0, n, (2000, n))].mean(axis=1)
        lo, hi = np.percentile(b, [2.5, 97.5])
        hits += lo <= 50 <= hi
    print(f"normal population, n = {n}: percentile coverage {hits / 2000:.3f}")

print("== week 5: two oven settings, bake minutes (synthetic)")
r = np.random.default_rng(5)
a = np.round(r.gamma(4, 5, 60), 1)
b = np.round(r.gamma(4, 4.2, 50), 1)
d = [r.choice(a, 60).mean() - r.choice(b, 50).mean() for _ in range(4000)]
print(f"means {a.mean():.2f} {b.mean():.2f} diff {a.mean() - b.mean():.2f} interval {np.percentile(d, [2.5, 97.5]).round(2)}")
x = np.arange(1, 6, dtype=float)
y = np.array([2.0, 4, 5, 4, 7])
print("slope of 5 points:", np.polyfit(x, y, 1)[0])

print("== week 6: shuffle example")
g1, g2 = np.array([3.0, 4, 6]), np.array([7.0, 9, 11])
pooled = np.r_[g1, g2]
obs = g2.mean() - g1.mean()
ds = []
for idx in combinations(range(6), 3):
    m = np.zeros(6, bool)
    m[list(idx)] = True
    ds.append(pooled[~m].mean() - pooled[m].mean())
ds = np.array(ds)
print(f"observed {obs:.3f}; splits {len(ds)}; |d| >= obs: {(np.abs(ds) >= obs - 1e-12).sum()} -> p {(np.abs(ds) >= obs - 1e-12).mean():.3f}")

print("== week 7: chance of at least one false finding, and a six-test example")
for m in [1, 5, 10, 20, 50]:
    print(f"m = {m}: 1 - 0.95^m = {1 - 0.95 ** m:.3f}; expected false findings {0.05 * m:.2f}")
p6 = np.array([0.001, 0.006, 0.012, 0.019, 0.044, 0.31])
for method in ["bonferroni", "holm", "fdr_bh"]:
    print(method, multipletests(p6, 0.05, method)[0].astype(int), "rejections", multipletests(p6, 0.05, method)[0].sum())

print("== week 8: power of the t test for a 0.5 SD difference (formula)")
for n in [10, 30, 100]:
    print(f"n = {n} per group: power {TTestIndPower().power(effect_size=0.5, nobs1=n, alpha=0.05):.3f}")
print("100 ideas, 10 real, alpha 0.05, power 0.5: false", 90 * 0.05, "true", 10 * 0.5, "share false", round(4.5 / 9.5, 3))
