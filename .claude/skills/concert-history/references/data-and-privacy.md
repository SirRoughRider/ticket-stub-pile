# Data model, privacy rules, and the build

Read this before adding, editing, or publishing anything.

## Contents
- The files
- Record schema
- Status values
- Privacy contract
- Build and check
- Working without the repo

## The files

```
stub-pile-data.json        PRIVATE master — the only file you edit by hand. Git-ignored.
stub-pile.html             PRIVATE tracker, all data baked in. Git-ignored. Generated.
stub-pile.jsx              PRIVATE React tracker. Git-ignored. Generated.
stub-pile-shows.jsx        PRIVATE SHOWS array only. Git-ignored. Generated.
public/ticket-stub-pile.json   public rows. Committed. Generated.
public/ticket-stub-pile.csv    same rows, flat. Committed. Generated.
public/ticket-stub-pile.md     same rows by year, readable. Committed. Generated.
docs/index.html            public tracker page for GitHub Pages. Committed. Generated.
build/build.py             the generator. build/*.tmpl are the page templates.
```

"Generated" means: never hand-edit; change the master or the template and rebuild.

## Record schema

One object per show in `items`, newest first. The master file wraps them:

```json
{ "exported": "2026-09-06", "count": 56, "items": [ ... ] }
```

| field | type | notes |
|---|---|---|
| `band` | string | the act the person names — headliner or the opener they came for |
| `support` | string | everyone else on the bill, comma-separated; parentheticals allowed: `Shadows Fall (co-headline)` |
| `tour` | string | tour or event name |
| `venue` | string | the name on the ticket that night, not the current name |
| `city` | string | `City, ST` |
| `date` | string | `YYYY-MM-DD` |
| `status` | string | see below |
| `seat` | string | private |
| `companions` | string | comma-separated names — **the only place a person's name may appear** |
| `tags` | string | comma-separated: genre, `festival`, `acoustic`, `comedy`, `food`, `upcoming` … |
| `rating` | number | 0–5 |
| `link` | string | private |
| `notes` | string | published — the detail that makes the night specific |
| `question` | string | published — what's still unresolved; drives "Still to find out" |
| `id` | string | `seed-<band10>-<date>`; generated if missing |

Identity is `band` + `date`. Splitting comma lists follows the app's rule: split on commas
that are not inside parentheses.

## Status values

| status | meaning | public? |
|---|---|---|
| `wishlist` | want to go, no ticket | no |
| `tickets` | ticket in hand, night not yet happened | no |
| `attended` | was there | yes |
| `missed` | had a ticket or a plan, didn't go | yes, stamped MISSED |

Rules the app applies: "shows seen" counts `attended`; "ahead" counts `tickets` + `wishlist`;
"got away" counts `missed`; artists / venues / cities / the year bar exclude `missed`.
When a show passes: `tickets` → `attended` or `missed`, and remove the `upcoming` tag.

## Privacy contract

The public set is produced only by `build/build.py`, which:

1. keeps rows whose status is `attended` or `missed` and whose date is not in the future;
2. drops `seat`, `companions`, `link`, `id`;
3. collects every name that appears in any `companions` field in the master and refuses to
   build if any of those names appears in a published field (`notes`, `question`, `tour`,
   `support`) — so a companion cannot leak through prose;
4. bakes `docs/index.html` with `PUBLIC = true`, which hides the solo stat, the who-with filter,
   the "ahead" count, and the "went with" block.

The pre-commit hook and the CI workflow run `build/build.py --check`, which fails if any
committed file is stale relative to the master or if a private filename is staged.

What this does **not** protect: prose that identifies someone without naming them ("went with my
wife"). Keep that kind of phrase out of `notes`; put people in `companions` only.

## Build and check

```
python3 build/build.py            # regenerate everything from the master
python3 build/build.py --check    # exit 1 if anything is stale; exit 2 on a privacy hit
```

Typical change:

1. Edit `stub-pile-data.json` (or import the app's Export → .json as the new master).
2. Bump `exported` to today; the build fixes `count`.
3. `python3 build/build.py` and read the summary line — the counts should match what you expect.
4. Commit. The hook re-runs the check.

If the person edited shows inside the app, their edits are only in that page's memory. Have
them Export → .json and treat that download as the new master before doing anything else.

## Working without the repo

In a plain chat session, the master is whatever JSON the person shares. Return the full
updated JSON (same shape, newest first), state the counts, and tell them to save it as
`stub-pile-data.json` and run the build. Don't produce a public copy by hand — the build is
the only path that applies the privacy contract.
