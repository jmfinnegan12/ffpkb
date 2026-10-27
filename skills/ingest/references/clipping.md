# Web clipping

Extra steps when the source is someone else's article saved from the web — usually by the Obsidian Web Clipper. A filed clipping carries `clipping: true`, `source:` (the URL) and `written_by: <angler>`.

A clipping is a raw source: the author's words, kept as saved. Never trim, summarise or reformat its body; it is held to the same rule as the angler's own notes.

## Before the review table

- **Frontmatter.** Keep what the clipper set; add only missing keys. `clipping: true` and `source:` must both be present — if the URL is missing, find it from the text (title, author, site) and say so in the row.
- **Filename.** The article's title, without the site-name suffix the clipper sometimes adds.
- **Duplicates.** Grep `Notes/` for the same `source:` URL. A second copy of an article already filed is merged into the first, not promoted.

## In the review table

The clipping's own row needs no detail unless something is off (a missing URL, a duplicate). Its Update pages rows propose what the article supports, contradicts or refines on existing pages — worded so the evidence is one outside article, with the author named — and any concept it introduces that deserves its own page. Batch every clipping from one run into the same table.

## On apply

Page lines drawn from a clipping cite both the clipping note and its URL, e.g. `… ([[Reading Riffles in Low Water]], [example.com](https://example.com/reading-riffles))`.
