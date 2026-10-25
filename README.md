# CIUK 2026 UCL challenge: antimicrobial resistance tree models

Team **UCLuster Too**. Decision-tree models for co-amoxiclav resistance in E. coli, run on UCL's Condenser
cloud platform. Team plan: [PLAN.md](PLAN.md).

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

TODO(B): command, runtime, and what appears in `outputs/`.
