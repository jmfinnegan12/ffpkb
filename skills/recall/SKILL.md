---
name: recall
description: Answer a question from the vault with what the angler saw or wrote kept separate from what Claude synthesised and from what the vault does not hold, every claim linked to its note
argument-hint: "[domain:<value>] <question>"
---

# /ffpkb:recall

The query step of the wiki loop: read the vault, answer with citations, never blend provenance. Nothing is written.

Question: $ARGUMENTS

## 1. Scope

When the first token is `domain:<value>`, restrict to notes whose frontmatter carries that `domain`. Otherwise search all of `Notes/`, plus `Inbox/` for the angler's raw captures.

## 2. Gather

Grep for the question's terms and their obvious variants (species, water, place, and concept names), then Read each hit far enough to judge it. For a `domain: fishing` question read the [[Fly Fishing]] hub first; it is the index. Record each note's `type`, `written_by`, and `created`, and for a research report the source-type tag and date it attaches to the claim.

## 3. Answer in three lanes, in this order

- **First-hand** — what the angler wrote or said: notes carrying the angler's `written_by`, trip journals, and clippings (`clipping: true`) in their author's own words. A note by the angler with `source:` is advice someone gave the angler: name that source ("the Example River Fly Shop, as the angler recorded it"). Quote or paraphrase closely, with the date.
- **Synthesised** — `written_by: claude` notes and research reports. Each claim carries the report's own source-type tag and date, for example "agency/gov, WDFW, 2026-05", and says when the source left it unverified.
- **Not in the vault** — the parts of the question nothing answers.

Every claim ends with a wikilink to its note. A lane with nothing gets one line saying so. A synthesised claim is never stated as something the angler experienced, and a Claude-written note is never presented as the angler's settled position.

## 4. Offer the next step

First-hand empty: offer `/ffpkb:ingest` for a trip entry or a clipping. Synthesised thin: offer `/ffpkb:fishing-research-report` for a fishing water or species, or a research note otherwise. An answer worth keeping: offer to file it as a `reference` note written by Claude, citing the notes it drew on. Never file it unasked.
