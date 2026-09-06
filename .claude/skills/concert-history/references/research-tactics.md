# Research tactics

Read this when a show isn't turning up with a straightforward date search.

## Contents
- Sources, ranked
- Query patterns
- Disambiguation
- Venue name changes
- Festivals and package tours
- Comedy and non-music shows
- Upcoming shows
- When to stop

## Sources, ranked

1. **Setlist archives** — indexed by band and date, usually with the full bill. Best first stop for anything from roughly 2005 onward.
2. **Concert archive sites** — broader coverage of small venues, often where setlist sites have gaps.
3. **The band's own tour archive** — some bands keep meticulous per-show records including live debuts and rarities. When available, the richest source of the detail that makes a night specific.
4. **Venue calendars and event listings** — good for upcoming shows and for confirming a venue existed and was booking on a given date.
5. **Local music press** — reviews and photo galleries pin down attendance, weather, technical failures, crowd size. Often the only source for a memorable incident.
6. **Tour announcement press releases** — full routing at announcement time. Routings change: treat an announced date as provisional and confirm against a source that records what actually happened.

## Query patterns

Most specific first:

```
<band> <month> <day> <year> setlist
<band> <month> <day> <year> setlist venue
<band> <year> <city> setlist
<band> <tour name> <city> date
"<venue>" "<month> <day>, <year>" concert
<band> tour dates <year> list <state>
```

Quoting the exact date string helps on venue-anchored searches. If a tour list is truncated in a snippet, fetch the page — routings are usually complete there.

## Disambiguation

**Multiple cities in one week.** Compare against the home metro. Alone, a longer drive is plausible; with companions, closer is likelier.

**Two shows in one city on one tour.** Distinguish by support act, venue, or day of week.

**Two shows in one day.** Matinee and evening performances are common for holiday and family tours. Ask which.

**A band with a common word for a name.** Add genre or a bandmate's name to the query.

**Support versus headliner.** If a set ran notably short, they were supporting. Search the venue and date to find who closed.

## Venue name changes

Confirm the venue existed under that name on that date. Common traps:

- A room named by its *current* name for a show that predates the renaming
- A venue closed entirely on that date and reopened later
- Two venues in one metro with similar names, one downtown and one in a suburb
- A suburb name that sounds like a venue name

Record the name in use at the time and mention the continuity — people often don't realise two entries in their own log are the same building. The tracker's venue registry does the grouping; add a line to it when a building gets a new name.

## Festivals and package tours

- Identify which stage the band played; side-stage sets typically run about half an hour
- Put the headliners in `support`, since a single entry hides a whole day of bands
- Ask whether notable acts on the bill should also go in `tags`, so they're searchable
- Radio-station one-offs are poorly documented; the station's own archive or local press may be the only record

## Comedy and non-music shows

Setlist archives rarely cover comedians, podcasters, or culinary tours. Use instead:

- The performer's own tour archive or press page (often lists past dates by year)
- The club's or theater's past-events page, or its social media around the remembered month
- Local press and alt-weeklies ("<comedian> <city> <year> review")
- For a podcast or radio show taped live, the episode archive: the taping city is usually in the episode title or notes, which pins the date exactly
- Ticketing-site event pages linger for years and often survive as search snippets with the date in them

Comedy clubs book the same act many times; a name plus a city may match six dates across a decade. Ask for anything that narrows it — the year, the season, who else was on, what the person was doing in life then — before listing candidates.

When the person can't name the act ("a one-liner comedian"), offer three or four candidates who fit the description and played that room, with the years they did, and let them pick. Don't record a guess as the band.

## Upcoming shows

Verify against the venue's own listing plus one ticketing source. Confirm date, day of week, and time agree. Record the venue's own billing as the tour/event name. Note doors/showtime in `notes`; they're useful on the night and harmless afterwards.

## When to stop

Stop and ask for a detail when:

- Three or four differently-phrased searches return nothing for the date
- The venue is a small club and the date is a weeknight before about 2012
- The event was a local radio promotion

One good detail from the person — a support act, a venue, who they went with, a song — is worth more than five more searches. Ask for the most discriminating one, not "any more info?"

Say plainly which sources were checked and came up empty. That makes the gap real rather than a lack of effort, and stops the same ground being covered again.
