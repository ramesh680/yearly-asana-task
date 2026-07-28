"""
ingest_export.py
----------------
Convert **a tool's own output rows** into an ingest-template file (.xlsx), using
the same ingest-template logic as the Title Automation tool.

This is the piece behind the "Ingest Template (.xlsx)" export that sits next to
each tool's existing CSV / Excel buttons. Ops runs a tool (e.g. Billboard Artist
100), clicks one button, and gets back an ingest-ready BDR file for the title
category that tool produces (Billboard artists -> Talent).

How it works
------------
Each tool declares an INGEST PROFILE: which title category its rows belong to,
which column holds the title/name, and how its other columns map onto ingest
columns. We turn the rows into a CSV in the ingest column vocabulary and hand it
to the Title Automation service, which applies the real ingest templates.

Why a CSV of mapped columns (and not just names): the tools already scrape
official websites, IMDb ids, Wikipedia URLs and social handles. The generator
treats uploaded values as authoritative and only fills the blanks, so passing
them through keeps the data the tool already found and enriches the rest.

Add a new tool by adding one PROFILES entry -- no new code.
"""
from __future__ import annotations

import csv
import io
import re
from typing import Any, Callable, Iterable, Optional

from bdr_ingest import BdrIngestError, BdrIngestService


# --- ingest column vocabulary we may emit -------------------------------------
# (names must match the Title Automation upload schema)
TITLE = "title"
CATEGORY = "title_category"
PROFESSION = "profession"          # talent disambiguation hint
SOCIAL_TRIGGER = "twitter_handle"  # presence of a social column selects the
                                   # full-schema upload path upstream


def _s(v: Any) -> str:
    return "" if v is None else str(v).strip()


# --- value normalizers --------------------------------------------------------
def _imdb(v: Any) -> str:
    """Accept an nm/tt code or a full URL; emit a URL the generator understands."""
    s = _s(v)
    if not s:
        return ""
    m = re.search(r"(nm|tt)\d{5,}", s, re.I)
    if not m:
        return ""
    code = m.group(0)
    kind = "name" if code.lower().startswith("nm") else "title"
    return f"https://www.imdb.com/{kind}/{code}"


def _url(v: Any) -> str:
    s = _s(v)
    if not s or s.lower() in {"n/a", "na", "-", "none"}:
        return ""
    if s.startswith("//"):
        return "https:" + s
    if not s.startswith("http") and "." in s:
        return "https://" + s
    return s if s.startswith("http") else ""


def _handle(v: Any) -> str:
    """Reduce a social URL or @handle to the bare handle."""
    s = _s(v).lstrip("@")
    if not s:
        return ""
    if "/" in s:
        s = s.rstrip("/").rsplit("/", 1)[-1]
    return s.split("?")[0]


def _gender_line(v: Any) -> str:
    """Normalize a raw gender value to the ingest template's line format."""
    s = _s(v).lower()
    if s.startswith("m"):
        return "Gender - Man"
    if s.startswith("f") or s.startswith("w"):
        return "Gender - Woman"
    return ""


def _first_of(v: Any) -> str:
    """First entry of a delimited list (e.g. 'singer, songwriter' -> 'singer')."""
    s = _s(v)
    if not s:
        return ""
    for sep in ("|", ";", ","):
        if sep in s:
            return s.split(sep)[0].strip()
    return s


# --- profile definition -------------------------------------------------------
class IngestProfile:
    """Declares how one tool's rows convert into ingest rows.

    category  : the ingest title category ('Talent', 'Movies', 'TV Shows', ...)
    title_from: source column(s) holding the title/name -- first non-blank wins
    columns   : {ingest_column: source_column | (source_column, normalizer)}
    """

    def __init__(self, category: str, title_from, columns: Optional[dict] = None,
                 label: str = "") -> None:
        self.category = category
        self.title_from = [title_from] if isinstance(title_from, str) else list(title_from)
        self.columns = columns or {}
        self.label = label or category

    def title_of(self, row: dict) -> str:
        for col in self.title_from:
            v = _s(_get_ci(row, col))
            if v:
                return v
        return ""

    def ingest_row(self, row: dict) -> dict:
        out = {TITLE: self.title_of(row), CATEGORY: self.category}
        for target, source in self.columns.items():
            norm: Optional[Callable] = None
            if isinstance(source, tuple):
                source, norm = source
            # source may be a single column or a list of candidates (raw row
            # keys AND display labels), so one profile works whether it is fed
            # the tool's internal rows or its exported/labelled rows.
            candidates = [source] if isinstance(source, str) else list(source)
            raw = ""
            for cand in candidates:
                raw = _get_ci(row, cand)
                if _s(raw):
                    break
            val = norm(raw) if norm else _s(raw)
            if val:
                out[target] = val
        return out


def _get_ci(row: dict, col: str) -> Any:
    """Case-insensitive column lookup."""
    if col in row:
        return row[col]
    low = {str(k).strip().lower(): k for k in row}
    key = low.get(str(col).strip().lower())
    return row.get(key, "") if key else ""


# --- source-column candidates -------------------------------------------------
# The yearly tools store socials under short keys ('twitter') and export them
# under display labels ('X / Twitter'); list both so one profile handles either.
_WIKI = ["wikipedia", "Wikipedia", "Wikipedia URL"]
_TW = ["twitter", "X / Twitter", "Twitter"]
_IG = ["instagram", "Instagram"]
_FB = ["facebook", "Facebook"]
_YT = ["youtube", "YouTube"]
_TT = ["tiktok", "TikTok"]
_LI = ["linkedin", "LinkedIn"]
_SITE = ["website", "Official Website", "Website"]


# --- tool -> profile registry -------------------------------------------------
# Keyed by a short slug used in the export routes.
PROFILES: dict[str, IngestProfile] = {
    # ---------------- media-tools-hub ----------------
    # Billboard artists are people -> Talent. Occupations/gender come from the
    # tool's own Wikidata enrichment, which is exactly what the Talent template
    # needs for title_sub_category (Talent Type / Subtype / Gender).
    "billboard-artist-100": IngestProfile(
        "Talent",
        ["Artist Name", "Artist"],
        {
            "imdb_id": ("IMDb URL", _imdb),
            "wikipedia_page": ("Wikipedia URL", _url),
            PROFESSION: ("Occupations", _first_of),
            "gender": ("Gender", _gender_line),
        },
        label="Billboard Artist 100",
    ),
    "tv-premiere-calendar": IngestProfile(
        "TV Shows",
        ["Title", "Show", "Series"],
        {
            "imdb_id": ("IMDb ttcode", _imdb),
            "network": "Network",
            "released_on": "Premiere Date",
            "metacritic": ("Metacritic URL", _url),
        },
        label="TV Premiere Calendar",
    ),
    "movie-release-calendar": IngestProfile(
        "Movies",
        ["Title", "Movie"],
        {
            "imdb_id": ("IMDb ttcode", _imdb),
            "released_on": "Release Date",
            "metacritic": ("Metacritic URL", _url),
        },
        label="Movie Release Calendar",
    ),
    "game-release-calendar": IngestProfile(
        "Video Game",
        ["Title", "Game"],
        {"released_on": "Release Date", "metacritic": ("Metacritic URL", _url)},
        label="Game Release Calendar",
    ),

    # ---------------- yearly-asana-task ----------------
    # People -> Talent
    "twitch-streamers": IngestProfile(
        "Talent",
        ["channel", "Channel", "Streamer", "Name"],
        {
            "wikipedia_page": (_WIKI, _url),
            "twitter_handle": (_TW, _handle),
            "instagram_user": (_IG, _handle),
            "youtube_channel_username": (_YT, _url),
            "facebook_page": (_FB, _url),
            "tiktok_user": (_TT, _handle),
            # streamers are Internet Personalities -> seeds the Talent subtype
            PROFESSION: (["channel", "Channel"], lambda v: "streamer" if _s(v) else ""),
        },
        label="Top Twitch Streamers",
    ),
    # Brands -> Health & Beauty
    "sephora-brands": IngestProfile(
        "Health & Beauty",
        ["brand", "Brand", "Brand Name"],
        {
            "wikipedia_page": (_WIKI, _url),
            "twitter_handle": (_TW, _handle),
            "instagram_user": (_IG, _handle),
            "facebook_page": (_FB, _url),
            "youtube_channel_username": (_YT, _url),
            "tiktok_user": (_TT, _handle),
        },
        label="Sephora Brands",
    ),
    "ulta-brands": IngestProfile(
        "Health & Beauty",
        ["brand", "Brand", "Brand Name"],
        {
            "wikipedia_page": (_WIKI, _url),
            "twitter_handle": (_TW, _handle),
            "instagram_user": (_IG, _handle),
            "facebook_page": (_FB, _url),
            "youtube_channel_username": (_YT, _url),
            "tiktok_user": (_TT, _handle),
        },
        label="Ulta Brands",
    ),
    "beauty-brands": IngestProfile(
        "Health & Beauty",
        ["brand", "Brand", "Brand Name"],
        {
            "wikipedia_page": (_WIKI, _url),
            "twitter_handle": (_TW, _handle),
            "instagram_user": (_IG, _handle),
            "facebook_page": (_FB, _url),
        },
        label="Top Beauty Brands",
    ),
}

# Sports-team tools all share the same shape -> Sports Franchise.
_SPORTS_TOOLS = {
    "premier-league": ("Premier League", ["club", "team", "Club", "Team"]),
    "saudi-pro-league": ("Saudi Pro League", ["club", "team", "Club", "Team"]),
    "nfl-teams": ("NFL Teams", ["team", "Team"]),
    "nba-teams": ("NBA Teams", ["team", "Team"]),
    "nhl-teams": ("NHL Teams", ["team", "Team"]),
    "mlb-teams": ("MLB Teams", ["team", "Team"]),
    "milb-teams": ("MiLB Teams", ["team", "Team"]),
    "mls-teams": ("MLS Teams", ["team", "Team"]),
    "nwsl-teams": ("NWSL Teams", ["team", "Team"]),
    "wnba-teams": ("WNBA Teams", ["team", "Team"]),
    "brasileirao": ("Brasileirao", ["club", "team", "Club", "Team"]),
    "bundesliga": ("Bundesliga", ["club", "team", "Club", "Team"]),
    "laliga": ("LaLiga", ["club", "team", "Club", "Team"]),
    "serie-a": ("Serie A", ["club", "team", "Club", "Team"]),
    "ligue1": ("Ligue 1", ["club", "team", "Club", "Team"]),
}
for _slug, (_label, _title_cols) in _SPORTS_TOOLS.items():
    PROFILES[_slug] = IngestProfile(
        "Sports Franchise",
        _title_cols,
        {
            "wikipedia_page": (_WIKI, _url),
            "twitter_handle": (_TW, _handle),
            "instagram_user": (_IG, _handle),
            "facebook_page": (_FB, _url),
            "youtube_channel_username": (_YT, _url),
            "tiktok_user": (_TT, _handle),
        },
        label=_label,
    )


def profile_for(slug: str) -> IngestProfile:
    p = PROFILES.get(slug)
    if p is None:
        raise BdrIngestError(
            f"No ingest profile is defined for '{slug}'. Add one to "
            f"ingest_export.PROFILES (title category + column mapping)."
        )
    return p


# --- conversion ---------------------------------------------------------------
def build_ingest_csv(rows: Iterable[dict], profile: IngestProfile) -> bytes:
    """Map a tool's rows onto ingest columns and serialize as CSV bytes."""
    mapped = []
    for row in rows:
        ingest = profile.ingest_row(row)
        if ingest.get(TITLE):
            mapped.append(ingest)
    if not mapped:
        raise BdrIngestError(
            "No usable titles were found in this report, so there is nothing to "
            "convert. (Check that the report has a name/title column.)"
        )
    # stable column order; always include a social column so the upstream
    # generator takes the full-schema path and honours our explicit values
    cols: list[str] = [TITLE, CATEGORY]
    for m in mapped:
        for k in m:
            if k not in cols:
                cols.append(k)
    if SOCIAL_TRIGGER not in cols:
        cols.append(SOCIAL_TRIGGER)

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    writer.writeheader()
    for m in mapped:
        writer.writerow({c: m.get(c, "") for c in cols})
    return buf.getvalue().encode("utf-8")


def convert_rows_to_ingest(
    rows: Iterable[dict],
    slug: str,
    *,
    enrich: bool = True,
    include_dar: bool = True,
    service: Optional[BdrIngestService] = None,
    progress=None,
) -> dict:
    """Turn a tool's output rows into an ingest-template .xlsx.

    Returns the same shape as BdrIngestService.generate():
      {filename, content, media_type, row_count, enriched_count, ...}
    """
    profile = profile_for(slug)
    rows = list(rows)
    csv_bytes = build_ingest_csv(rows, profile)
    svc = service or BdrIngestService()
    result = svc.generate(
        file_content=csv_bytes,
        filename=f"{slug}_ingest_source.csv",
        title_type=profile.category,
        include_dar=include_dar,
        auto_fetch=enrich,
        progress=progress,
    )
    result["filename"] = f"{slug.replace('-', '_')}_{profile.category.lower().replace(' ', '_').replace('&', 'and')}_ingest.xlsx"
    result["source_label"] = f"{profile.label} -> {profile.category} ingest template"
    result["category"] = profile.category
    return result
