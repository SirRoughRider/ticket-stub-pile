#!/usr/bin/env python3
"""Stub Pile build — regenerate every derived file from the private master.

    python3 build/build.py                # build everything
    python3 build/build.py --check        # verify derived files are current (CI / pre-commit)
    python3 build/build.py --master PATH  # master JSON somewhere other than ./stub-pile-data.json

Inputs
  stub-pile-data.json          PRIVATE master. Single source of truth. Never committed.
  build/stub-pile.html.tmpl    tracker page template  (__DATA_JSON__ etc. are filled in)
  build/stub-pile.jsx.tmpl     React tracker template (__SHOWS_BLOCK__ etc.)
  build/stubs.png              masthead illustration embedded in the .docx export

Private outputs (beside the master; never committed)
  stub-pile.html               tracker with ALL data baked in (phone / offline copy)
  stub-pile.jsx                React version, same data
  stub-pile-shows.jsx          SHOWS array only

Public outputs (safe to commit / publish)
  public/concert-history.json  attended + missed shows only, companions stripped
  public/concert-history.csv   same rows, flat
  public/concert-history.md    same rows, grouped by year, human-readable
  docs/index.html              tracker page baked with the PUBLIC data (GitHub Pages)

Privacy rules applied to the public set (see README):
  * status must be "attended" or "missed" — no tickets / wishlist / anything dated in the future
  * companions, seat, link, id are dropped
  * notes are scanned for every companion name that appears anywhere in the master;
    a hit aborts the build so a name never slips out through prose
"""
import argparse, base64, csv, io, json, os, re, sys
from datetime import date
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PUBLIC_STATUSES = {"attended", "missed"}
PUBLIC_FIELDS = ["date", "band", "support", "tour", "venue", "city", "status", "tags", "rating", "notes", "question"]
SHOWS_KEYS = ["band", "date", "companions", "tags", "venue", "city", "tour", "support", "notes", "question", "status"]
ALL_FIELDS = ["band", "support", "tour", "venue", "city", "date", "status", "seat",
              "companions", "tags", "rating", "link", "notes", "question", "id"]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s, outputs, check):
    """Write s to p, or in --check mode just record whether p is already identical."""
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    current = read(p) if os.path.exists(p) else None
    outputs.append((p, current == s))
    if not check:
        with open(p, "w", encoding="utf-8") as f:
            f.write(s)


def js_str(v):
    return json.dumps("" if v is None else str(v), ensure_ascii=False)


def split_list(s):
    # same rule as the app: split on commas, but not commas inside parentheses
    return [t.strip() for t in re.split(r",(?![^(]*\))", str(s or "")) if t.strip()]


def seed_id(band, d):
    return "seed-" + re.sub(r"[^a-z]", "", band.lower())[:10] + "-" + d


def normalise(items):
    """Fill every field, give every row an id, sort newest first."""
    out = []
    for it in items:
        row = {k: it.get(k, 0 if k == "rating" else "") for k in ALL_FIELDS}
        row["rating"] = int(row["rating"] or 0)
        if not row["id"]:
            row["id"] = seed_id(row["band"], row["date"])
        out.append(row)
    out.sort(key=lambda r: (r["date"], r["band"]), reverse=True)
    return out


def shows_block(items):
    """The SHOWS array in the same shape the app's 'Source .jsx' export produces."""
    objs = []
    for r in items:
        lines = []
        for k in SHOWS_KEYS:
            v = r.get(k, "")
            if v in ("", None):
                continue
            if k == "status" and v == "attended":
                continue
            lines.append("    " + k + ": " + js_str(v) + ",")
        objs.append("  {\n" + "\n".join(lines) + "\n  },")
    return "const SHOWS = [\n" + "\n".join(objs) + "\n];\n"


def public_rows(items, today):
    names = set()
    for r in items:
        for p in split_list(r["companions"]):
            names.add(p)
    leaks = []
    rows = []
    for r in items:
        if r["status"] not in PUBLIC_STATUSES:
            continue
        if r["date"] and r["date"] > today:
            continue
        pub = {k: r[k] for k in PUBLIC_FIELDS}
        text = " ".join(str(pub.get(k, "")) for k in ("notes", "question", "tour", "support"))
        for n in sorted(names):
            if re.search(r"\b" + re.escape(n) + r"\b", text):
                leaks.append((r["band"], r["date"], n))
        rows.append(pub)
    return rows, leaks, names


def public_md(rows, today):
    by_year = {}
    for r in rows:
        by_year.setdefault(r["date"][:4] or "Undated", []).append(r)
    out = ["# Concert history", "",
           f"{len(rows)} shows, {len({r['band'] for r in rows})} artists. "
           f"Generated {today} from the private master — see the README for what is and isn't published here.", ""]
    for y in sorted(by_year, key=lambda k: (k != "Undated", k), reverse=True):
        out.append(f"## {y}")
        out.append("")
        for r in by_year[y]:
            d = r["date"].split("-")
            when = f"{MONTHS[int(d[1]) - 1]} {int(d[2])}" if len(d) == 3 else "date unknown"
            line = f"- **{when}** — **{r['band']}**"
            place = " · ".join(x for x in (r["venue"], r["city"]) if x)
            if place:
                line += f" — {place}"
            if r["tour"]:
                line += f" _({r['tour']})_"
            if r["status"] == "missed":
                line += " — *missed*"
            out.append(line)
            if r["support"]:
                out.append(f"  - with {r['support']}")
            if r["notes"]:
                out.append(f"  - {r['notes']}")
        out.append("")
    return "\n".join(out)


def public_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=PUBLIC_FIELDS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default=os.path.join(ROOT, "stub-pile-data.json"))
    ap.add_argument("--check", action="store_true", help="fail if any derived file is stale")
    ap.add_argument("--today", default=date.today().isoformat())
    a = ap.parse_args()

    master = json.loads(read(a.master))
    items = normalise(master["items"])
    exported = master.get("exported", a.today)
    count = len(items)
    data_json = json.dumps(items, indent=2, ensure_ascii=False)

    png_path = os.path.join(HERE, "stubs.png")
    png_b64 = base64.b64encode(open(png_path, "rb").read()).decode() if os.path.exists(png_path) else ""

    html_t = read(os.path.join(HERE, "stub-pile.html.tmpl"))
    jsx_t = read(os.path.join(HERE, "stub-pile.jsx.tmpl"))

    def fill(t, rows_json, n, ex, public=False):
        return (t.replace("__DATA_JSON__", rows_json)
                 .replace("__PUBLIC__", "true" if public else "false")
                 .replace("__COUNT__", str(n))
                 .replace("__EXPORTED__", ex))

    outputs = []
    # ---- private, full-data outputs
    write(os.path.join(ROOT, "stub-pile.html"), fill(html_t, data_json, count, exported), outputs, a.check)
    jsx = (jsx_t.replace("__SHOWS_BLOCK__", shows_block(items).rstrip("\n"))
                .replace("__COUNT__", str(count))
                .replace("__EXPORTED__", exported)
                .replace("__STACK_PNG_B64__", png_b64))
    write(os.path.join(ROOT, "stub-pile.jsx"), jsx, outputs, a.check)
    write(os.path.join(ROOT, "stub-pile-shows.jsx"), shows_block(items), outputs, a.check)

    # ---- public outputs
    rows, leaks, names = public_rows(items, a.today)
    if leaks:
        print("REFUSING to build public files — a companion's name appears in public text:", file=sys.stderr)
        for band, d, n in leaks:
            print(f"  {band} {d}: '{n}'", file=sys.stderr)
        print("Reword the note in stub-pile-data.json (or remove the name) and rebuild.", file=sys.stderr)
        sys.exit(2)
    pub_json = json.dumps({"generated": a.today, "count": len(rows), "items": rows}, indent=2, ensure_ascii=False) + "\n"
    write(os.path.join(ROOT, "public", "concert-history.json"), pub_json, outputs, a.check)
    write(os.path.join(ROOT, "public", "concert-history.csv"), public_csv(rows), outputs, a.check)
    write(os.path.join(ROOT, "public", "concert-history.md"), public_md(rows, a.today) + "\n", outputs, a.check)
    pub_items = [{**{k: "" for k in ALL_FIELDS}, "rating": 0, **r, "id": seed_id(r["band"], r["date"])} for r in rows]
    write(os.path.join(ROOT, "docs", "index.html"),
          fill(html_t, json.dumps(pub_items, indent=2, ensure_ascii=False), len(rows), a.today, public=True), outputs, a.check)

    # ---- report
    st = Counter(r["status"] for r in items)
    print(f"master: {count} shows  ({', '.join(f'{k} {v}' for k, v in sorted(st.items()))})  exported {exported}")
    print(f"public: {len(rows)} shows  (companion names screened: {len(names)})")
    stale = [p for p, ok in outputs if not ok]
    for p, ok in outputs:
        print(("  ok     " if ok else ("  STALE  " if a.check else "  wrote  ")) + os.path.relpath(p, ROOT))
    if a.check and stale:
        print(f"{len(stale)} derived file(s) out of date — run build/build.py", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
