"""
Saudi Pro League tool.

Serves the 18 clubs of the current Saudi Pro League (Roshn Saudi League) season,
ordered by final league position, with each club's home city, stadium, points,
official website and social handles. Like the other tools, it serves a curated,
versioned snapshot from ``saudi_pro_league_data.py`` because the official Saudi
Pro League site is JavaScript-rendered. Refresh the snapshot each season by
editing saudi_pro_league_data.py.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import saudi_pro_league_data as DATA
from . import socials

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]

INFO = {
    "label": "Saudi Pro League - Clubs",
    "edition": DATA.SPL_EDITION,
    "url": DATA.SPL_SOURCE_URL,
    "note": "Clubs ordered by final league position for the season.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from spl.com.sa. The page is JavaScript-rendered,
    so a server-side fetch returns no usable club rows -> we return None and fall
    back to the cached snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.SPL_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        return None
    except Exception:
        return None


def get_clubs(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.SAUDI_PRO_LEAGUE_CLUBS:
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
        socials.fill(item, item.get("club"))
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
