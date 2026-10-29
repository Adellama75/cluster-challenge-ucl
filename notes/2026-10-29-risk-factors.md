# Thu 29 Oct: which factors predict resistance, and which are noise

Script: `src/risk_factors.py`. Results: `outputs/risk_factors_*`. Every number below comes from that
run (seed 42, 100 shuffled copies per factor). It takes about 2 minutes on a laptop.

## Why we did this

The brief asks "What are the main risk factors?" Until now we had only compared age and imd, and the
evidence was the random forest's feature importance (age 0.91, imd 0.09). That left two gaps. The
other columns had never been tested, and a small importance doesn't say whether a factor is real or
chance. So we tested every patient factor in the data, one at a time and all together, against noise.

## What counts as a candidate

Patient factors known before the lab result: age, sex, surgery in the past year, deprivation (imd
quintile), ethnicity, NHS trust (238 trusts) and diagnosis (ICD code, grouped by its first letter,
because there are 964 different codes for 1000 patients). Left out, and why:

- `id` and `dob`: identifiers. Age is the whole years from date of birth to specimen date, so `dob`
  adds nothing beyond age.
- `organism`: always E. coli.
- `spec_date`: all 36 dates fall between 25 May and 29 June 2014, so there's no trend to find.
- `cipro` and `gentam`: resistance results from the same sample. They aren't known before the test,
  so using them as predictors would be cheating. Co-resistance is weak here anyway: co-amoxiclav
  resistance is 28% in the 89 cipro-resistant samples against 24% in the rest, and 22% in the 41
  gentamicin-resistant ones against 24%.

We also added a column of random numbers as a control. It should come out as noise.

## Method, and why each step

1. **Each factor on its own, in two simple models.** A logistic regression (categories become one
   0/1 column per level) and a class-balanced decision tree of depth 2. Both are scored by 5-fold
   cross-validated ROC AUC. AUC doesn't depend on a threshold: 0.5 means the factor ranks resistant
   patients no better than chance. Cross-validation matters because a factor with many levels can fit
   the training patients well by luck and then fail on new ones.
2. **A noise level for each factor, from shuffled copies.** We shuffle the factor's values across
   patients 100 times and score each shuffled copy. Shuffling breaks any real link with resistance but
   keeps the factor's levels and how common each one is, so the shuffled scores show how high this
   factor can score by luck. That differs a lot between factors: 238 trusts leave far more room for a
   lucky score than a yes/no column. A factor beats noise only if both models score above 95% of their
   shuffled copies (p ≤ 0.05).
3. **All factors together, as a regression.** One logistic regression with age (per 10 years), sex,
   surgery, imd and ethnicity gives adjusted odds ratios with 95% intervals. It checks whether a
   factor matters once the others are accounted for. Trust and ICD chapter are left out: with about 4
   patients per trust there's nothing to estimate.
4. **All factors together, in trees.** The same random forest as our best model (depth 3, 200 trees,
   class-balanced, same train/test split), given the patient factors plus two noise columns: one
   continuous like age, one with five levels like imd. Its permutation importance is how much the
   test-set AUC drops when one column is shuffled. A real risk factor has to clear the noise columns.

## Results

Each factor on its own: cross-validated ROC AUC, with the score that 95% of its shuffled copies stay
below in brackets.

| Factor | Regression | Tree | Verdict |
|---|---|---|---|
| Age | 0.708 (0.540) | 0.685 (0.533) | beats noise: p = 0.01, the smallest possible with 100 copies |
| Sex (male) | 0.522 (0.535) | 0.522 (0.534) | noise |
| Surgery in past year | 0.478 (0.519) | 0.478 (0.520) | noise |
| Deprivation (imd quintile) | 0.537 (0.551) | 0.521 (0.541) | noise |
| Ethnicity | 0.506 (0.543) | 0.503 (0.537) | noise |
| NHS trust (238) | 0.501 (0.550) | 0.504 (0.512) | noise |
| Diagnosis (ICD chapter) | 0.510 (0.547) | 0.524 (0.519) | noise: the tree is just above its band, the regression isn't |
| Random numbers (control) | 0.480 (0.540) | 0.492 (0.530) | noise |

All together, adjusted odds ratios with 95% intervals:

- Age per 10 years: 1.59 (1.44 to 1.76).
- Male: 1.24 (0.91 to 1.69). Surgery in the past year: 0.89 (0.53 to 1.49).
- Imd quintiles 2, 3, 4 and 5 against quintile 1 (most deprived): 0.69, 0.60 (0.36 to 0.97), 0.92
  and 0.90.
- Asian, Black, Mixed and Other against White: 0.82, 0.79, 0.63 (0.38 to 1.04) and 0.78.

The odds ratios come from an exact fit (tolerance 1e-10). Scikit-learn's default tolerance stops
early enough to move three of them by 0.01.

Random forest, drop in test AUC when a column is shuffled (mean ± sd over 50 shuffles): age
0.202 ± 0.033, imd 0.004 ± 0.008, ethnicity 0.002 ± 0.006, random numbers (continuous) 0.001 ± 0.007,
sex 0.001 ± 0.005, random numbers (5 levels) −0.003 ± 0.004, surgery −0.005 ± 0.008.

## Reasoning: risk factor or noise

- **Age is a real risk factor by every test.** Its AUC of 0.71 is well above the 0.54 that 95% of its
  shuffled copies stay below. The interval on its adjusted odds ratio, 1.44 to 1.76, is nowhere near 1. In
  the forest it carries all the importance: a 0.20 drop in AUC against 0.004 or less for every other
  column. Resistance is 8.4% at ages 20 to 40 and 40.7% at 71 to 79, and each decade of age
  multiplies the odds of resistance by about 1.6.
- **Everything else is noise in this data.** Every other factor fails at least one of the two tests
  on its own, and in the forest each sits level with the columns of random numbers.
- **Two near-misses, and why they don't count.** The ICD-chapter tree scored 0.524 against a band top
  of 0.519, but the regression on the same factor didn't, and grouping 964 codes that look random
  into 26 letters is just where a lucky split turns up. The seven non-age rows give 14 scores, each
  with a 1-in-20 chance of clearing its band by luck, so one doing so is unsurprising (about 0.7
  expected). Requiring both models to clear the band guards against exactly this. In the adjusted
  regression, imd quintile 3's interval (0.36 to 0.97) ends just under 1. The 10 non-age intervals
  each have the same 1-in-20 chance, and there's no gradient: quintiles 2 to 5 give 0.69, 0.60, 0.92
  and 0.90. A real deprivation effect would rise or fall steadily across the quintiles.
- **Not established isn't the same as ruled out.** Male sex has an odds ratio of 1.24 with an
  interval of 0.91 to 1.69, which includes 1. With 1000 patients we can't rule out a modest effect
  of sex, or of the other factors; we can only say this data shows none.
- **The forest's 0.09 for deprivation in `feature_importance_age_imd.png` is not evidence.** That
  chart uses impurity-based importance, which favours columns with many distinct values. In our
  noise-check forest (`outputs/risk_factors_forest_importance.csv`), a continuous column of random
  numbers scores 0.16 on that measure, more than imd's 0.07. The five-level noise column scores 0.05,
  so imd is only a little above noise of its own shape. Permutation importance on held-out patients
  doesn't have that bias, and there imd (0.004 ± 0.008) sits level with the noise columns (0.001 and
  −0.003).

## What it means for the model and the video

- All the signal is in age, so a tree that splits on age is the right shape of model. Depth beyond 2
  or 3 can only fit noise, which matches the overfitting curve. The two imd splits in our depth-3 tree
  change no prediction: both leaves under each one predict the same class.
- Video: Q6 now says who is at risk, with the figures, and that no other factor beat random noise
  (screen: `outputs/risk_factors_vs_noise.png`). Q7 gives the odds ratio (screen:
  `outputs/risk_factors_adjusted_odds_ratios.png`). The outro says age is the only clear risk factor.

## Caveats

- The data is synthetic, so these are the patterns its generator put in, not necessarily those in
  real UKHSA data.
- 1000 patients give limited power for small effects, as with sex above.
- Wald intervals and permutation p-values are approximations. With 100 shuffled copies the smallest
  possible p-value is 0.01. Raise `--permutations` for finer ones.
