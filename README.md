# CIUK 2026 UCL challenge: antimicrobial resistance tree models

Team **UCLuster Too** (Ada Ge, Bobby Ta, Eric Huang, James Loke). `src/amr_trees.py` trains tree models
to predict which patients' E. coli infections resist co-amoxiclav, from age and deprivation (IMD).
`src/risk_factors.py` tests every patient factor in the data against noise to find the real risk
factors. Both run on UCL's Condenser cloud platform.

## Quick start (on our VM)

```bash
cd ~/cluster-challenge-ucl
source .venv/bin/activate
python src/amr_trees.py                 # about 35 seconds; results in outputs/
cat outputs/run_summary_age_imd.txt     # best tree, best model, feature importance
python src/risk_factors.py              # up to about 2 minutes
cat outputs/risk_factors_summary.txt    # which factors beat noise, odds ratios
```

## 1 Accessing the environment

The server is only reachable from Condenser's JupyterHub; there is no SSH from outside.

1. Go to https://cluster-challenge.arc.ucl.ac.uk, choose **Sign in with AWS Cognito**, and log in with
   the details from the Condenser welcome email.
2. Choose **CPU Server**, then **Start**. In JupyterLab, open **File > New > Terminal**.
3. First time only: save the team's private key from the ARC Education email and restrict it:
   ```bash
   mkdir -p ~/.ssh && chmod 700 ~/.ssh
   # paste the key into ~/.ssh/id_ed25519 with the JupyterLab editor, then:
   chmod 600 ~/.ssh/id_ed25519
   ```
4. Connect with `ssh cc@<server IP>` (IP from the same email). The project is in `~/cluster-challenge-ucl`.

No passwords, keys or IP addresses are stored in this repository.

## 2 How the environment was created

On the VM (AlmaLinux, Python 3.12.13, no root):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pandas scikit-learn matplotlib
pip freeze | grep -iE '^(pandas|scikit-learn|matplotlib)==' > requirements.txt
```

Only the three packages the scripts import are installed, pinned in `requirements.txt`. Graphviz needs
root, so trees are drawn with matplotlib instead.

**From scratch** on a new machine (the VM has no git, so the code comes as a tarball):

```bash
curl -L https://github.com/adellama75/cluster-challenge-ucl/archive/refs/heads/main.tar.gz | tar xz
mv cluster-challenge-ucl-main cluster-challenge-ucl && cd cluster-challenge-ucl
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## 3 Getting the data and securing it

```bash
mkdir -p data && chmod 700 data
curl -L -o data/dig_health_hub_amr.csv \
  "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
chmod 600 data/dig_health_hub_amr.csv
```

The file downloads readable by every user (`-rw-r--r--`). It holds patient-style records, so
`chmod 600` limits it to our account (`-rw-------`) and `chmod 700` stops others listing `data/`.

## 4 Running the scripts

```bash
source .venv/bin/activate
python src/amr_trees.py --data data/dig_health_hub_amr.csv --out outputs
python src/risk_factors.py --data data/dig_health_hub_amr.csv --out outputs
chmod 750 outputs && chmod 640 outputs/*
```

`amr_trees.py` fits decision trees (plain and class-balanced), bagging, random forests and gradient
boosting at depths 1 to 8, and ranks them by 5-fold cross-validated balanced accuracy (resistant cases
are only 24%, so plain accuracy would reward predicting "susceptible" for everyone). Options:
`--features` (add `sex_male had_surgery_past_yr`), `--max-depth`, `--test-size`, `--seed` (default 42).

`risk_factors.py` scores each patient factor on its own (age, sex, recent surgery, deprivation,
ethnicity, NHS trust, diagnosis chapter, and a column of random numbers as a control) with a logistic
regression and a small tree, and compares the score with shuffled copies of that factor. It then fits
the factors together, as adjusted odds ratios and as a random forest that also gets two noise columns.
Options: `--permutations` (shuffled copies per factor, default 100), `--seed` (default 42).

Outputs in `outputs/`:

| File | What |
|---|---|
| `model_comparison.csv` | Every model and depth with cross-validation and test metrics, best first |
| `run_summary_age_imd.txt` | Best single tree, best model overall, risk factors, package versions |
| `best_tree_age_imd.png` | The best single decision tree |
| `tree_balanced_depth*_age_imd.png` / `.txt` | Tree diagrams for depths 1–4, text for all depths |
| `decision_surface_*_age_imd.png` | Predicted risk across age and deprivation |
| `balanced_accuracy_vs_depth_age_imd.png` | Model quality vs depth |
| `feature_importance_age_imd.png` | Feature importance in the best model |
| `risk_factors_summary.txt` | Which factors beat noise, odds ratios, forest importance, package versions |
| `risk_factors_one_at_a_time.csv` | Each factor alone: cross-validated ROC AUC of a regression and a tree, noise band, verdict |
| `risk_factors_vs_noise.png` | Each factor's score against its noise band, and the forest's importances |
| `risk_factors_adjusted_odds_ratios.csv` / `.png` | Age, sex, surgery, deprivation and ethnicity together: odds ratios with 95% intervals |
| `risk_factors_forest_importance.csv` | Random forest permutation importance next to two noise columns |

## 5 Updating code and retrieving results

We edit on our laptops and push to GitHub; the VM copy is never edited directly. To update a file:

```bash
curl -sL -o src/amr_trees.py \
  https://raw.githubusercontent.com/adellama75/cluster-challenge-ucl/main/src/amr_trees.py
```

To download results, run this in the JupyterLab terminal (not inside `ssh`), then right-click
`outputs.tar.gz` in the file browser and choose **Download**:

```bash
ssh cc@<server IP> 'cd ~/cluster-challenge-ucl && tar czf - outputs' > ~/outputs.tar.gz
```
