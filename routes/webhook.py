import logging
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify
from datetime import datetime
from services.security import verify_token, verify_ip
from services.bybit import send_order, calculate_safe_qty, position_is_open
from database_engine import get_db
from models.models import User, Trade
from utils.crypt_key import decrypt_api_key

webhook_bp = Blueprint("webhook", __name__)
logging.basicConfig(level=logging.INFO)
@app.before_request
def log_request_info():
    try:
        data = request.get_data(as_text=True)  # nie używa request.data bezpośrednio
        logging.info(f"{request.remote_addr} - {request.method} {request.path} - {data}")
    except Exception as e:
        logging.warning(f"Request log failed: {e}")
def handle_new_order(data, user, db):
    symbol, order_type, take_profit, stop_loss, time = data.get("symbol"), data.get("order_type"), data.get(
        "take_profit"), data.get("stop_loss"), data.get("time")
    if not all([symbol, order_type, time]):
        return {"error": "Missing required fields for new order"}, 400

    api_key, api_secret = decrypt_api_key(user.bybit_api_key), decrypt_api_key(user.bybit_api_secret_key)

    position_status = position_is_open(api_key, api_secret, "ETHUSDT")
    position_status_on_BTCUSDT = position_is_open(api_key, api_secret, "BTCUSDT")

    if isinstance(position_status, dict) and position_status.get("error"):
        return position_status, 401

    if position_status:
        return {"error": "Position is already open"}, 400

    if isinstance(position_status_on_BTCUSDT, dict) and position_status_on_BTCUSDT.get("error"):
        return position_status_on_BTCUSDT, 401

    if position_status_on_BTCUSDT:
        return {"error": "Position is already open"}, 400

    entry_price = data["price"]
    qty = calculate_safe_qty(entry_price, user.balance, 7, 100)
    if symbol == "ETHUSDT":
        qty = round(qty, 2)
    else:
        qty = round(qty, 3)

    response = send_order(symbol, order_type, take_profit, stop_loss, api_key, api_secret, qty)

    if isinstance(response, dict) and response.get("retCode") == 0:
        db.add(Trade(
            user_identifier=user.username,
            symbol=symbol,
            trade_type=order_type,
            take_profit=take_profit,
            stop_loss=stop_loss,
            buy_price=data["price"],
            trade_time=datetime.now(),
            signal_time=datetime.now(),
            order_id=response["result"].get("orderId")
        ))
        db.commit()

    return response, 200

def handle_user_order(data, user, db):

    handler = handle_new_order if not data.get("isAmend", "false") else handle_new_order
    response, status_code = handler(data, user, db)
    return {"user": user.username, "response": response, "status_code": status_code}


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    if not verify_ip():
        return jsonify({"error": "Unauthorized IP"}), 403

    data = request.get_json()
    if not verify_token(data):
        return jsonify({"error": "Unauthorized token"}), 403

    db = next(get_db())

    active_users = db.query(User).filter_by(enabled_trading=True).all()
    if not active_users:
        return jsonify({"message": "No active traders"}), 200

    responses = []


    with ThreadPoolExecutor(max_workers=len(active_users)) as executor:
        futures = []
        for user in active_users:
            futures.append(executor.submit(handle_user_order, data, user, db))


        for future in futures:
            response = future.result()
            if isinstance(response['response'], dict) and response['response'].get("error"):
                logging.error(f"Error processing order for user {response['user']}: {response['response']}")
            responses.append({"user": response.get("user"), "response": response.get("response"),
                              "status": response.get("status_code")})

    return jsonify(responses), 200

@webhook_bp.route("/info", methods=["GET"])
def info():
    if not verify_ip():
        return jsonify({"error": "Unauthorized IP"}), 403


    client_ip = request.headers.get('CF-Connecting-IP')
    client_ip_v2 = request.remote_addr

    return jsonify({"client_ip_cloundflare": client_ip,"client_ip": client_ip_v2})
