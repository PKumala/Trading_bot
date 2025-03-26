import requests
from config import BYBIT_API_KEY, BYBIT_API_SECRET

BASE_URL = "https://api.bybit.com"

def send_order(symbol, side, price, quantity):
    payload = {
        "symbol": symbol,
        "side": side,
        "price": price,
        "quantity": quantity,
        "api_key": BYBIT_API_KEY
    }
    response = requests.post(f"{BASE_URL}/v2/private/order/create", json=payload)
    return response.json()

def amend_order(order_id, price, quantity):
    payload = {
        "order_id": order_id,
        "price": price,
        "quantity": quantity,
        "api_key": BYBIT_API_KEY
    }
    response = requests.post(f"{BASE_URL}/v2/private/order/replace", json=payload)
    return response.json()
