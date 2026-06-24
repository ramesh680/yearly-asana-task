"""S&P 500 section."""
from __future__ import annotations
import csv, io
from . import sp500_data as DATA
from . import socials

SOCIAL_FIELDS = socials.SOCIAL_FIELDS
INFO = {"label": "S&P 500", "edition": DATA.SP500_EDITION, "url": DATA.SP500_SOURCE_URL, "note": "S&P 500 index constituents (503 securities)."}

def _clean(v): return (v or "").strip() if isinstance(v, str) else v
def _display(url): return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")

def get_rows(live: bool = False):
    rows = []
    for r in DATA.SP500_COMPANIES:
        website = _clean(r.get("website"))
        item = {"rank": r.get("rank"), "website": website, "website_display": _display(website)}
        for _lbl, f in [('Ticker', 'ticker'), ('Company', 'company'), ('Sector', 'sector'), ('Headquarters', 'hq')]:
            item[f] = _clean(r.get(f))
        socials.fill(item, item.get("company"))
        item["wikipedia"] = _clean(r.get("wikipedia"))
        rows.append(item)
    meta = {"label": INFO["label"], "edition": INFO["edition"], "url": INFO["url"], "note": INFO["note"],
            "count": len(rows), "social_fields": SOCIAL_FIELDS, "live": False, "live_attempted": bool(live)}
    return rows, meta

def columns():
    cols = [("Rank", "rank")] + [('Ticker', 'ticker'), ('Company', 'company'), ('Sector', 'sector'), ('Headquarters', 'hq')] + [("Website", "website")]
    for f, l in SOCIAL_FIELDS: cols.append((l, f))
    cols.append(("Wikipedia", "wikipedia"))
    return cols

def to_csv(rows):
    buf = io.StringIO(); w = csv.writer(buf); cols = columns()
    w.writerow([l for l, _k in cols])
    for r in rows: w.writerow([r.get(k, "") for _l, k in cols])
    return buf.getvalue()
