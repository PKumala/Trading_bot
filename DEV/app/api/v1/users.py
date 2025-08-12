# app/api/v1/users.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from ...database.database import db
from ...models.trade_models import User
from ...utils.crypt_key import encrypt_api_key

users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    # ... (walidacja danych bez zmian) ...
    if not data or not all(
            k in data for k in ['username', 'password', 'bybit_api_key', 'bybit_api_secret_key', 'balance']):
        return jsonify({"error": "Missing required fields"}), 400

    # Ta linia teraz zadziała poprawnie!
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409

    # Alternatywny, nowszy sposób (również zadziała):
    # if db.session.execute(db.select(User).filter_by(username=data["username"])).scalar_one_or_none():
    #     return jsonify({"error": "Username already exists"}), 409

    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        password_hash=data["password"],  # Zapisujemy hasło
        bybit_api_key=encrypt_api_key(data["bybit_api_key"]),
        bybit_api_secret_key=encrypt_api_key(data["bybit_api_secret_key"]),
        balance=float(data["balance"]),
    )

    # ... (logika dodawania do bazy bez zmian) ...
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error while creating user: {e}")
        return jsonify({"error": "Could not create user"}), 500
    finally:
        db.session.close()

    return jsonify({"message": "User created successfully"}), 201