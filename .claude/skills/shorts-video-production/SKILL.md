---
name: shorts-video-production
description: Use when producing a new YouTube Short for the series: writing the script, building the video, and preparing title, description and upload checks.
---

# Produce a YouTube Short

## Format

- Vertical 9:16, 1080x1920.
- Target length under 60 seconds. Shorts can run up to 3 minutes, but shorter loops perform well.
- The first 2 seconds state the payoff or ask the question.
- End on a line that leads back to the opening, so the video loops.
- Add on-screen text for the key point, since many viewers watch without sound.

## Steps

1. Confirm the niche and the episode topic with the owner. Do not start without both.
2. Write `scripts/<episode>.md` in this order: hook (0-2 s), setup, one turn or surprise, payoff, loop line, sources. Keep narration under 150 words.
3. Build scenes as separate, editable files in `scenes/` using the chosen tool (code-based animation preferred).
4. Render to `renders/`. Check frame by frame for clipped text and for any visual that looks like a real person or place.
5. Run the `shorts-policy-check` skill before the video is marked ready.
6. Write metadata: title under 70 characters, a short description with one clear claim, and 3 to 5 hashtags.
7. Give the owner a checklist: file name, title, description, AI disclosure setting, thumbnail frame, upload time.
8. Update the tracker rows for production and pilot tasks, after the owner confirms.

## Rules

- Do not publish. The owner uploads the video.
- Do not invent facts. Every factual claim needs a source in the script's `sources` field.
- Keep each episode structurally different from the last.
