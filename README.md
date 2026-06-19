# Yearly Asana task

A shared hub of yearly data tools, modeled on the Media Data Tools Hub. The
landing page lists tools; each tool has its own page with a table view and
CSV / Excel downloads.

## Tools

### Best Hospitals (US)
Two sources, switchable from a dropdown:
- **U.S. News Best Hospitals Honor Roll (2025-2026)** — 20 Honor Roll hospitals.
- **Newsweek / Statista World's Best Hospitals 2026 (US)** — ranked top 50 with score.

Columns: rank (Newsweek), hospital, city, state, score (Newsweek), official
**website**, **Facebook / Instagram / X / YouTube / LinkedIn**, and **Wikipedia**.

### Best Colleges (US)
- **U.S. News Best National Universities 2026** — ranked top 100 (ties shared as
  published, so rank numbers repeat and aren't consecutive).

Columns: rank, university, city, state, official **website**, the five **social**
handles, and **Wikipedia**.

## Data, accuracy, and refreshing

Each tool serves a **curated, versioned snapshot** stored in `tools/*_data.py`.
This is deliberate: the ranking sites (U.S. News, Newsweek) are JavaScript-
rendered and/or login-gated, so a server-side scrape can't reliably read them.

- Social handles are official accounts, filled where verifiable and left blank
  otherwise. Spot-check before relying on them.
- Wikipedia links use Wikipedia's search-redirect, so they always resolve to the
  right page.

### Live refresh (and its limits)
Each tool page has a **"Try live refresh"** link (`?live=1`). When clicked, the
app attempts to fetch the source live and falls back to the cached snapshot if
it can't (showing a clear note). In practice U.S. News won't fetch (login wall)
and Newsweek returns only partial data, so the cached snapshot is normally what
you see — that's expected and trustworthy.

### Refreshing the data each year / in a few months
Edit the snapshot files and redeploy:
- Hospitals: `tools/hospitals_data.py`
- Colleges: `tools/colleges_data.py`

Update the `*_EDITION` strings and the rows. The page badge always shows which
edition is being served, so it's obvious when a refresh is due.

## Run locally
```bash
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

## Deploy to Render
Includes `render.yaml` and `Procfile` (start command binds to `$PORT`).
New → Blueprint → point at the repo, or New → Web Service with
`pip install -r requirements.txt` and `gunicorn app:app --bind 0.0.0.0:$PORT`.

## Add another tool
1. Add a dict to `TOOLS` in `app.py` (key, category, title, description, endpoint).
2. Add a route + template, and a `tools/<tool>.py` module (mirror `best_colleges.py`).
3. It appears on the hub automatically.

Sources:
- https://health.usnews.com/health-care/best-hospitals/articles/best-hospitals-honor-roll-and-overview
- https://rankings.newsweek.com/worlds-best-hospitals-2026/united-states
- https://www.usnews.com/best-colleges/rankings/national-universities
