---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week7"
day: 7
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week7.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

## Week 7: Many tests and forking paths

Test enough things and something will look real

#### [week7#title] Many tests and forking paths

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 7: Test enough things and something will look real

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week7#agenda] Many tests and forking paths

*This week*

- **Session 1 · Multiple testing and false discoveries**: Multiple testing and false discoveries, family-wise and false-discovery-rate corrections, forking paths and pre-specified analyses

#### [week7#review-week6] Read the result

*Review · week 6*

**Question:** A permutation test of a new checkout layout gives p = 0.21 on 40 shops. A manager writes: "the layout has no effect". What is the best correction?

- A. "The data cannot tell at this size; the interval for the effect is wide."
- B. "There is a 79% chance the layout works."
- C. "The layout makes things worse."
- D. "Retest at α = 0.01 to confirm there is no effect."

### Session 1: Multiple testing and false discoveries

#### [week7#s1] Multiple testing and false discoveries

*Session 1*

- Measure by simulation how often uncorrected tests produce false findings
- Apply Bonferroni, Holm and Benjamini-Hochberg corrections and say what each controls
- Spot forking paths in a reported analysis and name the pre-specification that prevents them

#### [week7#many-tests] Test enough true nulls and something will pass

*Block A · many tests*

| Tests, all with no true effect | Expected false findings | Chance of at least one |
| --- | --- | --- |
| 1 | 0.05 | 0.050 |
| 5 | 0.25 | 0.226 |
| 10 | 0.50 | 0.401 |
| 50 | 2.50 | 0.923 |

#### [week7#dashboards] Dashboards, subgroup tables and "we also looked at" paragraphs run many tests

*Block A · where it happens*

- One test per product line, region or customer segment
- Many outcomes for one change: sales, visits, basket size, returns
- Results reported only when they pass, so the reader never sees the count

> **What goes wrong.** A "finding" that is one of twenty tests is about as surprising as one heads in twenty coin tosses.

#### [week7#check-many] How surprising is this?

*Checkpoint*

**Question:** A regional report tests 40 districts for a change in complaints after a policy, each at α = 0.05. Two districts show a "significant" change. Assume the policy did nothing. How many would you expect?

- A. None, since α is only 5%
- B. About 0.05
- C. About 2
- D. About 32

#### [week7#two-error-rates] Control the chance of any false finding, or the share of false findings

*Block B · what to control*

- **Family-wise error rate.** The chance of at least one false finding in the family. Bonferroni: reject when p ≤ α / m. Holm: the same guarantee, step by step, more power.
- **False discovery rate.** The expected share of false findings among all findings. Benjamini-Hochberg: largest k with p₍ₖ₎ ≤ k α / m.

#### [week7#six-tests] Six p-values, three procedures, three answers

*Block B · an example*

| Sorted p | Bonferroni, p ≤ 0.0083 | Holm, 0.05 / (6, 5, 4, …) | BH, k × 0.05 / 6 |
| --- | --- | --- | --- |
| 0.001 | ✓ | ✓ | ✓ |
| 0.006 | ✓ | ✓ | ✓ |
| 0.012 |  | ✓ | ✓ |
| 0.019 |  |  | ✓ |
| 0.044 |  |  |  |
| 0.310 |  |  |  |

#### [week7#corrections-code] Write the corrections once, then check them against a library

*Block B · in code*

```python
# file: statsmodels
from scipy import stats
from statsmodels.stats import (
    multitest as mt)

r = mt.multipletests(
    p, alpha=0.05, method="holm")
reject, p_adj = r[0], r[1]
# BH-adjusted p-values
q = stats.false_discovery_control(p)
```

#### [week7#check-correction] Which procedure fits the purpose?

*Checkpoint*

**Question:** A team screens 300 product ideas from survey data to pick some for a costly follow-up trial; a few false picks are acceptable if most picks are real. Which control fits?

- A. No correction: each test is at 5%
- B. Benjamini-Hochberg, controlling the share of false picks
- C. Bonferroni, controlling any false pick at all
- D. Test each idea at α = 0.01 instead

#### [week7#forking-paths] One test can hide many: every choice made after seeing the data is a fork

*Block C · forking paths*

- Which outcome: units, value, share of baskets
- Which units: all branches, large ones, one sector
- What to do with outliers, which weeks, which test

- **No fishing needed.** Each choice can be reasonable. Making them after looking still inflates the false-finding rate, even when only one test is run.

#### [week7#pre-specify] Write the analysis down before you look, and report every test you ran

*Block C · the cure*

- **Before.** Question, outcome, groups, test, outlier rule, family of claims.
- **During.** Any change to the plan is logged with its reason.
- **After.** Report the planned results first; label the rest exploratory.

#### [week7#check-forking] Name the problem

*Checkpoint*

**Question:** A summary reports that a staff-training course "significantly reduced errors among evening-shift staff over 40 (p = 0.03)". The full data covered all shifts and ages; no subgroup was planned. What is the main problem?

- A. Evening staff may be less careful
- B. None: p = 0.03 is below 0.05
- C. The subgroup is too small for a permutation test
- D. A forking path: the subgroup was picked after seeing the data

#### [week7#lab-7-1] Twenty tests on pure noise, with and without correction

Lab 7.1 · 105 min

Test twenty lines with no true effect, then simulate a thousand dashboards with and without correction.

[W7_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W7_1.ipynb)

- [ ] Set up; the promotion dashboard (10 min)
- [ ] Bonferroni, Holm and Benjamini-Hochberg by hand on five p-values (15 min)
- [ ] Twenty permutation tests on the dashboard (15 min)
- [ ] The three corrections on the dashboard (10 min)
- [ ] A thousand dashboards of pure noise: the table of false-finding rates (25 min)
- [ ] Forking paths: one line, eight reasonable analyses (15 min)
- [ ] Record how this was checked (15 min)
- [ ] ✱ Stretch: Give four lines a true effect and compare Bonferroni with Benjamini-Hochberg

#### [week7#debrief-rates] Uncorrected, 63% of pure-noise dashboards showed a finding; corrected, 3.5%

*Debrief · lab 7.1*

| 1,000 simulated dashboards, 20 lines, no effect | False-finding rate |
| --- | --- |
| Single test, uncorrected | 0.049 |
| At least one of 20, uncorrected | 0.627 |
| Bonferroni | 0.035 |
| Holm | 0.035 |
| Benjamini-Hochberg | 0.035 |

#### [week7#debrief-forking] One planned test erred 5% of the time; the best of eight paths, 19%

*Debrief · lab 7.1*

- **0.050** one planned test, 300 noise lines
- **0.190** smallest p of eight reasonable paths

With four true effects among 20 lines (stretch), BH found more of them than Bonferroni (power 0.24 against 0.17) with few false discoveries.

#### [week7#wrap-up] Three things to keep

*Week 7 · wrap-up*

- **Count the tests.** Twenty true nulls give a finding most of the time.
- **Correct for the family.** Holm for decisive claims, BH for screening.
- **Fix the path first.** Choices made after looking are hidden tests.

#### [week7#next] Week 8: Error rates, power and honest reporting

*Next*

Problem set 7 (50 minutes, AI off for the first attempt): labs/problem-sets/PS7.ipynb. Bring a public dataset idea for the capstone.
