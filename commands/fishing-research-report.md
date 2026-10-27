---
description: Fly-fishing research. By default, an in-depth, cited research note on how to catch fish on one water, species, or technique (holding water, behaviour, flies, presentation, reading water), then the fish, technique, and water pages it supports. `deep` runs the full multi-agent regional survey. Invoke as `/fishing-research-report <water-or-species>, <season>` or `/fishing-research-report deep <region-or-species>, <window>`.
---

# Fishing Research Report

`$ARGUMENTS` names the subject and the season. If it does not start with `deep`, write a **report**: invoke the `fishing-research` skill and follow its "Report" steps. That means:
- no plan-approval gate;
- parallel research subagents by angle, aimed at the gaps the angler's trip notes name;
- technique sources of any age, and two or more for each key piece of advice;
- no regulation detail, only links;
- at the end, the wiki pages' advice sections rewritten, on approval.

The rest of this file is the **deep survey** and runs only for `deep`, or when the angler asks for a deep survey in words.

## Deep survey

Orchestrate a deep fishing research report to the `fishing-research` skill's quality bar. You are the orchestrator (main session); the heavy research runs in parallel subagents so it goes deep without flooding this context.

**Read first:** `.claude/skills/fishing-research/references/quality-bar.md`, and whichever template applies (below). The bar is non-negotiable — depth over scan, source-type tags, recency flags, primary-source verification, technique-vs-gear-rule checks, conflicts surfaced.

`$ARGUMENTS` names the subject and window/focus (e.g. `Idaho panhandle, late July / early August` or `coho salmon, Puget Sound + Olympic Peninsula`). If empty, ask.

## Phase 1 — Intake

Infer from `$ARGUMENTS`:
- **Report type:** regional `fishery-survey` (a place) vs `species-profile` (a species). If ambiguous, ask.
- **Subject** (region or species) and **window** (season) and/or **regional focus** (for species reports).

Ask only for what's missing or genuinely ambiguous — access tiers of interest, must-hit waters or questions, regional focus for a species report. Don't over-interview.

## Phase 2 — Research plan → APPROVAL GATE

Load the matching template (`.claude/skills/fishing-research/references/fishery-survey-template.md` or `species-profile-template.md`) and propose a plan:
- Scope and the specific **research angles** (from the template), with what each will cover.
- The specific waters / subtopics each angle will investigate.
- The source targets each angle must hit (agency/primary, peer-reviewed, forums/social, guides).
- The report outline.

**Then STOP and get the angler's approval. Do not dispatch any research until they sign off.** Revise the plan if they change scope.

If the subject is a **British Columbia** region, mention the optional geodata/maps track (`references/bc-geodata-toolkit.md` + `scripts/build_map.py`) as part of the plan — ask whether they want coordinates/access-detail/per-sub-region maps this time, rather than assuming either way.

## Phase 3 — Parallel deep research

After approval, spawn **one subagent per research angle, in parallel** (multiple Task calls in a single message):
- `subagent_type: general-purpose`, `model: opus`
- Each subagent prompt: (1) instruct it to **read `.claude/skills/fishing-research/references/researcher-brief.md` and `.claude/skills/fishing-research/references/quality-bar.md` first**, then (2) give it its ONE angle, the subject, and the window/focus, and (3) tell it to return the structured findings block the brief specifies (claims · links · source-type tags · dates · confidence · conflicts · check-worthy-claims list · gaps).

Wait for all angle subagents to return.

## Phase 4 — Verification pass

Collect the **check-worthy claims** the researchers flagged (regs, licences, gear rules, closures, size/retention, status, population, superlatives, and any recommended techniques). Spawn a verification subagent (`general-purpose`, `opus`) instructed to **read `.claude/skills/fishing-research/references/verifier-brief.md` first**, then verify each claim against a primary source and run the gear-rule↔technique check. Drop or tag `unverified` anything it can't confirm; apply its corrections; treat blocking contradictions as must-fix.

## Phase 5 — Synthesize

Assemble the verified findings into the template's structure. General context up front (so seasonal/technique/reg material isn't repeated per water); then the tiered/section body; then the comparison table (fishery-survey) or comparative section (species-profile); then "Sources & data-quality notes."

## Phase 6 — Self-critique / contradiction pass

Apply `quality-bar.md` §8 to the assembled draft: hunt internal contradictions (**deliberately re-check every recommended technique against the stated regs**), unsupported claims, missing source-type tags, unflagged dated sources, marketing leakage, and any framing creep against the angler's own practices, such as catch-and-release, in a verdict (§6). Fix all before filing.

## Phase 7 — Save

Write the report to `Notes/YYYY-MM-DD <Descriptive Title>.md` with frontmatter `type: research`, `domain: fishing`, `written_by: claude`, and `created:` set to today. Fill `related:` with wikilinks to the waters, species, and techniques covered — unresolved links are wanted, they mark the reference notes worth writing next. `Notes/` is flat; do not create a folder for the report.

Then, if the agent can publish a Claude Artifact, publish the report as one so it is readable on a phone without Obsidian, and put the URL on an `artifact:` line in the frontmatter.

Then propose the wiki updates, following the skill's "Feed the wiki" step. End your reply to the angler with the file path, the artifact URL, and the **flagged-uncertainties list** (conflicts + anything left `unverified`) so they know what to trust.

## Notes

- Don't skip the approval gate, and don't let a subagent's single source stand in for verification.
- If the verification pass surfaces that the bar didn't hold (thin sourcing, contradictions), fix and re-verify rather than filing a scan.
