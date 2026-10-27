# Fishing note formats

The single spec for the four kinds of fishing note. `/ffpkb:ingest` (for trips and passed-on advice) and the `fishing-research` skill both write to it.

Every note serves one goal: helping the angler catch more fish and become a better angler. A sentence that would not change what they do on the water does not belong.

| Note | Type, author | Job |
| --- | --- | --- |
| Trip note | `journal`, `written_by: <angler>` | Raw source: what happened, and what it taught |
| Passed-on note | `reference`, `written_by: <angler>`, `source:` | Raw source: what a named guide, shop, friend, book, video or article told the angler |
| Wiki page (fish, technique, water) | `reference`, `written_by: claude` | The current best advice. The angler reads these before a trip |
| Research note | `research`, `written_by: claude` | Answers one question in depth and feeds the wiki pages |

**Who wrote it.** `written_by` records who composed the words. The angler's own notes (trip notes, passed-on notes and clippings) carry the angler's name, written `<angler>` in these files. Pages and research notes the agent writes carry the agent's name, e.g. `claude`.

## Regulations are not knowledge

No note carries regulation detail: limits, seasons, closures, gear rules, fees or passes.

- **Water pages:** each ends with a **Before you go** line of links to the official rules page, the emergency-rules page and the flow gauges.
- **Before a trip:** when the angler says they are going fishing, check the rules and conditions live and answer in chat. Write nothing.
- **The one exception:** when a gear rule on that water forbids a recommended technique (a second fly, bait, a barbed hook), add one clause saying so where the technique is described.

## Trip note

The angler's entry is the body, verbatim. It is never reworded, reordered or summarised.

Frontmatter, and nothing else:

```yaml
type: journal
created: YYYY-MM-DD      # the day it was filed; the filename carries the trip date
written_by: <angler>
domain: fishing
water: "[[<Water>]]"
flow_cfs:                # daily mean at the main gauge named on the water page
water_temp_f:            # daily mean, at the nearest gauge that records it
```

The body is a marked Claude debrief at the top, then the entry:

```markdown
> [!summary] Debrief — Claude, YYYY-MM-DD
> **Where:** [[<Water>#<Spot>]] → [[<Water>#<Spot>]] (scouted) → …
> **Conditions:** flow and trend at <gauge> · water °F · sky and air range · light: when shade or sun reached the water, sunset. Each number links to its source.
> **Fish:** who hooked or landed what, on which fly, where, and when in the swing or the day
> **Learned:** 2–4 lines, each ending with the page it updated → [[Sink tips]]
> **Try next:** 1–3 tests for the next outing, drawn from the pages' Try next lists
```

- **Earlier tests:** when the entry gives evidence on an earlier Try next item, the debrief says how it went.
- **Spots:** link them, never repeat them. Coordinates live on the water page.
- **Inferences:** state them as the angler's guess or as a guess ("probably a coho, per the angler"), never as fact.

## Passed-on note

Advice someone else gave the angler: a guide on a float, the counter at a fly shop, a friend, a book, a video, an article. The angler's capture is the body, verbatim, however rough. Web articles saved whole are clippings instead (`/ffpkb:ingest`'s `references/clipping.md`).

Frontmatter, and nothing else:

```yaml
type: reference
created: YYYY-MM-DD      # the day it was filed
written_by: <angler>
domain: fishing
source: <who or what said it: "Example River Fly Shop", a guide's name, a book title, or a URL>
```

- **Filename:** `<Source> on <subject>`, e.g. `Example River Fly Shop on low-water coho flies`.
- **The source is named, never guessed.** If the capture doesn't say who it came from, ask once. If the angler doesn't know ("a guy at the ramp"), that is the source.
- **Advice inside a trip entry** ("the shop said go small") stays in the trip note. Pages cite it as passed on, naming who said it.

## Wiki pages

These pages are the product. Each puts advice first and evidence after, and is rewritten as understanding improves, not appended to.

**Every line names its source.** An advice line with no citation is sourced or cut. Exempt: `## Try next` items, which are tests, and a line saying no source covers something.

Citations go inline, and the three kinds stay distinct:
- **Research:** link the research note's section, e.g. `([[<research note>#Presentation|research]])`. Add a source-type tag when a claim rests on one kind of source.
- **Trip:** link the trip note and say it was the angler's experience, e.g. "on [[2025-09-14 Example River|09-14]] both fish came on chartreuse after shade reached the water".
- **Passed on:** name who said it and link the note that records it, e.g. "the Example River shop told the angler to go small in low water ([[Example River Fly Shop on low-water coho flies|shop, via the angler]])". Advice from a trip entry links the trip note the same way.
- **Keep them apart:** a research claim is never phrased as the angler's experience, advice passed on to the angler is never phrased as their own observation, and one trip is an observation, not a pattern.
- **Disagreement:** where sources disagree, say so on that line.

Sections by kind of page:

- **Fish** (Coho salmon, Chum salmon…): a one-line intro, then:
  - `## Where they hold`
  - `## When they take`: light, flow, temperature, time of day, fresh vs coloured fish
  - `## Flies`
  - `## Presentation`
  - `## On <Water>`: one per water the angler fishes, covering timing, where in the reach and at what flows
  - `## Try next`
  - `## Trips`
- **Technique** (Swinging flies, Sink tips, Snap T…): an intro, then:
  - `## How to do it`
  - `## How to tell it's working`
  - `## Common mistakes`
  - `## Try next`
  - `## Trips`
- **Water** (Example River…): an intro, then:
  - `## How it fishes`: the river's character and colour, flows that fish well, what's in when, and the gauges
  - `## Spots`: one `### <Spot>` heading per spot, with a maps link to its coordinates, access, how it fishes and at what flow, and results
  - `## Try next`
  - `## Trips`
  - `## Before you go`: links only

Rules for every page:
- **`## Try next`** holds tests for the next outing, turning the angler's stated gaps and the research into something to do. For example: "On the upper bar, fish a heavier tip and count before starting the swing; note whether it ticks bottom." Once a trip answers an item, remove it and fold the answer into the advice.
- **`## Trips`** gets one dated line per trip: what happened that bears on this page, with a link to the trip note.
- **Empty sections** are left out, not stubbed.
- **One subject per page.** When a section's topic is a concept of its own, such as a sink-tip system inside Swinging flies, give it a page and leave one line and a link.

## Research note

It answers one question in depth and is readable on its own.

Structure:
- **In short: what to do.** 5–8 actionable bullets.
- **Sections by practical question.** For a water in a season, typically:
  - Where the fish hold, including run timing by week or month (no forecast counts)
  - What triggers a take
  - Flies
  - Presentation
  - Reading the water
  - Common mistakes
- **`## Where sources disagree`.**
- **Numbered `## Sources`:** publisher or author, title, link, date, type tag.

Sourcing:
- **Tags:** `[book]` · `[guide/shop]` · `[manufacturer]` · `[video]` · `[forum/social]` · `[media]` · `[peer-reviewed]` · `[agency/gov]`.
- **Corroboration:** key advice cites two or more independent sources. A claim resting on one is marked `single source`.
- **Freshness:** technique does not age. A classic book or an older video is a valid source; give its date and move on. Run timing and conditions need current sources.

Length follows the useful content. Every section must give the angler something they can do differently on the water. Cut forecast counts, fees, passes, management news and regulation detail.
