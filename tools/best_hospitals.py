"""
Best Hospitals tool.

Serves the latest U.S. "best hospital" lists from two sources, normalized to:

    {"rank": int|None, "hospital": str, "city": str, "state": str,
     "score": str, "website": str, "website_display": str}

We serve the curated, versioned snapshot in ``hospitals_data.py`` rather than a
live scrape: the ranking sites are JavaScript-rendered and bot-protected, so a
server-side scrape only recovers partial rows. Since this is yearly data, the
offline snapshot is the reliable source of truth. Set ALLOW_LIVE_FETCH = True
to experiment with a live fetch (only accepted if it returns full columns).
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


def _normalize(rows, ordinal):
    out = []
    for r in rows:
        website = (r.get("website") or "").strip()
        display = website.replace("https://", "").replace("http://", "").rstrip("/")
        out.append(
            {
                "rank": r.get("rank") if ordinal else None,
                "hospital": (r.get("hospital") or "").strip(),
                "city": (r.get("city") or "").strip(),
                "state": (r.get("state") or "").strip(),
                "score": (r.get("score") or "").strip(),
                "website": website,
                "website_display": display,
            }
        )
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
            rows.append({"rank": rank, "hospital": name, "city": "", "state": "", "score": "", "website": ""})
    return rows


def get_hospitals(source: str):
    if source not in SOURCES:
        source = "newsweek"
    info = SOURCES[source]

    rows = None
    live = False

    if ALLOW_LIVE_FETCH and source == "newsweek":
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
    }
    return rows, meta


def to_csv(rows, meta) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    if meta["ordinal"]:
        writer.writerow(["Rank", "Hospital", "City", "State", "Score", "Website"])
        for r in rows:
            writer.writerow([r["rank"], r["hospital"], r["city"], r["state"], r["score"], r["website"]])
    else:
        writer.writerow(["Hospital", "City", "State", "Website"])
        for r in rows:
            writer.writerow([r["hospital"], r["city"], r["state"], r["website"]])
    return buf.getvalue()
