---
name: ingest
description: File new fishing material into the wiki and update every page it bears on — fishing trip entries, advice passed on by a guide, shop, friend, book, video or article, and web clippings about fishing. Writes one review table the angler edits in Obsidian, then applies it as edited.
argument-hint: "[optional: an Inbox note, pasted text, or an image path — default is the fishing notes in Inbox/]"
---

# /ffpkb:ingest

The ingest step of the wiki loop: a source goes in untouched, and the notes around it get updated. `/ffpkb:recall` is the query step. Read `${CLAUDE_PLUGIN_ROOT}/skills/fishing-research/references/wiki-page-format.md` first — it carries the note formats and citation rules this leans on. Every note filed carries `domain: fishing`.

Source: $ARGUMENTS

Filing a note means placing it: links both ways, splits, superseded drafts marked, the pages it teaches something updated. Steps 3 and 4 are the job.

**Two rules hold throughout.**
- **A source is never reworded.** The angler's trip entries, passed-on notes and clippings keep their words; text may be added, moved verbatim to another note, or have a link retargeted, nothing else.
- **Nothing is written, moved or committed until the angler has edited the review table and said it's ready.** The table is the one write allowed before that.

## 1. Gather the sources

- With `$ARGUMENTS`: a filename or match in `Inbox/`, pasted text, or an image path (read and transcribe it). An audio file cannot be read: ask for the transcript and stop.
- Without: every fishing note in `Inbox/*.md`, read in full. Notes about anything else are left where they are. Every fishing source leaves Inbox — promoted, merged, or archived. "Keep in Inbox" is not an action.

Pasted or transcribed text gets written verbatim to `Inbox/` first, as the angler's note, so it has a file to file.

## 2. Sort each source

| Source | How to tell | Extra steps |
| --- | --- | --- |
| Fishing trip entry | A day on the water: a river, flies, fish, flows | `references/fishing-trip.md` |
| Web clipping | `clipping: true`, or a `source:` URL and someone else's article | `references/clipping.md` |
| Passed-on advice | The angler relays what a guide, shop, friend, book, video or article told them | `written_by: <angler>`, plus `source:` naming who said it — ask once if the capture doesn't say. The passed-on note format in `${CLAUDE_PLUGIN_ROOT}/skills/fishing-research/references/wiki-page-format.md` |

**Who wrote it.** Decide from voice (the angler's captures are usually rough notes; agent prose is polished and refers to the angler in the third person) and, if the vault is under git, from history (`git log --format='%ad %s' --date=short -- <file>`; descriptive messages or `Co-authored-by` trailers mean an agent). Never change an existing `written_by`. A restamp the angler approves in the table is a one-line edit they make themselves in Obsidian; list it in the closing report.

## 3. Place each source in the vault

Fan out Explore agents by cluster (a water, a fish, a technique; up to five), each reading its sources in full and grepping `Notes/` and `Inbox/` for titles, key terms and wikilinks in both directions. Spot-check what they return before using it. For each source, settle:

- **Hub.** Which of the [[Fly Fishing]] hub's lists the source or a new page joins.
- **Links.** Specific existing notes for `related:`, and which of them link back. Verify every target exists.
- **Type.** Match how comparable notes are typed; the formats in `wiki-page-format.md` set it for trips and passed-on notes.
- **Atomicity.** Two subjects under one title → name the split. Text duplicated in another note → say which keeps it and link.
- **Chronology.** Draft → rewrite: name the sequence with dates. A superseded draft gets one dated line saying what replaced it.
- **Filename.** Fix spelling and capitalisation; follow the family's naming. Renames must carry inbound links with them: use `obsidian move` where the Obsidian CLI is available, otherwise retarget the links.

## 4. Find what the source teaches

Read the wiki pages the source bears on — `reference`, `research` and `hub` notes the agent wrote — and propose, for each:

- a claim the source **supports, contradicts or refines** — say which, and word it so the evidence's weight is clear (one trip, one article, one tip passed on);
- an **open question** a page carries that the source answers, or a new one it raises;
- a **new page** the source justifies — one subject, a bare name;
- the **hub** gaining the source or a new page.

Propose only what the source gives real evidence for. A source that teaches nothing new gets "no page updates". **Never edit a page the angler wrote to add synthesis** — the proposal is a new agent-written note `<Page> — <subject>`, linked from theirs.

Every line the agent adds to a page **cites its source**, in the citation forms of `wiki-page-format.md`: a wikilink to the source note, or the URL for outside material. Advice passed on to the angler also names who gave it.

## 5. Write the review table, then stop

Write `Inbox/Ingest Review YYYY-MM-DD.md` with `written_by: claude` and `created` in its frontmatter. The angler edits it in Obsidian, so the proposal goes there, not in chat.

It is a five-minute read for the angler, not a report.

- One line on top: move a row to another bucket to change its action, edit a cell to change the detail, then say it's ready. Everything that applies to all promotions (frontmatter, links both ways, filename fixes, citations) is said once there, never per note.
- `##` headings are the action buckets, only those that apply: Promote, Promote and mark what replaced it, Promote and split, Create, Update pages, Archive. Under each, a table with two columns: **Note** (wikilink) and **Important detail**.
- Most detail cells are empty. Fill one only with what the angler needs to approve: a split, an archive reason, a risk. Several notes with no detail can share a row, separated by ` · `.
- **Update pages** is the exception: one row per page, the detail cell saying the change in a few words and the source it comes from, e.g. `supports "fish small flies in low water" — one trip, [[2025-09-14 Example River]]`.
- Every source appears exactly once outside Update pages.

In chat, link the note and give the few cross-cutting findings (recurring questions, missing pages, drift between notes) in plain language. Commit nothing yet.

## 6. Apply the edited table

When the angler says it's ready, re-read the review note and apply it exactly as edited: their cells override the proposal. An ambiguous cell: ask about that row only and apply the rest.

- Frontmatter goes onto a source while it is still in `Inbox/`. Then move it to `Notes/` (`git mv` if the vault is under git). **Archive** means moving the note whole to `Archive/`, unedited, with links left pointing at it; it is the default way to retire a note. Delete only when the angler writes "delete" in a cell, and retarget inbound links first.
- **A split writes the new note first**, with the moved text verbatim, then removes it from the source. Check that the removed text now lives elsewhere.
- Page updates, hubs and split-outs carry `written_by: claude` on creation, follow `wiki-page-format.md`, and cite their source. Back-links go in `related:`.
- Run any extra steps from the source's reference file.
- Delete the review note (`git rm` it if it was already committed).

## 7. Commit, report

If the vault is under git, commit in finished units, staging by name; check `git diff --cached --stat` before each commit so nothing unrelated is swept in. Push if the vault has a remote.

Close with a short report: what moved, what was created, which pages changed, what was archived, any restamp the angler needs to make, and any row that couldn't be applied as written.
