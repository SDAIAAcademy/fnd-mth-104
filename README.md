<!-- academy:title -->
# Statistics by Simulation: Variation, Estimation and Testing

الإحصاء بالمحاكاة: التفاوت والتقدير والاختبار

Data & AI Foundations Track · SDAIA Academy · FND-MTH-104 · Level 100

REPLACE: one line under the title: what participants can do after the course

Participants approach inference by simulation before formulas. They draw repeated samples to see variation, build bootstrap intervals for means, medians, differences and slopes, run permutation tests, and report effect sizes with intervals rather than bare p-values. They find multiple-testing and forking-path problems in reported results. Each lab ends with a note on how the result was checked, and the capstone is an analysis brief on a public dataset, defended orally. Power analysis and study design follow in SPC-STA-201 and SPC-EXP-201.

**Format:** Extended: 8 weeks part-time, one session and one lab a week, weekly graded problem sets and a capstone

**Course page:** https://sdaiaacademy.github.io/fnd-mth-104/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Distinguish population, sample, parameter, statistic and sampling distribution, and explain what a standard error measures, given repeated samples from a known synthetic population | Awareness | supervised AI-off test, at least 70% correct |
| LO2 | Explain what p-values and confidence intervals mean and identify misreadings of them, given ten statements from synthetic reports | Awareness | each statement classified and corrected, eight of ten correct |
| LO3 | Identify multiple-testing, forking-path and confounding problems in a reported analysis, given a one-page synthetic summary | Awareness | a written critique naming each problem and its effect |
| LO4 | Compute bootstrap intervals for means, medians, group differences and regression slopes, given public data with skewed variables | Applied | a notebook whose intervals agree on rerun with a new seed |
| LO5 | Implement permutation tests and report each result as an effect size with an interval, given two public datasets and stated questions | Applied | notebooks with test code, intervals and a plain-language reading |
| LO6 | Apply family-wise and false-discovery-rate corrections and measure by simulation how often uncorrected tests produce false findings, given twenty outcomes with no true effect | Applied | a table of false-finding rates with and without correction |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Week 1 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week1.html`](slides/week1.html) |
| Week 2 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week2.html`](slides/week2.html) |
| Week 3 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week3.html`](slides/week3.html) |
| Week 4 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week4.html`](slides/week4.html) |
| Week 5 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week5.html`](slides/week5.html) |
| Week 6 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week6.html`](slides/week6.html) |
| Week 7 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week7.html`](slides/week7.html) |
| Week 8 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1 | [`slides/week8.html`](slides/week8.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Week 1 · Session 1 | REPLACE: what participants build in lab 1.1 | [`W1_1.ipynb`](labs/W1_1.ipynb) |
| 2.1 | Week 2 · Session 1 | REPLACE: what participants build in lab 2.1 | [`W2_1.ipynb`](labs/W2_1.ipynb) |
| 3.1 | Week 3 · Session 1 | REPLACE: what participants build in lab 3.1 | [`W3_1.ipynb`](labs/W3_1.ipynb) |
| 4.1 | Week 4 · Session 1 | REPLACE: what participants build in lab 4.1 | [`W4_1.ipynb`](labs/W4_1.ipynb) |
| 5.1 | Week 5 · Session 1 | REPLACE: what participants build in lab 5.1 | [`W5_1.ipynb`](labs/W5_1.ipynb) |
| 6.1 | Week 6 · Session 1 | REPLACE: what participants build in lab 6.1 | [`W6_1.ipynb`](labs/W6_1.ipynb) |
| 7.1 | Week 7 · Session 1 | REPLACE: what participants build in lab 7.1 | [`W7_1.ipynb`](labs/W7_1.ipynb) |
| 8.1 | Week 8 · Session 1 | REPLACE: what participants build in lab 8.1 | [`W8_1.ipynb`](labs/W8_1.ipynb) |
<!-- /academy:labs -->

## Capstone

A two-page analysis brief on a public dataset with estimate, interval, test, effect size and limits, submitted with its notebook and defended in a ten-minute oral check

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- FND-MTH-103 Probability for Data and AI
- Probability shown in the placement test is accepted in place of FND-MTH-103
- Computes group summaries with a DataFrame library (FND-DAT-102 or the pre-work notebook)

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Resampling and testing:** SciPy stats, statsmodels, R with the infer package
- **DataFrame library:** pandas, Polars
- **Notebook environment:** JupyterLab, marimo, a free hosted notebook service
- **Hint-only tutor:** an open-weight model in tutor mode, an approved assistant with a tutor instruction
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- SDAIA Data & AI Academic Programs Standards Framework (2026): bridging unit MSF-Statistics at Explain level: REPLACE: the address of the official text
