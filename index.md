---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/index.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

الإحصاء بالمحاكاة: التفاوت والتقدير والاختبار

Data & AI Foundations Track · 8 weeks + capstone · 45 hours · Level 100

Reason about variation, estimates and tests by simulating them, and report effect sizes with intervals, their limits and how each was checked

Participants approach inference by simulation before formulas. They draw repeated samples to see variation, build bootstrap intervals for means, medians, differences and slopes, run permutation tests, and report effect sizes with intervals rather than bare p-values. They find multiple-testing and forking-path problems in reported results. Each lab ends with a note on how the result was checked, and the capstone is an analysis brief on a public dataset, defended orally. Power analysis and study design follow in SPC-STA-201 and SPC-EXP-201.

**Who it is for:** Beginners. Career changers and non-computing graduates closing bridging gaps before advanced study, and computing graduates refreshing the mathematics behind models; a placement test lets participants skip any course whose content they already command.

**Format:** Extended: 8 weeks part-time, one session and one lab a week, weekly graded problem sets and a capstone

## The case study

**The bakery chain (fictional).** An unnamed chain of 24 neighbourhood bakeries in one city, with branches coded BR01 to BR24 and product lines L01 to L20; the labs speak to its operations manager, quality lead, finance analyst and customer insight lead by role only. Its data (a month of baskets, a known quarter of 40,000 baskets, waste records, a randomised discount trial and a promotion dashboard) is synthetic, written with seed 104; weeks 5 and 6 add two public-domain datasets bundled with statsmodels, read at run time and never copied into the course.

## The course

### Week 1: Describing data

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week1.md

- **Session 1: Centre, spread, shape and missing values**
  - Choose between the mean, the median and a trimmed mean for a long-tailed variable and justify the choice
  - Compute and read the interquartile range and the fences, and decide whether an extreme value is an error
  - Report a summary with the share and the likely direction of missing data
  - [Lab 1.1: Describing the chain's baskets (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W1_1.ipynb)

### Week 2: Sampling variation

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week2.md

- **Session 1: Populations, samples and standard error**
  - Name the population, the sample, the parameter and the statistic of a stated study
  - Estimate a standard error by drawing repeated samples and compare it with s/√n
  - Explain why a larger sample shrinks the standard error but not the bias of a wrong frame
  - [Lab 2.1: Repeated sampling from a synthetic population (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W2_1.ipynb)

### Week 3: Observational and experimental data

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week3.md

- **Session 1: Confounding and Simpson's paradox**
  - Tell observational from experimental data from how the treatment was assigned
  - Find a confounder that reverses a comparison (Simpson's paradox) and compare within its levels
  - Explain what a randomised assignment guarantees and what it does not
  - [Lab 3.1: Confounding in the waste records, against a randomised trial (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W3_1.ipynb)

### Week 4: The bootstrap

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week4.md

- **Session 1: The bootstrap and its coverage**
  - Build a percentile bootstrap interval for a mean and a median
  - Check an interval method's coverage by simulation against a known truth
  - Explain why bootstrap intervals under-cover for small samples from a long-tailed population
  - [Lab 4.1: Bootstrap intervals with coverage checked against a known truth (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W4_1.ipynb)

### Week 5: Intervals for differences and slopes

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week5.md

- **Session 1: Differences and slopes**
  - Build a bootstrap interval for a difference between two groups by resampling each group
  - Build a bootstrap interval for a regression slope by resampling whole rows
  - Show that intervals agree on rerun with a new seed, and suppress small groups before reporting
  - [Lab 5.1: Bootstrap intervals for differences and slopes on public skewed data (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W5_1.ipynb)

### Week 6: Permutation tests

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week6.md

- **Session 1: Null models, p-values and effect sizes**
  - State the null model of a comparison and test it by permutation
  - Read a p-value correctly and correct common misreadings
  - Report a result as an effect size with an interval and a plain-language reading
  - [Lab 6.1: Permutation tests for a group difference and a correlation on public data (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W6_1.ipynb)

### Week 7: Many tests and forking paths

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week7.md

- **Session 1: Multiple testing and false discoveries**
  - Measure by simulation how often uncorrected tests produce false findings
  - Apply Bonferroni, Holm and Benjamini-Hochberg corrections and say what each controls
  - Spot forking paths in a reported analysis and name the pre-specification that prevents them
  - [Lab 7.1: Twenty tests on pure noise, with and without correction (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W7_1.ipynb)

### Week 8: Error rates, power and honest reporting

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/week8.md

- **Session 1: Type I and II errors, power and reporting**
  - Estimate a test's Type I error rate and power by simulation at several sample sizes
  - Judge practical significance by comparing an interval with a threshold that matters
  - Write a result with its scope, limits and a record of how it was checked
  - [Lab 8.1: Type I error rate and power of a permutation test estimated by simulation at three sample sizes (105 min)](https://sdaiaacademy.github.io/fnd-mth-104/labs/W8_1.ipynb)

### Capstone: Capstone oral checks

Slides: https://sdaiaacademy.github.io/fnd-mth-104/slides/capstone.md

## Capstone

A two-page analysis brief on a public dataset with estimate, interval, test, effect size and limits, submitted with its notebook and defended in a ten-minute oral check

**What you submit:** A link to a public GitHub repository with the two-page brief, the notebook with its outputs, and the dataset's source and licence; then a ten-minute oral check in which the participant walks through the brief and reruns one test with a change the assessor specifies

**Rubric:**

- Question, dataset, source and licence, unit and scope stated; groups under 30 rows suppressed: 15%
- Estimate with a bootstrap interval resampled the way the data were collected; the interval agrees on rerun with a new seed: 25%
- Test with its null model stated, a permutation test, the effect size with an interval and a plain-language reading: 25%
- Limits: confounding, multiple comparisons and forking paths named where they apply, and what the analysis cannot show: 20%
- Notebook reruns from top to bottom; a record of how each result, and any AI-assisted step, was checked: 15%

## Outcomes

- **LO1** Distinguish population, sample, parameter, statistic and sampling distribution, and explain what a standard error measures, given repeated samples from a known synthetic population (Awareness) Evidence: supervised AI-off test, at least 70% correct
- **LO2** Explain what p-values and confidence intervals mean and identify misreadings of them, given ten statements from synthetic reports (Awareness) Evidence: each statement classified and corrected, eight of ten correct
- **LO3** Identify multiple-testing, forking-path and confounding problems in a reported analysis, given a one-page synthetic summary (Awareness) Evidence: a written critique naming each problem and its effect
- **LO4** Compute bootstrap intervals for means, medians, group differences and regression slopes, given public data with skewed variables (Applied) Evidence: a notebook whose intervals agree on rerun with a new seed
- **LO5** Implement permutation tests and report each result as an effect size with an interval, given two public datasets and stated questions (Applied) Evidence: notebooks with test code, intervals and a plain-language reading
- **LO6** Apply family-wise and false-discovery-rate corrections and measure by simulation how often uncorrected tests produce false findings, given twenty outcomes with no true effect (Applied) Evidence: a table of false-finding rates with and without correction

## Tools

- **Resampling and testing:** SciPy stats, statsmodels, R with the infer package
- **DataFrame library:** pandas, Polars
- **Notebook environment:** JupyterLab, marimo, a free hosted notebook service
- **Hint-only tutor:** an open-weight model in tutor mode, an approved assistant with a tutor instruction

## Prerequisites

- FND-MTH-103 Probability for Data and AI
- Probability shown in the placement test is accepted in place of FND-MTH-103
- Computes group summaries with a DataFrame library (FND-DAT-102 or the pre-work notebook)

## Sources

### Data

- [statsmodels: the RAND Health Insurance Experiment dataset (randhie), public domain](https://www.statsmodels.org/stable/datasets/generated/randhie.html)
- [statsmodels: the Engel food expenditure dataset (engel), public domain](https://www.statsmodels.org/stable/datasets/generated/engel.html)

### Methods and tools

- [SciPy: scipy.stats.bootstrap (default method BCa)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
- [SciPy: scipy.stats.permutation_test (two-sided p-value: twice the smaller one-sided p-value)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
- [statsmodels: multipletests (Bonferroni, Holm, Benjamini-Hochberg)](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)
- [Gelman and Loken (2013), The garden of forking paths: why multiple comparisons can be a problem, even when there is no fishing expedition](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)
- [American Statistical Association (2016), news release on its Statement on Statistical Significance and P-Values, listing the six principles](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf)
- [NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.7.3: Bonferroni's method](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm)
- [SciPy: scipy.stats.false_discovery_control (the Benjamini-Hochberg procedure, citing Benjamini and Hochberg, 1995)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.false_discovery_control.html)

---

SDAIA Academy · Data & AI Foundations Track · Statistics by Simulation: Variation, Estimation and Testing

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-25 · commit 0b561fb
