# Thu 29 Oct: checks behind Q4, Q6 and Q7 (guide C, steps 2 and 4 to 6)

Run on a laptop (Python 3.12.10, scikit-learn 1.9.1, pandas 3.0.6) on the data file from the brief's
link (94,198 bytes, the same size as the VM copy). The data stays out of the repo.

## The script reproduces

`python src/amr_trees.py --out <scratch folder>` gave exactly the committed numbers in `outputs/`:
`model_comparison.csv` and every tree `.txt` match apart from Windows line endings, and
`run_summary_age_imd.txt` matches apart from its version line. It took 60 s on the laptop. After the
docstrings were added the same day, a rerun was byte-identical.

## Data facts (step 2): all match notes/2026-10-25-data-first-look.md

- 1000 rows, no missing values, 24.1% resistant, ages 20 to 79.
- Ethnicity: Black 21.1%, Other 20.9%, Asian 20.7%, Mixed 19.7%, White 17.6%.
- Resistance by age: 8.4% at 20 to 40 (335 patients), 25.9% at 41 to 60 (352), 37.5% at 61 to 70
  (168), 40.7% at 71 to 79 (145).
- Resistance by imd quintile 1 to 5: 26.4%, 20.7%, 20.0%, 28.9%, 24.6%. No trend.
- The file also holds date of birth, specimen date, NHS trust code and diagnosis code. In real data
  those could identify a patient even without a name. That's another reason for synthetic data (Q5)
  and for locking the file down (Q3).

## Robustness to the random split (step 6)

`--seed` changes the train/test split, the cross-validation folds and the models' own randomness.

| Seed | Best single tree (CV balanced accuracy) | Best model overall | Age importance |
|---|---|---|---|
| 42 | balanced, depth 3 (0.659) | random forest, depth 3 (0.670) | 0.91 |
| 1 | balanced, depth 3 (0.653) | random forest, depth 3 (0.664) | 0.93 |
| 7 | balanced, depth 2 (0.638) | random forest, depth 4 (0.655) | 0.92 |
| 2026 | balanced, depth 1 (0.684) | random forest, depth 3 (0.693) | 0.94 |

Reading:

- The class-balanced tree is always the best single tree, and the random forest always the best
  model overall.
- Age carries more than 90% of the importance every time.
- The best tree depth moves between 1 and 3. In every seed, depths 1 to 5 all sit within one fold
  standard deviation of the best, so shallow trees are effectively tied, as the comment under Q6
  notes for depth 1.
- The trend is still clear: scores drift down as trees get deeper, and depth 8 is the worst
  class-balanced tree for every seed. (Plain, unweighted trees of depth 1 score 0.500 in every seed,
  because they call everyone susceptible.)

## Do the extra columns help? (step 4)

With `--features age imd sex_male had_surgery_past_yr` the best single tree is the balanced depth-1
tree, at CV balanced accuracy 0.655, slightly below the 0.659 of the best tree on age and imd alone.
The random forest moves from 0.670 to 0.673. Importance: age 0.83, imd 0.09, sex_male 0.05, had_surgery_past_yr 0.02. The extra
columns add almost nothing, so the final model keeps age and imd, the columns the brief asks about.

## Logistic regression baseline (step 5)

Same split and 5-fold cross-validation as the script (seed 42). Logistic regression with
`class_weight="balanced"` on age and imd. The tree and forest rows come from
`outputs/model_comparison.csv`.

| Model | CV balanced accuracy | CV ROC AUC | Test balanced accuracy | Test recall | Test ROC AUC |
|---|---|---|---|---|---|
| Logistic regression | 0.660 ± 0.036 | 0.696 ± 0.027 | 0.646 | 0.633 | 0.718 |
| Balanced tree, depth 3 | 0.659 ± 0.032 | 0.675 ± 0.031 | 0.622 | 0.650 | 0.685 |
| Random forest, depth 3 | 0.670 ± 0.024 | 0.692 ± 0.018 | 0.675 | 0.733 | 0.718 |

Fitted without class weights on the training set, logistic regression gives an odds ratio of 1.54 per
10 years of age and 1.07 per imd quintile. A straight line in age does as well as our tree, which
guide C said would be worth saying, so Q7 now does.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

df = pd.read_csv("data/dig_health_hub_amr.csv", index_col=0)
X_tr, X_te, y_tr, y_te = train_test_split(df[["age", "imd"]], df["coamox"], test_size=0.25,
                                          stratify=df["coamox"], random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
lr = LogisticRegression(class_weight="balanced", max_iter=1000)
s = cross_validate(lr, X_tr, y_tr, cv=cv, scoring=["balanced_accuracy", "roc_auc"])
print(s["test_balanced_accuracy"].mean(), s["test_roc_auc"].mean())            # 0.660, 0.696
p = lr.fit(X_tr, y_tr).predict_proba(X_te)[:, 1]
print(roc_auc_score(y_te, p), balanced_accuracy_score(y_te, p >= 0.5), recall_score(y_te, p >= 0.5))
odds = LogisticRegression(C=float("inf"), max_iter=1000).fit(X_tr, y_tr)        # no class weights
print(np.exp(10 * odds.coef_[0][0]), np.exp(odds.coef_[0][1]))                  # 1.54 per decade, 1.07 per quintile
```
