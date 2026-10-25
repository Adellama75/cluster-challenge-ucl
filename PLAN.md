# CIUK Cluster Challenge 2026: UCL subchallenge

Team plan, Mon 26 to Fri 30 October 2026. Brief: `UCL_Challenge_Updated.pdf` (team folder).

Team: UCLuster Too · Repo: https://github.com/adellama75/cluster-challenge-ucl

## At a glance

- **Task:** a Python script that trains decision-tree models on synthetic E. coli antimicrobial
  resistance data (`coamox` = resistant to co-amoxiclav, `age`, `imd` deprivation quintile) and runs on
  UCL's cloud VM, **Condenser**. Questions: which tree best identifies people at risk, and what are the
  main risk factors? Based on the Carpentries lesson *Introduction to Tree Models in Python*.
- **Dates:** login details go to the team captain on **Mon 26 Oct**. Deadline **Fri 30 Oct, 23:59**.
- **Marked:** the contents of our VM plus a **5-minute MP4 video** in the team's CIUK Challenge folder.
- **VM limits:** AlmaLinux, no root (so no graphviz), only vim installed (add `micro` via curl),
  files arrive via `curl`.

## 1 Where the marks are

| Marked item | Pts | Owner | What we do |
|---|---|---|---|
| Accessed Condenser | 5 | A | Log in on Monday. This also weights the whole technical mark, so it comes first. |
| Python environment | 5 | A | `python3 -m venv`, only the packages we import, pinned in `requirements.txt`. |
| ReadMe | 10 | A | How the env was made, how to get in, how to run. Tested from a fresh clone. |
| Python script | 20 | B | One well-structured, commented script: load, fit, compare, save figures and a results table. |
| File permissions and storage | 10 | A | Outputs in `outputs/` with meaningful names; data file no longer world-readable. |
| Cloud compute and security (video) | 10 | D | Q1 to Q3. |
| Data and machine learning (video) | 10 | C | Q4 and Q5: representative data, synthetic data, bias, data protection. |
| Technical solution and alternatives (video) | 10 | B + C | Q6 and Q7: who is at risk, best tree and why, other models. |
| Video quality | 5 | D | Exactly 5 min, MP4, clear audio, readable screens. |
| Team work | 15 | Everyone | Q8, shown in the video. `video/teamwork-log.md` collects the evidence as we go. |

Half the technical marks (25 of 50) are environment, ReadMe and file hygiene, not modelling. Those are
cheap if done carefully, so A owns them full-time.

## 2 Who does what

| Person | Build week (Mon to Thu) | Video |
|---|---|---|
| **A: VM and environment lead, editor** | Logs in Monday. Sets up micro, the venv, the folder layout and file permissions on the VM. Owns `README.md` and `requirements.txt`. Deploys B's script and runs it on Condenser. Does a fresh-clone test on Thursday. | Q3 (permissions: what we found, what we changed and why). Final check of the VM before the deadline. |
| **B: model and script lead** | Owns `src/`. Loads the data, fits trees of different types and depths, compares them on held-out data, saves tree diagrams (`plot_tree`, no graphviz) and a decision-surface plot, and writes a comparison table to `outputs/`. | Q6 (final model and why), with screens of the outputs. |
| **C: data and evaluation lead** | Explores the data locally (class balance, age and imd distributions, missing values). Chooses metrics that suit an imbalanced outcome (recall on the resistant class, ROC AUC, not only accuracy). Prototypes alternatives (logistic regression, random forest, gradient boosting) to compare against the trees. | Q4, Q5, Q7 (representative and synthetic data, bias, other techniques). |
| **D: video lead** | Owns `video/script.md`, the storyboard and the recording plan. Researches cloud computing and security basics. | Q1, Q2, Q8, and the edit: intro, transitions, timing to 5:00, MP4 export, upload. |

**Step-by-step guides per role:** `guides/A-vm-environment.md`, `guides/B-model-script.md`,
`guides/C-data-evaluation.md`, `guides/D-video.md`. Ada is A.

**Pairs for cover:** A↔B (VM and script) and C↔D (analysis and video).

**After every work session:** run `/script` in Claude Code (see `.claude/skills/script/`). It turns
what you just did into draft video narration under the right question, and logs teamwork evidence.

**Syncs:** 15 minutes at 18:00 Mon to Thu.

## 3 Day by day

**Mon 26: access and data**
- A: log in as soon as details arrive. Install micro, create the venv, `curl` the data file, record
  `ls -l` of the data file *before* changing anything (needed for Q3), then fix permissions.
- B and C: download the data locally and prototype in a notebook or script. C does the data exploration.
- D: script skeleton, cloud and security research, agree the recording tool (Panopto, Teams or Clipchamp).

**Tue 27: first full run on Condenser**
- B: script v1 runs end to end on the VM and writes to `outputs/`.
- C: metrics and baselines; first comparison of tree types and depths.
- A: README v1, `requirements.txt` pinned to what the VM actually has.

**Wed 28: choose the model**
- B and C agree the final tree with numbers to back it up, and the main risk factors.
- Freeze the script by 18:00. Only fixes after this.
- D: storyboard with a time budget per question; everyone drafts their lines (or runs `/script`).

**Thu 29: record**
- Everyone records their segments. Show screens at a readable size.
- A: fresh-clone test of the README on the VM, final permissions and file-name check.

**Fri 30: finish and submit**
- D: edit to exactly 5:00, export MP4, upload to the team CIUK Challenge folder by 18:00.
- A: last check that the VM has README, script, data file and `outputs/`, by 18:00.
- Deadline 23:59. Everything done by 18:00 leaves room for problems.

## 4 Video plan (5:00, about 700 words at 140 words per minute)

| Segment | Questions | Marks | Time |
|---|---|---|---|
| Intro: team name, members, task | | | 0:15 |
| Cloud and security | Q1, Q2 | 10 | 0:55 |
| File permissions | Q3 | (part of cloud/security) | 0:30 |
| Data | Q4, Q5 | 10 | 0:55 |
| Model and alternatives | Q6, Q7 | 10 | 1:10 |
| Team work | Q8 | 15 | 1:00 |
| Outro | | | 0:15 |

The questions: (1) What is cloud compute? (2) Key data security considerations for cloud computing?
(3) The data file was world-readable: why is that bad, did we change it, how and why? (4) Why a
representative data set? (5) Why synthetic instead of real patient data? (6) Our final tree model and why
it's best. (7) Other modelling techniques and why. (8) How we worked as a team.

## 5 Technical notes

- No graphviz on the VM: draw trees with `sklearn.tree.plot_tree` (matplotlib) and also save
  `export_text` output. Use the `Agg` matplotlib backend, since there's no display.
- Fix `random_state` everywhere so runs are reproducible.
- Packages: pandas, scikit-learn, matplotlib. Nothing else unless the script imports it.
- The data file is synthetic but we still treat it as patient data: not committed to this public repo,
  fetched with `curl` (command in the README), and not world-readable on the VM.
- Never commit Condenser login details, IPs or keys. The repo is public.

## 6 Later: the final presentation

The final 5-minute presentation probably covers all three challenges. Week 1 (EPCC, HPL/HPCG on Cirrus)
needs reconstructing: what we ran, what we found, what we'd do differently. Keep notes on Durham and UCL
as we go so we don't have to do that again.
