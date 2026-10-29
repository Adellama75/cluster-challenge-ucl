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

## 2026-10-27 10:00 · Ada Ge (A)
- Did: got onto the team VM through Condenser's JupyterHub terminal; downloaded the repo, built the
  venv and pinned pandas 3.1.0 / scikit-learn 1.9.1 / matplotlib 3.11.2 (Python 3.12.13); moved the
  data into `data/` and locked it down; ran the script end to end on the VM (34 s, 20 output files,
  same results as on a laptop). Bobby (B) can now run his script there.
- Problem: only Eric's login email arrived, and the SSH username wasn't in either email; guessing
  `root`, `ubuntu`, `almalinux` and others failed → How we solved it: shared Eric's JupyterHub login as
  instructed, and found the username (`cc`) in the access PDF the organisers posted on Slack.
- Problem: we wanted to SSH from our own laptops; tried the CS department's gateway, but it timed out
  → How we solved it: asked the organisers on Slack, who confirmed access is only through the
  JupyterHub terminal, so the ReadMe documents that route.
- Problem: the VM has no git (and no root to install it) → How we solved it: downloaded the repo as a
  tarball with curl, as planned in guide A.
- Problem: the data file arrived world-readable (`-rw-r--r--`) → How we solved it: recorded it first
  for Q3, then `chmod 700 data` and `chmod 600` on the file.
- Worked with: Eric (shared login, first data download on Monday); Claude typed in the JupyterHub
  terminal via the browser while Ada directed.

## 2026-10-29 11:50 · Eric Huang (D)
- Did: final timing pass on the video script, which read at about 6:00 (840 words at 140 words per
  minute) and now reads at about 4:47 (670 words); wrote the outro; finished Q1, Q2 and Q8; made the
  Q4 chart (`video/q4_our_data_vs_england_wales.png`) and a readable 1080p screen of the final tree
  (`video/q6_final_tree_readable.png`); wrote the storyboard, recording plan and cut list
  (`video/storyboard.md`). Then filled gaps in the other roles: ran C's open checks (other seeds,
  extra columns, a logistic-regression baseline; `notes/2026-10-29-model-checks.md`), added the
  docstrings that guide B's checklist asks for (same output, byte for byte), wrote a risk-factor
  screen (`src/risk_factors.py`, reasoning in `notes/2026-10-29-risk-factors.md`), and wrote Bobby's
  VM checklist (`notes/2026-10-29-vm-jobs-for-bobby.md`).
- Problem: the script ran a minute over the 5:00 limit → How we solved it: cut every segment down to
  its main points, noted what was cut under each one, and listed further cuts in case a recording
  still runs long.
- Problem: our answer to "what are the main risk factors?" rested on one feature-importance chart of
  two columns → How we solved it: tested every patient factor in the data, alone and together,
  against shuffled copies and columns of random numbers. Only age beats noise (cross-validated AUC
  0.71, where 95% of its shuffled copies stay below 0.54; odds of resistance 1.59 times higher per
  decade). The chart's 0.09 for deprivation isn't evidence: on the same measure a continuous column
  of random numbers scores 0.16, and on held-out patients deprivation is level with the noise.
- Problem: Q7 described logistic regression only in theory → How we solved it: ran it on the same
  split and folds as the script. It matched our tree (CV balanced accuracy 0.660 vs 0.659), so Q7
  now says we tried it.
- Problem: Q2 had to say where our data physically lives and whether Condenser is cleared for patient
  data, and we didn't know → How we solved it: checked Condenser's own about page: "All hardware
  resides in UCL facilities", and it is "not certified for the secure storage and processing of
  sensitive data".
- Problem: a fresh read-through found lines stronger than our sources ("everything is encrypted",
  real records "shouldn't go there") and a tree screen too small to read in a video → How we solved
  it: reworded them to match the sources, and rendered the tree at 1920 × 1080 with large text.
- Worked with: built on James's 29 Oct script pass and Ada's data notes; Q3 to Q7 owners to check
  their lines before recording; Bobby has the VM checklist.
