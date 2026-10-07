"""Refreshed-link overlay.

The curated snapshots in ``tools/*_data.py`` stay the source of truth for the
rows themselves (names, ranks, cities...). Their *links* - official website,
Wikipedia page and social accounts - go stale over time, so
``scripts/refresh_links.py`` re-checks them against the live websites,
Wikipedia and Wikidata and writes the results to ``data/link_refresh.json``.

At request time every tool's getter is wrapped (see ``install``) so the rows it
returns have the refreshed links applied on top. If the JSON is missing or
empty, rows are served exactly as before.
"""
from __future__ import annotations

import functools
import json
import os
import re
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "link_refresh.json")

# Link fields the refresher may update on a row.
LINK_FIELDS = ["website", "wikipedia", "facebook", "instagram", "twitter",
               "youtube", "tiktok", "linkedin", "twitch"]

# (overlay key, module name, getter name, positional args)
# Russell 3000 is excluded: it has its own refresh script and static page.
REGISTRY = [
    ("best_hospitals:usnews", "best_hospitals", "get_hospitals", ("usnews",)),
    ("best_hospitals:newsweek", "best_hospitals", "get_hospitals", ("newsweek",)),
    ("best_colleges", "best_colleges", "get_colleges", ()),
    ("premier_league", "premier_league", "get_clubs", ()),
    ("saudi_pro_league", "saudi_pro_league", "get_clubs", ()),
    ("twitch_streamers", "twitch_streamers", "get_streamers", ()),
    ("wnba_teams", "wnba_teams", "get_teams", ()),
    ("motorsports", "motorsports", "get_motorsports", ()),
    ("nfl_teams", "nfl_teams", "get_teams", ()),
    ("racquet_sports", "racquet_sports", "get_sports", ()),
    ("golf_tours", "golf_tours", "get_rows", ()),
    ("nba_teams", "nba_teams", "get_rows", ()),
    ("nhl_teams", "nhl_teams", "get_rows", ()),
    ("mls_teams", "mls_teams", "get_rows", ()),
    ("nwsl_teams", "nwsl_teams", "get_rows", ()),
    ("mlb_teams", "mlb_teams", "get_rows", ()),
    ("milb_teams", "milb_teams", "get_rows", ()),
    ("brasileirao", "brasileirao", "get_rows", ()),
    ("bundesliga", "bundesliga", "get_rows", ()),
    ("laliga", "laliga", "get_rows", ()),
    ("serie_a", "serie_a", "get_rows", ()),
    ("ligue1", "ligue1", "get_rows", ()),
    ("sp500", "sp500", "get_rows", ()),
    ("combat_sports", "combat_sports", "get_rows", ()),
    ("sporting_events", "sporting_events", "get_rows", ()),
    ("streaming_services", "streaming_services", "get_rows", ()),
    ("vg_franchises", "vg_franchises", "get_rows", ()),
    ("vg_platforms", "vg_platforms", "get_rows", ()),
    ("vg_publishers", "vg_publishers", "get_rows", ()),
    ("cpg_brands", "cpg_brands", "get_rows", ()),
    ("leagues_revenue", "leagues_revenue", "get_rows", ()),
    ("insurance", "insurance", "get_rows", ()),
    ("sephora_brands", "sephora_brands", "get_brands", ()),
    ("ulta_brands", "ulta_brands", "get_brands", ()),
]

# Field holding the entity name, per tool (first non-rank column).
_SKIP_NAME_COLS = {"rank", "position", "ticker"}


def name_field(module, meta=None):
    try:
        cols = module.columns(meta) if module.__name__.endswith("best_hospitals") else module.columns()
    except TypeError:
        cols = module.columns()
    for _label, key in cols:
        if key not in _SKIP_NAME_COLS:
            return key
    return "name"


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def row_keys(rows, field):
    """Stable per-row keys: normalized name, with #2, #3... for duplicates."""
    seen, keys = {}, []
    for r in rows:
        base = norm(str(r.get(field) or "")) or "row"
        seen[base] = seen.get(base, 0) + 1
        keys.append(base if seen[base] == 1 else "{}#{}".format(base, seen[base]))
    return keys


def display(url):
    return (url or "").replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


# ----------------------------------------------------------------- overlay
_cache = {"mtime": None, "data": {}}
_lock = threading.Lock()


def load():
    try:
        mtime = os.path.getmtime(DATA_PATH)
    except OSError:
        return {}
    with _lock:
        if _cache["mtime"] != mtime:
            try:
                with open(DATA_PATH, encoding="utf-8") as f:
                    _cache["data"] = json.load(f) or {}
            except (OSError, ValueError):
                _cache["data"] = {}
            _cache["mtime"] = mtime
        return _cache["data"]


def apply(key, module, rows, meta):
    data = load()
    tool = (data.get("tools") or {}).get(key)
    if not tool:
        return rows
    field = name_field(module, meta)
    overrides = tool.get("rows") or {}
    for rk, row in zip(row_keys(rows, field), rows):
        upd = overrides.get(rk)
        if not upd:
            continue
        for f in LINK_FIELDS:
            v = upd.get(f)
            if v:
                row[f] = v
        if upd.get("website"):
            row["website_display"] = display(upd["website"])
    if isinstance(meta, dict):
        meta["links_refreshed"] = data.get("generated", "")[:10]
    return rows


def _wrap(module, getter, fixed_key=None):
    original = getattr(module, getter)
    if getattr(original, "_link_refresh_wrapped", False):
        return

    @functools.wraps(original)
    def wrapped(*args, **kwargs):
        rows, meta = original(*args, **kwargs)
        key = fixed_key
        if key is None:  # best_hospitals: key depends on source
            src = args[0] if args else kwargs.get("source", "")
            key = "{}:{}".format(module.__name__.rsplit(".", 1)[-1], (meta or {}).get("source") or src)
        try:
            apply(key, module, rows, meta)
        except Exception:  # never break a page because of the overlay
            pass
        return rows, meta

    wrapped._link_refresh_wrapped = True
    wrapped._link_refresh_original = original
    setattr(module, getter, wrapped)


def install():
    """Wrap every registered tool getter so refreshed links are applied."""
    import importlib
    done = set()
    for key, mod_name, getter, args in REGISTRY:
        if (mod_name, getter) in done:
            continue
        done.add((mod_name, getter))
        module = importlib.import_module("tools." + mod_name)
        multi = sum(1 for _k, m, g, _a in REGISTRY if m == mod_name and g == getter) > 1
        _wrap(module, getter, None if multi else key)
