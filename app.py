"""
Yearly Asana task — a shared hub of yearly data tools.

This mirrors the structure of the Media Data Tools Hub: a landing page that
lists tools, and one route per tool. The first tool is "Best Hospitals (US)".
Add more tools by appending to TOOLS and registering a new route + template.
"""
import datetime as _dt
import io

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    abort,
)

from tools import best_hospitals

app = Flask(__name__)

APP_NAME = "Yearly Asana task"

# Registry that drives the hub landing page. Each new tool gets one entry.
TOOLS = [
    {
        "key": "best-hospitals",
        "category": "Healthcare",
        "title": "Best Hospitals (US)",
        "description": (
            "Pulls the latest U.S. best-hospital lists from U.S. News & World "
            "Report (Honor Roll) and Newsweek/Statista (World's Best Hospitals). "
            "View the list and download it as CSV or Excel."
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
    base = f"best_hospitals_{meta['source']}_{meta['edition']}_{stamp}"

    if fmt == "xlsx":
        return _send_xlsx(rows, meta, f"{base}.xlsx")

    csv_text = best_hospitals.to_csv(rows, meta)
    return send_file(
        io.BytesIO(csv_text.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"{base}.csv",
    )


def _send_xlsx(rows, meta, filename):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except Exception:
        abort(500, "openpyxl is not installed; CSV export is still available.")

    wb = Workbook()
    ws = wb.active
    ws.title = "Best Hospitals"

    if meta["ordinal"]:
        headers = ["Rank", "Hospital", "City", "State", "Score"]
    else:
        headers = ["Hospital", "City", "State"]

    ws.append(headers)
    for c in ws[1]:
        c.font = Font(bold=True)

    for r in rows:
        if meta["ordinal"]:
            ws.append([r["rank"], r["hospital"], r["city"], r["state"], r["score"]])
        else:
            ws.append([r["hospital"], r["city"], r["state"]])

    # Reasonable column widths
    widths = [8, 56, 18, 18, 10] if meta["ordinal"] else [56, 18, 18]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = w

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
