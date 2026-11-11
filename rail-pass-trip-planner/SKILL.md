---
name: rail-pass-trip-planner
description: Plan a cost-optimised, multi-city European trip around a rail pass (Interrail / Eurail Global or One Country Pass) and deliver a detailed day-by-day itinerary with exact trains, time slots for sights, hotels near stations, booking checklist and budget, exportable to Word. Use this skill whenever someone holds or is considering an Interrail/Eurail pass, asks for the "cheapest" way to string several European cities together by train, wants a timetabled itinerary ("几点到几点", "what train do I take"), asks which trains need seat reservations or are not covered by the pass, or wants a trip plan turned into a document — even if they only mention one leg (e.g. "fly to Rome then train to Benevento") or never say the word "itinerary".
---

# Rail-pass trip planner

Turn a rough travel wish ("fly to Rome, see a friend, then Italy → south of France → Spain, about two weeks") into a plan someone can actually follow on the ground: every leg has a real train number, every sight has a time slot, every night has a bed, and every euro is accounted for.

The value of this skill is not the sightseeing ideas (any model has those) — it is the **verification discipline** and the **rail-pass economics**. Most rail-pass plans fail on the details: a train the pass doesn't cover, a reservation quota that sold out, a regional train that doesn't run on Sundays, a palace closed on Tuesdays, an airport express that only accepts 1st-class passes. Read `references/pass-rules.md` before planning any rail leg; it collects these traps.

## Workflow

Work in this order. Each step narrows the next, so don't jump ahead to hotels or a pretty document before the transport skeleton is verified.

### 1. Pin down the constraints (ask at most once, briefly)

Extract what the user already said; ask only for what changes the plan:

- **Pass**: Global vs One Country, **continuous vs flexi** (flexi days change whether a cheap leg is worth "spending" a travel day — under ~€20 point-to-point, buy a ticket instead), class (2nd class changes which airport expresses are covered), expiry date.
- **Fixed points**: start date and city, any fixed stays (e.g. staying with a friend — that is free accommodation and a natural base for day trips), end date or "about N days", where they must end up.
- **Luggage**: cabin bag vs underseat bag decides the cheapest airline, not the headline fare.
- **Style**: "exterior photos only unless the interior is exceptional" vs museum-goer; budget vs comfort; early starts OK?

If the user is away or the request is clear, assume sensible defaults (2nd class, cabin bag, budget-conscious, exterior-first) and say which you assumed.

### 2. Build the transport skeleton first

1. **Flights** (in/out of the rail area): search live fares (Google Flights or similar) for the exact dates. Compare *total* cost including the bag the user needs — e.g. Jet2 includes a 10 kg cabin bag; Ryanair/easyJet/Vueling basic fares only include an underseat bag. Note arrival time vs what the user wants to do that day. Check the direct-flight calendar: low-cost routes often don't fly every day, which can force an extra night.
2. **Rail legs**: for each leg, find the options in three tiers and pick deliberately:
   - **€0 tier** — regional trains (IT Regionale/RV, FR TER, ES Rodalies/Cercanías/MD): no reservation, just add the leg in Rail Planner.
   - **cheap tier** — IT Intercity (€3).
   - **fast tier** — high-speed with compulsory paid reservation (Frecciarossa €13, TGV €10/20, AVE domestic €10, AVE/TGV international €25–35). Quotas for pass holders are limited — flag these to book first.
   Prefer €0 when it costs < ~1.5 h extra and doesn't break the day; pay for speed when it buys a meaningful chunk of daylight (state that trade-off to the user in one line).
3. **Verify every leg against a real timetable for that weekday.** Use e656.net (Italy, shows periodicity notes like "non circola nei giorni festivi"), SNCF Connect / TER sites (France), Renfe / kombo / Omio (Spain, international). Record train numbers. Read the periodicity notes — weekday vs Saturday vs Sunday/holiday differences are the most common silent failure. Check the operator: a "direct" train may be a private line (e.g. EAV, Italo) the pass doesn't cover.
4. **Check public holidays** in each country for the dates (e.g. ES 6 Dec, 8 Dec; IT 8 Dec) and **weekly closing days** of key sights (e.g. Reggia di Caserta closed Tuesdays).

### 3. Lay out the days

For each day produce a time-slotted table: `time | activity | transport / cost`. Guidelines that made the reference trip work:

- Use a **base** (friend's home, or 2–3 night hotel) for day trips instead of moving every day; it saves accommodation and packing.
- Check **sunset time** for the season and put outdoor sights before it; put viewpoints *at* sunset; evening = lit squares, food.
- Respect the user's style: if "exterior only", route as a walking loop between landmarks and list interiors as "optional" with price and why it's worth it (only flag interiors that are genuinely exceptional, e.g. Sagrada Família).
- Build in luggage handling on travel days (station left-luggage, ~€5–6/5 h) and buffer before trains (15–30 min; more at big stations).
- Give a concrete **backup** for any fragile link (tight connection, low-frequency bus, quota-limited train).

### 4. Accommodation

Search live prices for the exact nights (Google Hotels is fine), filtered to walking distance of the station the user arrives at / leaves from. Give **3 options per city** in a table: name, stars/rating, price per night, one-line reason (cheapest / best rated / closest to the early train). Note city tax is extra and paid on arrival (IT/FR/ES roughly €1–8 per person per night).

### 5. Checklist, rules, budget

- **Booking checklist** as tick-boxes, ordered by urgency (quota-limited reservations first, then flights, hotels, timed-entry tickets).
- **Pass rules** that apply to *this* trip (what's not covered, where to book reservations without the €2 Interrail fee — e.g. Trenitalia app for Italian trains).
- **Budget table**: look up today's FX rate; give low/high per category (flights incl. bags, local transfers, reservations, local transport, hotels, city tax, food per country-day, tickets, optional, ~10% contingency) and a total in the user's home currency. Say which categories dominate and where the savings are.
- **Practical tips**: pickpocket hotspots on the route, emergency number 112, plug type, card vs cash, strike checks (Italy: Trenitalia "Infomobilità"), visa scope (Schengen covers Monaco; a single-entry visa is enough if the trip never leaves Schengen).

### 6. Deliver

- Default: a shareable living document (Claude Docs / artifact) so the user can edit and comment; fill section by section.
- If the user asks for **Word**, write the itinerary as Markdown following `references/itinerary-template.md`, then run:
  ```bash
  python scripts/md_to_docx.py itinerary.md "Trip itinerary.docx"
  ```
  (needs `pandoc` and `python-docx`; produces A4, CJK-friendly font, coloured table headers).
- Keep the chat reply short: what changed, the main decisions, what the user must verify themselves.

### 7. When the user changes something

Users iterate ("move it to the 23rd", "I need a bag", "drop the extra day", "make it two weeks"). Re-run only the affected steps, re-check downstream knock-ons (a shifted date changes weekday-only trains, holidays, closing days, flight availability), and keep every copy (doc, Word file) in sync — say explicitly if one copy is now stale.

## Honesty rules

- Never present a train time you haven't checked as confirmed. If you only found it for a different date, say "based on the timetable for <date>; re-check in the app 1–2 days before".
- Prices are snapshots: label them with the query date.
- When you correct an earlier claim (e.g. "the airport express is covered" → it isn't for 2nd class), say so plainly.
- Don't book, pay, or activate the pass for the user unless they explicitly ask; link them to where to do it.

## Files

- `references/pass-rules.md` — reservation fees, what the pass does *not* cover, country-specific traps. Read before planning rail legs.
- `references/itinerary-template.md` — Markdown skeleton for the final document.
- `scripts/md_to_docx.py` — Markdown → styled .docx.
- `examples/rome-benevento-riviera-barcelona-2weeks.md` — a complete worked example (Chinese), useful to calibrate the level of detail.
