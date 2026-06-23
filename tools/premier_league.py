"""
English Premier League tool.

Serves the 20 clubs of the current Premier League season (ordered by final
league position) with each club's home city, stadium, points, official website
and social handles. Like the hospitals and colleges tools, it serves a curated,
versioned snapshot from ``premier_league_data.py`` because the official Premier
League site is JavaScript-rendered. Refresh the snapshot each season by editing
premier_league_data.py.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import premier_league_data as DATA

SOCIAL_FIELDS = [
    ("twitter", "X / Twitter"),
    ("instagram", "Instagram"),
    ("facebook", "Facebook"),
    ("youtube", "YouTube"),
]

INFO = {
    "label": "Premier League - Clubs",
    "edition": DATA.PL_EDITION,
    "url": DATA.PL_SOURCE_URL,
    "note": "Clubs ordered by final league position for the season.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from premierleague.com. The page is
    JavaScript-rendered, so a server-side fetch returns no usable club rows ->
    we return None and fall back to the cached snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.PL_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        # The club list is not present in the static HTML; nothing reliable to
        # parse. Returning None keeps the trustworthy cached snapshot.
        return None
    except Exception:
        return None


def get_clubs(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.PREMIER_LEAGUE_CLUBS:
        website = _clean(r.get("website"))
        item = {
            "position": r.get("position"),
            "club": _clean(r.get("club")),
            "city": _clean(r.get("city")),
            "stadium": _clean(r.get("stadium")),
            "points": r.get("points"),
            "website": website,
            "website_display": _display(website),
        }
        for field, _label in SOCIAL_FIELDS:
            item[field] = _clean(r.get(field))
        item["wikipedia"] = _clean(r.get("wikipedia"))
        rows.append(item)

    meta = {
        "label": INFO["label"],
        "edition": INFO["edition"],
        "url": INFO["url"],
        "note": INFO["note"],
        "count": len(rows),
        "social_fields": SOCIAL_FIELDS,
        "live": is_live,
        "live_attempted": bool(live),
    }
    return rows, meta


def columns():
    cols = [("Position", "position"), ("Club", "club"), ("City", "city"),
            ("Stadium", "stadium"), ("Points", "points"), ("Website", "website")]
    for field, label in SOCIAL_FIELDS:
        cols.append((label, field))
    cols.append(("Wikipedia", "wikipedia"))
    return cols


def to_csv(rows) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    cols = columns()
    writer.writerow([label for label, _key in cols])
    for r in rows:
        writer.writerow([r.get(key, "") for _label, key in cols])
    return buf.getvalue()
