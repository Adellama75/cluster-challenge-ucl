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

## 2026-10-25 22:10 · Ada Ge (A)
- Did: wrote the submitted ReadMe's quick start, layout, environment and access sections; moved the
  team-only `/script` notes out of it (to `video/README.md`) so markers only see setup and run steps;
  drafted the Q1/Q2 cloud-and-security lines for D to take over.
- Problem: the VM login method, Python version and folder path aren't known until the emails arrive on
  Monday → How we solved it: wrote everything we do know and marked the five gaps as `[Mon: …]`, so
  filling them in on Monday is a five-minute job.
- Learned along the way: `lscpu` lists CPU side-channel bugs (Spectre-style) and their patches, a
  concrete example of why shared cloud hardware needs security; ACLs can grant access that `ls -l`
  doesn't show, so we'll check `getfacl` on the VM too.
- Worked with: role guides now in `guides/` for Bobby (B) and whoever takes C and D.
