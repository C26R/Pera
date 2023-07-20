from flask import Blueprint, render_template, request
from pprint import pprint

from app.db.db import get_kiwisavers, refresh_kiwisavers, get_formatted_kiwisavers_history

kiwisaver_bp = Blueprint("kiwisaver",
                         __name__,
                         template_folder="templates",
                         static_folder="static",
                         static_url_path="/kiwisaver/static")


@kiwisaver_bp.route("/", methods=["GET", "POST"])
def kiwisaver():
    if "kiwisaver-refresh" in request.form:
        refresh_kiwisavers()

    kiwisaver_historical = get_formatted_kiwisavers_history()
    labels = []
    data = []

    for row in kiwisaver_historical:
        labels.append(row[0])
        data.append(row[1])

    account = get_kiwisavers()[0]

    return render_template("kiwisaver.html",
                           account=account,
                           labels=labels,
                           data=data)
