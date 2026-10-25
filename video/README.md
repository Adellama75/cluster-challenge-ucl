# Video script workflow (team only)

After each work session, run `/script` in Claude Code started **inside this repo**, optionally with notes:
`/script got the venv working; the first numpy wheel failed so we pinned an older one`. It drafts
narration for the matching video question in `video/script.md` (numbers only from repo files or your
notes, `[TODO]` otherwise), keeps each segment within its time budget, adds a teamwork entry to
`video/teamwork-log.md`, and commits locally. Then push. Mark finished lines `<!-- locked -->` to keep them.
Not using Claude Code? Paste `.claude/skills/script/SKILL.md` into your assistant along with your notes.
