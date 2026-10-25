# Role C: data and evaluation lead

You make sure we choose the model for the right reasons and can explain the data. You share the
technical-solution segment with B, and own the data-and-ML video segment (10 marks).
Video: Q4 (representative data), Q5 (synthetic data), Q7 (other techniques).

Run `/script` after each session, with a line of notes.

## Day 1: know the data

1. **Set up locally** exactly as in B's guide steps 1 and 2.
2. **Explore** (paste into `python` inside the venv):
   ```python
   import pandas as pd
   d = pd.read_csv("data/dig_health_hub_amr.csv", index_col=0)
   print(d.shape, d.isna().sum().sum())                  # rows, columns; missing values
   print(d.coamox.value_counts(normalize=True))          # class balance
   print(d.groupby("imd").coamox.mean())                 # resistance by deprivation quintile
   print(d.groupby(pd.cut(d.age, [0, 40, 60, 70, 80])).coamox.agg(["mean", "size"]))
   print(d.ethnicity.value_counts(normalize=True))
   ```
3. **Interpret:**
   - About 24% resistant: an **imbalanced** outcome. Accuracy alone misleads (76% for "nobody is
     resistant"), which is why the script ranks models on balanced accuracy and reports recall.
   - Resistance rises steeply with **age** (roughly 8% at 20–40 to about 40% at 70+). With **imd** there is no
     clear trend. Check these numbers yourself and put them in `notes/`.
   - Look at who is in the data: age range (20–79, so no children), ethnicity mix, sex. Anyone missing
     or rare is someone the model knows little about. That's the core of Q4.

## Days 2 to 3: evaluate and compare

4. **Do more columns help?** Run with the extra numeric columns and compare `run_summary` files:
   ```bash
   python src/amr_trees.py --features age imd sex_male had_surgery_past_yr --out outputs
   ```
   *Interpret:* if CV balanced accuracy barely moves, the extra columns add little and the simpler model
   is better. Decide with B whether the final model uses them (the brief asks about age and imd).
5. **Alternative techniques for Q7.** Try one non-tree baseline, for example logistic regression with
   `class_weight="balanced"`, using the same split and metrics. If a straight line in age does as well as
   a tree, that's worth saying. Other techniques to discuss even if not run: logistic regression
   (interpretable odds ratios), k-nearest neighbours, gradient-boosted trees with tuned learning rates,
   and survival or time-trend models if dates (`spec_date`) are used.
6. **Robustness:** rerun with two or three different `--seed` values. If the best model changes, the
   models are effectively tied: prefer the simplest.

## Video: Q4, Q5, Q7 (about 130 words in total)

- **Q4, representative data:** a model only learns the population it sees. If groups are missing or rare
  (by age, ethnicity, deprivation, region), predictions for them are worse and can bake in unfair
  differences (algorithmic bias). Use our data's actual make-up as the example.
- **Q5, synthetic data:** real patient records are personal health data (UK GDPR special category).
  Synthetic data mimics the statistical patterns without being real people, so it can be shared and
  used for training and teaching with far less privacy risk, though it may miss rare real patterns.
- **Q7:** the alternatives from step 5 and why you'd pick each.
