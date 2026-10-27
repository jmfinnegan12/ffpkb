# Fishing trip entry

Extra steps when the source is a day on the water. The angler's entry goes in verbatim; Claude adds the day's conditions and a short debrief above it. Formats: `${CLAUDE_PLUGIN_ROOT}/skills/fishing-research/references/wiki-page-format.md` — read it first.

## Before the review table

**The note may already exist.** When the trip is already filed as `Notes/YYYY-MM-DD <Water>.md`, take that note as the entry and bring its frontmatter to the format.

1. **Trip note.** The source is filed as `Notes/YYYY-MM-DD <Water>.md` from `Templates/fishing trip.md`, named for the trip date, with `water` set as a link to the water page (unresolved if the page doesn't exist yet). If the entry gives no date or no water, ask once for both together; never guess them. The body is the entry as written — a transcript gets punctuation and paragraph breaks only, a handwritten page gets transcribed, each paragraph on one line.

2. **Conditions.** They go in two places: `flow_cfs` and `water_temp_f` in the frontmatter, and the debrief's Conditions line, with a link for every number. If no source has a value, leave it empty; never estimate one.
   - **Flow:** the daily mean at the main gauge named on the water page, the trend over the prior two days, and any major tributary in between. US rivers: USGS daily values, e.g. `https://waterservices.usgs.gov/nwis/dv/?format=json&sites=<id>&startDT=<d-2>&endDT=<d>&parameterCd=00060,00010`. BC rivers: Water Survey of Canada.
   - **Water temperature:** from the same gauge, or the nearest one that records it. Name the gauge.
   - **Weather and light:** sky, air-temperature range, rain that day and the day before, wind, sunset, and when shade or sun reached the water if the entry says. Open-Meteo works for any past date; label its values as model values, not a station reading.

3. **Spots.** When the entry mentions saved map pins, get them from a shared map list link the angler gives (a Google Maps list, for example) or coordinates they paste. Never place a spot from the entry's description alone. If the pins aren't available, say so. A spot not yet on the water page becomes a proposed `### <Spot>` heading there.

4. **Debrief, first three lines.** Draft the debrief callout in the format's shape with **Where**, **Conditions** and **Fish**. **Where** links the spots' headings on the water page, in the order fished. **Fish** says who hooked or landed what, on which fly, where, and when. A guess in the entry stays a guess.

## In the review table

The trip note's detail cell gives the conditions in one line. For its Update pages rows, read the water, fish and technique pages the trip touches, and the research notes on the water. Kinds of change:
- a line under `## Trips`;
- an advice line the trip supports, contradicts or refines, worded so it is clear the evidence is one trip;
- advice someone gave the angler that day (a guide, the shop, another angler), cited as passed on and naming who said it, not as their observation;
- a Try next item answered (fold the answer into the advice and remove the item), added, or dropped;
- a new spot heading on the water page;
- the trip on the [[Fly Fishing]] hub's Trips line, and any new page on its lists.

Under the Update pages table, draft the debrief's **Learned** lines (each ending with the page it updates) and **Try next** lines (from the pages' Try next lists, plus anything the entry suggests).

## On apply

Write the debrief callout — all five parts — above the entry, then the approved page changes. The callout is marked as Claude's (`> [!summary] Debrief — Claude, YYYY-MM-DD`), which is what lets it be revised later inside the angler's trip note.

When no research note covers the water, end the report with one line offering `/ffpkb:fishing-research-report <water>, <season>`.
