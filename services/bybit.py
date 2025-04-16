import logging
import requests
from pybit.unified_trading import HTTP
import pybit.exceptions

def send_order(symbol, order_type, take_profit, stop_loss, api_key, api_secret_key, qty):
    try:
        order_side = "Buy" if order_type == "Long" else "Sell"
        session = HTTP(
            api_key=api_key,
            api_secret=api_secret_key,
            recv_window=10000,
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
        return response_json

    except Exception as e:
        return {"error": "Request failed", "details": str(e)}, 200

def change_tp_sl(new_stop_loss,new_take_profit, symbol, api_key, api_secret_key):
    try:

        session = HTTP(
            api_key=api_key,
            api_secret=api_secret_key,
        )

        response = session.set_trading_stop(
            category="linear",
            symbol=symbol,
            takeProfit=new_take_profit,
            stopLoss=new_stop_loss,
        )

        response_json = response if isinstance(response, dict) else response.json()
        return response_json


    except Exception as e:
        return {"error": "Amend failed", "details": str(e)}


def position_is_open(api_key, api_secret_key, symbol):
    try:
        session = HTTP(
            api_key=api_key,
            api_secret=api_secret_key,
        )
        response = session.get_positions(
            category="linear",
            symbol=symbol,
        )

        logging.info(f"Response from Bybit API: {response}")

        response_json = response if isinstance(response, dict) else response.json()

        if response_json.get("retCode") != 0:
            logging.error(f"Error in response from Bybit API: {response_json.get('retMsg')}")
            return {"error": "Failed to get position information", "details": response_json.get('retMsg')}

        positions = response_json.get("result", {}).get("list", [])
        if positions:
            position = positions[0]
            if position.get("size", "0") != "0":
                logging.info(f"Position for {symbol} is open with size: {position['size']}")
                return True
            else:
                logging.info(f"Position for {symbol} is closed.")
        else:
            logging.info(f"No position found for {symbol}")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for API key : {str(e)}")
        return {"error": "Request failed", "details": str(e)}
    except pybit.exceptions.FailedRequestError as e:
        logging.error(f"Failed request for user with API key : {str(e)}")
        return {"error": "Unauthorized request, invalid API key", "details": str(e)}
    except Exception as e:
        logging.error(f"Unexpected error for API key: {str(e)}")
        return {"error": "An unexpected error occurred", "details": str(e)}

def get_real_money(api_key, api_secret_key):
    try:
        session = HTTP(
            api_key=api_key,
            api_secret=api_secret_key,
        )
        response = session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT",
        )
        response_json = response if isinstance(response, dict) else response.json()

        return response_json["result"]["list"][0]["totalEquity"]

    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}

def set_leverage(symbol, leverage, api_key, api_secret_key):
    try:
        session = HTTP(
            api_key=api_key,
            api_secret=api_secret_key,
        )
        response = session.set_leverage(
            category="linear",
            symbol=symbol,
            buyLeverage=leverage,
            sellLeverage=leverage,
        )
        response_json = response if isinstance(response, dict) else response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}


def calculate_safe_qty(entry_price, account_balance, price_drop_percent, balance_usage_percent=90):
    entry_price = float(entry_price)
    account_balance = float(account_balance)
    price_drop_percent = float(price_drop_percent)
    balance_usage_percent = float(balance_usage_percent)

    usable_margin = account_balance * (balance_usage_percent / 100)
    qty = usable_margin / (entry_price * price_drop_percent / 100)
    qty = float(qty * 100) / 100
    return qty