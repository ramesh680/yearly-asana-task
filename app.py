"""
Yearly Asana task - a shared hub of yearly data tools.

The landing page lists tools; each tool has its own route. Add more tools by
appending to TOOLS and registering a new route + template.
"""
import datetime as _dt
import io

from flask import Flask, render_template, request, send_file, abort

from tools import best_hospitals, best_colleges, premier_league, saudi_pro_league, twitch_streamers, wnba_teams, motorsports

app = Flask(__name__)

APP_NAME = "Yearly Asana task"

TOOLS = [
    {
        "key": "best-hospitals",
        "category": "Healthcare",
        "title": "Best Hospitals (US)",
        "description": (
            "Pulls the latest U.S. best-hospital lists from U.S. News & World "
            "Report (Honor Roll) and Newsweek/Statista (World's Best Hospitals), "
            "with each hospital's official website and social handles. View and "
            "download as CSV or Excel."
        ),
        "endpoint": "best_hospitals_view",
        "available": True,
    },
    {
        "key": "best-colleges",
        "category": "Education",
        "title": "Best Colleges (US)",
        "description": (
            "U.S. News Best National Universities (Top 100, 2026), with each "
            "school's official website and social handles (Facebook, Instagram, "
            "X, YouTube, LinkedIn). View and download as CSV or Excel."
        ),
        "endpoint": "best_colleges_view",
        "available": True,
    },
    {
        "key": "russell-3000",
        "category": "Finance",
        "title": "Russell 3000",
        "description": (
            "All Russell 3000 constituents (via iShares IWV holdings), ranked "
            "by index weight, with each company's official website, Wikipedia "
            "page, and social handles (Facebook, Instagram, X, YouTube, "
            "LinkedIn). View and download as CSV or Excel."
        ),
        "endpoint": "russell_3000_view",
        "available": True,
    },
    {
        "key": "premier-league",
        "category": "Sports",
        "title": "English Premier League",
        "description": (
            "The 20 English Premier League clubs (2025/26 season, via the "
            "official Premier League site), ordered by final league position, "
            "with each club's home city, stadium, points, official website and "
            "social handles (X, Instagram, Facebook, YouTube) plus Wikipedia. "
            "View and download as CSV or Excel."
        ),
        "endpoint": "premier_league_view",
        "available": True,
    },
    {
        "key": "saudi-pro-league",
        "category": "Sports",
        "title": "Saudi Pro League",
        "description": (
            "The 18 Saudi Pro League (Roshn Saudi League) clubs (2025/26 season, "
            "via the official Saudi Pro League site), ordered by final league "
            "position, with each club's home city, stadium, points, official "
            "website and social handles (X, Instagram, Facebook, YouTube) plus "
            "Wikipedia. View and download as CSV or Excel."
        ),
        "endpoint": "saudi_pro_league_view",
        "available": True,
    },
    {
        "key": "twitch-streamers",
        "category": "Streaming",
        "title": "Top Twitch Streamers",
        "description": (
            "The top channels from TwitchTracker's overall ranking (a 30-day "
            "blend of average viewers, followers, views and stream time), with "
            "each channel's average viewers, all-time peak, hours watched, "
            "Twitch link and social handles (X, YouTube) plus Wikipedia. View "
            "and download as CSV or Excel."
        ),
        "endpoint": "twitch_streamers_view",
        "available": True,
    },
    {
        "key": "wnba-teams",
        "category": "Basketball",
        "title": "WNBA Teams",
        "description": (
            "The 13 Women's National Basketball Association teams (2025 season, "
            "via wnba.com), ordered by final regular-season standing, with each "
            "team's home city, arena, win-loss record, official website and "
            "social handles (X, Instagram, Facebook) plus Wikipedia. View and "
            "download as CSV or Excel."
        ),
        "endpoint": "wnba_teams_view",
        "available": True,
    },
    {
        "key": "motorsports",
        "category": "Motorsport",
        "title": "Top Motorsports",
        "description": (
            "The 10 most popular motorsport series and events (Formula 1, "
            "NASCAR, MotoGP, IndyCar, Le Mans, WRC, Dakar, Formula E, MXGP, "
            "Isle of Man TT), with each one's discipline, official website and "
            "social handles (X, Instagram, YouTube) plus Wikipedia. Ranked by "
            "popularity. View and download as CSV or Excel."
        ),
        "endpoint": "motorsports_view",
        "available": True,
    },
]


@app.context_processor
def inject_globals():
    return {"app_name": APP_NAME, "today": _dt.date.today().isoformat()}


@app.route("/")
def index():
    return render_template("index.html", tools=TOOLS)


# ---------------------------------------------------------------- Hospitals
@app.route("/best-hospitals")
def best_hospitals_view():
    source = request.args.get("source", "newsweek")
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = best_hospitals.get_hospitals(source, live=live)
    return render_template(
        "best_hospitals.html", rows=rows, meta=meta, sources=best_hospitals.SOURCES,
    )


@app.route("/best-hospitals/export")
def best_hospitals_export():
    source = request.args.get("source", "newsweek")
    fmt = request.args.get("fmt", "csv")
    rows, meta = best_hospitals.get_hospitals(source)
    stamp = _dt.date.today().isoformat()
    base = "best_hospitals_{}_{}_{}".format(meta["source"], meta["edition"], stamp)
    if fmt == "xlsx":
        return _send_xlsx(best_hospitals.columns(meta), rows, "Best Hospitals", base + ".xlsx")
    return _send_csv(best_hospitals.to_csv(rows, meta), base + ".csv")


# ---------------------------------------------------------------- Colleges
@app.route("/best-colleges")
def best_colleges_view():
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = best_colleges.get_colleges(live=live)
    return render_template("best_colleges.html", rows=rows, meta=meta)


@app.route("/best-colleges/export")
def best_colleges_export():
    fmt = request.args.get("fmt", "csv")
    rows, meta = best_colleges.get_colleges()
    stamp = _dt.date.today().isoformat()
    base = "best_colleges_national_universities_{}_{}".format(meta["edition"], stamp)
    if fmt == "xlsx":
        return _send_xlsx(best_colleges.columns(), rows, "Best Colleges", base + ".xlsx")
    return _send_csv(best_colleges.to_csv(rows), base + ".csv")

# ---------------------------------------------------------------- Russell 3000
@app.route("/russell-3000")
def russell_3000_view():
    import os
    path = os.path.join(app.root_path, "templates", "russell-3000.html")
    with open(path, encoding="utf-8") as f:
        return f.read()

# ------------------------------------------------------------ Premier League
@app.route("/premier-league")
def premier_league_view():
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = premier_league.get_clubs(live=live)
    return render_template("premier-league.html", rows=rows, meta=meta)


@app.route("/premier-league/export")
def premier_league_export():
    fmt = request.args.get("fmt", "csv")
    rows, meta = premier_league.get_clubs()
    stamp = _dt.date.today().isoformat()
    base = "premier_league_clubs_{}_{}".format(meta["edition"].replace("/", "-"), stamp)
    if fmt == "xlsx":
        return _send_xlsx(premier_league.columns(), rows, "Premier League", base + ".xlsx")
    return _send_csv(premier_league.to_csv(rows), base + ".csv")


# ---------------------------------------------------------- - Saudi Pro League
@app.route("/saudi-pro-league")
def saudi_pro_league_view():
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = saudi_pro_league.get_clubs(live=live)
    return render_template("saudi-pro-league.html", rows=rows, meta=meta)


@app.route("/saudi-pro-league/export")
def saudi_pro_league_export():
    fmt = request.args.get("fmt", "csv")
    rows, meta = saudi_pro_league.get_clubs()
    stamp = _dt.date.today().isoformat()
    base = "saudi_pro_league_clubs_{}_{}".format(meta["edition"].replace("/", "-"), stamp)
    if fmt == "xlsx":
        return _send_xlsx(saudi_pro_league.columns(), rows, "Saudi Pro League", base + ".xlsx")
    return _send_csv(saudi_pro_league.to_csv(rows), base + ".csv")


# ----------------------------------------------------------- Twitch Streamers
@app.route("/twitch-streamers")
def twitch_streamers_view():
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = twitch_streamers.get_streamers(live=live)
    return render_template("twitch-streamers.html", rows=rows, meta=meta)


@app.route("/twitch-streamers/export")
def twitch_streamers_export():
    fmt = request.args.get("fmt", "csv")
    rows, meta = twitch_streamers.get_streamers()
    stamp = _dt.date.today().isoformat()
    base = "top_twitch_streamers_{}".format(stamp)
    if fmt == "xlsx":
        return _send_xlsx(twitch_streamers.columns(), rows, "Top Twitch Streamers", base + ".xlsx")
    return _send_csv(twitch_streamers.to_csv(rows), base + ".csv")


# ---------------------------------------------------------------- WNBA Teams
@app.route("/wnba-teams")
def wnba_teams_view():
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = wnba_teams.get_teams(live=live)
    return render_template("wnba-teams.html", rows=rows, meta=meta)


@app.route("/wnba-teams/export")
def wnba_teams_export():
    fmt = request.args.get("fmt", "csv")
    rows, meta = wnba_teams.get_teams()
    stamp = _dt.date.today().isoformat()
    base = "wnba_teams_{}_{}".format(meta["edition"].replace(" ", "_"), stamp)
    if fmt == "xlsx":
        return _send_xlsx(wnba_teams.columns(), rows, "WNBA Teams", base + ".xlsx")
    return _send_csv(wnba_teams.to_csv(rows), base + ".csv")


# ---------------------------------------------------------------- Motorsports
@app.route("/motorsports")
def motorsports_view():
    live = request.args.get("live") in ("1", "true", "yes")
    rows, meta = motorsports.get_motorsports(live=live)
    return render_template("motorsports.html", rows=rows, meta=meta)


@app.route("/motorsports/export")
def motorsports_export():
    fmt = request.args.get("fmt", "csv")
    rows, meta = motorsports.get_motorsports()
    stamp = _dt.date.today().isoformat()
    base = "top_motorsports_{}".format(stamp)
    if fmt == "xlsx":
        return _send_xlsx(motorsports.columns(), rows, "Top Motorsports", base + ".xlsx")
    return _send_csv(motorsports.to_csv(rows), base + ".csv")


# ---------------------------------------------------------------- Helpers
def _send_csv(csv_text, filename):
    return send_file(
        io.BytesIO(csv_text.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename,
    )


def _send_xlsx(cols, rows, sheet_title, filename):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        from openpyxl.utils import get_column_letter
    except Exception:
        abort(500, "openpyxl is not installed; CSV export is still available.")

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title

    ws.append([label for label, _key in cols])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for r in rows:
        ws.append([r.get(key, "") for _label, key in cols])

    width_by_label = {
        "Rank": 8, "Hospital": 52, "University": 44, "City": 16, "State": 18,
        "Score": 9, "Website": 30, "Facebook": 42, "Instagram": 38,
        "X / Twitter": 30, "YouTube": 44, "LinkedIn": 52, "Wikipedia": 30,
        "Position": 9, "Club": 30, "Stadium": 28, "Points": 9,
        "Channel": 26, "Avg Viewers": 14, "Peak Viewers": 14,
        "Hours Watched": 16, "Twitch": 28,
        "Seed": 7, "Team": 26, "Arena": 26, "W": 6, "L": 6,
        "Series / Event": 26, "Category": 26,
    }
    for i, (label, _key) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width_by_label.get(label, 24)

    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    return send_file(
        bio,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
