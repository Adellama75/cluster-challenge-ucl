---
name: script
description: Turn the work session that just finished into draft narration for the team's 5-minute UCL challenge video, and log teamwork evidence. Use when someone types /script, or says they're done for now, logging off, or wrapping up a work session on this repo.
---

# /script: draft video narration from a work session

Run this at the end of every work session. It writes draft narration into `video/script.md` and a
teamwork entry into `video/teamwork-log.md`, based on what actually happened since the last run. The
person's words after `/script` are notes about the session ("got the venv working, numpy wheel failed
first") and take priority over anything you infer.

## 1 Gather what happened

- `video/.script-state` holds the commit hash of the last run (missing on the first run: use the
  whole history).
- `git log --stat <last>..HEAD` and `git diff <last>..HEAD` (ignore large generated files).
- New or changed files in `outputs/` (figure names, the comparison table) and `notes/`.
- The person's notes from the command arguments, and who they are (`git config user.name`).

If nothing changed and there are no notes, ask one question: what did you work on and what was hard?
Don't invent a session.

## 2 Write narration under the right questions

`video/script.md` has one section per segment, in video order, each with a time budget. Map the session
onto them:

| Work | Segment |
|---|---|
| Logging in, VM, cloud setup, security choices | Q1, Q2 |
| Data file permissions (`ls -l` before and after, `chmod`) | Q3 |
| Data exploration, class balance, synthetic data | Q4, Q5 |
| Model fitting, comparison, the chosen tree, risk factors | Q6 |
| Other models tried or considered | Q7 |
| Who did what, problems hit and how they were solved | Q8 |

For each segment touched, add or revise lines of narration in plain spoken English, first person
plural ("we"), plus a `[screen: …]` line saying what to show (a figure from `outputs/`, a terminal
command). Rules:

- **Numbers come only from files in the repo or the person's notes.** Cite the source next to the line:
  `<!-- src: outputs/model_comparison.csv -->`. If a number isn't available yet, write
  `[TODO: number from …]` instead of guessing.
- Keep each segment within its word budget (140 words per minute). If it's over, tighten the weakest
  lines rather than dropping new material, and say so.
- Revise, don't append forever: merge new lines into the segment so it reads as one script.
- Keep lines marked `<!-- locked -->` exactly as they are.

## 3 Log teamwork evidence

Append one entry to `video/teamwork-log.md`:

```
## <date> <time> · <name> (<role letter if known>)
- Did: …
- Problem: … → How we solved it: …
- Worked with: …
```

Only what happened. This is the evidence for the 15 teamwork marks, so problems and how they were
solved matter more than polish.

## 4 Finish

1. Write the current `HEAD` hash to `video/.script-state`.
2. Show the person: the segments changed (a short diff summary), the word count per segment against its
   budget, the total against 700, and the open TODOs.
3. Commit `video/` with the message `script: <one-line summary of the session>`. Don't push. Remind
   them to push so teammates get the update.
