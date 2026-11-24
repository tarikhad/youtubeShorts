---
name: shorts-project-resume
description: Use when resuming the YouTube Shorts project or asking what to do next; reads the project tracker and saved notes and reports the next open step.
---

# Resume the YouTube Shorts project

Use this skill at the start of any session about the Shorts project, so work continues where it stopped.

## Steps

1. Read `CLAUDE.md` and the file list under `scripts/` and `scenes/`.
2. Read the project tracker (Sheets artifact, tab "Plan") through the Claude Docs connector. Get the current revision first.
3. List the rows with status "In progress". Then list the first 3 rows with status "To do", in row order.
4. Report in at most 5 lines: what is in progress, what comes next, and any open decision (for example, the niche choice).
5. Ask the owner to confirm before changing any status.

## Rules

- Never mark a row "Done" unless the owner confirms the work is finished.
- If the tracker and the repository disagree, say so and ask which is current.
- After the owner confirms a change, update the row and summarize what changed.
- Do not repeat the full plan. The owner needs the next step, not the whole list.
