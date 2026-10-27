# ffpkb

A fly fishing personal knowledge base: a [Karpathy-style LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) applied to a fly fishing stream journal, kept in Obsidian and run by an agent (Claude Code). The angler works inside the wiki: reads it, navigates it, and keeps it current with the agent's help.

It is a framework connected to an agent, not software. Nothing is hosted, there is no fee, and no data is collected.

## How it works

Two flows:

- **Adding:** information → agent → knowledge base.
- **Retrieving:** question ↔ agent ↔ knowledge base.

Three kinds of input:

- the angler's own observations, as trip entries;
- secondary knowledge the angler enters, passed on by a guide, fly shop, book, video, article or friend;
- agent research, written up with citations.

Every item names its source. Sources stay as written, and the fish, technique and water pages cite each line as research, a trip, or passed on, keeping the three apart. `written_by` records who composed a note: the angler's own notes (trips, passed-on notes, clippings) carry the angler's name, and pages and research the agent writes carry the agent's name, e.g. `claude`. Regulations are not stored: water pages link the official rules, which are checked live before a trip.

## What is in the repo

- `skills/fishing-research/` researches a water, species or technique and feeds the pages. Its `references/` and `scripts/` hold the note formats, the quality bar, report templates, subagent briefs and an optional British Columbia geodata toolkit.
- `skills/ingest/` files trip entries, passed-on advice and web clippings about fishing, through one review table the angler edits before anything is written.
- `skills/recall/` answers a question from the vault, keeping what the angler saw apart from what the agent synthesised.
- `skills/fishing-research-report/` runs a research report, or a deep multi-agent survey.
- `templates/` holds the trip template, a starter `Fly Fishing` hub and `Fly Fishing.base`.

The repo is a Claude Code plugin and its own marketplace.

## How to use it

1. In the vault, install the plugin at project scope, so it is recorded in the vault's `.claude/settings.json`:
   ```
   claude plugin marketplace add jmfinnegan12/ffpkb --scope project
   claude plugin install ffpkb@ffpkb --scope project
   ```
2. Copy `templates/fishing trip.md` into the vault's `Templates/` folder and replace `<angler>` in it with the angler's name. The trip template uses the Templater plugin.
3. Copy `templates/Fly Fishing.base` into the vault, and create the hub at `Notes/Fly Fishing.md` from `templates/Fly Fishing.md`.
4. Open Claude Code in the vault and run `/ffpkb:ingest`, `/ffpkb:recall` or `/ffpkb:fishing-research-report`.

The tools expect `Inbox/` for raw captures, a flat `Notes/` folder for everything filed, `Templates/`, and the `Fly Fishing` hub in `Notes/`.

## Status

Early prototype. A personal hobby project of Jim Finnegan's, shared to see whether other anglers want it.
