import requests
from flask import json
from pybit.unified_trading import HTTP



def send_order(symbol, order_type, take_profit, stop_loss, api_key, api_secret_key, qty):
    try:
        order_side = "Buy" if order_type == "Long" else "Sell"

        session = HTTP(
            demo=True,
            testnet=True,
            api_key=api_key,
            api_secret=api_secret_key,
        )
        take = round(float(take_profit), 2)
        loss = round(float(stop_loss), 2)

        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=order_side,
            orderType="Market",
            qty=qty,
            takeProfit=take,
            stopLoss=loss,
        )

        response_json = response if isinstance(response, dict) else response.json()
        print(f"Zlecenie {order_side} wysłane: {json.dumps(response_json, indent=4)}")

    except Exception as e:
        print(f"Błąd składania zlecenia: {e}")

def amend_order():
    print()
    #todo amend order
