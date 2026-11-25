# Labs: what each one should show

The numbers below come from running the solution notebooks in full (not quick) mode with the committed data and the
seeds in the notebooks. Quick mode (`STA_QUICK=1`) uses fewer resamples and repeats, so its simulated rates move by a
few points; every number that comes from the data alone is the same.

| Lab | Planted in the data | What the participant should find |
|---|---|---|
| 1.1 | A long right tail; basket BK-M02818 is a till error (9,999.00 for 3 items); BK-M04411 is a real order (612.40 for 140 items); waits missing in 21.3% of BR07's evenings against about 2% elsewhere; BR15's till writes −1 for a missing wait | Mean 24.79 with the error, 23.20 without; median 18.76 both times; IQR 16.45; 324 baskets above the high fence (honest baskets, not errors); skewness 7.67, of the logarithms 0.11 |
| 2.1 | 40,000 baskets: mean 21.931, median 17.61, sd 17.768; members are a third of baskets and spend more | Simulated standard error of the mean 3.60, 1.81 and 0.86 at n = 25, 100 and 400, against σ/√n 3.55, 1.78 and 0.89; a members-only frame is about 2.5 riyals too high at n = 100 and at n = 1,600 |
| 3.1 | Managers put the display in 10 of 12 large branches and 2 of 12 small ones; large branches waste more | Display 7.3% against 6.2% overall (+1.06 points), but 1.41 points lower in large branches and 1.22 lower in small ones; the randomised discount changed waste by −0.87 points against control; the trial's arms have 6 large branches each and an uneven spread over sectors, by chance |
| 4.1 | The known quarter of baskets | The first sample of 50 gives a mean interval 14.59 to 19.94 that misses the true mean 21.93 (a reminder that 95% is about the method); coverage of the percentile interval for the mean 0.853, 0.897 and 0.920 at n = 10, 30 and 100, for the median 0.937, 0.932 and 0.939; SciPy's percentile interval equals the participant's, its default BCa is 14.82 to 20.25 |
| 5.1 | Public data: three plan-by-health cells under 30 rows | Free care 3.12 visits a year against 2.11 at 95% coinsurance, difference 1.01 (0.83 to 1.18), an interval too narrow because rows are person-years and the subset has no person identifier to resample people by; medians 2 and 1 with degenerate intervals; slope of food on income 0.485 (0.405 to 0.594); every end moves by under 4% of the interval's width on rerun |
| 6.1 | Public data | Exact p of the tiny case 0.1 (SciPy's two-sided 0.2: twice the smaller one-sided p); Q1 difference 1.01 visits, ratio 1.48 (1.37 to 1.60), p at the floor 1/5,001 (SciPy's two-sided floor is 2/2,001 with its 2,000 shuffles); Q2 r = 0.91 (0.89 to 0.95), p at the floor; two random halves of one plan give p = 0.84 |
| 7.1 | Twenty product lines with no true effect | Lines L07 (p = 0.030) and L10 (0.048) pass uncorrected; none after any correction; over 1,000 noise dashboards: single tests 4.9%, at least one finding uncorrected 62.7% (theory 64.2%), Bonferroni, Holm and BH 3.5% each; one planned test 5.0% against 19.0% for the best of eight analysis paths |
| 8.1 | The known quarter as the customers; a multiplicative 10% uplift (0.12 standard deviations) | Type I error rate 0.050, 0.034 and 0.035 at 50, 200 and 800 per group (near α, within Monte Carlo error); power 0.100, 0.263 and 0.658; one simulated trial at 200 per group: +3.46 riyals (−0.05 to 7.49), p = 0.08, "unclear" against the 1.50 threshold |

The worked answers to the problem sets, both supervised tests, the LO2 and LO3 assessment sheets and the oral
check's change cards are not in this repository.
