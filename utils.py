import requests
import logging

BASE_URL = "http://localhost:5001/api"

def fetch_orders(limit=None):
    params = {}
    if limit:
        params["limit"] = limit
    resp = requests.get(f"{BASE_URL}/orders", params=params)
    if resp.status_code != 200:
        logging.error("API fetch failed with status %s", resp.status_code)
        return []
    return resp.json().get("raw_orders", [])

def fetch_order_by_id(order_id):
    resp = requests.get(f"{BASE_URL}/order/{order_id}")
    return resp.json().get("raw_order")
