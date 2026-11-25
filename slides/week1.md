---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week1.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

## Week 1: Describing data

A typical value, its spread, and who is missing from the data

#### [week1#title] Describing data

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 1: A typical value, its spread, and who is missing from the data

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week1#agenda] Describing data

*This week*

- **Session 1 · Centre, spread, shape and missing values**: Centre and spread with the median and interquartile range, distribution shape and outliers, and missing data in summaries

#### [week1#setup-check] Check that a lab notebook runs on your machine or in the hosted notebook

*Before we start*

- **Hosted:** open the pre-work notebook from the course page; its first cell clones the course and installs what it needs
- **Local:** from `labs/`, run `uv run --with jupyterlab jupyter lab`
- The proof: the pre-work notebook runs to its last cell

- **Pre-work.** Group summaries with a DataFrame library, 60 minutes. Done before today if you have not taken FND-DAT-102.

#### [week1#case-intro] All term you are the new analyst of a chain of 24 neighbourhood bakeries

*The case study*

- Branches BR01 to BR24 in five sectors of one city; product lines L01 to L20
- Four readers ask the questions: the operations manager, the quality lead, the finance analyst and the customer insight lead
- Every file is synthetic and generated with a fixed seed, so everyone gets the same numbers

- **Why synthetic.** You can know the truth. In weeks 2, 4 and 8 a whole quarter of baskets plays the population, so every estimate can be checked against it.

### Session 1: Centre, spread, shape and missing values

#### [week1#s1] Centre, spread, shape and missing values

*Session 1*

- Choose between the mean, the median and a trimmed mean for a long-tailed variable and justify the choice
- Compute and read the interquartile range and the fences, and decide whether an extreme value is an error
- Report a summary with the share and the likely direction of missing data

#### [week1#mean-median-questions] The mean and the median answer different questions

*Block A · centre*

Nine catering orders, in riyals:

40, 45, 50, 52, 55, 58, 60, 75, 400

| Summary | Value |
| --- | --- |
| Mean | 92.78 |
| Median | 55.00 |
| 20% trimmed mean | 56.43 |

- The **mean** is the total shared out equally: useful for budgets
- The **median** is the middle order: "a typical order"
- The **trimmed mean** drops a share at each end, then averages

#### [week1#robust] One mistyped value moves the mean and leaves the median alone

*Block A · robustness*

- **92.78 → 492.78** the mean, when 400 is keyed as 4000
- **55.00 → 55.00** the median, unchanged

> **Robust** means one bad row cannot drag the summary far. The median and the trimmed mean are robust; the mean and the standard deviation are not.

#### [week1#long-tail] Money, waits and counts usually have a long right tail

*Block A · shape*

- Most values are small; a few are much larger; none are below zero
- The mean sits above the median, pulled by the tail
- **Skewness** measures the lean: 0 for a symmetric shape, large and positive for a long right tail
- On a log scale the tail often becomes nearly symmetric

> **For a report.** Say which summary you used and why: "median basket" and "mean basket" are different numbers.

#### [week1#check-centre] Which summary for this request?

*Checkpoint*

**Question:** The finance analyst must forecast next month's total delivery charges from this month's 2,000 deliveries, whose charges have a long right tail. Which summary of this month's charges does the forecast need?

- A. The median charge
- B. The 20% trimmed mean charge
- C. The mean charge
- D. The interquartile range of the charges

#### [week1#spread] The interquartile range is the width of the middle half

*Block B · spread*

| The nine orders | Value |
| --- | --- |
| Q1 (25th percentile) | 50.00 |
| Q3 (75th percentile) | 60.00 |
| IQR = Q3 − Q1 | 10.00 |
| Standard deviation | 115.64 |

- The standard deviation is dominated by the one large order
- The IQR describes the eight ordinary ones
- Percentiles have several rules; NumPy's default interpolates. Say which you used

#### [week1#fences] A fence flags values to look at; it is not a rule for deleting them

*Block B · outliers*

1. **1 · Fence** Q3 + 1.5 × IQR = 60 + 15 = 75
2. **2 · Flag** 400 is above it
3. **3 · Look** Is it an error or a real order?

> **What goes wrong.** In a long right tail many honest values sit above the fence. Deleting them all makes the data look tamer than the business is.

#### [week1#error-or-real] Decide "error or real" from evidence in the other columns

*Block B · evidence*

- **Value per item.** Ten items for 400 is plausible; three items for 4,000 is not.
- **Source.** A till known to repeat a key, a manual entry, an import from another system.
- **Context.** A catering booking that day; a branch that was closed; a time outside opening hours.

> **Rule of the course:** remove only what you can show is an error, remove it alone, and say so in the note.

#### [week1#check-outlier] What do you do with this order?

*Checkpoint*

**Question:** A month of 3,000 coffee orders has a high fence of 31 riyals. Forty orders lie above it, the largest 96 riyals for 14 drinks at a branch next to an office block. What do you do?

- A. Keep it: value per drink is ordinary, so it is a real large order
- B. Delete all forty orders above the fence
- C. Replace it with the fence value, 31
- D. Delete it, because it will distort the median

#### [week1#missing-cause] Missing values have a cause, and the cause decides the bias

*Block C · missing data*

| Why the value is missing | What dropping the rows does |
| --- | --- |
| By chance: a form lost at random | Fewer rows, no bias |
| Linked to something recorded: more gaps on weekends | Bias, fixable by comparing within the recorded groups |
| Linked to the value itself: long waits not logged when staff are busy | Bias that the data cannot reveal: waits look shorter than they are |

#### [week1#missing-codes] A missing value may not look missing: check for codes before you summarise

*Block C · codes*

- Empty cells become NaN when read
- Some systems write 0, −1, 999 or a date like 1900-01-01 instead
- A code left as a number quietly enters the mean

```python
# file: pandas
# share empty
df["x"].isna().mean()
# impossible values
(df["x"] < 0).sum()
# decode, then report
bad = df["x"] < 0
df.loc[bad, "x"] = np.nan
```

#### [week1#report-missing] Report the missing share and its likely direction beside every summary

*Block C · reporting*

- **A sentence that does the job has four parts.** The summary of the recorded values; the share not recorded; where the gaps are; and which way they probably move the true value.

> **Every lab ends with a note:** the result, how it was checked, its limits, and who reruns it before it is used. The analyst who ran it does not sign it off alone.

#### [week1#check-missing] Which way does the bias run?

*Checkpoint*

**Question:** A delivery service logs delivery times by hand. Drivers often skip the log when they are running late. The median of the logged times is 28 minutes. What is the most likely relation to the true median?

- A. About the same, since a median ignores missing rows
- B. The true median is lower than 28 minutes
- C. Impossible to say, because medians are robust
- D. The true median is higher than 28 minutes

#### [week1#lab-1-1] Describing the chain's baskets

Lab 1.1 · 105 min

Describe a month of baskets with robust summaries, settle two extreme baskets, and find who is missing.

[W1_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W1_1.ipynb)

- [ ] Set up and load the month of baskets (10 min)
- [ ] Centre: mean, median and trimmed mean (15 min)
- [ ] Spread: SD, IQR and the fences (15 min)
- [ ] Shape: skewness, bins and the log scale (15 min)
- [ ] Two extreme baskets: an error or a real order? (15 min)
- [ ] Missing waits: decode and locate them (20 min)
- [ ] Branch summaries with the missing share (10 min)
- [ ] Record how this was checked (5 min)
- [ ] ✱ Stretch: The mean wait under three ways of handling missing waits

#### [week1#debrief-centre] One till error moved the mean by 1.59 riyals and the median not at all

*Debrief · lab 1.1*

| 6,278 baskets | Mean | Median | 20% trimmed |
| --- | --- | --- | --- |
| With the till error | 24.79 | 18.76 | 19.56 |
| Without it | 23.20 | 18.76 | 19.55 |

The error: 9,999.00 for 3 items. The real order: 612.40 for 140 items. 324 baskets sit above the high fence, all honest.

#### [week1#debrief-missing] Waits were missing in 21% of the busiest branch's evenings, about 2% elsewhere

*Debrief · lab 1.1*

- Overall only 3.6% of waits are missing: the average hides where they are
- The busiest branch's median recorded wait (4.1 minutes) is already the longest, and probably understated
- One branch's till wrote −1 for "not recorded": decoded before any summary

#### [week1#wrap-up] Three things to keep

*Week 1 · wrap-up*

- **The question picks the summary.** Mean for totals, median for "typical"; say which.
- **Fences flag, evidence decides.** Remove only proven errors, one at a time.
- **Missing has a cause.** Report the share and the direction of the bias.

#### [week1#next] Week 2: Sampling variation

*Next*

Problem set 1 (50 minutes, AI off for the first attempt): labs/problem-sets/PS1.ipynb.
