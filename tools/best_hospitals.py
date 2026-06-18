"""
Best Hospitals tool.

Pulls the latest "best hospital" lists for the United States from two
sources and normalizes them into a common row shape:

    {"rank": <int|None>, "hospital": str, "city": str, "state": str, "score": str}

It tries a live fetch first; if the source can't be reached or parsed it
falls back to the versioned offline snapshot in ``hospitals_data.py`` and
reports which path was used so the UI can show a clear "live / cached" badge.
"""
from __future__ import annotations

import csv
import io
import re

try:
    import requests
except Exception:  # pragma: no cover - requests is in requirements.txt
    requests = None

from . import hospitals_data as DATA

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
        out.append(
            {
                "rank": r.get("rank") if ordinal else None,
                "hospital": r.get("hospital", "").strip(),
                "city": r.get("city", "").strip(),
                "state": r.get("state", "").strip(),
                "score": r.get("score", "").strip(),
            }
        )
    return out


def _try_live_newsweek():
    """Attempt to scrape the live Newsweek US ranking table."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.NEWSWEEK_SOURCE_URL, headers=HEADERS, timeout=12)
        if resp.status_code != 200 or len(resp.text) < 2000:
            return None
        html = resp.text
        # The page is largely client-rendered; rows occasionally appear in the
        # static HTML. Be conservative: only accept a live result if we can
        # recover a sensible number of ranked rows.
        rows = _parse_newsweek_html(html)
        if len(rows) >= 25:
            return rows
        return None
    except Exception:
        return None


def _parse_newsweek_html(html):
    """Best-effort parser for Newsweek's ranking rows from raw HTML."""
    rows = []
    # Rows look like: <td>1</td> ... <a ...>Hospital Name</a> ... <td>City</td><td>State</td>
    pattern = re.compile(
        r"<tr[^>]*>.*?>(\d{1,3})<.*?<a[^>]*>(.*?)</a>.*?</tr>",
        re.IGNORECASE | re.DOTALL,
    )
    for m in pattern.finditer(html):
        rank = int(m.group(1))
        name = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if name:
            rows.append({"rank": rank, "hospital": name, "city": "", "state": "", "score": ""})
    return rows


def get_hospitals(source: str):
    """
    Returns (rows, meta).

    meta = {
        "source": key, "label": ..., "edition": ..., "url": ...,
        "ordinal": bool, "live": bool, "count": int, "note": str,
    }
    """
    if source not in SOURCES:
        source = "newsweek"
    info = SOURCES[source]

    rows = None
    live = False

    # NOTE: We intentionally serve the curated, versioned snapshot rather than
    # the live scrape. The ranking sites are JavaScript-rendered, so a server
    # scrape only recovers partial rows (rank + name, with empty city/state/
    # score and HTML-escaped names). Since this is yearly data, the complete
    # offline snapshot in hospitals_data.py is the reliable source of truth.
    # To re-enable an experimental live fetch, set ALLOW_LIVE_FETCH = True.
    ALLOW_LIVE_FETCH = False

    if ALLOW_LIVE_FETCH and source == "newsweek":
        live_rows = _try_live_newsweek()
        # Only accept a live result if it actually carries full columns.
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
        writer.writerow(["Rank", "Hospital", "City", "State", "Score"])
        for r in rows:
            writer.writerow([r["rank"], r["hospital"], r["city"], r["state"], r["score"]])
    else:
        writer.writerow(["Hospital", "City", "State"])
        for r in rows:
            writer.writerow([r["hospital"], r["city"], r["state"]])
    return buf.getvalue()
