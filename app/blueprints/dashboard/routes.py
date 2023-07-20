import numpy as np

from bokeh.palettes import Purples
from flask import Blueprint, render_template, request
from pandas import DataFrame

from app.db.db import get_accounts, refresh_accounts, get_mtd_transactions, get_qtd_transactions, get_ytd_transactions
from app.db.db import get_month_transactions, get_quarter_transactions, get_year_transactions
from app.db.db import get_kiwisavers, refresh_kiwisavers

dashboard_bp = Blueprint("dashboard",
                         __name__,
                         template_folder="templates",
                         static_folder="static",
                         static_url_path="/dashboard/static")


def get_categories_amounts(transactions):
    data = DataFrame(transactions, columns=["transaction_id",
                                            "account_id",
                                            "date",
                                            "amount",
                                            "description",
                                            "type",
                                            "category",
                                            "sub_category",
                                            "added"])

    data = data.groupby("category", as_index=False).agg(amount=("amount", "sum"))
    data["amount"] = data["amount"].map(lambda amount: abs(amount))

    categories = data["category"].tolist()
    amounts = data["amount"].tolist()

    return categories, amounts


def get_income_expenses(transactions):
    df = DataFrame(transactions, columns=["transaction_id",
                                          "account_id",
                                          "date",
                                          "amount",
                                          "description",
                                          "type",
                                          "category",
                                          "sub_category",
                                          "added"])

    income = np.sum(df["amount"].where(df["amount"] > 0, 0))
    expenses = abs(np.sum(df["amount"].where(df["amount"] < 0, 0)))

    return ["Income", "Expenses"], [income, expenses]


@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard():
    choices = [
        ("mtd", "Month to Date (MTD)"),
        ("qtd", "Quarter to Date (QTD)"),
        ("ytd", "Year to Date (YTD)"),
        ("month", "One Month"),
        ("quarter", "One Quarter"),
        ("year", "One Year")
    ]

    if "accounts-refresh" in request.form:
        refresh_accounts()

    if "kiwisaver-refresh" in request.form:
        refresh_kiwisavers()

    if "pie-refresh" in request.form:
        selected = request.form.get("pie-range")

        if selected == "mtd":
            pie_labels, pie_data = get_categories_amounts(get_mtd_transactions())
            bar_labels, bar_data = get_income_expenses(get_mtd_transactions(income=True))
        elif selected == "qtd":
            pie_labels, pie_data = get_categories_amounts(get_qtd_transactions())
            bar_labels, bar_data = get_income_expenses(get_qtd_transactions(income=True))
        elif selected == "ytd":
            pie_labels, pie_data = get_categories_amounts(get_ytd_transactions())
            bar_labels, bar_data = get_income_expenses(get_ytd_transactions(income=True))
        elif selected == "month":
            pie_labels, pie_data = get_categories_amounts(get_month_transactions())
            bar_labels, bar_data = get_income_expenses(get_month_transactions(income=True))
        elif selected == "quarter":
            pie_labels, pie_data = get_categories_amounts(get_quarter_transactions())
            bar_labels, bar_data = get_income_expenses(get_quarter_transactions(income=True))
        elif selected == "year":
            pie_labels, pie_data = get_categories_amounts(get_year_transactions())
            bar_labels, bar_data = get_income_expenses(get_year_transactions(income=True))
    else:
        selected = "mtd"
        pie_labels, pie_data = get_categories_amounts(get_mtd_transactions())
        bar_labels, bar_data = get_income_expenses(get_mtd_transactions(income=True))

    colours = list(Purples[len(pie_data)])

    return render_template("dashboard.html",
                           accounts=get_accounts(),
                           kiwisavers=get_kiwisavers(),
                           pie_labels=pie_labels,
                           pie_data=pie_data,
                           bar_labels=bar_labels,
                           bar_data=bar_data,
                           colours=colours,
                           choices=choices,
                           selected=selected)
