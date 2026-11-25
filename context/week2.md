---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week2.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

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
