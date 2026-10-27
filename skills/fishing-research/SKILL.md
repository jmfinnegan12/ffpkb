---
name: fishing-research
description: Research how to catch fish on a water, a species, or with a technique — where the fish hold, what makes them take, which flies, how to present them, how to read the water — and file an in-depth, cited research note that feeds the fishing wiki's fish, technique, and water pages. Use whenever the angler asks for a fishing research report, "what's the fishing like in X", "how to fish X", a waters survey, or a species report. The deep multi-agent regional survey runs only when the angler asks for one. Regulations are never researched into notes; they are checked live before a trip. /fishing-research-report runs it.
---

# Fishing Research

A research note answers one question about catching fish: where they hold, what makes them take, which flies, how to present them, and how to read the water. It goes in depth and sources every claim. It is a source for the vault's Karpathy-style wiki. What lasts from it is rewritten into the fish, technique and water pages, which are what the angler reads before a trip. `references/wiki-page-format.md` holds the formats for all three kinds of fishing note; read it first.

## Report (the default)

1. **Scope.** One question per note, taken from the request. Ask only when the water or the season is missing.
   - Before researching, read what the vault already holds: the [[Fly Fishing]] hub, the pages for this water, species and technique, and the angler's trip notes on the water.
   - The angler's trip notes name what they are working to improve.
   - The research aims at those gaps first.
2. **Research.** Split the reading across parallel subagents, one per angle. Typical angles are fish behaviour and holding water; presentation and line systems; and flies plus local practitioner knowledge. Each writes its findings to a scratchpad file, not prose. Brief each one with:
   - The angler's gaps and the facts of their recent trips on the water.
   - **Sources:** books, guide and shop articles, guide videos (a YouTube transcript tool, if the agent has one, reads their transcripts), forums, magazines, and science on fish behaviour. Technique does not age: date old sources, don't discount them. Run timing and conditions need current sources.
   - **Corroboration:** two or more independent sources for each key piece of advice. A claim resting on one is marked `single source`, and disagreements are kept.
   - **Specifics over generalities:** tip weights and lengths, sink rates, leader length and strength, fly patterns and sizes, water speed and depth, where to stand.
   - **Exclusions:** no regulations, forecasts, fees, passes or management news.
3. **Write the note** in the research-note format:
   - Save it as `Notes/YYYY-MM-DD <Question>.md` with `type: research`, `domain: fishing`, `written_by: claude`, and `related:` listing the pages it feeds.
   - Every section must give the angler something to do differently on the water, and length follows the useful content.
4. **Feed the wiki.** Rewrite the advice sections of the fish, technique and water pages the findings support, in the wiki-page format, citing the note inline.
   - Add Try next items where the research speaks to one of the angler's gaps.
   - Create a page only when the findings give it real content, and add new pages to the [[Fly Fishing]] hub.
   - Propose the changes and write them on the angler's approval, or straight away if they have already said to.
5. **Reply** with:
   - the note's path;
   - the pages touched;
   - the three or four findings most likely to change what the angler does;
   - where sources disagree.

Always:
- **Regulations stay out of notes.** A water page carries a Before you go line of links. When the angler says they are going fishing, check the rules and conditions live and answer in chat. When a gear rule on that water forbids a recommended technique, add one clause saying so.
- **The angler's own practices never count against a water.** A rule that asks only for what the angler already does, such as catch-and-release or fishing one fly, is not a mark against it.
- Surface conflicts between sources rather than smoothing them over.
- Don't repeat marketing superlatives as fact.

## Deep survey (only when the angler asks)

A multi-water regional survey or a species literature review. `/fishing-research-report deep <subject>, <window>` runs the full pipeline:
- a plan-approval gate;
- parallel research subagents, one per angle;
- a verification subagent that checks primary sources;
- a template synthesis;
- a self-critique pass;
- an Artifact for reading on a phone.

The pipeline's standard is `references/quality-bar.md`, with `references/fishery-survey-template.md` or `references/species-profile-template.md`. A deep survey still ends with step 4 above.

For a **British Columbia** survey that needs coordinates, gravel-road access, or maps, read `references/bc-geodata-toolkit.md` first. `scripts/build_map.py` is a seed script: copy it to the scratchpad and edit the bounding box and points for each sub-region. It has been used on one report so far. Offer it; don't force it.

## Bundled files

- `references/wiki-page-format.md`: the trip, wiki-page, and research-note formats. Read for every report, deep or not.
- `references/quality-bar.md`: the depth and verification standard.
- `references/fishery-survey-template.md` and `references/species-profile-template.md`: report structures and research angles.
- `references/researcher-brief.md` and `references/verifier-brief.md`: briefs for the research and verification subagents.
- `references/bc-geodata-toolkit.md` and `scripts/build_map.py`: optional, BC only.
