---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week5"
day: 5
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week5.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

## Week 5: Intervals for differences and slopes

Resample the way the data were collected

#### [week5#title] Intervals for differences and slopes

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 5: Resample the way the data were collected

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week5#agenda] Intervals for differences and slopes

*This week*

- **Session 1 · Differences and slopes**: Intervals for differences between groups and for regression slopes on public skewed data, with small groups suppressed and reruns compared

#### [week5#review-week4] What does the 95% describe?

*Review · week 4*

**Question:** An analyst builds a 95% percentile bootstrap interval for the median waiting time from one sample. Which statement about it is correct?

- A. 95% of waits fall inside it
- B. Its method contains the true median in about 95% of samples, if the method's coverage is right
- C. The true median has a 95% chance of being inside this interval
- D. 95% of the bootstrap resamples contain the true median

### Session 1: Differences and slopes

#### [week5#s1] Differences and slopes

*Session 1*

- Build a bootstrap interval for a difference between two groups by resampling each group
- Build a bootstrap interval for a regression slope by resampling whole rows
- Show that intervals agree on rerun with a new seed, and suppress small groups before reporting

#### [week5#public-data] Before any analysis of public data: source, licence, unit and what a row is

*Block A · public data*

| Question | Why it matters |
| --- | --- |
| Who published it, and under which licence? | Whether you may use and share results; the source caption on every table |
| What is one row? | A person, a person-year, a household: it decides what can be resampled |
| How were groups formed? | Random assignment, or observation (week 3) |

#### [week5#suppression] Suppress small groups before any table leaves your notebook

*Block A · reporting rule*

- The course's rule: no group of fewer than 30 rows is reported
- Blank the value **and** the exact count: "under 30"
- A small group's mean is imprecise, and can point to identifiable people

```python
# file: pandas
cells = df.groupby(["plan", "health"])["visits"].agg(
    n="size", mean="mean")
shown = U.suppress(cells, "n", min_n=30)
```

#### [week5#check-suppress] What leaves the notebook?

*Checkpoint*

**Question:** A table of mean monthly spending by district and age band has one cell of 11 customers whose mean is unusually high. What do you publish for that cell?

- A. The mean, flagged as based on few customers
- B. The cell merged into its largest neighbour, without saying so
- C. "Suppressed", with the count shown only as under 30
- D. The median of the 11 instead of their mean

#### [week5#difference] For a difference between two groups, resample each group separately

*Block B · differences*

```python
# file: numpy
d = [rng.choice(a, len(a)).mean()
     - rng.choice(b, len(b)).mean()
     for _ in range(B)]
low, high = np.percentile(d, [2.5, 97.5])
```

- Each group keeps its own size, as it was collected
- Pooling the groups would resample "no difference": that is next week's test
- Any statistic: difference of means, of medians, a ratio

#### [week5#oven-example] Two oven settings, an interval for the difference that includes zero

*Block B · an example*

| Bake minutes | Mean |
| --- | --- |
| Setting A, 60 batches | 18.51 |
| Setting B, 50 batches | 17.90 |
| A − B (95% interval) | 0.61 (−2.71 to 3.81) |

- **Reading.** The data fit a difference anywhere from B being 2.7 minutes slower to A being 3.8 slower: this sample cannot say which setting is faster.

#### [week5#overlap] Compare groups with an interval for their difference, not by overlapping intervals

*Block B · a misreading*

- Two 95% intervals can overlap while the interval for the difference excludes zero
- The rule "no overlap means a real difference" is too strict; "overlap means none" is wrong
- The question is about the difference: estimate the difference

#### [week5#check-difference] How do you resample?

*Checkpoint*

**Question:** You want a bootstrap interval for the difference in median call length between two support teams (220 and 90 calls). Which resampling scheme fits?

- A. 220 calls with replacement from team one, 90 from team two
- B. 310 calls from the pooled calls, split 220 and 90
- C. 90 calls from each team
- D. 220 and 90 calls without replacement

#### [week5#slope] For a slope, resample whole rows so each x keeps its own y

*Block C · slopes*

Five points: (1, 2), (2, 4), (3, 5), (4, 4), (5, 7)

Least-squares slope: **1.0**

Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = 10 / 10

```python
# file: numpy
i = rng.integers(0, n, n)     # rows
b = slope(x[i], y[i])
```

> **What goes wrong.** Resampling x and y separately breaks the pairs: every slope comes out near zero.

#### [week5#rerun] An interval you report must survive a rerun with a new seed

*Block C · reruns*

- Run every interval twice, with two seeds
- Measure the largest move of an end against the interval's width
- Report to the precision that does not move

- **The outcome's evidence.** LO4 asks for a notebook whose intervals agree on rerun with a new seed. The lab builds that table.

#### [week5#check-slope] Which resampling for a slope?

*Checkpoint*

**Question:** You fit the slope of energy use on floor area for 140 buildings and want a bootstrap interval for it. Which draws one resample?

- A. 140 areas and, separately, 140 energy values, both with replacement
- B. The 140 energy values shuffled against fixed areas
- C. 70 buildings drawn without replacement
- D. 140 buildings drawn with replacement, each with its own area and energy

#### [week5#lab-5-1] Bootstrap intervals for differences and slopes on public skewed data

Lab 5.1 · 105 min

Intervals for a mean, a median, a difference and a slope on two public datasets, checked on rerun.

[W5_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W5_1.ipynb)

- [ ] Set up; the public data and its licence (10 min)
- [ ] Suppress small groups before any table (10 min)
- [ ] Intervals for the mean and the median of visits (15 min)
- [ ] An interval for a difference between plans (20 min)
- [ ] A slope by hand, then in code (10 min)
- [ ] A bootstrap interval for a slope (20 min)
- [ ] Rerun with a new seed and compare every interval (10 min)
- [ ] Record how this was checked (10 min)
- [ ] ✱ Stretch: The slope on the log scale, and what it means

#### [week5#debrief-difference] Free care: about one more doctor visit a year than 95% coinsurance

*Debrief · lab 5.1*

| Outpatient visits a year | Free care | 95% coinsurance | Difference (95% interval) |
| --- | --- | --- | --- |
| Mean | 3.12 | 2.11 | 1.01 (0.83 to 1.18) |
| Median | 2 | 1 | 1 (1 to 1) |

> **Limit.** Rows are person-years and the subset has no person identifier, so the lab resampled rows, not people: these intervals are too narrow.

Source: RAND Health Insurance Experiment subset bundled with statsmodels (public domain); 10,997 and 2,653 person-years. Three plan-by-health cells under 30 rows were suppressed.

#### [week5#debrief-slope] Food spending rose by 0.49 for each unit of income, and the intervals held on rerun

*Debrief · lab 5.1*

- **0.485** slope, 95% interval 0.405 to 0.594
- **< 4%** largest move of any end on rerun, as a share of its interval's width

Source: Engel's food expenditure data bundled with statsmodels (public domain), 235 households.

#### [week5#wrap-up] Three things to keep

*Week 5 · wrap-up*

- **Resample as collected.** Groups separately; rows whole.
- **Estimate the difference.** Not the overlap of two intervals.
- **Suppress, then report.** No group under 30 rows leaves the notebook.

#### [week5#next] Week 6: Permutation tests

*Next*

Problem set 5 (50 minutes, AI off for the first attempt): labs/problem-sets/PS5.ipynb.
