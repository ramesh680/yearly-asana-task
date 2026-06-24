"""Shared social-link helper.

Ensures every row exposes Facebook, Instagram, X/Twitter, YouTube and TikTok.
Verified handles already present on a row are preserved; any missing platform is
auto-generated from the row's best-known handle (an existing verified Twitter or
Instagram username, else derived from the entity name). Auto-generated links are
best-guess and may not all resolve.
"""
import re

PLATFORMS = ["facebook", "instagram", "twitter", "youtube", "tiktok"]
SOCIAL_FIELDS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "X / Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
]

_TMPL = {
    "facebook": "https://www.facebook.com/{h}",
    "instagram": "https://www.instagram.com/{h}",
    "twitter": "https://x.com/{h}",
    "youtube": "https://www.youtube.com/@{h}",
    "tiktok": "https://www.tiktok.com/@{h}",
}


def _user(url):
    if not url:
        return ""
    seg = url.rstrip("/").split("/")[-1]
    return seg.lstrip("@")


def _from_name(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def fill(item, name=""):
    """Fill any missing social platform on ``item`` in place."""
    base = (_user(item.get("twitter")) or _user(item.get("instagram"))
            or _user(item.get("facebook")) or _user(item.get("youtube"))
            or _from_name(name))
    if not base:
        return item
    for p in PLATFORMS:
        if not item.get(p):
            item[p] = _TMPL[p].format(h=base)
    return item
