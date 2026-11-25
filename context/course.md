---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/"
---

# Statistics by Simulation: Variation, Estimation and Testing

Reason about variation, estimates and tests by simulating them, and report effect sizes with intervals, their limits and how each was checked

Participants approach inference by simulation before formulas. They draw repeated samples to see variation, build bootstrap intervals for means, medians, differences and slopes, run permutation tests, and report effect sizes with intervals rather than bare p-values. They find multiple-testing and forking-path problems in reported results. Each lab ends with a note on how the result was checked, and the capstone is an analysis brief on a public dataset, defended orally. Power analysis and study design follow in SPC-STA-201 and SPC-EXP-201.

- **Audience:** Beginners. Career changers and non-computing graduates closing bridging gaps before advanced study, and computing graduates refreshing the mathematics behind models; a placement test lets participants skip any course whose content they already command.
- **Prerequisites:** FND-MTH-103 Probability for Data and AI; Probability shown in the placement test is accepted in place of FND-MTH-103; Computes group summaries with a DataFrame library (FND-DAT-102 or the pre-work notebook)
- **Case study:** The bakery chain (fictional): An unnamed chain of 24 neighbourhood bakeries in one city, with branches coded BR01 to BR24 and product lines L01 to L20; the labs speak to its operations manager, quality lead, finance analyst and customer insight lead by role only. Its data (a month of baskets, a known quarter of 40,000 baskets, waste records, a randomised discount trial and a promotion dashboard) is synthetic, written with seed 104; weeks 5 and 6 add two public-domain datasets bundled with statsmodels, read at run time and never copied into the course.

## Outcomes

- LO1 (Awareness): Distinguish population, sample, parameter, statistic and sampling distribution, and explain what a standard error measures, given repeated samples from a known synthetic population
- LO2 (Awareness): Explain what p-values and confidence intervals mean and identify misreadings of them, given ten statements from synthetic reports
- LO3 (Awareness): Identify multiple-testing, forking-path and confounding problems in a reported analysis, given a one-page synthetic summary
- LO4 (Applied): Compute bootstrap intervals for means, medians, group differences and regression slopes, given public data with skewed variables
- LO5 (Applied): Implement permutation tests and report each result as an effect size with an interval, given two public datasets and stated questions
- LO6 (Applied): Apply family-wise and false-discovery-rate corrections and measure by simulation how often uncorrected tests produce false findings, given twenty outcomes with no true effect

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

## Week 2: Sampling variation

The same question, a different sample, a different answer

#### [week2#title] Sampling variation

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 2: The same question, a different sample, a different answer

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week2#agenda] Sampling variation

*This week*

- **Session 1 · Populations, samples and standard error**: Populations, samples and sampling frames, sampling distributions and the standard error by simulation

#### [week2#review-week1] Which change moves the median?

*Review · week 1*

**Question:** Eleven parcel weights have a median of 2.4 kg. Which single change can move the median?

- A. Doubling the heaviest parcel
- B. Halving the lightest parcel
- C. Adding two more parcels, both heavier than 2.4 kg
- D. Rounding every weight to one decimal

### Session 1: Populations, samples and standard error

#### [week2#s1] Populations, samples and standard error

*Session 1*

- Name the population, the sample, the parameter and the statistic of a stated study
- Estimate a standard error by drawing repeated samples and compare it with s/√n
- Explain why a larger sample shrinks the standard error but not the bias of a wrong frame

#### [week2#vocabulary] A parameter describes the population; a statistic is computed from the sample

*Block A · words*

| Word | In a quality check of one day's 2,000 croissants, 30 weighed |
| --- | --- |
| **Population** | All 2,000 croissants of the day |
| **Sample** | The 30 weighed |
| **Parameter** | The mean weight of all 2,000: unknown |
| **Statistic** | The mean weight of the 30: known, and different for another 30 |

#### [week2#samples-differ] Every sample gives a different answer, even from the same population

*Block A · variation*

A population of three values: 3, 9, 12. All samples of two:

| Sample | Mean |
| --- | --- |
| 3, 9 | 6.0 |
| 3, 12 | 7.5 |
| 9, 12 | 10.5 |

- **The sampling distribution.** The list of every possible value of the statistic, with how often each occurs. Here: 6.0, 7.5 and 10.5, each one time in three. Their standard deviation is 1.87.

#### [week2#simulate-it] When the population is known, draw thousands of samples and look

*Block A · simulation*

1. **1 · Draw** A sample of n from the population
2. **2 · Compute** The statistic
3. **3 · Repeat** Two thousand times
4. **4 · Look** Centre, spread, shape

```python
# file: numpy
stats = [np.mean(rng.choice(pop, n, replace=False)) for _ in range(2000)]
```

#### [week2#check-vocabulary] Which number is a statistic?

*Checkpoint*

**Question:** An auditor checks 80 of a branch's 1,200 invoices for the month and finds 6 with errors. Which of these is a statistic?

- A. The share of errors among the 80 checked, 7.5%
- B. The 1,200 invoices of the month
- C. The share of errors among all 1,200 invoices
- D. The number of invoices checked, 80

#### [week2#standard-error] The standard error is the spread of a statistic from sample to sample

*Block B · standard error*

- Not the spread of the values: the spread of the **statistic**
- It answers: how far does my estimate typically land from the truth?
- By simulation: the standard deviation of the thousands of statistics

- **Two spreads, two questions.** Standard deviation of baskets: how different are customers? Standard error of the mean basket: how sure is my estimate?

#### [week2#root-n] For a mean, the standard error falls like one over the square root of n

*Block B · the formula*

| σ = 12 | n | σ / √n |
| --- | --- | --- |
|  | 36 | 2.00 |
|  | 144 | 1.00 |
|  | 576 | 0.50 |

- Four times the data halves the standard error
- σ is unknown in practice: s / √n from one sample stands in
- For a median there is no simple formula: simulate

#### [week2#clt-recap] Sample means tend to a normal shape as n grows, slowly on a long tail

*Block B · recap from FND-MTH-103*

- The central limit theorem: for large n the sampling distribution of a mean is close to normal
- "Large" depends on the population: the longer its tail, the larger n must be
- Simulation shows the actual shape at your n; you do not need to assume it

> **Pointer.** FND-MTH-103 covered the theorem and where the normal approximation fails. Here it is one reason to prefer simulation.

#### [week2#check-se] How many more croissants?

*Checkpoint*

**Question:** Weighing 25 croissants gives a standard error of 2 g for the mean weight. The quality lead wants a standard error of 1 g. About how many croissants must she weigh?

- A. 50
- B. 100
- C. 400
- D. 25, but weighed more carefully

#### [week2#frame] The sampling frame decides which population a sample can speak for

*Block C · the frame*

- The **frame** is the list you can actually draw from: members with contact details, a phone directory, today's visitors
- A random sample from the frame represents the frame, not those outside it
- If those outside differ, the estimate is **biased**

- **Example.** A survey of daytime callers misses everyone who shops after work; their baskets may differ.

#### [week2#bias-precision] Sample size fixes imprecision; it does not fix bias

*Block C · two errors*

- **Imprecision.** Estimates scatter around the truth. Shrinks with n, like 1/√n. Measured by the standard error.
- **Bias.** Estimates centre on the wrong value. The same at every n. Not shown by the standard error at all.

> **What goes wrong.** A huge sample from the wrong frame gives a narrow interval around the wrong number.

#### [week2#check-frame] Precise, but about what?

*Checkpoint*

**Question:** A gym estimates members' weekly visits from 5,000 check-ins logged by its entrance machine, which records only members who use the app to enter. What is the main weakness?

- A. The sample is too small for a stable mean
- B. Visit counts have a large standard deviation
- C. Visits are whole numbers, so the mean is rounded
- D. The frame leaves out members who enter another way

#### [week2#lab-2-1] Repeated sampling from a synthetic population

Lab 2.1 · 105 min

Draw thousands of samples from a known quarter of baskets and measure the standard error.

[W2_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W2_1.ipynb)

- [ ] Set up; the quarter as a known population (10 min)
- [ ] Every sample of a tiny population, by hand (10 min)
- [ ] Two thousand samples at three sizes (20 min)
- [ ] The standard error by simulation against s/√n (15 min)
- [ ] The sampling distribution of the median (15 min)
- [ ] A frame of loyalty members only (15 min)
- [ ] The shape of the sampling distribution at n = 10 (10 min)
- [ ] Record how this was checked (10 min)
- [ ] ✱ Stretch: Does sixteen times n quarter the median's standard error too?

#### [week2#debrief-se] The simulated standard errors followed σ/√n; one sample's s/√n did not always

*Debrief · lab 2.1*

| n | Simulated SE | σ / √n | One sample's s / √n |
| --- | --- | --- | --- |
| 25 | 3.60 | 3.55 | 2.76 |
| 100 | 1.81 | 1.78 | 1.31 |
| 400 | 0.86 | 0.89 | 0.87 |

Population of 40,000 baskets: mean 21.93, median 17.61, sd 17.77, skewness 6.57.

#### [week2#debrief-frame] The members-only frame was 2.5 riyals too high at 100 baskets and at 1,600

*Debrief · lab 2.1*

- **+2.66** bias at n = 100
- **+2.55** bias at n = 1,600

> Sixteen times the sample made the estimate more precise about members, and no closer to all customers.

#### [week2#wrap-up] Three things to keep

*Week 2 · wrap-up*

- **Statistics vary.** A new sample, a new answer; the sampling distribution shows how much.
- **SE is that variation.** The spread of the statistic; for a mean it falls like 1/√n.
- **Frames decide.** Size buys precision, never representativeness.

#### [week2#next] Week 3: Observational and experimental data

*Next*

Problem set 2 (50 minutes, AI off for the first attempt): labs/problem-sets/PS2.ipynb.

## Week 3: Observational and experimental data

Who chose the treatment decides what a comparison can show

#### [week3#title] Observational and experimental data

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 3: Who chose the treatment decides what a comparison can show

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week3#agenda] Observational and experimental data

*This week*

- **Session 1 · Confounding and Simpson's paradox**: Observational versus experimental data, confounding and Simpson's paradox, and what randomisation buys

#### [week3#review-week2] What shrinks when the sample grows?

*Review · week 2*

**Question:** A survey's sample grows from 200 to 800 people drawn from the same frame. What happens to the standard error of the mean and to the bias from the frame?

- A. Both are halved
- B. The standard error falls to a quarter; the bias is unchanged
- C. Neither changes
- D. The standard error is halved; the bias is unchanged

### Session 1: Confounding and Simpson's paradox

#### [week3#s1] Confounding and Simpson's paradox

*Session 1*

- Tell observational from experimental data from how the treatment was assigned
- Find a confounder that reverses a comparison (Simpson's paradox) and compare within its levels
- Explain what a randomised assignment guarantees and what it does not

#### [week3#two-kinds] Who chose the treatment decides what a comparison can show

*Block A · two kinds of data*

- **Observational.** Someone else decided who got what: managers, customers, history. The groups may differ in many ways besides the treatment.
- **Experimental.** A random draw decided. The groups differ in the treatment, and otherwise only by chance.

> **Ask of every comparison:** how were the groups formed?

#### [week3#examples-kinds] The same question can be studied either way

*Block A · examples*

| Question | Observational version | Experimental version |
| --- | --- | --- |
| Does a loyalty discount raise visits? | Compare customers who signed up with those who did not | Offer the discount to a random half |
| Does a new oven cut burnt trays? | Compare branches that bought one | Install it in branches drawn at random |
| Does training cut errors? | Compare staff who chose the course | Enrol a random half first |

#### [week3#check-kind] Observational or experimental?

*Checkpoint*

**Question:** A depot tries a new route plan. Drivers who volunteered used it for a month; their deliveries were 6% faster than other drivers'. What kind of evidence is this, and what is its main weakness?

- A. Experimental; the month is too short
- B. Observational; volunteers may be faster drivers anyway
- C. Observational; too few deliveries were timed
- D. Experimental; the groups worked in the same month

#### [week3#confounder] A confounder drives both who gets the treatment and the outcome

*Block B · confounding*

**Confounder** Branch size → **Treatment** Who gets the new equipment

**Confounder** Branch size → **Outcome** The waste rate

> **What goes wrong.** The comparison of treated and untreated mixes the treatment's effect with the confounder's.

#### [week3#simpson-lines] Line P damages fewer items in each product and more overall

*Block B · Simpson's paradox*

| Damaged / packed | Rolls | Cakes | Overall |
| --- | --- | --- | --- |
| Line P | 6 / 200 = 3% | 40 / 400 = 10% | 46 / 600 = 7.7% |
| Line Q | 20 / 500 = 4% | 13 / 100 = 13% | 33 / 600 = 5.5% |

P packs mostly cakes, which are damaged more on any line.

#### [week3#compare-within] Compare within levels of the confounder, then combine with the same weights

*Block B · what helps*

- **Stratify:** compare within rolls and within cakes
- **Standardise:** apply each line's rates to the same mix of products
- Both need the confounder to be **known and recorded**

- **The limit.** An unrecorded confounder cannot be adjusted for. Only a random assignment protects against those.

#### [week3#check-simpson] Which hospital would you choose?

*Checkpoint*

**Question:** Hospital H has a higher overall death rate than hospital K, but a lower rate both for routine and for emergency admissions. H takes most of the region's emergencies. Which hospital has the better record for a given kind of admission?

- A. K, because its overall rate is lower
- B. Neither: the figures contradict each other
- C. H, because it does better within each kind of admission
- D. Neither until both treat the same number of patients

#### [week3#randomisation] A random assignment makes every difference between groups a matter of chance

*Block C · randomisation*

- Recorded or not, every characteristic is shared out by the same draw
- The groups are **not identical**: by chance one may hold more large branches
- So the difference in outcomes still varies: is it larger than chance alone would give? Week 6 answers that with a permutation test

> **Check balance:** count the obvious characteristics in each arm, and report any imbalance rather than "fixing" it afterwards.

#### [week3#limits-experiment] An experiment answers one question about the units it was run on

*Block C · limits*

- **Scope.** 24 branches in one city in one season: say so.
- **Compliance.** A branch assigned the discount may not apply it every evening.
- **Size.** Few units mean a lot of chance variation in the difference.

#### [week3#check-random] What does randomisation buy?

*Checkpoint*

**Question:** Twenty schools are assigned a reading programme at random, ten each way. The programme schools happen to have slightly more pupils on average. What is the right reading?

- A. A chance imbalance: report it; the comparison is still fair on average
- B. The randomisation failed and must be redone
- C. Any difference in reading scores is caused by the programme
- D. The study is now observational

#### [week3#lab-3-1] Confounding in the waste records, against a randomised trial

Lab 3.1 · 105 min

Explain why the display looks worse overall and better within each size, beside a randomised trial.

[W3_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W3_1.ipynb)

- [ ] Set up; observational and experimental data (10 min)
- [ ] Simpson's paradox by hand on a small table (15 min)
- [ ] Waste rate by display, all branches together (10 min)
- [ ] Waste rate by display within each branch size (15 min)
- [ ] Who chose the display: the confounder (10 min)
- [ ] The randomised trial: balance and the difference (20 min)
- [ ] Balance of size and sector in the two studies (15 min)
- [ ] Record how this was checked (10 min)
- [ ] ✱ Stretch: Standardise the display comparison to the chain's mix of branch sizes

#### [week3#debrief-display] The display looked 1.06 points worse overall and was better within each size

*Debrief · lab 3.1*

| Waste rate | No display | Display | Difference |
| --- | --- | --- | --- |
| Large branches | 9.0% | 7.6% | −1.41 |
| Small branches | 5.0% | 3.8% | −1.22 |
| All branches | 6.2% | 7.3% | +1.06 |

Managers put the display in 10 of 12 large branches and 2 of 12 small ones.

#### [week3#debrief-trial] The randomised discount cut waste by 0.87 points against control

*Debrief · lab 3.1*

- Each arm had 6 large branches of 12: balanced on size, this time, by chance
- Sectors were not balanced: one sector had 5 control branches and no discount branch
- With 24 branches, is −0.87 more than chance? The permutation test of week 6 answers that kind of question

#### [week3#wrap-up] Three things to keep

*Week 3 · wrap-up*

- **Ask who chose.** Observational groups can differ in everything.
- **Compare within.** A recorded confounder can reverse an overall comparison.
- **Randomise when you can.** It handles the confounders nobody recorded.

#### [week3#next] Week 4: The bootstrap

*Next*

Problem set 3 (50 minutes, AI off for the first attempt): labs/problem-sets/PS3.ipynb. The first supervised test follows week 4.

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

## Week 8: Error rates, power and honest reporting

How often a test errs, and how to say what was checked

#### [week8#title] Error rates, power and honest reporting

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Week 8: How often a test errs, and how to say what was checked

Data & AI Foundations Track · 8 weeks + capstone · 1 session · 1 lab · FND-MTH-104

#### [week8#agenda] Error rates, power and honest reporting

*This week*

- **Session 1 · Type I and II errors, power and reporting**: Type I and Type II errors and a first look at power by simulation, effect size and practical significance, and recording how each result was checked

#### [week8#review-week7] Which correction, and what does it promise?

*Review · week 7*

**Question:** A safety report makes five claims, each of which would trigger a costly recall. The analyst wants a low chance of even one false claim. Which procedure fits?

- A. Benjamini-Hochberg
- B. No correction, α = 0.05 each
- C. Holm, which controls the family-wise error rate
- D. Report only the claim with the smallest p-value

### Session 1: Type I and II errors, power and reporting

#### [week8#s1] Type I and II errors, power and reporting

*Session 1*

- Estimate a test's Type I error rate and power by simulation at several sample sizes
- Judge practical significance by comparing an interval with a threshold that matters
- Write a result with its scope, limits and a record of how it was checked

#### [week8#simulate-errors] Simulate the study many times, with and without an effect, and count rejections

*Block A · measure the errors*

1. **1 · Generate** Data as the study would collect it
2. **2 · Add** No effect, or the effect that matters
3. **3 · Test** Exactly as planned
4. **4 · Count** Rejections: Type I rate, or power

#### [week8#power-table] For a half-standard-deviation effect, 10 per group finds it one time in five

*Block A · power grows with n*

| n per group | Power of the t test, α = 0.05 |
| --- | --- |
| 10 | 0.185 |
| 30 | 0.478 |
| 100 | 0.940 |

- Normal data, a difference of 0.5 standard deviations
- Smaller effects or longer tails need more data
- The Type I error rate stays at α at every n

#### [week8#check-power] What does the null result say?

*Checkpoint*

**Question:** A pilot with 10 customers per group finds no significant effect of a new menu on spending. A simulation says the test had 18% power for the effect that would matter. What should the report say?

- A. The new menu does not change spending
- B. The false-finding rate was 82%
- C. The new menu reduces spending
- D. The pilot was too small to tell; it would miss that effect about four times in five

#### [week8#false-share] With few real effects and low power, nearly half the findings are false

*Block B · findings*

| 100 ideas tested, 10 real | Expected |
| --- | --- |
| False findings: 90 × 0.05 | 4.5 |
| True findings: 10 × 0.5 power | 5.0 |
| Share of findings that are false | 47% |

- **Not 5%.** α is the rate among true nulls, not the share of findings that are wrong. That share depends on power and on how many ideas are real.

#### [week8#practical] Compare the interval with the smallest effect that would change the decision

*Block B · practical significance*

- **Worth it.** The whole interval is above the threshold.
- **Not worth it.** The whole interval is below it, even if p is tiny.
- **Unclear.** The interval straddles it: more data, or a decision that accepts the risk.

#### [week8#check-practical] Decide

*Checkpoint*

**Question:** A new delivery route must save at least 3 minutes a trip to justify the change. A trial gives a saving of 1.1 minutes, 95% interval 0.6 to 1.6, p < 0.001. What is the decision?

- A. Adopt it: the saving is highly significant
- B. Do not adopt it: even the top of the interval is below 3 minutes
- C. Unclear: run a larger trial
- D. Adopt it: p below 0.001 means a large saving

#### [week8#honest-report] Every result travels with its scope, its limits and how it was checked

*Block C · honest reporting*

| Part of the note | What it says |
| --- | --- |
| Result | The estimate, its interval, the test, in plain words |
| Checked by | A hand case, a second method, a rerun with a new seed, a known truth |
| Limits | Scope, confounding, the number of tests, suppressed groups |
| Reviewer | A second person reruns it before it is used |

#### [week8#ai-assisted] In the capstone you may use an AI assistant; record how you checked what it gave you

*Block C · AI-assisted analysis*

- The capstone is AI-full and defended orally: you must be able to rerun every step yourself
- For each assisted step: what it produced, how you checked it, what was wrong
- Only public material goes into a generative AI tool: nothing classified above Public

> Checking assisted analysis run to run is taught in SPC-ANL-202.

#### [week8#capstone-brief] A two-page brief on a public dataset: estimate, interval, test, effect size and limits

*Block C · the capstone*

- A public dataset whose licence allows reuse, with no personal data
- One question, written down with its analysis before you look
- The notebook reruns; intervals agree with a new seed

- **Then a ten-minute oral check.** Three minutes on the brief; seven rerunning one test with a change the assessor specifies, and reading the result.

#### [week8#check-report] What is missing from this note?

*Checkpoint*

**Question:** A note says: "Result: the new rota cut overtime by 6 hours a month (interval 2 to 10). Checked by: an assistant wrote the code. Limits: one region. Reviewer: the team lead." What is the weakest part?

- A. "Checked by": it says who wrote the code, not how the result was verified
- B. "Result": it should give the p-value instead of the interval
- C. "Limits": a limit should never be stated in a report
- D. "Reviewer": the analyst should review their own work

#### [week8#lab-8-1] Type I error rate and power of a permutation test estimated by simulation at three sample sizes

Lab 8.1 · 105 min

Simulate a planned trial with and without a 10% uplift to estimate Type I error and power.

[W8_1.ipynb](https://sdaiaacademy.github.io/fnd-mth-104/labs/W8_1.ipynb)

- [ ] Set up; the planned trial and its question (10 min)
- [ ] Type I and II errors by hand (10 min)
- [ ] A fast permutation test with fixed shuffles (15 min)
- [ ] The Type I error rate at 50, 200 and 800 per group (20 min)
- [ ] Power at the same sizes for a 10% uplift (20 min)
- [ ] Effect size and practical significance (15 min)
- [ ] The note, and your capstone plan (15 min)
- [ ] ✱ Stretch: Welch's t test on the same trials

#### [week8#debrief-power] A 10% uplift on baskets: found one time in ten at 50 per group, two in three at 800

*Debrief · lab 8.1*

| n per group | Type I error rate | Power, 10% uplift |
| --- | --- | --- |
| 50 | 0.050 | 0.100 |
| 200 | 0.034 | 0.263 |
| 800 | 0.035 | 0.658 |

1,000 simulated trials per cell, Monte Carlo error up to about ±0.03. The Type I error rate stayed near α at every size.

#### [week8#debrief-decision] One trial at 200 per group: +3.46 riyals, interval −0.05 to 7.49, decision unclear

*Debrief · lab 8.1*

- p = 0.08: not below 0.05, and the uplift was real in the simulation
- The interval straddles the 1.50 threshold: unclear, not "no effect"
- At 200 per group, 3 trials in 4 would miss this uplift: plan the size first (SPC-STA-201, SPC-EXP-201)

#### [week8#wrap-up] Three things to keep

*Week 8 · wrap-up*

- **Simulate the plan.** Count false findings and missed effects before you run the study.
- **Decide on the interval.** Against the threshold that matters, not on p.
- **Note every result.** Scope, limits, how it was checked, who reran it.

#### [week8#next] The capstone, and the second supervised test

*Next*

Problem set 8 (50 minutes, AI off for the first attempt): labs/problem-sets/PS8.ipynb. Then the second test, 90 minutes, AI off, and the capstone brief.

## Capstone: Capstone oral checks

Ten minutes each: three to walk through the brief, seven to rerun one test with the assessor's change and read the result

#### [capstone#title] Capstone oral checks

*SDAIA Academy · Statistics by Simulation: Variation, Estimation and Testing*

Capstone: Ten minutes each: three to walk through the brief, seven to rerun one test with the assessor's change and read the result

Data & AI Foundations Track · 8 weeks + capstone · 3 min talk and demo · 7 min Q&A · FND-MTH-104

#### [capstone#agenda] How the oral checks run

*Capstone*

- **Expectations and final preparation**: the rubric, the oral check, a last rerun of each notebook
- **Oral checks**: ten minutes each: the brief, then a rerun with a change
- **Review and closing**: the trainer's review, what next

#### [capstone#rubric] The rubric

*How the brief and notebook are scored (30% of the course)*

| Item | Value |
| --- | --- |
| Question, data, licence, scope; small groups suppressed | 15% |
| Bootstrap interval, resampled as collected, stable on rerun | 25% |
| Permutation test, effect size with interval, plain reading | 25% |
| Limits: confounding, many tests, forking paths | 20% |
| Reruns; how each result and AI step was checked | 15% |

#### [capstone#oral-format] Ten minutes: three on the brief, seven rerunning one test with a change

*The oral check · 10% of the course*

- **1 · The brief.** The question, the estimate with its interval, the test, the limits. Three minutes.
- **2 · The change.** The assessor names one change: a subgroup, a statistic, a number of shuffles, a seed.
- **3 · The rerun.** You make the change, rerun the test and read the new result aloud.

> Say what you expect before you run it, then compare. The reading matters as much as the code.

#### [capstone#oral-scoring] The oral check rewards a correct rerun and an honest reading

*What the assessor listens for*

| The assessor checks | A strong answer |
| --- | --- |
| The change is made correctly | The right line changed; the notebook reruns |
| The new result is read | Effect size and interval first; the p-value read as a conditional |
| What the change means | Says whether it strengthens or weakens the conclusion, and why |

#### [capstone#running-order] Who is checked when

*Running order*

| # | Participant | Dataset |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final preparation · 20 minutes

*Before the first oral check*

Restart your notebook and run it from the top. Know where your test's code is.

#### [capstone#now-presenting] The brief

*Oral check*

##### The change and the rerun

#### [capstone#review] What the briefs showed

*Trainer review*

- **Strongest patterns.** What several briefs got right.
- **Common gaps.** What most briefs would fix next.
- **One surprise.** Something nobody expected.

#### [capstone#what-next] Keep going

*After the course*

- **Your brief stays yours:** keep the notebook reproducible, with its seed, source and licence
- **SPC-STA-201** Statistical Inference by Simulation: clustered data, better intervals, power by simulating the planned analysis
- **SPC-EXP-201** Designing and Reading Experiments: pre-registration and sample size
- **SPC-ANL-202** Analysis with AI Assistants: checking assisted analysis run to run

#### [capstone#thanks] Thank you

*SDAIA Academy*

Statistics by Simulation: Variation, Estimation and Testing
