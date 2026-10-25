# CIUK 2026 UCL challenge: antimicrobial resistance tree models

Team **UCLuster Too**. Decision-tree models for co-amoxiclav resistance in E. coli, run on UCL's Condenser
cloud platform. Team plan: [PLAN.md](PLAN.md). Step-by-step guides per role: [guides/](guides/).

> This README is the submitted ReadMe and will be completed during the week (owner: A).

## Layout

| Path | What |
|---|---|
| `src/` | The Python script |
| `outputs/` | Tree diagrams, decision-surface plots and the model comparison table, written by the script |
| `data/` | The data file (not committed; fetched with curl) |
| `video/` | Video script and teamwork log |
| `notes/` | Session notes |

## Video script workflow (team only)

After each work session, run `/script` in Claude Code started **inside this repo**, optionally with notes:
`/script got the venv working; the first numpy wheel failed so we pinned an older one`. It drafts
narration for the matching video question in `video/script.md` (numbers only from repo files or your
notes, `[TODO]` otherwise), keeps each segment within its time budget, adds a teamwork entry to
`video/teamwork-log.md`, and commits locally. Then push. Mark finished lines `<!-- locked -->` to keep them.
Not using Claude Code? Paste `.claude/skills/script/SKILL.md` into your assistant along with your notes.

## 1 How the environment was created

TODO(A): exact commands run on the VM, Python version, `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2 Accessing the environment

TODO(A): how a marker reaches the VM and where the files are. No credentials in this file.

## 3 Getting the data

```bash
mkdir -p data
curl -L -o data/dig_health_hub_amr.csv \
  "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
chmod 600 data/dig_health_hub_amr.csv   # TODO(A): final permission choice and why
```

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
`--seed` (default 42, for reproducible results). Output files are created without world read access.
