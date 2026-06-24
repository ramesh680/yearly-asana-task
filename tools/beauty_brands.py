"""
Top Beauty Brands tool.

Serves beauty brands sourced from Ulta.com. Ranks 1-10 are the best-selling
brands on Ulta.com in 2025 by share of online sales (WWD / Navigo Marketing),
with category, sales share and verified social/Wikipedia links. Ranks 11-500
are Ulta's brand directory (ulta.com/brand/all) in alphabetical order, each
linking to its official Ulta brand page. Serves a curated, versioned snapshot
from ``beauty_brands_data.py``; refresh by re-reading ulta.com/brand/all.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import beauty_brands_data as DATA

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
]

INFO = {
    "label": "Top Beauty Brands - Ulta.com",
    "edition": DATA.BEAUTY_EDITION,
    "url": DATA.BEAUTY_SOURCE_URL,
    "note": "Top 10 verified; ranks 11-500 link to Ulta. Facebook/YouTube (and 11-500 Instagram/X) are auto-generated from the brand name and unverified.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from ulta.com. The site is JavaScript-rendered, so
    a server-side fetch returns no usable rows -> we fall back to the cached
    snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.BEAUTY_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        return None
    except Exception:
        return None


def get_brands(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.TOP_BEAUTY_BRANDS:
        ulta = _clean(r.get("ulta_url"))
        item = {
            "rank": r.get("rank"),
            "brand": _clean(r.get("brand")),
            "category": _clean(r.get("category")),
            "share": _clean(r.get("share")),
            "ulta_url": ulta,
            "ulta_display": _display(ulta),
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
    cols = [("Rank", "rank"), ("Brand", "brand"), ("Category", "category"),
            ("Ulta.com Share", "share"), ("Ulta Page", "ulta_url")]
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
