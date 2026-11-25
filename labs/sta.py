"""Helpers shared by the labs of Statistics by Simulation (FND-MTH-104).

    import sta as U

- U.QUICK is True when the environment variable STA_QUICK is 1: fewer resamples and repeats.
- U.pick(full, quick) returns the small value in quick mode.
- U.load(name) reads labs/data/<name> into a pandas DataFrame (the bakery chain's synthetic data).
- U.reference(name) reads labs/data/reference/<name>.json, the safety net of an exercise.
- U.check(condition, message) prints [ok] or raises AssertionError.
- U.keep(name, value) returns value; the trainer's tool (STA_WRITE_REF=1) also saves it as a
  reference file.
- U.health_experiment() and U.food_budgets() return the two public-domain datasets bundled with
  statsmodels, read from the installed package (no download).
- U.suppress(table, n_col, min_n) blanks the cells of groups smaller than min_n.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"
QUICK = os.environ.get("STA_QUICK", "0") == "1"

for _stream in (sys.stdout, sys.stderr):  # a Windows console may not default to UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

pd.set_option("display.width", 110)
pd.set_option("display.precision", 3)
np.set_printoptions(precision=4, suppress=True, linewidth=110)

# The course's own reporting rule: a group with fewer rows than this is not reported
MIN_GROUP = 30


def pick(full, quick):
    """The full value, or the small one in quick mode."""
    return quick if QUICK else full


def load(name: str) -> pd.DataFrame:
    """A CSV file of labs/data as a DataFrame."""
    return pd.read_csv(DATA / name)


def reference(name: str):
    """The reference result of an exercise, for the safety net."""
    return json.loads((REF / f"{name}.json").read_text(encoding="utf-8"))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError("not yet: " + message)
    print("[ok]", message)


def _round(obj, nd: int = 5):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, (list, tuple)):
        return [_round(x, nd) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, np.ndarray):
        return _round(obj.tolist(), nd)
    if isinstance(obj, np.generic):
        return _round(obj.item(), nd)
    return obj


def keep(name: str, value):
    """Return value; when STA_WRITE_REF=1 (the trainer's tool), also save it as a reference file."""
    if os.environ.get("STA_WRITE_REF") == "1":
        REF.mkdir(parents=True, exist_ok=True)
        (REF / f"{name}.json").write_text(json.dumps(_round(value), indent=1) + "\n", encoding="utf-8", newline="\n")
    return value


NOTE_KEYS = ("result", "checked_by", "limits", "reviewer")


def note(write_note) -> dict:
    """Run the participant's write_note(), check that the four parts are there, and print them.

    The note that ends every lab: the result, how it was checked, its limits, and who reruns it
    before it is used (a second person: the one who ran it does not sign it off alone).
    """
    try:
        n = write_note()
    except NotImplementedError:
        print("✏️ The note is not written yet: write_note() should return", ", ".join(NOTE_KEYS))
        return {k: None for k in NOTE_KEYS}
    check(isinstance(n, dict) and all(n.get(k) for k in NOTE_KEYS), "the note has its four parts")
    for k in NOTE_KEYS:
        print(f"{k}: {n[k]}")
    return n


def optional(fn) -> None:
    """Run a stretch exercise if it is written."""
    try:
        fn()
    except NotImplementedError:
        print("✱ stretch not attempted")


PLAN_OF = {0: "free care", 25: "25% coinsurance", 50: "50% coinsurance", 95: "95% coinsurance", 100: "100% coinsurance"}


def health_experiment() -> pd.DataFrame:
    """The RAND Health Insurance Experiment subset bundled with statsmodels (public domain).

    One row per person-year (20,190 rows). Columns used in the labs: `visits` (outpatient visits
    to a doctor in the year), `coins` (the coinsurance rate of the randomly assigned plan, in %),
    `plan` (its label), `health` (self-rated: excellent, good, fair, poor), `chronic` (a count
    index of chronic disease), `limited` (1 if a physical limitation).
    """
    from statsmodels.datasets import randhie

    d = randhie.load_pandas().data
    coins = np.rint(np.expm1(d["lncoins"])).astype(int)
    health = np.select([d["hlthp"] == 1, d["hlthf"] == 1, d["hlthg"] == 1], ["poor", "fair", "good"], "excellent")
    return pd.DataFrame({
        "visits": d["mdvis"].astype(int),
        "coins": coins,
        "plan": coins.map(PLAN_OF),
        "health": pd.Categorical(health, ["excellent", "good", "fair", "poor"], ordered=True),
        "chronic": d["disea"].round(2),
        "limited": d["physlm"].astype(int),
    })


def food_budgets() -> pd.DataFrame:
    """Engel's household income and food expenditure (235 households), bundled with statsmodels
    (public domain). Both columns are annual amounts in the historical currency of the survey."""
    from statsmodels.datasets import engel

    return engel.load_pandas().data.rename(columns={"foodexp": "food"})


def suppress(table: pd.DataFrame, n_col: str = "n", min_n: int = MIN_GROUP) -> pd.DataFrame:
    """Blank every column except the count of a group with fewer than min_n rows, and mark it."""
    out = table.copy()
    small = out[n_col] < min_n
    for c in out.columns:
        if c != n_col:
            out[c] = out[c].astype(object)
            out.loc[small, c] = "suppressed"
    out[n_col] = out[n_col].astype(object)
    out.loc[small, n_col] = f"< {min_n}"
    return out
