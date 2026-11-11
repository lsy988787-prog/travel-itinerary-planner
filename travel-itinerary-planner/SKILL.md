---
name: travel-itinerary-planner
license: MIT
compatibility: Works best with web search/browsing for live prices and timetables, and Python 3 (+ pandoc, python-docx) for the bill and Word export; degrades gracefully without them.
description: Plan a trip end to end and deliver a ready-to-follow itinerary — first pin down where from/to, how many days, how to travel and what kind of trip it is (fun & entertainment, history & culture, food, photo spots), then produce a day-by-day timed plan with verified transport, hotels, cost estimate, itemised bill, pitfalls guide and holiday/closure warnings, exportable to Word. Use this skill whenever someone wants to plan, design or optimise a trip or holiday (旅行/行程/攻略/自由行/怎么玩), asks "what's the cheapest way to get from A to B and what to see", wants a multi-city route, a rail-pass (Interrail/Eurail) plan, a food or photography trip, or wants an existing plan made more detailed, costed or turned into a document — even for a single leg or a weekend.
---

# Travel itinerary planner

Turn "I want to go somewhere" into a plan someone can follow on the ground: every leg has a real departure, every stop has a time slot chosen for *their* kind of trip, every night has a bed, every euro is in the bill, and the traps are flagged before they bite.

Two things make this skill worth more than a generic answer:

1. **Intake before planning.** The same city is a different trip for a foodie, a history lover, a photographer or someone who just wants to have fun. Ask, then tailor.
2. **Verification discipline.** Plans fail on details — a train the pass doesn't cover, a museum closed on Mondays, a restaurant shut for August, a cheap flight that isn't cheap once you add the bag. Check the things that decide the plan against live sources, and label what you couldn't check.

## Phase 1 — Intake (ask first, briefly)

Read `references/intake.md` for the full question list and sensible defaults. In short, collect:

| Must know | Ask if not given |
| --- | --- |
| From → to (cities/region), start date, number of days | — |
| How they'll travel and any preferred mode (fly / train / rail pass / drive / bus / mix) | pass type & class, car, budget airline OK? |
| Trip style — one or more of **fun & entertainment**, **history & culture**, **food**, **photo spots**, or relaxed sightseeing | interiors vs exterior-only, pace |
| Budget level and party (solo / couple / family / friends) | — |
| Fixed points: friends to stay with, events, must-sees, dates that can't move | luggage (cabin bag?), dietary needs, mobility |

Ask everything you still need **in one round** (if your environment has a multiple-choice question tool, use it with ≤ 4 questions; otherwise one short message with defaults in brackets). Extract what the user already said rather than asking again. If the user is away or says "just plan it", assume defaults (budget-conscious, cabin bag, relaxed sightseeing, public transport) and state them at the top of the plan.

## Phase 2 — Route and transport skeleton

Fix the skeleton before hotels or pretty documents, because everything else hangs off it.

1. **Route**: order the stops to avoid backtracking; use a base (a friend's home or a 2–3 night hotel) for day trips instead of moving daily — it saves money and packing.
2. **Long-distance legs**: search live options for the exact dates. Compare the *total* cost the user will actually pay (bags, seat reservations, transfers to remote airports). Check whether low-cost routes fly every day.
3. **Rail**: if a rail pass is involved, read `references/transport/rail-pass.md` first — it lists what the pass does not cover, reservation fees and country traps. For any train, verify against a timetable for that **weekday** (Saturday/Sunday/holiday patterns differ) and record train numbers.
4. **Other modes** (driving, buses, ferries, city transport): see `references/transport/other-modes.md`.
5. **Closures & holidays**: check public holidays in each country for the dates, weekly closing days of key sights, seasonal closures (ferries, mountain roads, restaurants in August), strikes.

## Phase 3 — Day plans tailored to the trip style

Read the style guide(s) that match the user's answers and weave them into each day:

- `references/styles/fun.md` — entertainment, nightlife, experiences, pacing for maximum enjoyment
- `references/styles/history-culture.md` — what's genuinely worth it, short background stories, how to visit (tickets, guides, order)
- `references/styles/food.md` — local specialities, where locals eat cheaply, beating queues, dietary needs
- `references/styles/photo.md` — exact spots, best light/time, angles and pose ideas, crowd avoidance

Each day gets a table `time | activity | transport / cost`, plus 1–3 bullet notes. General rules:

- Check sunset time for the season; outdoor sights before it, viewpoints *at* it.
- Put luggage handling and buffers (15–30 min before trains, 2 h before flights) into the timeline on travel days.
- Mark interiors/paid extras as *optional* with price and the reason they're worth it.
- Give a concrete backup for any fragile link (tight connection, rare bus, weather-dependent sight).

## Phase 4 — Hotels, money, warnings

- **Hotels**: live prices for the exact nights, near the station/area that suits the plan; 3 options per stop (cheapest / best rated / most convenient) in a table; note city tax.
- **Cost estimate (预估花费)**: low/high per category with today's FX rate, in the user's home currency; say which categories dominate and where to save.
- **Itemised bill (预估账单)**: one line per payable item (date, item, who/where to pay, amount, status: paid / to book / pay on the spot). Write it as CSV and run `python scripts/bill.py bill.csv --rate EUR:GBP=0.84 --home GBP` to get the totals table — arithmetic done by code, not by hand.
- **Pitfalls guide (避坑指南)**: scams and pickpocket hotspots on this route, tourist-trap restaurants, tickets that must be pre-booked, transport that the pass/card doesn't cover, common mistakes at these specific stations/airports.
- **Holiday & closure warnings (节假日/闭馆提醒)**: a dated list of what is closed or different on the trip days.
- **Friendly tips (温馨提示)**: visa/entry, weather and clothing, plugs, payment/cash, apps, emergency numbers, a booking checklist ordered by urgency.

## Phase 5 — Deliver

Follow `references/deliverable-template.md`. If your environment offers a shareable/editable document format, use it; otherwise write the plan as Markdown (a file if you can write files, else directly in the reply). If the user asks for Word, write Markdown to the template and run:

```bash
python scripts/md_to_docx.py itinerary.md "Trip itinerary.docx"
```

Keep the chat reply short: the key decisions, the total cost range, what the user must book first and what to re-check before departure.

## When the user changes something

Users iterate ("move it to the 23rd", "I need a cabin bag", "make it two weeks"). Re-run only the affected phases, re-check knock-ons (a new date changes weekday-only trains, holidays, closures, flight availability), and keep every copy (doc, Word, bill) in sync — say explicitly if a copy is stale.

## If your environment lacks a capability

This skill is written to work in any agent that can read `SKILL.md` (Claude, Codex, Cursor, Gemini CLI, …) and as a plain prompt in chat assistants (DeepSeek, ChatGPT, Kimi, Qwen …). Adapt instead of failing:

- **No web search / browsing**: plan from general knowledge, mark every price, timetable and opening hour as *estimate — verify*, and give the user the exact sites/apps to check (operator apps, official museum pages, flight search).
- **No code execution**: compute the bill by hand, show the subtotal per category, and double-check the grand total.
- **No file writing**: put the full itinerary in the reply in Markdown, following the template; the user can paste it into any editor.
- **No question tool**: ask the intake questions in one plain message.

## Honesty rules

- Don't present a departure time, price or opening hour you haven't checked as confirmed. If it came from a different date, say "based on <date>; re-check 1–2 days before".
- Label prices with the query date.
- When correcting an earlier claim, say so plainly.
- Never book, pay or activate passes for the user unless they explicitly ask.

## Files

- `references/intake.md` — question list, defaults, how to phrase the one-round intake
- `references/styles/*.md` — fun, history-culture, food, photo
- `references/transport/rail-pass.md` — Interrail/Eurail rules and traps (IT/FR/ES)
- `references/transport/other-modes.md` — flights, driving, buses, ferries, city transport
- `references/deliverable-template.md` — final document structure
- `scripts/bill.py` — itemised bill CSV → totals by category and currency
- `scripts/md_to_docx.py` — Markdown → styled .docx
- `examples/rome-benevento-riviera-barcelona-2weeks.md` — complete worked example (Chinese, rail pass, budget, exterior-photo style)
