"""
Sephora Brands tool.

Serves Sephora's full A-Z brand directory (sephora.com/brands-list). Each brand
links to its Sephora brand page, with Facebook / Instagram / X / YouTube / TikTok
handles. Handles are auto-generated from the brand name (unverified) except a
small set of prominent brands with verified handles baked into
``sephora_brands_data.py``. Serves a curated, versioned snapshot; refresh by
re-reading sephora.com/brands-list.
"""
from __future__ import annotations

import csv
import io

from . import sephora_brands_data as DATA
from . import socials

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]

INFO = {
    "label": "Sephora Brands - sephora.com",
    "edition": DATA.SEPHORA_EDITION,
    "url": DATA.SEPHORA_SOURCE_URL,
    "note": "Full A-Z Sephora brand directory. Brand pages link to Sephora. "
            "Facebook/Instagram/X/YouTube/TikTok handles are auto-generated from "
            "the brand name and unverified, except select prominent brands.",
}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def get_brands(live: bool = False):
    rows = []
    for r in DATA.SEPHORA_BRANDS:
        sephora = _clean(r.get("sephora_url"))
        item = {
            "rank": r.get("rank"),
            "brand": _clean(r.get("brand")),
            "sephora_url": sephora,
            "sephora_display": _display(sephora),
        }
        for field, _label in SOCIAL_FIELDS:
            item[field] = _clean(r.get(field))
        socials.fill(item, item.get("brand"))
        item["wikipedia"] = _clean(r.get("wikipedia"))
        rows.append(item)

    meta = {
        "label": INFO["label"],
        "edition": INFO["edition"],
        "url": INFO["url"],
        "note": INFO["note"],
        "count": len(rows),
        "social_fields": SOCIAL_FIELDS,
        "live": False,
        "live_attempted": bool(live),
    }
    return rows, meta


def columns():
    cols = [("Rank", "rank"), ("Brand", "brand"), ("Sephora Page", "sephora_url")]
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
