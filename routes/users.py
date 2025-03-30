import uuid
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.database import db
from models.models import User
from uuid import uuid4

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.username} for u in users])


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        bybit_api_key=generate_password_hash(data["bybit_api_key"]),
        bybit_api_secret_key=generate_password_hash(data["bybit_api_secret_key"]),
        user_token=uuid4(),
        hashed_password=hashed_password,
        qty=data["qty"],
    )
    #todo bybit api key szyfrowanie aes
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Użytkownik utworzony"}), 201
