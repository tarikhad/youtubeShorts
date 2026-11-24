# YouTube Shorts project

Series of AI-generated YouTube Shorts. The creator does not appear on camera.

## Operating mode

Work autonomously under `OPERATING.md`. Read it first. Record decisions in `DECISIONS.md`, progress in `STATUS.md`, and out-of-scope findings in `NOTES.md`. Only the stop items in `OPERATING.md` need the owner's approval.

## Working rules

- Work in English in code and files. Plan notes for the owner may be in German.
- Never publish or upload. The owner uploads manually after review.
- Every factual claim in a script needs a source the owner can check. Keep a `sources` field in each script file.
- Check every video against the `shorts-policy-check` skill before it is marked ready.
- Vertical 9:16, under 60 seconds, 1080x1920.
- Keep each episode structurally different. Do not reuse one template with only the content swapped.

## Layout

- `scripts/` one file per episode: hook, setup, turn, payoff, loop line, sources.
- `scenes/` editable scene files for the chosen animation tool.
- `renders/` rendered output, not committed (see `.gitignore`).
- `.claude/skills/` project skills.
- `.claude/agents/` project subagents.

## Tracker

The project plan lives in a Sheets tracker (tab "Plan"). Mark a row Done when the work is finished and verified. Rows that need the owner's action (account creation, uploads, payments) stay open until the owner reports them done.

## Tooling

- Renderer: `tools/render_episode01.py` (Python + Pillow + numpy, frames piped to ffmpeg). Manim and Remotion were not installable in the build environment; see `DECISIONS.md`.
- Render: `python3 tools/render_episode01.py` writes `renders/episode-01-water-bottle.mp4`.
