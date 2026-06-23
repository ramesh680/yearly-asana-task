"""
Top Beauty Brands tool.

Serves the best-selling beauty brands on Ulta.com (by share of online sales)
with each brand's category, Ulta.com online sales share, official website and
social handles. Like the other tools, it serves a curated, versioned snapshot
from ``beauty_brands_data.py``. Refresh the snapshot periodically by editing
beauty_brands_data.py.
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
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
]

INFO = {
    "label": "Top Beauty Brands - Ulta.com online sales share",
    "edition": DATA.BEAUTY_EDITION,
    "url": DATA.BEAUTY_SOURCE_URL,
    "note": "Ranked by 2025 share of online sales on ulta.com (Navigo Marketing via WWD); excludes in-store and app sales.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from ulta.com. The site is JavaScript-rendered and
    does not expose a ranking, so we return None and fall back to the cached
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
        website = _clean(r.get("website"))
        item = {
            "rank": r.get("rank"),
            "brand": _clean(r.get("brand")),
            "category": _clean(r.get("category")),
            "share": _clean(r.get("share")),
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
    cols = [("Rank", "rank"), ("Brand", "brand"), ("Category", "category"),
            ("Ulta.com Share", "share"), ("Website", "website")]
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
