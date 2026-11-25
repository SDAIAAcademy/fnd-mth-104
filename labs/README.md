# Statistics by Simulation: Variation, Estimation and Testing: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository and installs `requirements-colab.txt`.
- Locally: clone the repository and, from `labs/`, open the notebooks with `uv run --with jupyterlab jupyter lab` (the dependencies are in `pyproject.toml`; `uv.lock` pins them). The data in `data/` is already there; `uv run prepare_data.py` writes it again, identically.

| Unit | Session | Lab | Notebook |
|---|---|---|---|
| Pre-work | Group summaries with a DataFrame library (60 minutes, before week 1) | | [`PW_group_summaries.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/PW_group_summaries.ipynb) |
| Week 1 | Centre, spread, shape and missing values | Describing the chain's baskets: centre, spread, shape, outliers and missing values | [`W1_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W1_1.ipynb) |
| Week 2 | Populations, samples and standard error | Repeated sampling from a synthetic population | [`W2_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W2_1.ipynb) |
| Week 3 | Confounding and Simpson's paradox | Confounding in the waste records, against a randomised trial | [`W3_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W3_1.ipynb) |
| Week 4 | The bootstrap and its coverage | Bootstrap intervals with coverage checked against a known truth | [`W4_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W4_1.ipynb) |
| Week 5 | Bootstrap intervals for differences and slopes | Bootstrap intervals for differences and slopes on public skewed data | [`W5_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W5_1.ipynb) |
| Week 6 | Null models, p-values and effect sizes | Permutation tests for a group difference and a correlation on public data | [`W6_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W6_1.ipynb) |
| Week 7 | Multiple testing and false discoveries | Twenty tests on pure noise, with and without correction | [`W7_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W7_1.ipynb) |
| Week 8 | Type I and II errors, power and reporting | Type I error rate and power of a permutation test estimated by simulation at three sample sizes | [`W8_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/fnd-mth-104/blob/main/labs/W8_1.ipynb) |

Labs 2.1, 4.1, 6.1, 7.1 and 8.1 are the catalog entry's five lab lines, in the entry's order and with its wording. Labs 1.1, 3.1 and 5.1 are additions, so that each of the eight weekly sessions has a lab: they practise the entry's topics of describing data, of observational and experimental data with confounding and Simpson's paradox, and of intervals for differences and slopes.

Every lab starts with a small case done by hand, then does the same at scale and checks one against the other. An exercise left undone raises `NotImplementedError`; the notebook then falls back on a reference value in `data/reference/` or on the library, so that every later step still runs. Every lab ends with a short note: the result, how it was checked, its limits, and who reruns it before it is used. The worked versions are in [`solutions/`](solutions/); [`solutions/answer_key.md`](solutions/answer_key.md) lists what each lab should show.

## Problem sets

[`problem-sets/PS1.ipynb`](problem-sets/) to `PS8.ipynb`, one a week, 50 minutes each, AI off for the first attempt. The last cell of each calls [`pscheck.py`](problem-sets/pscheck.py), which prints one line per item and a score. It stores no answers: it checks that each hand answer agrees with your own function on the same small case, and runs your functions on new random data against properties, SciPy or statsmodels. The worked answers are kept by the trainer.

## Data

- `prepare_data.py` wrote the bakery chain's synthetic data in `data/` with seed 104: a month of baskets (`baskets.csv`), a known quarter of 40,000 baskets (`population.csv`), branch-month waste records (`waste.csv`), the randomised discount trial (`trial.csv`) and the promotion dashboard (`promo.csv`). Branches, product lines and baskets are codes; no person, place or brand is named.
- Labs 5.1 and 6.1 use two datasets bundled with statsmodels and marked public domain in its documentation: the RAND Health Insurance Experiment subset (`randhie`, 20,190 person-years) and Engel's food expenditure data (`engel`, 235 households). `sta.health_experiment()` and `sta.food_budgets()` read them from the installed package; nothing is downloaded and no row of them is copied into this repository.
- The course's reporting rule: a group with fewer than 30 rows is not reported (`sta.MIN_GROUP`, `sta.suppress`).

## Settings

| Variable | Effect |
|---|---|
| `STA_QUICK=1` | Fewer resamples, shuffles and simulated samples, for a fast run-through; simulated rates then move by a few points |

## Tutor

[`tutor/TUTOR.md`](tutor/TUTOR.md) is the instruction for the hint-only tutor allowed in labs: hints, never answers.

## For maintainers

The notebooks are generated from the percent-format sources in `labs/_src/` and `labs/problem-sets/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the lab solutions to `labs/solutions/`. Problem-set sources hold no solution. Edit the sources, not the notebooks. The reference files in `data/reference/` are written by running a solution source with `STA_WRITE_REF=1`.
