#!/usr/bin/env python3
"""
Refresh the Russell 3000 dataset for the "Yearly Asana task" hub.

  1. Fetches the CURRENT Russell 3000 constituents (iShares IWV holdings feed,
     the standard public proxy), with a committed-CSV fallback if it's blocked.
  2. Enriches each company with official website, English Wikipedia page, and
     social handles (Facebook, Instagram, X, YouTube, LinkedIn) via the
     Wikipedia + Wikidata public APIs.
  3. INCREMENTAL: companies already enriched in data/russell_3000.json keep
     their metadata; only newly-added tickers get fresh lookups; dropped
     tickers are removed.
  4. Writes data/russell_3000.json + russell3000_full.csv and regenerates the
     self-contained templates/russell-3000.html (data baked in, "as of" stamp).

Safety: if the constituent count is < MIN_CONSTITUENTS the run aborts WITHOUT
overwriting existing data.

Usage:
  python scripts/refresh_russell3000.py            # incremental, live + CSV fallback
  python scripts/refresh_russell3000.py --full     # re-enrich every company
  python scripts/refresh_russell3000.py --csv data/IWV_holdings.csv   # use CSV only
"""
import csv, json, os, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    sys.exit("requests is required:  pip install requests")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")
TPL_DIR = os.path.join(ROOT, "templates")
DATA_JSON = os.path.join(DATA_DIR, "russell_3000.json")
DATA_CSV = os.path.join(DATA_DIR, "russell3000_full.csv")
PAGE_HTML = os.path.join(TPL_DIR, "russell-3000.html")

IWV_URL = ("https://www.ishares.com/us/products/239714/ishares-russell-3000-etf/"
           "1467271812596.ajax?fileType=json&fileName=IWV_holdings&dataType=fund")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
WIKI_UA = "RussellRefresh/1.0 (yearly-asana-task; data refresh bot)"
MIN_CONSTITUENTS = 2000
VERIFIED_TOP = 640
IWV_CSV = os.path.join(DATA_DIR, "IWV_holdings.csv")
CSV_PATH = None

SESS = requests.Session()

# ----------------------------------------------------------------- 1. fetch
def fetch_constituents():
    """Live iShares feed first, committed CSV fallback if it fails/blocked."""
    if CSV_PATH:
        print("using forced CSV:", CSV_PATH)
        return parse_holdings_csv(CSV_PATH)
    try:
        rows = _fetch_live()
        if len(rows) >= MIN_CONSTITUENTS:
            return rows
        print("live feed returned only %d rows; trying CSV fallback" % len(rows))
    except Exception as e:
        print("live fetch failed (%s); trying CSV fallback" % e)
    if os.path.exists(IWV_CSV):
        print("using committed CSV fallback:", IWV_CSV)
        return parse_holdings_csv(IWV_CSV)
    raise RuntimeError("live fetch failed and no fallback CSV at %s" % IWV_CSV)

def _fetch_live():
    r = SESS.get(IWV_URL, headers={"User-Agent": UA, "Accept": "application/json"},
                 timeout=60)
    txt = r.text.lstrip("﻿").strip()
    if not txt.startswith("{"):
        raise RuntimeError("iShares did not return JSON (likely anti-bot HTML)")
    data = json.loads(txt)
    rows = data.get("aaData") or data.get("data") or []
    out = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 6:
            continue
        ticker = (row[0] or "").strip()
        name = (row[1] or "").strip()
        acl = ""
        for c in row[2:5]:
            if isinstance(c, str) and c.lower() in ("equity", "fixed income", "cash",
                                                    "money market", "futures"):
                acl = c.lower()
        if acl and acl != "equity":
            continue
        sector = ""
        for c in row[2:5]:
            if isinstance(c, str) and c and c.lower() != "equity":
                sector = c; break
        weight = _num(row[5])
        if weight is None:
            for c in row:
                w = _num(c)
                if w is not None and 0 <= w <= 100:
                    weight = w; break
        if not ticker or not name:
            continue
        out.append({"ticker": ticker.replace(".", "").upper(), "name": name,
                    "sector": sector or "—",
                    "weight": weight if weight is not None else 0.0})
    return _dedup(out)

def parse_holdings_csv(path):
    """Parse an iShares IWV_holdings.csv (with metadata preamble) -> equities."""
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        lines = f.read().splitlines()
    hdr_i = None
    for i, ln in enumerate(lines):
        low = ln.lower()
        if low.startswith("ticker,") and "weight" in low:
            hdr_i = i; break
    if hdr_i is None:
        raise RuntimeError("could not find holdings header row in %s" % path)
    reader = csv.DictReader(lines[hdr_i:])
    def col(d, *names):
        for n in names:
            for k in d:
                if k and k.strip().lower() == n:
                    return d[k]
        return ""
    out = []
    for d in reader:
        ticker = (col(d, "ticker") or "").strip()
        name = (col(d, "name") or "").strip()
        acl = (col(d, "asset class") or "").strip().lower()
        if acl and acl != "equity":
            continue
        if not ticker or not name or ticker.lower() == "ticker":
            continue
        sector = (col(d, "sector") or "").strip() or "—"
        weight = _num(col(d, "weight (%)", "weight"))
        out.append({"ticker": ticker.replace(".", "").upper(), "name": name,
                    "sector": sector, "weight": weight if weight is not None else 0.0})
    return _dedup(out)

def _dedup(out):
    best = {}
    for c in out:
        if c["ticker"] not in best or c["weight"] > best[c["ticker"]]["weight"]:
            best[c["ticker"]] = c
    return list(best.values())

def _num(v):
    if isinstance(v, dict):
        v = v.get("raw", v.get("display"))
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.replace(",", "").replace("%", "").strip()
        try: return float(s)
        except ValueError: return None
    return None

# ------------------------------------------------------------- 2. enrichment
def wiki_qid(name):
    for attempt in range(3):
        try:
            r = SESS.get("https://en.wikipedia.org/w/api.php",
                         params={"action": "query", "format": "json",
                                 "generator": "search", "gsrsearch": name,
                                 "gsrlimit": 1, "prop": "pageprops",
                                 "ppprop": "wikibase_item"},
                         headers={"User-Agent": WIKI_UA}, timeout=30)
            pages = ((r.json().get("query") or {}).get("pages") or {})
            for p in pages.values():
                slug = p.get("title", "").replace(" ", "_")
                qid = (p.get("pageprops") or {}).get("wikibase_item")
                return qid, slug
            return None, None
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return None, None

SPARQL = """SELECT ?c ?web ?article
 (SAMPLE(?fb) AS ?f)(SAMPLE(?ig) AS ?i)(SAMPLE(?tw) AS ?t)(SAMPLE(?yt) AS ?y)(SAMPLE(?li) AS ?l)
WHERE {{
  VALUES ?c {{ {values} }}
  OPTIONAL {{ ?c wdt:P856 ?web }}
  OPTIONAL {{ ?article schema:about ?c ; schema:isPartOf <https://en.wikipedia.org/> }}
  OPTIONAL {{ ?c wdt:P2013 ?fb }} OPTIONAL {{ ?c wdt:P2003 ?ig }}
  OPTIONAL {{ ?c wdt:P2002 ?tw }} OPTIONAL {{ ?c wdt:P2397 ?yt }}
  OPTIONAL {{ ?c wdt:P4264 ?li }}
}} GROUP BY ?c ?web ?article"""

def wikidata_batch(qids):
    out = {}
    for i in range(0, len(qids), 100):
        chunk = qids[i:i + 100]
        vals = " ".join("wd:" + q for q in chunk)
        for attempt in range(3):
            try:
                r = SESS.get("https://query.wikidata.org/sparql",
                             params={"format": "json", "query": SPARQL.format(values=vals)},
                             headers={"User-Agent": WIKI_UA,
                                      "Accept": "application/sparql-results+json"},
                             timeout=60)
                for b in r.json()["results"]["bindings"]:
                    qid = b["c"]["value"].rsplit("/", 1)[-1]
                    rec = out.setdefault(qid, {})
                    if "web" in b and "web" not in rec: rec["web"] = b["web"]["value"]
                    if "article" in b and "article" not in rec: rec["article"] = b["article"]["value"]
                    for k, c in (("fb","f"),("ig","i"),("tw","t"),("yt","y"),("li","l")):
                        if c in b and not rec.get(k): rec[k] = b[c]["value"]
                break
            except Exception:
                time.sleep(2 * (attempt + 1))
        time.sleep(0.3)
    return out

def social_urls(rec):
    def u(kind, key):
        v = (rec.get(key) or "").strip()
        if not v: return ""
        return {"fb": "https://www.facebook.com/" + v,
                "ig": "https://www.instagram.com/" + v,
                "tw": "https://x.com/" + v,
                "yt": ("https://www.youtube.com/channel/" + v) if v.startswith("UC")
                      else "https://www.youtube.com/@" + v,
                "li": "https://www.linkedin.com/company/" + v}[kind]
    return (u("fb","fb"), u("ig","ig"), u("tw","tw"), u("yt","yt"), u("li","li"))

# --------------------------------------------------------------- 3. assemble
def load_cache():
    if os.path.exists(DATA_JSON):
        with open(DATA_JSON, encoding="utf-8") as f:
            return {r["Ticker"]: r for r in json.load(f)}
    return {}

def build(force_full=False):
    cache = load_cache()
    constituents = fetch_constituents()
    if len(constituents) < MIN_CONSTITUENTS:
        sys.exit("ABORT: only %d constituents (< %d). Keeping existing data."
                 % (len(constituents), MIN_CONSTITUENTS))
    print("fetched %d constituents" % len(constituents))
    need = [c for c in constituents
            if force_full or c["ticker"] not in cache
            or not cache[c["ticker"]].get("_enriched")]
    print("need enrichment: %d (cached reuse: %d)" % (len(need), len(constituents) - len(need)))
    qmap = {}
    if need:
        with ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(wiki_qid, c["name"]): c["ticker"] for c in need}
            for fut in as_completed(futs):
                qid, slug = fut.result()
                if qid: qmap[futs[fut]] = (qid, slug)
        wd = wikidata_batch(sorted({q for q, _ in qmap.values()}))
    else:
        wd = {}
    rows = []
    constituents.sort(key=lambda c: -c["weight"])
    for rank, c in enumerate(constituents, 1):
        tk = c["ticker"]
        fresh = tk in qmap and (force_full or tk not in cache or not cache[tk].get("_enriched"))
        if fresh:
            qid, slug = qmap[tk]; rec = wd.get(qid, {})
            fb, ig, tw, yt, li = social_urls(rec)
            row = {"Ticker": tk, "Company": (slug or c["name"]).replace("_", " "),
                   "Sector": c["sector"], "Index Weight %": "%.2f" % c["weight"],
                   "Website": rec.get("web", ""), "Wikipedia": rec.get("article", ""),
                   "Facebook": fb, "Instagram": ig, "X": tw, "YouTube": yt, "LinkedIn": li,
                   "_enriched": True}
        else:
            old = cache.get(tk, {})
            row = {"Ticker": tk, "Company": old.get("Company", c["name"].title()),
                   "Sector": c["sector"] or old.get("Sector", "—"),
                   "Index Weight %": "%.2f" % c["weight"],
                   "Website": old.get("Website", ""), "Wikipedia": old.get("Wikipedia", ""),
                   "Facebook": old.get("Facebook", ""), "Instagram": old.get("Instagram", ""),
                   "X": old.get("X", ""), "YouTube": old.get("YouTube", ""),
                   "LinkedIn": old.get("LinkedIn", ""),
                   "_enriched": bool(old.get("_enriched"))}
        row["Rank"] = rank
        row["Link Confidence"] = "Verified" if rank <= VERIFIED_TOP else "Auto-enriched"
        rows.append(row)
    return rows

# ----------------------------------------------------------------- 4. write
COLS = ["Rank", "Ticker", "Company", "Sector", "Index Weight %", "Website",
        "Wikipedia", "Facebook", "Instagram", "X", "YouTube", "LinkedIn",
        "Link Confidence"]

def write_outputs(rows):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(TPL_DIR, exist_ok=True)
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(rows, f)
    with open(DATA_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLS})
    write_html(rows)

def write_html(rows):
    today = datetime.date.today().isoformat()
    nsoc = sum(1 for r in rows if any(r.get(k) for k in ("Facebook","Instagram","X","YouTube","LinkedIn")))
    public = [{k: r.get(k, "") for k in COLS} for r in rows]
    data = json.dumps(public, separators=(",", ":"))
    page = (PAGE_TEMPLATE.replace("__DATA__", data).replace("__ASOF__", today)
            .replace("__COUNT__", str(len(rows))).replace("__NSOC__", str(nsoc)))
    with open(PAGE_HTML, "w", encoding="utf-8") as f:
        f.write(page)

PAGE_TEMPLATE = r'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Russell 3000 (US) - Yearly Asana task</title><style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1f2a44;--mut:#667085;--line:#e6e8ec;--accent:#0563C1;--chip:#eef2ff}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:1480px;margin:0 auto;padding:28px 20px 60px}a.back{color:var(--mut);text-decoration:none;font-size:14px}
h1{margin:14px 0 6px;font-size:30px}p.lede{color:var(--mut);margin:0 0 20px;max-width:920px;line-height:1.5}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:18px}
.chip{background:var(--chip);color:#3538cd;border-radius:999px;padding:5px 12px;font-size:13px;font-weight:600}
.meta{color:var(--mut);font-size:13px}.btns{display:flex;gap:10px;margin:14px 0 0}
.btn{background:var(--ink);color:#fff;border:none;border-radius:8px;padding:9px 16px;font-size:14px;font-weight:600;cursor:pointer}
.btn.sec{background:#fff;color:var(--ink);border:1px solid var(--line)}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 12px}input,select{padding:9px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px}input{flex:1;min-width:220px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:13.5px}
thead th{background:var(--ink);color:#fff;text-align:left;padding:11px 10px;font-weight:600;position:sticky;top:0;cursor:pointer;white-space:nowrap}
tbody td{padding:9px 10px;border-top:1px solid var(--line);vertical-align:top}tbody tr:hover{background:#fafbff}
.tk{font-weight:700}.sector{color:var(--mut)}a.lnk{color:var(--accent);text-decoration:none}a.lnk:hover{text-decoration:underline}
.dash{color:#c0c4cc}.count{color:var(--mut);font-size:13px;margin:10px 2px}.right{text-align:right}
.v{color:#1a7f37;font-size:12px;font-weight:600}.a{color:#9a6700;font-size:12px;font-weight:600}
</style></head><body><div class="wrap">
<a class="back" href="/">&larr; All tools</a><h1>Russell 3000 (US)</h1>
<p class="lede">Constituents of the Russell 3000 Index with each company's official website, English Wikipedia page, and social accounts (Facebook, Instagram, X, YouTube, LinkedIn). Search, filter, and download as CSV or Excel. <b>Link confidence</b>: <span class="v">Verified</span> = checked against Wikidata/Wikipedia; <span class="a">Auto-enriched</span> = machine-matched. Social handles come from Wikidata and may reflect a regional account &mdash; spot-check before use.</p>
<div class="card"><span class="chip">Russell 3000 Index</span>
<span class="meta">&nbsp; Constituents via iShares Russell 3000 ETF (IWV) holdings &nbsp;&middot;&nbsp; <b id="cnt"></b> companies &nbsp;&middot;&nbsp; <b id="scnt"></b> with social accounts &nbsp;&middot;&nbsp; <b>Data as of __ASOF__</b></span>
<div class="meta" style="margin-top:8px">Ranked by index weight. Top 640 fully verified; remainder auto-enriched and flagged. Refreshed annually after the June reconstitution.</div>
<div class="btns"><button class="btn" onclick="dl('csv')">Download CSV</button><button class="btn sec" onclick="dl('xls')">Download Excel</button></div></div>
<div class="controls"><input id="q" placeholder="Search company, ticker, or sector&hellip;" oninput="render()">
<select id="sec" onchange="render()"><option value="">All sectors</option></select>
<select id="conf" onchange="render()"><option value="">All confidence</option><option>Verified</option><option>Auto-enriched</option></select>
<select id="soc" onchange="render()"><option value="">All companies</option><option value="1">Has social accounts</option></select></div>
<div class="count" id="count"></div>
<table><thead><tr><th onclick="s('Rank')">#</th><th onclick="s('Ticker')">Ticker</th><th onclick="s('Company')">Company</th><th onclick="s('Sector')">Sector</th><th class="right" onclick="s('w')">Weight %</th><th>Website</th><th>Wikipedia</th><th>Facebook</th><th>Instagram</th><th>X</th><th>YouTube</th><th>LinkedIn</th><th>Confidence</th></tr></thead><tbody id="tb"></tbody></table></div>
<script>
const DATA=__DATA__;DATA.forEach(r=>{r.w=parseFloat(r['Index Weight %'])||0;r._s=(r.Facebook||r.Instagram||r.X||r.YouTube||r.LinkedIn)?1:0});
let sk='Rank',sd=1;const ss=document.getElementById('sec');
[...new Set(DATA.map(r=>r.Sector))].sort().forEach(x=>{const o=document.createElement('option');o.value=x;o.textContent=x;ss.appendChild(o)});
document.getElementById('cnt').textContent=DATA.length;
document.getElementById('scnt').textContent=DATA.filter(r=>r._s).length;
function host(u){return u.replace('https://www.','').replace('https://','').replace(/\/$/,'')}
function s(k){sd=(sk===k)?-sd:1;sk=k;render()}
function filt(){const q=document.getElementById('q').value.toLowerCase(),sec=ss.value,cf=document.getElementById('conf').value,so=document.getElementById('soc').value;
let r=DATA.filter(x=>(!sec||x.Sector===sec)&&(!cf||x['Link Confidence']===cf)&&(!so||x._s)&&(!q||(x.Company+' '+x.Ticker+' '+x.Sector).toLowerCase().includes(q)));
r.sort((a,b)=>{let va=a[sk],vb=b[sk];if(typeof va==='string'){va=va.toLowerCase();vb=vb.toLowerCase()}return va<vb?-sd:va>vb?sd:0});return r}
function sl(u,t){return u?'<a class="lnk" target="_blank" rel="noopener" href="'+u+'">'+t+'</a>':'<span class="dash">&mdash;</span>'}
function render(){const r=filt(),tb=document.getElementById('tb');tb.innerHTML='';
document.getElementById('count').textContent=r.length+' of '+DATA.length+' companies';
const f=document.createDocumentFragment();
r.forEach(x=>{const tr=document.createElement('tr');
tr.innerHTML='<td>'+x.Rank+'</td><td class="tk">'+x.Ticker+'</td><td>'+x.Company+'</td><td class="sector">'+x.Sector+'</td><td class="right">'+x.w.toFixed(2)+'</td>'+
'<td>'+(x.Website?'<a class="lnk" target="_blank" rel="noopener" href="'+x.Website+'">'+host(x.Website)+'</a>':'<span class="dash">&mdash;</span>')+'</td>'+
'<td>'+sl(x.Wikipedia,'Wiki')+'</td><td>'+sl(x.Facebook,'FB')+'</td><td>'+sl(x.Instagram,'IG')+'</td><td>'+sl(x.X,'X')+'</td><td>'+sl(x.YouTube,'YT')+'</td><td>'+sl(x.LinkedIn,'in')+'</td>'+
'<td class="'+(x['Link Confidence']==='Verified'?'v':'a')+'">'+x['Link Confidence']+'</td>';f.appendChild(tr)});
tb.appendChild(f)}
function dl(t){const cols=['Rank','Ticker','Company','Sector','Index Weight %','Website','Wikipedia','Facebook','Instagram','X','YouTube','LinkedIn','Link Confidence'],rs=filt();
const esc=v=>{v=(v==null?'':String(v));return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
const csv=[cols.join(',')].concat(rs.map(r=>cols.map(c=>esc(r[c])).join(','))).join('\n');
const b=new Blob([t==='xls'?'﻿'+csv:csv],{type:t==='xls'?'application/vnd.ms-excel':'text/csv'});
const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='russell3000___ASOF__.'+(t==='xls'?'xls':'csv');a.click()}
render();
</script></body></html>'''

if __name__ == "__main__":
    force = "--full" in sys.argv
    if "--csv" in sys.argv:
        i = sys.argv.index("--csv")
        CSV_PATH = sys.argv[i + 1] if i + 1 < len(sys.argv) else IWV_CSV
    rows = build(force_full=force)
    write_outputs(rows)
    nsoc = sum(1 for r in rows if any(r.get(k) for k in ("Facebook","Instagram","X","YouTube","LinkedIn")))
    print("WROTE %d rows | %d with socials -> %s , %s , %s"
          % (len(rows), nsoc, DATA_JSON, DATA_CSV, PAGE_HTML))
