---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week8"
day: 8
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week8.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

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
