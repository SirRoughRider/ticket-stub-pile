---
name: concert-history
description: "Build and maintain a verified personal concert history (Stub Pile). Use whenever someone mentions a show they went to or have tickets for, gives a band with a partial date, asks when an act played their city, wants to add/correct/remove a show, or asks to rebuild or publish the tracker. Trigger on 'I saw X in 2016', 'add this concert', 'we didn't make it to X', 'when did X come to town', 'do we have X in the log', 'rebuild the tracker', 'publish my history' — even when no tracker is named."
---

# Concert history

Turn half-remembered nights into a verified, searchable record — and keep the private
record private when it is published.

## Two records, one master

| | Where | Contains | Who sees it |
|---|---|---|---|
| **Private master** | `stub-pile-data.json` in the repo root (git-ignored) | everything: companions, seats, links, upcoming shows | the owner only |
| **Public copy** | `public/` and `docs/` (committed, GitHub Pages) | past shows only, companions stripped | anyone |

The repo is `~/Documents/Concert History/` on the owner's Mac. Every change is made to the
master, then `python3 build/build.py` regenerates all derived files. Never hand-edit a
generated file. `references/data-and-privacy.md` has the schema, the exact privacy rules, and
the build steps; read it before touching data.

Not every session has the repo. In plain chat, work on the JSON the person shares, hand back
the updated JSON, and remind them to drop it in as the master and rebuild.

## Record schema (one object per show)

`band`, `headliner` (only when it wasn't `band`), `support` (comma list; parentheticals allowed), `tour`, `venue` (the name on the
ticket that night), `city` (`City, ST`), `date` (`YYYY-MM-DD`, may be empty if unknown),
`status`, `seat`, `companions` (comma list — **the only field where a person's name may
appear**), `tags` (comma list), `rating` (0–5), `link`, `notes`, `question`, `id`.
Master file: `{ "exported": "YYYY-MM-DD", "count": N, "items": [ ... ] }`, newest first.

Status: `wishlist` → `tickets` → `attended` or `missed`. Only `attended` and `missed` are
published, and only with a date that has passed. Public copies drop `seat`, `companions`,
`link`, `id`.

## The loop

1. **They name a show** — a band plus whatever they remember. If they ask whether a show is already logged, check the master first and answer from it.
2. **Research it** — exact date, venue (under the name it carried that night), tour, full bill.
3. **Report what you found**, including anything that contradicts what they said.
4. **Record it** in the master: add, correct, or change status. Never just describe the result.
5. **Log what's still unknown** as the show's `question`, so it surfaces in "Still to find out".
6. **Rebuild** when the repo is available, and say what the public copy will and won't show.

## Recording rules

- **Identity is band + date.** A band seen five times must not collide. Match on both before adding.
- **Fill blanks, never overwrite.** On an existing entry, only empty fields get research results; anything the person typed stays.
- **Status tells the truth about attendance.** `tickets` → `attended` after the night, or → `missed` if they didn't go. A missed show is kept, not deleted — it is still a band they want to see. Drop the `upcoming` tag when the status changes.
- **Deletions are deliberate.** Only remove a row when asked. Don't re-add a show that was removed.
- **Not-music is fine.** Comedy, culinary, theater, radio tapings and similar nights go in the same log with a descriptive tag (`comedy`, `food`, `musical`, `live taping`); the stats treat every row as a night out.
- **Every row gets its bill.** Research the full lineup for every show, not just the headliner: `headliner` when the person's act didn't close the night, everyone else in `support`, co-headlines tagged `(co-headline)` in `support`. A show with no opener is recorded as such in `notes` ("No opener") so it isn't re-researched. Sweep periodically for rows with an empty `support` and no such note.
- **Names stay in `companions`.** Never write a companion's name into `notes`, `tour`, `support` or `question` — those fields are published. The build refuses to run if one slips through, and "my wife"-style phrasing is just as much a leak.
- **Dates come from the person; corrections come from sources.** When research moves a date, keep the original in a note ("Logged as Aug 31 — the Dallas show was Aug 30").

## Research

**A tour date maps to one venue.** Band + date usually identifies the venue anywhere; start there before asking for a city.

**Establish the home metro early, then use it.** Once two or three shows land in one region, treat it as the default. If a band played three cities that week, the one near home is almost certainly it. Say so the first time.

**Search the specific date, not the tour.** `<band> <month> <day> <year> setlist` beats `<band> <year> tour`. Setlist archives, concert archives, band tour archives, venue calendars and local press all index by date. `references/research-tactics.md` has the sources and query patterns.

**Comedy and non-music acts aren't in setlist archives.** Use the performer's own tour page, the club's past-events page, local press, ticketing pages that linger in search snippets, and — for radio or podcast tapings — the episode archive, where the taping city pins the date. Clubs rebook the same act for years: ask for the year or season before listing candidates. When the person can't name the act, offer three or four who fit the description and played that room; never record a guess as the band.

**Give the whole bill.** Support acts and co-headliners are often what makes a memory click. If they name the opener, log it under the band they named and put the rest in `support`.

**Surface the detail that makes the night specific.** A song's first outing in a decade, a phone-free policy, a guest vocalist, an album played in full. Write it into `notes`.

**Upcoming shows get verified too.** For a ticketed date, confirm date, day of week, time and venue against the venue's own listing plus one ticketing source before recording. Announced routings change.

## Checks that catch real errors

**Verify the weekday.** If they gave a date, check what day it fell on. A matching weekday means the date probably came off a ticket — trust it over a search result that disagrees. Also check the weekday a *source* claims: a page that calls Nov 14, 2026 a Thursday is wrong about something.

**Check the venue existed under that name on that date.** Rooms get renamed and rebuilt. Record the name on the ticket; the venue registry in the tracker groups it with the building's other names. A suburb club remembered as "Dallas" (the Addison Improv, say) gets its real city.

**Watch for systematic date drift.** If several dates are off by a day in the same direction, say so, correct to the documented date, keep the original in a note.

**Don't let a near-match become a confirmation.** Say which parts matched and which didn't, and offer the discriminating question: "if you remember X being there, it's this night."

**A multi-week run needs the night, not the run.** Touring musicals and residencies play a city for weeks. Offer the runs first; the person usually knows which, and often the exact date once they see it.

## When it can't be found

Small club shows, weeknight bookings, radio one-offs and pre-2010 local gigs are often documented nowhere. Say so plainly. Never invent a venue, support act or date; never quietly upgrade a guess to a fact. Say what was ruled out, offer venues that were actually booking that kind of show then, add the row with what's known (an empty `date` is allowed), and attach a `question`. A guess the person asks to record is recorded — with a note that it came from memory.

## Reporting back

Lead with the answer: date, venue, bill. Then anything that contradicts what they said, then the distinctive detail. Keep it short — they asked about one concert.

Once several shows are in, patterns are worth mentioning as they emerge (the band seen most, the busiest year, a room visited under three names, who they go with across a decade). Offer these when they appear, not after every addition.

## Example

**They say:** "We had tickets for Avenged Sevenfold in August but didn't go."

**Good response:** Switched that one to *missed* rather than deleting it — you've only seen them once, opening for Metallica in 2017, so they stay on the still-to-see list. Dropped the *upcoming* tag and noted the last-minute cancellation. In the public copy it shows as a missed show with no one named. Rebuilt: 52 seen, 1 got away, 2 ahead.

**Why it works:** the status change is explained, the privacy consequence is stated, nothing was silently deleted, and the counts confirm the rebuild happened.
