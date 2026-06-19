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


def get_colleges():
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
        rows.append(item)

    meta = {
        "label": INFO["label"],
        "edition": INFO["edition"],
        "url": INFO["url"],
        "note": INFO["note"],
        "count": len(rows),
        "social_fields": SOCIAL_FIELDS,
    }
    return rows, meta


def columns():
    cols = [("Rank", "rank"), ("University", "university"), ("City", "city"),
            ("State", "state"), ("Website", "website")]
    for field, label in SOCIAL_FIELDS:
        cols.append((label, field))
    return cols


def to_csv(rows) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    cols = columns()
    writer.writerow([label for label, _key in cols])
    for r in rows:
        writer.writerow([r.get(key, "") for _label, key in cols])
    return buf.getvalue()
