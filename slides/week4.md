---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week4.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

## Week 4: The bootstrap

Resample the sample to see how much an estimate could move

#### [week4#title] The bootstrap

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 4: Resample the sample to see how much an estimate could move

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week4#agenda] The bootstrap

*This week*

- **Session 1 · The bootstrap and its coverage**: The bootstrap and its assumptions, percentile intervals, and interval coverage checked by simulation

#### [week4#review-week3] Why does the overall rate mislead?

*Review · week 3*

**Question:** Branches that chose a new oven burn more trays overall, but fewer within both small and large branches. Large branches chose the oven more often and burn more trays with any oven. What is branch size here?

- A. The outcome of the comparison
- B. A source of random error that averages out
- C. The treatment
- D. A confounder: it drives both the choice and the burn rate

### Session 1: The bootstrap and its coverage

#### [week4#s1] The bootstrap and its coverage

*Session 1*

- Build a percentile bootstrap interval for a mean and a median
- Check an interval method's coverage by simulation against a known truth
- Explain why bootstrap intervals under-cover for small samples from a long-tailed population

#### [week4#bootstrap-idea] Treat the sample as the population, and draw new samples from it

*Block A · the idea*

1. **1 · Resample** n values from the sample, **with replacement**
2. **2 · Compute** The statistic
3. **3 · Repeat** Thousands of times
4. **4 · Read** The spread of the statistics

> With replacement, because without it every resample would be the sample itself, reordered.

#### [week4#resamples] Five delivery times, three resamples, three different means

*Block A · an example*

Sample, in minutes: 12, 15, 18, 22, 60 (mean 25.4)

| Resample | Mean |
| --- | --- |
| 22, 60, 60, 18, 60 | 44.0 |
| 60, 60, 12, 18, 22 | 34.4 |
| 15, 15, 22, 60, 18 | 26.0 |

- Some values appear twice or three times, some not at all
- The one long delivery drives most of the variation
- No resample can contain a value the sample lacks

#### [week4#percentile-interval] A 95% percentile interval keeps the middle 95% of the bootstrap statistics

*Block A · the interval*

```python
# file: numpy
n = len(x)
# B resamples at once
idx = rng.integers(0, n, size=(B, n))
boots = x[idx].mean(axis=1)
low, high = np.percentile(boots, [2.5, 97.5])
```

- Works for any statistic: swap np.mean for np.median
- B of 2,000 or more keeps the ends steady; report B and the seed

#### [week4#check-resample] What can a resample contain?

*Checkpoint*

**Question:** A sample of six repair costs is 80, 95, 110, 120, 150, 400. Which of these can be a bootstrap resample of it?

- A. 80, 95, 100, 120, 150, 400
- B. 95, 110, 400
- C. 400, 400, 80, 120, 120, 95
- D. The six values in a new order only

#### [week4#ci-meaning] The 95% belongs to the method, not to one interval

*Block B · meaning*

- Draw many samples; build an interval from each
- A 95% method contains the true value in about 95% of them
- Any one interval either contains it or does not; we do not know which

- **A correct sentence.** "Our method gives intervals that contain the true mean in about 95% of samples; from this sample the interval is A to B."

#### [week4#ci-misreadings] Four common misreadings of a confidence interval

*Block B · misreadings*

| Misreading | Correction |
| --- | --- |
| "95% of the values lie in the interval" | The interval is for the mean (or median), not for single values |
| "The true mean has a 95% chance of being in this interval" | The 95% describes how often the method works |
| "A wider interval means a worse method" | Width reflects the data and n; a too-narrow method under-covers |
| "Two overlapping intervals mean no difference" | Overlap does not settle it: build an interval for the difference (week 5) |

#### [week4#check-ci] Classify the statement

*Checkpoint*

**Question:** A report says: "The 95% interval for the mean delivery time is 27 to 33 minutes, so 95% of deliveries take between 27 and 33 minutes." What is wrong?

- A. Nothing; it should just say 90%
- B. The interval should be centred exactly on 30
- C. Bootstrap intervals only describe medians
- D. It reads an interval for the mean as a range for single deliveries

#### [week4#coverage-check] When the truth is known, count how often the intervals contain it

*Block C · coverage*

| Normal population | Coverage of the 95% percentile interval |
| --- | --- |
| n = 10 | 0.900 |
| n = 40 | 0.933 |

- 2,000 samples per row, 2,000 resamples each
- Even on a well-behaved population, small samples give intervals a little too narrow
- A long-tailed population is harder: the lab measures it

#### [week4#assumptions] The bootstrap assumes the sample looks like the population, row by independent row

*Block C · assumptions*

- **Representative.** A biased frame gives a precise interval around the wrong value.
- **Big enough.** A small sample from a long tail rarely shows the tail.
- **Independent rows.** Repeated measures of the same person or branch need clustered resampling (SPC-STA-201).

#### [week4#library-default] Check which interval a library returns: SciPy's default is not the percentile method

*Block C · libraries*

```python
# file: scipy
from scipy import stats
# what you build in the lab
stats.bootstrap((x,), np.mean,
                method="percentile")
# the default method: BCa
stats.bootstrap((x,), np.mean)
```

> BCa (bias-corrected and accelerated) adjusts the ends; why it does is in SPC-STA-201. Name the method in every report.

#### [week4#check-coverage] What does this coverage study show?

*Checkpoint*

**Question:** A coverage study of a 95% interval method on a long-tailed population gives 0.86 at n = 12 and 0.94 at n = 150, from 1,000 samples each. What is the right conclusion?

- A. The method is close to its 95% at n = 150 and too narrow at n = 12
- B. The method fails at both sizes, since neither shows exactly 0.95
- C. Use more bootstrap resamples at n = 12 and it will reach 0.95
- D. The intervals at n = 150 are more often wrong because they are narrower

#### [week4#lab-4-1] Bootstrap intervals with coverage checked against a known truth

Lab 4.1 · 105 min

Build bootstrap intervals and count how often they contain the known mean and median.

[W4_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W4_1.ipynb)

- [ ] Set up; one sample and the truth (10 min)
- [ ] Every resample of a sample of two, by hand (10 min)
- [ ] A percentile bootstrap for any statistic (20 min)
- [ ] Intervals for the mean and the median from one sample of 50 (10 min)
- [ ] Coverage by simulation at n = 10, 30 and 100 (25 min)
- [ ] Compare with SciPy's bootstrap: percentile and its default method (15 min)
- [ ] Record how this was checked (15 min)
- [ ] ✱ Stretch: The coverage of the t interval for the mean at the same sizes

#### [week4#debrief-one-sample] The first sample's interval missed the true mean: that is what 95% allows

*Debrief · lab 4.1*

- **14.59 to 19.94** interval for the mean from 50 baskets
- **21.93** the true mean of the quarter

The median's interval, 12.48 to 18.00, did contain the true median, 17.61. A rerun with a new seed moved the ends by at most 0.32.

#### [week4#debrief-coverage] On the long-tailed baskets the mean's interval reached 0.92 only at n = 100

*Debrief · lab 4.1*

| n | Mean | Median |
| --- | --- | --- |
| 10 | 0.853 | 0.937 |
| 30 | 0.897 | 0.932 |
| 100 | 0.920 | 0.939 |

1,000 samples per row: each figure carries a Monte Carlo error of about ±0.014.

#### [week4#wrap-up] Three things to keep

*Week 4 · wrap-up*

- **Resample the sample.** Same size, with replacement, any statistic.
- **95% is the method's.** One interval either contains the truth or not.
- **Check coverage.** Small samples from long tails give intervals too narrow.

#### [week4#next] Week 5: Intervals for differences and slopes

*Next*

Problem set 4 (50 minutes, AI off for the first attempt): labs/problem-sets/PS4.ipynb. The first supervised test, 90 minutes, AI off, follows this week.
