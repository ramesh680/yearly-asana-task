#!/usr/bin/env python3
"""Refresh the website / Wikipedia / social links for every tool.

For each row of each tool registered in ``tools/link_refresh.py``:

1. Wikipedia - resolves the row's Wikipedia link to the page's current title
   (follows renames/redirects). Rows with no Wikipedia link are looked up by
   name and only accepted when Wikidata confirms the match.
2. Wikidata - reads the page's Wikidata item for the official website and the
   official Facebook / Instagram / X / YouTube / TikTok / LinkedIn / Twitch
   accounts.
3. Website - requests the row's website. Redirects to a new address on the same
   domain are followed and saved; dead sites are replaced with Wikidata's
   official website; blank websites are filled from Wikidata. Social links found
   on the homepage fill any platform Wikidata doesn't have.

Priority per social platform: Wikidata > official homepage > curated snapshot.
Anything still missing keeps the app's existing best-guess fallback.

Results go to ``data/link_refresh.json`` (applied at request time by the app)
and every change is listed in ``data/link_refresh_report.csv``.

Usage:
    python scripts/refresh_links.py                  # all tools
    python scripts/refresh_links.py --tools nba_teams,laliga
    python scripts/refresh_links.py --no-web         # skip website checks
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import importlib
import json
import os
import re
import sys
import time
import threading
from urllib.parse import unquote, urlsplit, parse_qs

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools import link_refresh as LR  # noqa: E402
from tools import socials  # noqa: E402

OUT_JSON = os.path.join(ROOT, "data", "link_refresh.json")
OUT_REPORT = os.path.join(ROOT, "data", "link_refresh_report.csv")

API_UA = "yearly-asana-task-link-refresh/1.0 (+https://github.com/ramesh680/yearly-asana-task)"
WEB_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")

SOCIAL_PLATFORMS = ["facebook", "instagram", "twitter", "youtube", "tiktok", "linkedin", "twitch"]

# Tools whose rows have no Wikipedia link: how to look them up by name.
NAME_LOOKUP = {
    "sephora_brands": {"suffixes": ["", " (brand)", " (cosmetics)", " (company)"],
                       "keywords": ["cosmetic", "beauty", "makeup", "make-up", "skin", "fragrance",
                                    "perfume", "hair", "nail", "brand", "company", "manufacturer",
                                    "personal care", "retailer", "business"]},
    "ulta_brands": {"suffixes": ["", " (brand)", " (cosmetics)", " (company)"],
                    "keywords": ["cosmetic", "beauty", "makeup", "make-up", "skin", "fragrance",
                                 "perfume", "hair", "nail", "brand", "company", "manufacturer",
                                 "personal care", "retailer", "business"]},
    "twitch_streamers": {"suffixes": [""], "keywords": [], "twitch_id": True},
}

session = requests.Session()
_local = threading.local()


def web_session():
    if not hasattr(_local, "s"):
        _local.s = requests.Session()
    return _local.s


# ------------------------------------------------------------------ helpers
def log(*a):
    print(*a, flush=True)


def chunks(seq, n):
    seq = list(seq)
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def api_get(url, params, tries=5):
    params = dict(params, format="json", formatversion=2, maxlag=5)
    for attempt in range(tries):
        try:
            r = session.get(url, params=params, headers={"User-Agent": API_UA}, timeout=60)
            if r.status_code == 429 or r.status_code >= 500:
                raise requests.HTTPError(str(r.status_code))
            data = r.json()
            if data.get("error", {}).get("code") == "maxlag":
                raise requests.HTTPError("maxlag")
            return data
        except (requests.RequestException, ValueError) as e:
            wait = 2 ** attempt
            log("  api retry in {}s ({})".format(wait, e))
            time.sleep(wait)
    return {}


def registrable(host):
    host = (host or "").lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 3 and (parts[-2] in ("co", "com", "org", "net", "ac", "gov", "edu") and len(parts[-1]) == 2):
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def loose(url):
    """Comparison form: no scheme, no www, no trailing slash, lowercase host."""
    if not url:
        return ""
    p = urlsplit(url if "://" in url else "https://" + url)
    host = p.netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    return host + p.path.rstrip("/")


# ---------------------------------------------------------------- Wikipedia
def wiki_title(url):
    """Return (lang, title, is_search) from a Wikipedia URL."""
    if not url:
        return None
    p = urlsplit(url)
    m = re.match(r"([a-z\-]+)\.(?:m\.)?wikipedia\.org$", p.netloc.lower())
    if not m:
        return None
    lang = m.group(1)
    q = parse_qs(p.query)
    if p.path.startswith("/wiki/"):
        title = unquote(p.path[len("/wiki/"):]).replace("_", " ")
        if title.startswith("Special:Search"):
            term = (q.get("search") or [title.split("/", 1)[-1]])[0]
            return lang, term, True
        return lang, title, False
    if "search" in q:
        return lang, q["search"][0], True
    if "title" in q:
        return lang, q["title"][0].replace("_", " "), False
    return None


def wiki_url(lang, title, fragment=""):
    # readable form like the curated data (accents kept); only escape URL-breaking characters
    t = title.replace(" ", "_").replace("%", "%25").replace("?", "%3F").replace("#", "%23")
    return "https://{}.wikipedia.org/wiki/{}".format(lang, t) + ("#" + fragment.replace(" ", "_") if fragment else "")


def resolve_titles(lang, titles):
    """Map input title -> {title, qid, missing, disambig, fragment}."""
    api = "https://{}.wikipedia.org/w/api.php".format(lang)
    out = {}
    for batch in chunks(sorted(set(titles)), 50):
        data = api_get(api, {"action": "query", "redirects": 1, "prop": "pageprops",
                             "ppprop": "wikibase_item|disambiguation", "titles": "|".join(batch)})
        q = data.get("query", {})
        norm_map = {n["from"]: n["to"] for n in q.get("normalized", [])}
        redir = {r["from"]: (r["to"], r.get("tofragment", "")) for r in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for t in batch:
            cur, frag = norm_map.get(t, t), ""
            hops = 0
            while cur in redir and hops < 5:
                cur, frag = redir[cur][0], redir[cur][1] or frag
                hops += 1
            p = pages.get(cur, {})
            pp = p.get("pageprops", {}) or {}
            out[t] = {"title": cur, "fragment": frag, "missing": bool(p.get("missing") or p.get("invalid") or not p),
                      "qid": pp.get("wikibase_item"), "disambig": "disambiguation" in pp}
    return out


def search_title(lang, term):
    data = api_get("https://{}.wikipedia.org/w/api.php".format(lang),
                   {"action": "query", "list": "search", "srsearch": term, "srlimit": 1})
    hits = data.get("query", {}).get("search", [])
    return hits[0]["title"] if hits else None


# ----------------------------------------------------------------- Wikidata
WD_API = "https://www.wikidata.org/w/api.php"
PROPS = {"P856": "website", "P2013": "facebook", "P2003": "instagram", "P2002": "twitter",
         "P11245": "youtube_handle", "P2397": "youtube_channel", "P7085": "tiktok",
         "P4264": "linkedin", "P5797": "twitch"}


def _best_value(statements, prefer_english=False):
    good = []
    for s in statements or []:
        if s.get("rank") == "deprecated":
            continue
        if "P582" in (s.get("qualifiers") or {}):  # has an end date -> no longer current
            continue
        dv = (s.get("mainsnak") or {}).get("datavalue") or {}
        v = dv.get("value")
        if not isinstance(v, str) or not v.strip():
            continue
        score = 2 if s.get("rank") == "preferred" else 1
        if prefer_english:
            langs = [((q.get("datavalue") or {}).get("value") or {}).get("id")
                     for q in (s.get("qualifiers") or {}).get("P407", [])]
            if "Q1860" in langs:
                score += 0.5
        good.append((score, v.strip()))
    if not good:
        return ""
    good.sort(key=lambda x: -x[0])
    return good[0][1]


def wikidata_entities(qids):
    out = {}
    for batch in chunks(sorted(set(q for q in qids if q)), 50):
        data = api_get(WD_API, {"action": "wbgetentities", "ids": "|".join(batch),
                                "props": "claims|descriptions|labels|aliases", "languages": "en"})
        for qid, ent in (data.get("entities") or {}).items():
            claims = ent.get("claims") or {}
            vals = {name: _best_value(claims.get(pid), prefer_english=(pid == "P856"))
                    for pid, name in PROPS.items()}
            links = {}
            if vals["website"]:
                links["website"] = vals["website"]
            if vals["facebook"]:
                links["facebook"] = "https://www.facebook.com/" + vals["facebook"]
            if vals["instagram"]:
                links["instagram"] = "https://www.instagram.com/" + vals["instagram"]
            if vals["twitter"]:
                links["twitter"] = "https://x.com/" + vals["twitter"]
            if vals["youtube_handle"]:
                links["youtube"] = "https://www.youtube.com/@" + vals["youtube_handle"].lstrip("@")
            elif vals["youtube_channel"]:
                links["youtube"] = "https://www.youtube.com/channel/" + vals["youtube_channel"]
            if vals["tiktok"]:
                links["tiktok"] = "https://www.tiktok.com/@" + vals["tiktok"].lstrip("@")
            if vals["linkedin"]:
                links["linkedin"] = "https://www.linkedin.com/company/" + vals["linkedin"]
            if vals["twitch"]:
                links["twitch"] = "https://www.twitch.tv/" + vals["twitch"]
            label = ((ent.get("labels") or {}).get("en") or {}).get("value", "")
            aliases = [a.get("value", "") for a in (ent.get("aliases") or {}).get("en", [])]
            desc = ((ent.get("descriptions") or {}).get("en") or {}).get("value", "")
            out[qid] = {"links": links, "label": label, "aliases": aliases, "description": desc,
                        "twitch_id": vals["twitch"].lower()}
    return out


def wikidata_by_twitch(channel):
    data = api_get(WD_API, {"action": "query", "list": "search", "srlimit": 2,
                            "srsearch": "haswbstatement:P5797={}".format(channel)})
    hits = data.get("query", {}).get("search", [])
    return hits[0]["title"] if len(hits) == 1 else None


def enwiki_for_qid(qids):
    out = {}
    for batch in chunks(sorted(set(qids)), 50):
        data = api_get(WD_API, {"action": "wbgetentities", "ids": "|".join(batch),
                                "props": "sitelinks", "sitefilter": "enwiki"})
        for qid, ent in (data.get("entities") or {}).items():
            sl = (ent.get("sitelinks") or {}).get("enwiki")
            if sl:
                out[qid] = sl["title"]
    return out


# ------------------------------------------------------------------ website
SOCIAL_RE = re.compile(
    r"""href=["'](https?://(?:www\.|m\.|[a-z]{2}\.)?"""
    r"""(facebook\.com|instagram\.com|twitter\.com|x\.com|youtube\.com|tiktok\.com|linkedin\.com|twitch\.tv)"""
    r"""/[^"'\s<>]*)""", re.I)
SOCIAL_BAD = re.compile(r"/(sharer|share|intent|plugins|dialog|hashtag|explore|p|reel|reels|watch|embed|"
                        r"status|home|login|signup|legal|privacy|policies|help|search|i|tr|video|shorts|"
                        r"playlist|feed|groups|events|photo|photos|stories|tag)(/|$|\?)", re.I)


def social_from_html(html):
    found = {}
    for m in SOCIAL_RE.finditer(html or ""):
        url, dom = m.group(1), m.group(2).lower()
        p = urlsplit(url)
        segs = [s for s in p.path.split("/") if s]
        if not segs or SOCIAL_BAD.search("/" + segs[0] + "/"):
            continue
        if dom in ("twitter.com", "x.com"):
            plat, canon = "twitter", "https://x.com/" + segs[0]
        elif dom == "facebook.com":
            if segs[0] in ("pages", "profile.php", "people"):
                continue
            plat, canon = "facebook", "https://www.facebook.com/" + segs[0]
        elif dom == "instagram.com":
            plat, canon = "instagram", "https://www.instagram.com/" + segs[0]
        elif dom == "tiktok.com":
            if not segs[0].startswith("@"):
                continue
            plat, canon = "tiktok", "https://www.tiktok.com/" + segs[0]
        elif dom == "youtube.com":
            if segs[0].startswith("@"):
                canon = "https://www.youtube.com/" + segs[0]
            elif segs[0] in ("channel", "c", "user") and len(segs) > 1:
                canon = "https://www.youtube.com/{}/{}".format(segs[0], segs[1])
            else:
                continue
            plat = "youtube"
        elif dom == "linkedin.com":
            if segs[0] not in ("company", "school") or len(segs) < 2:
                continue
            plat, canon = "linkedin", "https://www.linkedin.com/{}/{}".format(segs[0], segs[1])
        elif dom == "twitch.tv":
            plat, canon = "twitch", "https://www.twitch.tv/" + segs[0]
        else:
            continue
        canon = canon.split("?")[0].split("#")[0]
        found.setdefault(plat, {})
        found[plat][canon] = found[plat].get(canon, 0) + 1
    return {p: max(c.items(), key=lambda kv: kv[1])[0] for p, c in found.items()}


BLOCKED = {401, 403, 405, 406, 409, 429, 451, 503, 520, 521, 522, 523, 525, 526, 999}


def check_site(url):
    """Return dict(status=ok|blocked|dead|unknown, final=url, code=int, html=str)."""
    if not url:
        return {"status": "none"}
    if "://" not in url:
        url = "https://" + url
    last = None
    for attempt in range(2):
        try:
            r = web_session().get(url, headers={"User-Agent": WEB_UA, "Accept": "text/html,*/*;q=0.8",
                                          "Accept-Language": "en-US,en;q=0.9"},
                            timeout=(10, 25), allow_redirects=True, stream=True)
            html = ""
            if "html" in (r.headers.get("content-type") or "") and r.status_code < 400:
                raw = r.raw.read(1_500_000, decode_content=True) or b""
                html = raw.decode(r.encoding or "utf-8", errors="ignore")
            r.close()
            code = r.status_code
            if code < 400:
                return {"status": "ok", "final": r.url, "code": code, "html": html}
            if code in BLOCKED:
                return {"status": "blocked", "final": r.url, "code": code}
            if code in (404, 410):
                last = {"status": "dead", "final": r.url, "code": code}
            else:
                last = {"status": "unknown", "final": r.url, "code": code}
        except requests.exceptions.SSLError as e:
            last = {"status": "unknown", "error": "ssl: " + str(e)[:120]}
        except requests.exceptions.ConnectionError as e:
            msg = str(e)
            dns = any(s in msg for s in ("NameResolution", "Name or service not known",
                                         "nodename nor servname", "getaddrinfo", "No address associated"))
            last = {"status": "dead" if dns else "unknown", "error": msg[:160]}
        except requests.RequestException as e:
            last = {"status": "unknown", "error": str(e)[:160]}
        time.sleep(1.5)
    return last


BAD_FINAL = re.compile(r"(login|signin|sign-in|consent|captcha|404|not-found|error|cookie|unsupported|"
                       r"maintenance|blocked|access-denied)", re.I)
LOCALE_PATH = re.compile(r"^/?([a-z]{2}([-_][a-z]{2})?)(/([a-z]{2}([-_][a-z]{2})?))?/?(index\.html?)?$", re.I)


def updated_website(orig, res, wd_site):
    """Decide the new website from a check result. Returns (url, reason) or (None, flag)."""
    final = res.get("final") or ""
    if res["status"] in ("ok",) and final:
        fp, op = urlsplit(final), urlsplit(orig if "://" in orig else "https://" + orig)
        if BAD_FINAL.search(fp.path):
            return None, ""
        same = registrable(fp.netloc) == registrable(op.netloc)
        to_wd = wd_site and registrable(fp.netloc) == registrable(urlsplit(wd_site).netloc)
        if not (same or to_wd):
            return None, "redirects off-site to " + final
        orig_root = op.path in ("", "/") or LOCALE_PATH.match(op.path or "")
        if orig_root:
            new = "{}://{}/".format(fp.scheme, fp.netloc)  # don't pin geo/locale landing paths
        else:
            new = "{}://{}{}".format(fp.scheme, fp.netloc, fp.path)
        if loose(new) != loose(orig) or (op.scheme == "http" and fp.scheme == "https"):
            return new, "redirect"
        return None, ""
    return None, ""


# ---------------------------------------------------------------- main flow
def load_rows(mod_name, getter, args):
    module = importlib.import_module("tools." + mod_name)
    fn = getattr(module, getter)
    fn = getattr(fn, "_link_refresh_original", fn)
    rows_filled, meta = fn(*args)
    # same rows without the auto-guessed social handles -> what is actually curated
    orig_fill = socials.fill
    socials.fill = lambda item, name="": item
    try:
        rows_raw, _ = fn(*args)
    finally:
        socials.fill = orig_fill
    return module, rows_filled, rows_raw, meta


def name_matches(name, ent):
    n = LR.norm(name)
    cands = [LR.norm(ent.get("label", ""))] + [LR.norm(a) for a in ent.get("aliases", [])]
    return bool(n) and any(c == n or (len(n) >= 5 and c.startswith(n)) or (len(c) >= 5 and n.startswith(c))
                           for c in cands if c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", default="", help="comma-separated overlay keys (default: all)")
    ap.add_argument("--no-web", action="store_true", help="skip website checks / homepage scraping")
    ap.add_argument("--workers", type=int, default=24)
    a = ap.parse_args()
    wanted = {t.strip() for t in a.tools.split(",") if t.strip()}

    previous = {}
    if os.path.exists(OUT_JSON):
        try:
            previous = json.load(open(OUT_JSON, encoding="utf-8")).get("tools", {})
        except ValueError:
            previous = {}

    # ---- 1. gather rows
    items = []  # one dict per row
    for key, mod_name, getter, args in LR.REGISTRY:
        if wanted and key not in wanted:
            continue
        module, filled, raw, meta = load_rows(mod_name, getter, args)
        field = LR.name_field(module, meta)
        for rk, rf, rr in zip(LR.row_keys(filled, field), filled, raw):
            items.append({"tool": key, "rk": rk, "name": str(rf.get(field) or ""),
                          "filled": rf, "raw": rr, "new": {}, "notes": []})
        log("{:<24} {:>5} rows".format(key, len(filled)))
    log("Total rows: {}".format(len(items)))

    # ---- 2. Wikipedia: resolve existing links
    by_lang = {}
    for it in items:
        wt = wiki_title(it["raw"].get("wikipedia") or "")
        if wt:
            lang, title, is_search = wt
            if is_search:
                found = search_title(lang, title)
                if not found:
                    it["notes"].append("wikipedia search found nothing")
                    continue
                title = found
            it["wt"] = (lang, title)
            by_lang.setdefault(lang, set()).add(title)
    resolved = {}
    for lang, titles in by_lang.items():
        log("Resolving {} {}.wikipedia titles".format(len(titles), lang))
        for t, info in resolve_titles(lang, titles).items():
            resolved[(lang, t)] = info
    for it in items:
        if "wt" not in it:
            continue
        lang, title = it["wt"]
        info = resolved.get((lang, title))
        if not info or info["missing"]:
            it["notes"].append("wikipedia page not found: " + title)
            continue
        if info["disambig"]:
            it["notes"].append("wikipedia link is a disambiguation page: " + title)
            continue
        it["qid"] = info["qid"]
        new_url = wiki_url(lang, info["title"], info["fragment"])
        if info["title"] != title or info["fragment"] or "Special:Search" in (it["raw"].get("wikipedia") or ""):
            it["new"]["wikipedia"] = (new_url, "wikipedia page renamed/redirected")

    # ---- 3. Wikipedia: look up rows that have none, by name
    lookups = [it for it in items if not it["raw"].get("wikipedia") and it["tool"] in NAME_LOOKUP]
    if lookups:
        log("Looking up {} rows without a Wikipedia link".format(len(lookups)))
        cand_titles = set()
        for it in lookups:
            cfg = NAME_LOOKUP[it["tool"]]
            if cfg.get("twitch_id"):
                ch = (it["raw"].get("twitch") or "").rstrip("/").split("/")[-1] or it["name"]
                it["twitch_ch"] = ch.lower()
                continue
            bases = [it["name"]]
            short = re.split(r"\s+(?:by|x)\s+", it["name"], maxsplit=1, flags=re.I)[0].strip()
            if short and short != it["name"]:
                bases.append(short)  # "Fenty Beauty by Rihanna" -> "Fenty Beauty"
            it["cands"] = [b + s for b in bases for s in cfg["suffixes"] if b]
            cand_titles.update(it["cands"])
        info = resolve_titles("en", cand_titles) if cand_titles else {}
        twitch_q = {}
        for it in lookups:
            if it.get("twitch_ch"):
                q = wikidata_by_twitch(it["twitch_ch"])
                if q:
                    twitch_q[it["rk"]] = q
                    it["cand_qids"] = [(q, None)]
                continue
            it["cand_qids"] = [(info[c]["qid"], info[c]["title"]) for c in it.get("cands", [])
                               if c in info and not info[c]["missing"] and not info[c]["disambig"] and info[c]["qid"]]
        cand_ents = wikidata_entities({q for it in lookups for q, _t in it.get("cand_qids", [])})
        enwiki = enwiki_for_qid(list(twitch_q.values())) if twitch_q else {}
        for it in lookups:
            cfg = NAME_LOOKUP[it["tool"]]
            for qid, title in it.get("cand_qids", []):
                ent = cand_ents.get(qid)
                if not ent:
                    continue
                if cfg.get("twitch_id"):
                    ok = ent["twitch_id"] == it["twitch_ch"]
                    title = enwiki.get(qid)
                else:
                    desc = ent["description"].lower()
                    ok = name_matches(it["name"], ent) and any(k in desc for k in cfg["keywords"])
                if not ok:
                    continue
                it["qid"] = qid
                if title:
                    it["new"]["wikipedia"] = (wiki_url("en", title), "matched by name, confirmed on Wikidata")
                break

    # ---- 4. Wikidata: official website + socials
    ents = wikidata_entities({it.get("qid") for it in items if it.get("qid")})
    log("Fetched {} Wikidata items".format(len(ents)))
    for it in items:
        it["wd"] = (ents.get(it.get("qid")) or {}).get("links", {})

    # ---- 5. Websites
    def site_job(it):
        orig = it["raw"].get("website") or ""
        wd_site = it["wd"].get("website", "")
        res = check_site(orig) if orig else {"status": "none"}
        it["site"] = res
        new, why = None, ""
        if orig and res["status"] == "ok":
            new, flag = updated_website(orig, res, wd_site)
            if new:
                why = "website redirects to new address"
            elif flag:
                it["notes"].append(flag)
        if (not orig or res["status"] == "dead" or (orig and res["status"] == "ok" and not new
                                                     and any(n.startswith("redirects off-site") for n in it["notes"]))) \
                and wd_site and loose(wd_site) != loose(orig):
            res2 = check_site(wd_site)
            if res2["status"] in ("ok", "blocked", "unknown"):
                new = wd_site
                why = "filled from Wikidata" if not orig else "old site {} - replaced with Wikidata official site".format(
                    "dead" if res["status"] == "dead" else "moved")
                if res2["status"] == "ok":
                    better, _ = updated_website(wd_site, res2, wd_site)
                    new = better or wd_site
                    res = res2
                    it["site"] = res2
        elif orig and res["status"] == "dead" and not new:
            it["notes"].append("website looks dead ({}) and Wikidata has no replacement".format(
                res.get("code") or res.get("error", "")[:60]))
        if new:
            it["new"]["website"] = (new, why)
        # homepage socials (only for sites on their own domain, not league sub-pages)
        home = it["new"].get("website", (orig, ""))[0]
        hp = urlsplit(home if "://" in home else "https://" + home) if home else None
        if res.get("html") and hp and (hp.path in ("", "/") or LOCALE_PATH.match(hp.path)):
            it["home_socials"] = social_from_html(res["html"])
        return it

    if not a.no_web:
        targets = [it for it in items if it["raw"].get("website") or it["wd"].get("website")]
        log("Checking {} websites with {} workers".format(len(targets), a.workers))
        done = 0
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for _ in ex.map(site_job, targets):
                done += 1
                if done % 100 == 0:
                    log("  {} / {}".format(done, len(targets)))
    else:
        for it in items:
            if not it["raw"].get("website") and it["wd"].get("website"):
                it["new"]["website"] = (it["wd"]["website"], "filled from Wikidata (not checked)")

    # ---- 6. Socials: Wikidata > homepage > curated
    for it in items:
        home = it.get("home_socials", {})
        for p in SOCIAL_PLATFORMS:
            cur_filled = it["filled"].get(p) or ""
            curated = it["raw"].get(p) or ""
            val, why = "", ""
            if it["wd"].get(p):
                val, why = it["wd"][p], "Wikidata"
            elif home.get(p) and not curated:
                val, why = home[p], "official homepage"
            if val and loose(val).lower() != loose(cur_filled).lower():
                it["new"][p] = (val, why)

    # ---- 7. Write overlay + report
    out_tools, report = {}, []
    for it in items:
        tool = out_tools.setdefault(it["tool"], {"rows": {}})
        if it["new"]:
            tool["rows"][it["rk"]] = dict({"name": it["name"]}, **{f: v for f, (v, _w) in it["new"].items()})
        for f, (v, why) in sorted(it["new"].items()):
            old = it["filled"].get(f) or ""
            report.append([it["tool"], it["name"], f, old, v, why])
        for n in it["notes"]:
            report.append([it["tool"], it["name"], "FLAG", "", "", n])
    # keep results for tools not refreshed in this run
    for k, v in previous.items():
        if k not in out_tools:
            out_tools[k] = v

    stats = {}
    for it in items:
        s = stats.setdefault(it["tool"], {"rows": 0, "changed": 0, "flags": 0})
        s["rows"] += 1
        s["changed"] += 1 if it["new"] else 0
        s["flags"] += len(it["notes"])
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    payload = {"generated": now, "stats": stats, "tools": dict(sorted(out_tools.items()))}
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    with open(OUT_REPORT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tool", "name", "field", "old", "new", "reason"])
        w.writerows(report)

    # summary
    lines = ["| Tool | Rows | Rows updated | Flags |", "|---|---:|---:|---:|"]
    for k, s in stats.items():
        lines.append("| {} | {} | {} | {} |".format(k, s["rows"], s["changed"], s["flags"]))
    by_field = {}
    for r in report:
        by_field[r[2]] = by_field.get(r[2], 0) + 1
    lines.append("")
    lines.append("Changes by field: " + ", ".join("{} {}".format(k, v) for k, v in sorted(by_field.items())))
    summary = "\n".join(lines)
    log(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("## Link refresh " + now + "\n\n" + summary + "\n")


if __name__ == "__main__":
    main()
