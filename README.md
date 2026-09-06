# Stub Pile — a concert history

*The music we love, and the nights we were there.*

A verified log of live shows, kept two ways:

- **The private record** — every show, who came along, seats, links, and what's coming up.
  It lives only on my computer.
- **The public record** — the shows I've been to (and the odd one I missed), with the people
  and the future stripped out. That's what this repository publishes: browse
  [`public/concert-history.md`](public/concert-history.md), or open the tracker at the
  GitHub Pages site (`docs/index.html`).

The method for researching a half-remembered show — pinning a band and a rough date to a
real night, catching renamed venues and date drift, and logging honestly when it can't be
found — is a Claude skill in [`.claude/skills/concert-history/`](.claude/skills/concert-history/SKILL.md).

## Layout

```
stub-pile-data.json     PRIVATE master (git-ignored). Single source of truth.
build/                  build.py + page templates. Turns the master into everything below.
public/                 concert-history.json / .csv / .md — the public rows. Generated.
docs/index.html         the tracker page, public data only. Generated. Served by GitHub Pages.
.claude/skills/         the concert-history skill (method, schema, privacy contract).
scripts/pre-commit      guard: no private files, no stale outputs, no names in public files.
.github/workflows/      the same guard, run on every push.
```

Files that never enter git: `stub-pile-data.json`, `stub-pile.html`, `stub-pile.jsx`,
`stub-pile-shows.jsx`, and any export the tracker downloads (`.docx`, `.xlsx`, `.csv`).

## What is and isn't published

| published | kept private |
|---|---|
| band, support acts, tour, venue, city, date | who I went with |
| status `attended` or `missed` | shows with tickets or on the wish list |
| tags, rating, notes, open questions | seats, links |

`build/build.py` is the only thing that produces the public files. It drops the private
fields, skips anything with a future date or a pre-show status, and aborts if any name that
appears in a `companions` field turns up in a published field. The pre-commit hook and CI
repeat the check.

## Working on it

```sh
# one-time
ln -sf ../../scripts/pre-commit .git/hooks/pre-commit

# every change
#   1. edit stub-pile-data.json  (or Export → .json from the tracker and replace it)
#   2. rebuild
python3 build/build.py
#   3. commit — the hook re-runs the checks
```

`python3 build/build.py --check` reports whether anything is stale without writing.

Edits made inside the tracker page live only in that page's memory. To keep them, use
**Export → .json** and make that download the new master, then rebuild.

## The tracker

`stub-pile.html` (private) and `docs/index.html` (public) are the same single-file page with
different data baked in: search, filters by status / year / tag / person, sorting, clickable
artist / venue / city breakdowns, a year bar, and a venue registry that groups a building
across its renamings (Gexa Energy Pavilion → Dos Equis Pavilion) while showing the name that
was on the ticket. `stub-pile.jsx` is the same app as a React component with .xlsx / .docx
export.

## Status values

`wishlist` → `tickets` → `attended` or `missed`. Missed shows stay in the log — they're
still bands I want to see — stamped MISSED and left out of the artist / venue counts.

Comedy, culinary and other non-music nights go in the same list with a tag (`comedy`,
`food`, …). It's a log of nights out, not strictly of concerts.
