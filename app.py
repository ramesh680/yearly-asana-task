"""
Yearly Asana task - a shared hub of yearly data tools.

The landing page lists tools; each tool has its own route. The kickoff tool is
"Best Hospitals (US)". Add more tools by appending to TOOLS and registering a
new route + template.
"""
import datetime as _dt
import io

from flask import Flask, render_template, request, send_file, abort

from tools import best_hospitals

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
            "with each hospital's official website and social handles (Facebook, "
            "Instagram, X, YouTube, LinkedIn). View and download as CSV or Excel."
        ),
        "endpoint": "best_hospitals_view",
        "available": True,
    },
]


@app.context_processor
def inject_globals():
    return {"app_name": APP_NAME, "today": _dt.date.today().isoformat()}


@app.route("/")
def index():
    return render_template("index.html", tools=TOOLS)


@app.route("/best-hospitals")
def best_hospitals_view():
    source = request.args.get("source", "newsweek")
    rows, meta = best_hospitals.get_hospitals(source)
    return render_template(
        "best_hospitals.html",
        rows=rows,
        meta=meta,
        sources=best_hospitals.SOURCES,
    )


@app.route("/best-hospitals/export")
def best_hospitals_export():
    source = request.args.get("source", "newsweek")
    fmt = request.args.get("fmt", "csv")
    rows, meta = best_hospitals.get_hospitals(source)

    stamp = _dt.date.today().isoformat()
    base = "best_hospitals_{}_{}_{}".format(meta["source"], meta["edition"], stamp)

    if fmt == "xlsx":
        return _send_xlsx(rows, meta, base + ".xlsx")

    csv_text = best_hospitals.to_csv(rows, meta)
    return send_file(
        io.BytesIO(csv_text.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=base + ".csv",
    )


def _send_xlsx(rows, meta, filename):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        from openpyxl.utils import get_column_letter
    except Exception:
        abort(500, "openpyxl is not installed; CSV export is still available.")

    cols = best_hospitals.columns(meta)

    wb = Workbook()
    ws = wb.active
    ws.title = "Best Hospitals"

    ws.append([label for label, _key in cols])
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for r in rows:
        ws.append([r.get(key, "") for _label, key in cols])

    # Column widths keyed by header label.
    width_by_label = {
        "Rank": 8, "Hospital": 52, "City": 16, "State": 16, "Score": 9,
        "Website": 30, "Facebook": 42, "Instagram": 38, "X / Twitter": 30,
        "YouTube": 44, "LinkedIn": 52,
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
