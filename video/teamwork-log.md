# Teamwork log

One entry per work session, added by `/script`. Evidence for the teamwork marks (15).

## 2026-10-25 21:45 · Ada Ge (A)
- Did: created the public repo and invited the team; wrote the A–D plan, per-role step-by-step guides
  and the `/script` workflow; drafted the analysis script and ran a first look at the data.
- Problem: the first model selection (ROC AUC) chose a tree that flagged no resistant patients, since
  only 24% are resistant → How we solved it: switched to balanced accuracy and class-weighted trees;
  now the best tree catches 65% of resistant patients.
- Problem: the downloaded data file was world-readable (umask 002) → How we solved it: `chmod 600`, and
  the script sets umask 027 so its outputs aren't world-readable.
- Worked with: Bobby took role B (script) in the group chat; Eric and James to choose C and D.
