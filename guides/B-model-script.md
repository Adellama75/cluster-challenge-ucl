# Role B: model and script lead

You own `src/amr_trees.py` (20 marks for the script, plus the technical-solution video segment, 10).
A first working draft is already there: your job is to understand it, improve it, and own the final
model choice with C. Video: Q6, the final model and why.

Run `/script` after each session, with a line of notes.

## Day 1: run it and understand it

1. **Set up locally** (any laptop or PC; Condenser is only needed for the final run):
   ```bash
   git clone https://github.com/adellama75/cluster-challenge-ucl.git && cd cluster-challenge-ucl
   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   mkdir -p data && curl -L -o data/dig_health_hub_amr.csv "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
   ```
2. **Run it:** `python src/amr_trees.py` (about 20 s). It writes to `outputs/`.
3. **Read `outputs/run_summary_age_imd.txt` first.** It names the best single tree, the best model
   overall and the feature importances.
4. **Read the code top to bottom.** It's one file: `load_data` → `candidate_models` → `evaluate` →
   figures → summary. Every model type is in `candidate_models`.

## How to interpret the outputs

- **`model_comparison.csv`**: one row per model type and depth, sorted best first.
  - `cv_balanced_accuracy_mean`: what we choose on. It's measured by 5-fold cross-validation on the
    training data only, so the test set stays untouched. It averages the hit rate on resistant and on
    susceptible patients. **0.5 means no better than calling everyone susceptible.**
  - `test_recall_resistant`: of the truly resistant patients in the test set, the fraction the model
    flags. This is "does it identify those at risk". A model with high accuracy but recall near 0 is
    useless here: about 76% of patients are susceptible, so "everyone is fine" gets 76% accuracy.
  - `test_precision_resistant`: of the patients flagged, the fraction truly resistant. Low precision
    means many false alarms.
  - `test_roc_auc`: how well the model *ranks* patients by risk, independent of the cut-off. 0.5 is
    random, 1.0 is perfect.
  - `*_std`: spread across the 5 folds. If two models differ by less than this, treat them as tied and
    prefer the simpler (shallower, single tree) one.
- **`balanced_accuracy_vs_depth_*.png`**: watch the lines **fall** as depth grows.
  That's overfitting: deep trees memorise the training data.
- **`best_tree_*.png`**: read it from the top. Each box shows the split rule, the share of patients
  reaching it, and the class proportions. The first split is the strongest risk factor.
- **`decision_surface_*.png`**: red = predicted resistant, blue = susceptible, over age × imd. If the
  colour changes left to right but hardly bottom to top, age matters and deprivation doesn't.
- **`feature_importance_*.png`**: the main risk factors, as shares of the total importance.

## Days 2 to 3: improve and decide

5. **Things worth trying** (one change at a time; rerun; compare the CSV):
   - `--max-depth 12` to show overfitting more clearly.
   - Pruning by cost complexity (`ccp_alpha`) as another tree type, as in the Carpentries lesson.
   - A different `--seed` to check the winner doesn't change by chance.
6. **Agree the final model with C by Wednesday 18:00.** Criteria: best CV balanced accuracy, within the
   std of the best → choose the simplest. A single tree you can explain on screen may beat a forest that
   is 0.01 better.
7. **Code quality** (part of the 20 marks): every function has a docstring saying *why*, no dead code,
   no hard-coded paths outside `parse_args`. Freeze the script at Wednesday 18:00; only fixes after that.

## Video: Q6 (about 80 words), with screens of the outputs

Who is more at risk (older patients; say where the tree splits), which model we chose and the numbers
behind it (from `run_summary`), and why the depth we picked (the overfitting curve).
