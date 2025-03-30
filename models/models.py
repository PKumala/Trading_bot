from models.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    user_token = db.Column(db.String(255), nullable=False)
    qty = db.Column(db.Float, nullable=False)
    bybit_api_key = db.Column(db.String(255), nullable=True)
    bybit_api_secret_key = db.Column(db.String(255), nullable=True)
    #todo enable trading
    def __repr__(self):
        return f"<User {self.username}>"

class Trade(db.Model):
    __tablename__ = 'trading_db'
    id = db.Column(db.Integer, primary_key=True)
    user_identifier = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)
    buy_price = db.Column(db.Float, nullable=True)
    stop_loss = db.Column(db.Float, nullable=True)
    take_profit = db.Column(db.Float, nullable=True)
    trade_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Trade {self.symbol} - {self.trade_type}>"
