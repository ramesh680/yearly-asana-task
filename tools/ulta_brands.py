from __future__ import annotations
import csv
import io
from . import ulta_brands_data as DATA
from . import socials

INFO = {
    "label": "Ulta Brands - ulta.com",
    "edition": DATA.ULTA_EDITION,
    "url": DATA.ULTA_SOURCE_URL,
    "note": "Full A-Z Ulta brand directory. Brand pages link to Ulta. "
            "Facebook/Instagram/X/YouTube/TikTok handles are auto-generated from "
            "the brand name and unverified, except select prominent brands.",
}

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def get_brands(live: bool = False):
    rows = []
    for r in DATA.ULTA_BRANDS:
        ulta = _clean(r.get("ulta_url"))
        item = {
            "rank": r.get("rank"),
            "brand": _clean(r.get("brand")),
            "ulta_url": ulta,
            "ulta_display": _display(ulta),
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
    cols = [("Rank", "rank"), ("Brand", "brand"), ("Ulta Page", "ulta_url")]
    for field, label in SOCIAL_FIELDS:
        cols.append((label, field))
    cols.append(("Wikipedia", "wikipedia"))
    return cols


def to_csv(rows) -> str:
    cols = columns()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow([label for label, _ in cols])
    for r in rows:
        w.writerow([r.get(key, "") for _, key in cols])
    return buf.getvalue()
