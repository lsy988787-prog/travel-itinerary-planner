# AGENTS.md

This repository contains one agent skill: `travel-itinerary-planner/`.

When a user asks to plan, improve, cost or document a trip (旅行、行程、攻略、自由行、通票路线), read
`travel-itinerary-planner/SKILL.md` and follow its workflow. Load files under
`travel-itinerary-planner/references/` only when the workflow points to them.

Development notes for agents editing this repo:
- Keep `SKILL.md` portable: standard frontmatter only (`name`, `description`, `license`, `compatibility`), no tool-specific instructions without a fallback.
- `name` must stay equal to the folder name; `description` ≤ 1024 characters.
- After editing the skill, run `python scripts/build_prompt.py` to regenerate `dist/system-prompt.md`, and `python scripts/check.py` to validate.
