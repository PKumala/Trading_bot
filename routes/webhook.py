from flask import Blueprint, request, jsonify
from services.security import verify_token, verify_ip
from services.bybit import send_order, amend_order
from database import get_db
from models.orders import Order
from config import ENABLE_BYBIT_TRADING

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    if not verify_ip():
        return jsonify({"error": "Unauthorized IP"}), 403

    data = request.get_json()
    if not verify_token(data):
        return jsonify({"error": "Unauthorized token"}), 403

    if not ENABLE_BYBIT_TRADING:
        return jsonify({"error": "Trading is disabled"}), 403

    db = next(get_db())

    is_amend = data.get("isAmend", False)
    order_id = data.get("order_id")
    symbol = data.get("symbol")
    side = data.get("side")
    price = data.get("price")
    quantity = data.get("quantity")

    if is_amend:
        if not order_id:
            return jsonify({"error": "order_id is required for amend"}), 400
        response = amend_order(order_id, price, quantity)
        if response.get("ret_code") == 0:
            return jsonify({"message": "Order amended", "order_id": order_id})
        else:
            return jsonify({"error": "Amend failed", "details": response}), 400
    else:
        if not all([symbol, side, price, quantity]):
            return jsonify({"error": "Missing required fields for new order"}), 400

        response = send_order(symbol, side, float(price), float(quantity))
        if response.get("ret_code") == 0:
            order = Order(symbol=symbol, side=side, price=price, quantity=quantity, status="filled")
            db.add(order)
            db.commit()
            return jsonify({"message": "Order placed", "order_id": response["result"]["order_id"]})
        else:
            return jsonify({"error": "Order failed", "details": response}), 400
