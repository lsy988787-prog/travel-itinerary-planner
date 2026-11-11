# rail-pass-trip-planner

A Claude skill that plans **cost-optimised, multi-city European trips around an Interrail / Eurail pass** and delivers a day-by-day itinerary you can actually follow: verified train numbers, time slots for every sight, three hotel options near each station, a booking checklist, a budget in your home currency, and an optional Word export.

一个 Claude 技能：围绕 Interrail / Eurail 通票，规划最省钱的欧洲多城铁路旅行，输出可以照着走的逐日行程——核实过的车次、每个景点的时间段、车站附近 3 家住宿选择、订票清单、预算表，并可导出 Word。

## Why

Rail-pass plans usually fail on details, not ideas:

- a "direct" train the pass doesn't cover (Italo, EAV private lines, Leonardo Express for 2nd class)
- a pass-holder reservation quota that sold out (Renfe international AVE, TGV)
- a regional that doesn't run on Saturdays / Sundays / holidays
- a palace closed on Tuesdays, a sunset at 16:40 in December
- a cheap flight that isn't cheap once you add the cabin bag

The skill makes Claude verify each leg against a real timetable for that weekday, prefer reservation-free trains when they don't cost the day, flag what to book first, and keep every copy of the plan in sync when you change your mind.

## What's inside

```
rail-pass-trip-planner/
├── SKILL.md                         # the workflow Claude follows
├── references/
│   ├── pass-rules.md                # reservation fees, exclusions, country traps (IT / FR / ES)
│   └── itinerary-template.md        # skeleton of the final document
├── scripts/
│   └── md_to_docx.py                # Markdown → styled .docx (A4, CJK font, coloured tables)
└── examples/
    └── rome-benevento-riviera-barcelona-2weeks.md   # full worked example (Chinese)
```

## Install

- **Claude.ai / Claude app**: download `rail-pass-trip-planner.skill` from Releases (or zip the `rail-pass-trip-planner/` folder) and add it under *Settings → Capabilities → Skills*.
- **Claude Code**: copy the `rail-pass-trip-planner/` folder into `~/.claude/skills/` (or your project's `.claude/skills/`).

The Word export needs [`pandoc`](https://pandoc.org/) and `pip install python-docx`.

## Try it

> I have a continuous Interrail Global Pass (2nd class) until 31 Dec. I want to fly from Birmingham to Rome on 23 Nov, spend an afternoon in Rome, stay with a friend in Benevento for a few days, then go through Italy, the south of France and Spain and fly home from Spain — about two weeks. I'm on a budget and mostly want exterior photos of landmarks. Make a detailed plan and a Word file.

> 我有 Interrail 连续型通票，想从米兰到巴塞罗那玩 10 天，只坐不用订座的车可以吗？帮我排一下。

## Example output

See [`examples/rome-benevento-riviera-barcelona-2weeks.md`](rail-pass-trip-planner/examples/rome-benevento-riviera-barcelona-2weeks.md): 15 days, Rome → Benevento (base for Naples, Salerno, Caserta) → Florence → Pisa → Genoa → Nice/Èze/Monaco → Marseille → Barcelona, with only 3 paid reservations (≈ €41).

## Caveats

Fees, timetables and prices change. The skill tells Claude to label every price with its query date and to say when a train time was taken from a different date — always re-check in the operators' apps 1–2 days before travel. The skill never books or pays on your behalf.

## License

MIT — see [LICENSE](LICENSE).
