"""
Top Twitch Streamers tool.

Serves the top channels from TwitchTracker's overall ranking, with each channel's
30-day average viewers, all-time peak viewers, hours watched, Twitch channel link
and social handles. Like the other tools, it serves a curated, versioned snapshot
from ``twitch_streamers_data.py`` because the TwitchTracker ranking is
JavaScript-rendered and the figures change daily. Refresh the snapshot
periodically by editing twitch_streamers_data.py.
"""
from __future__ import annotations

import csv
import io

try:
    import requests
except Exception:
    requests = None

from . import twitch_streamers_data as DATA

SOCIAL_FIELDS = [
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
]

INFO = {
    "label": "TwitchTracker - Overall Channel Ranking",
    "edition": DATA.TWITCH_EDITION,
    "url": DATA.TWITCH_SOURCE_URL,
    "note": "Overall rank blends average viewers, followers, views and stream time over the trailing 30 days.",
}

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def _clean(v):
    return (v or "").strip() if isinstance(v, str) else v


def _display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def _try_live():
    """Best-effort live fetch from TwitchTracker. The ranking is
    JavaScript-rendered, so a server-side fetch returns no usable rows -> we
    return None and fall back to the cached snapshot."""
    if requests is None:
        return None
    try:
        resp = requests.get(DATA.TWITCH_SOURCE_URL, headers=_HEADERS, timeout=12)
        if resp.status_code != 200:
            return None
        return None
    except Exception:
        return None


def get_streamers(live: bool = False):
    is_live = False
    if live:
        live_rows = _try_live()
        is_live = bool(live_rows)
    rows = []
    for r in DATA.TOP_TWITCH_STREAMERS:
        twitch = _clean(r.get("twitch"))
        item = {
            "position": r.get("position"),
            "channel": _clean(r.get("channel")),
            "avg_viewers": r.get("avg_viewers"),
            "peak_viewers": r.get("peak_viewers"),
            "hours_watched": r.get("hours_watched"),
            "twitch": twitch,
            "twitch_display": _display(twitch),
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
    cols = [("Rank", "position"), ("Channel", "channel"),
            ("Avg Viewers", "avg_viewers"), ("Peak Viewers", "peak_viewers"),
            ("Hours Watched", "hours_watched"), ("Twitch", "twitch")]
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
