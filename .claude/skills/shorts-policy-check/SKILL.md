---
name: shorts-policy-check
description: Use before publishing or monetizing an AI-generated YouTube Short, to check AI disclosure and inauthentic-content risk.
---

# Check a Short against YouTube policy

This check reflects YouTube's rules as of the July 2026 clarification. Verify against the current YouTube Help pages before relying on it. Record the date of the check in the script file.

## Checks

1. **AI disclosure.** Does the video show realistic people, places, or events that were generated or meaningfully altered by AI? If yes, set the "AI use" option in YouTube Studio before upload. Stylized, clearly non-realistic animation usually does not need the label.
2. **Repetitive or template content.** Does this video follow the same template as the last one with only the content swapped? If yes, change the structure. Template-only series are not eligible for monetization.
3. **Off-putting or distressing content.** Could the video upset viewers without a clear purpose? Flag it.
4. **AI personas on sensitive topics.** Is an AI presenter discussing finance, legal, health, or medical topics? Flag it. These are not eligible for monetization.
5. **Misleading content.** Does any visual or claim suggest something happened or someone said something that did not? Flag it.

## Output

Return a table with one row per check: result (Pass, Flag, or Needs review), the reason in one sentence, and the fix. Then give an overall verdict: publish, fix first, or ask the owner.

## Rules

- Do not give legal advice. State the policy text and the risk, and recommend checking YouTube's Help pages for edge cases.
- If a check cannot be decided from the script or the render, mark it Needs review and say what would decide it.
