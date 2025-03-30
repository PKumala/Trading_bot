from flask import Blueprint, request, jsonify
from services.security import verify_token, verify_ip
from services.bybit import send_order, amend_order
from database_engine import get_db
from models.models import User
from config import Config
from models.models import Trade
webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    if not verify_ip():
        return jsonify({"error": "Unauthorized IP"}), 403

    data = request.get_json()
    if not verify_token(data):
        return jsonify({"error": "Unauthorized token"}), 403

    db = next(get_db())

    symbol = data.get("symbol")
    user_username = data.get("user_username")
    user_token = data.get("user_token")
    is_amend = data.get("isAmend", False)
    time = data.get("time")

    user = db.query(User).filter_by(username=user_username).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    if user.user_token != user_token:
        return jsonify({"error": "Invalid token for user"}), 403

    if is_amend:
        order_id = data.get("order_id")
        take_profit = data.get("new_take_profit")
        stop_loss = data.get("new_stop_loss")

        if not order_id:
            return jsonify({"error": "order_id is required for amend"}), 400

        response = amend_order(order_id, take_profit, stop_loss)
        if response.get("ret_code") == 0:
            return jsonify({"message": "Order amended", "order_id": order_id})
        else:
            return jsonify({"error": "Amend failed", "details": response}), 400

    else:
        if not all([symbol, user_username, user_token, time]):
            return jsonify({"error": "Missing required fields for new order"}), 400

        take_profit = data.get("take_profit")
        stop_loss = data.get("stop_loss")
        order_type = data.get("order_type")


        api_key = user.bybit_api_key
        api_secret_key = user.bybit_api_secret_key
        qty = user.qty

        # response = send_order(symbol, order_type, take_profit, stop_loss, api_key, api_secret_key, qty)
        # if response.get("ret_code") == 0:
        #     # Assuming `Order` is a model you use to store orders in DB
        order = Trade(
            user_identifier=user_username,
            symbol=symbol,
            trade_type=order_type,
            take_profit=take_profit,
            stop_loss=stop_loss,
            trade_time = time,
            status='open',
        )
        #todo dodać sprawdzanie otwartych pozycji
        db.add(order)
        db.commit()
        return "ok"
        #     return jsonify({"message": "Order created", "order": order.to_dict()}), 200
        # else:
        #     return jsonify({"error": "Order creation failed", "details": response}), 400