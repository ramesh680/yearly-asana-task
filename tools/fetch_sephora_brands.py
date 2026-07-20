"""
fetch_sephora_brands.py  --  run this LOCALLY (on your Windows laptop) to pull
the full A-Z brand list from Sephora and write sephora_brands.json, which the
Sephora Brands tool then serves.

Why local?  Sephora's brand list is JavaScript-rendered behind Akamai bot
protection, so a cloud host (Render) or a plain server-side fetch only gets the
empty page shell. Running from your own machine -- optionally with your logged-in
browser cookie -- gets past that, the same way your Zendesk extension reuses the
session cookie.

Usage (Windows, your py launcher / Python 3.14):
    py fetch_sephora_brands.py

If Akamai blocks the plain request, paste your browser cookie:
    1. Open https://www.sephora.com/brands-list in Chrome while signed in.
    2. DevTools (F12) -> Network -> click the brands-list request ->
       Headers -> Request Headers -> copy the whole "cookie:" value.
    3. Run:
         set SEPHORA_COOKIE=<paste the cookie value>
         py fetch_sephora_brands.py
   (PowerShell:  $env:SEPHORA_COOKIE = "<cookie>"  )

Output: sephora_brands.json next to this script. Commit + push it so Render
redeploys with the fresh list (same flow as your Media Tools Hub edits).

Zero third-party dependencies (stdlib only). `requests` is used automatically if
installed, otherwise urllib.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(HERE, "sephora_brands.json")

BASE = "https://www.sephora.com"
# Sephora's internal endpoints have shifted over time, so we try several and
# fall back to scraping brand data embedded in the HTML page.
API_CANDIDATES = [
    "https://www.sephora.com/api/catalog/brands/list",
    "https://www.sephora.com/api/catalog/brands",
    "https://www.sephora.com/api/v2/catalog/brands/list",
]
PAGE_URL = "https://www.sephora.com/brands-list"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": PAGE_URL,
}


# --------------------------------------------------------------------------- #
# HTTP (requests if available, else urllib)
# --------------------------------------------------------------------------- #
def _get(url: str, cookie: str | None) -> tuple[int, str]:
    headers = dict(HEADERS)
    if cookie:
        headers["Cookie"] = cookie
    try:
        import requests  # type: ignore

        r = requests.get(url, headers=headers, timeout=30)
        return r.status_code, r.text
    except ImportError:
        import urllib.error
        import urllib.request

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.getcode(), resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            return 0, f"__error__ {e}"


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #
def _walk_for_brands(obj, found: dict) -> None:
    """Recursively collect {displayName: seo/targetUrl} pairs from any JSON."""
    if isinstance(obj, dict):
        name = obj.get("displayName") or obj.get("brandName") or obj.get("name")
        url = (
            obj.get("targetUrl")
            or obj.get("seoName")
            or obj.get("brandSeoName")
            or obj.get("url")
        )
        looks_like_brand = (
            isinstance(name, str)
            and isinstance(url, str)
            and "/brand/" in str(url)
        )
        if looks_like_brand and name.strip():
            found[name.strip()] = url
        for v in obj.values():
            _walk_for_brands(v, found)
    elif isinstance(obj, list):
        for v in obj:
            _walk_for_brands(v, found)


def parse_json_payload(text: str) -> list[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    found: dict[str, str] = {}
    _walk_for_brands(data, found)
    return sorted(found.keys(), key=str.lower)


def parse_html_page(html: str) -> list[str]:
    """Pull brand names from JSON blobs embedded in the brands-list HTML."""
    names: dict[str, str] = {}
    # 1) Any embedded application/json or __PRELOADED_STATE__ style blobs
    for m in re.finditer(
        r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
        html,
        re.DOTALL,
    ):
        try:
            _walk_for_brands(json.loads(m.group(1)), names)
        except Exception:  # noqa: BLE001
            pass
    for m in re.finditer(r'(?:__PRELOADED_STATE__|linkStore)\s*=\s*(\{.*?\});', html, re.DOTALL):
        try:
            _walk_for_brands(json.loads(m.group(1)), names)
        except Exception:  # noqa: BLE001
            pass
    # 2) Fallback: anchors like <a href="/brand/rare-beauty">Rare Beauty</a>
    if not names:
        for m in re.finditer(
            r'href="(/brand/[a-z0-9\-]+)"[^>]*>\s*([^<]{2,60}?)\s*</a>', html
        ):
            label = re.sub(r"\s+", " ", m.group(2)).strip()
            if label and not label.lower().startswith(("shop", "view", "see")):
                names[label] = m.group(1)
    return sorted(names.keys(), key=str.lower)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def fetch() -> tuple[list[str], str]:
    cookie = os.environ.get("SEPHORA_COOKIE") or None
    if len(sys.argv) > 1 and sys.argv[1].startswith("--cookie="):
        cookie = sys.argv[1].split("=", 1)[1]

    for api in API_CANDIDATES:
        print(f"→ trying API: {api}")
        code, text = _get(api, cookie)
        print(f"   status {code}, {len(text)} bytes")
        if code == 200:
            brands = parse_json_payload(text)
            if brands:
                return brands, api
        time.sleep(1.0)

    print(f"→ falling back to HTML page: {PAGE_URL}")
    code, html = _get(PAGE_URL, cookie)
    print(f"   status {code}, {len(html)} bytes")
    if code == 200:
        brands = parse_html_page(html)
        if brands:
            return brands, PAGE_URL

    return [], ""


def main() -> int:
    brands, source = fetch()
    if not brands:
        print(
            "\n✗ Could not extract brands. Sephora likely served a bot-check\n"
            "  page. Re-run with your browser cookie (see the header of this\n"
            "  file). The tool will keep serving its existing snapshot until a\n"
            "  successful run overwrites sephora_brands.json."
        )
        return 1

    payload = {
        "source": source,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(brands),
        "brands": brands,
    }
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print(f"\n✓ {len(brands)} brands written to {OUT_FILE}")
    print(f"  first: {brands[0]}   last: {brands[-1]}")
    print("  Commit & push sephora_brands.json so Render redeploys with it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
