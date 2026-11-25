"""The auto-checker of the weekly problem sets (PS1 to PS8).

The last cell of each problem-set notebook calls `pscheck.check(n, globals())`. It prints one line
per item and a score. It checks two things, and stores no answer:

- agreement: each hand answer agrees, within a tolerance, with the result of your own function on
  the same small case;
- correctness of the code: your functions are run on fresh random data and checked against
  properties (a reproducible seed, an interval that contains its estimate, a rate near its
  theoretical value) or against SciPy and statsmodels.

A hand answer left as None scores nothing; so does a function that is not written yet.
"""
from __future__ import annotations

import sys

import numpy as np

for _stream in (sys.stdout, sys.stderr):  # a Windows console may not default to UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

TOL = 1e-3


def _close(a, b, tol=TOL) -> bool:
    try:
        return bool(np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol, rtol=tol))
    except (TypeError, ValueError):
        return False


def _run(fn, *args):
    try:
        return fn(*args), None
    except NotImplementedError:
        return None, "not written yet"
    except Exception as e:  # noqa: BLE001 - a learner's error is a result, not a crash
        return None, f"{type(e).__name__}: {e}"


def _agree(ns, key, fn_name, *args, pick=None, tol=TOL):
    """A hand answer against the learner's own function on the same case."""
    hand = (ns.get("hand") or {}).get(key)
    if hand is None:
        return False, "hand answer missing"
    fn = ns.get(fn_name)
    if fn is None:
        return False, f"function {fn_name} missing"
    got, err = _run(fn, *args)
    if err:
        return False, err
    if pick is not None:
        got = pick(got)
    ok = _close(hand, got, tol)
    return ok, "" if ok else "hand and code differ"


def _code(ns, fn_name, test):
    fn = ns.get(fn_name)
    if fn is None:
        return False, f"function {fn_name} missing"
    try:
        ok = bool(test(fn))
        return ok, "" if ok else "wrong on a random test case"
    except NotImplementedError:
        return False, "not written yet"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _rng():
    return np.random.default_rng(2027)


# ---------------------------------------------------------------- PS1 describing data
def _ps1(ns):
    from scipy import stats
    x = ns["x"]
    yield "1a hand median agrees with median_iqr(x)", _agree(ns, "median", "median_iqr", x, pick=lambda r: r[0])
    yield "1b hand IQR agrees with median_iqr(x)", _agree(ns, "iqr", "median_iqr", x, pick=lambda r: r[1])
    z = _rng().lognormal(3, 0.7, 301)
    q1, q3 = np.percentile(z, [25, 75])
    yield "2 median_iqr matches NumPy on random skewed data", _code(ns, "median_iqr", lambda f: _close(f(z), (np.median(z), q3 - q1)))
    yield "3 mad matches SciPy's median absolute deviation", _code(ns, "mad", lambda f: _close(f(z), stats.median_abs_deviation(z)))
    w = np.where(_rng().random(200) < 0.1, np.nan, 1.0)
    yield "4 missing_share counts missing values", _code(ns, "missing_share", lambda f: _close(f(w), np.isnan(w).mean()))


# ---------------------------------------------------------------- PS2 sampling variation
def _ps2(ns):
    pop4 = ns["pop4"]
    yield "1 hand standard error agrees with exact_se(pop4, 2)", _agree(ns, "se", "exact_se", pop4, 2)
    z = _rng().normal(0, 1, 5000)
    yield "2 exact_se matches σ/√n × finite-population factor on a random population", _code(
        ns, "exact_se", lambda f: _close(f(z[:8], 3), np.std(z[:8]) / np.sqrt(3) * np.sqrt((8 - 3) / (8 - 1)), 1e-6))
    yield "3 se_by_simulation is near σ/√n at n = 25", _code(
        ns, "se_by_simulation", lambda f: abs(f(z, 25, 2000, 1) - np.std(z) / 5) < 0.02)
    yield "4 se_by_simulation reruns identically with the same seed", _code(
        ns, "se_by_simulation", lambda f: f(z, 25, 300, 7) == f(z, 25, 300, 7))


# ---------------------------------------------------------------- PS3 confounding
def _ps3(ns):
    import pandas as pd
    t = ns["table"]
    yield "1a hand overall rate of X agrees with rates_by", _agree(ns, "X_all", "rates_by", t, "unit", "bad", "total",
                                                                  pick=lambda s: s["X"])
    yield "1b hand overall rate of Y agrees with rates_by", _agree(ns, "Y_all", "rates_by", t, "unit", "bad", "total",
                                                                  pick=lambda s: s["Y"])
    r = _rng()
    df = pd.DataFrame({"g": r.choice(["a", "b", "c"], 60), "num": r.integers(0, 10, 60), "den": r.integers(10, 30, 60)})
    want = df.groupby("g")["num"].sum() / df.groupby("g")["den"].sum()
    yield "2 rates_by sums before dividing", _code(ns, "rates_by", lambda f: _close(f(df, "g", "num", "den").sort_index(), want.sort_index()))
    simpson = pd.DataFrame({"unit": ["X", "Y", "X", "Y"], "stratum": ["s1", "s1", "s2", "s2"],
                            "bad": [1, 8, 40, 9], "total": [50, 200, 400, 60]})
    plain = pd.DataFrame({"unit": ["X", "Y", "X", "Y"], "stratum": ["s1", "s1", "s2", "s2"],
                          "bad": [1, 8, 10, 30], "total": [50, 200, 200, 300]})
    yield "3 reverses() flags a reversal and only a reversal", _code(
        ns, "reverses", lambda f: f(simpson, "unit", "stratum", "bad", "total") is True
        and f(plain, "unit", "stratum", "bad", "total") is False)


# ---------------------------------------------------------------- PS4 the bootstrap
def _ps4(ns):
    yield "1 hand bootstrap SE agrees with all_resample_se([1, 3])", _agree(ns, "boot_se", "all_resample_se", [1, 3])
    z = _rng().normal(10, 2, 200)

    def ok(f):
        a, b = f(z, np.mean, 2000, 5), f(z, np.mean, 2000, 5)
        lo, hi = a
        return a == b and lo < z.mean() < hi and abs((hi - lo) - 2 * 1.96 * 2 / np.sqrt(200)) < 0.15

    yield "2 percentile_ci: reproducible, contains the mean, about the right width", _code(ns, "percentile_ci", ok)
    yield "3 percentile_ci works for the median too", _code(
        ns, "percentile_ci", lambda f: f(z, np.median, 1000, 3)[0] < np.median(z) < f(z, np.median, 1000, 3)[1])
    small = np.array([1.0, 2.0, 2.5, 3.0, 40.0])
    said = (ns.get("hand") or {}).get("forty_inside")
    if said is None:
        item4 = (False, "hand answer missing")
    else:
        item4 = _code(ns, "percentile_ci", lambda f: (lambda c: (c[0] <= 40 <= c[1]) == bool(said))(f(small, np.mean, 4000, 1)))
    yield "4 hand yes/no (is 40 inside the interval for the mean of the five values?) agrees with percentile_ci", item4


# ---------------------------------------------------------------- PS5 differences and slopes
def _ps5(ns):
    px, py = ns["px"], ns["py"]
    yield "1 hand slope agrees with slope(px, py)", _agree(ns, "slope", "slope", px, py)
    r = _rng()
    x = r.uniform(0, 10, 80)
    y = 3 + 0.7 * x + r.normal(0, 1, 80)
    yield "2 slope matches the library fit", _code(ns, "slope", lambda f: _close(f(x, y), np.polyfit(x, y, 1)[0], 1e-6))
    a, b = r.lognormal(2, 0.8, 150), r.lognormal(2.2, 0.8, 120)

    def ok(f):
        c1, c2 = f(a, b, np.mean, 2000, 11), f(a, b, np.mean, 2000, 12)
        w = c1[1] - c1[0]
        return c1[0] < a.mean() - b.mean() < c1[1] and max(abs(c1[0] - c2[0]), abs(c1[1] - c2[1])) < 0.15 * w

    yield "3 diff_ci contains the observed difference and agrees on rerun with a new seed", _code(ns, "diff_ci", ok)
    yield "4 diff_ci gives the exact difference when both groups are constant", _code(
        ns, "diff_ci", lambda f: f(np.zeros(5), np.ones(50), np.mean, 200, 1) == (-1.0, -1.0))


# ---------------------------------------------------------------- PS6 permutation tests
def _ps6(ns):
    yield "1 hand p-value agrees with exact_p([1, 2], [4, 6])", _agree(ns, "p", "exact_p", [1, 2], [4, 6])
    r = _rng()
    same = r.normal(0, 1, (2, 30))
    far = np.vstack([r.normal(0, 1, 30), r.normal(3, 1, 30)])
    yield "2 perm_p: tiny for a three-SD shift", _code(ns, "perm_p", lambda f: f(far[0], far[1], 999, 1) <= 0.01)
    yield "3 perm_p: never zero, never above one", _code(
        ns, "perm_p", lambda f: 0 < f(far[0], far[1], 99, 2) <= 1 and 0 < f(same[0], same[1], 99, 2) <= 1)

    def unif(f):
        ps = [f(*r.normal(0, 1, (2, 12)), 199, int(s)) for s in range(200)]
        return abs(np.mean(np.array(ps) <= 0.05) - 0.05) < 0.04

    yield "4 perm_p rejects about 5% of true nulls", _code(ns, "perm_p", unif)


# ---------------------------------------------------------------- PS7 corrections
def _ps7(ns):
    from statsmodels.stats.multitest import multipletests
    p5 = ns["p5"]
    for k, fn in [("bonferroni", "bonferroni"), ("holm", "holm"), ("bh", "bh")]:
        yield f"1 hand count for {k} agrees with {fn}(p5)", _agree(ns, k, fn, p5, pick=lambda v: int(np.sum(v)))
    ps = _rng().uniform(0, 0.08, 25)
    for name, method in [("bonferroni", "bonferroni"), ("holm", "holm"), ("bh", "fdr_bh")]:
        yield f"2 {name} matches statsmodels on 25 random p-values", _code(
            ns, name, lambda f, m=method: bool((np.asarray(f(ps)) == multipletests(ps, 0.05, m)[0]).all()))
    yield "3 familywise_rate is near 1 − 0.95^m for m = 10", _code(
        ns, "familywise_rate", lambda f: abs(f(10, 0.05, 4000, 3) - (1 - 0.95 ** 10)) < 0.03)


# ---------------------------------------------------------------- PS8 error rates and power
def _ps8(ns):
    from statsmodels.stats.power import TTestIndPower
    for k in ["false_findings", "true_findings", "false_share"]:
        yield f"1 hand {k} agrees with expected_findings", _agree(ns, k, "expected_findings", 50, 50, 0.05, 0.8,
                                                                 pick=lambda d, k=k: d[k])
    yield "2 rejection_rate near 0.05 with no effect", _code(ns, "rejection_rate", lambda f: abs(f(30, 0.0, 3000, 1) - 0.05) < 0.02)
    want = TTestIndPower().power(effect_size=0.5, nobs1=40, alpha=0.05)
    yield "3 rejection_rate near the t-test power formula for d = 0.5, n = 40", _code(
        ns, "rejection_rate", lambda f: abs(f(40, 0.5, 3000, 2) - want) < 0.04)


SETS = {1: _ps1, 2: _ps2, 3: _ps3, 4: _ps4, 5: _ps5, 6: _ps6, 7: _ps7, 8: _ps8}


def check(n: int, ns: dict) -> float:
    items = list(SETS[n](ns))
    score = 0
    for label, (ok, why) in items:
        score += ok
        print(("[ok]  " if ok else "[--]  ") + label + ("" if ok else f"  ({why})"))
    print(f"Problem set {n}: {score} of {len(items)} items")
    return score / len(items)
