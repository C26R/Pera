import os
import requests

from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION = os.getenv("AUTHORIZATION")
AKAHU_ID = os.getenv("AKAHU_ID")

url = "https://api.akahu.io/v1"
headers = {
    "Authorization": AUTHORIZATION,
    "X-Akahu-ID": AKAHU_ID
}


def manual_refresh():
    """Requests manual refresh of data to Akahu API"""
    requests.post(f"{url}/refresh", headers=headers)


def get_transactions_range(start, end=date.today() + timedelta(days=1)):
    """Returns transactions for all accounts in given range"""
    transactions = []

    params = {
        "start": start,
        "end": end
    }

    r = requests.get(f"{url}/transactions", headers=headers, params=params)
    data = r.json()

    for transaction in data["items"]:
        transactions.append(transaction)

    while True:
        params = {
            "start": start,
            "end": end,
            "cursor": data["cursor"]["next"]
        }
        r = requests.get(f"{url}/transactions", headers=headers, params=params)
        data = r.json()

        for transaction in data["items"]:
            transactions.append(transaction)

        if data["cursor"]["next"] is None:
            break

    return transactions


def get_request_accounts():
    r = requests.get(f"{url}/accounts", headers=headers)
    data = r.json()

    return data["items"]


