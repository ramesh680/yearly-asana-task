"""
WNBA Teams tool.

Serves the Women's National Basketball Association teams for the most recent
season, ordered by final regular-season standing, with each team's home city,
arena, win-loss record, official website and social handles. Like the other
tools, it serves a curated, versioned snapshot from ``wnba_teams_data.py``
because wnba.com is JavaScript-rendered. Refresh the snapshot each season by
editing wnba_teams_data.py.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import wnba_teams_data as DATA
from . import socials

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]

INFO = {
    "label": "WNBA - Teams",
    "edition": DATA.WNBA_EDITION,
    "url": DATA.WNBA_SOURCE_URL,
    "note": "Ordered by final regular-season standing; Las Vegas Aces won the 2025 WNBA Finals.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from wnba.com. The standings are
    JavaScript-rendered, so a server-side fetch returns no usable rows -> we
    return None and fall back to the cached snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.WNBA_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        return None
    except Exception:
        return None


def get_teams(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.WNBA_TEAMS:
        website = _clean(r.get("website"))
        item = {
            "position": r.get("position"),
            "team": _clean(r.get("team")),
            "city": _clean(r.get("city")),
            "arena": _clean(r.get("arena")),
            "wins": r.get("wins"),
            "losses": r.get("losses"),
            "website": website,
            "website_display": _display(website),
        }
        for field, _label in SOCIAL_FIELDS:
            item[field] = _clean(r.get(field))
        socials.fill(item, item.get("team"))
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
    cols = [("Seed", "position"), ("Team", "team"), ("City", "city"),
            ("Arena", "arena"), ("W", "wins"), ("L", "losses"),
            ("Website", "website")]
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
