# Decisions

Format: date, question, options considered, choice, reason. The easiest option to reverse is preferred.

## 2026-11-24: Open time limit in the stop list
- **Question:** The operating rules contain an unfilled placeholder: "[X hours / one day] to undo".
- **Options:** a few hours; one day.
- **Choice:** One day.
- **Why:** It is the stricter of the two once applied as "anything taking longer than this to undo needs approval". Wider limits can be agreed later.

## 2026-11-24: Operating rules vs. "ask the owner" in CLAUDE.md and the skills
- **Question:** CLAUDE.md and the skills said to confirm tracker changes with the owner first. The new rules say decide and act.
- **Options:** keep asking; follow the new rules.
- **Choice:** The new rules win, except for the stop items. Tracker rows are marked Done when finished and verified. Rows needing the owner's own action stay open.
- **Why:** The owner's latest instruction is explicit. Recorded in OPERATING.md and CLAUDE.md.

## 2026-11-24: Generic product, no real brand
- **Question:** Video 1 product.
- **Choice:** Generic plastic water bottle. Owner agreed in chat.
- **Why:** Fewer sourcing, trademark, and accuracy risks.

## 2026-11-24: Rendering tool
- **Question:** Manim, Remotion, p5.js, or something else.
- **Options tried:** `pip download manim` failed (no package network access). Remotion and p5.js would need npm installs, also unavailable. Available: Python 3, Pillow 12.3, numpy 2.5, ffmpeg with libx264.
- **Choice:** Custom Python + Pillow renderer piping raw frames to ffmpeg (`tools/render_episode01.py`).
- **Why:** It works with what is installed, renders 55 s in about 25 s, and is fully code-controlled. Easy to reverse: scenes are simple functions that can be ported to Manim later.
- **Risk:** Hand-built animation is plainer than a dedicated tool. Revisit once package installs work.

## 2026-11-24: No voiceover in the pilot
- **Question:** Narration method (tracker row 15).
- **Options tried:** No text-to-speech engine installed (espeak, espeak-ng, pico2wave, festival, pyttsx3 all missing), and no package installs.
- **Choice:** Silent render with all script content as on-screen text. Narration text is kept in the script file for a later voiceover.
- **Why:** Shorts are often watched muted, so on-screen text is needed anyway.
- **Owner action:** Add a track from the YouTube Audio Library at upload (free, no licensing step), or record the narration.

## 2026-11-24: Video 1 twist
- **Question:** The first draft's twist (two-step molding) was weak.
- **Choice:** New twist: many water plants don't make their bottles; they arrive empty on pallets from a bottle maker. Two-step molding stays as the main explanation.
- **Why:** It is a real supply-chain fact, not just a manufacturing detail, and it fits the niche. Sourced to two trade-press plant profiles.
- **Risk:** "Many" rests on two examples. Safer wording, "Some", is noted in the script.

## 2026-11-24: Language and length
- **Choice:** English, 55 seconds.
- **Why:** Widest Shorts audience, and the owner's working language. 55 s stays under the 60 s target with room for a loop.

## 2026-11-24: Series structure
- **Choice:** Four episodes, each with a different storytelling structure (forward chain, reverse chain, parts count, clock). See `scripts/SERIES.md`.
- **Why:** YouTube's July 2026 clarification excludes "generic, repetitive, or template-based" content from monetization. Changing structure, not just product, is the safeguard.

## 2026-11-24: Public repository
- **Question:** The repo `tarikhad/youtubeShorts` is public. Pushing new files would publish them.
- **Choice:** Commit locally, do not push. Listed under BLOCKED FOR APPROVAL in STATUS.md.
- **Why:** Publishing previously private material is a stop item.
