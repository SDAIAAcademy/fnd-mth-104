---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week6"
day: 6
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week6.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

## Week 6: Permutation tests

Shuffle the labels to see what chance alone produces

#### [week6#title] Permutation tests

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 6: Shuffle the labels to see what chance alone produces

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week6#agenda] Permutation tests

*This week*

- **Session 1 · Null models, p-values and effect sizes**: Null models and permutation tests, what p-values do not mean, Type I and Type II errors, and effect size with practical significance

#### [week6#review-week5] Which interval answers the question?

*Review · week 5*

**Question:** Two warehouses' mean picking times have 95% intervals 11.0 to 13.0 and 12.5 to 14.5 minutes. A manager concludes there is no difference because the intervals overlap. What should the analyst do?

- A. Agree: overlapping intervals mean no difference
- B. Recompute both intervals at 99% to remove the overlap
- C. Build a bootstrap interval for the difference itself
- D. Pool both warehouses and build one interval

### Session 1: Null models, p-values and effect sizes

#### [week6#s1] Null models, p-values and effect sizes

*Session 1*

- State the null model of a comparison and test it by permutation
- Read a p-value correctly and correct common misreadings
- Report a result as an effect size with an interval and a plain-language reading

#### [week6#null-model] A null model says how the data would look if nothing were going on

*Block A · the null model*

- Groups assigned at random, no effect: the labels could have been any relabelling
- Two columns with no relation: any pairing is as likely as the observed one
- A permutation test builds the null by **shuffling**, and counts

- **The question it answers.** If the labels did not matter, how often would a shuffle give a difference at least as large as ours?

#### [week6#shuffle-example] Three against three: twenty splits, two as extreme as the data

*Block A · by hand*

Old layout: 3, 4, 6 sales. New layout: 7, 9, 11.

Observed difference: 9 − 4.33 = **4.67**

Choose any 3 of the 6 values as "old": 20 splits. Two give |difference| ≥ 4.67: the real one and its mirror.

**p = 2 / 20 = 0.10** two-sided, from every split

#### [week6#shuffle-code] With many rows, shuffle a few thousand times instead of listing every split

*Block A · at scale*

```python
# file: numpy
obs = x.mean() - y.mean()
pooled = np.concatenate([x, y])
k, count = len(x), 0
for _ in range(R):
    p = rng.permutation(pooled)
    d = p[:k].mean() - p[k:].mean()
    count += abs(d) >= abs(obs)
p_value = (count + 1) / (R + 1)
```

#### [week6#check-null] What do you shuffle?

*Checkpoint*

**Question:** Thirty stores were randomly given a new price label; thirty kept the old one. To test whether weekly sales differ, what does each permutation do?

- A. Resample each group with replacement
- B. Shuffle the 60 stores' labels and split them 30 and 30
- C. Sort the sales and give the top 30 the new label
- D. Add random noise to each store's sales

#### [week6#p-not-mean] What a p-value does not mean

*Block B · misreadings*

| Misreading of p = 0.03 | Correction |
| --- | --- |
| "A 3% chance that there is no effect" | p assumes no effect; it is not the probability of that assumption |
| "A 97% chance that the effect is real" | The same reversal, stated the other way |
| "The effect is large" | p mixes size and sample size; report the effect size |
| "p = 0.06, so there is no effect" | Not enough evidence at this size is not evidence of none |

#### [week6#errors] A test can err two ways: a false finding and a missed effect

*Block B · two errors*

|  | The test rejects | The test does not reject |
| --- | --- | --- |
| **No real effect** | Type I error: a false finding, at rate α | Correct |
| **A real effect** | Correct: the rate is the **power** | Type II error: a missed effect |

> α = 0.05 is a convention, not a law. Week 8 estimates both rates by simulation.

#### [week6#check-pvalue] Correct the sentence

*Checkpoint*

**Question:** A report says: "p = 0.01, so there is only a 1% chance that the new schedule has no effect." Which correction is right?

- A. "There is a 99% chance the schedule works."
- B. "The schedule improves the outcome by 1%."
- C. "If the schedule had no effect, a difference at least this large would arise in about 1% of relabellings."
- D. "The result is significant at the 5% level, so the effect is certain."

#### [week6#effect-size] Report how big the effect is, with an interval, then the test

*Block C · effect size*

- **Difference.** In the outcome's own units: minutes, riyals, visits.
- **Ratio.** "48% more": useful when the level differs between settings.
- **Correlation.** For two numeric columns: from −1 to 1, with its interval.

> **Practical significance:** compare the interval with the smallest effect that would change a decision.

#### [week6#plain-reading] A plain-language reading states the size, the uncertainty and what chance can explain

*Block C · the reading*

- **Template.** "[Group A] [did more/less] [outcome] than [group B]: [difference] ([interval]). Shuffling the labels gave a gap this large in [p as a share] of [R] shuffles. [What this does and does not show.]"

> **Avoid:** "proves", "significant" on its own, "the probability that the null is true", and causal words for observational data.

#### [week6#check-report] Which report meets the standard?

*Checkpoint*

**Question:** A permutation test of two packing methods on 400 boxes gives p = 0.004. Which report follows the course's standard?

- A. "Method B is significantly better (p < 0.05)."
- B. "p = 0.004 proves method B is better."
- C. "Method B is better with 99.6% probability."
- D. "B damaged 1.2 fewer boxes per hundred (interval 0.4 to 2.0); shuffles rarely gave a gap this large (p = 0.004)."

#### [week6#lab-6-1] Permutation tests for a group difference and a correlation on public data

Lab 6.1 · 105 min

Test a group difference and a correlation by permutation, and report effect sizes with intervals.

[W6_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W6_1.ipynb)

- [ ] Set up; the two questions and their null models (10 min)
- [ ] Every split of a tiny two-group sample, by hand (15 min)
- [ ] A permutation test for a difference in means (20 min)
- [ ] The effect size with an interval (15 min)
- [ ] A permutation test for a correlation (15 min)
- [ ] Compare with SciPy's permutation test (10 min)
- [ ] A plain-language reading of each result (10 min)
- [ ] Record how this was checked (10 min)
- [ ] ✱ Stretch: Q1 for poor health only, and why it is weaker

#### [week6#debrief-q1] Q1: free care gave about 48% more visits; no shuffle came close

*Debrief · lab 6.1*

| Free care against 95% coinsurance | Estimate | 95% interval |
| --- | --- | --- |
| Difference in mean visits a year | 1.01 | 0.82 to 1.18 |
| Ratio of means | 1.48 | 1.37 to 1.60 |
| Permutation p, 5,000 shuffles | 0.0002, the floor 1 / 5,001 |  |

Source: RAND Health Insurance Experiment subset bundled with statsmodels (public domain). Rows are person-years resampled and shuffled as if independent, so the interval is too narrow and the p-value too small (week 5).

#### [week6#debrief-q2] Q2: income and food spending went together, r = 0.91; and two p-value conventions

*Debrief · lab 6.1*

- r = 0.91 (95% interval 0.89 to 0.95), p at the floor: an association in one survey, not a cause
- Tiny case: counting |difference| gave p = 0.1; SciPy's two-sided gave 0.2, twice the smaller one-sided p
- Neither convention is wrong: state the one you used

Source: Engel's food expenditure data bundled with statsmodels (public domain).

#### [week6#wrap-up] Three things to keep

*Week 6 · wrap-up*

- **Shuffle to build the null.** Count how often chance does as well.
- **p is conditional.** It assumes no effect; it never measures that assumption.
- **Size first.** Effect size, interval, then the test, in plain words.

#### [week6#next] Week 7: Many tests and forking paths

*Next*

Problem set 6 (50 minutes, AI off for the first attempt): labs/problem-sets/PS6.ipynb.
