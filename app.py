"""
Yearly Asana task - a shared hub of yearly data tools.

The landing page lists tools; each tool has its own route. Add more tools by
appending to TOOLS and registering a new route + template.
"""
import datetime as _dt
import io

from flask import Flask, render_template, request, send_file, abort

from tools import best_hospitals, best_colleges

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
