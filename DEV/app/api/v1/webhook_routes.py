import logging
from flask import Blueprint, request, jsonify
from ...services.order_service import OrderProcessingService
from ...services.security_service import verify_ip, verify_token

webhook_bp = Blueprint("webhook_v1", __name__)
logger = logging.getLogger(__name__)

# ... (before_request i logowanie bez zmian) ...
@webhook_bp.before_request
def log_request_info():
    """Loguje każde przychodzące żądanie do tego blueprintu."""
    try:
        data = request.get_data(as_text=True)
        logger.info(f"{request.remote_addr} - {request.method} {request.path} - Data: {data[:200]}...")
    except Exception as e:
        logger.warning(f"Failed to log request data: {e}")

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    if not verify_ip(request):
        return jsonify({"error": "Unauthorized IP"}), 403

    data = request.get_json()
    # if not data or not verify_token(data):
    #     return jsonify({"error": "Invalid or missing token"}), 403

    # --- ZAKTUALIZOWANA WALIDACJA PÓL ---
    required_fields = ["symbol", "order_type", "price", "time", "strategy"]
    if not all(field in data for field in required_fields):
        missing = [field for field in required_fields if field not in data]
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    service = OrderProcessingService()
    results = service.process_webhook_for_all_users(data)

    return jsonify(results), 200

# ... (endpoint /info bez zmian) ...
@webhook_bp.route("/info", methods=["GET"])
def info():
    # if not verify_ip(request):
    #     return jsonify({"error": "Unauthorized IP"}), 403

    client_ip_header = request.headers.get('CF-Connecting-IP', request.remote_addr)
    return jsonify({"client_ip": client_ip_header})