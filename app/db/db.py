import sqlite3

from datetime import date

from app.api import manual_refresh, get_transactions_range, get_request_accounts

con = sqlite3.connect("db/db.db", check_same_thread=False)
cur = con.cursor()


def get_accounts():
    """Returns all bank accounts"""
    res = cur.execute("SELECT * FROM accounts;")

    return res.fetchall()


def get_kiwisavers():
    """Returns all KiwiSaver accounts"""
    res = cur.execute("SELECT * FROM kiwisavers;")

    return res.fetchall()


def get_formatted_kiwisavers_history():
    """Returns formatted KiwiSaver values"""
    res = cur.execute("SELECT date, MAX(amount) FROM kiwisavers_history GROUP BY date ORDER BY date ASC;")

    return res.fetchall()


def get_stocks():
    """Returns all stocks"""
    res = cur.execute("SELECT * FROM shares;")

    return res.fetchall()


def get_account_transactions(account=None):
    """Returns all transactions for an account or all accounts if none is given"""
    if account is None:
        statement = "SELECT * FROM transactions " \
                    "INNER JOIN accounts ON transactions.account_id = accounts.id " \
                    "ORDER BY transactions.date DESC;"
        res = cur.execute(statement)
    else:
        statement = "SELECT * FROM transactions " \
                    "INNER JOIN accounts ON transactions.account_id = accounts.id " \
                    "WHERE transactions.account_id = ? " \
                    "ORDER BY transactions.date DESC;"
        res = cur.execute(statement, (account,))

    return res.fetchall()


def refresh_accounts():
    """Updates bank accounts with latest data from Akahu API"""
    manual_refresh()

    accounts = get_request_accounts()
    formatted_accounts = []

    for account in accounts:
        if account["type"] not in ["KIWISAVER", "INVESTMENT", "WALLET"]:
            formatted_accounts.append((account["_id"],
                                       account["name"],
                                       account["balance"]["current"],
                                       account["formatted_account"],
                                       account["connection"]["name"],
                                       account["connection"]["logo"]))

    cur.execute("DELETE FROM accounts")
    cur.executemany("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?)", formatted_accounts)
    con.commit()


def refresh_kiwisavers():
    """Updates KiwiSaver accounts with latest data from Akahu API"""
    manual_refresh()

    accounts = get_request_accounts()
    formatted_accounts = []

    for account in accounts:
        if account["type"] == "KIWISAVER":
            # Only Kernel Wealth supported for KiwiSaver
            if account["connection"]["name"] == "Kernel Wealth":
                formatted_accounts.append((account["_id"],
                                           account["name"],
                                           account["balance"]["current"],
                                           account["connection"]["name"],
                                           account["connection"]["logo"],
                                           account["meta"]["breakdown"]["employer_contributions"],
                                           account["meta"]["breakdown"]["personal_contributions"],
                                           account["meta"]["breakdown"]["tax"],
                                           account["meta"]["breakdown"]["member_tax_credit"],
                                           account["meta"]["breakdown"]["fees"],
                                           account["meta"]["breakdown"]["previous_balance"],
                                           account["meta"]["breakdown"]["withdrawals"],
                                           date.today()))

    cur.execute("DELETE FROM kiwisavers")
    cur.executemany("INSERT INTO kiwisavers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", formatted_accounts)
    con.commit()


def refresh_transactions():
    """Refreshes bank transactions in the database"""
    manual_refresh()

    statement = "SELECT date FROM transactions " \
                "ORDER BY date DESC " \
                "LIMIT 1;"
    res = cur.execute(statement)

    try:
        start = res.fetchone()[0]
    except TypeError:
        start = str(date.today())

    start = start[:10]

    new_transactions = get_transactions_range(start)
    formatted_transactions = []

    for transaction in new_transactions:
        data = [transaction["_id"],
                transaction["_account"],
                transaction["date"],
                transaction["amount"],
                transaction["description"],
                transaction["type"],
                None,
                None,
                date.today()]

        if transaction["type"] in ["EFTPOS", "DEBIT", "DIRECT DEBIT"]:
            try:
                data[6] = transaction["category"]["groups"]["personal_finance"]["name"]
                data[7] = transaction["category"]["name"]
            except:
                data[6] = "Other"
                data[7] = "Other"

        formatted_transactions.append(tuple(data))

    cur.executemany("INSERT OR IGNORE INTO transactions VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", formatted_transactions)
    con.commit()


def refresh_stocks():
    manual_refresh()

    accounts = get_request_accounts()
    formatted_stocks = []

    for account in accounts:
        if account["type"] == "INVESTMENT":
            for stock in account["meta"]["portfolio"]:
                formatted_stocks.append((stock["fund_id"],
                                         stock["name"],
                                         stock["symbol"],
                                         stock["logo"],
                                         stock["shares"],
                                         stock["value"],
                                         stock["returns"]))

    cur.execute("DELETE FROM shares")
    cur.executemany("INSERT INTO shares VALUES(?, ?, ?, ?, ?, ?, ?)", formatted_stocks)
    con.commit()


def get_mtd_transactions(income=False):
    """Gets transactions for the current month from all accounts"""
    statement = "SELECT * FROM transactions " \
                "WHERE STRFTIME('%m', date) = STRFTIME('%m', DATE('now')) " \
                "AND STRFTIME('%Y', date) = STRFTIME('%Y', DATE('now'))"

    if not income:
        statement += " AND amount < 0 AND category IS NOT NULL;"

    res = cur.execute(statement)
    return res.fetchall()


def get_qtd_transactions(income=False):
    """Gets transactions for the current quarter from all accounts"""
    statement = "SELECT * FROM transactions " \
                "WHERE STRFTIME('%Y-%m-%d', date) >= DATE('now', 'start of month', '-3 months') " \
                "AND STRFTIME('%Y-%m-%d', date) < DATE('now', 'start of month')"

    if not income:
        statement += " AND amount < 0 AND category IS NOT NULL;"

    res = cur.execute(statement)
    return res.fetchall()


def get_ytd_transactions(income=False):
    """Gets transactions for the current year from all accounts"""
    statement = "SELECT * FROM transactions " \
                "WHERE STRFTIME('%Y', date) = STRFTIME('%Y', DATE('now')) "

    if not income:
        statement += " AND amount < 0 AND category IS NOT NULL;"

    res = cur.execute(statement)
    return res.fetchall()


def get_month_transactions(income=False):
    """Gets transactions from the past 30 days from all accounts"""
    statement = "SELECT * FROM transactions " \
                "WHERE STRFTIME('%Y-%m-%d', date) >= DATE('now', '-1 month') "

    if not income:
        statement += " AND amount < 0 AND category IS NOT NULL;"

    res = cur.execute(statement)
    return res.fetchall()


def get_quarter_transactions(income=False):
    """Gets transactions from the past 3 months from all accounts"""
    statement = "SELECT * FROM transactions " \
                "WHERE STRFTIME('%Y-%m-%d', date) >= DATE('now', '-3 months') "

    if not income:
        statement += " AND amount < 0 AND category IS NOT NULL;"

    res = cur.execute(statement)
    return res.fetchall()


def get_year_transactions(income=False):
    """Gets transactions from the past 12 months from all accounts"""
    statement = "SELECT * FROM transactions " \
                "WHERE STRFTIME('%Y-%m-%d', date) >= DATE('now', '-1 year') "

    if not income:
        statement += " AND amount < 0 AND category IS NOT NULL;"

    res = cur.execute(statement)
    return res.fetchall()
