"""
Best Colleges tool.

Serves the U.S. News Best National Universities ranking (Top 50, 2026 edition)
with each school's official website and social handles. Like the hospitals
tool, it serves a curated, versioned snapshot from ``colleges_data.py`` because
the U.S. News page is JavaScript-rendered and gates the full list behind a
login. Refresh the snapshot yearly by editing colleges_data.py.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import colleges_data as DATA

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("linkedin", "LinkedIn"),
]

INFO = {
    "label": "U.S. News - Best National Universities",
    "edition": DATA.COLLEGES_EDITION,
    "url": DATA.COLLEGES_SOURCE_URL,
    "note": "Ranks reflect ties as published by U.S. News (shared numbers).",
}


def _clean(v):
    return (v or "").strip()


def _display(url):
    return url.replace("https://", "").replace("http://", "").rstrip("/")


_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _try_live():
    """Best-effort live fetch from U.S. News. The page is JavaScript-rendered
    and gates the full list behind a login, so a server-side fetch returns no
    usable ranking rows -> we return None and fall back to the cached snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.COLLEGES_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        # The ranking rows are not present in the static HTML; nothing reliable
        # to parse. Returning None keeps the trustworthy cached snapshot.
        return None
    except Exception:
        return None


def get_colleges(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.NATIONAL_UNIVERSITIES:
        website = _clean(r.get("website"))
        item = {
            "rank": r.get("rank"),
            "university": _clean(r.get("university")),
            "city": _clean(r.get("city")),
            "state": _clean(r.get("state")),
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
    cols = [("Rank", "rank"), ("University", "university"), ("City", "city"),
            ("State", "state"), ("Website", "website")]
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
