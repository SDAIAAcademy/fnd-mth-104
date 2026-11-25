# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Write the bakery chain's synthetic data into labs/data/ (seed 104, standard library only).

    uv run prepare_data.py        (from labs/)

The output is the same on every run and every machine: Python's `random` module keeps its
streams stable across versions. Every file is synthetic. The chain, its city and its people have
no names: branches are codes BR01 to BR24 in five generic sectors, product lines are L01 to L20,
baskets are BK- codes. Money is in riyals with two decimals.

Files and what is planted in them (the trainer's key is solutions/answer_key.md):

- baskets.csv      one month of 6 branches' baskets (lab 1.1): a long right tail, a real catering
                   order or two, one till error of 9999.00, waits missing more often in the
                   evening at the busiest branch, and one branch whose till writes -1 for a
                   missing wait.
- population.csv   one quarter of all 24 branches' baskets, 40,000 rows (labs 2.1, 4.1, 8.1): the
                   known population; loyalty members are about a third of baskets and spend more.
- waste.csv        24 branches by 6 months of baked and wasted units (lab 3.1): managers put the
                   new display shelf mostly in large branches, which waste more, so the display
                   looks worse overall and is better within each size (Simpson's paradox).
- trial.csv        the randomised evening-discount trial on the same 24 branches (lab 3.1).
- promo.csv        24 branches by 20 product lines (lab 7.1): weekly change in units after a
                   flyer sent to 12 branches chosen at random; no line has a true effect.
"""
from __future__ import annotations

import csv
import math
import random
from pathlib import Path

SEED = 104
DATA = Path(__file__).resolve().parent / "data"

SECTORS = ["North", "South", "East", "West", "Central"]
BRANCHES = [f"BR{i:02d}" for i in range(1, 25)]
SECTOR_OF = {b: SECTORS[i % 5] for i, b in enumerate(BRANCHES)}
# large branches: 12 of 24
LARGE = {"BR01", "BR03", "BR04", "BR07", "BR09", "BR11", "BR12", "BR15", "BR17", "BR19", "BR20", "BR22"}


def write(name: str, header: list[str], rows: list[list]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote data/{name}: {len(rows):,} rows")


def basket_value(r: random.Random, member: bool, large: bool) -> tuple[int, float]:
    """Items and value of one basket: lognormal, members and large branches a little higher."""
    mu = math.log(16.0) + (0.18 if member else 0.0) + (0.08 if large else 0.0)
    value = r.lognormvariate(mu, 0.62)
    if r.random() < 0.004:  # a family or office order
        value *= r.uniform(4.0, 9.0)
    items = max(1, round(value / r.uniform(3.2, 4.6)))
    return items, round(value, 2)


def baskets(r: random.Random) -> None:
    six = ["BR03", "BR07", "BR11", "BR15", "BR19", "BR22"]
    busy = "BR07"
    rows, k = [], 0
    for day in range(1, 31):
        for b in six:
            n = r.randint(26, 40) + (12 if b == busy else 0)
            for _ in range(n):
                k += 1
                band = r.choices(["morning", "midday", "evening"], weights=[5, 3, 4])[0]
                member = r.random() < 0.34
                items, value = basket_value(r, member, b in LARGE)
                wait = r.gammavariate(2.0, 1.4 + (0.9 if band == "evening" else 0.0) + (0.8 if b == busy else 0.0))
                wait_txt = f"{wait:.1f}"
                p_missing = 0.02 + (0.20 if (b == busy and band == "evening") else 0.0)
                if r.random() < p_missing:
                    wait_txt = ""
                elif b == "BR15" and r.random() < 0.03:
                    wait_txt = "-1"
                rows.append([f"BK-M{k:05d}", b, SECTOR_OF[b], day, band, items, f"{value:.2f}", wait_txt, int(member)])
    # one till error: a key held down
    rows[2817][6] = "9999.00"
    rows[2817][5] = 3
    # one real catering order
    rows[4410][5], rows[4410][6] = 140, "612.40"
    write("baskets.csv", ["basket_ref", "branch", "sector", "day", "band", "items", "value", "wait_min", "member"], rows)


def population(r: random.Random) -> None:
    rows = []
    for k in range(1, 40001):
        b = r.choice(BRANCHES)
        member = r.random() < 0.33
        items, value = basket_value(r, member, b in LARGE)
        rows.append([f"BK-Q{k:05d}", b, SECTOR_OF[b], int(member), items, f"{value:.2f}"])
    write("population.csv", ["basket_ref", "branch", "sector", "member", "items", "value"], rows)


def waste(r: random.Random) -> None:
    display = {"BR01", "BR03", "BR04", "BR07", "BR09", "BR11", "BR12", "BR15", "BR17", "BR19", "BR06", "BR14"}
    rows = []
    for b in BRANCHES:
        large = b in LARGE
        for month in range(1, 7):
            baked = r.randint(5200, 6400) if large else r.randint(2300, 3100)
            rate = (0.090 if large else 0.050) - (0.012 if b in display else 0.0) + r.gauss(0, 0.006)
            wasted = round(baked * max(rate, 0.01))
            rows.append([b, SECTOR_OF[b], "large" if large else "small", int(b in display), month, baked, wasted])
    write("waste.csv", ["branch", "sector", "size", "display", "month", "baked", "wasted"], rows)


def trial(r: random.Random) -> None:
    order = BRANCHES[:]
    r.shuffle(order)
    treated = set(order[:12])
    rows = []
    for b in BRANCHES:
        large = b in LARGE
        base = (0.088 if large else 0.052) + r.gauss(0, 0.008)
        before = round(base, 4)
        after = round(base - (0.011 if b in treated else 0.0) + r.gauss(0, 0.006), 4)
        rows.append([b, SECTOR_OF[b], "large" if large else "small", int(b in treated), f"{before:.4f}", f"{after:.4f}"])
    write("trial.csv", ["branch", "sector", "size", "discount", "waste_rate_before", "waste_rate_after"], rows)


def promo(r: random.Random) -> None:
    order = BRANCHES[:]
    r.shuffle(order)
    flyer = set(order[:12])
    rows = []
    for line in range(1, 21):
        sd = r.uniform(4.0, 12.0)
        for b in BRANCHES:
            change = r.gauss(0.0, sd)  # no true effect for any line
            rows.append([b, SECTOR_OF[b], "large" if b in LARGE else "small", int(b in flyer), f"L{line:02d}", f"{change:.1f}"])
    write("promo.csv", ["branch", "sector", "size", "flyer", "line", "change_units"], rows)


if __name__ == "__main__":
    for i, step in enumerate([baskets, population, waste, trial, promo]):
        step(random.Random(SEED * 100 + i))
