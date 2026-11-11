#!/usr/bin/env python3
"""Build a single self-contained prompt from the skill folder.

For chat assistants without a skill system (DeepSeek, ChatGPT, Kimi, Qwen, ...),
paste dist/system-prompt.md as the system prompt / custom instructions, or at
the start of a conversation. Re-run after editing the skill so both stay in sync:

    python scripts/build_prompt.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "travel-itinerary-planner"
OUT = ROOT / "dist" / "system-prompt.md"

ORDER = [
    "references/intake.md",
    "references/styles/fun.md",
    "references/styles/history-culture.md",
    "references/styles/food.md",
    "references/styles/photo.md",
    "references/transport/rail-pass.md",
    "references/transport/other-modes.md",
    "references/deliverable-template.md",
]

PREAMBLE = """# Travel itinerary planner — standalone prompt

You are a travel-planning assistant. Follow the workflow below for any request
to plan, improve or cost a trip. This is the single-file version of the
`travel-itinerary-planner` skill: the referenced files are included as
appendices below, and scripts mentioned in the text are optional — if you
cannot run code, do the arithmetic yourself and show subtotals.

"""


def main():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    body = re.sub(r"\A---.*?---\s*", "", body, flags=re.S)  # drop frontmatter
    parts = [PREAMBLE, body.strip(), "\n\n---\n\n# Appendices\n"]
    for rel in ORDER:
        text = (SKILL / rel).read_text(encoding="utf-8").strip()
        parts.append(f"\n\n## Appendix: {rel}\n\n{text}\n")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(''.join(parts)):,} chars)")


if __name__ == "__main__":
    main()
