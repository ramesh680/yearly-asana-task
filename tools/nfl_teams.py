"""National Football League tool: 32 NFL teams by conference and division."""
from __future__ import annotations
import csv, io
try:
    import requests
except Exception:
    requests = None
from . import nfl_teams_data as DATA

SOCIAL_FIELDS = [("twitter", "X / Twitter"), ("instagram", "Instagram")]
INFO = {"label": "National Football League - Teams", "edition": DATA.NFL_EDITION,
        "url": DATA.NFL_SOURCE_URL,
        "note": "All 32 NFL teams grouped by conference (AFC/NFC) and division."}
_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def _clean(v): return (v or "").strip() if isinstance(v, str) else v
def _display(url): return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")

def _try_live():
    if requests is None: return None
    try:
        r = requests.get(DATA.NFL_SOURCE_URL, headers=_HEADERS, timeout=12)
        return None
    except Exception:
        return None

def get_teams(live: bool = False):
    is_live = False
    if live:
        is_live = bool(_try_live())
    rows = []
    for r in DATA.NFL_TEAMS:
        website = _clean(r.get("website"))
        item = {"rank": r.get("rank"), "team": _clean(r.get("team")),
                "conference": _clean(r.get("conference")), "division": _clean(r.get("division")),
                "city": _clean(r.get("city")), "stadium": _clean(r.get("stadium")),
                "website": website, "website_display": _display(website)}
        for f, _l in SOCIAL_FIELDS: item[f] = _clean(r.get(f))
        item["wikipedia"] = _clean(r.get("wikipedia"))
        rows.append(item)
    meta = {"label": INFO["label"], "edition": INFO["edition"], "url": INFO["url"],
            "note": INFO["note"], "count": len(rows), "social_fields": SOCIAL_FIELDS,
            "live": is_live, "live_attempted": bool(live)}
    return rows, meta

def columns():
    cols = [("Rank", "rank"), ("Team", "team"), ("Conference", "conference"),
            ("Division", "division"), ("City", "city"), ("Stadium", "stadium"), ("Website", "website")]
    for f, l in SOCIAL_FIELDS: cols.append((l, f))
    cols.append(("Wikipedia", "wikipedia"))
    return cols

def to_csv(rows):
    buf = io.StringIO(); w = csv.writer(buf); cols = columns()
    w.writerow([l for l, _k in cols])
    for r in rows: w.writerow([r.get(k, "") for _l, k in cols])
    return buf.getvalue()
