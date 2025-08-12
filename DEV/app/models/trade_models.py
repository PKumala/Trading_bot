# app/models/trade_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

# --- ZMIANA: Importujemy 'db' zamiast 'declarative_base' ---
from ..database.database import db

# Nie potrzebujemy już Base = declarative_base()

# --- ZMIANA: Wszystkie modele dziedziczą po db.Model ---
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    # Dodajmy pole na hasło, o którym mówiliśmy wcześniej
    password_hash = db.Column(db.String(128))
    bybit_api_key = db.Column(db.String, nullable=False)
    bybit_api_secret_key = db.Column(db.String, nullable=False)
    enabled_trading = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=1000.0)
    leverage = db.Column(db.Integer, nullable=False, default=10)
    strategies = db.Column(db.JSON, nullable=False, default=lambda: [])

class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_identifier = db.Column(db.String, index=True)
    symbol = db.Column(db.String, index=True)
    trade_type = db.Column(db.String)
    buy_price = db.Column(db.Float)
    order_id = db.Column(db.String, unique=True)
    trade_time = db.Column(db.DateTime)
    signal_time = db.Column(db.DateTime)
    take_profit = db.Column(db.Float, nullable=True)
    stop_loss = db.Column(db.Float, nullable=True)
    strategy = db.Column(db.String(50), nullable=False)

# Jeśli nadal używasz tej tabeli, ją również zaktualizuj
class QtyStorage(db.Model):
    __tablename__ = "qty_storage"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User")