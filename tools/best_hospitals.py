"""
Best Hospitals tool.

Serves the latest U.S. "best hospital" lists from two sources, normalized to a
common row shape with website + official social handles. We serve the curated,
versioned snapshot in ``hospitals_data.py`` rather than a live scrape: the
ranking sites are JavaScript-rendered and bot-protected, so a server-side
scrape only recovers partial rows. Set ALLOW_LIVE_FETCH = True to experiment.
"""
from __future__ import annotations

import csv
import io
import re

try:
    import requests
except Exception:  # requests is listed in requirements.txt
    requests = None

from . import hospitals_data as DATA

ALLOW_LIVE_FETCH = False

# Social platforms shown as columns, in display order.
SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("linkedin", "LinkedIn"),
]

SOURCES = {
    "usnews": {
        "label": "U.S. News & World Report - Best Hospitals Honor Roll",
        "edition": DATA.US_NEWS_EDITION,
        "url": DATA.US_NEWS_SOURCE_URL,
        "ordinal": False,
        "note": "Honor Roll is non-ordinal; hospitals are listed alphabetically by state.",
    },
    "newsweek": {
        "label": "Newsweek / Statista - World's Best Hospitals (United States)",
        "edition": DATA.NEWSWEEK_EDITION,
        "url": DATA.NEWSWEEK_SOURCE_URL,
        "ordinal": True,
        "note": "Ranked top 50 U.S. hospitals with overall score.",
    },
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def _clean(url):
    return (url or "").strip()


def _display(url):
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def _normalize(rows, ordinal):
    out = []
    for r in rows:
        website = _clean(r.get("website"))
        item = {
            "rank": r.get("rank") if ordinal else None,
            "hospital": _clean(r.get("hospital")),
            "city": _clean(r.get("city")),
            "state": _clean(r.get("state")),
            "score": _clean(r.get("score")),
            "website": website,
            "website_display": _display(website),
        }
        for field, _label in SOCIAL_FIELDS:
            item[field] = _clean(r.get(field))
        item["wikipedia"] = _clean(r.get("wikipedia"))
        out.append(item)
    return out


def _try_live_newsweek():
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.NEWSWEEK_SOURCE_URL, headers=HEADERS, timeout=12)
        if resp.status_code != 200 or len(resp.text) < 2000:
            return None
        rows = _parse_newsweek_html(resp.text)
        return rows if len(rows) >= 25 else None
    except Exception:
        return None


def _parse_newsweek_html(html):
    rows = []
    pattern = re.compile(
        r"<tr[^>]*>.*?>(\d{1,3})<.*?<a[^>]*>(.*?)</a>.*?</tr>",
        re.IGNORECASE | re.DOTALL,
    )
    for m in pattern.finditer(html):
        rank = int(m.group(1))
        name = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if name:
            rows.append({"rank": rank, "hospital": name})
    return rows


def get_hospitals(source: str, live: bool = False):
    if source not in SOURCES:
        source = "newsweek"
    info = SOURCES[source]

    rows = None
    live = False

    if (ALLOW_LIVE_FETCH or live) and source == "newsweek":
        live_rows = _try_live_newsweek()
        if live_rows and all(r.get("city") and r.get("state") for r in live_rows):
            rows = _normalize(live_rows, ordinal=True)
            live = True

    if rows is None:
        if source == "usnews":
            rows = _normalize(DATA.US_NEWS_HONOR_ROLL, ordinal=False)
        else:
            rows = _normalize(DATA.NEWSWEEK_US, ordinal=True)

    meta = {
        "source": source,
        "label": info["label"],
        "edition": info["edition"],
        "url": info["url"],
        "ordinal": info["ordinal"],
        "live": live,
        "count": len(rows),
        "note": info["note"],
        "social_fields": SOCIAL_FIELDS,
        "live_attempted": bool(live),
    }
    return rows, meta


def columns(meta):
    """Header labels + row keys, in order, for the given source."""
    cols = []
    if meta["ordinal"]:
        cols.append(("Rank", "rank"))
    cols.append(("Hospital", "hospital"))
    cols.append(("City", "city"))
    cols.append(("State", "state"))
    if meta["ordinal"]:
        cols.append(("Score", "score"))
    cols.append(("Website", "website"))
    for field, label in SOCIAL_FIELDS:
        cols.append((label, field))
    cols.append(("Wikipedia", "wikipedia"))
    return cols


def to_csv(rows, meta) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    cols = columns(meta)
    writer.writerow([label for label, _key in cols])
    for r in rows:
        writer.writerow([r.get(key, "") for _label, key in cols])
    return buf.getvalue()
