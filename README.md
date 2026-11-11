# travel-itinerary-planner

**An AI travel-planning skill that asks before it plans, verifies before it promises, and delivers a plan you can actually follow.**
一个先问清需求、再按偏好定制、最后交付可执行行程的 AI 旅行规划技能。

Works as an [Agent Skill](https://agentskills.io) in Claude, Codex, Cursor, Gemini CLI and other skill-compatible agents, and as a single paste-in prompt for chat assistants without skills (DeepSeek, ChatGPT, Kimi, Qwen, …).

## What it does / 它做什么

1. **Intake / 需求确认** — from where to where, how many days, how to travel (fly, train, Interrail/Eurail pass, drive…), budget, and the kind of trip:
   - 🎢 **Fun & entertainment 娱乐** — how to have the best time: events, nightlife, experiences, pacing
   - 🏛️ **History & culture 历史人文** — what's genuinely worth it, short background stories, how to visit
   - 🍝 **Food 美食** — signature dishes, cheap local spots, beating queues, dietary needs
   - 📸 **Photo spots 出片** — exact places to stand, best light, angles and pose ideas
2. **Route & transport skeleton** — live fares incl. bags, timetables checked for the actual weekday, rail-pass traps (what the pass doesn't cover, reservation quotas).
3. **Day-by-day plan** — time slots for every stop, tailored to the chosen style, sunsets, closing days, buffers, backups.
4. **Deliverable** — detailed itinerary · hotels (3 per stop) · **cost estimate 预估花费** · **itemised bill 预估账单** · **pitfalls guide 避坑指南** · **holiday & closure warnings 节假日/闭馆提醒** · friendly tips · booking checklist — as Markdown, a shared doc, or Word.

## Repository layout

```
travel-itinerary-planner/            ← the skill (copy this folder)
├── SKILL.md
├── references/
│   ├── intake.md
│   ├── deliverable-template.md
│   ├── styles/        fun · history-culture · food · photo
│   └── transport/     rail-pass (Interrail/Eurail, IT/FR/ES) · other-modes
├── scripts/
│   ├── bill.py        itemised bill CSV → totals by category & currency
│   └── md_to_docx.py  Markdown → styled Word
└── examples/
    └── rome-benevento-riviera-barcelona-2weeks.md
dist/system-prompt.md                ← single-file prompt for agents without skills
scripts/build_prompt.py · check.py   ← regenerate the prompt · validate the skill
AGENTS.md
```

## Install / 安装

| Platform | How |
| --- | --- |
| **Claude (app / claude.ai)** | Download `travel-itinerary-planner.skill` from Releases → Settings → Capabilities → Skills → upload. |
| **Claude Code** | `cp -r travel-itinerary-planner ~/.claude/skills/` (or `.claude/skills/` in a project) |
| **OpenAI Codex CLI** | `mkdir -p ~/.agents/skills && cp -r travel-itinerary-planner ~/.agents/skills/` (or `.agents/skills/` in a repo) |
| **Other skill-compatible agents** (Cursor, Gemini CLI, …) | Copy the folder into that tool's skills directory — see its docs. |
| **DeepSeek / ChatGPT / Kimi / Qwen / any chat assistant** | Paste [`dist/system-prompt.md`](dist/system-prompt.md) as the system prompt / custom instructions, or at the start of a chat. |

Optional for scripts: Python 3, `pip install python-docx`, and [pandoc](https://pandoc.org/) for Word export. Without web access or code execution the skill still works — it labels prices and timetables as estimates and does the arithmetic by hand.

## Try it / 试一试

> 我 11 月 23 日从伯明翰出发，有 Interrail 连续型通票，想去罗马玩半天，在贝内文托朋友家住几天，再经意大利、法国南部到西班牙，两周左右，从西班牙飞回。省钱优先，景点外观拍照就行。帮我出详细行程和 Word。

> Weekend in Lisbon for a couple, foodie trip, mid budget — where to eat without queues, and two great photo spots for sunset?

> 带爸妈去京都 5 天，历史人文为主，走路不能太多，每个景点讲讲背景。

## Example

[`examples/rome-benevento-riviera-barcelona-2weeks.md`](travel-itinerary-planner/examples/rome-benevento-riviera-barcelona-2weeks.md): 15 days Rome → Benevento (base for Naples, Salerno, Caserta) → Florence → Pisa → Genoa → Nice/Èze/Monaco → Marseille → Barcelona with only 3 paid rail reservations (≈ €41).

## Development

```bash
python scripts/check.py         # validate frontmatter, file references, script tests
python scripts/build_prompt.py  # regenerate dist/system-prompt.md after editing the skill
```

## Caveats

Prices, timetables and opening hours change. The skill labels every price with its query date and flags times taken from a different date — re-check in official apps 1–2 days before travel. It never books or pays on your behalf.

## License

MIT — see [LICENSE](LICENSE).
