"""
Top Motorsports tool.

Serves the most popular motorsport series and events with each one's discipline,
official website and social handles. Like the other tools, it serves a curated,
versioned snapshot from ``motorsports_data.py``. Refresh the snapshot
periodically by editing motorsports_data.py.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import motorsports_data as DATA

SOCIAL_FIELDS = [
    ("twitter", "X / Twitter"),
    ("instagram", "Instagram"),
    ("youtube", "YouTube"),
]

INFO = {
    "label": "Top Motorsports - Most Popular Series & Events",
    "edition": DATA.MOTORSPORT_EDITION,
    "url": DATA.MOTORSPORT_SOURCE_URL,
    "note": "Ranked by popularity (SportsWave), cross-referenced with Wikipedia's list of motorsport championships.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from the source. Returns None (the source list is
    editorial and the official sites are JavaScript-rendered), so we fall back
    to the cached snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.MOTORSPORT_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        return None
    except Exception:
        return None


def get_motorsports(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.TOP_MOTORSPORTS:
        website = _clean(r.get("website"))
        item = {
            "rank": r.get("rank"),
            "series": _clean(r.get("series")),
            "category": _clean(r.get("category")),
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
    cols = [("Rank", "rank"), ("Series / Event", "series"),
            ("Category", "category"), ("Website", "website")]
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
