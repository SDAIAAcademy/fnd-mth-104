---
course: "Statistics by Simulation: Variation, Estimation and Testing"
code: "FND-MTH-104"
version: "2027.1.0"
deck: "week3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-mth-104/slides/week3.html"
---

# Statistics by Simulation: Variation, Estimation and Testing

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
