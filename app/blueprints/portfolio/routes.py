import yfinance as yf

from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from pprint import pprint

from app.db.db import get_stocks, refresh_stocks

portfolio_bp = Blueprint("portfolio",
                         __name__,
                         template_folder="templates",
                         static_folder="static",
                         static_url_path="/portfolio/static")


@portfolio_bp.route("/", methods=["GET", "POST"])
def portfolio():
    if "portfolio-refresh" in request.form:
        refresh_stocks()

    stock_history = {}
    stock_info = {}

    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    offset = (page - 1) * limit

    all_stocks = get_stocks()
    page_stocks = all_stocks[offset:offset + limit]
    pagination = Pagination(page=page,
                            per_page=limit,
                            total=len(all_stocks),
                            offset=offset,
                            show_single_page=True,
                            alignment="center",
                            css_framework="bootstrap5",
                            bs_version=5)

    for page_stock in page_stocks:
        stock = yf.Ticker(page_stock[2])
        hist = stock.history(period="5y")

        if hist.empty:
            stock = yf.Ticker(page_stock[2] + ".NZ")
            hist = stock.history(period="5y")
            stock_info[page_stock[2]] = {"currency": "NZD"}
        else:
            stock_info[page_stock[2]] = {"currency": "USD"}

        stock_history[page_stock[2]] = {
            "labels": [str(date)[:10] for date in list(hist.index.values)],
            "data": hist["Close"].tolist(),
        }

    return render_template("portfolio.html",
                           stocks=page_stocks,
                           stock_history=stock_history,
                           stock_info=stock_info,
                           page=page,
                           limit=page,
                           pagination=pagination)
