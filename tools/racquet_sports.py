"""Racquet Sports tool: major racket sports + governing bodies, plus Wikipedia's list."""
from __future__ import annotations
import csv, io
try:
    import requests
except Exception:
    requests = None
from . import racquet_sports_data as DATA
from . import socials

SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]
INFO = {"label": "Racquet Sports", "edition": DATA.RACQUET_EDITION, "url": DATA.RACQUET_SOURCE_URL,
        "note": "Major racket sports list their international governing body; other sports link to Wikipedia (most have no single global body)."}
_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def _clean(v): return (v or "").strip() if isinstance(v, str) else v
def _display(url): return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")

def _try_live():
    if requests is None: return None
    try:
        requests.get(DATA.RACQUET_SOURCE_URL, headers=_HEADERS, timeout=12); return None
    except Exception:
        return None

def get_sports(live: bool = False):
    is_live = False
    if live: is_live = bool(_try_live())
    rows = []
    for r in DATA.RACQUET_SPORTS:
        website = _clean(r.get("website"))
        item = {"rank": r.get("rank"), "sport": _clean(r.get("sport")),
                "governing_body": _clean(r.get("governing_body")),
                "website": website, "website_display": _display(website)}
        for f, _l in SOCIAL_FIELDS: item[f] = _clean(r.get(f))
        socials.fill(item, item.get("sport"))
        item["wikipedia"] = _clean(r.get("wikipedia"))
        rows.append(item)
    meta = {"label": INFO["label"], "edition": INFO["edition"], "url": INFO["url"],
            "note": INFO["note"], "count": len(rows), "social_fields": SOCIAL_FIELDS,
            "live": is_live, "live_attempted": bool(live)}
    return rows, meta

def columns():
    cols = [("Rank", "rank"), ("Sport", "sport"), ("Governing Body", "governing_body"), ("Website", "website")]
    for f, l in SOCIAL_FIELDS: cols.append((l, f))
    cols.append(("Wikipedia", "wikipedia"))
    return cols

def to_csv(rows):
    buf = io.StringIO(); w = csv.writer(buf); cols = columns()
    w.writerow([l for l, _k in cols])
    for r in rows: w.writerow([r.get(k, "") for _l, k in cols])
    return buf.getvalue()
