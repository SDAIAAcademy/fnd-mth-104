<!-- academy:title -->
# Statistics by Simulation: Variation, Estimation and Testing

الإحصاء بالمحاكاة: التفاوت والتقدير والاختبار

Data & AI Foundations Track · SDAIA Academy · FND-MTH-104 · Level 100

Reason about variation, estimates and tests by simulating them, and report effect sizes with intervals, their limits and how each was checked

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
| Week 1 | Describing data | Centre, spread, shape and missing values | [`slides/week1.html`](slides/week1.html) |
| Week 2 | Sampling variation | Populations, samples and standard error | [`slides/week2.html`](slides/week2.html) |
| Week 3 | Observational and experimental data | Confounding and Simpson's paradox | [`slides/week3.html`](slides/week3.html) |
| Week 4 | The bootstrap | The bootstrap and its coverage | [`slides/week4.html`](slides/week4.html) |
| Week 5 | Intervals for differences and slopes | Differences and slopes | [`slides/week5.html`](slides/week5.html) |
| Week 6 | Permutation tests | Null models, p-values and effect sizes | [`slides/week6.html`](slides/week6.html) |
| Week 7 | Many tests and forking paths | Multiple testing and false discoveries | [`slides/week7.html`](slides/week7.html) |
| Week 8 | Error rates, power and honest reporting | Type I and II errors, power and reporting | [`slides/week8.html`](slides/week8.html) |
| Capstone | Capstone oral checks |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**The bakery chain (fictional).** An unnamed chain of 24 neighbourhood bakeries in one city, branches coded BR01 to BR24 in five sectors and product lines coded L01 to L20, wants to know what a typical basket is, how big a survey must be, whether a display shelf and an evening discount cut waste, whether a promotion worked and how large a trial should be. The labs speak to its operations manager, quality lead, finance analyst and customer insight lead, by role only. Its data is synthetic, written by [`labs/prepare_data.py`](labs/prepare_data.py) with seed 104: a month of 6,278 baskets, a known quarter of 40,000 baskets that plays the population, 144 branch-month waste records, a randomised discount trial on the 24 branches and a promotion dashboard of 20 product lines with no true effect.

Weeks 5 and 6 also use two public datasets, none copied into this repository:

| Dataset | Licence | How the labs get it |
|---|---|---|
| RAND Health Insurance Experiment subset (`randhie`, 20,190 person-years: outpatient visits, randomly assigned coinsurance plan, self-rated health) | Public domain, as stated in the statsmodels documentation | Bundled with statsmodels; read from the installed package, no download |
| Engel's food expenditure data (`engel`, 235 households: income and food spending) | Public domain, as stated in the statsmodels documentation | Bundled with statsmodels; read from the installed package, no download |

Groups with fewer than 30 rows in public data are suppressed before any table is reported (`labs/sta.py`, `suppress`).

## Plan and minutes

The entry's 45 hours, in minutes:

| Catalog hours | Minutes | How they are spent |
|---|---:|---|
| Instruction 14 | 840 | 8 weekly sessions × 105 minutes: three teaching blocks, each closed by a checkpoint, and the lab debrief |
| Lab 14 | 840 | 8 labs × 105 minutes, each with steps timed to the minute, one stretch and a closing note on how the result was checked |
| Guided self-study 8 | 480 | Pre-work notebook 60 ([`labs/PW_group_summaries.ipynb`](labs/PW_group_summaries.ipynb)), 8 problem sets × 50 = 400 ([`labs/problem-sets/`](labs/problem-sets/)), capstone dataset choice and licence check 20 |
| Assessment 3 | 180 | 2 supervised AI-off tests × 90 minutes (45 on paper, 45 at the keyboard), after week 4 and after week 8 |
| Capstone 6 | 360 | Dataset clinic 30, independent analysis and brief 280, peer dry run 25, oral check 10, changeover 5, written feedback 10 |
| **Total** | **2,700** | 45 hours |

## Assessment

| Assessed work | Weight |
|---|---:|
| Weekly problem sets, auto-checked | 20% |
| Two supervised AI-off tests, on paper and at the keyboard | 40% |
| Capstone brief and notebook, rubric-scored | 30% |
| Oral check | 10% |

**Passing:** 60% overall and at least 50% on each supervised test.

**Authenticity:** Proctored tests without assistance, and an oral check in which the participant reruns one test with a change the assessor specifies and reads the result.

**Certificate:** completion with assessed work.

The problem sets are scored by [`labs/problem-sets/pscheck.py`](labs/problem-sets/pscheck.py), which stores no answers: it checks that each hand answer agrees with the participant's own function, and runs the functions on new random data against properties, SciPy or statsmodels. The capstone rubric scores the brief and the notebook only; the oral check is scored on its own, so nothing counts twice.

| Outcome | Where its evidence is collected |
|---|---|
| LO1 | First supervised test (after week 4), at least 70% correct |
| LO2 | Second supervised test, paper part: ten statements from synthetic reports, each classified and corrected, eight of ten correct |
| LO3 | Second supervised test, paper part: a written critique of a one-page synthetic summary, naming each problem and its effect |
| LO4 | Lab 5.1 notebook, whose intervals agree on rerun with a new seed; the capstone notebook |
| LO5 | Lab 6.1 notebook with test code, intervals and plain-language readings; the capstone notebook |
| LO6 | Lab 7.1 notebook with its table of false-finding rates with and without correction |

**Held outside this repository**, in the trainer pack: the worked answers to the problem sets, the blueprint and items of the two tests with their keys (the ten LO2 statements and their corrections, the LO3 one-page summary and its marking rubric), the oral check's change cards with the expected readings, and the capstone marking notes. Publishing them would defeat the assessment. The lab solutions are public, in [`labs/solutions/`](labs/solutions/).

## AI policy

AI-off for first attempts at problem sets and in both tests. AI-tutor in labs, giving hints without answers. AI-full in the capstone, which is defended orally; run-to-run checking of assisted analysis is taught in SPC-ANL-202.

The tutor's instruction is [`labs/tutor/TUTOR.md`](labs/tutor/TUTOR.md). Only public material goes into a generative AI tool: nothing classified above Public.

## Responsible use

Covers honest reporting: participants see how many false findings uncorrected testing produces, state scope and limits in every brief, and record how they checked any AI-assisted analysis. Small groups in public data are suppressed before reporting.


<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Week 1 · Session 1 | Describing the chain's baskets | [`W1_1.ipynb`](labs/W1_1.ipynb) |
| 2.1 | Week 2 · Session 1 | Repeated sampling from a synthetic population | [`W2_1.ipynb`](labs/W2_1.ipynb) |
| 3.1 | Week 3 · Session 1 | Confounding in the waste records, against a randomised trial | [`W3_1.ipynb`](labs/W3_1.ipynb) |
| 4.1 | Week 4 · Session 1 | Bootstrap intervals with coverage checked against a known truth | [`W4_1.ipynb`](labs/W4_1.ipynb) |
| 5.1 | Week 5 · Session 1 | Bootstrap intervals for differences and slopes on public skewed data | [`W5_1.ipynb`](labs/W5_1.ipynb) |
| 6.1 | Week 6 · Session 1 | Permutation tests for a group difference and a correlation on public data | [`W6_1.ipynb`](labs/W6_1.ipynb) |
| 7.1 | Week 7 · Session 1 | Twenty tests on pure noise, with and without correction | [`W7_1.ipynb`](labs/W7_1.ipynb) |
| 8.1 | Week 8 · Session 1 | Type I error rate and power of a permutation test estimated by simulation at three sample sizes | [`W8_1.ipynb`](labs/W8_1.ipynb) |
<!-- /academy:labs -->

## Capstone

A two-page analysis brief on a public dataset with estimate, interval, test, effect size and limits, submitted with its notebook and defended in a ten-minute oral check

**Submission:** a link to a public GitHub repository with the two-page brief, the notebook with its outputs, and the dataset's source and licence; then a ten-minute oral check: three minutes walking through the brief, seven rerunning one test with a change the assessor specifies and reading the result.

| Rubric criterion (the brief and the notebook) | Weight |
|---|---:|
| Question, dataset, source and licence, unit and scope stated; groups under 30 rows suppressed | 15 |
| Estimate with a bootstrap interval resampled the way the data were collected; the interval agrees on rerun with a new seed | 25 |
| Test with its null model stated, a permutation test, the effect size with an interval and a plain-language reading | 25 |
| Limits: confounding, multiple comparisons and forking paths named where they apply, and what the analysis cannot show | 20 |
| Notebook reruns from top to bottom; a record of how each result, and any AI-assisted step, was checked | 15 |

The dataset is the participant's choice: any public dataset whose licence allows reuse (public domain, CC0, CC BY or an open government licence), with no personal data. The datasets bundled with statsmodels and marked public domain are a ready list to start from.

## Repository

```
course.json      the course manifest: outcomes, units, sessions, labs, capstone, tools, sources
slides/          one deck per week and the capstone deck; the engine builds them into the course site
labs/            the lab notebooks and their solutions, the pre-work notebook, the problem sets and their
                 checker, the helper module (sta.py), the data generator (prepare_data.py), the tutor instruction
assessments/     the public practice questions (bank.json); test items are never kept here
```

Build and check with the Academy engine: `node academy.mjs check`, `node academy.mjs build`.

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

### Data

- [statsmodels: the RAND Health Insurance Experiment dataset (randhie), public domain](https://www.statsmodels.org/stable/datasets/generated/randhie.html)
- [statsmodels: the Engel food expenditure dataset (engel), public domain](https://www.statsmodels.org/stable/datasets/generated/engel.html)

### Methods and tools

- [SciPy: scipy.stats.bootstrap (default method BCa)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
- [SciPy: scipy.stats.permutation_test (two-sided p-value: twice the smaller one-sided p-value)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
- [statsmodels: multipletests (Bonferroni, Holm, Benjamini-Hochberg)](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)
- [Gelman and Loken (2013), The garden of forking paths: why multiple comparisons can be a problem, even when there is no fishing expedition](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)
<!-- /academy:sources -->

### National references

- SDAIA Data & AI Academic Programs Standards Framework (2026): bridging unit MSF-Statistics at Explain level (one of the framework's common prerequisite and bridging knowledge units for post-bachelor programmes, section 3.6, Second Version, September 2026): https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/Academic-Programs-Standards-Framework-Q3.pdf
