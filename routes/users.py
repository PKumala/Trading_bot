import uuid
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.database import db
from models.models import User
from uuid import uuid4
from services.security import verify_token, verify_ip
from utils.crypt_key import encrypt_api_key
users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not verify_ip():
        return jsonify({"error": "Unauthorized IP"}), 403

    if not verify_token(data):
        return jsonify({"error": "Unauthorized token"}), 403


    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        bybit_api_key=encrypt_api_key(data["bybit_api_key"]),
        bybit_api_secret_key=encrypt_api_key(data["bybit_api_secret_key"]),
        user_token=uuid4(),
        hashed_password=hashed_password,
        balance=data["balance"],
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successful"}), 201


@users_bp.route("/update_user", methods=["PUT"])
def update_user():
    data = request.get_json()
    if not verify_ip():
        return jsonify({"error": "Unauthorized IP"}), 403

    if not verify_token(data):
        return jsonify({"error": "Unauthorized token"}), 403

    user_token = data.get("user_token")
    if not user_token:
        return jsonify({"error": "Token is invalid"}), 400

    user = db.session.query(User).filter_by(user_token=user_token).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    update_fields = {}

    if "password" in data:
        update_fields["hashed_password"] = generate_password_hash(data["password"])

    if "bybit_api_key" in data:
        update_fields["bybit_api_key"] = encrypt_api_key(data["bybit_api_key"])

    if "bybit_api_secret_key" in data:
        update_fields["bybit_api_secret_key"] = encrypt_api_key(data["bybit_api_secret_key"])

    if "balance" in data:
        update_fields["balance"] = data["balance"]

    for field, value in update_fields.items():
        setattr(user, field, value)

    db.session.commit()

    return jsonify({"message": "User data update successful"}), 200