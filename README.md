# CIUK 2026 UCL challenge: antimicrobial resistance tree models

Team **UCLuster Too** (Ada Ge, Bobby Ta, Eric Huang, James Loke). A Python script that trains
decision-tree models to identify patients whose E. coli infections resist co-amoxiclav, from age and
deprivation (IMD), and runs on UCL's Condenser cloud platform.

## Quick start on Condenser

Already set up on our VM. To rerun it:

```bash
cd ~/cluster-challenge-ucl            # [Mon: confirm path]
source .venv/bin/activate
python src/amr_trees.py               # about 20 seconds; results in outputs/
cat outputs/run_summary_age_imd.txt   # best tree, best model, main risk factors
```

From scratch on a new machine (Python 3 and internet access needed; no root):

```bash
git clone https://github.com/adellama75/cluster-challenge-ucl.git && cd cluster-challenge-ucl
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
mkdir -p data && curl -L -o data/dig_health_hub_amr.csv \
  "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
chmod 600 data/dig_health_hub_amr.csv
python src/amr_trees.py
```

## Layout

| Path | What |
|---|---|
| `src/amr_trees.py` | The analysis script |
| `requirements.txt` | The Python packages it needs, pinned to the versions on our VM |
| `data/` | The data file `dig_health_hub_amr.csv` (on the VM only; not in the public repo) |
| `outputs/` | Tree diagrams, decision-surface plots and the model comparison table, written by the script |
| `notes/` | Working notes, including the data file's permissions before and after we changed them |
| `video/` | Our video script and teamwork log |
| `PLAN.md`, `guides/` | Team plan and role guides |

## 1 How the environment was created

On the Condenser VM (AlmaLinux, no root access), as our own user:

```bash
python3 --version                     # [Mon: version]
python3 -m venv .venv                 # isolated environment inside the project folder
source .venv/bin/activate
pip install --upgrade pip
pip install pandas scikit-learn matplotlib
pip freeze | grep -iE '^(pandas|scikit-learn|matplotlib)==' > requirements.txt
```

Only the three packages the script imports are installed (numpy and the other dependencies come with
them), and `requirements.txt` pins the exact versions, so `pip install -r requirements.txt` rebuilds
the same environment. Graphviz is not installed (it needs root), so the script draws trees with
matplotlib instead.

We also installed the `micro` text editor into `~/bin` (the VM only has vim):

```bash
mkdir -p ~/bin && cd ~/bin && curl https://getmic.ro | bash && cd ~
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
```

## 2 Accessing the environment

1. Log in to Condenser with the account details from the Condenser welcome email.
   [Mon: web interface or SSH, and the exact steps]
2. Connect to our team server, using the details from the ARC Education email.
   [Mon: how]
3. The project is in `~/cluster-challenge-ucl` [Mon: confirm]. Run `source .venv/bin/activate` before
   using Python.

No passwords, keys or addresses are stored in this repository.

## 3 Getting the data

```bash
mkdir -p data
curl -L -o data/dig_health_hub_amr.csv \
  "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
chmod 600 data/dig_health_hub_amr.csv
```

The file is downloaded readable by every user on the machine. It holds patient-style health records
(synthetic, but treated as real), so `chmod 600` makes it readable and writable by our account only.
Before and after: `notes/permissions-before.txt`, `notes/permissions-after.txt`.

## 4 Running the script

```bash
source .venv/bin/activate
python src/amr_trees.py --data data/dig_health_hub_amr.csv --out outputs
```

Takes about 20 seconds. It fits decision trees (plain and class-balanced), bagging, random forests and
gradient boosting at depths 1 to 8, picks the best by 5-fold cross-validated balanced accuracy, and writes
to `outputs/`:

| File | What |
|---|---|
| `model_comparison.csv` | Every model and depth, with cross-validation and test-set metrics, best first |
| `run_summary_age_imd.txt` | Best single tree, best model overall, risk factors, package versions |
| `best_tree_age_imd.png` | The best single decision tree |
| `tree_balanced_depth{1-4}_age_imd.png`, `..._depth{1-8}_age_imd.txt` | Tree diagrams by depth (text for all depths) |
| `decision_surface_*_age_imd.png` | Predicted risk over age and deprivation |
| `balanced_accuracy_vs_depth_age_imd.png` | Model quality vs depth (shows overfitting) |
| `feature_importance_age_imd.png` | Main risk factors |

Options: `--features age imd sex_male had_surgery_past_yr` adds columns, `--max-depth`, `--test-size`,
`--seed` (default 42, for reproducible results). Output files are created without read access for other
users.
