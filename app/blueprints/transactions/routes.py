from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter

from app.db.db import get_accounts, get_account_transactions, refresh_transactions, refresh_accounts

transactions_bp = Blueprint("transactions",
                            __name__,
                            template_folder="templates",
                            static_folder="static")


@transactions_bp.route("/", methods=["GET", "POST"])
@transactions_bp.route("/<account>", methods=["GET", "POST"])
def transactions(account=None):
    if "transactions-refresh" in request.form:
        refresh_transactions()
    elif "accounts-refresh" in request.form:
        refresh_accounts()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    offset = (page - 1) * limit

    all_transactions = get_account_transactions(account)
    page_transactions = all_transactions[offset:offset + limit]
    pagination = Pagination(page=page,
                            per_page=limit,
                            total=len(all_transactions),
                            offset=offset,
                            show_single_page=True,
                            alignment="center",
                            css_framework="bootstrap5",
                            bs_version=5)

    return render_template("transactions.html",
                           accounts=get_accounts(),
                           account=account,
                           transactions=page_transactions,
                           page=page,
                           limit=limit,
                           pagination=pagination)
