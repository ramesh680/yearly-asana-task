"""
English Premier League tool.

Live mode: the participating clubs are scraped from the current Premier League
season's Wikipedia page (PL_SOURCE_URL). Clubs in a relegation position (their
"Qualification or relegation" cell mentions relegation) are EXCLUDED, so the
table always reflects the up-to-date, non-relegated side of the league table.
The result is cached briefly. If the live page can't be fetched or hasn't been
populated yet (e.g. clubs still listed as "TBD"), the tool falls back to the
baked snapshot in ``premier_league_data.py``.

Update behaviour: because it reads the live Wikipedia table on each refresh
(subject to a short cache), any change to that table - the confirmed line-up in
August, or relegations at season's end - is picked up automatically.
"""
from __future__ import annotations

import time
import csv
import io
from html.parser import HTMLParser

try:
    import requests
except Exception:
    requests = None

from . import premier_league_data as DATA
from . import socials

SOCIAL_FIELDS = socials.SOCIAL_FIELDS

SOURCE_URL = "https://en.wikipedia.org/wiki/2026%E2%80%9327_Premier_League"

INFO = {
    "label": "Premier League - Clubs",
    "edition": "2026/27 (live)",
    "url": SOURCE_URL,
    "note": "Live from the season's Wikipedia table; relegated clubs are excluded. Falls back to the cached snapshot if the live table isn't available yet.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (yearly-asana-task; +https://yearly-asana-task.onrender.com)"}
_CACHE = {"rows": None, "ts": 0.0, "live": False}
_CACHE_TTL = 6 * 3600  # 6 hours

# Per-club metadata (website + social + Wikipedia), keyed by normalised club name.
# Used to enrich whatever clubs the live table currently lists. Unknown clubs
# fall back to auto-generated socials and a derived Wikipedia link.
def _norm(name):
    return "".join(ch for ch in (name or "").lower() if ch.isalnum())

_CLUB_META = {}
for _c in DATA.PREMIER_LEAGUE_CLUBS:
    _CLUB_META[_norm(_c["club"])] = _c


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


# ---------------------------------------------------------------- HTML parsing
class _Tables(HTMLParser):
    """Collect every <table> as a list of rows; each row is a list of cell texts."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self._t = None
        self._row = None
        self._cell = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._t = []
        elif tag == "tr" and self._t is not None:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "table" and self._t is not None:
            self.tables.append(self._t); self._t = None
        elif tag == "tr" and self._row is not None:
            self._t.append(self._row); self._row = None
        elif tag in ("td", "th") and self._cell:
            self._row.append("".join(self._buf).strip()); self._cell = False; self._buf = []

    def handle_data(self, data):
        if self._cell:
            self._buf.append(data)


def _strip_refs(s):
    import re
    s = re.sub(r"\[[^\]]*\]", "", s or "")        # footnotes like [a]
    s = re.sub(r"\([CRTBD ]+\)\s*$", "", s.strip())  # trailing (C)/(R) markers
    return s.strip()


def _parse_clubs(html):
    """Return (ordered_clubs, relegated_set) from the season page HTML."""
    p = _Tables(); p.feed(html)
    teams = []          # club names from the Teams table (with stadium/location)
    standings = []      # (club, qualification_text) from the league table
    for tbl in p.tables:
        if not tbl:
            continue
        header = [h.strip().lower() for h in tbl[0]]
        # Teams table: has "team" and "stadium"
        if "team" in header and any("stadium" in h for h in header):
            ti = header.index("team")
            li = next((k for k, h in enumerate(header) if "location" in h), None)
            si = next((k for k, h in enumerate(header) if "stadium" in h), None)
            for row in tbl[1:]:
                if len(row) <= ti:
                    continue
                club = _strip_refs(row[ti])
                if not club or club.upper() == "TBD":
                    continue
                teams.append({
                    "club": club,
                    "location": _strip_refs(row[li]) if li is not None and len(row) > li else "",
                    "stadium": _strip_refs(row[si]) if si is not None and len(row) > si else "",
                })
        # Standings table: has "pos" and "pts" and a qualification column
        elif ("pos" in header or "pos." in header) and any(h == "pts" for h in header):
            qi = next((k for k, h in enumerate(header) if "qualification" in h or "relegation" in h), len(tbl[0]) - 1)
            ti2 = next((k for k, h in enumerate(header) if h == "team"), 1)
            for row in tbl[1:]:
                if len(row) <= ti2:
                    continue
                club = _strip_refs(row[ti2])
                qual = row[qi] if len(row) > qi else ""
                if club and club.upper() != "TBD":
                    standings.append((club, qual))
    return teams, standings


def _fetch_live():
    if requests is None:
        return None
    try:
        resp = requests.get(SOURCE_URL, headers=_HEADERS, timeout=15)
        if resp.status_code != 200 or len(resp.text) < 2000:
            return None
        teams, standings = _parse_clubs(resp.text)
        # determine relegated clubs from the standings qualification column
        relegated = {_norm(c) for c, q in standings if "relegat" in (q or "").lower()}
        # order: prefer standings order, fall back to teams-table order
        order = [c for c, _q in standings] or [t["club"] for t in teams]
        team_by_norm = {_norm(t["club"]): t for t in teams}
        seen = set(); clubs = []
        for name in order:
            n = _norm(name)
            if not n or n in seen or n in relegated:
                continue
            seen.add(n)
            clubs.append(team_by_norm.get(n, {"club": _strip_refs(name), "location": "", "stadium": ""}))
        # also include any teams-table clubs missing from standings (and not relegated)
        for t in teams:
            n = _norm(t["club"])
            if n and n not in seen and n not in relegated:
                seen.add(n); clubs.append(t)
        if len(clubs) < 15:        # not populated yet -> use snapshot
            return None
        return _build_rows(clubs, live=True)
    except Exception:
        return None


def _enrich(club_name, location, stadium):
    meta = _CLUB_META.get(_norm(club_name), {})
    item = {
        "club": club_name,
        "city": location or meta.get("city", ""),
        "stadium": stadium or meta.get("stadium", ""),
        "points": "",
        "website": meta.get("website", ""),
        "twitter": meta.get("twitter", ""),
        "instagram": meta.get("instagram", ""),
        "facebook": meta.get("facebook", ""),
        "youtube": meta.get("youtube", ""),
        "wikipedia": meta.get("wikipedia", "")
            or ("https://en.wikipedia.org/wiki/" + club_name.replace(" ", "_") + "_F.C."),
    }
    socials.fill(item, club_name)
    item["website_display"] = _display(item["website"])
    return item


def _build_rows(clubs, live):
    rows = []
    for i, c in enumerate(clubs, 1):
        item = _enrich(c.get("club", ""), c.get("location", ""), c.get("stadium", ""))
        item["position"] = i
        rows.append(item)
    return rows


def _snapshot_rows():
    rows = []
    for r in DATA.PREMIER_LEAGUE_CLUBS:
        item = {k: r.get(k, "") for k in ("position", "club", "city", "stadium", "points",
                                          "website", "twitter", "instagram", "facebook", "youtube", "wikipedia")}
        socials.fill(item, item.get("club"))
        item["website_display"] = _display(item.get("website"))
        rows.append(item)
    return rows


def get_clubs(live: bool = False):
    """Return (rows, meta). Always tries the live Wikipedia table (cached for a
    few hours), excludes relegated clubs, and falls back to the baked snapshot.
    Passing live=True forces a fresh refresh, bypassing the cache."""
    now = time.time()
    use_live = False
    rows = None
    fresh = _CACHE["rows"] is not None and (now - _CACHE["ts"]) < _CACHE_TTL
    if fresh and not live:
        rows = _CACHE["rows"]; use_live = _CACHE["live"]
    else:
        fetched = _fetch_live()
        if fetched:
            rows = fetched; use_live = True
            _CACHE.update(rows=rows, ts=now, live=True)
        elif fresh:
            rows = _CACHE["rows"]; use_live = _CACHE["live"]
    if rows is None:
        rows = _snapshot_rows(); use_live = False
    meta = {
        "label": INFO["label"], "edition": INFO["edition"], "url": INFO["url"], "note": INFO["note"],
        "count": len(rows), "social_fields": SOCIAL_FIELDS,
        "live": use_live, "live_attempted": bool(live),
    }
    return rows, meta


def columns():
    cols = [("Position", "position"), ("Club", "club"), ("City", "city"),
            ("Stadium", "stadium"), ("Points", "points"), ("Website", "website")]
    for f, l in SOCIAL_FIELDS:
        cols.append((l, f))
    cols.append(("Wikipedia", "wikipedia"))
    return cols


def to_csv(rows):
    buf = io.StringIO(); w = csv.writer(buf); cols = columns()
    w.writerow([l for l, _k in cols])
    for r in rows:
        w.writerow([r.get(k, "") for _l, k in cols])
    return buf.getvalue()
