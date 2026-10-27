# CIUK 2026 UCL challenge: antimicrobial resistance tree models

Team **UCLuster Too** (Ada Ge, Bobby Ta, Eric Huang, James Loke). A Python script that trains
decision-tree models to identify patients whose E. coli infections resist co-amoxiclav, from age and
deprivation (IMD), and runs on UCL's Condenser cloud platform.

## Quick start on Condenser

Already set up on our VM. To rerun it:

```bash
cd ~/cluster-challenge-ucl
source .venv/bin/activate
python src/amr_trees.py               # about 35 seconds on the VM; results in outputs/
cat outputs/run_summary_age_imd.txt   # best tree, best model, main risk factors
```

From scratch on a new machine (Python 3 and internet access needed; no root). Condenser has no git,
so the code comes down from GitHub as a tarball:

```bash
curl -L -o repo.tar.gz https://github.com/adellama75/cluster-challenge-ucl/archive/refs/heads/main.tar.gz
tar xzf repo.tar.gz && mv cluster-challenge-ucl-main cluster-challenge-ucl && rm repo.tar.gz
cd cluster-challenge-ucl
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
mkdir -p data && chmod 700 data && curl -L -o data/dig_health_hub_amr.csv \
  "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
chmod 600 data/dig_health_hub_amr.csv
python src/amr_trees.py
```

(Where git is available, `git clone https://github.com/adellama75/cluster-challenge-ucl.git` replaces
the first three lines.)

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
python3 --version                     # Python 3.12.13 on our VM
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

The VM has no git and no text editor, and without root we can't install them. So GitHub is the single
source of truth: we edit on our laptops, push, and fetch changed files onto the VM with `curl` from
GitHub's raw URLs. The VM copy is never edited directly. For example:

```bash
cd ~/cluster-challenge-ucl
curl -sL -o src/amr_trees.py https://raw.githubusercontent.com/adellama75/cluster-challenge-ucl/main/src/amr_trees.py
head -3 src/amr_trees.py              # check: Python code, not "404: Not Found"
```

## 2 Accessing the environment

Our server is only reachable from inside Condenser's web interface (a JupyterHub); there is no direct
SSH from outside.

1. Open https://cluster-challenge.arc.ucl.ac.uk, choose **Sign in with AWS Cognito**, and sign in with
   the username and temporary password from the Condenser welcome email (you set a new password the
   first time).
2. Choose **CPU Server** and **Start**. JupyterLab opens after a short wait.
3. Open a terminal (**File > New > Terminal**). The first time, save the team's private SSH key from the
   ARC Education email into `~/.ssh/id_ed25519`, then restrict it (repeat the `chmod` if the JupyterHub
   container restarts):
   ```bash
   mkdir -p ~/.ssh && chmod 700 ~/.ssh
   # paste the key into ~/.ssh/id_ed25519 with the JupyterLab text editor
   chmod 600 ~/.ssh/id_ed25519
   ```
4. Connect to the team server as user `cc`, with the IP address from the ARC Education email:
   ```bash
   ssh cc@<server IP>
   ```
5. The project is in `~/cluster-challenge-ucl`. Run `source .venv/bin/activate` before using Python.

No passwords, keys or addresses are stored in this repository.

## 3 Getting the data

```bash
mkdir -p data && chmod 700 data
curl -L -o data/dig_health_hub_amr.csv \
  "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
chmod 600 data/dig_health_hub_amr.csv
```

The file is downloaded readable by every user on the machine (`-rw-r--r--`). It holds patient-style
health records (synthetic, but treated as real), so `chmod 600` makes it readable and writable by our
account only (`-rw-------`), and `chmod 700` stops other users even listing the `data/` folder.
Before and after: `notes/permissions-before.txt`, `notes/permissions-after.txt`.

## 4 Running the script

```bash
source .venv/bin/activate
python src/amr_trees.py --data data/dig_health_hub_amr.csv --out outputs
```

Takes about 35 seconds on the VM. It fits decision trees (plain and class-balanced), bagging, random forests and
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
`--seed` (default 42, for reproducible results). The script sets `umask 027`, but `outputs/` comes with the
download and overwriting a file keeps its old permissions, so lock it down after a run:
`chmod 750 outputs && chmod 640 outputs/*`.

## 5 Getting results off the VM

There's no git on the VM to push with, and the JupyterLab file browser shows the JupyterHub container,
not the server. So results come off in two hops. In the JupyterLab terminal, **not** inside `ssh`:

```bash
ssh cc@<server IP> 'cd ~/cluster-challenge-ucl && tar czf - outputs' > ~/outputs.tar.gz
```

Then right-click `outputs.tar.gz` in the JupyterLab file browser and choose **Download**.
